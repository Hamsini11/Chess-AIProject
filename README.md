This Python project simulates a chess game with AI opponents. It utilizes the Minimax algorithm with alpha-beta pruning for intelligent decision-making.

Key Components:
---------------
###### ♔ ChessPiece:
♕ Represents a chess piece with its color and type.
♕ Provides methods for determining legal moves based on the piece type.

###### ♔ ChessBoard:
♕ Represents the chessboard and its current state.
♕ Handles board initialization, move validation, and game-ending conditions.

###### ♔ MinimaxAgent:
♕ Implements the Minimax algorithm with alpha-beta pruning to select the best move.
♕ Evaluates board positions based on material advantage.

###### ♔ RandomAgent:
♕ Selects moves randomly from the list of legal moves.

###### ♔ ChessGame:
♕ Manages the overall game flow, including player turns, move execution, and game termination.
♕ Visualizes the board and prints move information.

To Run:
-------
Clone the Repository:
```git clone https://github.com/Hamsini11/Chess-AIProject.git```

Execute the main.py script:
```python main.py```

This will start a chess game between the Minimax AI and the Random Agent. The game will be visualized on the console, and the moves will be printed.

_The max_moves parameter in the_ ```ChessGame``` _class can be adjusted to limit the number of moves per game._

Output:
-------
Starting Chess Game: Minimax (White) vs Random (Black)
======================================================
![image](https://github.com/user-attachments/assets/def6a96e-a3ac-4026-8bda-7bc5488e04fd)
Move 1:
Move time: 0.01 seconds
white moves: a2 -> a3 <br>
![image](https://github.com/user-attachments/assets/df538656-9f9a-4f30-921c-465ca93cecc6)
Move 2:
Move time: 0.00 seconds
black moves: a7 -> a5 <br>
![image](https://github.com/user-attachments/assets/f47b2a87-ef7f-4e11-9deb-309aea859680)
Move 3:
Move time: 0.02 seconds
white moves: a3 -> a4 <br>
![image](https://github.com/user-attachments/assets/60262c85-2ca6-4480-b607-f78cd27e4cb3)
Move 4:
Move time: 0.00 seconds
black moves: a8 -> a7 <br>
![image](https://github.com/user-attachments/assets/0fb9f048-be94-4f24-80b8-1fc255532c1e)
Move 5:
Move time: 0.02 seconds
white moves: b2 -> b3 <br>
![image](https://github.com/user-attachments/assets/70af1bc7-46ed-4dff-955a-43a02651daf8)
Move 6:
Move time: 0.00 seconds
black moves: b8 -> c6 <br>
![image](https://github.com/user-attachments/assets/c3c39a6f-4b6e-4154-a4c9-baae40455839)
Move 7:
Move time: 0.02 seconds
white moves: c1 -> b2 <br>
![image](https://github.com/user-attachments/assets/ad6006cd-2784-4f7c-9bc8-ef19e8aec819)
Move 8:
Move time: 0.00 seconds
black moves: f7 -> f5 <br>
![image](https://github.com/user-attachments/assets/ec65d5b9-af92-42d9-8b03-a160be3887d0)
Move 9:
Move time: 0.02 seconds
white moves: b2 -> c3 <br>
![image](https://github.com/user-attachments/assets/6605a47c-1bde-4a0c-a324-feb5836a91b9)
Move 10:
Move time: 0.00 seconds
black moves: g8 -> f6 <br>
![image](https://github.com/user-attachments/assets/c0129926-8e7c-4b47-8c76-21a460746183)
Move 11:
Move time: 0.03 seconds
white moves: b3 -> b4 <br>
![image](https://github.com/user-attachments/assets/dc4ce8bf-2585-4de5-9783-ba1739ea87d5)
Move 12:
Move time: 0.00 seconds
black moves: g7 -> g5 <br>
![image](https://github.com/user-attachments/assets/e998987e-c798-4d65-84f4-48b8fa502044)
Move 13:
Move time: 0.02 seconds
white moves: b4 -> b5 <br>
![image](https://github.com/user-attachments/assets/d3653497-a83f-4342-89ce-c195e7998af7)
Move 14:
Move time: 0.00 seconds
black moves: d7 -> d6 <br>
![image](https://github.com/user-attachments/assets/82aabad7-5e84-4ead-93fb-e36def982064)
Move 15:
Move time: 0.02 seconds
white moves: b5 -> c6 <br>
![image](https://github.com/user-attachments/assets/7be18bca-1b76-4eb6-b3c3-6c9eececdc6a)
Move 16:
Move time: 0.00 seconds
black moves: f8 -> g7 <br>
![image](https://github.com/user-attachments/assets/30600568-a2d5-4918-8198-0330f4429986)
Move 17:
Move time: 0.02 seconds
white moves: c6 -> b7 <br>
![image](https://github.com/user-attachments/assets/d08cfabd-7401-4c1c-9376-a36a01e8c813)
Move 18:
Move time: 0.00 seconds
black moves: h8 -> f8 <br>
![image](https://github.com/user-attachments/assets/ed451628-662e-4c5d-a698-797e5ec29c57)
Move 19:
Move time: 0.02 seconds
white moves: b7 -> c8 <br>
![image](https://github.com/user-attachments/assets/9c85dbf3-64a7-4e8d-bdfd-5892af5f1b63)
Move 20:
Move time: 0.00 seconds
black moves: f8 -> f7 <br>
![image](https://github.com/user-attachments/assets/bff4f09a-c845-4d72-8a33-13f50d34473e)
Move 21:
Move time: 0.02 seconds
white moves: c3 -> d4 <br>
![image](https://github.com/user-attachments/assets/baf6a57c-c0d2-4847-a57e-9e3fb4a0d6a1)
Move 22:
Move time: 0.00 seconds
black moves: e7 -> e6 <br>
![image](https://github.com/user-attachments/assets/1f6f5e44-d7d8-46ae-bc06-29a9bd5a8cb0)
Move 23:
Move time: 0.03 seconds
white moves: d4 -> a7 <br>
![image](https://github.com/user-attachments/assets/337f22f5-fc0c-4ae4-a3ab-4e0d8fa9476a)
Move 24:
Move time: 0.00 seconds
black moves: f7 -> e7 <br>
![image](https://github.com/user-attachments/assets/82b529bd-b2e7-4927-ac4b-4776fd2dffe6)
Move 25:
Move time: 0.02 seconds
white moves: a7 -> d4 <br>
![image](https://github.com/user-attachments/assets/ab18c421-743b-4ec8-b9de-e7c81afee9b8)
Move 26:
Move time: 0.00 seconds
black moves: f5 -> f4 <br>
![image](https://github.com/user-attachments/assets/21ff60ec-fe43-4038-b763-62a8f5a8442c)
Move 27:
Move time: 0.03 seconds
white moves: d4 -> c3 <br>
![image](https://github.com/user-attachments/assets/3548db1e-e2bb-48c5-8844-ae8e1a4acd95)
Move 28:
Move time: 0.00 seconds
black moves: e7 -> d7 <br>
![image](https://github.com/user-attachments/assets/a2fd5862-1d55-4937-a53c-c9033084e835)
Move 29:
Move time: 0.03 seconds
white moves: c3 -> b2 <br>
![image](https://github.com/user-attachments/assets/d9dbe0bb-472d-47f8-9520-24e91e334172)
Move 30:
Move time: 0.00 seconds
black moves: d6 -> d5 <br>
![image](https://github.com/user-attachments/assets/338d526a-ac4b-486a-967e-a5172c244e20)
Move 31:
Move time: 0.02 seconds
white moves: b2 -> e5 <br>
![image](https://github.com/user-attachments/assets/7a561e62-e95e-4686-a558-c93c087d29a8)
Move 32:
Move time: 0.00 seconds
black moves: d7 -> d6 <br>
![image](https://github.com/user-attachments/assets/0470c4bf-df60-4c33-8f1b-460f32134b76)
Move 33:
Move time: 0.04 seconds
white moves: c2 -> c3 <br>
![image](https://github.com/user-attachments/assets/06e7554e-bdef-44f1-860a-39b33008cf10)
Move 34:
Move time: 0.00 seconds
black moves: f6 -> e4 <br>
![image](https://github.com/user-attachments/assets/615427c9-88e7-4552-a952-098c1a1fc75b)
Move 35:
Move time: 0.03 seconds
white moves: e5 -> g7 <br>
![image](https://github.com/user-attachments/assets/a8ada3f6-72bc-4646-a7d4-3d00c39d620e)
Move 36:
Move time: 0.00 seconds
black moves: d8 -> d7 <br>
![image](https://github.com/user-attachments/assets/93cf54ef-cacc-4507-bfb1-953d16a39666)
Move 37:
Move time: 0.02 seconds
white moves: g7 -> e5 <br>
![image](https://github.com/user-attachments/assets/f149db89-0d04-4d9b-8617-cc697989bae0)
Move 38:
Move time: 0.00 seconds
black moves: e4 -> f2 <br>
![image](https://github.com/user-attachments/assets/009c985a-5794-408a-bde4-8ec442423e8c)
Move 39:
Move time: 0.05 seconds
white moves: e1 -> f2 <br>
![image](https://github.com/user-attachments/assets/af6462ce-8407-4935-8bee-81f801bf1699)
Move 40:
Move time: 0.00 seconds
black moves: d7 -> f7 <br>
![image](https://github.com/user-attachments/assets/ca152f60-fb5e-42d0-8990-ed91c3ea4d61)
Move 41:
Move time: 0.05 seconds
white moves: e5 -> d6 <br>
![image](https://github.com/user-attachments/assets/4fd91588-6471-4bf3-94c9-b58cd5a0aa3b)
Move 42:
Move time: 0.00 seconds
black moves: g5 -> g4 <br>
![image](https://github.com/user-attachments/assets/b83f903f-fd02-4d16-a9f7-ed203ecb8bb9)
Move 43:
Move time: 0.02 seconds
white moves: d6 -> e5 <br>
![image](https://github.com/user-attachments/assets/25b00948-fc7c-4b7f-a4fe-8805b027806e)
Move 44:
Move time: 0.00 seconds
black moves: f7 -> g8 <br>
![image](https://github.com/user-attachments/assets/94acc8f7-540b-41d3-bb2c-3a707e6e42bd)
Move 45:
Move time: 0.02 seconds
white moves: e5 -> c7 <br>
![image](https://github.com/user-attachments/assets/a6ab1f16-07ad-4428-8424-f158c8f91f59)
Move 46:
Move time: 0.00 seconds
black moves: g4 -> g3 <br>
![image](https://github.com/user-attachments/assets/928d62ed-6c50-4667-ba66-bc2cc1c2d73d)
Move 47:
Move time: 0.02 seconds
white moves: f2 -> g3 <br>
![image](https://github.com/user-attachments/assets/08e377a3-2c45-488f-9a51-cfc9afd8e144)
Move 48:
Move time: 0.00 seconds
black moves: g8 -> f8 <br>
![image](https://github.com/user-attachments/assets/20834b9c-677f-4582-a5d9-22fedfe6fe61)
Move 49:
Move time: 0.02 seconds
white moves: c7 -> a5 <br>
![image](https://github.com/user-attachments/assets/464389fc-17b6-49fb-b7fa-1260a483c268)
Move 50:
Move time: 0.00 seconds
black moves: d5 -> d4 <br>

Game Over! <br>
Result: draw_by_moves <br>

Game Statistics:
Total moves played: 50

Move History:
Move 1: a2 -> a3
Move 2: a7 -> a5
Move 3: a3 -> a4
Move 4: a8 -> a7
Move 5: b2 -> b3
Move 6: b8 -> c6
Move 7: c1 -> b2
Move 8: f7 -> f5
Move 9: b2 -> c3
Move 10: g8 -> f6
Move 11: b3 -> b4
Move 12: g7 -> g5
Move 13: b4 -> b5
Move 14: d7 -> d6
Move 15: b5 -> c6
Move 16: f8 -> g7
Move 17: c6 -> b7
Move 18: h8 -> f8
Move 19: b7 -> c8
Move 20: f8 -> f7
Move 21: c3 -> d4
Move 22: e7 -> e6
Move 23: d4 -> a7
Move 24: f7 -> e7
Move 25: a7 -> d4
Move 26: f5 -> f4
Move 27: d4 -> c3
Move 28: e7 -> d7
Move 29: c3 -> b2
Move 30: d6 -> d5
Move 31: b2 -> e5
Move 32: d7 -> d6
Move 33: c2 -> c3
Move 34: f6 -> e4
Move 35: e5 -> g7
Move 36: d8 -> d7
Move 37: g7 -> e5
Move 38: e4 -> f2
Move 39: e1 -> f2
Move 40: d7 -> f7
Move 41: e5 -> d6
Move 42: g5 -> g4
Move 43: d6 -> e5
Move 44: f7 -> g8
Move 45: e5 -> c7
Move 46: g4 -> g3
Move 47: f2 -> g3
Move 48: g8 -> f8
Move 49: c7 -> a5
Move 50: d5 -> d4

Performance Metrics: <br>
Minimax average move time: 0.02 seconds <br>
Random agent average move time: 0.00 seconds <br>
