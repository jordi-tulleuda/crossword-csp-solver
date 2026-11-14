# Authorship and scope

This is a group assignment developed for **Knowledge, Reasoning and Uncertainty (CRI)** at the Universitat Autònoma de Barcelona (academic year 2026–2027).

**Original implementation:** the three-person student team developed the solver from scratch. The course supplied the crossword boards and word-list files used to evaluate it; those materials are not redistributed in this portfolio copy. The original submitted implementation is preserved in [`original/code.py`](../original/code.py), and the submitted helper for creating reduced datasets is in [`original/reduir_txts.py`](../original/reduir_txts.py).

**Jordi's documented contributions:** collaborative development of backtracking and forward checking (especially Parts C and B); testing; a simplification in the inner loop of forward checking that replaces repeated full constraint checks with a direct crossing-letter comparison; and drafting the problem formulation and proposed-solution sections of the group report. The team developed and debugged much of the work together, so the repository does not claim sole authorship.

**Portfolio-only work:** `src/crossword_solver.py`, `run.py`, `examples/`, and `tests/` are a cleaned, parameterized presentation of the submitted algorithm, with a new self-contained example and independent checks. They are not presented as the original university submission.

**Important distinction:** the submitted file combines backtracking, forward checking and MRV. The original group's report discusses earlier versions and their performance, but those historical implementations are not all present in this repository. The submitted source uses lists of candidate words rather than the precomputed positional-set index discussed as an optimization in the report.

No license is attached to university-provided course data; please obtain it through the original course materials if you are authorized to use it. Publication of team-authored code should be agreed with the other contributors.
