# %% task
# Store the three results in a list `answers`, in order.
# %% solution
answers = [
    np.array(0) / np.array(0),
    np.array(0) // np.array(0),
    np.array([np.nan]).astype(int).astype(float),
]
print(answers)
# %% wrong
answers = [0, 0, np.nan]
# %% wrong
answers = [np.nan, np.nan, np.nan]
# %% case: `answers` has 3 entries
assert len(answers) == 3, f"answers should have 3 entries, got {len(answers)}."
# %% case: 0 / 0 is right
assert np.isnan(answers[0]), f"`np.array(0) / np.array(0)` is not {answers[0]!r}. Try running it."
# %% case: 0 // 0 is right
assert not np.isnan(answers[1]) and answers[1] == 0, f"`np.array(0) // np.array(0)` is not {answers[1]!r}. Integer division can't produce nan."
# %% case: nan -> int -> float is right
_want = np.array([np.nan]).astype(int).astype(float)
assert np.array_equal(np.ravel(answers[2]), _want), f"Casting nan to int is undefined, so you get a meaningless value: here {_want}. Store the result of the expression."
