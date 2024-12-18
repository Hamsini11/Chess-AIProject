import time
import random
import copy
from ChessGame import ChessGame
from ChessBoard import ChessBoard
from typing import Tuple, Optional, List, Union

class MinimaxAgent:
    def __init__(self, color: str, depth: int = 3, strategy: str = 'minimax', beam_width: int = 3):
        self.color = color
        self.depth = depth
        self.strategy = strategy
        self.beam_width = beam_width
        self.move_times = []

    def detect_threats(self, board: ChessBoard, color: str) -> dict[Tuple[int, int], List[Tuple[int, int]]]:
        """
        Detects threats to pieces of a specific color.

        Args:
            board (ChessBoard): The current state of the chessboard.
            color (str): Color of pieces to check for threats.

        Returns:
            Dict of pieces with their potential threats.
        """
        opponent_color = 'black' if color == 'white' else 'white'
        threats = {}

        # Get all opponent's attacked squares
        attacked_squares = board.get_all_attacked_squares(opponent_color)

        # Check each piece of the specified color
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece.color == color:
                    # If this piece's square is in opponent's attacked squares
                    if (row, col) in attacked_squares:
                        # Find which opponent pieces are threatening it
                        threatening_pieces = []
                        for t_row in range(8):
                            for t_col in range(8):
                                threat_piece = board.board[t_row][t_col]
                                if threat_piece and threat_piece.color == opponent_color:
                                    potential_moves = board._get_raw_attacked_squares(t_row, t_col)
                                    if (row, col) in potential_moves:
                                        threatening_pieces.append((t_row, t_col))
                        
                        if threatening_pieces:
                            threats[(row, col)] = threatening_pieces

        return threats

    def evaluate_board(self, board: ChessBoard, include_checkmate: bool = True) -> float:
        # Use the ChessBoard's evaluate_board method directly
        return board.evaluate_board(board, include_checkmate)

    def evaluate_move_priority(self, game: ChessGame, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> float:
        """
        Evaluates move priority based on strategic considerations.

        Args:
            game (ChessGame): The current game state.
            from_pos (Tuple[int, int]): Starting position of the move.
            to_pos (Tuple[int, int]): Ending position of the move.

        Returns:
            float: Priority score for the move.
        """
        piece = game.board.board[from_pos[0]][from_pos[1]]
        target = game.board.board[to_pos[0]][to_pos[1]]
        priority = 0

        # 1. Checkmate priority
        temp_game = copy.deepcopy(game)
        temp_game.make_move(from_pos, to_pos)
        if temp_game.board.is_checkmate(temp_game.current_player):
            return float('inf')

        # 2. Capture priority
        if target and target.color != piece.color:
            priority += 10 * game.board.piece_values.get(target.piece_type, 0)

        # 3. Avoiding capture
        threats = self.detect_threats(game.board, piece.color)
        if from_pos in threats:
            priority -= 5  # Penalty for moving from a threatened square

        # 4. Protecting pieces under threat
        my_threats = self.detect_threats(game.board, piece.color)
        for threatened_piece in my_threats:
            if abs(threatened_piece[0] - to_pos[0]) <= 1 and abs(threatened_piece[1] - to_pos[1]) <= 1:
                priority += 5  # Bonus for moves that protect threatened pieces

        # 5. King safety for check situations
        if piece.piece_type == 'king':
            opponent_color = 'black' if piece.color == 'white' else 'white'
            if game.board.is_king_in_check(piece.color):
                priority += 10  # Prioritize king moves when in check

        return priority

    def beam_search(self, game: ChessGame, depth: int) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Implements beam search strategy for move selection.

        Args:
            game (ChessGame): The current game state.
            depth (int): Search depth.

        Returns:
            Optional[Tuple[Tuple[int, int], Tuple[int, int]]]: The best move found.
        """
        possible_moves = []
        
        # Collect all possible moves
        for row in range(8):
            for col in range(8):
                piece = game.board.board[row][col]
                if piece is not None and piece.color == self.color:
                    legal_moves = game.board.get_legal_moves(row, col)
                    possible_moves.extend([((row, col), move) for move in legal_moves])
        
        if not possible_moves:
            return None
        
        # Rank moves by their initial evaluation
        move_rankings = []
        for move in possible_moves:
            # Simulate the move using a deep copy
            from_pos, to_pos = move
            temp_game = copy.deepcopy(game)
            result = temp_game.make_move(from_pos, to_pos)
            
            if result:
                # Evaluate the resulting board state
                score = self.evaluate_board(temp_game.board)
                move_rankings.append((move, score))
        
        # Select top moves based on beam width
        if move_rankings:
            move_rankings.sort(key=lambda x: x[1], reverse=True)
            selected_moves = move_rankings[:self.beam_width]
            return random.choice(selected_moves)[0]
        
        return None

    def iterative_deepening(self, game: ChessGame) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Implements iterative deepening search strategy.

        Args:
            game (ChessGame): The current game state.

        Returns:
            Optional[Tuple[Tuple[int, int], Tuple[int, int]]]: The best move found.
        """
        best_move = None
        for current_depth in range(1, self.depth + 1):
            try:
                _, current_best_move = self.minimax(copy.deepcopy(game), current_depth, float('-inf'), float('inf'), True)
                if current_best_move:
                    best_move = current_best_move
            except Exception:
                break
        
        return best_move

    def minimax(self, game: ChessGame, depth: int, alpha: float, beta: float, 
                maximizing_player: bool) -> Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """
        Enhanced minimax algorithm with threat-aware move selection.

        Args:
            game (ChessGame): The current game state.
            depth (int): The current depth of the search tree.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.
            maximizing_player (bool): Whether the current player is maximizing or minimizing.

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
                            # Prioritize moves
                            move_priority = self.evaluate_move_priority(game, (row, col), move)
                            
                            # Use deep copy for game state
                            temp_game = copy.deepcopy(game)
                            result = temp_game.make_move((row, col), move)
                            
                            if result:
                                eval_score, _ = self.minimax(temp_game, depth - 1, alpha, beta, False)
                                
                                # Adjust score with move priority
                                eval_score += move_priority
                                
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
                            # Use deep copy for game state
                            temp_game = copy.deepcopy(game)
                            result = temp_game.make_move((row, col), move)
                            
                            if result:
                                eval_score, _ = self.minimax(temp_game, depth - 1, alpha, beta, True)
                                
                                min_eval = min(min_eval, eval_score)
                                beta = min(beta, eval_score)
                                if beta <= alpha:
                                    break
            
            return min_eval, None

    def get_move(self, game: ChessGame) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Gets the best move for the agent and checks for game termination.

        Args:
            game (ChessGame): The current game state.

        Returns:
            Optional move or None if game is over.
        """
        # First, check game status
        game_status = game.check_game_status()
        if game_status != 'ongoing':
            return None

        if game.current_player != self.color:
            return None

        start_time = time.time()
   
        # Rest of your existing move selection logic remains the same
        if self.strategy == 'beam_search':
            best_move = self.beam_search(game, self.depth)
        elif self.strategy == 'iterative_deepening':
            best_move = self.iterative_deepening(game)
        else:  # Default to standard minimax
            _, best_move = self.minimax(copy.deepcopy(game), self.depth, float('-inf'), float('inf'), True)
    
        end_time = time.time()

        self.move_times.append(end_time - start_time)
        return best_move

    def evaluate_endgame_strategy(self, board: ChessBoard) -> float:
        """
        Enhanced endgame evaluation focusing on king safety, piece coordination, and strategic positioning.
    
        Args:
            board (ChessBoard): The current state of the chessboard.
    
        Returns:
            float: Endgame strategy score.
        """

        endgame_score = 0
        piece_values = {
            'pawn': 1,
            'knight': 3,
            'bishop': 3,
            'rook': 5,
            'queen': 9,
            'king': 0
        }

        # Count remaining pieces
        my_pieces = [piece for row in board.board for piece in row if piece and piece.color == self.color]
        opponent_pieces = [piece for row in board.board for piece in row if piece and piece.color != self.color]

        # King centralization bonus
        my_king = next((piece for row in board.board for piece in row 
                    if piece and piece.color == self.color and piece.piece_type == 'king'), None)
        opponent_king = next((piece for row in board.board for piece in row 
                           if piece and piece.color != self.color and piece.piece_type == 'king'), None)

        if my_king and opponent_king:
            # King centralization score
            king_center_distance = abs(my_king.row - 3.5) + abs(my_king.col - 3.5)
            endgame_score += (8 - king_center_distance) * 0.5

            # King proximity to opponent king can indicate endgame control
            king_distance = abs(my_king.row - opponent_king.row) + abs(my_king.col - opponent_king.col)
            endgame_score += (14 - king_distance) * 0.3

        # Pawn advancement bonus
        pawn_advancement_bonus = sum(
            (7 - row if piece.color == 'white' else row) 
            for row in range(8) 
            for piece in board.board[row] 
            if piece and piece.piece_type == 'pawn' and piece.color == self.color
        )
        endgame_score += pawn_advancement_bonus * 0.2

        # Piece mobility and control
        total_mobility = len(board.get_all_attacked_squares(self.color))
        opponent_mobility = len(board.get_all_attacked_squares('white' if self.color == 'black' else 'black'))
        endgame_score += (total_mobility - opponent_mobility) * 0.1

        # Material advantage with endgame weighting
        material_difference = sum(
            piece_values.get(piece.piece_type, 0) for piece in my_pieces
        ) - sum(
            piece_values.get(piece.piece_type, 0) for piece in opponent_pieces
        )
        endgame_score += material_difference * 1.5

        return endgame_score
