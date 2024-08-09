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
        self._directions = [(0, 1),  # Horizontal
                            (1, 0),  # Vertical
                            (1, 1),  # Positive diagonal
                            (-1, 1)]  # Negative diagonal

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
        return self._board[self._num_of_rows - 1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self._num_of_rows):
            if self._board[r][col] == 0:
                return r

    def print_board(self):
        print(np.flip(self._board, 0))

    def generate_successor(self, col, agent_index):
        successor = Connect4GameState(rows=self._num_of_rows,
                                      columns=self._num_of_columns,
                                      board=self._board.copy(),
                                      done=self._done)
        if col is not None:
            row = self.get_next_open_row(col)
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


    def winning_move(self, piece):
        def check_line(line):
            return all(cell == piece for cell in line)

        def is_valid_cell(r, c):
            return 0 <= r < self._num_of_rows and 0 <= c < self._num_of_columns

        def check_direction(r, c, dr, dc):
            line = []
            for i in range(4):
                nr, nc = r + dr * i, c + dc * i
                if is_valid_cell(nr, nc):
                    line.append(self._board[nr][nc])
                else:
                    return False
            return check_line(line)

        for r in range(self._num_of_rows):
            for c in range(self._num_of_columns):
                for dr, dc in self._directions:
                    if check_direction(r, c, dr, dc):
                        return True

        return False

    def get_all_four(self, piece):
        def check_line(line):
            temp = sum(line) // piece
            return temp if temp < 4 else 200

        def is_valid_cell(r, c):
            return 0 <= r < self._num_of_rows and 0 <= c < self._num_of_columns and self._board[r][c] in [piece, 0]

        def check_direction(r, c, dr, dc):
            line = []
            for i in range(4):
                nr, nc = r + dr * i, c + dc * i
                if is_valid_cell(nr, nc):
                    line.append(self._board[nr][nc])
                else:
                    return 0
            return check_line(line)

        score = 0

        for r in range(self._num_of_rows):
            for c in range(self._num_of_columns):
                for dr, dc in self._directions:
                    score += check_direction(r, c, dr, dc)

        return score