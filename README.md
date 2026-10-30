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

## Credits

Exercises, hints and reference solutions are from
[rougier/numpy-100](https://github.com/rougier/numpy-100) by Nicolas P. Rougier, used under
the MIT License. The original license is kept in
[`third_party/numpy-100/LICENSE`](third_party/numpy-100/LICENSE).
