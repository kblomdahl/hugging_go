from .sgf import parse_sgf

from datasets import load_dataset

def _sgf_to_examples(tokenizer):
    def _parse(example):
        sgf = parse_sgf(example['text'])
        tokenized_text = tokenizer(
            sgf.sequence,
            is_split_into_words=True,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            max_length=512
        )

        return {
            **tokenized_text,
            "winner": sgf.winner,
            "komi": sgf.komi,
            "labels": tokenized_text["input_ids"].copy()
        }

    return _parse

def load_sgf_files(files, tokenizer):
    dataset = load_dataset('text', data_files=files)

    return dataset.map(
        _sgf_to_examples(tokenizer),
        remove_columns=['text']
    )
