from .beam_search import beam_search
from .vertex import Vertex

import sys

class Agent:
    def __init__(self, pipe):
        self.pipe = pipe

    def play(self, board, color, vertex):
        if not board.state.is_valid(color, vertex):
            return False
        else:
            board.state.place(color, vertex)
            board.sequence.append(vertex.as_gtp())
            return True

    def genmove(self, board, color):
        def _pipe(seq):
            [candidates] = self.pipe(' '.join(seq))

            for cand in candidates:
                if cand['label'] == 'pass' or board.state.is_valid(color, Vertex.from_gtp(cand['label'])):
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

            assert board.state.is_valid(color, vertex)
            board.state.place(color, vertex)
            board.sequence.append(vertex.as_gtp())

            return vertex.as_gtp()
        except ValueError as e:
            traceback.print_exc()
            return 'pass'

def _pretty_print_candidates(candidates, base_seq_len):
        for cand in sorted(candidates, key=lambda c: c.score, reverse=True):
            seq_str = ' '.join(cand.sequence[base_seq_len:])

            print(f'  {seq_str.ljust(25)} (ln score is {cand.score:.3})', file=sys.stderr)
