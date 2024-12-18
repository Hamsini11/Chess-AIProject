This Python project simulates a chess game with AI opponents. It utilizes the Minimax algorithm and Monte Carlo Tree Search and their variations for intelligent decision-making.

##### Key Components:
---------------------
###### ♔ ChessPiece:
♕ Represents a chess piece with its color and type. <br/>
♕ Provides methods for determining legal moves based on the piece type.

###### ♔ ChessBoard:
♕ Represents the chessboard and its current state.<br/>
♕ Implements the chessboard and manages all core gameplay mechanics, including move validation, tracking attacked squares, and checking game-ending conditions like checkmate.

###### ♔ MinimaxAgent:
♕ An AI player implementation that uses the minimax algorithm with alpha-beta pruning, incorporating different search strategies (standard minimax, beam search, and iterative deepening) to make intelligent chess moves.

###### ♔ MCTS:
♕ A sophisticated AI player that implements Monte Carlo Tree Search with multiple variants (standard, progressive history, and RAVE), using simulation-based decision making to select chess moves.

###### ♔ RandomAgent:
♕ Selects moves randomly from the list of legal moves.

###### ♔ ChessGame:
♕ Represents the overarching game and coordinates interactions between the player and the chessboard.<br/>
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

Quick Tech Help!
----------------
##### To view all the results in console:
-------------
1. Go to File > Preferences > Settings
2. Search for 'scrollback'
3. It should be 1000 or higher

All CHECKMATES in the game!!
----------------------------
![image](https://github.com/user-attachments/assets/67c35abe-5ba8-4f6d-a3e4-04cc165f1c33)
![image](https://github.com/user-attachments/assets/d7b97122-0730-484b-988b-83751268d394)
![image](https://github.com/user-attachments/assets/3e3f9fe2-3e34-4fa4-a7be-de49128a73e0)
![image](https://github.com/user-attachments/assets/5558e853-4137-434d-ae77-a4b1a46fea37)
![image](https://github.com/user-attachments/assets/acbee8e8-5546-4dfd-b321-9c89b43eb5f1)
![image](https://github.com/user-attachments/assets/f1ffa3bf-ddd0-4569-b5f6-4995161eb61a)




