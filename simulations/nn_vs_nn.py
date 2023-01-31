#!/usr/bin/env python3

import time
import random
from typing import List, Tuple

from src.board import ChessBoard
from src.ai.neural_net import NeuralNetAI
from src.evaluation import PositionEvaluator
from src.visualization import ChessVisualizer


def collect_training_positions(
    num_positions: int = 300, max_random_moves: int = 20
) -> List[Tuple[str, float]]:
    evaluator = PositionEvaluator()
    positions: List[Tuple[str, float]] = []

    while len(positions) < num_positions:
        board = ChessBoard()
        num_moves = random.randint(0, max_random_moves)

        for _ in range(num_moves):
            legal_moves = board.get_legal_moves()
            if not legal_moves or board.is_game_over():
                break
            board.make_move(random.choice(legal_moves))

        if board.is_game_over():
            continue

        fen = board.get_fen()
        # Scale target to roughly match the network's internal output scale.
        target = evaluator.evaluate_position(board) / 1000.0
        positions.append((fen, float(target)))

    return positions


def play_nn_game():
    print("=== Chess Engine Demo ===")
    print("Playing a game between NeuralNet AI with itself")

    # Prepare and briefly train the network on simple evaluator-labeled data
    print("\nCollecting training positions...")
    positions = collect_training_positions(num_positions=400, max_random_moves=25)
    print(f"Collected {len(positions)} positions. Training...")

    nn_ai = NeuralNetAI()
    nn_ai.train_on_positions(positions, epochs=50)
    nn_ai.reset_stats()

    board = ChessBoard()
    visualizer = ChessVisualizer()

    move_count = 0
    max_moves = 100

    print(f"\nInitial position:")
    visualizer.display_board(board, title="Starting Position")

    while not board.is_game_over() and move_count < max_moves:
        print(f"\n--- Move {move_count + 1} ---")

        start_time = time.time()
        move = nn_ai.get_best_move(board)
        end_time = time.time()

        if move:
            san_move = board.get_move_san(move)
            print(f"Move: {san_move} ({board.get_move_uci(move)})")
            print(f"Time: {end_time - start_time:.2f} seconds")
            print(f"Nodes evaluated: {nn_ai.get_stats()['nodes_evaluated']}")

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
        f"\nFinal position evaluation: {nn_ai.evaluator.evaluate_position(board):.2f}"
    )


if __name__ == "__main__":
    play_nn_game()
