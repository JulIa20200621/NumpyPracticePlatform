# %% task
# The original asks for a shell command. Here, **print** the documentation of `np.add` from Python instead.
# %% solution
np.info(np.add)
# %% wrong
print(np.add)
# %% case: The documentation of np.add is printed
assert "element-wise" in _stdout and "add" in _stdout, "Your output doesn't look like np.add's documentation. Try `np.info(np.add)` or `help(np.add)`."
