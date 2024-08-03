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

    def get_legal_actions(self):
        legal_action = []
        for col in range(self._num_of_columns):
            if self.is_valid_location(col):
                legal_action += [col]
        print(legal_action)
        return legal_action

    def is_valid_location(self, col):
        print("bord", col,self._board[self._num_of_rows-1][col])
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
            print("move", row, col)
            successor.drop_piece(row, col, agent_index)
        return successor
