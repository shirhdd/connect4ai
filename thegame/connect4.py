import math
import sys
from display import Display, SQUARESIZE
import pygame
from game_state import Connect4GameState, PLAYER_ONE, PLAYER_TWO, \
    ROWS, COLUMNS

class Connect4GameRunner:
    def __init__(self):
        self.current_game = Connect4GameState()

    def run_game(self):
        game_over = False
        turn = 0
        display = Display()
        display.draw_board(self.current_game.board)

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                # Mouse hover
                if event.type == pygame.MOUSEMOTION:
                    display.draw_rect()
                    posx = event.pos[0]
                    display.draw_circle(turn, posx)

                # Mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))

                    # Verify action is valid
                    if self.current_game.is_valid_location(col):
                        display.draw_rect()
                        row = self.current_game.get_next_open_row(col)
                        self.current_game.drop_piece(row, col,
                                                     PLAYER_ONE if turn == 0 else PLAYER_TWO)
                        display.draw_board(self.current_game.board)
                        self.current_game.print_board()  # Print the board in the terminal

                        # check if move is a winning move
                        if self.current_game.winning_move(
                                PLAYER_ONE if turn == 0 else PLAYER_TWO):
                            display.write_winner_to_screen(turn)
                            display.update_screen()  # Update the display to show the win message
                            print(
                                f"Player {turn + 1} wins!")  # Print the win message in the terminal
                            game_over = True

                        turn += 1
                        turn = turn % 2

                        if game_over:
                            pygame.time.wait(3000)

                # Update the display to screen
                display.update_screen()



def main():
    game_runner = Connect4GameRunner()
    game_runner.run_game()


if __name__ == '__main__':
    main()
