import re
import sys

class Error:
    def __init__(self, message):
        self.message = message

    def with_id(self, id):
        self.id = id
        return self

    def __str__(self):
        if self.id is None:
            return f'? {self.message}\n\n'
        else:
            return f'?{self.id} {self.message}\n\n'

class UnknownCommand(Error):
    def __init__(self):
        super(UnknownCommand, self).__init__('unknown command')

class SyntaxError(Error):
    def __init__(self):
        super(SyntaxError, self).__init__('syntax error')

class UnacceptableSize(Error):
    def __init__(self):
        super(UnacceptableSize, self).__init__('unacceptable size')

class Success:
    def __init__(self, message):
        self.message = message

    def with_id(self, id):
        self.id = id
        return self

    def __str__(self):
        if self.id is None:
            return f'= {self.message}\n\n'
        else:
            return f'={self.id} {self.message}\n\n'

class Gtp:
    """ Go Text Protocol [1]

    [1] https://www.lysator.liu.se/~gunnar/gtp/gtp2-spec-draft2/gtp2-spec.html """

    KNOWN_COMMANDS = frozenset(
        ('protocol_version', 'name', 'version', 'known_command', 'list_commands', 'quit', 'boardsize', 'clear_board')
    )

    def __init__(self, *, board_factory=None):
        self.is_running = True
        self.board_factory = board_factory
        self.board_size = 19
        self.setUp()

    def setUp(self):
        self.board = self.board_factory.build(
            self.board_size
        )

    def process(self, line):
        id, tokens = self.preprocess(line)

        if not tokens or tokens[0] == '':
            return None
        elif tokens[0] == 'protocol_version':
            reply = self.protocol_version(tokens[1:])
        elif tokens[0] == 'name':
            reply = self.name(tokens[1:])
        elif tokens[0] == 'version':
            reply = self.version(tokens[1:])
        elif tokens[0] == 'known_command':
            reply = self.known_command(tokens[1:])
        elif tokens[0] == 'list_commands':
            reply = self.list_commands(tokens[1:])
        elif tokens[0] == 'quit':
            reply = self.quit(tokens[1:])
        elif tokens[0] == 'boardsize':
            reply = self.boardsize(tokens[1:])
        elif tokens[0] == 'clear_board':
            reply = self.clear_board(tokens[1:])
        else:
            reply = UnknownCommand()

        return str(reply.with_id(id))

    def preprocess(self, line):
        parts = re.split(r'\s+', line.lstrip())

        if parts[0].isnumeric():
            return int(parts[0]), parts[1:]
        else:
            return None, parts[0:]

    def protocol_version(self, line):
        return Success('2')

    def name(self, line):
        return Success('hugging_go')

    def version(self, line):
        return Success('0')

    def known_command(self, line):
        if len(line) != 1:
            return SyntaxError()

        if line[0] in self.KNOWN_COMMANDS:
            return Success('true')
        else:
            return Success('false')

    def list_commands(self, line):
        return Success('\n'.join(sorted(self.KNOWN_COMMANDS)))

    def quit(self, line):
        self.is_running = False

        return Success('')

    def boardsize(self, line):
        if not line or not line[0].isnumeric():
            return SyntaxError()

        size = int(line[0])
        if size != 19:
            return UnacceptableSize()
        else:
            self.board_size = size
            return Success('')

    def clear_board(self, line):
        self.setUp()
        return Success('')
