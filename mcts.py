import math
import random


class MCTSNode:

    def __init__(self, grid, parent=None, move=None, cumulative_score=0):
        self.grid = grid
        self.parent = parent
        self.move = move
        self.cumulative_score = cumulative_score 
        self.children = []
        self.visits = 0
        self.total_score = 0.0

    def is_fully_expanded(self):
        tried = {c.move for c in self.children}
        return tried == {'w', 'a', 's', 'd'}

    def best_child(self, c=100):
        return max(
            self.children,
            key=lambda n: (n.total_score / n.visits)
                        + c * math.sqrt(math.log(self.visits) / n.visits)
        )

    def untried_moves(self):
        tried = {c.move for c in self.children}
        return [m for m in ['w', 'a', 's', 'd'] if m not in tried]


class MCTS:
    def __init__(self, iterations=500, rollout_depth=5):
        self.iterations = iterations
        self.rollout_depth = rollout_depth

    def move_ai(self, board):
        if not board.can_move():
            return None

        root = MCTSNode([row[:] for row in board.grid])

        for _ in range(self.iterations):
            node = self._select(root)
            node = self._expand(node)
            score = self._simulate(node.grid, node.cumulative_score)
            self._backpropagate(node, score)

        if not root.children:
            return None

        return max(root.children, key=lambda n: n.visits).move


    def _select(self, node):
        while node.children and node.is_fully_expanded():
            if not self._can_move(node.grid):
                break
            node = node.best_child()
        return node

    def _expand(self, node):
        moves = node.untried_moves()
        if not moves or not self._can_move(node.grid):
            return node

        move = random.choice(moves)
        new_grid = [row[:] for row in node.grid]
        merge_points = self._apply_move(new_grid, move)

        if new_grid != node.grid:
            self._spawn_tile(new_grid)

        child = MCTSNode(
            new_grid,
            parent=node,
            move=move,
            cumulative_score=node.cumulative_score + merge_points
        )
        node.children.append(child)
        return child

    def _simulate(self, grid, current_score):
        g = [row[:] for row in grid]
        score = current_score

        for _ in range(self.rollout_depth):
            if not self._can_move(g):
                break
            valid = [m for m in ['w', 'a', 's', 'd'] if self._move_changes(g, m)]
            if not valid:
                break
            move = random.choice(valid)
            score += self._apply_move(g, move)
            self._spawn_tile(g)

        return score

    def _backpropagate(self, node, score):
        while node is not None:
            node.visits += 1
            node.total_score += score
            node = node.parent

    def _compress_row(self, row):
        r = [x for x in row if x != 0]
        points = 0
        i = 0
        while i < len(r) - 1:
            if r[i] == r[i + 1]:
                r[i] += 1
                points += 2 ** r[i] # Track merge score
                r.pop(i + 1)
            i += 1
        while len(r) < 4:
            r.append(0)
        return r, points

    def _apply_move(self, grid, move):
        total_points = 0
        if move == 'a':
            for i in range(4):
                new, pts = self._compress_row(grid[i])
                grid[i] = new
                total_points += pts
        elif move == 'd':
            for i in range(4):
                new, pts = self._compress_row(grid[i][::-1])
                grid[i] = new[::-1]
                total_points += pts
        elif move == 'w':
            for c in range(4):
                col = [grid[r][c] for r in range(4)]
                new, pts = self._compress_row(col)
                for r in range(4):
                    grid[r][c] = new[r]
                total_points += pts
        elif move == 's':
            for c in range(4):
                col = [grid[r][c] for r in range(4)]
                new, pts = self._compress_row(col[::-1])
                new = new[::-1]
                for r in range(4):
                    grid[r][c] = new[r]
                total_points += pts
        return total_points

    def _move_changes(self, grid, move):
        """Returns True if the move would change the grid."""
        test = [row[:] for row in grid]
        self._apply_move(test, move)
        return test != grid

    def _spawn_tile(self, grid):
        empty = [(r, c) for r in range(4) for c in range(4) if grid[r][c] == 0]
        if empty:
            r, c = random.choice(empty)
            grid[r][c] = 1 if random.random() < 0.9 else 2

    def _can_move(self, grid):
        for row in grid:
            if 0 in row:
                return True
        for r in range(4):
            for c in range(3):
                if grid[r][c] == grid[r][c + 1]:
                    return True
        for r in range(3):
            for c in range(4):
                if grid[r][c] == grid[r + 1][c]:
                    return True
        return False