"""Safety and recovery checks for the uploader; never contact Zenodo."""
import copy
import contextlib
import hashlib
import importlib.util
import io
from pathlib import Path
import tempfile
import threading
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location("zenodo_upload", Path(__file__).resolve().parents[1] / "scripts/zenodo_upload.py")
uploader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(uploader)


class InstantStop(threading.Event):
    def wait(self, timeout=None):
        return self.is_set()


class FakeClient:
    def __init__(self, behaviour="success"):
        self.behaviour = behaviour
        self.puts = 0
        self.value = {"id": uploader.RECORD, "state": "unsubmitted", "submitted": False, "files": [], "links": {"bucket": "https://zenodo.org/api/files/12345678-1234-1234-1234-123456789012"}}

    def draft(self):
        return copy.deepcopy(self.value)

    def upload(self, bucket, file, progress):
        self.puts += 1
        if self.behaviour == "quota":
            raise uploader.APIError(413)
        if self.behaviour == "disconnect" and self.puts == 1:
            raise OSError("simulated disconnect")
        content = file.read_bytes()
        checksum = hashlib.md5(content).hexdigest()
        self.value["files"] = [{"filename": file.name, "filesize": len(content), "checksum": checksum}]
        if self.behaviour == "lost_ack":
            raise OSError("server accepted the file but the reply was lost")
        return {"key": file.name, "size": len(content), "checksum": "md5:" + checksum}


class UploaderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.path = self.directory / "sample.zip"
        self.path.write_bytes(b"frozen scientific output\n")
        self.item = {"path": self.path, "size": self.path.stat().st_size, "sha256": hashlib.sha256(self.path.read_bytes()).hexdigest()}
        self.stop = InstantStop()
        self.cache = uploader.HashCache(self.directory / "hashes.json", self.stop)

    def run_upload(self, client):
        uploader.upload_one(self.path.name, self.item, client, self.cache, self.stop)

    def test_second_run_skips_the_verified_file(self):
        client = FakeClient()
        self.run_upload(client)
        self.run_upload(client)
        self.assertEqual(client.puts, 1)
        self.assertEqual(uploader.classify({self.path.name: self.item}, client.draft(), self.cache), ([self.path.name], []))

    def test_lost_acknowledgement_does_not_duplicate_upload(self):
        client = FakeClient("lost_ack")
        self.run_upload(client)
        self.assertEqual(client.puts, 1)

    def test_failed_file_is_retried_from_the_start(self):
        client = FakeClient("disconnect")
        self.run_upload(client)
        self.assertEqual(client.puts, 2)

    def test_remote_conflict_stops_without_overwrite(self):
        client = FakeClient()
        client.value["files"] = [{"filename": self.path.name, "filesize": self.item["size"], "checksum": "0" * 32}]
        with self.assertRaises(uploader.UploadError):
            self.run_upload(client)
        self.assertEqual(client.puts, 0)

    def test_local_same_size_corruption_is_rejected(self):
        self.cache.get(self.item)
        self.path.write_bytes(b"x" * self.item["size"])
        with self.assertRaises(uploader.UploadError):
            self.cache.get(self.item)

    def test_published_record_cannot_receive_uploads(self):
        client = FakeClient()
        client.value.update(submitted=True, state="done")
        with self.assertRaises(uploader.UploadError):
            self.run_upload(client)
        self.assertEqual(client.puts, 0)

    def test_quota_error_is_not_retried(self):
        client = FakeClient("quota")
        with self.assertRaises(uploader.APIError):
            self.run_upload(client)
        self.assertEqual(client.puts, 1)

    def test_cancelled_run_does_not_start_upload(self):
        client = FakeClient()
        self.stop.set()
        with self.assertRaises(uploader.Cancelled):
            self.run_upload(client)
        self.assertEqual(client.puts, 0)

    def test_credential_cannot_follow_foreign_bucket(self):
        for url in ("http://zenodo.org/api/files/123", "https://zenodo.org.attacker.test/api/files/123", "https://zenodo.org/api/files/123?token=x"):
            with self.assertRaises(uploader.UploadError):
                uploader.bucket_path(url)

    def test_publication_and_deletion_are_not_supported(self):
        client = uploader.Client("not-a-real-credential", self.stop)
        for method, path in [("POST", uploader.API_PATH + "/actions/publish"), ("DELETE", "/api/files/example")]:
            with self.assertRaises(uploader.UploadError):
                client.request(method, path)

    def test_extra_remote_file_requires_review(self):
        client = FakeClient()
        client.value["files"] = [{"filename": "unexpected.pdf", "filesize": 10, "checksum": "0" * 32}]
        with self.assertRaises(uploader.UploadError):
            uploader.classify({self.path.name: self.item}, client.draft(), self.cache)

    def test_transport_error_reports_type_without_sensitive_message(self):
        secret = "sensitive request content must not appear"
        self.assertNotIn(secret, uploader.connection_reason(ConnectionResetError(54, secret)))
        self.assertIn("errno=54", uploader.connection_reason(ConnectionResetError(54, secret)))
        self.assertIn("TimeoutError", uploader.connection_reason(TimeoutError(secret)))

    def test_last_failed_attempt_preserves_error_type(self):
        client = FakeClient()
        client.upload = mock.Mock(side_effect=TimeoutError("sensitive request content"))
        with self.assertRaisesRegex(uploader.UploadError, "TimeoutError") as caught:
            uploader.upload_one(self.path.name, self.item, client, self.cache, self.stop, attempts=1)
        self.assertNotIn("sensitive request content", str(caught.exception))

    def test_upload_has_longer_timeout_and_always_closes_connection(self):
        response = mock.Mock(status=200)
        response.read.return_value = b'{}'
        connection = mock.Mock()
        connection.getresponse.return_value = response
        client = uploader.Client("not-a-real-credential", self.stop)
        with mock.patch.object(uploader.http.client, "HTTPSConnection", return_value=connection) as factory:
            client.request("GET", uploader.API_PATH)
            self.assertEqual(factory.call_args.kwargs["timeout"], 60)
            client.upload(FakeClient().value["links"]["bucket"], self.path, None)
            self.assertEqual(factory.call_args.kwargs["timeout"], 300)
            self.assertEqual(connection.close.call_count, 2)
            connection.send.side_effect = uploader.Cancelled("Subida detenida.")
            with self.assertRaises(uploader.Cancelled):
                client.upload(FakeClient().value["links"]["bucket"], self.path, None)
            self.assertEqual(connection.close.call_count, 3)

    def main_fixture(self, client):
        files = {}
        # Deliberately supply the largest first.
        for name, size in [("large.zip", 300), ("small.zip", 100), ("medium.zip", 200)]:
            path = self.directory / name
            path.write_bytes(b"x" * size)
            files[name] = {"path": path, "size": size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        stack = contextlib.ExitStack()
        self.addCleanup(stack.close)
        stack.enter_context(mock.patch.object(uploader, "STATE_DIR", self.directory))
        stack.enter_context(mock.patch.object(uploader, "inventory", return_value=files))
        stack.enter_context(mock.patch.object(uploader, "load_token", return_value="fake"))
        stack.enter_context(mock.patch.object(uploader, "Client", return_value=client))
        stack.enter_context(mock.patch.object(uploader.signal, "signal"))
        return files

    def test_main_uploads_serially_smallest_first(self):
        client = FakeClient()
        files = self.main_fixture(client)
        order = []
        main_thread = threading.get_ident()
        original_upload = client.upload

        def upload(bucket, file, progress):
            self.assertEqual(threading.get_ident(), main_thread)
            self.assertEqual(len(client.value["files"]), len(order))
            saved = copy.deepcopy(client.value["files"])
            result = original_upload(bucket, file, progress)
            client.value["files"] = saved + client.value["files"]
            order.append(file.name)
            return result

        client.upload = upload
        self.assertEqual(uploader.main([]), 0)
        self.assertEqual(order, sorted(files, key=lambda name: files[name]["size"]))

    def test_failure_keeps_completed_file_and_does_not_start_later_file(self):
        client = FakeClient()
        self.main_fixture(client)
        original_upload = client.upload
        started = []

        def upload(bucket, file, progress):
            started.append(file.name)
            if file.name == "medium.zip":
                raise uploader.APIError(413)
            return original_upload(bucket, file, progress)

        client.upload = upload
        with self.assertRaises(uploader.APIError):
            uploader.main([])
        self.assertEqual(started, ["small.zip", "medium.zip"])
        status = uploader.json.loads((self.directory / "status.json").read_text())
        self.assertEqual(status["complete"], ["small.zip"])
        self.assertEqual(set(status["pending"]), {"medium.zip", "large.zip"})

    def test_parallel_setting_is_rejected_before_network_access(self):
        with mock.patch.object(uploader, "Client") as client, contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                uploader.main(["--workers", "2"])
            client.assert_not_called()


if __name__ == "__main__":
    unittest.main()
