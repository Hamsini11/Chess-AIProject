import random
import time
from ChessGame import ChessGame
from typing import Tuple, Optional

class RandomAgent:
    """
    A random agent for playing chess.

    Attributes:
        color (str): The color of the agent (either 'white' or 'black').
        move_times (list): A list to store the time taken for each move.
    """
    def __init__(self, color: str):
        self.color = color
        self.move_times = []
    
    def get_move(self, game: ChessGame) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Selects a random legal move from the available options.

        Args:
            game (ChessGame): The current game state.

        Returns:
            Optional[Tuple[Tuple[int, int], Tuple[int, int]]]: A randomly selected legal move, or None if it's not the agent's turn.
        """
        if game.current_player != self.color:
            return None
        
        start_time = time.time()
        possible_moves = []
        
        for row in range(8):
            for col in range(8):
                piece = game.board.board[row][col]
                if piece is not None and piece.color == self.color:
                    legal_moves = game.board.get_legal_moves(row, col)
                    possible_moves.extend([((row, col), move) for move in legal_moves])
        
        move = random.choice(possible_moves) if possible_moves else None
        end_time = time.time()
        self.move_times.append(end_time - start_time)
        
        return move
