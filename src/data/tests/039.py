# %% task
# The values should be evenly spaced: 1/11, 2/11, ..., 10/11. Store the vector in `Z`.
# %% wrong
Z = np.linspace(0, 1, 10)
# %% wrong
Z = np.linspace(0, 1, 10, endpoint=False)
# %% case: `Z` has shape (10,)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (10,), f"Z should have shape (10,), got {Z.shape}."
# %% case: 0 and 1 are excluded
assert np.all((Z > 0) & (Z < 1)), f"Every value should be strictly between 0 and 1. Z goes from {Z[0]} to {Z[-1]}."
# %% case: Values are evenly spaced 1/11 .. 10/11
assert np.allclose(Z, np.arange(1, 11) / 11), f"Expected 1/11, 2/11, ..., 10/11, got {Z}. One way: take 12 evenly spaced points from 0 to 1 and drop both ends."
