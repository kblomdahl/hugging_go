from .vertex import Vertex
from .sgf import parse_sgf_sequence

from tokenizers import AddedToken, Tokenizer, pre_tokenizers, models, trainers, normalizers, processors
from transformers import PreTrainedTokenizerFast

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

def get_tokenizer_corpus(files):
    for file in files:
        with open(file, 'r') as f:
            for line in f:
                sequence = parse_sgf_sequence(line)
                yield ' '.join(sequence)

def _all_tokens():
    for v in Vertex.all():
        yield AddedToken(v.as_gtp(), single_word=True)

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
