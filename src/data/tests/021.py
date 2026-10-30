# %% task
# Store it in `Z`, using 0 and 1, with `Z[0, 0] == 0`. Build it with `np.tile`.
# %% wrong
Z = np.tile(np.array([[1, 0], [0, 1]]), (4, 4))
# %% wrong
Z = np.tile(np.array([[0, 1], [1, 0]]), (8, 8))
# %% case: `Z` has shape (8, 8)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (8, 8), f"Z should have shape (8, 8), got {Z.shape}." + (" `np.tile` repeats the 2x2 block, so you only need 4 copies in each direction." if Z.shape == (16, 16) else "")
# %% case: Top-left corner is 0
assert Z[0, 0] == 0, "Z[0, 0] should be 0."
# %% case: Neighbours always differ (checkerboard)
_expected = np.indices((8, 8)).sum(axis=0) % 2
assert np.array_equal(Z, _expected), f"Every value should differ from its left/right/up/down neighbours, got\n{Z}"
