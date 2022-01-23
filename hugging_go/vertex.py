class Vertex:
    def __init__(self, *, x=None, y=None):
        self._x = x
        self._y = y

    def from_gtp(s):
        return Vertex(
            x=_GTP_LETTERS.index(s[0]),
            y=int(s[1:]) - 1
        )

    def from_sgf(s):
        if len(s) != 2:
            raise ValueError()
        else:
            return Vertex(
                x=_SGF_LETTERS.index(s[0]),
                y=_SGF_LETTERS.index(s[1])
            )

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def is_valid(self):
        return self._x >= 0 and self._x <= 18 and self._y >= 0 and self._y <= 18

    def as_gtp(self):
        return f'{_GTP_LETTERS[self.x]}{self.y + 1}'

    def as_sgf(self):
        return f'{_SGF_LETTERS[self.x]}{_SGF_LETTERS[self.y]}'

    def __eq__(self, other):
        return self.x == other.y and self.y == other.y

_GTP_LETTERS = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't'
)

_SGF_LETTERS = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'
)
