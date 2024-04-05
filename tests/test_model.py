from hugging_go.color import Color
from hugging_go.model import pretrained_model
from hugging_go.vertex import Vertex

import unittest

class TestModel(unittest.TestCase):
    def setUp(self):
        self.pipe = pretrained_model()

    def test_shape(self):
        candidates = self.pipe('', Color('B'))
        self.assertEqual(len(candidates), 1)
        self.assertEqual(len(candidates[0]), 362)

    def test_softmax(self):
        candidates = self.pipe('', Color('B'))
        self.assertAlmostEqual(sum([cand['score'] for cand in candidates[0]]), 1.0, places=5)

    def test_black_labels(self):
        candidates = self.pipe('', Color('B'))
        labels = set([cand['label'] for cand in candidates[0]])

        for v in Vertex.all():
            self.assertIn('B' + v.as_gtp(), labels)

    def test_white_labels(self):
        candidates = self.pipe('Bd4', Color('W'))
        labels = set([cand['label'] for cand in candidates[0]])

        for v in Vertex.all():
            self.assertIn('W' + v.as_gtp(), labels)

if __name__ == '__main__':
    unittest.main()
