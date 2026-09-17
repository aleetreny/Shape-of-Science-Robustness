"""Pinned local encoders; preserve raw vectors so later normalization is reversible."""
import hashlib
import struct
import time
import resource

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer


def format_text(title, abstract, style, sep):
    if style == 'sep':
        return title + sep + abstract
    if style == 'blank_line':
        return title + '\n\n' + abstract
    raise ValueError(f'Unknown text format: {style}')


def pool(hidden, mask, mode):
    if mode == 'cls':
        return hidden[:, 0]
    if mode == 'sep':
        return hidden[torch.arange(hidden.shape[0], device=hidden.device), mask.sum(1) - 1]
    if mode == 'mean':
        m = mask.unsqueeze(-1).to(hidden.dtype)
        return (hidden * m).sum(1) / m.sum(1).clamp(min=1)
    raise ValueError(f'Unknown pooling: {mode}')


def snapshot_path(cache, asset):
    return cache / ('models--' + asset['repo_id'].replace('/', '--')) / 'snapshots' / asset['revision']


class Encoder:
    def __init__(self, spec, cache, device='mps'):
        self.spec, self.device = spec, device
        path = snapshot_path(cache, spec)
        self.tokenizer = AutoTokenizer.from_pretrained(path, local_files_only=True, trust_remote_code=False,
                                                       use_fast=True)
        if not self.tokenizer.is_fast or self.tokenizer.padding_side != 'right':
            raise ValueError('Fast tokenizer with right padding required for coverage auditing')
        options = dict(local_files_only=True, trust_remote_code=False, torch_dtype=torch.float32,
                       attn_implementation='eager', output_loading_info=True,
                       use_safetensors=spec['weight_file'].endswith('.safetensors'))
        if 'adapter' in spec:
            from adapters import AutoAdapterModel
            model, info = AutoAdapterModel.from_pretrained(path, **options)
            model.load_adapter(str(snapshot_path(cache, spec['adapter'])), load_as='proximity', set_active=True)
        else:
            model, info = AutoModel.from_pretrained(path, **options)
        # Pretraining task heads may be unused; missing encoder weights must never be randomized silently.
        missing = [k for k in info['missing_keys'] if 'pooler' not in k]
        if missing or info.get('mismatched_keys') or info.get('error_msgs'):
            raise ValueError(f'Incomplete model weights: {info}')
        if spec['max_length'] > model.config.max_position_embeddings:
            raise ValueError('Configured length exceeds architecture')
        if model.config.hidden_size != spec['dimension']:
            raise ValueError('Configured dimension differs from checkpoint')
        self.loading_info = info
        self.model = model.eval().to(device)

    def encode(self, rows, batch_size=16):
        start = time.perf_counter()
        texts = [format_text(r['title'], r['abstract'], self.spec['text_format'], self.tokenizer.sep_token)
                 for r in rows]
        # Untruncated lengths plus actual token IDs make lost content visible without changing original texts.
        full = self.tokenizer(texts, truncation=False, padding=False, return_token_type_ids=False,
                              verbose=False)['input_ids']
        outputs = {p: [] for p in self.spec['poolings']}
        audit = []
        with torch.inference_mode():
            for offset in range(0, len(texts), batch_size):
                chosen = texts[offset:offset + batch_size]
                batch = self.tokenizer(chosen, padding=True, truncation=True,
                                       max_length=self.spec['max_length'], return_tensors='pt',
                                       return_token_type_ids=False, return_offsets_mapping=True)
                offsets = batch.pop('offset_mapping').tolist()
                ids, masks = batch['input_ids'].tolist(), batch['attention_mask'].tolist()
                for j, (tokens, mask, positions) in enumerate(zip(ids, masks, offsets)):
                    n = sum(mask)
                    tokens = tokens[:n]
                    text = chosen[j]
                    audit.append({'tokens_original': len(full[offset+j]), 'tokens_used': n,
                                  'truncated': len(full[offset+j]) > self.spec['max_length'],
                                  'formatted_text_sha256': hashlib.sha256(text.encode()).hexdigest(),
                                  'token_ids_sha256': hashlib.sha256(struct.pack('<' + 'I'*n, *tokens)).hexdigest(),
                                  'last_content_character': max(b for a,b in positions[:n]),
                                  'formatted_characters': len(text)})
                batch = {k: v.to(self.device) for k, v in batch.items()}
                hidden = self.model(**batch).last_hidden_state
                for name in outputs:
                    outputs[name].append(pool(hidden, batch['attention_mask'], name).cpu().numpy())
        if self.device == 'mps':
            torch.mps.synchronize()
        seconds = time.perf_counter() - start
        stats = {'seconds': seconds, 'rows': len(rows), 'batch_size': batch_size,
                 'truncated_rows': sum(r['truncated'] for r in audit),
                 'tokens_original': sum(r['tokens_original'] for r in audit),
                 'tokens_used': sum(r['tokens_used'] for r in audit)}
        stats['process_peak_rss_gib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30
        if self.device == 'mps':
            stats['mps_driver_allocated_gib_at_shard_end'] = torch.mps.driver_allocated_memory() / 2**30
        return {k: np.concatenate(v).astype(np.float32, copy=False) for k,v in outputs.items()}, audit, stats
