"""Small terminal interface; status never starts a download."""
import argparse
from contextlib import contextmanager
import fcntl
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys

from dotenv import dotenv_values

from .legacy import LegacyIndex, build_index
from .runner import ApiClient, Runner
from .store import utcnow, write_json

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / 'data/corpus_500k'
LEGACY_SOURCE = Path('/Users/alejandrotreny/Workspace/Mapping-Science/data/processed/works_text_2000_2024_400py.parquet')
LEGACY_INDEX = ROOT / 'data/cache/legacy_index.sqlite'


def read_config(path):
    config = json.loads(Path(path).read_text())
    for name in ('base_target', 'extra_target', 'seed', 'block_size', 'per_page', 'min_abstract_words'):
        if type(config.get(name)) is not int or config[name] < 0:
            raise ValueError(f'Configuración inválida: {name}')
    if not 1 <= config['per_page'] <= 100 or not 1 <= config['block_size'] <= 10000:
        raise ValueError('El tamaño de página o bloque no es válido para OpenAlex')
    if not config['base_target'] or config['min_abstract_words'] != 50:
        raise ValueError('La base y el filtro deben respetar el protocolo')
    if config.get('field_ids') != list(range(11, 37)) or config.get('period_starts') != list(range(2000, 2025, 5)):
        raise ValueError('Deben conservarse los 26 Fields y los cinco períodos del protocolo')
    if (config.get('year_min'), config.get('year_max'), config.get('schema_version')) != (2000, 2024, 1):
        raise ValueError('Versión o ventana temporal incompatible con el protocolo')
    for name in ('request_delay', 'retry_seconds'):
        if not isinstance(config.get(name), (int, float)) or config[name] < 0:
            raise ValueError(f'Configuración inválida: {name}')
    return config


@contextmanager
def writer_lock(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    with (output / 'download.lock').open('a+') as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError('Ya hay una descarga abierta en esta carpeta. Usa ./download.sh status.') from None
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def show_status(output):
    output = Path(output)
    if not (output / 'state.sqlite').exists():
        print('La descarga todavía no se ha iniciado. Para empezar: ./download.sh')
        return
    db = sqlite3.connect((output / 'state.sqlite').resolve().as_uri() + '?mode=ro', uri=True)
    try:
        count = dict(db.execute('SELECT cohort,count(*) FROM works GROUP BY cohort'))
        config = json.loads(db.execute('SELECT value FROM meta WHERE key=\'config\'').fetchone()[0])
        complete = db.execute("SELECT 1 FROM meta WHERE key='complete'").fetchone() is not None
        pages = db.execute('SELECT count(*) FROM pages').fetchone()[0]
        active = db.execute("SELECT id,n_pages FROM blocks WHERE status='downloading' ORDER BY id LIMIT 1").fetchone()
    finally:
        db.close()
    running = False
    lock_path = output / 'download.lock'
    if lock_path.exists():
        with lock_path.open('r') as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_SH | fcntl.LOCK_NB)
                fcntl.flock(handle, fcntl.LOCK_UN)
            except BlockingIOError:
                running = True
    total = sum(count.values()); target = config['base_target'] + config['extra_target']
    state = 'TERMINADA' if complete else 'EN MARCHA' if running else 'PAUSADA'
    print(f'{state} · {total:,} de {target:,} trabajos válidos ({total/target:.1%}).')
    print(f"Base: {count.get('base', 0):,}/{config['base_target']:,}. Complemento: {count.get('extra', 0):,}/{config['extra_target']:,}.")
    print(f'{pages:,} páginas guardadas. Los trabajos se incorporan al terminar cada bloque.')
    if active:
        print(f'Bloque pendiente: {active[0]}.')
    progress_path = output / 'progress.json'
    if progress_path.exists():
        progress = json.loads(progress_path.read_text())
        print(f"Última actividad: {progress['updated_at']} · {progress['phase']}.")
    print(f'Carpeta: {output.resolve()}')
    if not running and not complete:
        print('Para continuar, usa el mismo comando con el que empezaste.')


def get_key():
    key = os.environ.get('OPENALEX_API_KEY')
    if not key:
        for env_path in (ROOT / '.env', LEGACY_SOURCE.parents[2] / '.env'):
            if env_path.exists():
                key = dotenv_values(env_path).get('OPENALEX_API_KEY')
                if key:
                    break
    if not key:
        raise ValueError('No encuentro la clave de OpenAlex ya configurada. Pide revisar su ubicación; no la pegues en el comando.')
    return key


def main(argv=None):
    parser = argparse.ArgumentParser(description='Descarga de OpenAlex con pausa y reanudación.')
    parser.add_argument('action', nargs='?', default='start', choices=['start', 'status', 'prepare-cache'])
    parser.add_argument('--config', type=Path, default=ROOT / 'config/corpus.json')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--max-pages', type=int, help='Límite de páginas nuevas, solo para comprobar la reanudación.')
    args = parser.parse_args(argv)
    runner = api = legacy = None
    try:
        if args.action == 'status':
            show_status(args.output)
            return 0
        if args.action == 'prepare-cache':
            with writer_lock(LEGACY_INDEX.parent):
                build_index(LEGACY_SOURCE, LEGACY_INDEX, lambda msg: print(msg, flush=True))
            return 0
        config = read_config(args.config)
        if args.max_pages is not None and args.max_pages < 1:
            raise ValueError('--max-pages debe ser un número positivo')
        if args.output.resolve() == DEFAULT_OUTPUT.resolve() and (config['base_target'], config['extra_target']) != (400000, 100000):
            raise ValueError('Las pruebas pequeñas deben guardarse en otra carpeta; no en la descarga definitiva.')
        key = get_key()
        legacy = LegacyIndex(LEGACY_INDEX, LEGACY_SOURCE)
        with writer_lock(args.output):
            api = ApiClient(key)
            runner = Runner(args.output, config, api, report=lambda msg: print(msg, flush=True), legacy=legacy)
            source_hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in sorted((ROOT / 'sos_download').glob('*.py'))}
            frozen = runner.store.get_meta('implementation')
            if frozen and frozen != source_hashes:
                raise ValueError('El programa cambió desde que empezó esta descarga. Pide revisar el cambio antes de continuar.')
            runner.store.set_meta('implementation', source_hashes)
            runner.store.set_meta('legacy_source', legacy.source)
            print('Preparación: 400.000 base + 100.000 complemento.' if config['base_target'] == 400000 else 'Prueba pequeña; separada de la descarga definitiva.', flush=True)
            print('Ctrl+C pausa. El mismo comando continúa. Mantén esta terminal abierta.', flush=True)
            write_json(args.output / 'run.json', dict(pid=os.getpid(), started_at=utcnow(), implementation=source_hashes))
            try:
                runner.run(max_pages=args.max_pages)
            except KeyboardInterrupt:
                runner.status('pausado por el usuario', message='Avance guardado. Continúa con el mismo comando.')
                return 130
            except Exception as error:
                # No traceback, URL or network exception body can expose the API key.
                runner.status('pausado por un error', error_type=type(error).__name__)
                raise
        return 0
    except KeyboardInterrupt:
        print('\nPausado. Puedes repetir el mismo comando.', flush=True)
        return 130
    except (ValueError, FileNotFoundError) as error:
        print(f'No se ha continuado: {error}', file=sys.stderr)
        return 1
    except Exception as error:
        print(f'No se ha continuado ({type(error).__name__}). El avance guardado se conserva; pide revisar esta descarga.', file=sys.stderr)
        return 1
    finally:
        if runner:
            runner.close()
        if api:
            api.close()
        if legacy:
            legacy.close()


if __name__ == '__main__':
    sys.exit(main())
