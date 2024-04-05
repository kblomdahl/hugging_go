from hugging_go.tokenizer import pretrained_tokenizer

import unittest

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = pretrained_tokenizer()

    def test_tokenize(self):
        sequence = 'Wq16 Bd4 Wq3 Bd17 Wr9 Bo17 Wq14 Bk16 Wd15'

        self.assertEqual(
            self.tokenizer.tokenize(sequence),
            ['Wq16', 'Bd4', 'Wq3', 'Bd17', 'Wr9', 'Bo17', 'Wq14', 'Bk16', 'Wd15']
        )

    def test_cls_sep(self):
        cls_token_id, sep_token_id = self.tokenizer.convert_tokens_to_ids(['[CLS]', '[SEP]'])

        self.assertEqual(
            self.tokenizer('').input_ids,
            [cls_token_id, sep_token_id]
        )
        self.assertEqual(
            len(self.tokenizer('Bq16 Wd4 Bq3 Wd17 Br9 Wo17 Bq14 Wk16 Bd15').input_ids),
            11
        )

    def test_all_moves(self):
        for color in ('B', 'W'):
            for x in ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'):
                for y in range(1, 20):
                    ids = self.tokenizer.convert_tokens_to_ids(self.tokenizer.tokenize(f'{color}{x}{y}'))

                    self.assertNotEqual(
                        ids,
                        [0], # `0` is the `[UNK]` token
                        f'missing token for `{color}{x}{y}`'
                    )
                    self.assertEqual(len(ids), 1, f'is split into more than one token `{color}{x}{y}`')

if __name__ == '__main__':
    unittest.main()
