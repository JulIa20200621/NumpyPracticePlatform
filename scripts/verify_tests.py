"""Check every test in src/data/tests/ against its reference solution and wrong answers.

For each exercise with a test file:
  - the reference solution must pass every case
  - every `# %% wrong` answer must fail
Runs with local NumPy through the same harness the browser uses.

Usage: python scripts/verify_tests.py [-v] [exercise ids...]
  -v  also print the message each wrong answer gets
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src" / "worker"))

from exercise_meta import NO_PRELUDE  # noqa: E402
from harness import execute  # noqa: E402
from test_files import load_all  # noqa: E402

KTX_EXERCISES = ROOT / "src" / "data" / "exercises.json"


def describe(result: dict) -> str:
    if result["error"]:
        return "raised:\n" + result["error"]
    failed = [c for c in result["cases"] if c["status"] == "fail"]
    return "; ".join(f"[{c['name']}] {c['message']}" for c in failed)


def main() -> int:
    original = {e["id"]: e["solution"] for e in json.loads(KTX_EXERCISES.read_text(encoding="utf-8"))}
    tests = load_all()
    args = sys.argv[1:]
    verbose = "-v" in args
    only = {int(a) for a in args if a != "-v"}
    problems = []

    for n, spec in tests.items():
        if only and n not in only:
            continue
        run = lambda code: execute(code, spec["given"], spec["setup"], spec["cases"], n not in NO_PRELUDE)  # noqa: E731
        solution = spec["solution"] or original[n]
        res = run(solution)
        if not res["passed"]:
            problems.append(f"{n:03}: reference solution FAILS: {describe(res)}")
        if not spec["wrong"]:
            problems.append(f"{n:03}: no '# %% wrong' answers")
        for i, wrong in enumerate(spec["wrong"], 1):
            res = run(wrong)
            if verbose:
                print(f"{n:03} wrong #{i}: {describe(res)}")
            if res["passed"]:
                problems.append(f"{n:03}: wrong answer #{i} PASSES:\n{wrong}")
            elif res["error"]:
                # Fine, but the student only sees a traceback: worth knowing when writing tests.
                print(f"note {n:03}: wrong answer #{i} raises instead of failing a case")

    checked = len(only & tests.keys()) if only else len(tests)
    for p in problems:
        print("FAIL", p)
    print(f"{checked} exercises checked, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
