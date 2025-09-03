from random import randint

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
        self.hidden_visual = [['O']*6 for _ in range(6)]
        self.ships = set()
        self.count_of_ships = {'1': 0, '2': 0, '3': 0}
        self.hid = hid
    state = [Dot(x, y) for y in range(1, 7) for x in range(1, 7)]

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

    def display(self):
        if not self.hid:
            print(' ' * 3, '1', '  2   3   4   5   6')
            for x in range(1, len(self.visual)+1):
                print(f'{x}', *self.visual[x-1], sep=' | ', end=' |')
                print()
        else:
            print(' ' * 3, '1', '  2   3   4   5   6')
            for x in range(1, len(self.hidden_visual) + 1):
                print(f'{x}', *self.hidden_visual[x - 1], sep=' | ', end=' |')
                print()



    def shot(self, dot: Dot):
        if dot not in self.state or self.visual[dot._y - 1][dot._x - 1] == 'T' or self.visual[dot._y - 1][dot._x - 1] == 'X':
            raise ValueError
        elif self.visual[dot._y - 1][dot._x - 1] == 'O':
            self.visual[dot._y - 1][dot._x - 1] = 'T'
            self.hidden_visual[dot._y - 1][dot._x - 1] = 'T'
        elif self.visual[dot._y - 1][dot._x - 1] == '■':
            self.visual[dot._y - 1][dot._x - 1] = 'X'
            self.hidden_visual[dot._y - 1][dot._x - 1] = 'X'

class Player:
    def __init__(self, selfboard: Board, enemyboard: Board):
        self.selfboard = selfboard
        self.enemyboard = enemyboard

    def ask(self):
        pass

    def move(self, flag=None):
        flag = True
        dot = self.ask()
        try:
            self.enemyboard.shot(dot)
        except ValueError:
            self.move()
        else:
            if self.enemyboard.visual[dot._y - 1][dot._x - 1] != 'X':
                flag = False
        return flag

class AI(Player):
    def ask(self):
        x, y = randint(1, 6), randint(1, 6)
        return Dot(x, y)

class User(Player):
    def ask(self):
        x, y = input('Введите координаты через пробел: ').split()
        return Dot(x, y)

class Game:
    def __init__(self, user: User, userboard: Board, comp: AI, compboard: Board):
        self.user = user
        self.userboard = userboard
        self.comp = comp
        self.compboard = compboard

    def random_board(self):
        brd = Board(False)

        while brd.count_of_ships['3'] < 1:
            count = 0
            while count < 100:
                ship = Ship(3, nose=Dot(randint(1, 6), randint(1, 6)), drctn=randint(0, 1))
                try:
                    brd.add_ship(ship)
                except ValueError:
                    count += 1
            return self.random_board() # если посл. влож. цикл завершился перепонением счётчика, значит нужна новая доска

        while brd.count_of_ships['2'] < 2:
            count = 0
            while count < 10_000:
                ship = Ship(2, nose=Dot(randint(1, 6), randint(1, 6)), drctn=randint(0, 1))
                try:
                    brd.add_ship(ship)
                except ValueError:
                    count += 1
            return self.random_board()

        while brd.count_of_ships['1'] < 4:
            count = 0
            while count < 20_000:
                ship = Ship(2, nose=Dot(randint(1, 6), randint(1, 6)), drctn=randint(0, 1))
                try:
                    brd.add_ship(ship)
                except ValueError:
                    count += 1
            return self.random_board()

        return brd

    def greet(self):
        pass

    def loop(self):
        usrbrd = self.random_board()
        cmpbrd = self.random_board()
        usr = User(usrbrd, cmpbrd)
        cmp = AI(cmpbrd, usrbrd)





ship1 = Ship(3, Dot(6, 6), 0)
ship2 = Ship(2, Dot(2, 1), 1)
pl1_board = Board(False)
pl1_board.add_ship(ship1)
pl1_board.add_ship(ship2)
pl1_board.display()
print()
pl1_board.shot(Dot(1, 1))
pl1_board.shot(Dot(2, 1))
pl1_board.shot(Dot(3, 1))
pl1_board.display()



