# %% task
# `Z` is given below. Round every value away from zero (2.1 → 3, -2.1 → -3) and store the result in `R`.
# %% given
np.random.seed(29)
Z = np.random.uniform(-10, +10, 10)
# %% solution
# Author: Charles R Harris

R = np.copysign(np.ceil(np.abs(Z)), Z)
print(R)

# More readable but less efficient
R = np.where(Z > 0, np.ceil(Z), np.floor(Z))
print(R)
# %% wrong
R = np.round(Z)
# %% wrong
R = np.ceil(Z)
# %% case: `R` has the same shape as Z
assert np.shape(R) == Z.shape, f"R should have shape {Z.shape}, got {np.shape(R)}."
# %% case: Positive values are rounded up
_pos = Z > 0
assert np.array_equal(np.asarray(R)[_pos], np.ceil(Z[_pos])), "Positive values should be rounded up (towards +inf), like `np.ceil`."
# %% case: Negative values are rounded down
_neg = Z < 0
assert np.array_equal(np.asarray(R)[_neg], np.floor(Z[_neg])), "Negative values should be rounded down (towards -inf), like `np.floor`."
