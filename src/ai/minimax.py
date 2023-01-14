import chess
import random
from typing import Optional
from ..board import ChessBoard
from ..evaluation import PositionEvaluator


class MinimaxAI:
    def __init__(self, depth: int = 3, evaluator: Optional[PositionEvaluator] = None):
        self.depth = depth
        self.evaluator = evaluator or PositionEvaluator()
        self.nodes_evaluated = 0

    def get_best_move(self, board: ChessBoard) -> chess.Move:
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return None

        best_move = None
        best_value = float("-inf") if board.get_turn() else float("inf")
        alpha = float("-inf")
        beta = float("inf")

        for move in legal_moves:
            board.make_move(move)
            value = self._minimax(
                board, self.depth - 1, alpha, beta, not board.get_turn()
            )
            board.undo_move()

            if board.get_turn():
                if value > best_value:
                    best_value = value
                    best_move = move
                alpha = max(alpha, value)
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                beta = min(beta, value)

            if alpha >= beta:
                break

        return best_move or random.choice(legal_moves)

    def _minimax(
        self, board: ChessBoard, depth: int, alpha: float, beta: float, maximizing: bool
    ) -> float:
        self.nodes_evaluated += 1

        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate_position(board)

        legal_moves = board.get_legal_moves()

        if maximizing:
            max_eval = float("-inf")
            for move in legal_moves:
                board.make_move(move)
                eval = self._minimax(board, depth - 1, alpha, beta, False)
                board.undo_move()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float("inf")
            for move in legal_moves:
                board.make_move(move)
                eval = self._minimax(board, depth - 1, alpha, beta, True)
                board.undo_move()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def reset_stats(self):
        self.nodes_evaluated = 0

    def get_stats(self) -> dict:
        return {"nodes_evaluated": self.nodes_evaluated, "search_depth": self.depth}
