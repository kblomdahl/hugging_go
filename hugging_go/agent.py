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
            board.sequence[:] = new_sequence
            return True
        else:
            return False

    def genmove(self, board, color):
        def _pipe(seq):
            [candidates] = self.pipe(' '.join(seq))

            for cand in candidates:
                if self._is_sequence_valid(seq + [cand['label']]):
                    yield cand

        best_candidate = _beam_search(_pipe, board.sequence)
        vertex = Vertex.from_gtp(best_candidate.label)
        board.sequence.append(vertex.as_gtp())

        return vertex.as_gtp()

def _beam_search(pipe, base_seq, depth=6, k=7):
    def _wrap_pipe(seq):
        _wrap_pipe.count += 1
        return pipe(seq)

    _wrap_pipe.count = 0

    base_seq_len = len(base_seq)
    candidates = beam_search(
        _wrap_pipe,
        base_seq,
        depth=depth,
        k=k,
        return_all_candidates=True
    )

    print(f'Eval: {_wrap_pipe.count}, Depth: {depth}, Width {k}', file=sys.stderr)
    for cand in sorted(candidates, key=lambda c: c.score, reverse=True):
        seq_str = ' '.join(cand.sequence[base_seq_len:])
        scr_str = ' '.join([f'{score:4.2f}' for score in cand.scores])

        print(f'  {seq_str.ljust(25)} ({scr_str} / ln: {cand.score:.3})', file=sys.stderr)

    return max(candidates, key=lambda c: c.score)