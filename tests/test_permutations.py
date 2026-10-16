# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: MPL-2.0

import itertools
import sys

import pytest

from succession_free_derangements import (
    circular_distance,
    has_succession,
    is_derangement,
    is_succession_free_derangement,
    succession_free_derangements,
)


def test_examples_from_notes():
    assert is_derangement((1, 2, 3, 0))
    assert has_succession((1, 2, 3, 0))
    assert not is_succession_free_derangement((1, 2, 3, 0))
    assert is_succession_free_derangement((1, 3, 0, 2))


def test_is_derangement_of_another_permutation():
    assert is_derangement((1, 0, 3, 2), (3, 2, 1, 0))
    assert not is_derangement((1, 2, 0, 3), (3, 2, 1, 0))
    assert is_derangement((0, 1, 3, 2), (3, 2, 1, 0))


def test_is_derangement_rejects_different_lengths():
    with pytest.raises(ValueError):
        is_derangement((1, 0), (0, 1, 2))


@pytest.mark.parametrize('n', range(8))
def test_generator_matches_brute_force(n):
    everything = itertools.permutations(range(n))
    expected = [p for p in everything if is_succession_free_derangement(p)]
    assert list(succession_free_derangements(n)) == expected


def test_negative_n_is_rejected():
    with pytest.raises(ValueError):
        succession_free_derangements(-1)


def test_large_n_is_not_bounded_by_recursion_limit():
    n = 2 * sys.getrecursionlimit()
    p = next(succession_free_derangements(n))
    assert sorted(p) == list(range(n))
    assert is_succession_free_derangement(p)


def test_circular_distance():
    assert circular_distance((0, 1, 2, 3, 4, 5)) == 0
    assert circular_distance((1, 2, 3, 4, 5, 0)) == 6
    assert circular_distance((5, 4, 3, 2, 1, 0)) == 10
    assert circular_distance((3, 5, 4, 0, 2, 1)) == 14
