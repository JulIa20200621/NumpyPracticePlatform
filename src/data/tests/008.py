# %% task
# `Z` is given below. Reverse it and store the result back in `Z`.
# %% given
Z = np.arange(50)
# %% wrong
Z = Z
# %% wrong
Z = Z[::-1][1:]
# %% case: `Z` still has 50 elements
assert np.shape(Z) == (50,), f"Z should still have shape (50,), but it has shape {np.shape(Z)}."
# %% case: `Z` is reversed
assert np.array_equal(Z, np.arange(49, -1, -1)), f"Z should go 49, 48, ..., 0. It starts with {np.asarray(Z)[:3]}. Try slicing with a step of -1."
