from hugging_go.model import pretrained_model
from hugging_go.vertex import Vertex

import unittest

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.pipe = pretrained_model()

    def test_shape(self):
        candidates = self.pipe('')
        self.assertEqual(len(candidates), 1)
        self.assertEqual(len(candidates[0]), 362)

    def test_softmax(self):
        candidates = self.pipe('')
        self.assertAlmostEqual(sum([cand['score'] for cand in candidates[0]]), 1.0, places=5)

    def test_labels(self):
        candidates = self.pipe('')
        labels = set([cand['label'] for cand in candidates[0]])

        for v in Vertex.all():
            self.assertIn(v.as_gtp(), labels)

if __name__ == '__main__':
    unittest.main()
