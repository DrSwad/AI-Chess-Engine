#!/usr/bin/env python3

from src.board import ChessBoard
from src.visualization import ChessVisualizer


def show_initial_board():
    print("=== Chess Engine ===")
    print("Showing the initial board")

    board = ChessBoard()
    visualizer = ChessVisualizer()

    visualizer.display_board(board, title="Starting Position")


if __name__ == "__main__":
    show_initial_board()
