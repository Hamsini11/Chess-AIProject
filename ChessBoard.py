from ChessPieces import ChessPieces # Importing the ChessPieces class for piece creation and manipulation
from typing import List, Tuple, Optional # Importing type hints for improved code readability and error checking

class ChessBoard:
    """
    An advanced chessboard with comprehensive chess rules and intelligent move validation.
    """
    def __init__(self):
        """
        Initializes the chessboard with rule sets.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]  # 8x8 board initialized with None
        self.initialize_board() # Sets up pieces in their initial positions
        self.move_history = [] # Tracks all moves made during the game
        self.halfmove_clock = 0 # Tracks the number of moves since the last pawn advance or capture
        self.capture_history = {'white': [], 'black': []} # Stores captured pieces for both players
        
        # TO DO Assign standard point values for each piece type
        # Piece point values (standard chess valuation)
        self.piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0  # Kings have no point value (cannot be captured)
        }

    def initialize_board(self):
        """
        Sets up the initial board state with standard chess piece arrangement.
        """
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        # Set up black and white major pieces on their respective rows
        for i, piece_type in enumerate(piece_order):
            self.board[0][i] = ChessPieces('black', piece_type) # Black's back row
            self.board[7][i] = ChessPieces('white', piece_type) # White's back row

        # Place pawns on the second and seventh rows
        for i in range(8):
            self.board[1][i] = ChessPieces('black', 'pawn') # Black pawns
            self.board[6][i] = ChessPieces('white', 'pawn') # White pawns

    def get_all_attacked_squares(self, color: str) -> set:
        """
        Returns all squares attacked by pieces of a specific color.

        Args:
            color (str): Color of the attacking pieces

        Returns:
            set: Set of (row, col) tuples representing attacked squares
        """
        attacked_squares = set() # Stores all attacked positions as (row, col) tuples
        for row in range(8): # Iterate through all rows
            for col in range(8): # Iterate through all columns
                piece = self.board[row][col] # Get the piece at the current position
                if piece and piece.color == color: # Check if the piece matches the given color
                    # Add raw attackable squares for the piece
                    moves = self._get_raw_attacked_squares(row, col)
                    attacked_squares.update(moves)
        return attacked_squares

    def _get_raw_attacked_squares(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Gets raw attacked squares for a piece without full legality check.

        Args:
            row (int): Row of the piece
            col (int): Column of the piece

        Returns:
            List of attacked squares
        """
        piece = self.board[row][col]
        if not piece: # Return an empty list if there is no piece
            return []

        attacked_squares = [] # Initialize an empty list of attackable squares
        
        # Define specific movement patterns for each type of piece
        if piece.piece_type == 'pawn': # Pawns attack diagonally
            direction = 1 if piece.color == 'black' else -1 # Determine attack direction based on color
            capture_cols = [col - 1, col + 1] # Pawns can attack diagonally to the left and right
            for new_col in capture_cols:
                new_row = row + direction
                if 0 <= new_row < 8 and 0 <= new_col < 8: # Ensure the target square is within bounds
                    attacked_squares.append((new_row, new_col))
        
        # Knight attack pattern (L-shape moves)
        elif piece.piece_type == 'knight':
            moves = [
                (row + 2, col + 1), (row + 2, col - 1),
                (row - 2, col + 1), (row - 2, col - 1),
                (row + 1, col + 2), (row + 1, col - 2),
                (row - 1, col + 2), (row - 1, col - 2)
            ]
            # Filter only valid board positions
            attacked_squares = [(r, c) for r, c in moves if 0 <= r < 8 and 0 <= c < 8]

        # Sliding pieces (rook, bishop, queen)
        elif piece.piece_type in ['rook', 'bishop', 'queen']:
            directions = []
            # Rook and queen can move horizontally and vertically
            if piece.piece_type in ['rook', 'queen']:
                directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
            # Bishop and queen can move diagonally
            if piece.piece_type in ['bishop', 'queen']:
                directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

            # Check each direction until blocked or edge of board
            for dir_row, dir_col in directions:
                new_row, new_col = row + dir_row, col + dir_col
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    attacked_squares.append((new_row, new_col))
                    # Stop if blocked by a piece
                    if self.board[new_row][new_col] is not None:
                        break
                    new_row += dir_row
                    new_col += dir_col
        # King attack pattern (one square in any direction)
        elif piece.piece_type == 'king':
            moves = [
                (row + 1, col), (row - 1, col),
                (row, col + 1), (row, col - 1),
                (row + 1, col + 1), (row + 1, col - 1),
                (row - 1, col + 1), (row - 1, col - 1)
            ]
            # Filter only valid board positions
            attacked_squares = [(r, c) for r, c in moves if 0 <= r < 8 and 0 <= c < 8]

        return attacked_squares

    def is_square_under_attack(self, row: int, col: int, by_color: str) -> bool:
        """
        Checks if a specific square is under attack by pieces of a given color.

        Args:
            row (int): Row of the square
            col (int): Column of the square
            by_color (str): Color of attacking pieces

        Returns:
            bool: True if square is under attack, False otherwise
        """
        # Use get_all_attacked_squares to check if position is under attack
        return (row, col) in self.get_all_attacked_squares(by_color)

    def is_move_safe(self, start_row: int, start_col: int, end_row: int, end_col: int) -> bool:
        """
        Checks if a move is safe by simulating the move and checking for checks.

        Args:
            start_row, start_col (int): Starting position
            end_row, end_col (int): Ending position

        Returns:
            bool: True if move is safe, False otherwise
        """
        # Make a deep copy of the current board state
        original_board = [row[:] for row in self.board]
        piece = self.board[start_row][start_col]
        
        # Simulate the move
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None

        # Check if the king of the moving piece's color is in check after the move
        is_safe = not self.is_king_in_check(piece.color)

        # Restore the original board state
        self.board = original_board

        return is_safe

    def get_legal_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Get legal moves for a piece, considering additional chess rules.

        Args:
            row (int): Row of the piece
            col (int): Column of the piece

        Returns:
            List of legal moves
        """
        piece = self.board[row][col]
        if not piece:
            return []

        # Get base moves without considering check
        base_moves = self._get_base_legal_moves(row, col)

        # Filter moves that would put the king in check or move into attacked squares
        legal_moves = [
            move for move in base_moves 
            if self.is_move_safe(row, col, move[0], move[1])
        ]

        return legal_moves

    def _get_base_legal_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Gets base legal moves without advanced rule checks.

        Args:
            row (int): Row of the piece
            col (int): Column of the piece

        Returns:
            List of base legal moves
        """
        piece = self.board[row][col]
        legal_moves = []
    
        if piece.piece_type == 'pawn':
            direction = 1 if piece.color == 'black' else -1
        
            # Forward move
            new_row = row + direction
            if 0 <= new_row < 8 and self.board[new_row][col] is None:
                legal_moves.append((new_row, col))
            
                # Initial two-square move
                if not piece.has_moved:
                    new_row = row + 2 * direction
                    if 0 <= new_row < 8 and self.board[new_row][col] is None:
                        legal_moves.append((new_row, col))
        
            # Captures
            capture_cols = [col - 1, col + 1]
            for new_col in capture_cols:
                new_row = row + direction
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target is not None and target.color != piece.color:
                        legal_moves.append((new_row, new_col))
    
        elif piece.piece_type == 'knight':
            moves = [
                (row + 2, col + 1), (row + 2, col - 1),
                (row - 2, col + 1), (row - 2, col - 1),
                (row + 1, col + 2), (row + 1, col - 2),
                (row - 1, col + 2), (row - 1, col - 2)
            ]
            for new_row, new_col in moves:
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target is None or target.color != piece.color:
                        legal_moves.append((new_row, new_col))
    
        elif piece.piece_type in ['rook', 'bishop', 'queen']:
            directions = []
            if piece.piece_type in ['rook', 'queen']:
                directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
            if piece.piece_type in ['bishop', 'queen']:
                directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])

            for dir_row, dir_col in directions:
                new_row, new_col = row + dir_row, col + dir_col
                while 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if target is None:
                        legal_moves.append((new_row, new_col))
                    else:
                        if target.color != piece.color:
                            legal_moves.append((new_row, new_col))
                        break
                    new_row += dir_row
                    new_col += dir_col
    
        elif piece.piece_type == 'king':
            moves = [
                (row + 1, col), (row - 1, col),
                (row, col + 1), (row, col - 1),
                (row + 1, col + 1), (row + 1, col - 1),
                (row - 1, col + 1), (row - 1, col - 1)
            ]
            for new_row, new_col in moves:
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    target = self.board[new_row][new_col]
                    if (target is None or target.color != piece.color):
                        legal_moves.append((new_row, new_col))

        return legal_moves

    def move_piece(self, start_row: int, start_col: int, end_row: int, end_col: int) -> Optional[float]:
        """
        Advanced move method with multiple chess rules.

        Args:
            start_row, start_col (int): Starting position
            end_row, end_col (int): Ending position

        Returns:
            Optional reward for the move, or None if move is illegal
        """
        piece = self.board[start_row][start_col]
        if not piece:
            return None

        # Get legal moves
        legal_moves = self.get_legal_moves(start_row, start_col)
        
        # Check if the move is legal
        if (end_row, end_col) not in legal_moves:
            return None

        # Capture mechanism
        target = self.board[end_row][end_col]
        reward = 0.0

        if target:
            # Prevent king capture
            if target.piece_type == 'king':
                return None
            
            # Add reward based on captured piece value
            reward = self.piece_values.get(target.piece_type, 0)
            self.capture_history[piece.color].append(target)

        # Auto-queen for pawns reaching the last row
        if piece.piece_type == 'pawn' and (end_row == 0 or end_row == 7):
            piece = ChessPieces(piece.color, 'queen')

        # Move the piece
        self.board[end_row][end_col] = piece
        self.board[start_row][start_col] = None

        # Update piece movement status
        piece.has_moved = True

        # Update halfmove clock (for draw by repetition)
        if piece.piece_type == 'pawn' or target:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        # Record the move
        self.move_history.append(self.get_board_state())

        return reward

    def is_king_in_check(self, color: str) -> bool:
        """
        Checks if the king of a specific color is in check.

        Args:
            color (str): Color of the king to check

        Returns:
            bool: True if the king is in check, False otherwise
        """
        # Find king position
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color and piece.piece_type == 'king':
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        
        # Check if the king's square is under attack by opponent pieces
        return self.is_square_under_attack(king_pos[0], king_pos[1], 'white' if color == 'black' else 'black')

    def is_checkmate(self, color: str) -> bool:
        """
        Checks if the specified color is in checkmate.

        Args:
            color (str): Color to check for checkmate

        Returns:
            bool: True if it's checkmate, False otherwise
        """
        # First, check if the king is in check
        if not self.is_king_in_check(color):
            return False

        # Check if any piece can make a move to get out of check
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    legal_moves = self.get_legal_moves(row, col)
                    if legal_moves:
                        return False

        return True

    def is_stalemate(self, color: str) -> bool:
        """
        Checks if the specified color is in stalemate.

        Args:
            color (str): Color to check for stalemate

        Returns:
            bool: True if it's stalemate, False otherwise
        """
        # Check that the king is not in check
        if self.is_king_in_check(color):
            return False

        # Check if any piece can make a legal move
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    legal_moves = self.get_legal_moves(row, col)
                    if legal_moves:
                        return False

        return True

    def is_draw(self, color: str) -> bool:
        """
        Checks for various draw conditions.

        Args:
            color (str): Color to check for draw conditions

        Returns:
            bool: True if the game is a draw, False otherwise
        """
        # Fifty-move rule check
        if self.halfmove_clock >= 50:
            return True

        # Threefold repetition check
        if self.is_draw_by_repetition():
            return True

        # Stalemate check
        if self.is_stalemate(color):
            return True

        # Insufficient material (basic implementation)
        white_pieces = sum(1 for row in self.board for piece in row if piece and piece.color == 'white')
        black_pieces = sum(1 for row in self.board for piece in row if piece and piece.color == 'black')

        if white_pieces <= 2 and black_pieces <= 2:
            # Check for only kings, or kings with one minor piece
            return True

        return False

    def is_draw_by_repetition(self) -> bool:
        """
        Checks if the game is a draw due to threefold repetition.

        Returns:
            bool: True if the game is a draw by threefold repetition, False otherwise
        """
        if len(self.move_history) < 5:
            return False
        
        current_state = self.get_board_state()
        count = sum(1 for past_state in self.move_history if past_state == current_state)
        
        return count >= 3

    def get_board_state(self) -> tuple:
        """
        Returns a tuple representing the current state of the chessboard.

        Returns:
            tuple: A tuple of tuples, where each inner tuple represents a row on the board.
        """
        state = []
        for row in range(8):
            row_state = []
            for col in range(8):
                piece = self.board[row][col]
                if piece is None:
                    row_state.append(None)
                else:
                    row_state.append((piece.color, piece.piece_type, piece.has_moved))
            state.append(tuple(row_state))
        return tuple(state)

    def print_board(self, color):
        """
        Prints a human-readable representation of the chessboard.
        """
        piece_symbols = {
            'pawn': '♙' if color == 'white' else '♟',
            'rook': '♖' if color == 'white' else '♜', 
            'knight': '♘' if color == 'white' else '♞',
            'bishop': '♗' if color == 'white' else '♝',
            'queen': '♕' if color == 'white' else '♛',
            'king': '♔' if color == 'white' else '♚'
        }

        print("  a b c d e f g h")
        for row in range(7, -1, -1):
            print(f"{row + 1}", end=" ")
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    symbol = piece_symbols.get((piece.piece_type, piece.color), '?')
                    print(symbol, end=" ")
                else:
                    print('.', end=" ")
            print(f"{row + 1}")
        print("  a b c d e f g h")

    def get_game_status(self, current_player: str) -> str:
        """
        Determines the current status of the game.

        Args:
            current_player (str): Color of the current player

        Returns:
            str: Game status (e.g., 'ongoing', 'checkmate', 'draw')
        """
        if self.is_checkmate(current_player):
            return 'checkmate'
        
        if self.is_draw(current_player) or self.is_stalemate(current_player):
            return 'draw'
        
        if self.is_king_in_check(current_player):
            return 'check'

        if self.is_stalemate(current_player):
            return 'stalemate'

        return 'ongoing'

    def evaluate_board(self, board=None, include_checkmate: bool = True) -> float:
        """
        Evaluates the current board state.

        Args:
            board (ChessBoard, optional): Board to evaluate. Defaults to self.
            include_checkmate (bool): Whether to include checkmate in evaluation. Defaults to True.

        Returns:
            float: A score representing the board's state from the perspective of white pieces.
        """
        # Use current board if no board is provided
        if board is None:
            board = self

        # Initialize score
        score = 0.0

        # Material evaluation
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece:
                    # Positive score for white pieces, negative for black pieces
                    value = self.piece_values.get(piece.piece_type, 0)
                    score += value if piece.color == 'white' else -value

        # Optional checkmate consideration
        if include_checkmate:
            if board.is_checkmate('black'):
                return float('inf')  # White wins
            elif board.is_checkmate('white'):
                return float('-inf')  # Black wins

        return score
