from .agent import Agent
from .board_factory import BoardFactory
from .gtp import Gtp
from .tokenizer import train_tokenizer

import sys

if sys.argv[1] == 'train-tokenizer':
    train_tokenizer(files=sys.argv[2:])
else:
    gtp = Gtp(
        agent=Agent(),
        board_factory=BoardFactory()
    )

    for line in sys.stdin:
        print(gtp.process(line), end='', flush=True)
        if not gtp.is_running:
            break
