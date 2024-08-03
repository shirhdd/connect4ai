import numpy as npimport abc# import util# from game import Agent, Actionfrom collections import Counterclass Agent(object):    def __init__(self):        super(Agent, self).__init__()    @abc.abstractmethod    def get_action(self, game_state):        return    def stop_running(self):        pass# class ReflexAgent(Agent):#     """#     A reflex agent chooses an action at each choice point by examining#     its alternatives via a state evaluation function.##     The code below is provided as a guide.  You are welcome to change#     it in any way you see fit, so long as you don't touch our method#     headers.#     """##     def get_action(self, game_state):#         """#         You do not need to change this method, but you're welcome to.##         get_action chooses among the best options according to the evaluation function.##         get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}#         """##         # Collect legal moves and successor states#         legal_moves = game_state.get_agent_legal_actions()##         # Choose one of the best actions#         scores = [self.evaluation_function(game_state, action) for action in legal_moves]#         best_score = max(scores)#         best_indices = [index for index in range(len(scores)) if scores[index] == best_score]#         chosen_index = np.random.choice(best_indices)  # Pick randomly among the best##         "Add more of your code here if you want to"##         return legal_moves[chosen_index]##     def evaluation_function(self, current_game_state, action):#         """#         Design a better evaluation function here.##         The evaluation function takes in the current and proposed successor#         GameStates (GameState.py) and returns a number, where higher numbers are better.##         """##         # Useful information you can extract from a GameState (game_state.py)##         successor_game_state = current_game_state.generate_successor(action=action)#         board = successor_game_state.board#         max_tile = successor_game_state.max_tile##         score = successor_game_state.score##         "*** YOUR CODE HERE ***"#         max_ind = len(board) - 1#         diff = 0#         for i in range(max_ind):#             for j in range(max_ind):#                 cur_val = board[i][j]#                 if i != len(board) - 1 and cur_val != 0 and board[i + 1][j] != 0:#                     diff += abs(board[i][j] - board[i + 1][j])#                 if j != len(board) - 1 and cur_val != 0 and board[i][j + 1] != 0:#                     diff += abs(board[i][j] - board[i][j + 1])##         return len(successor_game_state.get_empty_tiles()[0]) * 70 + score * 0.3 + max_tile - diff * 10#def score_evaluation_function(current_game_state):    """    This default evaluation function just returns the score of the state.    The score is the same one displayed in the GUI.    This evaluation function is meant for use with adversarial search agents    (not reflex agents).    """    return current_game_state.winning_move(1) or current_game_state.winning_move(2)class MultiAgentSearchAgent(Agent):    """    This class provides some common elements to all of your    multi-agent searchers.  Any methods defined here will be available    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.    You *do not* need to make any changes here, but you can if you want to    add functionality to all your adversarial search agents.  Please do not    remove anything, however.    Note: this is an abstract class: one that should not be instantiated.  It's    only partially specified, and designed to be extended.  Agent (game.py)    is another abstract class.    """    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):        self.evaluation_function = score_evaluation_function        self.depth = depth    @abc.abstractmethod    def get_action(self, game_state):        return# class MinmaxAgent(MultiAgentSearchAgent):#     def get_action(self, game_state):#         """#         Returns the minimax action from the current gameState using self.depth#         and self.evaluationFunction.##         Here are some method calls that might be useful when implementing minimax.##         game_state.get_legal_actions(agent_index):#             Returns a list of legal actions for an agent#             agent_index=0 means our agent, the opponent is agent_index=1##         Action.STOP:#             The stop direction, which is always legal##         game_state.generate_successor(agent_index, action):#             Returns the successor game state after an agent takes an action#         """#         """*** YOUR CODE HERE ***"""##         chosen_action = Action.STOP#         biggest_val = -np.inf##         for action in game_state.get_legal_actions(agent_index=0):#             successor = game_state.generate_successor(0, action)#             cur_val = self.helper(successor, (self.depth * 2) - 1, 1)##             if cur_val > biggest_val:#                 biggest_val = cur_val#                 chosen_action = action##         return chosen_action##     def helper(self, game_state, depth, agent_index):#         if depth == 0 or game_state.done:#             return self.evaluation_function(game_state)##         if agent_index == 0:#             chosen = -np.inf#             for action in game_state.get_legal_actions(agent_index=agent_index):#                 chosen = max(chosen, self.helper(game_state.generate_successor(agent_index, action), depth - 1, 1))#         else:#             chosen = np.inf#             for action in game_state.get_legal_actions(agent_index=agent_index):#                 chosen = min(chosen, self.helper(game_state.generate_successor(agent_index, action), depth - 1, 0))#         return chosenclass AlphaBetaAgent(MultiAgentSearchAgent):    """    Your minimax agent with alpha-beta pruning (question 3)    """    def get_action(self, game_state):        """        Returns the minimax action using self.depth and self.evaluationFunction        """        """*** YOUR CODE HERE ***"""        alpha = -np.inf        beta = np.inf        chosen_action = -2        biggest_val = -np.inf        for action in game_state.get_legal_actions():            successor = game_state.generate_successor(action, agent_index=0)            alpha = self.helper(successor, (2 * self.depth) - 1, 1, alpha, beta)            if alpha > biggest_val:                biggest_val = alpha                chosen_action = action            if beta <= alpha:                break        return chosen_action    def helper(self, game_state, depth, agent_index, alpha, beta):        if depth == 0 or game_state.done:            return self.evaluation_function(game_state)        if agent_index == 0:            for action in game_state.get_legal_actions():                suc = game_state.generate_successor(agent_index, action)                alpha = max(alpha, self.helper(suc, depth - 1, 1, alpha, beta))                if beta <= alpha:                    break            return alpha        else:            for action in game_state.get_legal_actions():                suc = game_state.generate_successor(agent_index, action)                beta = min(beta, self.helper(suc, depth - 1, 0, alpha, beta))                if beta <= alpha:                    break            return beta# class ExpectimaxAgent(MultiAgentSearchAgent):#     """#     Your expectimax agent (question 4)#     """##     def get_action(self, game_state):#         """#         Returns the expectimax action using self.depth and self.evaluationFunction##         The opponent should be modeled as choosing uniformly at random from their#         legal moves.#         """#         """*** YOUR CODE HERE ***"""#         chosen_action = Action.STOP#         biggest_val = -np.inf##         for action in game_state.get_legal_actions(0):#             successor = game_state.generate_successor(0, action)#             cur_val = self.helper(successor, (2 * self.depth) - 1, 1)##             if cur_val > biggest_val:#                 biggest_val = cur_val#                 chosen_action = action##         return chosen_action##     def helper(self, game_state, depth, agent_index):##         if depth == 0 or len(game_state.get_legal_actions(agent_index)) == 0:#             return self.evaluation_function(game_state)##         if agent_index == 0:#             chosen = -np.inf#             for action in game_state.get_legal_actions(agent_index):#                 chosen = max(chosen, self.helper(game_state.generate_successor(agent_index, action), depth - 1, 1))#         else:#             num_actions = len(game_state.get_legal_actions(agent_index))#             chosen = 0.0#             for action in game_state.get_legal_actions(agent_index):#                 chosen += float(self.helper(game_state.generate_successor(agent_index, action), depth - 1, 0)) * float(#                             1 / num_actions)##         return chosen#def better_evaluation_function(current_game_state):    """    Your extreme 2048 evaluation function (question 5).    DESCRIPTION: It considers five key features: bonus for high number of empty tiles,        a penalty for large differences between adjacent tiles to encourage a monotonic grid,        a penalty for tiles positioned in the middle rather than close to the sides,        a penalty for having a high frequency of tiles with the same number,        and a bonus if the highest value tile is positioned in a corner.    """    "*** YOUR CODE HERE ***"    board = current_game_state.board    diff_pen = 0    sides_pen = 0    empty_tiles = len(current_game_state.get_empty_tiles()[0])    corner_bonus = 0    tile2freq = dict()    for i in range(len(board)):        for j in range(len(board)):            cur_val = board[i][j]            # save freq of tiles to penalty high freq            if cur_val != 0:                if cur_val not in tile2freq.keys():                    tile2freq[cur_val] = 1                else:                    tile2freq[cur_val] += 1            # give bonus if max tile is in corner            if cur_val == current_game_state.max_tile and (i == 0 or i == len(board) - 1) and (j == 0 or j == len(board) - 1):                corner_bonus = 20000            # add a penalty for big difference between 2 adjacent tiles            if i != len(board) - 1 and cur_val != 0 and board[i+1][j] != 0:                diff_pen += abs(board[i][j] - board[i + 1][j])            if j != len(board) - 1 and cur_val != 0 and board[i][j+1] != 0:                diff_pen += abs(board[i][j] - board[i][j + 1])            # add penalty for distance from sides            sides_pen += min(abs(i - len(board) - 1), i, j, abs(j - len(board))) * board[i][j]    # add penalty for big amount of tiles with same number    max_freq = max(tile2freq.values())    return empty_tiles * 1500 - diff_pen * 15 - sides_pen * 10 - max_freq * 700 + corner_bonus# Abbreviationbetter = better_evaluation_function