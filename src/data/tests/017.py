# %% task
# Predict each result, then check your guess by running the expressions. Store the six results in a list `answers`, in order.
# Use `np.nan` for nan.
# %% solution
answers = [
    0 * np.nan,
    np.nan == np.nan,
    np.inf > np.nan,
    np.nan - np.nan,
    np.nan in set([np.nan]),
    0.3 == 3 * 0.1,
]
print(answers)
# %% wrong
answers = [0, False, False, np.nan, True, False]
# %% wrong
answers = [np.nan, True, True, np.nan, True, True]
# %% case: `answers` has 6 entries
assert len(answers) == 6, f"answers should have 6 entries, one per expression, got {len(answers)}."
# %% case: Each answer is correct
_expected = [np.nan, False, False, np.nan, True, False]
_exprs = ["0 * np.nan", "np.nan == np.nan", "np.inf > np.nan", "np.nan - np.nan", "np.nan in set([np.nan])", "0.3 == 3 * 0.1"]


def _same(want, got):
    if isinstance(want, float):
        return isinstance(got, (float, np.floating)) and np.isnan(got)
    return isinstance(got, (bool, np.bool_)) and got == want


_wrong = [e for e, want, got in zip(_exprs, _expected, answers) if not _same(want, got)]
assert not _wrong, "Not quite: re-check " + ", ".join(f"`{e}`" for e in _wrong) + ". Remember nan is not equal to anything, even itself."
