from collections import namedtuple
import unittest
from hugging_go.gtp import Gtp

FakeBoard = namedtuple('Board', ['size', 'komi'])

class FakeBoardFactory:
    def build(self, board_size, komi):
        return FakeBoard(size=board_size, komi=komi)

class FakeAgent:
    def play(self, board, color, vertex):
        return True if vertex == 'd4' else False

class TestGtp(unittest.TestCase):
    def setUp(self):
        self.gtp = Gtp(agent=FakeAgent(), board_factory=FakeBoardFactory())

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

    def test_known_command(self):
        self.assertEqual(
            self.gtp.process('known_command'),
            '? syntax error\n\n'
        )
        self.assertEqual(
            self.gtp.process('known_command protocol_version'),
            '= true\n\n'
        )
        self.assertEqual(
            self.gtp.process('known_command this-command-does-not-exist'),
            '= false\n\n'
        )

    def test_list_commands(self):
        commands = self.gtp.process('list_commands')
        self.assertNotEqual(commands, '? unknown command\n\n')

        for command in commands.lstrip('= ').split('\n'):
            if not command:
                continue

            self.assertEqual(
                self.gtp.process(f'known_command {command}'),
                '= true\n\n'
            )

    def test_quit(self):
        self.assertEqual(self.gtp.is_running, True)
        self.assertEqual(self.gtp.process('quit'), '= \n\n')
        self.assertEqual(self.gtp.is_running, False)

    def test_boardsize(self):
        self.assertEqual(
            self.gtp.process('boardsize'),
            '? syntax error\n\n'
        )
        self.assertEqual(
            self.gtp.process('boardsize 9'),
            '? unacceptable size\n\n'
        )
        self.assertEqual(
            self.gtp.process('boardsize 19'),
            '= \n\n'
        )

    def test_clear_board(self):
        self.assertEqual(
            self.gtp.process('boardsize 19'),
            '= \n\n'
        )
        self.assertEqual(
            self.gtp.process('komi 7.5'),
            '= \n\n'
        )
        self.assertEqual(
            self.gtp.process('clear_board'),
            '= \n\n'
        )
        self.assertEqual(
            self.gtp.board,
            FakeBoard(size=19, komi=7.5)
        )

    def test_komi(self):
        self.assertEqual(
            self.gtp.process('komi'),
            '? syntax error\n\n'
        )
        self.assertEqual(
            self.gtp.process('komi this-is-not-a-number'),
            '? syntax error\n\n'
        )
        self.assertEqual(
            self.gtp.process('komi -5.5'),
            '= \n\n'
        )

    def test_play(self):
        self.assertEqual(
            self.gtp.process('play'),
            '? syntax error\n\n'
        )
        self.assertEqual(
            self.gtp.process('play b d4'),
            '= \n\n'
        )
        self.assertEqual(
            self.gtp.process('play w d16'),
            '? illegal move\n\n'
        )

if __name__ == '__main__':
    unittest.main()
