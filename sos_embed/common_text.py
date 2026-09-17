"""Same source fragments for every model; native special separators are retained."""
import re

from .models import format_text


def common_fragment(title, abstract, pairs):
    def fits(t, a):
        for spec, tokenizer in pairs:
            s = format_text(t, a, spec['text_format'], tokenizer.sep_token)
            ids = tokenizer(s, truncation=False, verbose=False, return_token_type_ids=False)['input_ids']
            if len(ids) > spec['max_length']:
                return False
        return True

    def prefix(text, predicate):
        # Preserve original characters; candidates stop at ends of non-whitespace spans.
        ends = [0] + [m.end() for m in re.finditer(r'\S+', text)]
        lo, hi = 0, len(ends) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if predicate(text[:ends[mid]]):
                lo = mid
            else:
                hi = mid - 1
        result = text[:ends[lo]]
        if not predicate(result):
            raise ValueError('No common fragment fits all tokenizers')
        return result

    if fits(title, abstract):
        return title, abstract
    if fits(title, ''):
        return title, prefix(abstract, lambda a: fits(title, a))
    return prefix(title, lambda t: fits(t, '')), ''
