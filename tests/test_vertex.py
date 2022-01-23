from hugging_go.vertex import Vertex

import unittest

class TestVertex(unittest.TestCase):
    def test_d4(self):
        self.assertEqual(
            Vertex.from_gtp('d4'),
            Vertex(x=3, y=3)
        )

    def test_dd(self):
        self.assertEqual(
            Vertex.from_sgf('dd'),
            Vertex(x=3, y=3)
        )

    def test_q16(self):
        self.assertEqual(
            Vertex.from_gtp('q16'),
            Vertex(x=15, y=15)
        )

if __name__ == '__main__':
    unittest.main()
