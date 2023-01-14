#!/usr/bin/env python3

from src.board import ChessBoard
from src.ai.minimax import MinimaxAI
from src.visualization import ChessVisualizer
import time


def play_minimax_game():
    print("=== Chess Engine Demo ===")
    print("Playing a game between Minimax AI with itself")

    board = ChessBoard()
    minimax_ai = MinimaxAI(depth=3)
    visualizer = ChessVisualizer()

    move_count = 0
    max_moves = 100

    print(f"\nInitial position:")
    visualizer.display_board(board, title="Starting Position")

    while not board.is_game_over() and move_count < max_moves:
        print(f"\n--- Move {move_count + 1} ---")

        start_time = time.time()
        move = minimax_ai.get_best_move(board)
        end_time = time.time()

        if move:
            san_move = board.get_move_san(move)
            print(f"Move: {san_move} ({board.get_move_uci(move)})")
            print(f"Time: {end_time - start_time:.2f} seconds")
            print(f"Nodes evaluated: {minimax_ai.get_stats()['nodes_evaluated']}")

            board.make_move(move)
            move_count += 1

            print(f"Position after move:")
            visualizer.display_board(board, title=f"After {san_move}")

            if board.is_check():
                print("CHECK!")
            if board.is_checkmate():
                winner = "White" if board.get_winner() else "Black"
                print(f"CHECKMATE! {winner} wins!")
                break
        else:
            print("No legal moves available")
            break

    if not board.is_game_over():
        print(f"\nGame ended after {move_count} moves (max reached)")

    print(
        f"\nFinal position evaluation: {minimax_ai.evaluator.evaluate_position(board):.2f}"
    )


if __name__ == "__main__":
    play_minimax_game()
