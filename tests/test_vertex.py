from hugging_go.vertex import Vertex

import unittest

class TestVertex(unittest.TestCase):
    def test_d4(self):
        self.assertEqual(
            Vertex.from_gtp('d4'),
            Vertex(x=3, y=3)
        )
        self.assertEqual(
            Vertex.from_gtp('d4').as_gtp(),
            'd4'
        )

    def test_dd(self):
        self.assertEqual(
            Vertex.from_sgf('dd'),
            Vertex(x=3, y=3)
        )
        self.assertEqual(
            Vertex.from_sgf('dd').as_sgf(),
            'dd'
        )

    def test_q16(self):
        self.assertEqual(
            Vertex.from_gtp('q16'),
            Vertex(x=15, y=15)
        )
        self.assertEqual(
            Vertex.from_gtp('q16').as_gtp(),
            'q16'
        )

    def test_all(self):
        self.assertEqual(len(list(Vertex.all())), 361)

        for v in Vertex.all():
            self.assertEqual(Vertex.from_gtp(v.as_gtp()), v, f'{v.as_gtp()} is not the same before GTP serialization as after')
            self.assertEqual(Vertex.from_sgf(v.as_sgf()), v, f'{v.as_sgf()} is not the same before SGF serialization as after')

if __name__ == '__main__':
    unittest.main()
