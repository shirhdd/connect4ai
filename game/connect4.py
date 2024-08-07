import argparse
import math
import sys
import time
from datetime import datetime

import numpy

from display import Display, SQUARESIZE
import pygame
from multi_agents import AlphaBetaAgent, MonteCarloAgent, RandomAgent
from game_state import Connect4GameState, PLAYER_ONE, PLAYER_TWO


class Connect4GameRunner:
    def __init__(self, rows, cols):
        self.current_game = None

    def run_game(self, args):
        self.current_game = Connect4GameState(args.rows, args.columns)
        game_over = False
        turn = 0
        if args.agent == 'MonteCarloAgent':
            agent = MonteCarloAgent(args.simulations)
        else:
            agent = AlphaBetaAgent(args.evaluation_function, args.depth)
        display = Display(args.rows, args.columns)
        display.draw_board(self.current_game.board)
        randomAgent = RandomAgent()
        win = 0
        steps = 0
        begTime = datetime.now().time()
        while not game_over:
            action = -1
            if turn == 1:
                action = agent.get_action(self.current_game)
            elif args.player == "randomPlayer":
                action = randomAgent.get_action(self.current_game)

            elif args.player == "keyboardPlayer":
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()

                    if event.type == pygame.MOUSEMOTION:
                        display.draw_rect()
                        posx = event.pos[0]
                        display.draw_circle(turn, posx)

                        # Mouse click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        print("score: ", self.current_game.get_all_four(1) - self.current_game.get_all_four(2))
                        posx = event.pos[0]
                        tmp = int(math.floor(posx / SQUARESIZE))
                        action = tmp if self.current_game.is_valid_location(tmp) else -1
                        break

            if action != -1:
                steps += 1
                display.draw_rect()
                row = self.current_game.get_next_open_row(action)
                self.current_game.drop_piece(row, action,
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
                    win = 1 if turn == 1 else 0
                    game_over = True
                if self.current_game.get_legal_actions() == []:
                    display.write_draw()
                    display.update_screen()  # Update the display to show the win message
                    print(f"its a draw!")  # Print the win message in the terminal
                    game_over = True

                turn += 1
                turn = turn % 2
                if game_over:
                    pygame.time.wait(3000)
                    endTime = datetime.now().time()
                    begTime_dt = datetime.combine(datetime.today(), begTime)
                    endTime_dt = datetime.combine(datetime.today(), endTime)
                    time_difference = endTime_dt - begTime_dt
                    return win, steps, time_difference
            # Update the display to screen
            display.update_screen()

def main():
    parser = argparse.ArgumentParser(description='Connect4 game.')
    parser.add_argument('--random_seed', help='The seed for the random state.',
                        default=numpy.random.randint(100), type=int)
    displays = ['GUI', 'SummaryDisplay']
    agents = ['AlphaBetaAgent', 'MonteCarloAgent']
    # parser.add_argument('--display', choices=displays, help='The game ui.', default=displays[0], type=str)
    parser.add_argument('--agent', choices=agents, help='The agent.',
                        default=agents[1], type=str)
    player = ['keyboardPlayer', 'randomPlayer']
    parser.add_argument('--player', choices=player, help='the player against the agent.',
                        default=agents[0], type=str)
    parser.add_argument('--depth',
                        help='The maximum depth for to search in the game tree.',
                        default=3, type=int)
    parser.add_argument('--rows', help='Number of rows.', default=6, type=int)
    parser.add_argument('--columns', help='Number of columns.', default=7,
                        type=int)
    parser.add_argument('--simulations', help='Number of simulations.',
                        default=100,
                        type=int)
    parser.add_argument('--num_of_games', help='The number of games to run.',
                        default=20, type=int)
    parser.add_argument('--evaluation_function',
                        help='The evaluation function for ai agent.',
                        default='score_evaluation_function', type=str)
    args = parser.parse_args()
    print(args)
    numpy.random.seed(args.random_seed)
    game_runner = Connect4GameRunner(args.rows, args.columns)
    winRate = 0
    avgNumberOfsteps = 0
    avgTime = 0
    for game in range(args.num_of_games):
        (winner, steps, time) = game_runner.run_game(args)
        winRate += winner
        avgNumberOfsteps += steps
        avgTime += int(time.total_seconds())
        print("game: ", game, args.num_of_games)

    print("result:", winRate / args.num_of_games, avgNumberOfsteps / args.num_of_games, avgTime / args.num_of_games)


if __name__ == '__main__':
    main()
