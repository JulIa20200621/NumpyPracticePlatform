# %% task
# Store the vector in `Z`.
# %% wrong
Z = np.zeros(10)
Z[5] = 1
# %% wrong
Z = np.zeros(10)
# %% case: `Z` is a NumPy array of shape (10,)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (10,), f"Z should have shape (10,), but it has shape {Z.shape}."
# %% case: The fifth value is 1
assert Z[4] == 1, ("Z[4] should be 1. Indexing starts at 0, so the fifth value is Z[4]."
                   + (" You set Z[5] (the sixth value)." if Z[5] == 1 else ""))
# %% case: All other values are 0
assert np.count_nonzero(Z) == 1, f"Only the fifth value should be non-zero, but Z has {np.count_nonzero(Z)} non-zero values."
