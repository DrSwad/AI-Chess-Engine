#!/usr/bin/env python3

import unittest
import chess
from src.board import ChessBoard


class TestChessBoard(unittest.TestCase):
    def setUp(self):
        self.board = ChessBoard()

    def test_initial_position(self):
        self.assertEqual(self.board.get_fen(), chess.STARTING_FEN)
        self.assertTrue(self.board.get_turn())
        self.assertFalse(self.board.is_game_over())

    def test_legal_moves(self):
        legal_moves = self.board.get_legal_moves()
        self.assertEqual(len(legal_moves), 20)

        for move in legal_moves:
            self.assertTrue(move in self.board.board.legal_moves)

    def test_make_move(self):
        initial_fen = self.board.get_fen()
        legal_moves = self.board.get_legal_moves()

        if legal_moves:
            move = legal_moves[0]
            self.assertTrue(self.board.make_move(move))
            self.assertNotEqual(self.board.get_fen(), initial_fen)

    def test_undo_move(self):
        legal_moves = self.board.get_legal_moves()

        if legal_moves:
            initial_fen = self.board.get_fen()
            move = legal_moves[0]

            self.board.make_move(move)
            self.board.undo_move()

            self.assertEqual(self.board.get_fen(), initial_fen)

    def test_board_array(self):
        board_array = self.board.get_board_array()
        self.assertEqual(board_array.shape, (8, 8))

        # Check that pawns are in correct positions
        self.assertEqual(board_array[6, 0], 1)  # White pawn on a2
        self.assertEqual(board_array[1, 0], -1)  # Black pawn on a7

    def test_copy(self):
        legal_moves = self.board.get_legal_moves()

        if legal_moves:
            move = legal_moves[0]
            self.board.make_move(move)

            copied_board = self.board.copy()
            self.assertEqual(copied_board.get_fen(), self.board.get_fen())

            # Make sure they're independent
            copied_board.undo_move()
            self.assertNotEqual(copied_board.get_fen(), self.board.get_fen())


if __name__ == "__main__":
    unittest.main()
