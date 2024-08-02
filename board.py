class Board:

    def __init__(self, ROWS=6, COLUMNS=7):
        self.board = np.zeros((ROWS, COLUMNS))

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def is_valid_location(self, board, col):
        return board[ROWS - 1][col] == 0

    def get_next_open_row(self, board, col):
        for r in range(ROWS):
            if board[r][col] == 0:
                return r
        return None

    def draw_board(self):
        print(np.flip(board, 0))

    def get(self, row, col):
        return self.board[row][col]

    def get_empty(self):
        # TODO return all zeros