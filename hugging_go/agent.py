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
        color = Color('B')

        for label in seq:
            if label not in ['Bpass', 'Wpass']:
                vertex = Vertex.from_gtp(label[1:])
                if not board.is_valid(color, vertex):
                    return False
                board.place(color, vertex)

            color = color.opposite()

        return True

    def play(self, board, color, vertex):
        new_sequence = board.sequence + [str(color) + vertex.as_gtp()]

        if self._is_sequence_valid(new_sequence):
            board.sequence[:] = new_sequence
            return True
        else:
            return False

    def genmove(self, board, color):
        def _pipe(seq, next_color):
            [candidates, _] = self.pipe(' '.join(seq), next_color)

            for cand in candidates:
                if self._is_sequence_valid(seq + [cand['label']]):
                    yield cand

        if len(board.sequence) >= 512:
            return f'{str(color)}pass'

        best_candidate = _beam_search(_pipe, board.sequence, color)
        board.sequence.append(best_candidate.label)

        return best_candidate.label[1:]

def _beam_search(pipe, base_seq, next_color, depth=6, k=7):
    def _wrap_pipe(seq, color):
        _wrap_pipe.count += 1
        return pipe(seq, color)

    _wrap_pipe.count = 0

    base_seq_len = len(base_seq)
    candidates = beam_search(
        _wrap_pipe,
        base_seq,
        next_color,
        depth=depth,
        k=k,
        return_all_candidates=True,
        time_limit=1.0
    )

    print(f'Eval: {_wrap_pipe.count}, Depth: {depth}, Width {k}', file=sys.stderr)
    for cand in sorted(candidates, key=lambda c: c.score, reverse=True):
        seq_str = ' '.join(cand.sequence[base_seq_len:])
        scr_str = ' '.join([f'{score:4.2f}' for score in cand.scores])

        print(f'  {seq_str.ljust(25)} ({scr_str} / ln: {cand.score:.3})', file=sys.stderr)
    print(file=sys.stderr, flush=True)

    return max(candidates, key=lambda c: c.score)