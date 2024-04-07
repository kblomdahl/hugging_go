from hugging_go.color import Color
from hugging_go.model import pretrained_model
from hugging_go.vertex import Vertex

import unittest

class TestModel(unittest.TestCase):
    def setUp(self):
        self.pipe = pretrained_model()

    def test_shape(self):
        [candidates, winner, _] = self.pipe('', Color('B'))
        self.assertEqual(len(candidates), 362)
        self.assertTrue(isinstance(winner, float))

    def test_softmax(self):
        [candidates, winner, _] = self.pipe('', Color('B'))
        self.assertAlmostEqual(sum([cand['score'] for cand in candidates]), 1.0, places=5)
        self.assertGreaterEqual(winner, -1.0)
        self.assertLessEqual(winner, 1.0)

    def test_black_labels(self):
        [candidates, _, _] = self.pipe('', Color('B'))
        labels = set([cand['label'] for cand in candidates])

        for v in Vertex.all():
            self.assertIn('B' + v.as_gtp(), labels)

    def test_white_labels(self):
        [candidates, _, _] = self.pipe('Bd4', Color('W'))
        labels = set([cand['label'] for cand in candidates])

        for v in Vertex.all():
            self.assertIn('W' + v.as_gtp(), labels)

if __name__ == '__main__':
    unittest.main()
