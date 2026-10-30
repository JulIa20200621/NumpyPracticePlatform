# %% task
# The generator function `generate` is given below. Use it to build an array and store it in `Z`.
# %% given
def generate():
    for x in range(10):
        yield x
# %% solution
Z = np.fromiter(generate(),dtype=float,count=-1)
print(Z)
# %% wrong
Z = np.array(generate())
# %% wrong
Z = np.arange(9)
# %% case: `Z` is a 1-D array of 10 values
assert isinstance(Z, np.ndarray), f"Z is a {type(Z).__name__}, not a NumPy array."
assert Z.shape == (10,), f"Z should have shape (10,), got {Z.shape}." + (" `np.array(generator)` doesn't iterate the generator: it wraps it in a 0-d object array. Try `np.fromiter`." if Z.shape == () else "")
# %% case: `Z` holds the generated values 0..9
assert np.array_equal(Z, np.arange(10)), f"Z should hold 0, 1, ..., 9, got {Z}."
