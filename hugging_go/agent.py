class Agent:
    def play(self, board, color, vertex):
        if not board.is_valid(color, vertex):
            return False
        else:
            board.place(color, vertex)
            return True

    def genmove(self, board, color):
        return 'resign'
