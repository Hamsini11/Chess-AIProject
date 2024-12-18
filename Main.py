import time
from ChessGame import ChessGame
from ChessBoard import ChessBoard
from MinimaxAgent import MinimaxAgent
from MCTSAgent import MCTSAgent
import random

random.seed(42)  # Fixed seed for reproducible randomness

def visualize_board(board: ChessBoard):
    """Visualizes the current state of the chessboard."""
    print('\n    a b c d e f g h')
    print('  ┌─────────────────┐')
    
    for row in range(8):
        print(f'{8-row} │', end=' ')
        for col in range(8):
            piece = board.board[row][col]
            if piece is None:
                print('·', end=' ')
            else:
                print(str(piece), end=' ')
        print(f'│ {8-row}')
    
    print('  └─────────────────┘')
    print('    a b c d e f g h\n')

def play_game(white_agent, black_agent, max_moves=50, verbose=True):
    """Simulates a chess game between two agents."""
    game = ChessGame(max_moves=max_moves)
    moves_history = []
    performance_metrics = {'white': [], 'black': []}
    
    while game.game_status == 'ongoing':
        if verbose:
            visualize_board(game.board)
            print(f'\nMove {game.move_count + 1}:')
        
        current_agent = white_agent if game.current_player == 'white' else black_agent
        
        start_time = time.time()
        move = current_agent.get_move(game)
        end_time = time.time()
        move_time = end_time - start_time
        
        color = game.current_player
        performance_metrics[color].append(move_time)
        
        if move is None:
            if verbose:
                print(f'Game Over - No legal moves for {game.current_player}')
            break
        
        if verbose:
            print(f'Move time: {move_time:.2f} seconds')
            from_pos, to_pos = move
            from_square = chr(from_pos[1] + ord('a')) + str(8 - from_pos[0])
            to_square = chr(to_pos[1] + ord('a')) + str(8 - to_pos[0])
            print(f'{game.current_player} moves: {from_square} -> {to_square}')
        
        moves_history.append((move, game.current_player))
        if not game.make_move(*move):
            if verbose:
                print(f'Invalid move attempted by {game.current_player}')
            break
    
    if verbose:
        print('\nGame Over!')
        print(f'Result@playGame: {game.game_status}')
        visualize_board(game.board)
    
    return moves_history, game.game_status, performance_metrics

def compare_all_strategies():
    """Compares all MCTS and Minimax strategy combinations."""
    minimax_strategies = [
        ('Standard Minimax', 'minimax', 3),
        ('Beam Search', 'beam_search', 3),
        ('Iterative Deepening', 'iterative_deepening', 3)
    ]
    
    mcts_strategies = [
        ('Standard MCTS', 'standard', 1.0),
        ('Progressive MCTS', 'progressive', 1.0),
        ('RAVE MCTS', 'rave', 1.0)
    ]
    
    all_strategies = []
    
    # Create Minimax strategies
    for name, strategy_type, depth in minimax_strategies:
        all_strategies.append(('minimax', name, 
                             lambda color, n=name, s=strategy_type, d=depth: 
                             MinimaxAgent(color, depth=d, strategy=s)))
    
    # Create MCTS strategies
    for name, variant, sim_time in mcts_strategies:
        all_strategies.append(('mcts', name, 
                             lambda color, v=variant, t=sim_time: 
                             MCTSAgent(color, simulation_time=t, variant=v)))
    
    results = []
    
    # Play each strategy combination
    for i, (type1, name1, creator1) in enumerate(all_strategies):
        for j, (type2, name2, creator2) in enumerate(all_strategies):
            if i <= j and i != j:  # Avoids duplicate matchups with reversed colors and same strategy comparisons
            # if name1 == 'Standard Minimax' and name2 == 'Standard MCTS':
                print(f"\n{'-'*70}")
                print(f"Match: {name1} (White) vs {name2} (Black)")
                print(f"{'-'*70}")
                
                # Initialize agents
                white_agent = creator1('white')
                black_agent = creator2('black')
                
                # Play game
                moves_history, result, metrics = play_game(white_agent, black_agent, max_moves=50)
                
                # Record results
                match_data = {
                    'white_type': type1,
                    'black_type': type2,
                    'white_strategy': name1,
                    'black_strategy': name2,
                    'result': result,
                    'total_moves': len(moves_history),
                    'white_avg_time': sum(metrics['white']) / len(metrics['white']) if metrics['white'] else 0,
                    'black_avg_time': sum(metrics['black']) / len(metrics['black']) if metrics['black'] else 0
                }
                results.append(match_data)
                
                # Print match summary
                print('\nMatch Summary:')
                print(f'Result@compareallStrategies: {result}')
                print(f'Total moves: {match_data["total_moves"]}')
                print(f'White ({name1}) average move time: {match_data["white_avg_time"]:.2f} seconds')
                print(f'Black ({name2}) average move time: {match_data["black_avg_time"]:.2f} seconds')
    
    return results

def analyze_results(results):
    """Analyzes and prints comprehensive results of strategy comparisons."""
    print("\n=== Strategy Comparison Results ===\n")
    
    # Calculate strategy statistics
    strategy_stats = {}
    
    for result in results:
        # Initialize stats for new strategies
        for agent_type, strategy in [(result['white_type'], result['white_strategy']), 
                                   (result['black_type'], result['black_strategy'])]:
            key = f"{agent_type}_{strategy}"
            if key not in strategy_stats:
                strategy_stats[key] = {
                    'type': agent_type,
                    'name': strategy,
                    'games': 0,
                    'wins': 0,
                    'draws': 0,
                    'draws_by_repetition': 0,
                    'draws_by_moves': 0,
                    'stalemates': 0,
                    'total_time': 0,
                    'total_moves': 0
                }
    
        # Update statistics
        white_key = f"{result['white_type']}_{result['white_strategy']}"
        black_key = f"{result['black_type']}_{result['black_strategy']}"
        white_stats = strategy_stats[white_key]
        black_stats = strategy_stats[black_key]
        
        # Update game counts
        white_stats['games'] += 1
        black_stats['games'] += 1
        
        # Update results based on game outcome
        if result['result'] == 'checkmate':
            if result['total_moves'] % 2 == 0:  # Black won
                black_stats['wins'] += 1
            else:  # White won
                white_stats['wins'] += 1
        else:  # Different types of draws
            white_stats['draws'] += 1
            black_stats['draws'] += 1
            
            # Track specific draw types
            if result['result'] == 'draw_by_repetition':
                white_stats['draws_by_repetition'] += 1
                black_stats['draws_by_repetition'] += 1
            elif result['result'] == 'draw_by_moves':
                white_stats['draws_by_moves'] += 1
                black_stats['draws_by_moves'] += 1
            elif result['result'] == 'stalemate':
                white_stats['stalemates'] += 1
                black_stats['stalemates'] += 1
        
        # Update timing and move statistics
        white_stats['total_time'] += result['white_avg_time']
        black_stats['total_time'] += result['black_avg_time']
        white_stats['total_moves'] += result['total_moves']
        black_stats['total_moves'] += result['total_moves']
    
    # Print strategy performance
    print("\nDetailed Strategy Performance:")
    print("=" * 50)
    
    # Group strategies by type
    minimax_stats = {k: v for k, v in strategy_stats.items() if v['type'] == 'minimax'}
    mcts_stats = {k: v for k, v in strategy_stats.items() if v['type'] == 'mcts'}
    
    def print_strategy_group(title, stats_dict):
        print(f"\n{title}")
        print("-" * 40)
        for _, stats in sorted(stats_dict.items()):
            print(f"\nStrategy: {stats['name']}")
            print(f"Games played: {stats['games']}")
            print(f"Wins: {stats['wins']} ({stats['wins']/stats['games']*100:.1f}%)")
            print(f"Total Draws: {stats['draws']} ({stats['draws']/stats['games']*100:.1f}%)")
            print(f"  - Draws by repetition: {stats['draws_by_repetition']}")
            print(f"  - Draws by move limit: {stats['draws_by_moves']}")
            print(f"  - Stalemates: {stats['stalemates']}")
            print(f"Average move time: {stats['total_time']/stats['games']:.2f} seconds")
            print(f"Average game length: {stats['total_moves']/stats['games']:.1f} moves")
    
    print_strategy_group("Minimax Strategies", minimax_stats)
    print_strategy_group("MCTS Strategies", mcts_stats)
    
    # Print head-to-head statistics
    print("\nHead-to-Head Results:")
    print("=" * 50)
    
    for result in results:
        print(f"\n{result['white_strategy']} (White) vs {result['black_strategy']} (Black)")
        print(f"Result@analyzeResults: {result['result']}")
        print(f"Moves: {result['total_moves']}")
        print(f"Average move times - White: {result['white_avg_time']:.2f}s, Black: {result['black_avg_time']:.2f}s")

def main():
    """Main function to run strategy comparisons and analysis."""
    print("Starting Chess Strategy Tournament...")
    print("Comparing Minimax and MCTS variants...")
    results = compare_all_strategies()
    analyze_results(results)

if __name__ == '__main__':
    main()
