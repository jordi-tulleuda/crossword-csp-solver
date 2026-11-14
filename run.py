#!/usr/bin/env python3
"""Command-line interface for the crossword CSP solver."""
import argparse
import time
from src.crossword_solver import CrosswordSolver, read_board, read_dictionary

def main():
    parser = argparse.ArgumentParser(description="Crossword solver using backtracking, forward checking and MRV")
    parser.add_argument("--board", default="examples/crossword_demo.txt", help="Board file (0 empty, # blocked)")
    parser.add_argument("--dictionary", default="examples/dictionary_demo.txt", help="Word list, one per line")
    args = parser.parse_args()
    start = time.perf_counter()
    solver = CrosswordSolver(read_board(args.board), read_dictionary(args.dictionary))
    answer = solver.solve()
    if answer is None:
        print("No solution found.")
        return 1
    print("Solved crossword:")
    print("\n".join(solver.render(answer)))
    print(f"Slots: {len(solver.slots)} | Unique words: {len(set(answer.values()))}")
    print(f"Recursive calls: {solver.calls} | Elapsed: {time.perf_counter() - start:.4f}s")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
