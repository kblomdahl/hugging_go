from .agent import Agent
from .board_factory import BoardFactory
from .gtp import Gtp

import sys

gtp = Gtp(
    agent=Agent(),
    board_factory=BoardFactory()
)

for line in sys.stdin:
    print(gtp.process(line), end='', flush=True)
    if not gtp.is_running:
        break
