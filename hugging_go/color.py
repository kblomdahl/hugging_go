
class Color:
    def __init__(self, s):
        self.s = s

    def opposite(self):
        if self.s == 'B':
            return Color('W')
        else:
            return Color('B')

    def __str__(self):
        return self.s

    def __int__(self):
        if self.s == 'B':
            return 1
        elif self.s == 'W':
            return 2
        else:
            raise ValueError()
