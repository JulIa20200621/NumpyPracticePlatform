# %% task
# Store the matrix in `Z`.
# %% wrong
Z = np.arange(9)
# %% wrong
Z = np.arange(1, 10).reshape(3, 3)
# %% case: `Z` is a NumPy array
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
# %% case: `Z` has shape (3, 3)
assert Z.shape == (3, 3), f"Z should have shape (3, 3), but it has shape {Z.shape}." + (" Use `.reshape(3, 3)`." if Z.shape == (9,) else "")
# %% case: Values go 0..8 row by row
assert np.array_equal(Z, np.arange(9).reshape(3, 3)), f"Z should be [[0 1 2] [3 4 5] [6 7 8]], got\n{Z}"
