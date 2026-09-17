"""ContextLab: text token accounting, budget checks and cost scenarios."""
import argparse
import json
import math

def count_text(text, encoding=None):
    if encoding:
        import tiktoken
        tokenizer = tiktoken.get_encoding(encoding)
        ids = tokenizer.encode(text, disallowed_special=())
        return {'count': len(ids), 'mode': f'exact text encoding: {encoding}', 'token_ids': ids}
    return {'count': math.ceil(len(text.encode('utf-8'))/4),
            'mode': 'rough UTF-8-byte/4 estimate; not a model tokenizer', 'token_ids': None}

def budget(text, *, context=8192, reserve=1024, overhead=0, input_rate=0, output_rate=0, encoding=None):
    if any(not isinstance(v, int) or v < 0 for v in (context, reserve, overhead)) or context == 0:
        raise ValueError('Context must be positive; reserve and overhead must be nonnegative integers.')
    if any(not math.isfinite(v) or v < 0 for v in (input_rate, output_rate)):
        raise ValueError('Rates must be finite nonnegative numbers.')
    counted = count_text(text, encoding)
    input_tokens = counted['count']+overhead
    remaining = context-input_tokens-reserve
    return {**counted, 'input_tokens_with_manual_overhead': input_tokens,
            'remaining_tokens': remaining, 'fits': remaining >= 0,
            'reserved_output_tokens': reserve,
            'projected_cost_usd': round((input_tokens*input_rate+reserve*output_rate)/1_000_000, 8),
            'note': 'Rates and context limit are user-supplied scenarios, not current model prices. '
                    'Exact text tokenization does not include message framing, tools or multimodal inputs.'}

if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('text'); p.add_argument('--encoding')
    p.add_argument('--context', type=int, default=8192)
    p.add_argument('--reserve', type=int, default=1024)
    p.add_argument('--overhead', type=int, default=0)
    p.add_argument('--input-rate', type=float, default=0)
    p.add_argument('--output-rate', type=float, default=0)
    a = p.parse_args()
    try:
        print(json.dumps(budget(**vars(a)), indent=2))
    except Exception as exc:
        p.exit(1, f'ContextLab: {exc}\n')
