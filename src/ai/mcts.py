import chess
import math
import random
from typing import Optional
from ..board import ChessBoard
from ..evaluation import PositionEvaluator


class MCTSNode:
    def __init__(self, board: ChessBoard, parent=None, move=None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.untried_moves = board.get_legal_moves()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_terminal(self):
        return self.board.is_game_over()

    def get_winner(self):
        return self.board.get_winner()


class MCTSAI:
    def __init__(
        self,
        simulations: int = 1000,
        exploration_constant: float = 1.414,
        evaluator: Optional[PositionEvaluator] = None,
    ):
        self.simulations = simulations
        self.exploration_constant = exploration_constant
        self.evaluator = evaluator or PositionEvaluator()
        self.nodes_evaluated = 0

    def get_best_move(self, board: ChessBoard) -> chess.Move:
        root = MCTSNode(board)

        for _ in range(self.simulations):
            node = root
            state = board.copy()

            while node.is_fully_expanded() and not node.is_terminal():
                node = self._select(node)
                state.make_move(node.move)

            if not node.is_terminal():
                node = self._expand(node, state)

            result = self._simulate(state)
            self._backpropagate(node, result)

        return self._get_best_child(root).move

    def _select(self, node: MCTSNode) -> MCTSNode:
        best_child = None
        best_ucb = float("-inf")

        for child in node.children:
            if child.visits == 0:
                return child

            ucb = child.value / child.visits + self.exploration_constant * math.sqrt(
                math.log(node.visits) / child.visits
            )

            if ucb > best_ucb:
                best_ucb = ucb
                best_child = child

        return best_child

    def _expand(self, node: MCTSNode, state: ChessBoard) -> MCTSNode:
        if not node.untried_moves:
            return node

        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)

        state.make_move(move)
        child = MCTSNode(state, parent=node, move=move)
        node.children.append(child)

        return child

    def _simulate(self, state: ChessBoard) -> float:
        self.nodes_evaluated += 1

        while not state.is_game_over():
            legal_moves = state.get_legal_moves()
            if not legal_moves:
                break

            move = random.choice(legal_moves)
            state.make_move(move)

        if state.is_checkmate():
            return 1.0 if state.get_winner() else 0.0
        elif state.is_stalemate():
            return 0.5
        else:
            return self.evaluator.evaluate_position(state) / 10000

    def _backpropagate(self, node: MCTSNode, result: float):
        while node is not None:
            node.visits += 1
            node.value += result
            node = node.parent

    def _get_best_child(self, node: MCTSNode) -> MCTSNode:
        best_child = None
        best_visits = -1

        for child in node.children:
            if child.visits > best_visits:
                best_visits = child.visits
                best_child = child

        return best_child

    def reset_stats(self):
        self.nodes_evaluated = 0

    def get_stats(self) -> dict:
        return {
            "nodes_evaluated": self.nodes_evaluated,
            "simulations": self.simulations,
            "exploration_constant": self.exploration_constant,
        }
