from hugging_go.minimax import minimax
from hugging_go.color import Color

import unittest

class TestMiniMax(unittest.TestCase):
    def test_greedy(self):
        def _pipe(seq, _, **kwargs):
            if seq == []:
                return [[{ 'label': 'a', 'score': 0.5 }, { 'label': 'b', 'score': 0.5 }], 0.0, None]
            elif seq == ['a']:
                return [[], -1.0, None]
            elif seq == ['b']:
                return [[], 1.0, None]

        [best_candidate, _] = minimax(
            _pipe,
            [],
            Color('B'),
            depth=1,
            tfs_z=1.0
        )

        self.assertEqual(best_candidate.label, 'b')
        self.assertEqual(best_candidate.value, -1.0)

    def test_non_greedy(self):
        def _pipe(seq, _, **kwargs):
            if seq == []:
                return [[{ 'label': 'a', 'score': 0.5 }, { 'label': 'b', 'score': 0.5 }], 0.0, None]
            elif seq == ['a']:
                return [[{ 'label': 'a', 'score': 0.5 }, { 'label': 'b', 'score': 0.5 }], 0.0, None]
            elif seq == ['b']:
                return [[{ 'label': 'a', 'score': 0.5 }, { 'label': 'b', 'score': 0.5 }], 0.0, None]
            elif seq == ['a', 'a']:
                return [[], 0.1, None]
            elif seq == ['a', 'b']:
                return [[], 0.4, None]
            elif seq == ['b', 'a']:
                return [[], 0.2, None]
            elif seq == ['b', 'b']:
                return [[], 0.3, None]

        [best_candidate, _] = minimax(
            _pipe,
            [],
            Color('B'),
            depth=2,
            tfs_z=1.0
        )

        self.assertEqual(best_candidate.label, 'b')
        self.assertEqual(best_candidate.value, 0.3)
        self.assertEqual(best_candidate.child.label, 'b')

if __name__ == '__main__':
    unittest.main()
