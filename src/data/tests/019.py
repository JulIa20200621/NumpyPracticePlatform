# %% task
# Store it in `Z`, using 0 and 1, with `Z[0, 0] == 0`.
# %% wrong
Z = np.zeros((8, 8), dtype=int)
Z[::2, ::2] = 1
# %% wrong
Z = np.zeros((8, 8), dtype=int)
Z[1::2, ::2] = 1
Z[::2, 1::2] = 1
Z = 1 - Z
# %% case: `Z` has shape (8, 8)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (8, 8), f"Z should have shape (8, 8), got {Z.shape}."
# %% case: Top-left corner is 0
assert Z[0, 0] == 0, "Z[0, 0] should be 0."
# %% case: Neighbours always differ (checkerboard)
_expected = np.indices((8, 8)).sum(axis=0) % 2
assert np.array_equal(Z, _expected), f"Every value should differ from its left/right/up/down neighbours, got\n{Z}"
