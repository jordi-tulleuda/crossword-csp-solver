# Approach and constraints

Each across/down run of at least two white cells becomes a **CSP variable**. Its domain is the subset of dictionary words of matching length. The constraints are:

1. A word must match the slot length.
2. At a crossing, the horizontal and vertical words must have the same character.
3. Each dictionary word can be used at most once.
4. Every assigned word must belong to the provided dictionary.

The solver filters domains by length, uses **Minimum Remaining Values (MRV)** to choose the next slot and performs **forward checking** only on slots that intersect the newly assigned slot. Backtracking explores other assignments when a domain becomes empty. Word uniqueness is checked during the search rather than propagated to all remaining domains.

The original coursework covered:

- **Part C:** a small crossword with a 107-word vocabulary. The report compares a historical plain-backtracking baseline to its improved version.
- **Part B:** forward checking on the same board.
- **Part A:** a 12×12 crossword with a 581,980-word vocabulary.

The repo includes the *final submitted algorithm*, not separate frozen implementations of each development milestone. For the original benchmarks and the distribution of work, see the summarized results in the README and `docs/attribution.md`.

## Limitations

- The solver aims to find **one valid completion**, not enumerate all solutions.
- Forward checking propagates shared letters to directly neighboring slots. It does not implement generalized arc consistency (AC-3) or full propagation of the all-different constraint.
- Large-input run times are machine-dependent, and the university datasets are not shipped.
- The original submission (`original/code.py`) has hard-coded dataset paths; use the CLI wrapper for new inputs.
