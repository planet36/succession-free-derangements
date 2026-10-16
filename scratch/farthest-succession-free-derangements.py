# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: MPL-2.0

# pylint: disable=invalid-name

"""Print the succession-free derangements of 0..n-1 with the largest circular distance.

This checks every one of them, so n = 11 takes about 12 seconds and each step up in n takes
about ten times as long.

Usage: python3 scratch/farthest-succession-free-derangements.py [N]
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

# pylint: disable-next=wrong-import-position
from succession_free_derangements import circular_distance, succession_free_derangements

n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
best, farthest = -1, []
for p in succession_free_derangements(n):
    d = circular_distance(p)
    if d > best:
        best, farthest = d, [p]
    elif d == best:
        farthest.append(p)
if not farthest:
    sys.exit(f'no succession-free derangement of 0..{n - 1} exists')

print(f'distance {best}')
for p in farthest:
    print(*p)
