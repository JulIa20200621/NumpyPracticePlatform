"""Runs student code (and optionally a test) in a fresh namespace.

Shared by the browser (Pyodide worker) and scripts/verify_tests.py, so grading
behaves the same in both places. Pure Python: no Pyodide-specific code here.
"""

import ast
import contextlib
import io
import json
import linecache
import traceback

import numpy as np  # noqa: F401  (warm the import so the first Run is fast)

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


def _run_code(code, ns):
    """exec the code; if the last statement is an expression, return its value (like a REPL)."""
    tree = ast.parse(code, USER_FILE, "exec")
    last = None
    if tree.body and isinstance(tree.body[-1], ast.Expr):
        last = ast.Expression(tree.body.pop().value)
    exec(compile(tree, USER_FILE, "exec"), ns)
    if last is not None:
        return eval(compile(last, USER_FILE, "eval"), ns)
    return None


def _truncate(s):
    return s if len(s) <= MAX_OUTPUT else s[:MAX_OUTPUT] + "\n… (truncated)"


def execute(code, test=None, setup=""):
    """Run `setup` + student `code`, then `test` (if given) in the same namespace.

    Returns a dict:
      stdout   captured print output
      value    repr of the last expression, or None
      error    trimmed traceback if the student's code raised, else None
      passed   None (no test) / True / False
      message  failure message from the test
    """
    ns = {"__name__": "__main__"}
    out = _LimitedIO()
    result = {"stdout": "", "value": None, "error": None, "passed": None, "message": None}
    _register_source(USER_FILE, code)

    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
        exec(PRELUDE, ns)
        if setup:
            exec(compile(setup, "<setup>", "exec"), ns)
        try:
            value = _run_code(code, ns)
            if value is not None:
                result["value"] = _truncate(repr(value))
        except BaseException as exc:  # SystemExit too: student code must not kill the runner
            result["error"] = _format_user_error(exc)

        student_stdout = out.getvalue()
        if test is not None:
            if result["error"] is not None:
                result["passed"] = False
                result["message"] = "Your code raised an error (see above)."
            else:
                ns["_stdout"] = student_stdout
                try:
                    exec(compile(test, TEST_FILE, "exec"), ns)
                    result["passed"] = True
                except AssertionError as exc:
                    result["passed"] = False
                    result["message"] = str(exc) or "Wrong answer."
                except Exception as exc:
                    result["passed"] = False
                    result["message"] = f"Checking your answer failed with {type(exc).__name__}: {exc}"

    result["stdout"] = student_stdout + ("\n… (output truncated)" if out.truncated else "")
    return result


def execute_json(code, test=None, setup=""):
    return json.dumps(execute(code, test, setup))
