# %% task
# Store your answer in `answer` as `True` or `False`.
# %% solution
print(np.sqrt(-1), np.emath.sqrt(-1))
answer = False
# %% wrong
answer = True
# %% wrong
answer = "False"
# %% case: `answer` is a boolean
assert isinstance(answer, (bool, np.bool_)), f"answer should be True or False, got {answer!r}."
# %% case: `answer` is right
assert answer == False, "Print both sides: `np.sqrt(-1)` gives nan (with a warning), while `np.emath.sqrt(-1)` gives 1j."  # noqa: E712
