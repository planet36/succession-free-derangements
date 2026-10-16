# SPDX-FileCopyrightText: Steven Ward
# SPDX-License-Identifier: MPL-2.0

# Print the succession-free derangements of 0..n-1 with the largest circular distance.  This
# checks every one of them, so n = 11 takes about 17 seconds and each step up in n takes about
# ten times as long.
#
# Usage: python3 scratch/farthest-succession-free-derangements.py [N]

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from succession_free_derangements import circular_distance, succession_free_derangements

n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
perms = list(succession_free_derangements(n))
if not perms:
    sys.exit(f'no succession-free derangement of 0..{n - 1} exists')
best = max(map(circular_distance, perms))
farthest = [p for p in perms if circular_distance(p) == best]

print(f'distance {best}')
for p in farthest:
    print(*p)
