from hugging_go.beam_search import beam_search

import unittest

class TestBeamSearch(unittest.TestCase):
    def test_greedy(self):
        best_candidate = beam_search(
            lambda _: [
                { 'label': 'a', 'score': 0.9 },
                { 'label': 'b', 'score': 0.1 }
            ],
            [],
            k=2,
            depth=3
        )

        self.assertEqual(best_candidate.label, 'a')
        self.assertEqual(best_candidate.sequence, ['a', 'a', 'a'])

    def test_non_greedy(self):
        def _pipe(seq):
            if seq == []:
                return [
                    { 'label': 'a', 'score': 0.1 },
                    { 'label': 'b', 'score': 0.9 },
                ]
            elif seq == ['a']:
                return [
                    { 'label': 'a', 'score': 0.4 },
                    { 'label': 'b', 'score': 0.6 },
                ]
            elif seq == ['b']:
                return [
                    { 'label': 'a', 'score': 0.05 },
                    { 'label': 'b', 'score': 0.01 },
                ]

        best_candidate = beam_search(
            _pipe,
            [],
            k=3,
            depth=2
        )

        self.assertEqual(best_candidate.label, 'a')
        self.assertEqual(best_candidate.sequence, ['a', 'b'])

if __name__ == '__main__':
    unittest.main()
