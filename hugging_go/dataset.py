from .sgf import parse_sgf_sequence
from .vertex import Vertex

from datasets import load_dataset, Features, Value, ClassLabel

def _sgf_to_examples(labels_meta):
    def _parse(example):
        texts = []
        labels = []

        for text in example['text']:
            sequence = parse_sgf_sequence(text)
            for i in range(len(sequence) - 1):
                texts.append(' '.join(sequence[:i]))
                labels.append(labels_meta.str2int(sequence[i]))

        return {
            'text': texts,
            'label': labels
        }

    return _parse

def _all_labels():
    for v in Vertex.all():
        yield v.as_gtp()
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
