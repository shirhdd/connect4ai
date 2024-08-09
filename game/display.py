import pygame
from game_state import PLAYER_ONE, PLAYER_TWO, BLOCKED

SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
RED_IMG = r'.\images\red_70x70.png'
YELLOW_IMG = r'.\images\yellow_70x70.png'


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
        self.red_piece = pygame.image.load("./images/red_70x70.png")
        self.yellow_piece = pygame.image.load("./images/yellow_70x70.png")
        self.red_piece = pygame.transform.scale(self.red_piece,
                                                (SQUARESIZE, SQUARESIZE))
        self.yellow_piece = pygame.transform.scale(self.yellow_piece,
                                                   (SQUARESIZE, SQUARESIZE))

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
                    self.screen.blit(self.red_piece, (
                        c * SQUARESIZE, self.height - (r + 1) * SQUARESIZE))
                elif board[r][c] == PLAYER_TWO:
                    self.screen.blit(self.yellow_piece, (
                        c * SQUARESIZE, self.height - (r + 1) * SQUARESIZE))
                elif board[r][c] == BLOCKED:
                    pygame.draw.circle(self.screen, BLUE, (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)),
                                       RADIUS)
        pygame.display.update()

    # TODO : change name to purpose (cover top?)
    def draw_rect(self):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))

    # TODO : change name to purpose
    def draw_circle(self, turn, posx):
        image = self.red_piece if turn == 0 else self.yellow_piece
        self.screen.blit(image, (posx - SQUARESIZE // 2, 0))

    def write_winner_to_screen(self, turn):
        label = self.myfont.render(f"Player {turn + 1} wins!!", 1,
                                   RED if turn == 0 else YELLOW)
        self.screen.blit(label, (40, 10))

    def write_draw(self):
        label = self.myfont.render(f"its a draw...", 1, BLACK)
        self.screen.blit(label, (40, 10))

    def update_screen(self):
        pygame.display.update()
