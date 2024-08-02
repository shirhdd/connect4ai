import argparse
import numpy as np
import sys
import pygame
import math
from connect4_game_state import Connect4GameState

# Constants
DEFAULT_BOARD_ROWS = 6
DEFAULT_BOARD_COLUMNS = 7

# Pygame Constants
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Connect4GameRunner:
    def __init__(self):
        super(Connect4GameRunner, self).__init__()
        self.current_game = None
        pygame.init()
        self.width = DEFAULT_BOARD_COLUMNS * SQUARESIZE
        self.height = (DEFAULT_BOARD_ROWS + 1) * SQUARESIZE
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.myfont = pygame.font.SysFont("monospace", 75)

    def new_game(self, initial_state=None):
        if initial_state is None:
            initial_state = Connect4GameState()
        self.current_game = initial_state
        self.run_game()

    def run_game(self):
        game_over = False
        turn = 0

        self.draw_board(self.current_game.board)
        pygame.display.update()

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(self.screen, BLACK,
                                     (0, 0, self.width, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == 0:
                        pygame.draw.circle(self.screen, RED,
                                           (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(self.screen, YELLOW,
                                           (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(self.screen, BLACK,
                                     (0, 0, self.width, SQUARESIZE))
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    if self.current_game.is_valid_location(col):
                        self.current_game.apply_action(col,
                                                       1 if turn == 0 else 2)
                        self.draw_board(self.current_game.board)

                        if self.current_game.done:
                            label = self.myfont.render(
                                f"Player {turn + 1} wins!!", 1,
                                RED if turn == 0 else YELLOW)
                            self.screen.blit(label, (40, 10))
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        if game_over:
                            pygame.time.wait(3000)

    def draw_board(self, board):
        for c in range(DEFAULT_BOARD_COLUMNS):
            for r in range(DEFAULT_BOARD_ROWS):
                pygame.draw.rect(self.screen, BLUE, (
                c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE,
                SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2),
                int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(DEFAULT_BOARD_COLUMNS):
            for r in range(DEFAULT_BOARD_ROWS):
                if board[r][c] == 1:
                    pygame.draw.circle(self.screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int((
                                                                          DEFAULT_BOARD_ROWS - r - 1) * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                       RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(self.screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), int((
                                                                          DEFAULT_BOARD_ROWS - r - 1) * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                       RADIUS)
        pygame.display.update()


def main():
    parser = argparse.ArgumentParser(description='Connect 4 game.')
    parser.add_argument('--rows', help='Number of rows for the board.',
                        default=DEFAULT_BOARD_ROWS, type=int)
    parser.add_argument('--columns', help='Number of columns for the board.',
                        default=DEFAULT_BOARD_COLUMNS, type=int)
    args = parser.parse_args()

    initial_state = Connect4GameState(rows=args.rows, columns=args.columns)
    game_runner = Connect4GameRunner()
    game_runner.new_game(initial_state=initial_state)


if __name__ == '__main__':
    main()
