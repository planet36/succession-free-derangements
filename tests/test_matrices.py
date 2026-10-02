# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: MPL-2.0

import functools
import pathlib

import pytest

from succession_free_derangements import (
    format_matrix,
    is_succession_free_matrix,
    main,
    modular_matrix,
    parse_matrices,
    search_matrices,
)

RESULTS = pathlib.Path(__file__).parent.parent / 'results'


def saved(n):
    return parse_matrices((RESULTS / f'succession-free-derangements-{n}.txt').read_text())


# Several tests search the same n, and the n = 10 search is the slowest step in the suite.
@functools.cache
def searched(n):
    return list(search_matrices(n))


@pytest.mark.parametrize('n', [2, 4, 6, 8, 10])
def test_search_reproduces_saved_results(n):
    assert searched(n) == saved(n)


@pytest.mark.parametrize('n', [2, 4, 6, 8, 10])
def test_search_yields_only_valid_matrices(n):
    assert all(is_succession_free_matrix(m) for m in searched(n))


# Searching for 12 is too slow for the tests, so check the saved file directly.
def test_saved_results_for_12_are_valid():
    matrices = saved(12)
    assert len(matrices) == 482
    assert all(is_succession_free_matrix(m) for m in matrices)


@pytest.mark.parametrize('n', [0, 3, 5])
def test_search_rejects_bad_n(n):
    with pytest.raises(ValueError):
        next(search_matrices(n))


def test_validator_rejects_broken_matrices():
    good = saved(6)[0]
    assert is_succession_free_matrix(good)

    swapped_rows = [good[0], good[2], good[1], good[4], good[3], good[5]]
    assert not is_succession_free_matrix(swapped_rows)

    # Swapping two columns keeps every row a permutation but breaks symmetry.
    swapped_cols = [[row[0], row[2], row[1], row[3], row[4], row[5]] for row in good]
    assert not is_succession_free_matrix(swapped_cols)

    assert not is_succession_free_matrix([row[:5] for row in good[:5]])


# Obeys every rule except the mirror rule.  Such matrices first appear at n = 8.
UNMIRRORED_8 = [
    [0, 1, 2, 3, 4, 5, 6, 7],
    [1, 6, 0, 7, 2, 4, 3, 5],
    [2, 0, 4, 6, 5, 7, 1, 3],
    [3, 7, 6, 4, 1, 0, 5, 2],
    [4, 2, 5, 1, 7, 3, 0, 6],
    [5, 4, 7, 0, 3, 6, 2, 1],
    [6, 3, 1, 5, 0, 2, 7, 4],
    [7, 5, 3, 2, 6, 1, 4, 0],
]

# Obeys every rule except that rows 1 through 4 repeat a value.
REPEATED_VALUES_6 = [
    [0, 1, 2, 3, 4, 5],
    [1, 3, 0, 5, 1, 4],
    [2, 0, 4, 2, 5, 3],
    [3, 5, 2, 4, 0, 2],
    [4, 1, 5, 0, 3, 1],
    [5, 4, 3, 2, 1, 0],
]

# Obeys every rule except that pairs repeat, such as (3, 2) in rows 1 and 3.
REPEATED_PAIR_4 = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]


@pytest.mark.parametrize('m', [
    pytest.param([], id='empty'),
    pytest.param([[0]], id='odd-size'),
    pytest.param([[5 - v for v in row] for row in saved(6)[0]], id='row-0-not-identity'),
    pytest.param(REPEATED_VALUES_6, id='row-not-permutation'),
    pytest.param(UNMIRRORED_8, id='no-mirror'),
    pytest.param(REPEATED_PAIR_4, id='repeated-pair'),
])
def test_validator_rejects_each_broken_rule(m):
    assert not is_succession_free_matrix(m)


@pytest.mark.parametrize('n', [2, 4, 6, 10, 12, 16, 18, 22, 28, 30])
def test_modular_matrix_is_valid(n):
    assert is_succession_free_matrix(modular_matrix(n))


def test_modular_matrix_matches_saved_result_for_10():
    assert modular_matrix(10) in saved(10)


@pytest.mark.parametrize('n', [8, 14, 1, 3])
def test_modular_matrix_rejects_bad_n(n):
    with pytest.raises(ValueError):
        modular_matrix(n)


@pytest.mark.parametrize('n', [2, 4, 6, 8, 10, 12])
def test_format_matches_saved_files(n):
    text = (RESULTS / f'succession-free-derangements-{n}.txt').read_text()
    assert '\n\n'.join(format_matrix(m) for m in parse_matrices(text)) == text.strip()


def test_format_pads_wide_values():
    assert format_matrix([[0, 10], [10, 0]]) == '[[ 0 10]\n [10  0]]'


def test_format_and_parse_edge_cases():
    assert format_matrix([]) == '[]'
    assert parse_matrices('') == []
    m = [[-1, 2], [3, -10]]
    assert parse_matrices(format_matrix(m)) == [m]


def test_cli_matrices_output_matches_saved_file(capsys):
    assert main(['matrices', '8']) == 0
    expected = (RESULTS / 'succession-free-derangements-8.txt').read_text()
    assert capsys.readouterr().out == expected


def test_cli_limit_and_permutations(capsys):
    main(['matrices', '10', '--limit', '1'])
    assert len(parse_matrices(capsys.readouterr().out)) == 1

    main(['permutations', '4'])
    assert capsys.readouterr().out == '1 0 3 2\n1 3 0 2\n2 0 3 1\n3 2 1 0\n'

    main(['permutations', '4', '--limit', '2'])
    assert capsys.readouterr().out == '1 0 3 2\n1 3 0 2\n'


def test_cli_reports_bad_n(capsys):
    with pytest.raises(SystemExit):
        main(['matrices', '7'])
    assert 'even' in capsys.readouterr().err


def test_cli_rejects_modular_permutations(capsys):
    with pytest.raises(SystemExit):
        main(['permutations', '4', '--modular'])
    assert 'only to "matrices"' in capsys.readouterr().err


@pytest.mark.parametrize('limit', ['-1', 'x'])
def test_cli_reports_bad_limit(capsys, limit):
    with pytest.raises(SystemExit):
        main(['permutations', '4', '--limit', limit])
    assert 'nonnegative integer' in capsys.readouterr().err
