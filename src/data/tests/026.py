# %% task
# The script prints two numbers. Predict them, run it to check, and store them in a list `answers`: `[first, second]`.
# %% solution
# Author: Jake VanderPlas

print(sum(range(5),-1))
from numpy import *
print(sum(range(5),-1))

answers = [9, 10]
# %% wrong
answers = [10, 10]
# %% wrong
answers = [9, 9]
# %% case: `answers` has 2 entries
assert len(answers) == 2, f"answers should have 2 entries, got {len(answers)}."
# %% case: The first number is right
assert answers[0] == 9, "Not quite: the first `sum` is Python's built-in, where the second argument is a start value."
# %% case: The second number is right
assert answers[1] == 10, "Not quite: after `from numpy import *`, `sum` is `np.sum`, where the second argument is `axis`."
