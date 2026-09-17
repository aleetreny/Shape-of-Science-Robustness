"""Read-only lookup of historical IDs/texts; cache belongs to this new project."""
import json
import os
from pathlib import Path
import sqlite3

from .records import short_id, text_hash


def fingerprint(source):
    source = Path(source).resolve()
    stat = source.stat()
    return dict(path=str(source), size=stat.st_size, mtime_ns=stat.st_mtime_ns)


class LegacyIndex:
    def __init__(self, path, source):
        self.db = sqlite3.connect(Path(path).resolve().as_uri() + '?mode=ro', uri=True)
        saved = json.loads(self.db.execute('SELECT value FROM meta WHERE key=\'source\'').fetchone()[0])
        if saved != fingerprint(source):
            self.db.close()
            raise ValueError('El corpus antiguo ha cambiado: hay que actualizar su índice local.')
        self.source = saved

    def lookup(self, work_id, text_sha256):
        row = self.db.execute('SELECT text_sha256 FROM legacy WHERE work_id=?', (work_id,)).fetchone()
        return row is not None, row is not None and row[0] == text_sha256

    def close(self):
        self.db.close()


def build_index(source, output, report=print):
    import pyarrow.parquet as pq
    source, output = Path(source), Path(output)
    original = fingerprint(source)
    if output.exists():
        existing = LegacyIndex(output, source)
        count = existing.db.execute('SELECT count(*) FROM legacy').fetchone()[0]
        existing.close()
        report(f'Índice local ya preparado: {count:,} trabajos.')
        return count
    output.parent.mkdir(parents=True, exist_ok=True)
    temp = output.with_suffix('.sqlite.tmp')
    if temp.exists():
        temp.unlink()
    db = sqlite3.connect(temp)
    try:
        db.execute('CREATE TABLE legacy(work_id TEXT PRIMARY KEY,text_sha256 TEXT NOT NULL) WITHOUT ROWID')
        db.execute('CREATE TABLE meta(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
        parquet = pq.ParquetFile(source)
        columns = parquet.schema_arrow.names
        id_column = 'work_id' if 'work_id' in columns else 'id'
        count = 0
        for batch in parquet.iter_batches(batch_size=20000, columns=[id_column, 'title', 'abstract']):
            rows = [(short_id(r[id_column]), text_hash(r['title'] or '', r['abstract'] or '')) for r in batch.to_pylist()]
            with db:
                db.executemany('INSERT INTO legacy VALUES(?,?)', rows)
            count += len(rows)
            if count % 200000 == 0:
                report(f'Preparando índice del TFM: {count:,} trabajos leídos (sin modificarlo).')
        if fingerprint(source) != original:
            raise ValueError('El corpus antiguo cambió mientras se preparaba el índice')
        with db:
            db.execute('INSERT INTO meta VALUES(?,?)', ('source', json.dumps(original)))
            db.execute('INSERT INTO meta VALUES(?,?)', ('rows', json.dumps(count)))
    finally:
        db.close()
    with temp.open('rb') as handle:
        os.fsync(handle.fileno())
    os.replace(temp, output)
    report(f'Índice local preparado: {count:,} trabajos. No se ha descargado nada.')
    return count
