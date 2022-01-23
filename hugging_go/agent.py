from .beam_search import beam_search
from .board import Board
from .color import Color
from .vertex import Vertex

import sys

class Agent:
    def __init__(self, pipe):
        self.pipe = pipe

    def _is_sequence_valid(self, seq):
        board = Board()
        color = Color('b')

        for label in seq:
            if label != 'pass':
                vertex = Vertex.from_gtp(label)
                if not board.is_valid(color, vertex):
                    return False
                board.place(color, vertex)

            color = color.opposite()

        return True

    def play(self, board, color, vertex):
        new_sequence = board.sequence + [vertex.as_gtp()]

        if self._is_sequence_valid(new_sequence):
            board.sequence = new_sequence
            return True
        else:
            return False

    def genmove(self, board, color):
        def _pipe(seq):
            [candidates] = self.pipe(' '.join(seq))

            for cand in candidates:
                if self._is_sequence_valid(seq + [cand['label']]):
                    yield cand

        try:
            candidates = beam_search(
                _pipe,
                board.sequence,
                depth=6,
                k=7,
                return_all_candidates=True
            )

            _pretty_print_candidates(candidates, len(board.sequence))

            best_candidate = max(candidates, key=lambda c: c.score)
            vertex = Vertex.from_gtp(best_candidate.label)
            board.sequence.append(vertex.as_gtp())

            return vertex.as_gtp()
        except ValueError as e:
            traceback.print_exc()
            return 'pass'

def _pretty_print_candidates(candidates, base_seq_len):
        for cand in sorted(candidates, key=lambda c: c.score, reverse=True):
            seq_str = ' '.join(cand.sequence[base_seq_len:])

            print(f'  {seq_str.ljust(25)} (ln score is {cand.score:.3})', file=sys.stderr)
