class Dot:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other._x and self._y == other._y

    def __str__(self):
        return f'Dot({self._x}, {self._y})'


class Ship:
    def __init__(self, length: int, nose: Dot, drctn: int): #если drctn==0 => направление вертикальное, 1 = горизонтальное
        self.__length = length
        self.__nose = nose
        self.__drctn = drctn
        self.__life = length

    def __eq__(self, other):
        return self.__length == other.length and self.__drctn == other.__drctn
    @property
    def dots(self):
        if self.__drctn == 0:
            return [Dot(self.__nose._x, y) for y in range(self.__nose._y - self.__length + 1, self.__nose._y + 1)]
        elif self.__drctn == 1:
            return [Dot(x, self.__nose._y) for x in range(self.__nose._x - self.__length + 1, self.__nose._x + 1)]


class Board:
    def __init__(self):
        self.visual = [['О']*6 for _ in range(6)]

    state = [Dot(x, y) for y in range(1, 7) for x in range(1, 7)]
    hid = True
    count_alive = 0

    def add_ship(self, ship):
        flag = True
        for dot in ship.dots:
            if dot not in Board.state:
                flag = False
        if flag:
            for dot in ship.dots:
                self.visual[dot._y-1][dot._x-1] = '■'


class Player:
    pass
ship1 = Ship(2, Dot(4, 3), 1)
pl1_board = Board()
pl1_board.add_ship(ship1)
print(*pl1_board.visual, sep='\n')


