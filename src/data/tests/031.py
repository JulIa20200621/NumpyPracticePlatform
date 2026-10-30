# %% task
# Compute `Z = np.ones(1) / 0` **without** a RuntimeWarning being printed.
# Use `np.errstate`, so warnings are switched back on afterwards.
# %% solution
with np.errstate(all="ignore"):
    Z = np.ones(1) / 0

# Also possible, but remember to restore the old settings:
# defaults = np.seterr(all="ignore")
# Z = np.ones(1) / 0
# _ = np.seterr(**defaults)
# %% wrong
Z = np.ones(1) / 0
# %% wrong
np.seterr(all="ignore")
Z = np.ones(1) / 0
# %% case: `Z` is [inf]
assert np.array_equal(Z, [np.inf]), f"Z should be np.ones(1) / 0, i.e. [inf], got {Z}."
# %% case: No warning was printed
assert "Warning" not in _stdout, "A warning was printed. Wrap the division in `with np.errstate(all=\"ignore\"):`."
# %% case: Warnings are switched back on afterwards
assert np.geterr()["divide"] != "ignore", "Division warnings are still turned off for all later code. Use `with np.errstate(...)`, which only applies inside the `with` block."
