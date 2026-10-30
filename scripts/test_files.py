"""Reader for the per-exercise test files in src/data/tests/NNN.py.

A test file is split into sections by `# %% <kind>` marker lines:

    # %% task        What to store and where, shown under the question (Markdown,
                     written as `# ` comment lines)
    # %% given       Code run before the student's code and shown to them
    # %% setup       Hidden code run after `given` (e.g. remember id(A) for in-place checks)
    # %% solution    Reference solution, replacing numpy-100's answer when the task was rewritten
    # %% wrong       A wrong answer; verify_tests.py checks that it fails (repeatable)
    # %% case: name  A test case: asserts with a helpful message (repeatable, run in order)

Only `case:` is required. Test cases see the student's variables, plus `_stdout`
(everything the student's code printed).
"""

import re
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent.parent / "src" / "data" / "tests"
MARKER = re.compile(r"^# %% (task|given|setup|solution|wrong|case:\s*(.+))\s*$")


def _clean(lines: list[str]) -> str:
    return "\n".join(lines).strip("\n")


def read_test_file(path: Path) -> dict:
    spec = {"task": "", "given": "", "setup": "", "solution": None, "wrong": [], "cases": []}
    kind, name, lines = None, None, []

    def flush():
        if kind is None:
            if _clean(lines):
                raise ValueError(f"{path.name}: code before the first '# %%' marker")
            return
        body = _clean(lines)
        if kind == "task":
            spec["task"] = "\n".join(re.sub(r"^# ?", "", l) for l in body.splitlines())
        elif kind in ("given", "setup"):
            spec[kind] = body
        elif kind == "solution":
            spec["solution"] = body
        elif kind == "wrong":
            spec["wrong"].append(body)
        else:
            spec["cases"].append({"name": name, "code": body})

    for line in path.read_text(encoding="utf-8").splitlines():
        m = MARKER.match(line)
        if m:
            flush()
            kind, name, lines = ("case", m.group(2).strip(), []) if m.group(2) else (m.group(1), None, [])
        else:
            lines.append(line)
    flush()

    if not spec["cases"]:
        raise ValueError(f"{path.name}: no '# %% case:' sections")
    return spec


def load_all() -> dict[int, dict]:
    return {int(p.stem): read_test_file(p) for p in sorted(TESTS_DIR.glob("[0-9][0-9][0-9].py"))}
