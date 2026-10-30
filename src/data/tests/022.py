# %% task
# `Z` is given below. Normalize it so its values have mean 0 and standard deviation 1, and store the result back in `Z`.
# %% given
np.random.seed(22)
Z = np.random.random((5, 5))
# %% solution
Z = (Z - np.mean(Z)) / (np.std(Z))
print(Z)
# %% wrong
Z = Z / Z.max()
# %% wrong
Z = Z - Z.mean()
# %% wrong
Z = (Z - Z.mean(axis=0)) / Z.std(axis=0)
# %% case: `Z` still has shape (5, 5)
assert np.shape(Z) == (5, 5), f"Z should still have shape (5, 5), got {np.shape(Z)}."
# %% case: The mean of Z is 0
assert np.isclose(np.mean(Z), 0), f"The mean of Z should be 0, got {np.mean(Z):.4f}. Subtract the mean."
# %% case: The standard deviation of Z is 1
assert np.isclose(np.std(Z), 1), f"The standard deviation of Z should be 1, got {np.std(Z):.4f}. Divide by the standard deviation."
# %% case: Z is the original matrix, shifted and scaled as a whole
np.random.seed(22)
_Z0 = np.random.random((5, 5))
assert np.allclose(Z, (_Z0 - _Z0.mean()) / _Z0.std()), "Use the mean and std of the whole matrix (no `axis`), not per row or column."
