from game import Board


class AI:
    def __init__(self):
        self.Moves = ['a', 'd', 'w', 's']

    def clone_board(self, board):
        cloned = Board.__new__(Board)
        cloned.grid = [row[:] for row in board.grid]
        return cloned

    def simulated_turn(self, board, direction):
        moved = False
        new_board = self.clone_board(board)

        if direction == 'a':
            moved, _ = new_board.move_left()
        elif direction == 'd':
            moved, _ = new_board.move_right()
        elif direction == 'w':
            moved, _ = new_board.move_up()
        elif direction == 's':
            moved, _ = new_board.move_down()

        return new_board, moved

    def expectimax(self, board, depth, player):
        if depth == 0:
            return Heuristics.heuristic(board)

        if player:
            best_value = float('-inf')
            moved_any = False

            for move in self.Moves:
                simulated_board, moved = self.simulated_turn(board, move)
                if not moved:
                    continue

                moved_any = True
                value = self.expectimax(simulated_board, depth - 1, False)
                best_value = max(best_value, value)

            if not moved_any:
                return Heuristics.heuristic(board)

            return best_value

        else:
            empty = board.empty_cells()

            if not empty:
                return self.expectimax(board, depth - 1, True)

            expected_value = 0.0
            p = 1 / len(empty)

            for r, c in empty:
                # Case where random piece is 2 
                board2 = self.clone_board(board)
                board2.grid[r][c] = 1
                expected_value += p * 0.9 * self.expectimax(board2, depth - 1, True)

                # Case where random piece is 4
                board4 = self.clone_board(board)
                board4.grid[r][c] = 2
                expected_value += p * 0.1 * self.expectimax(board4, depth - 1, True)

            return expected_value

    def move_ai(self, board):
        empty_count = len(board.empty_cells())

        if empty_count == 0:
            depth = 6
        elif empty_count <= 2:
            depth = 5
        else:
            depth = 3

        best_move = None
        best_value = float('-inf')

        for move in self.Moves:
            simulated_board, moved = self.simulated_turn(board, move)
            if not moved:
                continue

            value = self.expectimax(simulated_board, depth, False)

            if value >= best_value:
                best_value = value
                best_move = move

        return best_move


class Helper:
    @staticmethod
    def transpose(grid):
        return [list(row) for row in zip(*grid)]

    @staticmethod
    def rotate(grid):
        return [list(row) for row in zip(*grid[::-1])]


class Heuristics:
    @staticmethod
    def heuristic(board):
        return (
            12.0 * Heuristics.snake_pattern_heuristic(board)
        )

    @staticmethod
    def get_snake_patterns():
        snake1 = [
            [16, 15, 14, 13],
            [9, 10, 11, 12],
            [8, 7, 6, 5],
            [1, 2, 3, 4]
        ]

        snake2 = Helper.transpose(snake1)
        patterns = []

        for snake in [snake1, snake2]:
            current = [row[:] for row in snake]
            for _ in range(4):
                patterns.append([row[:] for row in current])
                current = Helper.rotate(current)

        return patterns

    @staticmethod
    def snake_pattern_heuristic(board):
        best_score = float("-inf")

        for pattern in Heuristics.get_snake_patterns():
            score = 0
            for r in range(4):
                for c in range(4):
                    exp = board.grid[r][c]
                    score += (2 ** exp) * pattern[r][c]
            best_score = max(best_score, score)

        return best_score