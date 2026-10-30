# %% task
# `Z` is given below. Add a border of zeros **around** it (the result is 7x7) and store the result back in `Z`.
# %% given
Z = np.ones((5, 5))
# %% solution
Z = np.pad(Z, pad_width=1, mode='constant', constant_values=0)
print(Z)
# %% wrong
Z[:, [0, -1]] = 0
Z[[0, -1], :] = 0
# %% wrong
Z = np.pad(Z, pad_width=2)
# %% case: `Z` has shape (7, 7)
assert np.shape(Z) == (7, 7), f"Z should have shape (7, 7), but it has shape {np.shape(Z)}." + (" The border goes around the array, not on top of it. Look at `np.pad`." if np.shape(Z) == (5, 5) else "")
# %% case: The border is 0 and the inside is the original array
_expected = np.zeros((7, 7))
_expected[1:-1, 1:-1] = 1
assert np.array_equal(Z, _expected), f"Expected a 5x5 block of ones surrounded by zeros, got\n{Z}"
