from .minimax import minimax
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
        def _pipe(seq, next_color, **kwargs):
            [candidates, winner, past_key_values] = self.pipe(' '.join(seq), next_color, **kwargs)
            candidates = [cand for cand in candidates if self._is_sequence_valid(seq + [cand['label']])]

            return [candidates, winner, past_key_values]

        if len(board.sequence) >= 512:
            return f'{str(color)}pass'

        best_candidate = _minimax(_pipe, board.sequence, color)
        board.sequence.append(best_candidate.label)

        return best_candidate.label[1:]

def _minimax(pipe, base_seq, next_color, time_limit=3.0, depth=6, tfs_z=0.95):
    def _wrap_pipe(*args, **kwargs):
        _wrap_pipe.count += 1
        return pipe(*args, **kwargs)

    _wrap_pipe.count = 0
    [candidates, max_depth] = minimax(
        _wrap_pipe,
        base_seq,
        next_color,
        depth=depth,
        tfs_z=tfs_z,
        return_all_candidates=True,
        time_limit=time_limit
    )

    print(f'Eval: {_wrap_pipe.count}, Depth: {max_depth}', file=sys.stderr)
    for cand in sorted(candidates, key=lambda c: c.value):
        curr = cand
        seq_list = []
        scr_list = []

        while curr is not None:
            if curr.child is not None:
                seq_list.append(curr.label[1:])
                scr_list.append(curr.score)
            curr = curr.child

        seq_str = ' '.join(seq_list)
        scr_str = ' '.join([f'{score:4.2f}' for score in scr_list])

        print(f'  {seq_str.ljust(25)} ({scr_str} / val: {-cand.value:.3})', file=sys.stderr)
    print(file=sys.stderr, flush=True)

    return min(candidates, key=lambda c: c.value)
