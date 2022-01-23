from .agent import Agent
from .board_factory import BoardFactory
from .dataset import load_sgf_files
from .gtp import Gtp
from .model import train, pretrained_model
from .tokenizer import train_tokenizer, pretrained_tokenizer

import sys

if len(sys.argv) > 1 and sys.argv[1] == 'train-tokenizer':
    train_tokenizer(files=sys.argv[2:])
elif len(sys.argv) > 1 and sys.argv[1] == 'train-model':
    tokenizer = pretrained_tokenizer()
    train(
        load_sgf_files(sys.argv[2:], tokenizer),
        tokenizer=tokenizer
    )
else:
    gtp = Gtp(
        agent=Agent(pretrained_model()),
        board_factory=BoardFactory()
    )

    for line in sys.stdin:
        print(gtp.process(line), end='', flush=True)
        if not gtp.is_running:
            break
