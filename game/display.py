import pygame
from game_state import Connect4GameState, PLAYER_ONE, PLAYER_TWO

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class Display:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.width = self.cols * SQUARESIZE
        self.height = (self.rows + 1) * SQUARESIZE
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        pygame.init()
        self.myfont = pygame.font.SysFont("monospace", 75)

    def draw_board(self, board):

        for c in range(self.cols):
            for r in range(self.rows):
                pygame.draw.rect(self.screen, BLUE, (
                    c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE,
                    SQUARESIZE))
                pygame.draw.circle(self.screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2),
                    int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

        for c in range(self.cols):
            for r in range(self.rows):
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

    # TODO : change name to purpose (cover top?)
    def draw_rect(self):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))

    # TODO : change name to purpose
    def draw_circle(self, turn, posx):
        pygame.draw.circle(self.screen, RED if turn == 0 else YELLOW,
                           (posx, int(SQUARESIZE / 2)), RADIUS)

    def write_winner_to_screen(self, turn):
        label = self.myfont.render(f"Player {turn + 1} wins!!", 1,
                                   RED if turn == 0 else YELLOW)
        self.screen.blit(label, (40, 10))

    def update_screen(self):
        pygame.display.update()
