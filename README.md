This Python project simulates a chess game with AI opponents. It utilizes the Minimax algorithm and Monte Carlo Tree Search and their variations for intelligent decision-making.

##### Key Components:
---------------------
###### ♔ ChessPiece:
♕ Represents a chess piece with its color and type.
♕ Provides methods for determining legal moves based on the piece type.

###### ♔ ChessBoard:
♕ Represents the chessboard and its current state.
♕ Implements the chessboard and manages all core gameplay mechanics, including move validation, tracking attacked squares, and checking game-ending conditions like checkmate.

###### ♔ MinimaxAgent:
♕ An AI player implementation that uses the minimax algorithm with alpha-beta pruning, incorporating different search strategies (standard minimax, beam search, and iterative deepening) to make intelligent chess moves.

###### ♔ MCTS:
♕ A sophisticated AI player that implements Monte Carlo Tree Search with multiple variants (standard, progressive history, and RAVE), using simulation-based decision making to select chess moves.

###### ♔ RandomAgent:
♕ Selects moves randomly from the list of legal moves.

###### ♔ ChessGame:
♕ Represents the overarching game and coordinates interactions between the player and the chessboard.
♕ Visualizes the board and prints move information.

Each class is designed to work together in a modular fashion, with ChessGame using ChessBoard which in turn uses ChessPieces, while both MinimaxAgent and MCTSAgent can be used as players within the ChessGame framework.

##### To Run:
-------------
Clone the Repository:
```git clone https://github.com/your_username/Hamsini11.git```

Execute the main.py script:
```python main.py```

This will start a chess game between the variations of Minimax AI and the MCTS AI. The game will be visualized on the console, and the moves will be printed, followed by summary stats.

_The max_moves parameter in the_ ```ChessGame``` _class can be adjusted to limit the number of moves per game._
