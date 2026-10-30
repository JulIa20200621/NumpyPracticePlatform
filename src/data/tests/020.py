# %% task
# Store the index in `idx` as a tuple `(x, y, z)`.
# %% solution
idx = np.unravel_index(99, (6, 7, 8))
print(idx)
# %% wrong
idx = np.unravel_index(100, (6, 7, 8))
# %% wrong
idx = (1, 3, 5)
# %% case: `idx` has three coordinates
assert len(idx) == 3, f"idx should have 3 coordinates (x, y, z), got {len(idx)}."
# %% case: `idx` is the index of the 100th element
_idx = tuple(int(i) for i in idx)
assert _idx != (1, 5, 4), "That's the 101st element. The 100th element has flat index 99, since counting starts at 0."
assert _idx == (1, 5, 3), f"{_idx} is not the right index. Look at `np.unravel_index`."
