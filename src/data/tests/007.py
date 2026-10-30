# %% task
# Store the vector in `Z` (10 and 49 both included).
# %% wrong
Z = np.arange(10, 49)
# %% wrong
Z = list(range(10, 50))
# %% case: `Z` is a NumPy array
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array. Use `np.arange`."
# %% case: `Z` starts at 10
assert Z.ndim == 1 and len(Z) > 0 and Z[0] == 10, f"Z should start at 10, got {Z[:1]}."
# %% case: `Z` ends at 49
assert Z[-1] == 49, f"Z should end at 49, but its last value is {Z[-1]}." + (" `np.arange(start, stop)` excludes stop." if Z[-1] == 48 else "")
# %% case: `Z` has 40 consecutive values
assert np.array_equal(Z, np.arange(10, 50)), "Z should be 10, 11, 12, ..., 49."
