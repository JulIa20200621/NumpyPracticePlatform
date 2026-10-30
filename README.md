# NumPy Practice

A LeetCode-style site for practicing the 100 NumPy exercises from
[rougier/numpy-100](https://github.com/rougier/numpy-100). Python runs entirely in the
browser via [Pyodide](https://pyodide.org); there is no backend.

## Run locally

```sh
npm install
npm run dev
```

Regenerate `src/data/exercises.json` after editing `scripts/exercise_meta.py`:

```sh
npm run data
```

## How grading works

**Run** executes your code and shows what it prints and the value of the last line.
**Submit** also runs the problem's test cases, which check the *result* (variables you
stored), never the text of your code.

Each graded exercise has a test file `src/data/tests/NNN.py`, split into sections:

```python
# %% task
# Store the vector in `Z`.            <- shown under the question
# %% given
Z = np.arange(50)                     # run before the student's code, shown to them
# %% setup
_Z_id = id(Z)                         # hidden, run after `given`
# %% solution
Z = Z[::-1]                           # reference solution (optional: replaces numpy-100's answer)
# %% wrong
Z = Z[1:]                             # a wrong answer that must fail (at least one)
# %% case: `Z` is reversed
assert np.array_equal(Z, np.arange(49, -1, -1)), "Helpful message shown to the student"
```

Test cases run in order and stop at the first failure. They can read `_stdout`
(everything the student's code printed). The same Python harness
(`src/worker/harness.py`) runs in the browser and locally.

### Adding or changing a test

```sh
# write src/data/tests/NNN.py, then:
python scripts/verify_tests.py -v NNN   # solution must pass, every wrong answer must fail
npm run data                            # rebuild src/data/exercises.json
```

CI runs `verify_tests.py` for every exercise with the same NumPy version as the site (2.4.6).

## Credits

Exercises, hints and reference solutions are from
[rougier/numpy-100](https://github.com/rougier/numpy-100) by Nicolas P. Rougier, used under
the MIT License. The original license is kept in
[`third_party/numpy-100/LICENSE`](third_party/numpy-100/LICENSE).
