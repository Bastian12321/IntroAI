from game import Game,Board
class AI:
    def __init__(self):
        self.Moves = ['a', 'd', 'w', 's']
        pass

    def clone_board(self, board):
        cloned = Board()
        for i in range(4):
            for j in range(4):
                cloned.grid[i][j] = board.grid[i][j]
        return cloned
    
    def simulated_turn(self, board, direction):
        moved = False
        new_board = self.clone_board(board)

        if direction == 'a':
            moved = new_board.move_left()
        elif direction == 'd':
            moved = new_board.move_right()
        elif direction == 'w':
            moved = new_board.move_up()
        elif direction == 's':
            moved = new_board.move_down()
        
        return new_board, moved
    
    def empty_cells(self, board):
        empty = []
        for i in range(4):
            for j in range(4):
                if board.grid[i][j] == 0:
                    empty.append((i, j))
        return empty

    def expectimax(self, board, depth, player):
        if depth == 0:
            return self.heuristic(board)
        
        if player:
            best_value = float('-inf')
            for move in self.Moves:
                simulated_board, moved = self.simulated_turn(board, move)
                if not moved:
                    continue
                value = self.expectimax(simulated_board, depth - 1, False)
                best_value = max(best_value, value)
            return best_value
        else:
            empty = self.empty_cells(board)
            expected_value = 0.0
            if not empty:
                return self.expectimax(board, depth - 1, True)
            
            for r,c in empty:
                board2 = self.clone_board(board)
                board2.grid[r][c] = 2
                expected_value += (1/len(empty)) * 0.9 * self.expectimax(board2, depth - 1, True)

                board4 = self.clone_board(board)
                board4.grid[r][c] = 4
                expected_value += (1/len(empty)) * 0.1 * self.expectimax(board4, depth - 1, True)
            
            return expected_value
    
    def move_ai(self, board):
        best_move = None
        best_value = float('-inf')

        for move in self.Moves:
            simulated_board, moved = self.simulated_turn(board, move)
            if not moved:
                continue
            value = self.expectimax(simulated_board, 3, False)
            if value >= best_value:
                best_value = value
                best_move = move
        return best_move

    #Simple heuristic.
    def heuristic(self, board):
        return self.weightedcellsheuristic(board)
    
    def emptycellsheuristic(self, board):
        empty_cells = self.empty_cells(board)
        return len(empty_cells)
    
    def weightedcellsheuristic(self, board):
        weight = [[16, 15, 14, 13],
                  [9, 10, 11, 12],
                  [8, 7, 6, 5],
                  [1, 2, 3, 4]]
        score = 0
        for i in range(4):
            for j in range(4):
                score += board.grid[i][j] * weight[i][j]
        return score