import numpy as np
import chess
import random
from typing import Optional, List, Tuple
from ..board import ChessBoard
from ..evaluation import PositionEvaluator


class SimpleNeuralNetwork:
    def __init__(
        self, input_size: int = 64, hidden_size: int = 128, output_size: int = 1
    ):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.weights1 = np.random.randn(input_size, hidden_size) * 0.01
        self.bias1 = np.zeros((1, hidden_size))
        self.weights2 = np.random.randn(hidden_size, output_size) * 0.01
        self.bias2 = np.zeros((1, output_size))

    def forward(self, x: np.ndarray) -> np.ndarray:
        z1 = np.dot(x, self.weights1) + self.bias1
        a1 = np.tanh(z1)
        z2 = np.dot(a1, self.weights2) + self.bias2
        return z2

    def train(
        self,
        training_data: List[Tuple[np.ndarray, float]],
        epochs: int = 100,
        learning_rate: float = 0.01,
    ):
        for epoch in range(epochs):
            total_loss = 0
            for x, y in training_data:
                x = x.reshape(1, -1)
                y = np.array([[y]])

                z1 = np.dot(x, self.weights1) + self.bias1
                a1 = np.tanh(z1)
                z2 = np.dot(a1, self.weights2) + self.bias2

                loss = z2 - y
                total_loss += np.mean(loss**2)

                dz2 = loss
                dw2 = np.dot(a1.T, dz2)
                db2 = np.sum(dz2, axis=0, keepdims=True)

                dz1 = np.dot(dz2, self.weights2.T) * (1 - np.tanh(z1) ** 2)
                dw1 = np.dot(x.T, dz1)
                db1 = np.sum(dz1, axis=0, keepdims=True)

                self.weights2 -= learning_rate * dw2
                self.bias2 -= learning_rate * db2
                self.weights1 -= learning_rate * dw1
                self.bias1 -= learning_rate * db1

            if epoch % 10 == 0:
                print(f"Epoch {epoch}, Loss: {total_loss / len(training_data):.6f}")


class NeuralNetAI:
    def __init__(
        self,
        network: Optional[SimpleNeuralNetwork] = None,
        evaluator: Optional[PositionEvaluator] = None,
    ):
        self.network = network or SimpleNeuralNetwork()
        self.evaluator = evaluator or PositionEvaluator()
        self.nodes_evaluated = 0

    def get_best_move(self, board: ChessBoard) -> chess.Move:
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return None

        best_move = None
        best_value = float("-inf") if board.get_turn() else float("inf")

        for move in legal_moves:
            board.make_move(move)
            value = self._evaluate_position(board)
            board.undo_move()

            if board.get_turn():
                if value > best_value:
                    best_value = value
                    best_move = move
            else:
                if value < best_value:
                    best_value = value
                    best_move = move

        return best_move or random.choice(legal_moves)

    def _evaluate_position(self, board: ChessBoard) -> float:
        self.nodes_evaluated += 1

        if board.is_checkmate():
            return -10000 if board.get_turn() else 10000

        if board.is_stalemate():
            return 0

        board_array = board.get_board_array()
        input_data = board_array.flatten().astype(np.float32) / 6.0

        evaluation = self.network.forward(input_data)[0, 0]
        return evaluation * 1000

    def train_on_positions(self, positions: List[Tuple[str, float]], epochs: int = 100):
        training_data = []
        for fen, target_value in positions:
            board = ChessBoard(fen)
            board_array = board.get_board_array()
            input_data = board_array.flatten().astype(np.float32) / 6.0
            training_data.append((input_data, target_value))

        self.network.train(training_data, epochs=epochs)

    def reset_stats(self):
        self.nodes_evaluated = 0

    def get_stats(self) -> dict:
        return {
            "nodes_evaluated": self.nodes_evaluated,
            "network_layers": [
                self.network.input_size,
                self.network.hidden_size,
                self.network.output_size,
            ],
        }
