"""Prepare a clean copy. Status and preflight never download or run embeddings."""
import argparse
import hashlib
import json
from pathlib import Path

from sos_download.cli import get_key, writer_lock, LEGACY_INDEX, LEGACY_SOURCE
from sos_download.legacy import LegacyIndex
from sos_download.runner import ApiClient
from .quality import Quality
from .runner import CleanRunner, readonly
from .export import export_prepared

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT/'data/corpus_clean_v1'
REPORTS = ROOT/'research/cleaning_2026-09-15'


class LazyAPI:
    def __init__(self, allow_network=True):
        self.client = None
        self.allow_network = allow_network

    def get(self, params):
        if not self.allow_network:
            raise ValueError('Saved candidates are insufficient; rerun without --offline to fill the deficit')
        if self.client is None:
            self.client = ApiClient(get_key())
        return self.client.get(params)

    def close(self):
        if self.client:self.client.close()


def status():
    if not (OUTPUT/'state.sqlite').exists():
        print('La selección limpia todavía no ha empezado.');return
    db = readonly(OUTPUT/'state.sqlite')
    counts = dict(db.execute('SELECT cohort,count(*) FROM works GROUP BY cohort'))
    complete = db.execute("SELECT value FROM meta WHERE key='clean_complete'").fetchone()
    print(('LIMPIEZA VERIFICADA' if complete else 'PREPARACIÓN EN CURSO O PENDIENTE DE VERIFICACIÓN')+' · '+str(counts))
    db.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action',choices=['prepare','status','preflight'],nargs='?',default='status')
    parser.add_argument('--offline',action='store_true')
    parser.add_argument('--max-blocks',type=int)
    parser.add_argument('--max-pages',type=int)
    args = parser.parse_args()
    if args.action=='status':status();return
    if args.action=='preflight':
        from .verify import preflight
        print(json.dumps(preflight(OUTPUT),ensure_ascii=False,indent=2));return
    if any(x is not None and x<1 for x in (args.max_blocks,args.max_pages)):
        parser.error('Los límites deben ser positivos.')
    OUTPUT.mkdir(parents=True,exist_ok=True)
    config = json.loads((ROOT/'config/corpus.json').read_text())
    with writer_lock(OUTPUT):
        quality = legacy = runner = None
        api = LazyAPI(not args.offline)
        try:
            quality = Quality(OUTPUT,ROOT/'config/cleaning_v1.json',ROOT/'data/audit_models/lid.176.bin',ROOT/'data/corpus_audit/language.sqlite')
            legacy = LegacyIndex(LEGACY_INDEX,LEGACY_SOURCE)
            runner = CleanRunner(OUTPUT,config,api,quality,ROOT/'data/corpus_500k',report=lambda s:print(s,flush=True),legacy=legacy)
            if runner.store.get_meta('clean_complete'):
                status();return
            if runner.run(max_pages=args.max_pages,max_blocks=args.max_blocks):
                export_prepared(runner,REPORTS)
                from .verify import verify
                verify(runner,REPORTS)
        except KeyboardInterrupt:
            print('Pausado. Lo guardado se conserva; usa el mismo comando para continuar.')
        finally:
            if runner:runner.close()
            if quality:quality.close()
            if legacy:legacy.close()
            api.close()


if __name__=='__main__':main()
