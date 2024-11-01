import time
from ChessGame import ChessGame
from ChessBoard import ChessBoard
from MinimaxAgent import MinimaxAgent
from RandomAgent import RandomAgent

def visualize_board(board: ChessBoard):
    """
    Visualizes the current state of the chessboard.
    """
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

def play_game(white_agent, black_agent, max_moves=50):
    """
    Simulates a chess game between two agents.

    Args:
        white_agent: The agent playing as white.
        black_agent: The agent playing as black.
        max_moves (int, optional): The maximum number of moves allowed. Defaults to 50.

    Returns:
        list: A list of moves made during the game.
    """
    game = ChessGame(max_moves=max_moves)
    moves_history = []
    
    while game.game_status == 'ongoing':
        visualize_board(game.board)
        print(f'\nMove {game.move_count + 1}:')
        
        current_agent = white_agent if game.current_player == 'white' else black_agent
        
        start_time = time.time()
        move = current_agent.get_move(game)
        end_time = time.time()
        
        if move is None:
            print(f'Game Over - No legal moves for {game.current_player}')
            break
        
        print(f'Move time: {end_time - start_time:.2f} seconds')
        
        from_pos, to_pos = move
        from_square = chr(from_pos[1] + ord('a')) + str(8 - from_pos[0])
        to_square = chr(to_pos[1] + ord('a')) + str(8 - to_pos[0])
        print(f'{game.current_player} moves: {from_square} -> {to_square}')
        
        moves_history.append((from_pos, to_pos))
        if not game.make_move(from_pos, to_pos):
            print(f'Invalid move attempted by {game.current_player}')
            break
    
    print('\nGame Over!')
    print(f'Result: {game.game_status}')
    return moves_history

def main():
    """
    Main function to set up the game and start the simulation.
    """
    # Initialize agents
    minimax_agent = MinimaxAgent('white', depth=3)
    random_agent = RandomAgent('black')
    
    # Play game
    print("Starting Chess Game: Minimax (White) vs Random (Black)")
    print("=" * 50)
    
    moves_history = play_game(minimax_agent, random_agent, max_moves=50)
    
    # Print final statistics
    print('\nGame Statistics:')
    print(f'Total moves played: {len(moves_history)}')
    print('\nMove History:')
    for i, (from_pos, to_pos) in enumerate(moves_history, 1):
        from_square = chr(from_pos[1] + ord('a')) + str(8 - from_pos[0])
        to_square = chr(to_pos[1] + ord('a')) + str(8 - to_pos[0])
        print(f'Move {i}: {from_square} -> {to_square}')
    
    # Print performance metrics
    print('\nPerformance Metrics:')
    if minimax_agent.move_times:
        print(f'Minimax average move time: {sum(minimax_agent.move_times) / len(minimax_agent.move_times):.2f} seconds')
    if random_agent.move_times:
        print(f'Random agent average move time: {sum(random_agent.move_times) / len(random_agent.move_times):.2f} seconds')

if __name__ == '__main__':
    main()