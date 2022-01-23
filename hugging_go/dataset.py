from .sgf import parse_sgf_sequence
from .vertex import Vertex

from datasets import load_dataset, Features, Value, ClassLabel

def _sgf_to_examples(labels_meta, tokenizer):
    def _parse(example):
        texts = []
        labels = []

        for text in example['text']:
            sequence = parse_sgf_sequence(text)

            for i in range(len(sequence) - 1):
                texts.append(sequence[:i])
                labels.append(labels_meta.str2int(sequence[i]))

        tokenized_text = tokenizer(
            texts,
            is_split_into_words=True,
            return_token_type_ids=False,
            truncation=True,
            max_length=512
        )

        return {
            'input_ids': tokenized_text['input_ids'],
            'attention_mask': tokenized_text['attention_mask'],
            'label': labels
        }

    return _parse

def _all_labels():
    for v in Vertex.all():
        yield v.as_gtp()
    yield 'pass'

def load_sgf_files(files, tokenizer):
    labels = ClassLabel(names=list(_all_labels()))
    features = Features({
        'input_ids': [Value('int64')],
        'attention_mask': [Value('int64')],
        'label': labels
    })
    dataset = load_dataset(
        'text',
        data_files={'train': files},
        features=Features({'text': Value('string')})
    )

    return dataset.map(
        _sgf_to_examples(labels, tokenizer),
        batched=True,
        remove_columns=['text'],
        features=features
    )
