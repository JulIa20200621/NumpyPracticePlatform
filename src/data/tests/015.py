# %% task
# Make it 10x10 and store it in `Z`.
# %% wrong
Z = np.ones((10, 10))
# %% wrong
Z = np.ones((10, 10))
Z[1:-2, 1:-2] = 0
# %% case: `Z` has shape (10, 10)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (10, 10), f"Z should have shape (10, 10), got {Z.shape}."
# %% case: The border is 1
assert np.all(Z[0] == 1) and np.all(Z[-1] == 1) and np.all(Z[:, 0] == 1) and np.all(Z[:, -1] == 1), "Every value on the border (first/last row and column) should be 1."
# %% case: The inside is 0
assert np.all(Z[1:-1, 1:-1] == 0), "Every value not on the border should be 0. `Z[1:-1, 1:-1]` selects the inside."
