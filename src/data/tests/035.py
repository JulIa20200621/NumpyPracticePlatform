# %% task
# `A` and `B` are given below. Compute `((A+B)*(-A/2))` and store the result in `A` itself, without creating new arrays
# (use the `out=` argument of `np.add`, `np.divide`, ...).
# %% given
A = np.ones(3)*1
B = np.ones(3)*2
# %% setup
_A_id = id(A)
# %% solution
np.add(A,B,out=B)
np.divide(A,2,out=A)
np.negative(A,out=A)
np.multiply(A,B,out=A)
# %% wrong
A = (A + B) * (-A / 2)
# %% wrong
np.add(A, B, out=B)
np.multiply(A, B, out=A)
# %% case: `A` holds ((A+B)*(-A/2))
assert np.allclose(A, -1.5), f"A should be [-1.5 -1.5 -1.5], got {A}."
# %% case: `A` was modified in place
assert id(A) == _A_id, "A is a new array. Write the result into the original with `np.multiply(..., out=A)`."
