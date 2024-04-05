""" Tokenizer for algebraic notation for Go.

Word-level tokenizer for game records using a modified A1 (or Korschelt) [1]
algebraic notation. The A1 notation use `a1` to `t19` to represent coordinates.

In A1 notation the owner of each move is implied by the order of the moves. We
choose to make this explicit by adding the color to each move. For example `a1`
becomes `Ba1`.

For example:

```
Bq16 Wd17 Bq5 Wq3 Bc5 Wd15 Br3 Wr2 Br4 Wp2
```

# Handicap

Using this notation we can represent handicapped games by prefixing the
handicap stones to the normal moves.

# Komi

The A1 notation does not include komi and it is currently unclear how to
include it.

[1] https://senseis.xmp.net/?Coordinates%2FA1
"""

from .vertex import Vertex
from .sgf import parse_sgf

from tokenizers import AddedToken, Tokenizer, pre_tokenizers, models, trainers, processors
from transformers import PreTrainedTokenizerFast

_TOKENIZER_FILE_PATH = 'model/tokenizer.json'
NUM_SPECIAL_TOKENS = 5
VOCAB_SIZE = 724 + NUM_SPECIAL_TOKENS

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
                sgf = parse_sgf(line)
                if sgf.success:
                    yield ' '.join(sgf.sequence)

def _all_tokens():
    for v in Vertex.all():
        yield AddedToken('B' + v.as_gtp(), single_word=True)
        yield AddedToken('W' + v.as_gtp(), single_word=True)
    yield AddedToken('Bpass', single_word=True)
    yield AddedToken('Wpass', single_word=True)

def train_tokenizer(files):
    tokenizer = Tokenizer(model=models.WordLevel(unk_token='[UNK]'))
    tokenizer.pre_tokenizer = pre_tokenizers.WhitespaceSplit()

    trainer = trainers.WordLevelTrainer(
        vocab_size=VOCAB_SIZE,
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
