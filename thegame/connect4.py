import argparse
import numpy as np
import sys
from connect4_game_state import Connect4GameState

class Connect4GameRunner:
    def __init__(self):
        super(Connect4GameRunner, self).__init__()
        self.current_game = None

    def new_game(self, initial_state=None):
        if initial_state is None:
            initial_state = Connect4GameState()
        self.current_game = initial_state
        return self.run_game()

    def run_game(self):
        game_over = False
        turn = 0
        while not game_over:
            self.print_board(self.current_game.board)
            col = int(input(f"Player {turn + 1}'s turn. Select column (0-{self.current_game._num_of_columns - 1}): "))

            if self.current_game.is_valid_location(col):
                self.current_game.apply_action(col, 1 if turn == 0 else 2)
                if self.current_game.done:
                    self.print_board(self.current_game.board)
                    print(f"Player {turn + 1} wins!")
                    game_over = True
                turn += 1
                turn %= 2
            else:
                print("Invalid move. Try again.")
        return self.current_game.board

    def print_board(self, board):
        print(np.flip(board, 0))

def main():
    parser = argparse.ArgumentParser(description='Connect 4 game.')
    parser.add_argument('--rows', help='Number of rows for the board.', default=DEFAULT_BOARD_ROWS, type=int)
    parser.add_argument('--columns', help='Number of columns for the board.', default=DEFAULT_BOARD_COLUMNS, type=int)
    args = parser.parse_args()

    initial_state = Connect4GameState(rows=args.rows, columns=args.columns)
    game_runner = Connect4GameRunner()
    game_runner.new_game(initial_state=initial_state)

if __name__ == '__main__':
    main()
