"""
##############################################################################################################
# Connect4 Game State Management for Connect 4 AI Project                                                    #
#                                                                                                            #
# This module defines the game state for Connect 4, including the board setup, game rules, and the mechanics #
# of how pieces are placed, how the game progresses, and how winning conditions are evaluated. It provides   #
# the necessary functionality for managing the game and interacting with AI agents.                          #
##############################################################################################################
"""

import numpy as np

ROWS = 6  # Default number of rows in the game board
COLUMNS = 7  # Default number of columns in the game board
PLAYER_ONE = 1
PLAYER_TWO = 2
BLOCK = 3
OPEN = 0


class Connect4GameState:
    """
    Manages the Connect 4 game board, handles piece placement, checks for valid moves and winning conditions,
    and generates game successors for multi-agent searches.
    """

    def __init__(self, rows=ROWS, columns=COLUMNS, board=None, done=False, numberOfBlocks=5):
        self._done = done
        if board is None:
            board = np.zeros((rows, columns), dtype=np.int32)
            self._add_blocks(board, numberOfBlocks, rows, columns)
        self._board = board
        self._num_of_rows, self._num_of_columns = rows, columns
        self._directions = [(0, 1),  # Horizontal
                            (1, 0),  # Vertical
                            (1, 1),  # Positive diagonal
                            (-1, 1)]  # Negative diagonal

    def _add_blocks(self, board, num, rows, columns):
        """
        Randomly adds a specified number of blocked spots (BLOCK) to the board at the beginning of the game.
        """
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
        """
        Places a player's piece at the specified row and column.
        """
        self._board[row][col] = piece
        self._done = self.winning_move(piece)

    def get_legal_actions(self):
        """
        Returns a list of valid columns where a piece can be dropped.
        """
        legal_action = []
        for col in range(self._num_of_columns):
            if self.is_valid_location(col):
                legal_action += [col]
        return legal_action

    def is_valid_location(self, col):
        """
        Checks if a column has any open spaces for a new piece.
        """
        for ind in range(self._num_of_rows):
            if self._board[ind][col] == 0:
                return True
        return False

    def get_next_open_row(self, col):
        """
        Returns the next available row for a piece to be placed in the specified column.
        """
        for r in range(self._num_of_rows):
            if self._board[r][col] == 0:
                return r

    def print_board(self):
        """
        Prints the current game board to console.
        """
        print(np.flip(self._board, 0))

    def generate_successor(self, col, agent_index):
        """
        Returns a new game state after applying a move by a player or AI agent.
        """
        successor = Connect4GameState(rows=self._num_of_rows,
                                      columns=self._num_of_columns,
                                      board=self._board.copy(),
                                      done=self._done)
        if col is not None:
            row = self.get_next_open_row(col)
            successor.drop_piece(row, col, 1 if agent_index == 0 else 2)
        return successor

    def winning_move(self, piece):
        """
        Checks if a given piece has won the game by forming a line of four in a row.
        """

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
        """
        Evaluates the board to calculate how close a player is to achieving a four-in-a-row.
        """

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
