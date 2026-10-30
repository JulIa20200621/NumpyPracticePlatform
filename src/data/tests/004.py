# %% task
# `Z` is given below. Store its memory size **in bytes** in `size`.
# %% given
Z = np.zeros((10, 10))
# %% solution
size = Z.size * Z.itemsize
print("%d bytes" % size)

# Simpler alternative
size = Z.nbytes
# %% wrong
size = Z.size
# %% wrong
size = Z.itemsize
# %% case: `size` is a number
assert isinstance(size, (int, np.integer)), f"size should be an integer number of bytes, got {type(size).__name__}."
# %% case: `size` is the number of bytes
assert size != Z.size, f"{size} is the number of elements. Each element takes Z.itemsize = {Z.itemsize} bytes."
assert size == Z.nbytes, f"Expected {Z.nbytes} bytes, got {size}."
