# %% task
# Store the array in `Z`, its minimum in `Zmin` and its maximum in `Zmax`.
# %% wrong
Z = np.random.random((10, 10))
Zmin, Zmax = Z.max(), Z.min()
# %% wrong
Z = np.random.random((10, 10))
Zmin, Zmax = Z.min(axis=0), Z.max(axis=0)
# %% case: `Z` is a random 10x10 array
assert isinstance(Z, np.ndarray) and Z.shape == (10, 10), f"Z should be a NumPy array with shape (10, 10), got shape {np.shape(Z)}."
assert len(np.unique(Z)) > 1, "All values are equal: that doesn't look random."
# %% case: `Zmin` is the minimum of Z
assert np.ndim(Zmin) == 0, f"Zmin should be a single number, got shape {np.shape(Zmin)}. Don't pass an axis."
assert Zmin == Z.min(), f"Zmin is {Zmin}, but the smallest value in Z is {Z.min()}."
# %% case: `Zmax` is the maximum of Z
assert np.ndim(Zmax) == 0, f"Zmax should be a single number, got shape {np.shape(Zmax)}."
assert Zmax == Z.max(), f"Zmax is {Zmax}, but the largest value in Z is {Z.max()}."
