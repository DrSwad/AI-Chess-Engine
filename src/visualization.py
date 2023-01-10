import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from typing import Optional, List
from .board import ChessBoard


class ChessVisualizer:
    def __init__(self):
        self.piece_symbols = {
            1: "♙",
            -1: "♟",
            2: "♘",
            -2: "♞",
            3: "♗",
            -3: "♝",
            4: "♖",
            -4: "♜",
            5: "♕",
            -5: "♛",
            6: "♔",
            -6: "♚",
        }

        self.colors = {
            "light": "#F0D9B5",
            "dark": "#B58863",
            "highlight": "#FFD700",
            "check": "#FF6B6B",
        }

    def display_board(
        self,
        board: ChessBoard,
        highlight_squares: Optional[List[int]] = None,
        title: str = "Chess Position",
    ):
        fig, ax = plt.subplots(figsize=(8, 8))
        board_array = board.get_board_array()

        for rank in range(8):
            for file in range(8):
                square = rank * 8 + file
                color = (
                    self.colors["light"]
                    if (rank + file) % 2 == 0
                    else self.colors["dark"]
                )

                if highlight_squares and square in highlight_squares:
                    color = self.colors["highlight"]

                rect = patches.Rectangle(
                    (file, 7 - rank),
                    1,
                    1,
                    facecolor=color,
                    edgecolor="black",
                    linewidth=1,
                )
                ax.add_patch(rect)

                piece_value = board_array[rank, file]
                if piece_value != 0:
                    piece_symbol = self.piece_symbols[piece_value]
                    piece_color = "white" if piece_value > 0 else "black"
                    ax.text(
                        file + 0.5,
                        7 - rank + 0.5,
                        piece_symbol,
                        fontsize=30,
                        ha="center",
                        va="center",
                        color=piece_color,
                    )

        ax.set_xlim(0, 8)
        ax.set_ylim(0, 8)
        ax.set_aspect("equal")
        ax.set_xticks(np.arange(0.5, 8.5, 1))
        ax.set_yticks(np.arange(0.5, 8.5, 1))
        ax.set_xticklabels(["a", "b", "c", "d", "e", "f", "g", "h"])
        ax.set_yticklabels(["8", "7", "6", "5", "4", "3", "2", "1"])
        ax.grid(False)
        ax.set_title(title)

        plt.tight_layout()
        plt.show()
