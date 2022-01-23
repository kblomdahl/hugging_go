class Vertex:
    def __init__(self, s=None, *, x=None, y=None):
        self._x = x if x is not None else _GTP_LETTERS.index(s[0])
        self._y = y if y is not None else int(s[1:]) - 1

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def as_gtp(self):
        return f'{_GTP_LETTERS[self.x]}{self.y + 1}'

    def __eq__(self, other):
        return self.x == other.y and self.y == other.y

_GTP_LETTERS = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't'
)
