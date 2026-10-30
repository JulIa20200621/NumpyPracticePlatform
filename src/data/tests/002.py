# %% task
# Print the version first, then the configuration.
# %% wrong
print(np.__name__)
# %% wrong
np.show_config()
# %% case: The NumPy version is printed
assert np.__version__ in _stdout, f"Your output doesn't contain the version string {np.__version__!r}. Try `print(np.__version__)`."
# %% case: The configuration is printed
assert len(_stdout.strip().splitlines()) > 3, "Only a line or two was printed. Did you call `np.show_config()`?"
