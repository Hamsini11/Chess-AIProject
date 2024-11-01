This Python project simulates a chess game with AI opponents. It utilizes the Minimax algorithm with alpha-beta pruning for intelligent decision-making.

KEY COMPONENTS:
---------------
###### 1. ChessPiece:
♕ Represents a chess piece with its color and type.
♕ Provides methods for determining legal moves based on the piece type.

###### ChessBoard:
♕ Represents the chessboard and its current state.
♕ Handles board initialization, move validation, and game-ending conditions.

###### MinimaxAgent:
♕ Implements the Minimax algorithm with alpha-beta pruning to select the best move.
♕ Evaluates board positions based on material advantage.

###### RandomAgent:
♕ Selects moves randomly from the list of legal moves.

###### ChessGame:
♕ Manages the overall game flow, including player turns, move execution, and game termination.
♕ Visualizes the board and prints move information.
