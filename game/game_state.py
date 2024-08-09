import numpy as np

ROWS = 6
COLUMNS = 7
PLAYER_ONE = 1
PLAYER_TWO = 2
BLOCK = 3
OPEN = 0


class Connect4GameState:
    def __init__(self, rows=ROWS, columns=COLUMNS, board=None, done=False, numberOfBlocks=5):
        self._done = done
        if board is None:
            board = np.zeros((rows, columns), dtype=np.int32)
            self._addBlocks(board, numberOfBlocks, rows, columns)
        self._board = board
        self._num_of_rows, self._num_of_columns = rows, columns
        self._directions = [(0, 1),  # Horizontal
                            (1, 0),  # Vertical
                            (1, 1),  # Positive diagonal
                            (-1, 1)]  # Negative diagonal

    def _addBlocks(self, board, num, rows, columns):
        total_elements = rows * columns
        grid_indices = np.arange(total_elements).reshape(rows, columns)
        random_flat_indices = np.random.choice(total_elements, num, replace=False)
        random_indices = np.unravel_index(random_flat_indices, (rows, columns))
        random_indices_2d = list(zip(random_indices[0], random_indices[1]))
        for x, y in random_indices_2d:
            board[x][y] = BLOCK

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
        return legal_action

    def is_valid_location(self, col):
        # print("bord", col,self._board[self._num_of_rows-1][col])
        for ind in range(self._num_of_rows):
            if self._board[ind][col] == 0:
                return True
        return False

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
            count = 0
            for pos in line:
                if pos == piece:
                    count += 1
            if count == 4:
                return 200
            return count if count < 4 else 200

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
