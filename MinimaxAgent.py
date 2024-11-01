import time
from ChessGame import ChessGame
from ChessBoard import ChessBoard
from typing import Tuple, Optional

class MinimaxAgent:
    """
    A Minimax agent for playing chess.

    Attributes:
        color (str): The color of the agent (either 'white' or 'black').
        depth (int): The maximum search depth for the minimax algorithm.
        move_times (list): A list to store the time taken for each move.
    """
    def __init__(self, color: str, depth: int = 3):
        self.color = color
        self.depth = depth
        self.move_times = []

    def evaluate_board(self, board: ChessBoard) -> float:
        """
        Evaluates the current board position based on material advantage.

        Args:
            board (ChessBoard): The current state of the chessboard.

        Returns:
            float: A score representing the evaluation of the position.
        """
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0
        }
        
        score = 0
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece is not None:
                    value = piece_values[piece.piece_type]
                    if piece.color == self.color:
                        score += value
                    else:
                        score -= value
        
        return score

    def minimax(self, game: ChessGame, depth: int, alpha: float, beta: float, 
                maximizing_player: bool) -> Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """
        Implements the minimax algorithm with alpha-beta pruning.

        Args:
            game (ChessGame): The current game state.
            depth (int): The current depth of the search tree.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.
            maximizing_player (bool):   
            Whether the current player is maximizing or minimizing.

        Returns:
            Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]: A tuple containing the evaluation score and the best move.
        """
        if depth == 0 or game.game_status != 'ongoing':
            return self.evaluate_board(game.board), None
        
        best_move = None
        if maximizing_player:
            max_eval = float('-inf')
            for row in range(8):
                for col in range(8):
                    piece = game.board.board[row][col]
                    if piece is not None and piece.color == self.color:
                        legal_moves = game.board.get_legal_moves(row, col)
                        for move in legal_moves:
                            # Make temporary move
                            temp_piece = game.board.board[move[0]][move[1]]
                            game.board.board[move[0]][move[1]] = piece
                            game.board.board[row][col] = None
                            
                            eval_score, _ = self.minimax(game, depth - 1, alpha, beta, False)
                            
                            # Undo move
                            game.board.board[row][col] = piece
                            game.board.board[move[0]][move[1]] = temp_piece
                            
                            if eval_score > max_eval:
                                max_eval = eval_score
                                best_move = ((row, col), move)
                            alpha = max(alpha, eval_score)
                            if beta <= alpha:
                                break
                            
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for row in range(8):
                for col in range(8):
                    piece = game.board.board[row][col]
                    if piece is not None and piece.color != self.color:
                        legal_moves = game.board.get_legal_moves(row, col)
                        for move in legal_moves:
                            # Make temporary move
                            temp_piece = game.board.board[move[0]][move[1]]
                            game.board.board[move[0]][move[1]] = piece
                            game.board.board[row][col] = None
                            
                            eval_score, _ = self.minimax(game, depth - 1, alpha, beta, True)
                            
                            # Undo move
                            game.board.board[row][col] = piece
                            game.board.board[move[0]][move[1]] = temp_piece
                            
                            min_eval = min(min_eval, eval_score)
                            beta = min(beta, eval_score)
                            if beta <= alpha:
                                break
                            
            return min_eval, None

    def get_move(self, game: ChessGame) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Gets the best move for the agent using the minimax algorithm.

        Args:
            game (ChessGame): The current game state.

        Returns:
            Optional[Tuple[Tuple[int, int], Tuple[int, int]]]: The best move, or None if it's not the agent's turn.
        """
        if game.current_player != self.color:
            return None
        
        start_time = time.time()
        _, best_move = self.minimax(game, self.depth, float('-inf'), float('inf'), True)
        end_time = time.time()
        
        self.move_times.append(end_time - start_time)
        return best_move
