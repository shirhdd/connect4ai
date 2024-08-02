import pygame
import math
import sys
from game_state import Connect4GameState, PLAYER_ONE, PLAYER_TWO, \
    ROWS, COLUMNS

# Pygame Constants
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Connect4GameRunner:
    def __init__(self):
        pygame.init()
        self.width = COLUMNS * SQUARESIZE
        self.height = (ROWS + 1) * SQUARESIZE
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.myfont = pygame.font.SysFont("monospace", 75)
        self.current_game = Connect4GameState()

    def draw_board(self):
        board = self.current_game.board
        for c in range(COLUMNS):
            for r in range(ROWS):
                pygame.draw.rect(self.screen, BLUE, (
                c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE,
                SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2),
                int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(COLUMNS):
            for r in range(ROWS):
                if board[r][c] == PLAYER_ONE:
                    pygame.draw.circle(self.screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(self.height - (r * SQUARESIZE + SQUARESIZE / 2))),
                                       RADIUS)
                elif board[r][c] == PLAYER_TWO:
                    pygame.draw.circle(self.screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(self.height - (r * SQUARESIZE + SQUARESIZE / 2))),
                                       RADIUS)
        pygame.display.update()

    def run_game(self):
        game_over = False
        turn = 0

        self.draw_board()
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
                        row = self.current_game.get_next_open_row(col)
                        self.current_game.drop_piece(row, col,
                                                     PLAYER_ONE if turn == 0 else PLAYER_TWO)
                        self.draw_board()
                        self.current_game.print_board()  # Print the board in the terminal

                        if self.current_game.winning_move(
                                PLAYER_ONE if turn == 0 else PLAYER_TWO):
                            label = self.myfont.render(
                                f"Player {turn + 1} wins!!", 1,
                                RED if turn == 0 else YELLOW)
                            self.screen.blit(label, (40, 10))
                            pygame.display.update()  # Update the display to show the win message
                            print(
                                f"Player {turn + 1} wins!")  # Print the win message in the terminal
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        if game_over:
                            pygame.time.wait(3000)


def main():
    game_runner = Connect4GameRunner()
    game_runner.run_game()


if __name__ == '__main__':
    main()
