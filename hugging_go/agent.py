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
        candidates = self.pipe(' '.join(board.sequence))

        for cand in sorted(candidates[0], key=lambda c: c['score'], reverse=True):
            vertex = Vertex.from_gtp(cand['label'])

            if board.state.is_valid(color, vertex):
                board.state.place(color, vertex)
                board.sequence.append(vertex.as_gtp())
                return vertex.as_gtp()

        return 'resign'
