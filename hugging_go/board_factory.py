from .board import Board

from collections import namedtuple

BoardWithHistory = namedtuple('BoardWithHistory', ['state', 'sequence'])

class BoardFactory:
    def build(self, board_size, komi):
        assert board_size == 19, 'only 19×19 boards are supported'

        return BoardWithHistory(
            state=Board(komi),
            sequence=[]
        )
