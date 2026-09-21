#!/usr/bin/env python3
"""Upload the frozen 32-file release to its existing Zenodo draft.

Only GET and bucket PUT are used. No publication, deletion or metadata editing.
The macOS Keychain holds the credential; state contains only file fingerprints.
Uses Python's standard library. Interrupted files restart from byte zero.
"""
import argparse
import fcntl
import hashlib
import http.client
import json
import os
from pathlib import Path
import re
import signal
import ssl
import subprocess
import sys
import threading
import time
from urllib.parse import quote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
RECORD = 22863543
SERVICE = "shape-of-science-zenodo-22863543"
API_PATH = f"/api/deposit/depositions/{RECORD}"
PINNED = {
    "UPLOAD_FILES.txt": "fa48d04489839eb2b1c49fe6a62236cc46aa6438f45a2a542d84ea510c1daace",
    "SHA256SUMS": "52853f87584f2bfd4980adf351ec34613bce467dec5f2fc4d16f02a4d6855931",
}
STATE_DIR = ROOT / "data/zenodo_upload_v1"
OUTPUT_LOCK = threading.Lock()
UPLOAD_TIMEOUT = 300


class UploadError(Exception):
    pass


class Cancelled(UploadError):
    pass


class APIError(UploadError):
    def __init__(self, status, retry_after=0):
        self.status = status
        self.retry_after = retry_after
        reasons = {401: "clave rechazada", 403: "sin permiso de escritura o acceso", 409: "conflicto en el borrador", 413: "cuota o tamaño excedidos", 429: "límite temporal de peticiones"}
        super().__init__(f"Zenodo respondió HTTP {status}: {reasons.get(status, 'petición no completada')}.")

    @property
    def retryable(self):
        return self.status in {408, 425, 429, 500, 502, 503, 504}


def say(message):
    with OUTPUT_LOCK:
        print(message, flush=True)


def connection_reason(error):
    """Report useful transport details without logging request/credential text."""
    if isinstance(error, TimeoutError):
        return "Tiempo de espera de red agotado (TimeoutError)."
    number = getattr(error, "errno", None)
    detail = f", errno={number}" if isinstance(number, int) else ""
    return f"Conexión interrumpida ({type(error).__name__}{detail})."


def atomic_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
    temporary.replace(path)


def fingerprint(path):
    stat = path.stat()
    return [stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns, stat.st_ino]


def inventory(directory, pinned=PINNED):
    for name, digest in pinned.items():
        if hashlib.sha256((directory / name).read_bytes()).hexdigest() != digest:
            raise UploadError(f"Cambió {name}. Este script corresponde al paquete congelado del 21-09-2026.")
    files = {}
    for line in (directory / "UPLOAD_FILES.txt").read_text().splitlines():
        match = re.fullmatch(r"\s*(\d+)\s+([A-Za-z0-9_.-]+)", line)
        if match:
            size, name = int(match[1]), match[2]
            if name in files or name in {".", ".."}:
                raise UploadError("Lista de subida ambigua.")
            files[name] = {"path": directory / name, "size": size}
    if len(files) != 32 or sum(f["size"] for f in files.values()) != 51186372854:
        raise UploadError("La lista no corresponde a los 32 archivos previstos.")
    present = {p.name for p in directory.iterdir()}
    if set(files) - present:
        raise UploadError("Faltan archivos de la entrega. No se subirá nada.")
    if present - set(files):
        say("Se omiten archivos fuera de la lista: " + ", ".join(sorted(present - set(files))))
    hashes = {}
    for line in (directory / "SHA256SUMS").read_text().splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9_.-]+)", line)
        if not match or match[2] in hashes:
            raise UploadError("SHA256SUMS no tiene el formato esperado.")
        hashes[match[2]] = match[1]
    if set(hashes) != set(files) - set(pinned):
        raise UploadError("Las huellas no cubren el paquete previsto.")
    for name, item in files.items():
        if item["path"].is_symlink() or not item["path"].is_file() or item["path"].stat().st_size != item["size"]:
            raise UploadError(f"Archivo local ausente, enlazado o de otro tamaño: {name}")
        item["sha256"] = pinned.get(name, hashes.get(name))
    return files


def load_token():
    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        try:
            result = subprocess.run(["/usr/bin/security", "find-generic-password", "-a", "zenodo.org", "-s", SERVICE, "-w"], capture_output=True, text=True, timeout=30)
            token = result.stdout.strip() if result.returncode == 0 else ""
        except (OSError, subprocess.TimeoutExpired):
            token = ""
    if not token or any(c.isspace() for c in token):
        raise UploadError("No se pudo leer la clave del Llavero. Desbloquea el Llavero de inicio de sesión o define ZENODO_TOKEN.")
    return token


def bucket_path(url):
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "zenodo.org" or parsed.query or parsed.fragment or not re.fullmatch(r"/api/files/[0-9a-f-]{36}", parsed.path):
        raise UploadError("Zenodo devolvió un destino de archivos inesperado.")
    return parsed.path


def remote_files(draft):
    if draft.get("id") != RECORD or draft.get("submitted") is not False or draft.get("state") != "unsubmitted":
        raise UploadError("El registro no es el borrador sin publicar previsto. No se modifica.")
    result = {}
    for item in draft.get("files", []):
        name = item.get("filename") or item.get("key")
        if not name or name in result:
            raise UploadError("Lista remota ambigua.")
        result[name] = item
    return result


def same_remote(remote, local):
    checksum = str(remote.get("checksum", "")).removeprefix("md5:")
    size = int(remote.get("filesize", remote.get("size", -1)))
    return size == local["size"] and checksum == local["md5"]


class Client:
    def __init__(self, token, stop):
        self.token, self.stop = token, stop
        self.context = ssl.create_default_context()

    def request(self, method, path, file=None, progress=None):
        if method not in {"GET", "PUT"} or (method == "GET" and path != API_PATH) or (method == "PUT" and not path.startswith("/api/files/")):
            raise UploadError("Operación fuera del alcance del cargador.")
        connection = http.client.HTTPSConnection("zenodo.org", timeout=UPLOAD_TIMEOUT if file is not None else 60, context=self.context)
        try:
            if self.stop.is_set():
                raise Cancelled("Subida detenida.")
            headers = {"Authorization": "Bearer " + self.token, "Accept": "application/json", "User-Agent": "ShapeOfScienceUploader/1.0"}
            if file is None:
                connection.request(method, path, headers=headers)
            else:
                size = file.stat().st_size
                headers.update({"Content-Length": str(size), "Content-Type": "application/octet-stream"})
                connection.putrequest(method, path)
                for key, value in headers.items():
                    connection.putheader(key, value)
                connection.endheaders()
                sent = 0
                with file.open("rb") as stream:
                    while block := stream.read(1024 * 1024):
                        if self.stop.is_set():
                            raise Cancelled("Subida detenida.")
                        connection.send(block)
                        sent += len(block)
                        if progress:
                            progress(sent, size)
                if sent != size:
                    raise UploadError("El archivo cambió de tamaño durante el envío.")
            response = connection.getresponse()
            raw = response.read(2 * 1024 * 1024 + 1)
            if not 200 <= response.status < 300:
                retry = response.getheader("Retry-After", "0")
                raise APIError(response.status, min(float(retry), 300) if retry.isdigit() else 0)
            if len(raw) > 2 * 1024 * 1024:
                raise UploadError("Respuesta API inesperadamente grande.")
            try:
                return json.loads(raw)
            except (ValueError, UnicodeError):
                raise UploadError("Zenodo devolvió una respuesta que no es JSON.") from None
        finally:
            connection.close()

    def draft(self):
        for attempt in range(5):
            try:
                return self.request("GET", API_PATH)
            except APIError as error:
                if not error.retryable or attempt == 4:
                    raise
                delay = max(error.retry_after, 2 ** attempt)
            except (OSError, http.client.HTTPException):
                if attempt == 4:
                    raise UploadError("No se pudo consultar el borrador tras cinco intentos.") from None
                delay = 2 ** attempt
            if self.stop.wait(delay):
                raise Cancelled("Consulta detenida.")

    def upload(self, bucket, file, progress):
        return self.request("PUT", bucket_path(bucket) + "/" + quote(file.name, safe=""), file, progress)


class HashCache:
    def __init__(self, path, stop):
        self.path, self.stop, self.lock = path, stop, threading.Lock()
        self.entries = json.loads(path.read_text()) if path.exists() else {}

    def get(self, item):
        path = item["path"]
        stamp = fingerprint(path)
        with self.lock:
            saved = self.entries.get(str(path))
        if saved and saved["fingerprint"] == stamp and saved["sha256"] == item["sha256"]:
            return saved
        if item["size"] > 100_000_000:
            say(f"Comprobando archivo local: {path.name} ({item['size'] / 1e9:.2f} GB)...")
        sha, md5 = hashlib.sha256(), hashlib.md5()
        with path.open("rb") as stream:
            while block := stream.read(4 * 1024 * 1024):
                if self.stop.is_set():
                    raise Cancelled("Comprobación detenida.")
                sha.update(block)
                md5.update(block)
        if fingerprint(path) != stamp or sha.hexdigest() != item["sha256"]:
            raise UploadError(f"El archivo cambió o no coincide con la huella congelada: {path.name}")
        value = {"fingerprint": stamp, "size": item["size"], "sha256": sha.hexdigest(), "md5": md5.hexdigest()}
        with self.lock:
            self.entries[str(path)] = value
            atomic_json(self.path, self.entries)
        return value


def classify(files, draft, cache):
    remote = remote_files(draft)
    extras = set(remote) - set(files)
    if extras:
        raise UploadError("Hay archivos remotos fuera de la entrega: " + ", ".join(sorted(extras)))
    complete = []
    for name, uploaded in remote.items():
        local = cache.get(files[name])
        if not same_remote(uploaded, local):
            raise UploadError(f"El archivo remoto difiere del local: {name}. Se detiene sin sobrescribirlo.")
        complete.append(name)
    pending = [name for name in files if name not in remote]
    return sorted(complete), pending


def upload_one(name, item, client, cache, stop, attempts=5):
    local = cache.get(item)
    for attempt in range(attempts):
        if stop.is_set():
            raise Cancelled("Subida detenida.")
        draft = client.draft()
        remote = remote_files(draft)
        if name in remote:
            if not same_remote(remote[name], local):
                raise UploadError(f"Conflicto en {name}; no se sobrescribe.")
            say(f"Verificado, ya estaba completo: {name}")
            return
        if fingerprint(item["path"]) != local["fingerprint"]:
            raise UploadError(f"El archivo local cambió después de comprobarlo: {name}")
        started, last_progress = time.monotonic(), [0.0]
        say(f"Subiendo {name}: {item['size'] / 1e9:.3f} GB (intento {attempt + 1}/{attempts})")

        def progress(sent, total):
            now = time.monotonic()
            if now - last_progress[0] >= 10 or sent == total:
                speed = sent / max(now - started, 0.001)
                remaining = (total - sent) / max(speed, 1) / 60
                say(f"  {name}: {sent / total:.1%} · {speed / 1e6:.2f} MB/s · quedan ~{remaining:.0f} min")
                last_progress[0] = now

        try:
            result = client.upload(draft["links"]["bucket"], item["path"], progress)
            if fingerprint(item["path"]) != local["fingerprint"] or not same_remote(result, local):
                raise UploadError(f"No coincide la comprobación final de {name}. Se detiene.")
            say(f"Completado y verificado: {name}")
            return
        except APIError as error:
            if not error.retryable:
                raise
            delay = max(error.retry_after, min(2 ** (attempt + 1), 30))
            reason = str(error)
        except (OSError, http.client.HTTPException) as error:
            delay, reason = min(2 ** (attempt + 1), 30), connection_reason(error)
        # Reconcile a lost acknowledgement before attempting another PUT.
        remote = remote_files(client.draft())
        if name in remote:
            if same_remote(remote[name], local):
                say(f"Completado y verificado tras recuperar la conexión: {name}")
                return
            raise UploadError(f"Zenodo conserva una copia distinta de {name}; no se sobrescribe.")
        if attempt == attempts - 1:
            raise UploadError(f"{name}: {reason} Se agotaron los {attempts} intentos. Vuelve a ejecutar el comando.")
        say(f"{name}: {reason} Nuevo intento en {delay:.0f} s; este archivo empezará desde cero.")
        if stop.wait(delay):
            raise Cancelled("Subida detenida.")


def save_status(complete, pending, files):
    atomic_json(STATE_DIR / "status.json", {"record": RECORD, "checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "complete": sorted(complete), "pending": pending, "remaining_bytes": sum(files[name]["size"] for name in pending), "published": False})


def main(argv=None):
    parser = argparse.ArgumentParser(description="Subir los archivos pendientes al borrador Zenodo 22863543.")
    parser.add_argument("--status", action="store_true", help="Comprobar lo ya subido y mostrar lo pendiente, sin subir.")
    parser.add_argument("--only", metavar="ARCHIVO", help="Subir solo este archivo de la lista (útil para una prueba pequeña).")
    parser.add_argument("--workers", type=int, choices=[1], default=1, help="Solo 1: las subidas paralelas pueden bloquearse en Zenodo.")
    args = parser.parse_args(argv)
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with (STATE_DIR / "upload.lock").open("a") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise UploadError("Ya hay otra instancia de este cargador en marcha.") from None
        stop = threading.Event()
        def interrupt(signum, frame):
            stop.set()
            raise Cancelled("Subida detenida.")
        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, interrupt)
        files = inventory(ROOT / "output/zenodo")
        if args.only and args.only not in files:
            raise UploadError("El archivo solicitado no pertenece a la entrega.")
        client, cache = Client(load_token(), stop), HashCache(STATE_DIR / "hashes.json", stop)
        draft = client.draft()
        complete, pending = classify(files, draft, cache)
        remaining = sum(files[name]["size"] for name in pending)
        say(f"Zenodo {RECORD}: {len(complete)}/32 archivos completos y verificados; faltan {len(pending)} ({remaining / 1e9:.2f} GB).")
        for name in sorted(pending, key=lambda name: files[name]["size"]):
            say(f"  Pendiente: {name} ({files[name]['size'] / 1e9:.3f} GB)")
        save_status(complete, pending, files)
        if args.status:
            return 0
        selected = [name for name in pending if args.only is None or name == args.only]
        selected.sort(key=lambda name: files[name]["size"])
        if selected:
            say(f"Archivos a subir: {len(selected)}; una sola conexión, de menor a mayor tamaño. Ctrl+C para detener; repite el comando para continuar.")
            for name in selected:
                upload_one(name, files[name], client, cache, stop)
                complete.append(name)
                pending.remove(name)
                save_status(complete, pending, files)
        # Listings can lag briefly behind a successful bucket response.
        for attempt in range(6):
            complete, pending = classify(files, client.draft(), cache)
            if not set(selected).intersection(pending):
                break
            if stop.wait(2):
                raise Cancelled("Verificación detenida.")
        else:
            raise UploadError("La lista remota aún no confirma todos los envíos. Ejecuta --status para volver a comprobar.")
        remaining = sum(files[name]["size"] for name in pending)
        save_status(complete, pending, files)
        say(f"Verificación final: {len(complete)}/32 completos; quedan {len(pending)} ({remaining / 1e9:.2f} GB).")
        if not pending:
            say(f"Carga terminada. Revisa el borrador y pulsa Publish cuando esté listo: https://zenodo.org/uploads/{RECORD}")
        say("El registro sigue como borrador. El script no publica.")
        return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Cancelled as error:
        say(str(error) + " Repite el mismo comando para continuar.")
        sys.exit(130)
    except (UploadError, OSError, ValueError) as error:
        # No HTTP bodies, request headers or credential values are logged.
        say("ERROR: " + (str(error) if isinstance(error, UploadError) else type(error).__name__))
        sys.exit(1)
