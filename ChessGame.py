from ChessBoard import ChessBoard
from typing import Tuple

class ChessGame:
    """
    Represents a chess game.

    Attributes:
        board (ChessBoard): The current state of the chessboard.
        current_player (str): The color of the player whose turn it is.
        max_moves (int): The maximum number of moves allowed in the game.
        move_count (int): The number of moves made so far.
        game_status (str): The current status of the game (ongoing, draw, etc.).
    """
    def __init__(self, max_moves: int = 50):
        """
        Initializes a new chess game.

        Args:
            max_moves (int, optional): The maximum number of moves allowed. Defaults to 50.
        """
        self.board = ChessBoard()
        self.current_player = 'white'
        self.max_moves = max_moves
        self.move_count = 0
        self.game_status = 'ongoing'

    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """
        Makes a move on the chessboard.

        Args:
            from_pos (Tuple[int, int]): The starting position of the piece.
            to_pos (Tuple[int, int]): The ending position of the piece.

        Returns:
            bool: True if the move was successful, False otherwise.
        """
        if self.game_status != 'ongoing':
            return False

        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        piece = self.board.board[from_row][from_col]
        if piece is None or piece.color != self.current_player:
            return False
        
        legal_moves = self.board.get_legal_moves(from_row, from_col)
        if to_pos not in legal_moves:
            return False
        
        # Make the move
        self.board.board[to_row][to_col] = piece
        self.board.board[from_row][from_col] = None
        piece.has_moved = True
        
        # Update move history
        self.board.move_history.append(self.board.get_board_state())
        
        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        self.move_count += 1
        
        # Check game-ending conditions
        if self.move_count >= self.max_moves:
            self.game_status = 'draw_by_moves'
        elif self.board.is_draw_by_repetition():
            self.game_status = 'draw_by_repetition'
        else:
            self.game_status = self.check_game_status()
        
        return True

    def check_game_status(self):
        """
        Determine the game status and handle game conclusion.
    
        Returns:
            str: Current game status ('ongoing', 'checkmate', 'draw', 'stalemate')
        """
        current_player = self.current_player

        # Check for checkmate
        if self.board.is_checkmate(current_player):
            self.game_status = 'checkmate'
            self.winner = 'white' if current_player == 'black' else 'black'
            return self.game_status
    
        # Check for draw conditions
        if self.board.is_draw(current_player):
            self.game_status = 'draw'
            self.winner = None
            return self.game_status

        # Check for stalemate
        if self.board.is_stalemate(current_player):
            self.game_status = 'stalemate'
            self.winner = None
            return self.game_status

        return 'ongoing'
