# Connect4 AI Game

This project is a command-line Connect4 game that allows users to play against an AI agent. The AI agent can either be the **AlphaBetaAgent** or the **MonteCarloAgent**. Various gameplay options such as the number of rows, columns, and depth for the search tree can be configured using command-line arguments.

## Requirements

- Python 3.x
- `argparse`
- `numpy`

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/shirhdd/connect4ai.git
   cd connect4ai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

You can run the game by executing the `connect4.py` file in the terminal. Various options are available to customize your gameplay experience. Below is the general command structure:

```bash
python connect4.py [options]
```

### Command-Line Arguments

| Argument              | Description                                                                               | Default Value               |
|-----------------------|-------------------------------------------------------------------------------------------|-----------------------------|
| `--random_seed`        | Sets a seed for reproducibility in random moves.                                           | Random integer               |
| `--agent`              | Specifies the AI agent to play against: `AlphaBetaAgent` or `MonteCarloAgent`.            | `AlphaBetaAgent`             |
| `--player`             | Defines the player type: `keyboardPlayer` (human input) or `randomPlayer` (random moves). | `keyboardPlayer`             |
| `--depth`              | Sets the maximum depth for the AlphaBetaAgent search tree.                                 | `2`                          |
| `--rows`               | Number of rows on the game board.                                                         | `6`                          |
| `--columns`            | Number of columns on the game board.                                                      | `7`                          |
| `--simulations`        | Number of simulations for the MonteCarloAgent.                                            | `100`                        |
| `--num_of_games`       | Number of games to run in a single session.                                               | `1`                          |
| `--evaluation_function`| Specifies the evaluation function used by the AlphaBetaAgent.                             | `score_evaluation_function`  |

### Examples

1. **Run the game with default settings**:
   ```bash
   python connect4.py
   ```

2. **Play with the AlphaBetaAgent and increase the search depth to 4**:
   ```bash
   python connect4.py --agent AlphaBetaAgent --depth 4
   ```

3. **Play using the MonteCarloAgent with 200 simulations**:
   ```bash
   python connect4.py --agent MonteCarloAgent --simulations 200
   ```

4. **Run 5 games with a random player**:
   ```bash
   python connect4.py --player randomPlayer --num_of_games 5
   ```

5. **Set a random seed for reproducibility**:
   ```bash
   python connect4.py --random_seed 42
   ```

### Notes

- **Random Seed**: Using the `--random_seed` argument allows you to replicate game outcomes by controlling the randomness.
- **Depth**: The `--depth` argument is specific to the `AlphaBetaAgent`. It controls how deep the agent explores the game tree when making decisions.
- **Simulations**: The `--simulations` argument is specific to the `MonteCarloAgent`. It sets how many simulations the agent runs to evaluate potential moves.


![image](https://github.com/user-attachments/assets/ddf421e6-26a6-46f8-8ba0-e93e587df334)

