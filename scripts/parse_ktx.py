"""Parse third_party/numpy-100/exercises.ktx into src/data/exercises.json.

Merges in the per-exercise test files from src/data/tests/ (task text, given code,
test cases, rewritten solutions). Wrong answers stay out of the JSON: they are only
for scripts/verify_tests.py.

Usage: python scripts/parse_ktx.py
"""

import json
import re
import sys
from pathlib import Path

from exercise_meta import DIFFICULTY_OVERRIDES, NO_PRELUDE, TAGS
from test_files import load_all

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "third_party" / "numpy-100" / "exercises.ktx"
OUT = ROOT / "src" / "data" / "exercises.json"

STARS = re.compile(r"\s*\(([★☆]{3})\)")


def read_ktx(path: Path) -> dict[str, str]:
    """Same format as numpy-100's generators.py: a line starting with '<' opens a new key."""
    entries: dict[str, str] = {}
    key = None
    for line in path.read_text(encoding="utf-8").splitlines(keepends=True):
        if line.startswith("<"):
            key = line[1:].strip()
            entries[key] = ""
        elif key is not None:
            entries[key] += line
    return {k: v.strip() for k, v in entries.items()}


def parse_question(n: int, text: str) -> tuple[str, int]:
    m = STARS.search(text)
    if m:
        difficulty = m.group(1).count("★")
        text = (text[: m.start()] + text[m.end() :]).strip()
    elif n in DIFFICULTY_OVERRIDES:
        difficulty = DIFFICULTY_OVERRIDES[n]
    else:
        sys.exit(f"q{n}: no star rating and no entry in DIFFICULTY_OVERRIDES")
    return text, difficulty


def main() -> None:
    entries = read_ktx(SRC)
    tests = load_all()
    exercises = []
    for n in range(1, 101):
        question, difficulty = parse_question(n, entries[f"q{n}"])
        hint = re.sub(r"^hint:\s*", "", entries[f"h{n}"])
        test = tests.get(n, {})
        exercises.append(
            {
                "id": n,
                "title": question.splitlines()[0].rstrip(":"),
                "question": question,
                "hint": hint,
                "solution": test.get("solution") or entries[f"a{n}"],
                "difficulty": difficulty,
                "tags": TAGS[n],
                "prelude": n not in NO_PRELUDE,
                "task": test.get("task", ""),
                "given": test.get("given", ""),
                "setup": test.get("setup", ""),
                "cases": test.get("cases", []),
            }
        )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(exercises, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Wrote {len(exercises)} exercises to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
