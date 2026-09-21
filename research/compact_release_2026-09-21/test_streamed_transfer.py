"""Prove the uploader survives slow progress beyond a socket's single-write timeout."""
import ast,hashlib,http.client,http.server,json,socket,ssl,tempfile,threading,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
payload=b'0123456789abcdef'*(128*1024)
class Handler(http.server.BaseHTTPRequestHandler):
    def do_PUT(self):
        remaining=int(self.headers['Content-Length']);received=bytearray()
        while remaining:
            block=self.rfile.read(min(16384,remaining))
            if not block:return
            received.extend(block);remaining-=len(block);time.sleep(.005)
        result=json.dumps({'bytes':len(received),'sha256':hashlib.sha256(received).hexdigest()}).encode()
        self.send_response(200);self.send_header('Content-Length',str(len(result)));self.end_headers()
        try:self.wfile.write(result)
        except (BrokenPipeError,ConnectionResetError):pass
    def log_message(self,*args):pass
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
def connection():
    conn=http.client.HTTPConnection('127.0.0.1',server.server_port,timeout=.3)
    conn.connect();conn.sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,16384)
    return conn
# The old one-buffer transport must fail despite the peer continually reading.
conn=connection();old_timed_out=False
try:
    conn.request('PUT','/api/files/test/file.bin',body=payload)
    conn.getresponse().read()
except TimeoutError:old_timed_out=True
finally:conn.close()
assert old_timed_out,'Fixture did not reproduce the original timeout'
module=ast.parse((ROOT/'data/compact_release_v1/package/.github/scripts/deposit.py').read_text())
function=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='request')
class Client:
    @staticmethod
    def HTTPSConnection(*args,**kwargs):return connection()
namespace={'http':type('Http',(),{'client':Client}),'CONTEXT':ssl.create_default_context(),'TOKEN':'unit-test-token','API':'/api/deposit/depositions/22876602','Path':Path,'time':time,'json':json}
exec(compile(ast.Module(body=[function],type_ignores=[]),'<request-under-test>','exec'),namespace)
try:
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'file.bin';path.write_bytes(payload)
        started=time.monotonic();result=namespace['request']('PUT','/api/files/test/file.bin',path);elapsed=time.monotonic()-started
    assert elapsed>.3 and result['bytes']==len(payload) and result['sha256']==hashlib.sha256(payload).hexdigest()
    receipt={'old_transport_timed_out':True,'streamed_transport_passed':True,'bytes':len(payload),'socket_timeout_seconds':.3,'transfer_seconds':elapsed}
    (HERE/'streamed_transfer_test.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
finally:server.shutdown();server.server_close()
