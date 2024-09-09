"""
#########################################################################################
# Display Module for Connect 4 AI Project                                               #
#                                                                                       #
# This module is responsible for rendering the game board, updating the visual          #
# elements during the game, and managing the graphical interface using Pygame. It       #
# includes methods for drawing the game board, placing pieces, displaying the winner,   #
# and updating the screen in real-time.                                                 #
#########################################################################################
"""

import pygame
from game_state import PLAYER_ONE, PLAYER_TWO, BLOCK

SQUARESIZE = 100  # Size of each square in the Connect 4 grid.
RADIUS = int(SQUARESIZE / 2 - 5)  # Radius of the circles drawn on the grid representing empty spaces.
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
RED_IMG = r'.\images\red_70x70.png'
YELLOW_IMG = r'.\images\yellow_70x70.png'


class Display:
    """
    Manages all graphical aspects of the game, such as drawing the board, pieces, and updating the game window.
    """

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
        """
        Draws the given board on the screen and calls the update screen function.
        This function should be called every time the game display should change.
        """
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
                elif board[r][c] == BLOCK:
                    pygame.draw.circle(self.screen, BLUE, (
                        int(c * SQUARESIZE + SQUARESIZE / 2),
                        int(self.height - (r * SQUARESIZE + SQUARESIZE / 2))),
                                       RADIUS)
        pygame.display.update()

    def cover_top(self):
        """
        Covers the top area of the game display where the player's next piece is shown before placement.
        """
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, SQUARESIZE))

    def draw_piece(self, turn, posx):
        """
        Draws a piece for the current player at the specified horizontal position.
        """
        image = self.red_piece if turn == 0 else self.yellow_piece
        self.screen.blit(image, (posx - SQUARESIZE // 2, 0))

    def write_winner_to_screen(self, turn):
        """
        Displays a message declaring the winner based on the current player's turn.
        """
        label = self.myfont.render(f"Player {turn + 1} wins!!", 1,
                                   RED if turn == 0 else YELLOW)
        self.screen.blit(label, (40, 10))

    def write_draw(self):
        """
        Displays a message indicating the game ended in a draw.
        """
        label = self.myfont.render(f"its a draw...", 1, BLACK)
        self.screen.blit(label, (40, 10))

    def update_screen(self):
        """
        Updates the Pygame display window with the latest changes.
        """
        pygame.display.update()
