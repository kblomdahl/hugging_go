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

    def __init__(self):
        pass

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
        else:
            reply = UnknownCommand()

        return str(reply.with_id(id))

    def preprocess(self, line):
        parts = re.split(r'\W+', line.lstrip())

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
