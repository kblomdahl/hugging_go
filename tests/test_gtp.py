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

if __name__ == '__main__':
    unittest.main()
