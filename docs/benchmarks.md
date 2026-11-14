# Benchmark notes

The following figures were recorded **locally** using both the original submitted file and the new parameterized runner with the UAB course materials on 14 November 2026. They are descriptive measurements, not performance guarantees.

| Input | Original `code.py` | Portfolio runner `run.py` | Verification |
| --- | ---: | ---: | --- |
| 7×6 small board, 107-word dictionary | ~0.0005 s printed algorithm time | ~0.001 s including input loading | 11/11 slots, 11 distinct words |
| 12×12 large board, 581,980-word dictionary | ~3.64 s printed algorithm time | ~3.46 s including input loading | 51/51 slots, 51 distinct words |

These numbers compare different code entrypoints on the same machine. They are **not** a rigorous cross-platform comparison of backtracking and forward checking.

The group's academic report also documents earlier historical runs (roughly 3,000 recursive calls for plain backtracking on the small board; 12 calls with forward checking; around 1,814 calls reported for a different large-board optimization). Those are **report-derived figures**, not reruns of the historical code; the historical variants are not archived here. In particular, the submitted script does not use the precomputed positional-set index mentioned as an experimental approach in the report.

The public CI exercises the synthetic example and unit tests only, so it remains independent of the faculty-provided datasets.
