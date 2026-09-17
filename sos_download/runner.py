"""Restartable sampling; only complete, validated blocks enter the corpus."""
import collections
from email.utils import parsedate_to_datetime
import hashlib
import json
import random
import time

import requests

from .records import allocate_extra, normalize_work
from .store import Store, utcnow, write_json

SELECT = ('id,doi,title,abstract_inverted_index,publication_year,publication_date,type,language,'
          'primary_topic,topics,is_retracted,is_paratext,updated_date,cited_by_count')


class PageDrift(ValueError):
    pass


class RetryableHTTP(Exception):
    def __init__(self, status, delay=0):
        self.status, self.delay = status, delay


class ApiClient:
    def __init__(self, key, url='https://api.openalex.org/works'):
        self.key, self.url = key, url
        self.session = requests.Session()
        self.session.headers['User-Agent'] = 'Shape-of-Science-Robustness/1.0 (research corpus)'
        if key:
            self.session.headers['Authorization'] = 'Bearer ' + key

    def close(self):
        self.session.close()

    def get(self, params):
        # The key travels only to OpenAlex. Never retain the prepared URL or exception text.
        with self.session.get(self.url, params=params,
                              timeout=(15, 60), allow_redirects=False) as response:
            if response.status_code in (408,429) or response.status_code >= 500:
                retry = response.headers.get('Retry-After', '0')
                try:
                    delay = float(retry)
                except ValueError:
                    try:
                        delay = parsedate_to_datetime(retry).timestamp() - time.time()
                    except (ValueError, TypeError, OverflowError):
                        delay = 0
                if response.status_code == 429 and response.headers.get('X-RateLimit-Remaining') == '0':
                    try:
                        delay = max(delay, float(response.headers.get('X-RateLimit-Reset', 0)))
                    except ValueError:
                        pass
                raise RetryableHTTP(response.status_code, max(0, delay))
            if response.status_code != 200:
                raise ValueError(f'OpenAlex devuelve HTTP {response.status_code}. Se ha conservado el avance.')
            payload = response.json()
            # Defence in depth in case an API error ever echoes a credential inside JSON.
            if self.key:
                payload = json.loads(json.dumps(payload).replace(self.key, '[REDACTED]'))
            return payload


class Runner:
    def __init__(self, root, config, api, fault=None, report=None, legacy=None):
        self.config, self.api = config, api
        self.store = Store(root, config)
        self.fault = fault or (lambda _: None)
        self.report = report or (lambda _: None)
        self.legacy = legacy
        self.checked_blocks = set()
        self.new_pages = 0
        self.last_request = 0
        self.api_calls = 0
        self.connection_recovered = False

    def close(self):
        self.store.close()

    def status(self, phase, **details):
        counts = self.store.counts()
        value = dict(updated_at=utcnow(), phase=phase, counts=counts,
                     target=self.config['base_target'] + self.config['extra_target'],
                     pages_saved=self.store.db.execute('SELECT count(*) FROM pages').fetchone()[0],
                     **details)
        write_json(self.store.root / 'progress.json', value)
        total = sum(counts.values())
        detail = details.get('message', '')
        if 'block' in details:
            label = f"Bloque {details['block']}"
            if 'page' in details:
                label += f", página {details['page']}/{details['pages']}"
            detail = label + '. ' + detail
        self.report(f"{total:,}/{value['target']:,} trabajos guardados · {phase}. {detail}")

    def request(self, params):
        failures = 0
        while True:
            delay = self.config['request_delay'] - (time.monotonic() - self.last_request)
            if delay > 0:
                time.sleep(delay)
            self.last_request = time.monotonic()
            self.api_calls += 1
            try:
                response = self.api.get(params)
                if failures:
                    self.connection_recovered = True
                return response
            except (requests.RequestException, RetryableHTTP) as error:
                failures += 1
                wait = max(getattr(error, 'delay', 0),
                           min(60, self.config['retry_seconds'] * 2 ** min(failures - 1, 6)))
                reason = f"HTTP {error.status}" if isinstance(error, RetryableHTTP) else 'conexión interrumpida'
                self.store.event('retry', dict(reason=reason, wait_seconds=wait, attempt=failures))
                self.status('esperando conexión o disponibilidad de OpenAlex',
                            message=f'Reintento en {wait:g} segundos ({reason}). Ctrl+C permite pausar.')
                # Sleep remains interruptible; long rate-limit waits still show that the job is alive.
                until = time.monotonic() + wait
                while (remaining := until - time.monotonic()) > 0:
                    time.sleep(min(remaining, 30))
                    if remaining > 30:
                        self.report('Seguimos esperando a OpenAlex; el avance está guardado.')

    def params(self, block, page):
        start, end = self.config['year_min'], self.config['year_max']
        field = '!null'
        if block['cohort'] == 'extra':
            start, end = block['period_start'], block['period_start'] + 4
            field = str(block['field_id'])
        filters = (f'publication_year:{start}-{end},type:article|review|conference-paper,'
                   f'language:en,has_abstract:true,is_retracted:false,is_paratext:false,primary_topic.field.id:{field}')
        return dict(corpus='core', filter=filters, sample=block['sample_size'], seed=block['seed'],
                    per_page=self.config['per_page'], page=page, select=SELECT)

    def validate_page(self, block, page, response):
        if not isinstance(response, dict) or not isinstance(response.get('results'), list):
            raise ValueError('OpenAlex no ha devuelto una página completa reconocible')
        count = response.get('meta', {}).get('count')
        if type(count) is not int or count < 0:
            raise ValueError('OpenAlex no ha devuelto el recuento de la selección')
        total = min(count, block['sample_size'])
        expected = max(0, min(self.config['per_page'], total - (page - 1) * self.config['per_page']))
        if len(response['results']) != expected:
            raise PageDrift('La página tiene un tamaño inesperado. Se conserva lo guardado para revisar.')
        if block['sample_result_count'] is not None and count != block['sample_result_count']:
            raise PageDrift('El tamaño de la selección de OpenAlex ha cambiado durante este bloque.')
        ids = [w.get('id') for w in response['results'] if isinstance(w, dict)]
        if len(ids) != expected or any(not isinstance(wid, str) for wid in ids) or len(set(ids)) != len(ids):
            raise PageDrift('La página contiene IDs ausentes o repetidos; no se aplica al corpus.')

    def block(self, block_id):
        return self.store.db.execute('SELECT * FROM blocks WHERE id=?', (block_id,)).fetchone()

    def check_saved_ids(self, block, saved):
        self.status('comprobando la reanudación', message=f'Verificando IDs de {saved} páginas; sin volver a descargar sus textos.')
        checks = []
        for page in range(1, saved + 1):
            response = self.request({**self.params(block, page), 'select': 'id'})
            self.validate_page(block, page, response)
            previous = self.store.read_page(block['id'], page)['response']
            if [w['id'] for w in response['results']] != [w['id'] for w in previous['results']]:
                raise PageDrift('OpenAlex ha cambiado las páginas de este bloque. Se ha pausado sin sobrescribir los datos. Pide revisar esta descarga.')
            checks.append(dict(page=page, checked_at=utcnow(), ids_sha256=hashlib.sha256(
                '\n'.join(w['id'] for w in response['results']).encode()).hexdigest()))
            if page % 10 == 0:
                self.report(f'Reanudación: comprobadas {page}/{saved} páginas.')
        self.store.event('resume_pages_checked', dict(block=block['id'], checks=checks))
        self.connection_recovered = False

    def new_block(self, cohort, cell=None):
        db = self.store.db
        block_id = db.execute('SELECT COALESCE(max(id),0)+1 FROM blocks').fetchone()[0]
        token = f"{self.config['seed']}:{block_id}:{cohort}:{cell}"
        seed = int.from_bytes(hashlib.sha256(token.encode()).digest()[:4], 'big') % (2**31 - 1)
        # Seeds are permanent and distinct, even in the unlikely event of a hash collision.
        while db.execute('SELECT 1 FROM blocks WHERE seed=?', (seed,)).fetchone():
            seed = (seed + 1) % (2**31 - 1)
        field, period = cell or (None, None)
        size = self.config['block_size']
        if cell:
            target = db.execute('SELECT target FROM allocations WHERE field_id=? AND period_start=?', cell).fetchone()[0]
            have = db.execute("SELECT count(*) FROM works WHERE cohort='extra' AND field_id=? AND period_start=?", cell).fetchone()[0]
            # Avoid downloading a whole 10k block for a ~2k supplement. Size affects cost only;
            # accepted candidates are still shuffled and never selected by API page order.
            needed = max(1, target - have)
            size = min(size, max(self.config['per_page'], ((needed * 3 // 2 + self.config['per_page'] - 1) // self.config['per_page']) * self.config['per_page']))
            previous = db.execute("SELECT sample_size,stats_json FROM blocks WHERE cohort='extra' AND field_id=? AND period_start=? AND status='applied' ORDER BY id DESC LIMIT 1", cell).fetchone()
            if previous and json.loads(previous['stats_json']).get('accepted', 0) == 0:
                # A tiny repeated sample cannot establish exhaustion of a larger cell.
                # Expand deterministically so cells below the API ceiling can reach a census.
                size = min(self.config['block_size'], max(size, previous['sample_size'] * 2))
        with db:
            db.execute('INSERT INTO blocks(id,cohort,field_id,period_start,seed,sample_size,status,created_at) VALUES(?,?,?,?,?,?,?,?)',
                       (block_id, cohort, field, period, seed, size, 'downloading', utcnow()))
        return self.block(block_id)

    def download_block(self, block, max_pages):
        bid = block['id']
        # Adopt an atomic file left by a crash between rename and SQLite commit.
        page = 1
        while envelope := self.store.read_page(bid, page):
            if envelope['parameters'] != self.params(block, page):
                raise ValueError('Los parámetros de una página guardada no coinciden')
            self.validate_page(block, page, envelope['response'])
            self.store.register_page(block, page, self.store.page_path(bid, page), envelope)
            block = self.block(bid)
            page += 1
        saved = page - 1
        if block['n_pages'] is not None and saved > block['n_pages']:
            raise ValueError('Hay más páginas guardadas de las esperadas')
        if saved and saved < block['n_pages'] and bid not in self.checked_blocks:
            self.check_saved_ids(block, saved)
        self.checked_blocks.add(bid)
        while block['n_pages'] is None or page <= block['n_pages']:
            if max_pages is not None and self.new_pages >= max_pages:
                return False
            params = self.params(block, page)
            response = self.request(params)
            self.validate_page(block, page, response)
            if page > 1 and self.connection_recovered:
                self.check_saved_ids(block, page - 1)
            self.store.persist_page(block, page, params, response, self.fault)
            self.new_pages += 1
            block = self.block(bid)
            self.status('descargando', block=bid, page=page, pages=block['n_pages'])
            page += 1
        return True

    def apply_block(self, block):
        candidates, seen = [], set()
        for page in range(1, block['n_pages'] + 1):
            envelope = self.store.read_page(block['id'], page)
            self.validate_page(block, page, envelope['response'])
            for index, raw in enumerate(envelope['response']['results']):
                if raw['id'] in seen:
                    raise PageDrift('Un ID aparece en varias páginas del mismo bloque. Se conserva el bloque sin aplicarlo.')
                seen.add(raw['id'])
                candidates.append((raw, page, index, envelope['retrieved_at']))
        random.Random(block['seed']).shuffle(candidates)
        db = self.store.db
        counts = self.store.counts()
        cohort = block['cohort']
        if cohort == 'base':
            remaining = self.config['base_target'] - counts.get('base', 0)
        else:
            cell = (block['field_id'], block['period_start'])
            target = db.execute('SELECT target FROM allocations WHERE field_id=? AND period_start=?', cell).fetchone()[0]
            existing = db.execute("SELECT count(*) FROM works WHERE cohort='extra' AND field_id=? AND period_start=?", cell).fetchone()[0]
            remaining = target - existing
        stats = collections.Counter(candidates=len(candidates), accepted=0)
        order = sum(counts.values())
        with db:
            for raw, page, index, retrieved in candidates:
                if stats['accepted'] >= remaining:
                    break
                record, reason = normalize_work(raw, self.config)
                if reason:
                    stats['rejected_' + reason] += 1
                    continue
                if cohort == 'extra' and (record['field_id'], record['period_start']) != cell:
                    raise PageDrift('OpenAlex devolvió un trabajo de otra área o período.')
                if db.execute('SELECT 1 FROM works WHERE work_id=?', (record['work_id'],)).fetchone():
                    stats['duplicate_work_id'] += 1
                    continue
                stats['accepted'] += 1
                order += 1
                record.update(cohort=cohort, selection_order=order, source_block=block['id'],
                              source_page=page, source_page_index=index, source_seed=block['seed'],
                              retrieved_at=retrieved, legacy_id_present=False, legacy_text_match=False)
                if self.legacy:
                    record['legacy_id_present'], record['legacy_text_match'] = self.legacy.lookup(record['work_id'], record['text_sha256'])
                db.execute('INSERT INTO works VALUES(?,?,?,?,?,?,?,?,?)',
                           (record['work_id'], order, cohort, record['field_id'], record['period_start'], record['doi'],
                            record['text_sha256'], block['id'], json.dumps(record, ensure_ascii=False)))
                self.fault('during_apply')
            stats['not_examined_after_target'] = len(candidates) - sum(v for k, v in stats.items() if k != 'candidates')
            db.execute("UPDATE blocks SET status='applied',applied_at=?,stats_json=? WHERE id=?",
                       (utcnow(), json.dumps(stats), block['id']))
            if cohort == 'extra' and len(candidates) < block['sample_size'] and stats['accepted'] < remaining:
                db.execute('UPDATE allocations SET exhausted=1 WHERE field_id=? AND period_start=?', cell)
        self.fault('after_apply')
        self.status('bloque guardado', block=block['id'], message=f"{stats['accepted']} trabajos nuevos válidos.")
        # A strictly smaller sample is a census of this filtered cell at retrieval time.
        # meta.count == requested sample does NOT give the population size.
        if cohort == 'extra' and len(candidates) < block['sample_size'] and stats['accepted'] < remaining:
            self.store.event('cell_exhausted', dict(field_id=cell[0], period_start=cell[1], candidates=len(candidates)))
            self.reallocate()
        elif stats['accepted'] == 0:
            rows = db.execute('SELECT stats_json FROM blocks WHERE cohort=? AND field_id IS ? AND period_start IS ? AND status=\'applied\' ORDER BY id DESC LIMIT 20',
                              (cohort, block['field_id'], block['period_start'])).fetchall()
            if len(rows) == 20 and all(json.loads(r[0]).get('accepted', 0) == 0 for r in rows):
                raise ValueError('20 bloques seguidos no añaden trabajos. Se pausa para revisar, sin cambiar el protocolo.')

    def reallocate(self):
        db = self.store.db
        counts = self.store.cell_counts(self.config)
        remaining = self.config['extra_target'] - self.store.counts().get('extra', 0)
        exhausted = {(r[0], r[1]) for r in db.execute('SELECT field_id,period_start FROM allocations WHERE exhausted=1')}
        increments = allocate_extra(counts, remaining, exhausted)
        with db:
            for (field, period), extra in increments.items():
                have = db.execute("SELECT count(*) FROM works WHERE cohort='extra' AND field_id=? AND period_start=?", (field,period)).fetchone()[0]
                db.execute('INSERT INTO allocations VALUES(?,?,?,?) ON CONFLICT(field_id,period_start) DO UPDATE SET target=excluded.target',
                           (field, period, have + extra, int((field, period) in exhausted)))
        self.store.event('supplement_allocated', dict(remaining=remaining, exhausted=sorted(exhausted)))

    def run(self, max_pages=None):
        while True:
            counts = self.store.counts()
            active = self.store.db.execute("SELECT * FROM blocks WHERE status='downloading' ORDER BY id LIMIT 1").fetchone()
            if not active:
                if counts.get('base', 0) < self.config['base_target']:
                    active = self.new_block('base')
                elif counts.get('extra', 0) < self.config['extra_target']:
                    # Recomputing from saved counts is idempotent and recovers a crash
                    # after an exhausted cell was committed but before its redistribution.
                    self.reallocate()
                    row = self.store.db.execute('''SELECT a.field_id,a.period_start FROM allocations a
                        LEFT JOIN (SELECT field_id,period_start,count(*) n FROM works WHERE cohort='extra' GROUP BY 1,2) w
                        ON a.field_id=w.field_id AND a.period_start=w.period_start
                        WHERE a.exhausted=0 AND a.target>COALESCE(w.n,0) ORDER BY a.field_id,a.period_start LIMIT 1''').fetchone()
                    if row is None:
                        self.reallocate()
                        continue
                    active = self.new_block('extra', tuple(row))
                else:
                    self.status('comprobando y creando la tabla final')
                    result = self.store.export(self.config)
                    self.status('completo', validation=result)
                    return result
            if not self.download_block(active, max_pages):
                self.status('pausado', message='Continúa con el mismo comando.')
                return None
            self.apply_block(self.block(active['id']))
