# %% task
# Store the array in `Z` (random values in [0, 1)).
# %% wrong
Z = np.zeros((3, 3, 3))
# %% wrong
Z = np.random.random((3, 3))
# %% case: `Z` has shape (3, 3, 3)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (3, 3, 3), f"Z should have shape (3, 3, 3), but it has shape {Z.shape}. Pass the shape as a tuple: `np.random.random((3, 3, 3))`."
# %% case: Values are random floats in [0, 1)
assert np.issubdtype(Z.dtype, np.floating), f"Z should hold floats, got dtype {Z.dtype}."
assert np.all((Z >= 0) & (Z < 1)), "Values should be in [0, 1)."
assert len(np.unique(Z)) > 1, "All values are equal: that doesn't look random."
