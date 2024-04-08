""" Dataset of game records from SGF files.

Loads a dataset of game records from SGF files. The dataset is tokenized using
a custom tokenizer that uses a modified A1 algebraic notation.

The output of each example in the dataset is a dictionary with the following
keys:
  - `input_ids`: The tokenized game record.
  - `attention_mask`: The attention mask for the tokenized game record.
  - `komi`: The komi for the game.
  - `winner`: The winner of the game (`B` or `W`).
  - `labels`: A combined list of the winner (for the value head) at index 0, and
              then the tokenized game record (for the policy head).
"""

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
            "komi": sgf.komi,
            "winner": sgf.winner,
            "labels": [
                0 if sgf.winner == 'B' else 1,
                *tokenized_text["input_ids"].copy()
            ]
        }

    return _parse

def _only_with_winner(example):
    return example["winner"] in ['B', 'W']

def load_sgf_files(files, tokenizer):
    dataset = load_dataset('text', data_files=files)

    return dataset.map(_sgf_to_examples(tokenizer), remove_columns=['text']).filter(_only_with_winner)
