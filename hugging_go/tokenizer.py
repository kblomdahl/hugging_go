from tokenizers import AddedToken, Tokenizer, pre_tokenizers, models, trainers, normalizers, processors
from transformers import PreTrainedTokenizerFast

import re

_TOKENIZER_FILE_PATH = 'model/tokenizer.json'

def pretrained_tokenizer():
    return PreTrainedTokenizerFast(
        tokenizer_file=_TOKENIZER_FILE_PATH,
        bos_token='[CLS]',
        eos_token='[SEP]',
        unk_token='[UNK]',
        sep_token='[SEP]',
        pad_token='[PAD]',
        cls_token='[CLS]',
        mask_token='[MASK]',
        padding_side='right'
    )

_SGF_LETTERS = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
)

_GTP_LETTERS = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
)

def _sgf_to_gtp(v):
    if len(v) != 2:
        return 'pass'
    else:
        x = _SGF_LETTERS.index(v[0])
        y = _SGF_LETTERS.index(v[1])

        if x > 18 or y > 18: # sometimes `pass` is written as `tt`
            return 'pass'

        return f'{_GTP_LETTERS[x]}{y + 1}'

def _get_sequence_from_line(line):
    sequence = []

    for vertex in re.findall(r'[BW]\[([a-z]{0,2})\]', line):
        vertex = _sgf_to_gtp(vertex)
        if vertex is None:
            return None

        sequence.append(f'{vertex}')

    return ' '.join(sequence)

def get_tokenizer_corpus(files):
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                sequence = _get_sequence_from_line(line)
                if sequence:
                    yield sequence

def _all_tokens():
    for x in _GTP_LETTERS:
        for y in range(1, 20):
            yield AddedToken(f'{x}{y}', single_word=True)

    yield AddedToken('pass', single_word=True)

def train_tokenizer(files):
    tokenizer = Tokenizer(model=models.WordLevel(unk_token='[UNK]'))
    tokenizer.pre_tokenizer = pre_tokenizers.WhitespaceSplit()

    trainer = trainers.WordLevelTrainer(
        vocab_size=362 + 5,
        special_tokens=[
            AddedToken('[UNK]', single_word=True),
            AddedToken('[PAD]', single_word=True),
            AddedToken('[CLS]', single_word=True),
            AddedToken('[SEP]', single_word=True),
            AddedToken('[MASK]', single_word=True)
        ] + list(_all_tokens())
    )
    tokenizer.train_from_iterator(
        get_tokenizer_corpus(files),
        trainer=trainer
    )

    cls_token_id = tokenizer.token_to_id('[CLS]')
    sep_token_id = tokenizer.token_to_id('[SEP]')
    tokenizer.post_processor = processors.TemplateProcessing(
        single='[CLS] $0 [SEP]',
        special_tokens=[
            ('[CLS]', cls_token_id),
            ('[SEP]', sep_token_id),
        ]
    )
    tokenizer.save(_TOKENIZER_FILE_PATH)
