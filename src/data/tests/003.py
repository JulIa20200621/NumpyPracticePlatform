# %% task
# Store the vector in `Z`.
# %% wrong
Z = [0] * 10
# %% wrong
Z = np.zeros(9)
# %% wrong
Z = np.ones(10)
# %% case: `Z` is a NumPy array
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array. Use `np.zeros`."
# %% case: `Z` has shape (10,)
assert Z.shape == (10,), f"Z should have shape (10,), but it has shape {Z.shape}."
# %% case: Every value is 0
assert np.all(Z == 0), "Z should contain only zeros."
