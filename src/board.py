import chess
import numpy as np
from typing import List


class ChessBoard:
    def __init__(self, fen: str = chess.STARTING_FEN):
        self.board = chess.Board(fen)
        self.move_history = []

    def get_legal_moves(self) -> List[chess.Move]:
        return list(self.board.legal_moves)

    def make_move(self, move: chess.Move) -> bool:
        if move in self.board.legal_moves:
            self.move_history.append(move)
            self.board.push(move)
            return True
        return False

    def undo_move(self) -> bool:
        if self.move_history:
            self.board.pop()
            self.move_history.pop()
            return True
        return False

    def is_game_over(self) -> bool:
        return self.board.is_game_over()

    def get_fen(self) -> str:
        return self.board.fen()

    def get_turn(self) -> bool:
        return self.board.turn

    def get_board_array(self) -> np.ndarray:
        board_array = np.zeros((8, 8), dtype=int)
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                rank, file = divmod(square, 8)
                value = piece.piece_type
                if piece.color == chess.BLACK:
                    value = -value
                board_array[7 - rank, file] = value
        return board_array

    def copy(self) -> "ChessBoard":
        new_board = ChessBoard()
        new_board.move_history = self.move_history.copy()
        # Replay all moves from the beginning
        for move in self.move_history:
            new_board.board.push(move)
        return new_board
