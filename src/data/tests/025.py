# %% task
# `Z` is given below. Negate the elements strictly between 3 and 8 **in place**: modify `Z` itself, don't create a new array.
# %% given
Z = np.arange(11)
# %% setup
_Z_id = id(Z)
# %% solution
# Author: Evgeni Burovski

Z[(3 < Z) & (Z < 8)] *= -1
print(Z)
# %% wrong
Z[(3 <= Z) & (Z <= 8)] *= -1
# %% wrong
Z = np.where((3 < Z) & (Z < 8), -Z, Z)
# %% case: Elements strictly between 3 and 8 are negated
_expected = np.array([0, 1, 2, 3, -4, -5, -6, -7, 8, 9, 10])
assert np.array_equal(Z, _expected), f"Expected {_expected}, got {Z}." + (" 'Strictly between' excludes 3 and 8 themselves." if np.array_equal(np.abs(Z), np.arange(11)) and Z[3] == -3 else "")
# %% case: `Z` was modified in place
assert id(Z) == _Z_id, "Z is a new array. Modify the original with boolean indexing, e.g. `Z[mask] *= -1`."
