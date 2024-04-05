from hugging_go.board import Board
from hugging_go.color import Color
from hugging_go.vertex import Vertex

import unittest

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.komi = 5.5
        self.board = Board(komi=self.komi)

    def test_double_place(self):
        self.board.place(Color('B'), Vertex.from_gtp('d4'))
        self.assertFalse(
            self.board.is_valid(Color('B'), Vertex.from_gtp('d4'))
        )

if __name__ == '__main__':
    unittest.main()
