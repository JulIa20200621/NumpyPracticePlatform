# %% task
# Store the sorted vector in `Z` (smallest first).
# %% wrong
Z = np.random.random(10)
# %% wrong
Z = np.sort(np.random.random(10))[::-1]
# %% wrong
Z = np.arange(10)
# %% case: `Z` has shape (10,)
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (10,), f"Z should have shape (10,), got {Z.shape}."
# %% case: Values are random
assert np.issubdtype(Z.dtype, np.floating) and not np.allclose(np.diff(Z), np.diff(Z)[0]), "Z doesn't look random. Start from `np.random.random(10)`."
# %% case: `Z` is sorted, smallest first
assert np.all(np.diff(Z) >= 0), f"Z is not sorted in increasing order: {Z}." + (" It's in decreasing order." if np.all(np.diff(Z) <= 0) else " Use `Z.sort()` or `np.sort(Z)`.")
