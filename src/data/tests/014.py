# %% task
# Store the vector in `Z` and its mean in `m`.
# %% wrong
Z = np.random.random(30)
m = Z.sum()
# %% wrong
Z = np.random.random((30, 30))
m = Z.mean()
# %% case: `Z` is a random vector of size 30
assert isinstance(Z, np.ndarray) and Z.shape == (30,), f"Z should be a NumPy array with shape (30,), got shape {np.shape(Z)}."
assert len(np.unique(Z)) > 1, "All values are equal: that doesn't look random."
# %% case: `m` is the mean of Z
assert np.ndim(m) == 0, f"m should be a single number, got shape {np.shape(m)}."
assert np.isclose(m, Z.mean()), f"m is {m}, but the mean of Z is {Z.mean()}." + (" That's the sum." if np.isclose(m, Z.sum()) else "")
