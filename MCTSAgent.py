import time
import random
import math
import copy
from typing import Tuple, Optional, List, Dict, TYPE_CHECKING
from collections import defaultdict

if TYPE_CHECKING:
    from ChessGame import ChessGame
    from ChessBoard import ChessBoard

class MCTSNode:
    """
    Node class for MCTS tree.
    """
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move  # Move that led to this state
        self.children = {}  # Dict of move: MCTSNode
        self.wins = 0
        self.visits = 0
        self.untried_moves = self._get_untried_moves()
        self.rave_wins = defaultdict(int)  # For RAVE variant
        self.rave_visits = defaultdict(int)  # For RAVE variant
        
    def _get_untried_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Gets list of untried moves from current state."""
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = self.game_state.board.board[row][col]
                if piece and piece.color == self.game_state.current_player:
                    legal_moves = self.game_state.board.get_legal_moves(row, col)
                    possible_moves.extend([((row, col), move) for move in legal_moves])
        return possible_moves

    def is_terminal(self) -> bool:
        """Checks if node represents a terminal game state."""
        return self.game_state.game_status != 'ongoing'

    def is_fully_expanded(self) -> bool:
        """Checks if all possible moves have been tried."""
        return len(self.untried_moves) == 0

class MCTSAgent:
    """
    Base MCTS agent with configurable variants.
    """
    def __init__(self, color: str, simulation_time: float = 1.0, exploration_weight: float = 1.41,
                 variant: str = 'standard', rave_constant: float = 300):
        self.color = color
        self.simulation_time = simulation_time
        self.exploration_weight = exploration_weight
        self.variant = variant
        self.rave_constant = rave_constant
        self.move_history = defaultdict(lambda: {'wins': 0, 'visits': 0})
        self.move_times = []

    def get_move(self, game: 'ChessGame') -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Gets best move using specified MCTS variant."""
        if game.game_status != 'ongoing' or game.current_player != self.color:
            return None

        # Get all possible moves first
        possible_moves = []
        for row in range(8):
            for col in range(8):
                piece = game.board.board[row][col]
                if piece and piece.color == self.color:
                    legal_moves = game.board.get_legal_moves(row, col)
                    possible_moves.extend([((row, col), move) for move in legal_moves])
        
        # If no legal moves, return None
        if not possible_moves:
            return None
            
        # If only one move possible, return it immediately
        if len(possible_moves) == 1:
            return possible_moves[0]

        start_time = time.time()
        root = MCTSNode(copy.deepcopy(game))
        
        # Run MCTS for specified time
        end_time = start_time + self.simulation_time
        while time.time() < end_time:
            node = root
            game_copy = copy.deepcopy(game)
            
            # Selection
            while not node.is_terminal() and node.is_fully_expanded():
                selected = self._select_child(node)
                if selected is None:
                    break
                node = selected
                if node.move:
                    game_copy.make_move(*node.move)
            
            # Expansion
            if not node.is_terminal() and node.untried_moves:
                move = random.choice(node.untried_moves)
                node.untried_moves.remove(move)
                game_copy.make_move(*move)
                child = MCTSNode(game_copy, parent=node, move=move)
                node.children[move] = child
                node = child
            
            # Simulation
            game_simulation = copy.deepcopy(game_copy)
            result = self._simulate(game_simulation)
            
            # Backpropagation
            self._backpropagate(node, result)
        
        # Select best move
        best_move = self._select_best_move(root)
        
        move_time = time.time() - start_time
        self.move_times.append(move_time)
        
        return best_move

    def _select_child(self, node: MCTSNode) -> Optional[MCTSNode]:
        """
        Selects child node based on MCTS variant.
        """
        if not node.children:
            return None
            
        if self.variant == 'standard':
            return self._uct_select(node)
        elif self.variant == 'progressive':
            return self._progressive_history_select(node)
        elif self.variant == 'rave':
            return self._rave_select(node)
        else:
            raise ValueError(f"Unknown MCTS variant: {self.variant}")

    def _uct_select(self, node: MCTSNode) -> MCTSNode:
        """Standard UCT selection."""
        best_score = float('-inf')
        best_child = None
        
        for move, child in node.children.items():
            if child.visits == 0:
                return child
                
            # UCT formula
            exploit = child.wins / child.visits
            explore = math.sqrt(math.log(node.visits) / child.visits)
            score = exploit + self.exploration_weight * explore
            
            if score > best_score:
                best_score = score
                best_child = child
                
        return best_child

    def _progressive_history_select(self, node: MCTSNode) -> MCTSNode:
        """Progressive history selection with move history influence."""
        best_score = float('-inf')
        best_child = None
        
        for move, child in node.children.items():
            if child.visits == 0:
                return child
            
            # Combine UCT with move history
            move_history = self.move_history[move]
            history_score = move_history['wins'] / max(move_history['visits'], 1)
            
            exploit = child.wins / child.visits
            explore = math.sqrt(math.log(node.visits) / child.visits)
            history_weight = 0.1  # Weight for historical influence
            
            score = (1 - history_weight) * (exploit + self.exploration_weight * explore) + \
                   history_weight * history_score
            
            if score > best_score:
                best_score = score
                best_child = child
                
        return best_child

    def _rave_select(self, node: MCTSNode) -> MCTSNode:
        """RAVE selection using rapid action value estimation."""
        best_score = float('-inf')
        best_child = None
        
        for move, child in node.children.items():
            if child.visits == 0:
                return child
            
            # RAVE formula
            beta = math.sqrt(self.rave_constant / (3 * node.visits + self.rave_constant))
            
            # MC score
            mc_score = child.wins / child.visits
            
            # AMAF score (All-Moves-As-First)
            amaf_score = child.rave_wins[move] / max(child.rave_visits[move], 1)
            
            # Combine scores
            score = (1 - beta) * mc_score + beta * amaf_score + \
                   self.exploration_weight * math.sqrt(math.log(node.visits) / child.visits)
            
            if score > best_score:
                best_score = score
                best_child = child
                
        return best_child

    def _simulate(self, game: 'ChessGame') -> float:
        """
        Simulates random game from current state until terminal state.
        Returns 1 for win, 0 for loss/draw.
        """
        max_moves = 100  # Prevent infinite games
        moves_made = 0
        original_player = game.current_player
        
        try:
            while game.game_status == 'ongoing' and moves_made < max_moves:
                possible_moves = []
                for row in range(8):
                    for col in range(8):
                        piece = game.board.board[row][col]
                        if piece and piece.color == game.current_player:
                            legal_moves = game.board.get_legal_moves(row, col)
                            possible_moves.extend([((row, col), move) for move in legal_moves])
                
                if not possible_moves:
                    break
                    
                move = random.choice(possible_moves)
                if not game.make_move(*move):
                    break
                moves_made += 1
        except Exception as e:
            print(f"Simulation error: {e}")
            return 0.5  # Return draw in case of error
        
        if game.game_status == 'checkmate':
            return 1.0 if game.current_player != self.color else 0.0
        else:
            return 0.5  # Draw

    def _backpropagate(self, node: MCTSNode, result: float):
        """
        Backpropagates simulation result up the tree.
        Updates both regular and RAVE statistics.
        """
        while node:
            node.visits += 1
            node.wins += result
            
            # Update RAVE statistics if using RAVE variant
            if self.variant == 'rave' and node.parent:
                move = node.move
                if move:
                    node.parent.rave_visits[move] += 1
                    node.parent.rave_wins[move] += result
            
            # Update move history for progressive history variant
            if self.variant == 'progressive' and node.move:
                self.move_history[node.move]['visits'] += 1
                self.move_history[node.move]['wins'] += result
            
            node = node.parent

    def _select_best_move(self, root: MCTSNode) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Selects best move based on most visited child."""
        if not root.children:
            return None
            
        best_visits = -1
        best_move = None
        
        for move, child in root.children.items():
            if child.visits > best_visits:
                best_visits = child.visits
                best_move = move
                
        return best_move
