# %% task
# Store the matrix in `Z`.
# %% wrong
Z = np.diag(1 + np.arange(4), k=1)
# %% wrong
Z = np.diag(np.arange(4), k=-1)
# %% case: `Z` has shape (5, 5)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (5, 5), f"Z should have shape (5, 5), got {Z.shape}."
# %% case: 1, 2, 3, 4 are just below the diagonal, everything else is 0
_expected = np.diag(1 + np.arange(4), k=-1)
assert not np.array_equal(Z, _expected.T), "Your values are just *above* the diagonal. `np.diag(v, k)` puts them below when k is negative."
assert np.array_equal(Z, _expected), f"Expected\n{_expected}\ngot\n{Z}"
