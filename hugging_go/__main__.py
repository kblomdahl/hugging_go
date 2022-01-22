from .agent import Agent
from .board_factory import BoardFactory
from .dataset import load_sgf_files
from .gtp import Gtp
from .model import train
from .tokenizer import train_tokenizer, pretrained_tokenizer

import sys

if sys.argv[1] == 'train-tokenizer':
    train_tokenizer(files=sys.argv[2:])
if sys.argv[1] == 'train-model':
    dataset = load_sgf_files(sys.argv[2:])
    train(
        dataset,
        tokenizer=pretrained_tokenizer()
    )
else:
    gtp = Gtp(
        agent=Agent(),
        board_factory=BoardFactory()
    )

    for line in sys.stdin:
        print(gtp.process(line), end='', flush=True)
        if not gtp.is_running:
            break
