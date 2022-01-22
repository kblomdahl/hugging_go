from hugging_go.tokenizer import pretrained_tokenizer

import unittest

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = pretrained_tokenizer()

    def test_tokenize(self):
        sequence = 'q16 d4 q3 d17 r9 o17 q14 k16 d15'

        self.assertEqual(
            self.tokenizer.tokenize(sequence),
            ['q16', 'd4', 'q3', 'd17', 'r9', 'o17', 'q14', 'k16', 'd15']
        )

    def test_all_moves(self):
        for x in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'):
            for y in range(1, 20):
                ids = self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(f'{x}{y}'))

                self.assertNotEqual(
                    ids,
                    [0], # `0` is the `[UNK]` token
                    f'missing token for `{x}{y}`'
                )
                self.assertEqual(len(ids), 1, f'is split into more than one token `{x}{y}`')

if __name__ == '__main__':
    unittest.main()
