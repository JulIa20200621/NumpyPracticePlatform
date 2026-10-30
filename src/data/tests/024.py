# %% task
# `A` (5x3) and `B` (3x2) are given below. Store their matrix product in `Z`.
# %% given
A = np.arange(15).reshape(5, 3)
B = np.arange(6).reshape(3, 2)
# %% solution
Z = np.matmul(A, B)
print(Z)

# Alternative solution, in Python 3.5 and above
Z = A @ B
print(Z)
# %% wrong
Z = B.T @ A.T
# %% wrong
Z = A[:, :2] * B[:2, :2].sum()
# %% case: `Z` has shape (5, 2)
assert np.shape(Z) == (5, 2), f"Z should have shape (5, 2), got {np.shape(Z)}." + (" That's (A @ B).T: check the order of the factors." if np.shape(Z) == (2, 5) else "")
# %% case: `Z` is the matrix product A @ B
assert np.array_equal(Z, A @ B), f"Z is not the matrix product. `*` multiplies element by element; use `@` or `np.matmul`. Expected\n{A @ B}\ngot\n{Z}"
