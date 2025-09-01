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

    def __hash__(self):
        return hash((self._x, self._y))


class Ship:
    def __init__(self, length: int, nose: Dot, drctn: int): #если drctn==0 => направление вертикальное, 1 = горизонтальное
        self._length = length
        self._nose = nose
        self._drctn = drctn
        self._life = length

    def __eq__(self, other):
        return self._length == other._length and self._drctn == other._drctn

    @property
    def dots(self):
        if self._drctn == 0:
            return [Dot(self._nose._x, y) for y in range(self._nose._y - self._length + 1, self._nose._y + 1)]
        elif self._drctn == 1:
            return [Dot(x, self._nose._y) for x in range(self._nose._x - self._length + 1, self._nose._x + 1)]

    @property
    def get_shipdots(self):
        return [str(i) for i in self.dots]


class Board:
    def __init__(self, hid: bool):
        self.visual = [['O']*6 for _ in range(6)] # это буква, а не ноль
        self.ships = set()
        self.count_of_ships = {'1': 0, '2': 0, '3': 0}
        self.hid = True
        # self.contour = self.ships мб без контура
    state = [Dot(x, y) for y in range(1, 7) for x in range(1, 7)]
    count_ships = 0

    @property
    def get_shipsdots(self):
        return [str(i) for i in self.ships]

    def add_ship(self, ship: Ship):
        flag = True

        if ship._length == 3 and self.count_of_ships['3'] == 1:
            raise ValueError
        elif ship._length == 3:
            self.count_of_ships['3'] += 1
        elif ship._length == 2 and self.count_of_ships['2'] == 2:
            raise ValueError
        elif ship._length == 2:
            self.count_of_ships['2'] += 1
        elif ship._length == 1 and self.count_of_ships['1'] == 4:
            raise ValueError
        elif ship._length == 1:
            self.count_of_ships['1'] += 1

        for dot in ship.dots:
            if (dot not in self.state) or (dot in self.ships):
                flag = False
        if flag:
            for dot in ship.dots:
                self.visual[dot._y - 1][dot._x - 1] = '■'
                # self.ships.add(dot) мб без контура
                for x in range(dot._x - 1, dot._x + 2):
                    for y in range(dot._y - 1, dot._y + 2):
                        self.ships.add(Dot(x, y))
        else:
            raise ValueError

    def shot(self, dot: Dot):
        if dot not in self.state or self.visual[dot._y - 1][dot._x - 1] == 'T' or self.visual[dot._y - 1][dot._x - 1] == 'X':
            raise ValueError
        elif self.visual[dot._y - 1][dot._x - 1] == 'O':
            self.visual[dot._y - 1][dot._x - 1] = 'T'
        elif self.visual[dot._y - 1][dot._x - 1] == '■':
            self.visual[dot._y - 1][dot._x - 1] = 'X'

class Player:
    pass

ship1 = Ship(3, Dot(6, 6), 0)
ship2 = Ship(2, Dot(2, 1), 1)
pl1_board = Board(True)
pl1_board.add_ship(ship1)
pl1_board.add_ship(ship2)
print(*pl1_board.visual, sep='\n')
print()
pl1_board.shot(Dot(1, 1))
pl1_board.shot(Dot(2, 1))
pl1_board.shot(Dot(3, 1))
print(*pl1_board.visual, sep='\n')



