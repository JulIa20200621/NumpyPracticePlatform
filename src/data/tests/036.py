# %% task
# `Z` is given below. Store four (or more) different ways of getting its integer part in a list `parts`, e.g. `parts = [Z // 1, ...]`.
# %% given
np.random.seed(36)
Z = np.random.uniform(0, 10, 10)
# %% solution
parts = [
    Z - Z % 1,
    Z // 1,
    np.floor(Z),
    Z.astype(int),
    np.trunc(Z),
]
for p in parts:
    print(p)
# %% wrong
parts = [np.round(Z)] * 4
# %% wrong
parts = [Z // 1, np.floor(Z)]
# %% case: `parts` has at least 4 entries
assert len(parts) >= 4, f"parts should have at least 4 entries, got {len(parts)}."
# %% case: Every entry is the integer part of Z
_bad = [i for i, p in enumerate(parts) if np.shape(p) != Z.shape or not np.allclose(p, np.trunc(Z))]
assert not _bad, f"parts[{_bad[0]}] is not the integer part of Z. Expected {np.trunc(Z)}, got {parts[_bad[0]]}." if _bad else ""
