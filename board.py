import random
from enum import Enum


class Util:
    @staticmethod
    def settle(arr, start):
        for i in range(start, 3):
            arr[i] = arr[i + 1]
        arr[3] = 0
        return arr

    @staticmethod
    def slide(arr):
        new_arr = [x for x in arr if x != 0]
        while len(new_arr) < 4:
            new_arr.append(0)
        return new_arr

    @staticmethod
    def compress(arr):
        arr = Util.slide(arr)

        for i in range(3):
            if arr[i] != 0 and arr[i] == arr[i + 1]:
                arr[i] *= 2
                arr = Util.settle(arr, i + 1)

        arr = Util.slide(arr)
        return arr


class RandomGenerator:
    @staticmethod
    def generate_position():
        return (random.randint(0, 3), random.randint(0, 3))

    @staticmethod
    def generate_block():
        return 2 if random.random() < 0.9 else 4


class Board:
    def __init__(self):
        self.grid = [[0] * 4 for _ in range(4)]

        row1, col1 = RandomGenerator.generate_position()
        row2, col2 = RandomGenerator.generate_position()
        while (row1, col1) == (row2, col2):
            row2, col2 = RandomGenerator.generate_position()

        self.grid[row1][col1] = RandomGenerator.generate_block()
        self.grid[row2][col2] = RandomGenerator.generate_block()

    def spawn_tile(self):
        empty = []
        for r in range(4):
            for c in range(4):
                if self.grid[r][c] == 0:
                    empty.append((r, c))

        if not empty:
            return False

        row, col = random.choice(empty)
        self.grid[row][col] = RandomGenerator.generate_block()
        return True

    def move_left(self):
        moved = False
        for i in range(4):
            old_row = self.grid[i][:]
            self.grid[i] = Util.compress(self.grid[i])
            if self.grid[i] != old_row:
                moved = True
        return moved

    def move_right(self):
        moved = False
        for i in range(4):
            old_row = self.grid[i][:]
            reversed_row = self.grid[i][::-1]
            new_row = Util.compress(reversed_row)[::-1]
            self.grid[i] = new_row
            if self.grid[i] != old_row:
                moved = True
        return moved

    def move_up(self):
        moved = False
        for col in range(4):
            old_col = [self.grid[row][col] for row in range(4)]
            new_col = Util.compress(old_col)

            for row in range(4):
                self.grid[row][col] = new_col[row]

            if new_col != old_col:
                moved = True
        return moved

    def move_down(self):
        moved = False
        for col in range(4):
            old_col = [self.grid[row][col] for row in range(4)]
            reversed_col = old_col[::-1]
            new_col = Util.compress(reversed_col)[::-1]

            for row in range(4):
                self.grid[row][col] = new_col[row]

            if new_col != old_col:
                moved = True
        return moved

    def print_board(self):
        for row in self.grid:
            print(row)
        print()


class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.pretty_print()

    def play_turn(self, direction):
        moved = False

        if direction == 'a':
            moved = self.board.move_left()
        elif direction == 'd':
            moved = self.board.move_right()
        elif direction == 'w':
            moved = self.board.move_up()
        elif direction == 's':
            moved = self.board.move_down()

        if moved:
            self.board.spawn_tile()

        self.pretty_print()
        
        return moved
    
    def pretty_print(self):
        for row in self.board.grid:
            print(*row)
        print()