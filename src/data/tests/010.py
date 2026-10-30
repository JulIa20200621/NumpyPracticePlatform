# %% task
# Store the indices in `nz`. Either the tuple returned by `np.nonzero` or a 1-D array of indices is accepted.
# %% wrong
nz = np.array([1, 2, 4])
# %% wrong
nz = [0, 1, 2]
# %% case: `nz` holds the indices of the non-zero elements
_nz = np.asarray(nz[0] if isinstance(nz, tuple) else nz).ravel()
assert not np.array_equal(_nz, [1, 2, 4]), "nz holds the non-zero *values*. The task asks for their *indices* (positions)."
assert np.array_equal(_nz, [0, 1, 4]), f"Expected indices [0 1 4], got {_nz}."
