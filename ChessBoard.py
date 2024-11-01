from ChessPiece import ChessPiece

class ChessBoard:
    """
    Represents a chessboard with its current state and methods for manipulating it.

    Attributes:
        board (list[list[ChessPiece]]): A 2D list representing the chessboard.
        move_history (list): A list of previous moves.
        halfmove_clock (int): A counter used for the fifty-move rule.
    """
    def __init__(self):
        """
        Initializes the chessboard with the standard starting position.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()
        self.move_history = []
        self.halfmove_clock = 0

    def initialize_board(self):
        """
        Sets up the initial board state with the standard chess piece arrangement.
        """
        # Initialize pawns
        for i in range(8):
            self.board[1][i] = ChessPiece('black', 'pawn')
            self.board[6][i] = ChessPiece('white', 'pawn')

        # Initialize other pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for i, piece_type in enumerate(piece_order):
            self.board[0][i] = ChessPiece('black', piece_type)
            self.board[7][i] = ChessPiece('white', piece_type)

    def is_valid_position(self, row: int, col: int) -> bool:
        """
        Checks if a given position is within the bounds of the chessboard.

        Args:
            row (int): The row index.
            col (int): The column index.

        Returns:
            bool: True if the position is valid, False otherwise.
        """
        return 0 <= row < 8 and 0 <= col < 8

    def get_legal_moves(self, row: int, col: int) -> list:
        """
        Calculates all legal moves for a given piece at the specified position.

        Args:
            row (int): The row index of the piece.
            col (int): The column index of the piece.

        Returns:
            list: A list of tuples representing legal moves. Each tuple contains the starting and ending positions.
        """
        piece = self.board[row][col]
        if piece is None:
            return []

        legal_moves = []
        
        if piece.piece_type == 'pawn':
            direction = 1 if piece.color == 'black' else -1
            
            # Forward move
            new_row = row + direction
            if self.is_valid_position(new_row, col) and self.board[new_row][col] is None:
                legal_moves.append((new_row, col))
                
                # Initial two-square move
                if not piece.has_moved:
                    new_row = row + 2 * direction
                    if self.is_valid_position(new_row, col) and self.board[new_row][col] is None:
                        legal_moves.append((new_row, col))
            
            # Captures
            for col_offset in [-1, 1]:
                new_col = col + col_offset
                new_row = row + direction
                if self.is_valid_position(new_row, new_col):
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
                if self.is_valid_position(new_row, new_col):
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
                while self.is_valid_position(new_row, new_col):
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
                if self.is_valid_position(new_row, new_col):
                    target = self.board[new_row][new_col]
                    if target is None or target.color != piece.color:
                        legal_moves.append((new_row, new_col))

        return legal_moves

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
                    row_state.append((piece.color, piece.piece_type))
            state.append(tuple(row_state))
        return tuple(state)

    def is_draw_by_repetition(self) -> bool:
        """
        Checks if the game is a draw due to threefold repetition.

        Returns:
            bool: True if the game is a draw by threefold repetition, False otherwise.
        """
        if len(self.move_history) < 3:
            return False
        
        current_state = self.get_board_state()
        count = 1
        for past_state in self.move_history:
            if past_state == current_state:
                count += 1
                if count >= 3:
                    return True
        return False

    def is_king_in_check(self, color: str) -> bool:
        """
        Checks if the king of the specified color is in check.

        Args:
            color (str): The color of the king to check.

        Returns:
            bool: True if the king is in check, False otherwise.
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
        
        # Check if any opponent piece can attack the king
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    legal_moves = self.get_legal_moves(row, col)
                    if king_pos in legal_moves:
                        return True
        return False