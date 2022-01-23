from .beam_search import beam_search
from .vertex import Vertex

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
            best_candidate = beam_search(
                _pipe,
                board.sequence,
                depth=6,
                k=7
            )

            vertex = Vertex.from_gtp(best_candidate.label)

            assert board.state.is_valid(color, vertex)
            board.state.place(color, vertex)
            board.sequence.append(vertex.as_gtp())

            return vertex.as_gtp()
        except ValueError as e:
            traceback.print_exc()
            return 'pass'
