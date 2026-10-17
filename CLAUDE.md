# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Python project that generates succession-free derangements, organized out of a disorganized, unfinished collection of scripts, notes, ideas, and output.  Everything worth keeping from that material has moved into the module, and the rest was deleted.

## Prose style

`COMMENT-STYLE.md` sets the rules for code comments, docstrings, commit messages, and documentation files, this one included.  Follow it in anything you write here.

## Commands

All the code is in one module, `succession_free_derangements.py`.  It has no runtime dependencies and needs Python 3.10 or later.  It is meant to be run or imported as a plain file, not installed as a package, so don't add packaging metadata.  `make install` only copies the module to `$(PREFIX)/lib/python/` and the wrapper to `$(PREFIX)/bin/`, with `PREFIX` defaulting to `~/.local`.  The tests need pytest, and `pyproject.toml` holds only its settings.

The Makefile also has `all` and `clean` targets that do nothing.  A parent Makefile that builds many directories runs those targets in each one, so keep them.

```sh
pytest                                         # all tests
pytest tests/test_matrices.py -k modular       # a subset
make lint                                      # ruff, mypy, and pylint
make install                                   # copy into ~/.local
python3 succession_free_derangements.py permutations 6
python3 succession_free_derangements.py matrices 8
python3 succession_free_derangements.py matrices 12 --limit 1
python3 succession_free_derangements.py matrices 16 --modular
```

`python3 -m succession_free_derangements` works the same as running the file, and so does `./succession-free-derangements`, a wrapper that imports the module and calls `main`.  The wrapper sits at the repo root because Python puts a script's own directory first on the import path, so in a checkout it imports the checkout's module rather than an installed copy.

## Two kinds of output

The module has a section for each kind, followed by the command-line interface.  The first section handles single permutations.  A succession-free derangement of `0..n-1` has no fixed point and no succession, where a succession is a value followed by the value one greater.  Descending steps such as `3 2` are allowed.

The second section handles the matrices that most of the scratch work was about.  The module docstring holds the definition.  In short, for even `n`, the matrix is symmetric, row 0 is the identity, row `n-1-k` is row `k` reversed, and no ordered pair of adjacent values appears in two rows.  The search and the validator both rely on consequences of that definition, which the docstring spells out.

- `search_matrices(n)` backtracks one row at a time over the top half.  Symmetry fixes every entry of the next row except the middle ones.  Because each row's reversal is also a row, the search tracks unordered adjacent pairs, and each pair may appear once.  Every matrix for n = 10 takes under a second, and the first one for n = 12 takes several seconds, but all 482 of them take over half an hour.
- `modular_matrix(n)` builds one matrix directly when `n+1` is prime, with entry `(k, i)` equal to `((k+1)(i+1) mod (n+1)) - 1`.  It is one of the saved n = 10 results.

## Results

`results/succession-free-derangements-{2,4,6,8,10,12}.txt` are the known solutions in numpy's integer-array print format, one matrix per block, separated by blank lines.  `format_matrix` and `parse_matrices` read and write that format, and `matrices N` prints it.  The tests check that the search reproduces every file but the one for 12 exactly, so a change to the format or to the search order will show up there.  Searching for 12 is too slow for the tests, so they only check that its file round-trips through those two functions and holds 482 valid matrices.

## scratch/

`farthest-succession-free-derangements.py` imports the module and prints the succession-free derangements with the largest `circular_distance`.  It checks every one, so n = 12 takes about two and a half minutes, and each step up in n takes about ten times as long.  Neither the module nor the tests refer to `scratch/`.

## Conventions

Python files start with SPDX headers (`MPL-2.0`, Steven Ward).  `succession_free_derangements.py` carries `__author__`, `__license__`, and a date-string `__version__`.
