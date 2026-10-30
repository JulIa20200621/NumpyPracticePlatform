# %% task
# `Z` is given below. Store six booleans in a list `legal`, one per expression in order: `True` if it runs without error.
# %% given
Z = np.arange(1, 6)
# %% solution
legal = []
for expr in ["Z**Z", "2 << Z >> 2", "Z <- Z", "1j*Z", "Z/1/1", "Z<Z>Z"]:
    try:
        eval(expr)
        legal.append(True)
    except Exception:
        legal.append(False)
print(legal)
# %% wrong
legal = [True] * 6
# %% wrong
legal = [True, True, False, True, True, False]
# %% case: `legal` has 6 entries
assert len(legal) == 6, f"legal should have 6 entries, got {len(legal)}."
# %% case: Each entry is right
_exprs = ["Z**Z", "2 << Z >> 2", "Z <- Z", "1j*Z", "Z/1/1", "Z<Z>Z"]
_expected = [True, True, True, True, True, False]
_wrong = [e for e, want, got in zip(_exprs, _expected, legal) if bool(got) != want]
assert not _wrong, "Re-check " + ", ".join(f"`{e}`" for e in _wrong) + ". Try running each one."
