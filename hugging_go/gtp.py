from .color import Color
from .vertex import Vertex

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

class IllegalMove(Error):
    def __init__(self):
        super(IllegalMove, self).__init__('illegal move')

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
        ('protocol_version', 'name', 'version', 'known_command', 'list_commands', 'quit', 'boardsize', 'clear_board', 'komi', 'play', 'genmove')
    )

    def __init__(self, *, agent=None, board_factory=None):
        self._is_running = True
        self._agent = agent
        self._board_factory = board_factory
        self._board_size = 19
        self._komi = 5.5
        self.setUp()

    def setUp(self):
        self._board = self._board_factory.build(
            self._board_size,
            self._komi
        )

    @property
    def is_running(self):
        return self._is_running

    @property
    def board(self):
        return self._board

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
        elif tokens[0] == 'komi':
            reply = self.komi(tokens[1:])
        elif tokens[0] == 'play':
            reply = self.play(tokens[1:])
        elif tokens[0] == 'genmove':
            reply = self.genmove(tokens[1:])
        else:
            reply = UnknownCommand()

        return str(reply.with_id(id))

    def preprocess(self, line):
        parts = re.split(r'\s+', line.strip())

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
        self._is_running = False

        return Success('')

    def boardsize(self, line):
        if not line or not line[0].isnumeric():
            return SyntaxError()

        size = int(line[0])
        if size != 19:
            return UnacceptableSize()
        else:
            self._board_size = size
            return Success('')

    def clear_board(self, line):
        self.setUp()
        return Success('')

    def komi(self, line):
        if not line:
            return SyntaxError()

        try:
            self._komi = float(line[0])
            return Success('')
        except ValueError:
            return SyntaxError()

    def play(self, line):
        if len(line) != 2:
            return SyntaxError()

        try:
            [color, vertex] = line
            color = _normalize_color(color)
            vertex = _normalize_vertex(vertex)

            if self._agent.play(self._board, color, vertex):
                return Success('')
            else:
                return IllegalMove()
        except ValueError:
            return SyntaxError()

    def genmove(self, line):
        if len(line) != 1:
            return SyntaxError()

        try:
            color = _normalize_color(line[0])
            vertex = self._agent.genmove(self._board, color)

            return Success(vertex)
        except ValueError:
            return SyntaxError()


def _normalize_color(color):
    color = color.lower()

    if color == 'black' or color == 'b':
        return Color('b')
    elif color == 'white' or color == 'w':
        return Color('w')
    else:
        raise ValueError()

def _normalize_vertex(vertex):
    vertex = vertex.lower()

    if re.match(r'[a-z][0-9]+', vertex):
        return Vertex.from_gtp(vertex)
    else:
        raise ValueError()
