class ChessPieces:
    """
    Represents a chess piece with its color and type.

    Attributes:
        color (str): The color of the piece (either 'white' or 'black').
        piece_type (str): The type of the piece (e.g., 'king', 'queen', 'rook', etc.).
        has_moved (bool): Indicates whether the piece has moved from its initial position.
    """

    def __init__(self, color: str, piece_type: str):
        """
        Initializes a ChessPiece object.

        Args:
            color (str): The color of the piece.
            piece_type (str): The type of the piece.
        """
        self.color = color
        self.piece_type = piece_type
        self.has_moved = False

    def __str__(self):
        """
        Returns the Unicode symbol representing the chess piece.

        Returns:
            str: The Unicode symbol of the piece.
        """
        symbols = {
            'white': {'king': '♔', 'queen': '♕', 'rook': '♖', 'bishop': '♗', 'knight': '♘', 'pawn': '♙'},
            'black': {'king': '♚', 'queen': '♛', 'rook': '♜', 'bishop': '♝', 'knight': '♞', 'pawn': '♟'}
        }
        return symbols[self.color][self.piece_type]