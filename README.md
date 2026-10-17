# Succession-free derangements

A derangement of `0 1 2 3` moves every value away from its original position.  `1 2 3 0` is a derangement, but it keeps the runs `1 2` and `2 3` from the original.  A succession-free derangement keeps no such run, so no value is ever followed by the value one greater.  `1 3 0 2` is one.

This project generates succession-free derangements, and it also generates square matrices built from them.  For an even `n`, each matrix has `n` rows that are permutations of `0..n-1`:

```
[[0 1 2 3 4 5]
 [1 3 0 5 2 4]
 [2 0 4 1 5 3]
 [3 5 1 4 0 2]
 [4 2 5 0 3 1]
 [5 4 3 2 1 0]]
```

The first row is the identity, the last is its reverse, and each row mirrors the row the same distance from the other end.  The matrix is symmetric, so any two rows are derangements of each other.  No two rows share an adjacent pair of values in the same order.  Each matrix is therefore a row-complete Latin square: every value appears once in each row and each column, and every ordered pair of distinct values sits side by side in exactly one row.  The docstring at the top of `succession_free_derangements.py` gives the full definition and what follows from it.

## Running it

It needs Python 3.10 or later and nothing else.  Run the file directly, or run `./succession-free-derangements`, which takes the same arguments:

```sh
python3 succession_free_derangements.py permutations 4
python3 succession_free_derangements.py matrices 8
python3 succession_free_derangements.py matrices 12 --limit 1
python3 succession_free_derangements.py matrices 16 --modular
```

`permutations N` prints every succession-free derangement of `0..N-1`, one per line.  `matrices N` searches for every matrix of order `N`, which must be even, and prints them separated by blank lines.  The search lists every matrix for 10 in under a second, but all 482 matrices for 12 take over half an hour, so `--limit` stops after that many.

`--modular` skips the search and builds a single matrix directly, with entry `(k, i)` equal to `((k+1)(i+1) mod (N+1)) - 1`.  That works whenever `N+1` is prime, so it reaches sizes the search cannot.

`make install` copies the module to `~/.local/lib/python/` and the wrapper to `~/.local/bin/`, and `make uninstall` removes them.  Set `PREFIX` to install somewhere other than `~/.local`.  The installed wrapper finds the module only if that `lib/python/` directory is on `PYTHONPATH`.

To use it from Python, import it from the repo root, or copy the file anywhere on the import path:

```python
from succession_free_derangements import modular_matrix, search_matrices

first = next(search_matrices(8))
```

## Running the tests

The tests use pytest, which is the only thing to install.  Run it from the repo root:

```sh
pytest                                    # all tests
pytest tests/test_matrices.py             # one file
pytest tests/test_matrices.py -k modular  # tests whose names match
```

`pyproject.toml` holds only the pytest settings, which put the repo root on the import path.

## What's here

- `succession_free_derangements.py` holds all the code: single permutations, the matrix search and construction, and the command-line interface.
- `succession-free-derangements` is a short script that imports the module and runs its command-line interface.
- `Makefile` installs the module and the wrapper, and lints them.
- `tests/` checks the generators against brute force and against the saved results.
- `results/` holds the known matrices for every even order from 2 to 12 in the format that `matrices` prints.  The search reproduces the files for 2 through 10 exactly.
- `scratch/` holds a script that prints the succession-free derangements with the largest circular distance.
- `COMMENT-STYLE.md` sets the rules for comments, docstrings, commit messages, and documentation.

## License

MPL-2.0, as stated in each source file's SPDX header.
