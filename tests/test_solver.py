import tempfile
import unittest
from pathlib import Path
from src.crossword_solver import CrosswordSolver, find_slots, read_board, read_dictionary

class SolverTests(unittest.TestCase):
    def setUp(self):
        self.board = [list("000"), list("000"), list("000")]
        self.words = ["CAB", "ORE", "TAN", "COT", "ARA", "BEN", "CAT", "PEN", "BAR"]

    def test_extracts_six_slots(self):
        slots = find_slots(self.board)
        self.assertEqual(6, len(slots))
        self.assertEqual(3, sum(s.direction == 'across' for s in slots))
        self.assertEqual(3, sum(s.direction == 'down' for s in slots))

    def test_demo_solution_is_consistent(self):
        solver = CrosswordSolver(self.board, self.words)
        answer = solver.solve()
        self.assertIsNotNone(answer)
        self.assertEqual(6, len(answer))
        self.assertEqual(6, len(set(answer.values())))
        grid = solver.render(answer)
        self.assertTrue(all("0" not in row for row in grid))
        self.assertTrue(all(w in self.words for w in answer.values()))

    def test_no_solution_without_six_distinct_words(self):
        self.assertIsNone(CrosswordSolver(self.board, ["CAB", "ORE", "TAN", "COT", "ARA"]).solve())

    def test_prevents_duplicate_word_assignment(self):
        self.assertIsNone(CrosswordSolver(self.board, ["AAA"]).solve())

    def test_detects_length_incompatibility(self):
        self.assertIsNone(CrosswordSolver(self.board, ["AB", "CDEF"]).solve())

    def test_blocked_cells_remain_blocked(self):
        board = [list("000"), list("0#0"), list("000")]
        slots = find_slots(board)
        self.assertEqual(4, len(slots))
        self.assertTrue(all((1, 1) not in s.cells for s in slots))

    def test_rejects_irregular_board(self):
        with self.assertRaises(ValueError):
            CrosswordSolver([list("000"), list("00")], self.words)

    def test_loaders(self):
        with tempfile.TemporaryDirectory() as folder:
            board = Path(folder) / "board.txt"
            words = Path(folder) / "words.txt"
            board.write_text("0\t0 #\n# 0 0\n", encoding="utf-8")
            words.write_text("CAB\nORE\n", encoding="latin-1")
            self.assertEqual([list("00#"), list("#00")], read_board(board))
            self.assertEqual(["CAB", "ORE"], read_dictionary(words))

if __name__ == "__main__":
    unittest.main()
