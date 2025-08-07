class Dot:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __str__(self):
        return f'Dot: {self._x}_{self._y}'


class Ship(Dot):
    def __init__(self, length=0, nose=Dot(0, 0), drctn='вертикально'):
        self.__length = length
        self.__nose = nose
        self.__drctn = drctn
        self.__life = length

    def __eq__(self, other):
        return self.__length == other.length and self.__drctn == other.__drctn
    @property
    def dots(self):
        if self.__drctn == 'вертикально':
            return [str(Dot(self.__nose._x, i)) for i in range(self.__nose._y - self.__length + 1, self.__nose._y + 1)]
        else:
            return 

ship1 = Ship(3, nose=Dot(6, 6), drctn='вертикально')
print(ship1.dots)

