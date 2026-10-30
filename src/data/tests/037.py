# %% task
# Every row should be `[0, 1, 2, 3, 4]`. Store the matrix in `Z`.
# %% wrong
Z = np.tile(np.arange(5), (5, 1)).T
# %% wrong
Z = np.arange(25).reshape(5, 5)
# %% case: `Z` has shape (5, 5)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (5, 5), f"Z should have shape (5, 5), got {Z.shape}."
# %% case: Every row is 0, 1, 2, 3, 4
_expected = np.tile(np.arange(5), (5, 1))
assert not np.array_equal(Z, _expected.T), "Your *columns* are 0..4. Each *row* should be [0 1 2 3 4]."
assert np.array_equal(Z, _expected), f"Every row should be [0 1 2 3 4], got\n{Z}"
