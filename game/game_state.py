import numpy as np

ROWS = 6
COLUMNS = 7
PLAYER_ONE = 1
PLAYER_TWO = 2

class Connect4GameState:
    def __init__(self, rows=ROWS, columns=COLUMNS, board=None, done=False):
        self._done = done
        if board is None:
            board = np.zeros((rows, columns), dtype=np.int32)
        self._board = board
        self._num_of_rows, self._num_of_columns = rows, columns

    @property
    def done(self):
        return self._done

    @property
    def board(self):
        return self._board

    def drop_piece(self, row, col, piece):
        self._board[row][col] = piece
        self._done = self.winning_move(piece)


    def get_legal_actions(self):
        legal_action = []
        for col in range(self._num_of_columns):
            if self.is_valid_location(col):
                legal_action += [col]
        # print(legal_action)
        return legal_action

    def is_valid_location(self, col):
        # print("bord", col,self._board[self._num_of_rows-1][col])
        return self._board[self._num_of_rows-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self._num_of_rows):
            if self._board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self._board, 0))

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self._num_of_columns-3):
            for r in range(self._num_of_rows):
                if self._board[r][c] == piece and self._board[r][c+1] == piece and self._board[r][c+2] == piece and self._board[r][c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self._num_of_columns):
            for r in range(self._num_of_rows-3):
                if self._board[r][c] == piece and self._board[r+1][c] == piece and self._board[r+2][c] == piece and self._board[r+3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(self._num_of_columns-3):
            for r in range(self._num_of_rows-3):
                if self._board[r][c] == piece and self._board[r+1][c+1] == piece and self._board[r+2][c+2] == piece and self._board[r+3][c+3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(self._num_of_columns-3):
            for r in range(3, self._num_of_rows):
                if self._board[r][c] == piece and self._board[r-1][c+1] == piece and self._board[r-2][c+2] == piece and self._board[r-3][c+3] == piece:
                    return True
        return False

    def generate_successor(self, col, agent_index):
        successor = Connect4GameState(rows=self._num_of_rows,
                                      columns=self._num_of_columns,
                                      board=self._board.copy(),
                                      done=self._done)
        if col is not None:
            row = self.get_next_open_row(col)
            # print("move", row, col)
            successor.drop_piece(row, col, 1 if agent_index == 0 else 2)
        return successor

    def potential_row(self, player, first):
        potenial = 0
        for i in range(first[1], self._num_of_columns):
            if self._board[first[0]][i] != 0 and self._board[first[0]][i] != player:
                break
            potenial += 1
        for i in range(first[1] - 1, 0, -1):
            if self._board[first[0]][i] != 0 and self._board[first[0]][i] != player:
                break
            potenial += 1
        return potenial >= 4

    def potential_cols(self, player, first):
        potenial = 0
        for i in range(first[0], self._num_of_rows):
            if self._board[i][first[1]] != 0 and self._board[i][first[1]] != player:
                break
            potenial += 1
        return potenial >= 4

    def find_largest_streak(self, player):
        max_streak = 0
        first = (-1, -1)
        last = -1

        # Check rows for streaks
        for r in range(self._num_of_rows):
            streak = 0
            for c in range(self._num_of_columns):
                if self._board[r][c] == player:
                    if streak == 0:
                        first = (r, c)
                    streak += 1
                else:
                    if self.potential_row(player, first) and streak > max_streak:
                        max_streak = streak

                    streak = 0

        # Check columns for streaks
        for c in range(self._num_of_columns):
            streak = 0
            for r in range(self._num_of_rows):
                if self._board[r][c] == player:
                    if streak == 0:
                        first = (r, c)
                    streak += 1

                else:
                    if self.potential_cols(player, first) and streak > max_streak:
                        max_streak = streak
                    streak = 0

        # Check positively sloped diagonals for streaks
        for r in range(self._num_of_rows - 3):
            for c in range(self._num_of_columns - 3):
                streak = 0
                for i in range(min(self._num_of_rows - r, self._num_of_columns - c)):
                    if self._board[r + i][c + i] == player:
                        streak += 1
                        if streak > max_streak:
                            max_streak = streak
                    else:
                        streak = 0

        # Check negatively sloped diagonals for streaks
        for r in range(3, self._num_of_rows):
            for c in range(self._num_of_columns - 3):
                streak = 0
                for i in range(min(r + 1, self._num_of_columns - c)):
                    if self._board[r - i][c + i] == 1:
                        streak += 1
                        if streak > max_streak:
                            max_streak = streak
                    else:
                        streak = 0

        return max_streak





    def get_all_four(self, piece):
        score = 0

        # Check horizontal locations for win
        for c in range(self._num_of_columns-3):
            for r in range(self._num_of_rows):
                if self._board[r][c] in [piece, 0] and self._board[r][c+1] in [piece, 0] and self._board[r][c+2] in [piece, 0] and self._board[r][c+3] in [piece, 0]:
                    score += sum(self._board[r][c: c + 4]) / piece

        # Check vertical locations for win
        for c in range(self._num_of_columns):
            for r in range(self._num_of_rows-3):
                if self._board[r][c] in [piece, 0] and self._board[r+1][c] in [piece, 0]  and self._board[r+2][c] in [piece, 0]  and self._board[r+3][c] in [piece, 0]:
                    score += sum(self._board[r: r + 4][c]) / piece

        # Check positively sloped diagonals
        for c in range(self._num_of_columns-3):
            for r in range(self._num_of_rows-3):
                if self._board[r][c] in [piece, 0] and self._board[r+1][c+1] in [piece, 0] and self._board[r+2][c+2] in [piece, 0] and self._board[r+3][c+3] in [piece, 0]:
                    score += sum(self._board[r: r + 4][c: c + 4]) / piece

        # Check negatively sloped diagonals
        for c in range(self._num_of_columns-3):
            for r in range(3, self._num_of_rows):
                if self._board[r][c] in [piece, 0] and self._board[r-1][c+1] in [piece, 0] and self._board[r-2][c+2] in [piece, 0] and self._board[r-3][c+3] in [piece, 0]:
                    score += sum(self._board[r - 3: r + 1][c: c + 4]) / piece

