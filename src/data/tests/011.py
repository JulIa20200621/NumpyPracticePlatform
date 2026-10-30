# %% task
# Store the matrix in `Z`.
# %% wrong
Z = np.ones((3, 3))
# %% wrong
Z = np.eye(3)[0]
# %% case: `Z` has shape (3, 3)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (3, 3), f"Z should have shape (3, 3), but it has shape {Z.shape}."
# %% case: `Z` is the identity
assert np.allclose(Z, np.eye(3)), f"Z should have 1 on the diagonal and 0 elsewhere, got\n{Z}"
