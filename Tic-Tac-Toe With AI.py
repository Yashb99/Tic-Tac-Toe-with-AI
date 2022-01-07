import random


class PlayerIsUser:
    def __init__(self, field, level, item):
        self.coord = []
        self.field = field
        self.item = item
        self.level = level

    def get_coordinates(self):
        while True:
            print('Enter the coordinates: ')
            self.coord = input().split()  # coord[0] - row and coord[1] - col
            # check the two coordinates is digits
            if not self.coord[0].isdigit() or not self.coord[1].isdigit():
                print('You should enter numbers!')
                continue
            if len(self.coord) != 2:
                print('You should enter two numbers of coordinates.')
                continue
            self.coord = [int(ui) - 1 for ui in self.coord]
            if not (0 <= self.coord[0] < 3 and 0 <= self.coord[1] < 3):
                print('Coordinates should be from 1 to 3!')
                continue
            self.coord[1] = 2 - self.coord[1]
            self.coord[0], self.coord[1] = self.coord[1], self.coord[0]
            if self.field[self.coord[0]][self.coord[1]] != ' ':
                print('This cell is occupied! Choose another one!')
                continue
            break

    def make_move(self):
        self.get_coordinates()
        self.field[self.coord[0]][self.coord[1]] = self.item


class PlayerIsAI:
    def __init__(self, field, level, item):
        self.coord = []
        self.field = field
        self.level = level
        self.item = item
        self.item_opponent = 'O' if item == 'X' else 'X'

    def get_ai_coord_for_easy(self):
        empty_cells = [[row, col] for row in range(len(self.field))
                       for col in range(len(self.field[row]))
                       if self.field[row][col] == ' ']
        self.coord = random.choice(empty_cells)

    def get_priority_cell(self, item):
        for row in range(len(self.field)):
            if self.field[row].count(item) == 2 and self.field[row].count(' ') == 1:
                self.coord = [row, self.field[row].index(' ')]
                return True
        for col in range(len(self.field[0])):
            column = [self.field[row][col] for row in range(len(self.field))]
            if column.count(item) == 2 and column.count(' ') == 1:
                self.coord = [column.index(' '), col]
                return True
        diag = [self.field[i][i] for i in range(len(self.field))]
        if diag.count(item) == 2 and diag.count(' ') == 1:
            idx = diag.index(' ')
            self.coord = [idx, idx]
            return True
        diag = [self.field[i][len(self.field) - 1 - i] for i in range(len(self.field))]
        if diag.count(item) == 2 and diag.count(' ') == 1:
            idx = diag.index(' ')
            self.coord = [idx, len(self.field) - 1 - idx]
            return True
        return False

    def get_ai_coord_for_medium(self):
        if self.get_priority_cell(self.item):
            return
        if self.get_priority_cell(self.item_opponent):
            return
        empty_cells = [[row, col] for row in range(len(self.field))
                       for col in range(len(self.field[row]))
                       if self.field[row][col] == ' ']
        self.coord = random.choice(empty_cells)

    def max(self):
        maxv = -2
        x = None
        y = None
        result = TicTacToe.check_game_status(self)
        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result is True:
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.field[i][j] == ' ':
                    self.field[i][j] = 'O'
                    m, min_i, min_j = self.min()
                    if m > maxv:
                        maxv = m
                        x = i
                        y = j
                    self.field[i][j] = ' '
        return maxv, x, y

    def min(self):
        minv = 2
        x = None
        y = None
        result = TicTacToe.check_game_status(self)

        if result == 'X':
            return -1, 0, 0
        elif result == 'O':
            return 1, 0, 0
        elif result is True:
            return 0, 0, 0

        for i in range(0, 3):
            for j in range(0, 3):
                if self.field[i][j] == ' ':
                    self.field[i][j] = 'X'
                    m, max_i, max_j = self.max()
                    if m < minv:
                        minv = m
                        x = i
                        y = j
                    self.field[i][j] = ' '
        return minv, x, y

    def get_ai_coord_for_hard(self):
        # If it's X player
        if self.item == 'X':
            m, row, col = self.min()
            self.coord = [row, col]
        # If it's O player
        else:
            m, row, col = self.max()
            self.coord = [row, col]

    def make_move(self):
        if self.level == 'easy':
            self.get_ai_coord_for_easy()
            print('Making move level "easy"')
        elif self.level == 'medium':
            self.get_ai_coord_for_medium()
            print('Making move level "medium"')
        else:
            self.get_ai_coord_for_hard()
            print('Making move level "hard"')
        self.field[self.coord[0]][self.coord[1]] = self.item


class TicTacToe:
    def __init__(self):
        self.player_1 = None
        self.player_2 = None
        self.command = ['easy', 'medium', 'hard', 'user']
        self.field = [[' ', ' ', ' '],  # (1, 3) (2, 3) (3, 3)
                      [' ', ' ', ' '],  # (1, 2) (2, 2) (3, 2)
                      [' ', ' ', ' ']]  # (1, 1) (2, 1) (3, 1)
        self.game_logic()

    def print_field(self):
        print('---------')
        for i in range(3):
            out = '| '
            for j in range(3):
                out += self.field[i][j] + ' '
            out += '|'
            print(out)
        print('---------')

    def check_game_status(self):
        for i in range(0, 3):
            if self.field[i] == ['X', 'X', 'X']:
                return 'X'
            elif self.field[i] == ['O', 'O', 'O']:
                return 'O'
        for i in range(0, 3):
            if (self.field[0][i] != ' ' and
                    self.field[0][i] == self.field[1][i] and
                    self.field[1][i] == self.field[2][i]):
                return self.field[0][i]
        if (self.field[0][0] != ' ' and
                self.field[0][0] == self.field[1][1] and
                self.field[0][0] == self.field[2][2]):
            return self.field[0][0]
        if (self.field[0][2] != ' ' and
                self.field[0][2] == self.field[1][1] and
                self.field[0][2] == self.field[2][0]):
            return self.field[0][2]
        for row in self.field:
            if ' ' in row:
                return False
        return True

    def command_handler(self):
        while True:
            print('Input command:')
            user_input = input().split()
            if user_input[0] == 'exit':
                return False
            if len(user_input) != 3 or user_input[0] != 'start':
                print('Bad parameters!')
                continue
            for i in range(1, 2):
                if not any(user_input[i] == command for command in self.command):
                    print('Bad parameters!')
                    continue
            if user_input[1] == 'user':
                self.player_1 = PlayerIsUser(self.field, user_input[1], 'X')
            else:
                self.player_1 = PlayerIsAI(self.field, user_input[1], 'X')
            if user_input[2] == 'user':
                self.player_2 = PlayerIsUser(self.field, user_input[2], 'O')
            else:
                self.player_2 = PlayerIsAI(self.field, user_input[2], 'O')
            return True

    def game_logic(self):
        if self.command_handler():
            self.print_field()
            whose_turn = 1
            while True:
                if whose_turn == 1:
                    self.player_1.make_move()
                    self.print_field()
                    whose_turn = 2
                else:
                    self.player_2.make_move()
                    self.print_field()
                    whose_turn = 1

                winner = self.check_game_status()
                if winner is True:
                    print('Draw')
                    break
                if winner == 'X' or winner == 'O':
                    print(winner, 'wins')
                    break


tic = TicTacToe()
