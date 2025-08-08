class Dot:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y

    def __eq__(self, other):
        if not isinstance(other, Dot):
            return False
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
    def __init__(self, hid: bool):
        self.visual = [['O']*6 for _ in range(6)]
        self.ships = set()
        self.count_of_ships = {'1': 0, '2': 0, '3': 0}
        self.hid = True
        self.contour = self.ships
    state = [Dot(x, y) for y in range(1, 7) for x in range(1, 7)]
    count_ships = 0

    def add_ship(self, ship: Ship):
        flag = True
        for dot in ship.dots:
            if dot not in Board.state:
                flag = False
            if flag:
                for dot in ship.dots:
                    self.visual[dot._y-1][dot._x-1] = '■'
                    self.ships.add(dot)
                    for x in range(dot._x-1, dot._x+2):
                        for y in range(dot._y-1, dot._y+2):
                            self.contour.add(Dot(x, y))
            else:
                raise ValueError

class Player:
    pass

ship1 = Ship(3, Dot(4, 6), 0)
pl1_board = Board(True)
# pl1_board.add_ship(ship1)
print(*pl1_board.visual, sep='\n')


