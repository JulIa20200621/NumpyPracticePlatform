# NumPy Practice Platform — Project Spec

> **中文摘要：** 做一个仿 LeetCode 的 NumPy 练习网站。题目来自 rougier/numpy-100（MIT license）。全部在浏览器里运行（Pyodide），不需要服务器，部署在 GitHub Pages。每题有编辑器、运行、自动判题、提示和答案，进度存在浏览器里。界面中英对照。先做前 40 题，跑通后再补全 100 题。

This file is the brief for Claude Code. Read it fully before writing code, then work through the milestones in order.

---

## 1. Goal

A LeetCode-style web app for practicing the 100 exercises from **rougier/numpy-100**:

- Problem list → open a problem → write Python/NumPy in an editor → **Run** → see output → **Submit** → automatic ✅ / ❌ with a helpful message
- Hints and reference solutions available on demand
- Progress remembered between visits
- **No backend.** Python runs in the browser via **Pyodide** (includes NumPy)
- Hosted free on **GitHub Pages**

The user is a student in a linear algebra course (MATH 257, UIUC) who knows C++ and is learning Python/NumPy. The platform should specifically help with their weak spots (see §9).

---

## 2. Source material and license

- Source repo: https://github.com/rougier/numpy-100 — **MIT license**
- Exercises live in `source/exercises.ktx`: a key-value text format where each exercise has three keys: question (`q<N>`), hint (`h<N>`), answer (`a<N>`). Inspect the file to confirm the exact syntax before writing the parser.
- **Required:** keep the original `LICENSE` text and copyright notice in this repo (e.g. `third_party/numpy-100/LICENSE`), and credit the source in `README.md` and in the app footer.
- Don't scrape the website; download the raw `exercises.ktx` once and commit it under `third_party/numpy-100/`.

---

## 3. Tech stack

Keep it simple and dependency-light.

| Part | Choice | Notes |
|---|---|---|
| Framework | **Vite + vanilla TypeScript** (or plain JS) | No React needed unless it clearly helps. Static build output |
| Python runtime | **Pyodide** (pin an exact version) | Load NumPy with `pyodide.loadPackage("numpy")`. Run Python in a **Web Worker** so the UI doesn't freeze |
| Editor | **CodeMirror 6** with the Python language mode | Tab = 4 spaces, line numbers, bracket matching |
| Storage | `localStorage` (wrap all access in try/catch) | progress, last code per problem, settings |
| Deploy | **GitHub Pages** via GitHub Actions | Set Vite `base` to the repo name |

Pin every dependency version in `package.json`.

---

## 4. Data pipeline

1. `scripts/parse_ktx.(py|ts)` reads `third_party/numpy-100/exercises.ktx` → writes `src/data/exercises.json`:
   ```json
   {
     "id": 1,
     "question": "Import the numpy package under the name `np`",
     "hint": "import … as",
     "solution": "import numpy as np",
     "difficulty": 1,
     "tags": ["basics"]
   }
   ```
2. **Difficulty:** numpy-100 marks difficulty with stars (★☆☆ / ★★☆ / ★★★) in the question text. Parse them into `difficulty` 1–3 and strip them from the displayed question.
3. **Tags:** assign by hand or with simple keyword rules. Suggested tags: `basics`, `create`, `index-slice`, `shape`, `axis`, `broadcasting`, `dtype`, `sort-argmax`, `linear-algebra`, `random`, `misc`.
4. **Chinese translation (`question_zh`, `hint_zh`)**: optional field. Add for the first 40 exercises; show both languages in the UI when present.

---

## 5. Grading (the hard part)

Many exercises have more than one correct answer (e.g. `np.zeros(10)` vs `np.zeros(10, dtype=int)`), so **never compare the student's code text to the solution**. Instead, each exercise gets a **test** that checks the *result*.

### 5.1 Test format

Store tests in `src/data/tests/NNN.py` (or one `tests.json`). Each test is Python that runs **after** the student's code in the same namespace, and raises `AssertionError` with a clear message on failure:

```python
# Exercise 3: Create a null vector of size 10
assert 'Z' in dir(), "Define a variable named Z 定义一个叫 Z 的变量"
assert isinstance(Z, np.ndarray), "Z should be a NumPy array, not a list"
assert Z.shape == (10,), f"Z should have shape (10,), got {Z.shape}"
assert np.all(Z == 0), "All entries of Z should be 0"
```

### 5.2 Conventions

- Each exercise's prompt must say **which variable name** the answer goes in (most numpy-100 solutions use `Z`). Add this to the displayed question if the original doesn't say it.
- For exercises that only **print** something, capture stdout and compare normalized output, or rewrite the task to store the result in a variable.
- For exercises with **random** data, set `np.random.seed(...)` in a hidden prelude, or test properties (shape, dtype, range) instead of exact values.
- Compare floats with `np.allclose`, never `==`.
- Error messages are **bilingual (English + 中文)** and point at the likely mistake (wrong shape, list instead of array, wrong dtype, etc.).

### 5.3 Execution

- Hidden prelude before student code: `import numpy as np`.
- Run student code + test in a fresh namespace per Submit.
- **Timeout** (e.g. 5 s): if the worker doesn't respond, terminate and recreate it, show "Time limit exceeded".
- Show Python tracebacks to the student, trimmed to their own code's lines.
- **Run** = execute code and show stdout / the last expression's value. **Submit** = run + test.

### 5.4 Writing the tests

Generate tests for all exercises, but **verify each one against the reference solution in CI**: a script runs `solution + test` for every exercise in Python (local NumPy) and must pass. Also add at least one *wrong* answer per test in a small fixture set to make sure the test can fail.

---

## 6. UI

### Problem list page
- Table: `#`, title (first line of question), difficulty (Easy / Medium / Hard), tags, status (✅ solved / ◐ attempted / blank)
- Filters: difficulty, tag, status; search box
- Progress bar: "23 / 100 solved"

### Problem page (LeetCode-style split view)
- **Left:** question (EN + 中文 if available), tags, difficulty; buttons **Show hint** and **Show solution** (solution behind a confirm step: "Try first! 先自己试试")
- **Right:** editor; buttons **Run**, **Submit**, **Reset code**; output panel below (stdout, value, errors, test result)
- Prev / Next problem buttons
- Remember the last code typed per problem

### General
- Light and dark mode
- Works on a laptop screen; mobile can be stacked vertically
- Footer: credit to rougier/numpy-100 (MIT)
- Show a loading state while Pyodide downloads (first load takes a few seconds)

---

## 7. Repo layout

```
numpy-practice/
├─ README.md                 # what it is, how to run, credits
├─ PROJECT_SPEC.md           # this file
├─ LICENSE                   # license for this project's own code (MIT suggested)
├─ third_party/numpy-100/
│  ├─ exercises.ktx
│  └─ LICENSE                # original MIT license, unchanged
├─ scripts/
│  ├─ parse_ktx.py
│  └─ verify_tests.py        # runs solution + test for every exercise
├─ src/
│  ├─ data/exercises.json
│  ├─ data/tests/…
│  ├─ worker/pyodide-worker.ts
│  ├─ pages/…
│  └─ main.ts
├─ index.html
├─ package.json
├─ vite.config.ts
└─ .github/workflows/
   ├─ ci.yml                 # verify_tests.py + build
   └─ deploy.yml             # build + publish to GitHub Pages
```

---

## 8. Milestones

Do these in order. Stop after each one and show the user how to try it.

1. **M1 — Skeleton:** Vite project, parse `exercises.ktx` → `exercises.json`, problem list page renders all 100 questions.
2. **M2 — Run code:** Pyodide in a Web Worker, CodeMirror editor, Run button prints output. Loading indicator.
3. **M3 — Grading:** test runner + tests for **exercises 1–40**, `verify_tests.py` passes. Submit shows ✅/❌ with messages.
4. **M4 — Progress & polish:** localStorage progress, filters, hints/solutions, dark mode, bilingual text for 1–40.
5. **M5 — Deploy:** GitHub Actions → GitHub Pages. README with the live link.
6. **M6 — Remaining tests:** exercises 41–100, verified in CI.
7. **M7 (optional) — Course extras:** see §9.

---

## 9. Course-specific extras (optional, after M6)

Extra problems written in the same format, targeting the user's known weak spots from MATH 257 labs. Put them in a separate "Course" tab.

| Weak spot | Example extra problem |
|---|---|
| `np.zeros((m, n))` vs `np.zeros(m, n)` | "Create a 3×4 matrix of zeros" (test catches 1-D result) |
| `shape[0]` vs `shape[1]`, rows vs columns | "Store the number of columns of A in `c`" |
| `axis=0` vs `axis=1` | "Store the column sums of A in `s`" |
| Column normalization | "Make every column of A sum to 1 (A has no zero columns)" |
| Zero columns → `nan` | "Normalize columns; an all-zero column becomes 1/N" (PageRank) |
| `.T` and row-major typing | "Given each state's outgoing probabilities as rows, build the column-stochastic matrix" |
| `A[to, from]` from an edge list | "Build an adjacency matrix from `edges` where each row is [from, to]" |
| `@` vs `*`, vector @ vector = scalar | "Compute M @ x three times starting from a one-hot vector" |
| One-hot start, index → label | "Start 100% in state 0; return the probability of state 1 after 3 steps (a float)" |
| Power iteration | "Return the steady state of M (shape (n,), sums to 1)" |
| int array truncation | "Fix this code so 0.25 isn't stored as 0" |
| `argmax` / `argsort` with labels | "Return the names ranked by score, highest first" |

Hint messages for these should name the specific mistake (e.g. "Your result has shape (12,) — did you write `np.zeros(3, 4)` instead of `np.zeros((3, 4))`?").

---

## 10. Definition of done

- `npm run build` succeeds; `scripts/verify_tests.py` passes for all exercises
- Every reference solution passes its test; every test fails on at least one wrong answer
- Live site on GitHub Pages loads, runs NumPy, grades answers, remembers progress
- README explains: how to run locally (`npm install`, `npm run dev`), how tests work, how to add an exercise, and credits rougier/numpy-100 (MIT)

---

## 11. Git workflow

- New repository under the user's account (not a fork of numpy-100; credit it instead)
- Default branch `main`; one feature branch per milestone (`m1-skeleton`, `m2-pyodide`, …), merged when the milestone works
- Small, descriptive commits
- **Public** repo if using free GitHub Pages
