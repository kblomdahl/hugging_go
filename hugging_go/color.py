
class Color:
    def __init__(self, s):
        self.s = s

    def opposite(self):
        if self.color == 'b':
            return Color('w')
        else:
            return Color('b')

    def __int__(self):
        if self.s == 'b':
            return 0
        elif self.s == 'w':
            return 1
        else:
            raise ValueError()
