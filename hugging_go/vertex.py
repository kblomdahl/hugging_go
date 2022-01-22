class Vertex:
    def __init__(self, s=None, *, x=None, y=None):
        self._x = x if x is not None else _LETTERS.index(s[0])
        self._y = y if y is not None else int(s[1:]) - 1

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __eq__(self, other):
        return self.x == other.y and self.y == other.y

_LETTERS = (
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't'
)
