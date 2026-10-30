# %% task
# `Z1` and `Z2` are given below. Store their common values in `C`, each value once, sorted.
# %% given
np.random.seed(30)
Z1 = np.random.randint(0, 10, 10)
Z2 = np.random.randint(0, 10, 10)
# %% solution
C = np.intersect1d(Z1, Z2)
print(C)
# %% wrong
C = Z1[np.isin(Z1, Z2)]
# %% wrong
C = np.union1d(Z1, Z2)
# %% case: `C` contains each value once, sorted
_C = np.asarray(C)
assert len(np.unique(_C)) == len(_C), f"C contains duplicates: {_C}. Each common value should appear once."
assert np.array_equal(_C, np.sort(_C)), f"C should be sorted, got {_C}."
# %% case: `C` contains exactly the common values
_expected = np.intersect1d(Z1, Z2)
_extra = np.setdiff1d(_C, _expected)
assert len(_extra) == 0, f"These values are not in both arrays: {_extra}."
assert np.array_equal(_C, _expected), f"Some common values are missing: {np.setdiff1d(_expected, _C)}."
