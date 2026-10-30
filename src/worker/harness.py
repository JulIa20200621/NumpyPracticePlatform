"""Runs student code (and, on Submit, its test cases) in a fresh namespace.

Shared by the browser (Pyodide worker) and scripts/verify_tests.py, so grading
behaves the same in both places. Pure Python: no Pyodide-specific code here.
"""

import ast
import contextlib
import io
import json
import linecache
import time
import traceback
import tracemalloc
import warnings

import numpy as np  # also warms the import so the first Run is fast

USER_FILE = "<solution>"
TEST_FILE = "<test>"
PRELUDE = "import numpy as np"
MAX_OUTPUT = 20_000


class _LimitedIO(io.StringIO):
    """stdout buffer that stops growing past MAX_OUTPUT characters."""

    truncated = False

    def write(self, s):
        room = MAX_OUTPUT - self.tell()
        if room <= 0:
            self.truncated = True
            return len(s)
        if len(s) > room:
            self.truncated = True
            super().write(s[:room])
            return len(s)
        return super().write(s)


def _register_source(filename, source):
    # Lets tracebacks show the student's source lines.
    lines = source.splitlines(keepends=True)
    linecache.cache[filename] = (len(source), None, lines, filename)


def _format_user_error(exc):
    """Traceback with only the frames from the student's own code."""
    tbe = traceback.TracebackException.from_exception(exc)
    frames = [f for f in tbe.stack if f.filename == USER_FILE]
    if frames:
        tbe.stack = traceback.StackSummary.from_list(frames)
        text = "".join(tbe.format())
    else:  # e.g. SyntaxError: the error happened before any student line ran
        text = "".join(tbe.format_exception_only())
    return text.replace(f'File "{USER_FILE}", ', "")


def _compile_code(code):
    """Compile the code. A final expression statement is compiled separately so its
    value can be shown, like in a REPL. Returns (body, last_or_None)."""
    tree = ast.parse(code, USER_FILE, "exec")
    last = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = compile(ast.Expression(tree.body.pop().value), USER_FILE, "eval")
    return compile(tree, USER_FILE, "exec"), last


def _truncate(s):
    return s if len(s) <= MAX_OUTPUT else s[:MAX_OUTPUT] + "\n… (truncated)"


def _run_case(case_code, ns):
    """Run one test case. Returns (status, message) with status "pass" or "fail"."""
    try:
        exec(compile(case_code, TEST_FILE, "exec"), ns)
        return "pass", None
    except AssertionError as exc:
        return "fail", str(exc) or "Wrong answer."
    except NameError as exc:
        return "fail", f"{exc}. Did you store your answer in the variable the task asks for?"
    except Exception as exc:
        return "fail", f"Checking your answer raised {type(exc).__name__}: {exc}"


def execute(code, given="", setup="", cases=None, prelude=True):
    """Run student code, then (on Submit) the test cases, in one fresh namespace.

    Order: prelude (`import numpy as np`, unless prelude=False) -> `given` (shown to
    the student) -> `setup` (hidden) -> student `code` -> each case in `cases`.

    `cases` is None for Run, or a list of {"name", "code"} for Submit. Cases run in
    order and stop at the first failure (later cases are reported as "skipped").

    Returns a dict:
      stdout   captured print output (also visible to cases as `_stdout`)
      value    repr of the last expression, or None
      error    trimmed traceback if the student's code raised, else None
      time_ms  run time of the student's code
      memory   peak bytes allocated by the student's code (Python + NumPy buffers)
      passed   None (Run) / True / False
      cases    [{"name", "status": "pass"|"fail"|"skipped", "message"}] or None
    """
    ns = {"__name__": "__main__"}
    out = _LimitedIO()
    result = {"stdout": "", "value": None, "error": None, "time_ms": None, "memory": None, "passed": None, "cases": None}
    _register_source(USER_FILE, code)
    np_err = np.geterr()

    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out), warnings.catch_warnings():
        warnings.simplefilter("default")
        try:
            if prelude:
                exec(PRELUDE, ns)
            if given:
                exec(compile(given, "<given>", "exec"), ns)
            if setup:
                exec(compile(setup, "<setup>", "exec"), ns)

            try:
                body, last = _compile_code(code)
            except SyntaxError as exc:
                result["error"] = _format_user_error(exc)
            else:
                # Measure only the student's code running (not compiling it).
                value = None
                tracemalloc.start()
                start = time.perf_counter()
                try:
                    exec(body, ns)
                    if last is not None:
                        value = eval(last, ns)
                except BaseException as exc:  # SystemExit too: student code must not kill the runner
                    result["error"] = _format_user_error(exc)
                finally:
                    result["time_ms"] = (time.perf_counter() - start) * 1000
                    result["memory"] = tracemalloc.get_traced_memory()[1]
                    tracemalloc.stop()
                if value is not None:
                    result["value"] = _truncate(repr(value))

            student_stdout = out.getvalue()
            if cases is not None:
                ns["_stdout"] = student_stdout
                result["cases"] = []
                failed = result["error"] is not None
                for case in cases:
                    if failed:
                        status, message = "skipped", None
                    else:
                        status, message = _run_case(case["code"], ns)
                        failed = status != "pass"
                    result["cases"].append({"name": case["name"], "status": status, "message": message})
                result["passed"] = not failed
        finally:
            np.seterr(**np_err)  # student code may have called np.seterr

    result["stdout"] = student_stdout + ("\n… (output truncated)" if out.truncated else "")
    return result


def execute_json(code, given="", setup="", cases_json="null", prelude=True):
    return json.dumps(execute(code, given, setup, json.loads(cases_json), prelude))
