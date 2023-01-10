#!/usr/bin/env python3

from src.board import ChessBoard
from src.visualization import ChessVisualizer
from src.opening_book import OpeningBook
import chess


def demonstrate_opening_book():
    print("\n=== Opening Book Demo ===")

    board = ChessBoard()
    opening_book = OpeningBook()

    print("Available openings:")
    for opening in opening_book.get_available_openings():
        print(f"- {opening}")

    print(f"\nPlaying Ruy Lopez opening:")
    ruy_lopez_moves = opening_book.get_opening_moves("Ruy Lopez")

    for i, move_uci in enumerate(ruy_lopez_moves):
        move = chess.Move.from_uci(move_uci)
        san_move = board.get_move_san(move)
        print(f"Move {i+1}: {san_move}")
        board.make_move(move)

    visualizer = ChessVisualizer()
    visualizer.display_board(board, title="After Ruy Lopez Opening")


if __name__ == "__main__":
    demonstrate_opening_book()
