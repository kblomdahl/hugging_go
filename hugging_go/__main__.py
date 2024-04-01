from .agent import Agent
from .board_factory import BoardFactory
from .dataset import load_sgf_files
from .gtp import Gtp
from .model import train, pretrained_model
from .tokenizer import train_tokenizer, pretrained_tokenizer

import fire
import sys

def main(*files, train_token=False, train_model=False):
    if train_token:
        train_tokenizer(files=files)
    elif train_model:
        tokenizer = pretrained_tokenizer()
        train(
            load_sgf_files(files, tokenizer),
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

if __name__ == '__main__':
    fire.Fire(main)
