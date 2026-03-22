import random

BOARD_SIZE = 4

class LineOps:
    @staticmethod
    def slide(line):
        values = [x for x in line if x != 0]
        return values + [0] * (BOARD_SIZE - len(values))

    @staticmethod
    def merge(line):
        line = LineOps.slide(line)
        score_gained = 0

        for i in range(BOARD_SIZE - 1):
            if line[i] != 0 and line[i] == line[i + 1]:
                line[i] += 1
                score_gained += 2 ** line[i]
                line[i + 1] = 0

        line = LineOps.slide(line)
        return line, score_gained

class RandomGenerator:
    @staticmethod
    def generate_position(empty_cells):
        return random.choice(empty_cells)

    @staticmethod
    def generate_block():
        return 1 if random.random() < 0.9 else 2


class Board:
    def __init__(self):
        self.grid = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.spawn_tile()
        self.spawn_tile()

    def empty_cells(self):
        return [
            (r, c)
            for r in range(BOARD_SIZE)
            for c in range(BOARD_SIZE)
            if self.grid[r][c] == 0
        ]

    def spawn_tile(self):
        empty = self.empty_cells()
        if not empty:
            return False

        row, col = RandomGenerator.generate_position(empty)
        self.grid[row][col] = RandomGenerator.generate_block()
        return True

    def get_row(self, r):
        return self.grid[r][:]

    def set_row(self, r, row):
        self.grid[r] = row[:]

    def get_col(self, c):
        return [self.grid[r][c] for r in range(BOARD_SIZE)]

    def set_col(self, c, col):
        for r in range(BOARD_SIZE):
            self.grid[r][c] = col[r]
            
    def get_calculated_board(self):
        return [
            [0 if exp == 0 else 2 ** exp for exp in row]
            for row in self.grid
        ]

    def move_left(self):
        moved = False
        total_score = 0

        for r in range(BOARD_SIZE):
            old_row = self.get_row(r)
            new_row, gained = LineOps.merge(old_row)
            self.set_row(r, new_row)

            if new_row != old_row:
                moved = True
            total_score += gained

        return moved, total_score

    def move_right(self):
        moved = False
        total_score = 0

        for r in range(BOARD_SIZE):
            old_row = self.get_row(r)
            reversed_row = old_row[::-1]
            merged_row, gained = LineOps.merge(reversed_row)
            new_row = merged_row[::-1]
            self.set_row(r, new_row)

            if new_row != old_row:
                moved = True
            total_score += gained

        return moved, total_score

    def move_up(self):
        moved = False
        total_score = 0

        for c in range(BOARD_SIZE):
            old_col = self.get_col(c)
            new_col, gained = LineOps.merge(old_col)
            self.set_col(c, new_col)

            if new_col != old_col:
                moved = True
            total_score += gained

        return moved, total_score

    def move_down(self):
        moved = False
        total_score = 0

        for c in range(BOARD_SIZE):
            old_col = self.get_col(c)
            reversed_col = old_col[::-1]
            merged_col, gained = LineOps.merge(reversed_col)
            new_col = merged_col[::-1]
            self.set_col(c, new_col)

            if new_col != old_col:
                moved = True
            total_score += gained

        return moved, total_score

    def can_move(self):
        if self.empty_cells():
            return True

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return True

        for r in range(BOARD_SIZE - 1):
            for c in range(BOARD_SIZE):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return True

        return False

    def max_exponent(self):
        return max(max(row) for row in self.grid)

    def max_value(self):
        exp = self.max_exponent()
        return 0 if exp == 0 else 2 ** exp

    def avg_value(self):
        total = 0
        for row in self.grid:
            for exp in row:
                if exp != 0:
                    total += 2 ** exp
        return total / (BOARD_SIZE * BOARD_SIZE)

    def display_value(self, exp):
        return "." if exp == 0 else str(2 ** exp)

    def print_board(self):
        for row in self.grid:
            print(" ".join(f"{self.display_value(x):>5}" for x in row))
        print()

    def print_raw_board(self):
        for row in self.grid:
            print(row)
        print()

    def is_late_game(self):
        return self.max_exponent() >= 11

    def is_in_danger(self):
        return len(self.empty_cells()) <= 2


class Game:
    def __init__(self):
        self.board = Board()
        self.score = 0
        self.won = False
        self.game_over = False
        self.pretty_print()

    def play_turn(self, direction):
        if self.game_over:
            print("Game is already over.")
            return False

        moves = {
            "a": self.board.move_left,
            "d": self.board.move_right,
            "w": self.board.move_up,
            "s": self.board.move_down,
        }

        move_fn = moves.get(direction)
        if move_fn is None:
            print("Invalid move. Use w/a/s/d.")
            return False

        moved, gained = move_fn()

        if not moved:
            return False

        self.score += gained

        if self.board.has_won() and not self.won:
            self.won = True
            print("You win!")

        self.board.spawn_tile()

        if not self.board.can_move():
            self.game_over = True
            self.pretty_print()
            print("You lose!")
            return True

        return True

    def pretty_print(self):
        self.board.print_raw_board()
        print(f"Score: {self.score}")
        print()


if __name__ == "__main__":
    game = Game()

    while not game.game_over:
        move = input("Move (w/a/s/d): ").strip().lower()
        if game.play_turn(move):
            game.pretty_print()