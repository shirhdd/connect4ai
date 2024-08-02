import numpy as np

DEFAULT_BOARD_ROWS = 6
DEFAULT_BOARD_COLUMNS = 7

class Connect4GameState:
    def __init__(self, rows=DEFAULT_BOARD_ROWS, columns=DEFAULT_BOARD_COLUMNS, board=None, done=False):
        super(Connect4GameState, self).__init__()
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

    def get_legal_actions(self):
        return [col for col in range(self._num_of_columns) if self._board[0, col] == 0]

    def apply_action(self, col, piece):
        if not self.is_valid_location(col):
            raise Exception("Illegal action.")
        row = self.get_next_open_row(col)
        self._board[row, col] = piece
        if self.winning_move(piece):
            self._done = True

    def is_valid_location(self, col):
        return self._board[0, col] == 0

    def get_next_open_row(self, col):
        for r in range(self._num_of_rows-1, -1, -1):
            if self._board[r, col] == 0:
                return r

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

    def generate_successor(self, agent_index=0, action=None):
        successor = Connect4GameState(rows=self._num_of_rows, columns=self._num_of_columns, board=self._board.copy(), done=self._done)
        if action is not None:
            if agent_index == 0:
                successor.apply_action(action[1], action[0])
            elif agent_index == 1:
                successor.apply_action(action[1], action[0])
            else:
                raise Exception("Illegal agent index.")
        return successor
