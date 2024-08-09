import numpy as npimport abc# import util# from game import Agent, Actionfrom collections import Counterimport numpy as npfrom game_state import Connect4GameState, PLAYER_ONE, PLAYER_TWOclass Agent(object):    def __init__(self):        super(Agent, self).__init__()    @abc.abstractmethod    def get_action(self, game_state):        return    def stop_running(self):        passdef score_evaluation_function(current_game_state):    """    This default evaluation function just returns the score of the state.    The score is the same one displayed in the GUI.    This evaluation function is meant for use with adversarial search agents    (not reflex agents).    """    score = 0    # opponent_piece = 1 if piece == 2 else 2    score += current_game_state.get_all_four(2)    score -= current_game_state.get_all_four(1)    return scoreclass RandomAgent(Agent):    def __init__(self):        super().__init__()    def get_action(self, game_state):        return np.random.choice(game_state.get_legal_actions())class MultiAgentSearchAgent(Agent):    """    This class provides some common elements to all of your    multi-agent searchers.  Any methods defined here will be available    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.    You *do not* need to make any changes here, but you can if you want to    add functionality to all your adversarial search agents.  Please do not    remove anything, however.    Note: this is an abstract class: one that should not be instantiated.  It's    only partially specified, and designed to be extended.  Agent (game.py)    is another abstract class.    """    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):        self.evaluation_function = score_evaluation_function        self.depth = depth    @abc.abstractmethod    def get_action(self, game_state):        returnclass AlphaBetaAgent(MultiAgentSearchAgent):    """    Your minimax agent with alpha-beta pruning (question 3)    """    def get_action(self, game_state):        """        Returns the minimax action using self.depth and self.evaluationFunction        """        alpha = -np.inf        beta = np.inf        chosen_action = -1        biggest_val = -np.inf        for action in game_state.get_legal_actions():            successor = game_state.generate_successor(action, 1)            alpha = self.helper(successor, (2 * self.depth) - 1, 0, alpha,                                beta)            if alpha > biggest_val:                biggest_val = alpha                chosen_action = action            if beta <= alpha:                break        return chosen_action    def helper(self, game_state, depth, agent_index, alpha, beta):        if depth == 0 or game_state.done:            return self.evaluation_function(game_state)        if agent_index == 1:            for action in game_state.get_legal_actions():                suc = game_state.generate_successor(action, agent_index)                alpha = max(alpha, self.helper(suc, depth - 1, 0, alpha, beta))                if beta <= alpha:                    break            return alpha        else:            for action in game_state.get_legal_actions():                suc = game_state.generate_successor(action, agent_index)                beta = min(beta, self.helper(suc, depth - 1, 1, alpha, beta))                if beta <= alpha:                    break            return betaclass MonteCarloAgent:    def __init__(self, simulations=100):        self.simulations = simulations    def get_action(self, game_state):        legal_moves = game_state.get_legal_actions()        best_move = None        best_win_rate = -1        for move in legal_moves:            win_rate = self.simulate_move(game_state, move, self.simulations)            if win_rate > best_win_rate:                best_win_rate = win_rate                best_move = move        return best_move    def simulate_move(self, game_state, move, simulations):        wins = 0        for _ in range(simulations):            if self.simulate_game(game_state, move):                wins += 1        return wins / simulations    def simulate_game(self, game_state, move):        state = game_state.generate_successor(move, 1)        current_player = 0        while not state.done:            legal_moves = state.get_legal_actions()            if not legal_moves:                break            next_move = np.random.choice(legal_moves)            state = state.generate_successor(next_move, current_player)            current_player = 1 - current_player        return state.winning_move(PLAYER_TWO)