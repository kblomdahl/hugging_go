import unittest
from hugging_go.gtp import Gtp

class TestGtp(unittest.TestCase):
    def setUp(self):
        self.gtp = Gtp()

    def test_empty(self):
        self.assertEqual(
            self.gtp.process(''),
            None
        )

    def test_unknown_command(self):
        self.assertEqual(
            self.gtp.process('this-command-does-not-exist'),
            '? unknown command\n\n'
        )

    def test_protocol_version(self):
        self.assertEqual(
            self.gtp.process('protocol_version'),
            '= 2\n\n'
        )

    def test_name(self):
        self.assertEqual(
            self.gtp.process('name'),
            '= hugging_go\n\n'
        )

    def test_version(self):
        self.assertEqual(
            self.gtp.process('version'),
            '= 0\n\n'
        )

if __name__ == '__main__':
    unittest.main()
