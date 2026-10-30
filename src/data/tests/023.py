# %% task
# Store the dtype in `color`, with fields named `r`, `g`, `b`, `a`.
# %% wrong
color = np.dtype(np.uint32)
# %% wrong
color = np.dtype([("r", np.int8), ("g", np.int8), ("b", np.int8), ("a", np.int8)])
# %% wrong
color = [("r", np.ubyte), ("g", np.ubyte), ("b", np.ubyte), ("a", np.ubyte)]
# %% case: `color` is a NumPy dtype
assert isinstance(color, np.dtype), f"color is a {type(color).__name__}. Wrap your field list in `np.dtype(...)`."
# %% case: Fields are r, g, b, a
assert color.names == ("r", "g", "b", "a"), f"color should have fields ('r', 'g', 'b', 'a'), got {color.names}."
# %% case: Each field is an unsigned byte
_bad = [n for n in color.names if color.fields[n][0] != np.uint8]
assert not _bad, f"Fields {_bad} are not unsigned bytes. Use `np.ubyte` (or `np.uint8`), which holds 0..255."
