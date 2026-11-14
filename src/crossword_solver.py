"""Crossword constraint-satisfaction solver.

Portfolio refactoring of the team's original CRI assignment. The search follows
backtracking + forward checking with minimum remaining values (MRV).
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

@dataclass(frozen=True)
class Slot:
    id: int
    row: int
    col: int
    direction: str
    cells: tuple[tuple[int, int], ...]

    @property
    def length(self) -> int:
        return len(self.cells)

def read_board(path: str | Path) -> list[list[str]]:
    board = []
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        row = [char for char in line if char in "0#"]
        if row:
            board.append(row)
    if not board or len({len(row) for row in board}) != 1:
        raise ValueError("Board must be a nonempty rectangular grid of 0 and #")
    return board

def read_dictionary(path: str | Path) -> list[str]:
    # Original university word lists are encoded as Latin-1.
    lines = Path(path).read_text(encoding="latin-1").splitlines()
    return [word.strip().upper() for word in lines if word.strip()]

def find_slots(board: list[list[str]]) -> list[Slot]:
    slots = []
    height, width = len(board), len(board[0])
    for direction in ("across", "down"):
        for primary in range(height if direction == "across" else width):
            current: list[tuple[int, int]] = []
            extent = width if direction == "across" else height
            for secondary in range(extent + 1):
                r, c = ((primary, secondary) if direction == "across"
                        else (secondary, primary))
                if secondary < extent and board[r][c] == "0":
                    current.append((r, c))
                else:
                    if len(current) >= 2:
                        sr, sc = current[0]
                        slots.append(Slot(len(slots), sr, sc, direction, tuple(current)))
                    current = []
    return slots

class CrosswordSolver:
    def __init__(self, board: list[list[str]], words: Iterable[str]):
        if not board or len({len(row) for row in board}) != 1:
            raise ValueError("Invalid crossword board")
        self.board = [row.copy() for row in board]
        self.slots = find_slots(board)
        sizes = {slot.length for slot in self.slots}
        by_length: dict[int, list[str]] = {size: [] for size in sizes}
        seen = set()
        for raw in words:
            word = raw.strip().upper()
            if word not in seen and len(word) in by_length:
                seen.add(word)
                by_length[len(word)].append(word)
        self.domains = {slot.id: by_length[slot.length] for slot in self.slots}
        self.neighbors: dict[int, dict[int, tuple[int, int]]] = {
            slot.id: {} for slot in self.slots
        }
        lookup: dict[tuple[int, int], list[tuple[int, int]]] = {}
        for slot in self.slots:
            for pos, coords in enumerate(slot.cells):
                lookup.setdefault(coords, []).append((slot.id, pos))
        for hits in lookup.values():
            if len(hits) == 2:
                (first, a), (second, b) = hits
                self.neighbors[first][second] = (a, b)
                self.neighbors[second][first] = (b, a)
        self.calls = 0

    def solve(self) -> dict[int, str] | None:
        """Return a slot-to-word assignment, or None if no solution exists."""
        self.calls = 0
        if any(not words for words in self.domains.values()):
            return None
        return self._search({}, self.domains)

    def _search(self, assigned: dict[int, str], domains: dict[int, list[str]]):
        self.calls += 1
        if len(assigned) == len(self.slots):
            return assigned
        remaining = [slot.id for slot in self.slots if slot.id not in assigned]
        choice = min(remaining, key=lambda i: len(domains[i]))  # MRV
        used = set(assigned.values())
        for word in domains[choice]:
            if word in used:
                continue  # All-different constraint
            if any(word[pos] != assigned[other][other_pos]
                   for other, (pos, other_pos) in self.neighbors[choice].items()
                   if other in assigned):
                continue
            future = domains.copy()
            viable = True
            for neighbor, (pos, neighbor_pos) in self.neighbors[choice].items():
                if neighbor in assigned:
                    continue
                candidates = [w for w in domains[neighbor]
                              if w[neighbor_pos] == word[pos]]
                if not candidates:
                    viable = False
                    break
                future[neighbor] = candidates
            if viable:
                answer = self._search({**assigned, choice: word}, future)
                if answer is not None:
                    return answer
        return None

    def render(self, assignment: dict[int, str]) -> list[str]:
        if len(assignment) != len(self.slots):
            raise ValueError("Incomplete assignment")
        board = [row.copy() for row in self.board]
        if len(set(assignment.values())) != len(assignment):
            raise ValueError("Repeated words are not allowed")
        for slot in self.slots:
            word = assignment[slot.id]
            if len(word) != slot.length:
                raise ValueError("Word length mismatch")
            for (r, c), letter in zip(slot.cells, word):
                if board[r][c] not in ("0", letter):
                    raise ValueError("Inconsistent crossing letters")
                board[r][c] = letter
        return [" ".join(row) for row in board]
