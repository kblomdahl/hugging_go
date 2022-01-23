from datasets import load_dataset, Features, Value, ClassLabel

import re

def _sgf_to_gtp(v):
    if len(v) != 2:
        return 'pass'
    else:
        v = Vertex.from_sgf(v)
        return v.to_gtp() if v.is_valid() else 'pass'

def _get_sequence_from_line(line):
    sequence = []

    for vertex in re.findall(r'[BW]\[([a-z]{0,2})\]', line):
        vertex = _sgf_to_gtp(vertex)
        if vertex is None:
            return None

        sequence.append(vertex)

    return sequence

def _sgf_to_examples(labels_meta):
    def _parse(example):
        texts = []
        labels = []

        for text in example['text']:
            sequence = _get_sequence_from_line(text)
            for i in range(len(sequence) - 1):
                texts.append(' '.join(sequence[:i]))
                labels.append(labels_meta.str2int(sequence[i]))

        return {
            'text': texts,
            'label': labels
        }

    return _parse

def _all_labels():
    for x in _GTP_LETTERS:
        for y in range(1, 20):
            yield f'{x}{y}'

    yield 'pass'

def load_sgf_files(files):
    labels = ClassLabel(names=list(_all_labels()))
    features = Features({
        'text': Value('string'),
        'label': labels
    })
    dataset = load_dataset(
        'text',
        data_files={'train': files},
        features=Features({'text': Value('string')})
    )

    dataset = dataset.map(_sgf_to_examples(labels), batched=True, features=features)
    return dataset
