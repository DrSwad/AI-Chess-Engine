#!/usr/bin/env python3

import unittest
from src.board import ChessBoard
from src.ai.minimax import MinimaxAI


class TestMinimaxAI(unittest.TestCase):
    def setUp(self):
        self.board = ChessBoard()
        self.ai = MinimaxAI(depth=2)

    def test_get_best_move(self):
        move = self.ai.get_best_move(self.board)
        self.assertIsNotNone(move)
        self.assertIn(move, self.board.get_legal_moves())

    def test_depth_impact(self):
        ai_depth_1 = MinimaxAI(depth=1)
        ai_depth_2 = MinimaxAI(depth=2)

        move1 = ai_depth_1.get_best_move(self.board)
        move2 = ai_depth_2.get_best_move(self.board)

        stats1 = ai_depth_1.get_stats()
        stats2 = ai_depth_2.get_stats()

        self.assertLess(stats1["nodes_evaluated"], stats2["nodes_evaluated"])

    def test_checkmate_detection(self):
        # A position with checkmate
        fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        board = ChessBoard(fen)

        ai = MinimaxAI(depth=3)
        move = ai.get_best_move(board)

        # Should find a move that avoids or delays checkmate
        if board.get_legal_moves():
            self.assertIsNotNone(move)
        else:
            self.assertIsNone(move)

    def test_stats_reset(self):
        self.ai.get_best_move(self.board)
        initial_stats = self.ai.get_stats()

        self.ai.reset_stats()
        reset_stats = self.ai.get_stats()

        self.assertEqual(reset_stats["nodes_evaluated"], 0)
        self.assertGreater(initial_stats["nodes_evaluated"], 0)


if __name__ == "__main__":
    unittest.main()
