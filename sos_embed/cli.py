"""Command line entrypoint. Model inference is offline after download/verification."""
import os
import sys
os.environ.setdefault('HF_HUB_DISABLE_IMPLICIT_TOKEN', '1')
os.environ.setdefault('TOKENIZERS_PARALLELISM', 'false')
os.environ.setdefault('HF_HUB_DISABLE_PROGRESS_BARS', '1')
if len(sys.argv)>1 and sys.argv[1] not in ('download','freeze-assets'):
    os.environ['HF_HUB_OFFLINE']='1'
    os.environ['TRANSFORMERS_OFFLINE']='1'

import argparse
import json

from . import runner


def main():
    p = argparse.ArgumentParser(description='Diez modelos, mismos artículos y cálculo reanudable')
    sub = p.add_subparsers(dest='command', required=True)
    sub.add_parser('download', help='Descargar solo archivos fijados y verificar contra el autor')
    sub.add_parser('freeze-assets', help='Verificar archivos ya descargados contra el autor')
    sub.add_parser('prepare-pilot', help='Seleccionar 1.300 artículos para la prueba técnica')
    sub.add_parser('prepare-control', help='Preparar fragmentos idénticos en la misma prueba técnica')
    sub.add_parser('preflight', help='Comprobar corpus, versiones locales y disponibilidad de MPS')
    for command in ('run','status','verify','model'):
        q = sub.add_parser(command)
        q.add_argument('--scope', choices=['pilot','full','control'], default='pilot')
        if command in ('run','model'):
            q.add_argument('--device', choices=['mps','cpu'], default='mps')
        if command == 'model':
            q.add_argument('model', choices=[m['key'] for m in runner.config()['models']])
            q.add_argument('--max-shards', type=int)
    args = p.parse_args()
    if args.command == 'download': result = runner.download_assets()
    elif args.command == 'freeze-assets': result = runner.freeze_assets()
    elif args.command == 'prepare-pilot': result = runner.prepare_pilot()
    elif args.command == 'prepare-control': result = runner.prepare_control()
    elif args.command == 'preflight':
        result = {'corpus': runner.corpus_check(), 'environment': runner.environment(),
                  'mps_available': runner.torch.backends.mps.is_available(),
                  'production_input_policy_approved': runner.config()['production_input_policy_approved'],
                  'models_verified': [m['key'] for m in runner.config()['models'] if runner.verify_assets(m)]}
    elif args.command == 'model':
        if args.max_shards is not None and args.max_shards < 1: p.error('--max-shards must be positive')
        result = runner.run_model(args.model, args.scope, args.device, args.max_shards)
    elif args.command == 'run': result = runner.run_all(args.scope, args.device)
    else: result = runner.status(args.scope, verify=args.command == 'verify')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrumpido. Los bloques completos están guardados; repita el mismo comando.', file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f'No se continúa: {type(e).__name__}: {e}', file=sys.stderr)
        sys.exit(1)
