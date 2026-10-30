/// <reference lib="webworker" />
import harnessSource from "./harness.py?raw";
import type { RunRequest, WorkerMessage } from "./protocol";

// Pinned Pyodide release (Python 3.14, NumPy 2.4.6), loaded from the jsDelivr CDN.
const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/";

interface PyFunction {
  (...args: unknown[]): string;
}
interface Pyodide {
  loadPackage(name: string): Promise<void>;
  runPython(code: string): void;
  globals: { get(name: string): PyFunction };
}

const post = (msg: WorkerMessage) => self.postMessage(msg);

async function init(): Promise<PyFunction> {
  const { loadPyodide } = await import(/* @vite-ignore */ `${PYODIDE_URL}pyodide.mjs`);
  const pyodide: Pyodide = await loadPyodide({ indexURL: PYODIDE_URL });
  post({ type: "progress", text: "Loading NumPy…" });
  await pyodide.loadPackage("numpy");
  pyodide.runPython(harnessSource);
  return pyodide.globals.get("execute_json");
}

const ready = init().then(
  (fn) => {
    post({ type: "ready" });
    return fn;
  },
  (err) => {
    post({ type: "init-error", text: String(err) });
    throw err;
  },
);

self.onmessage = async (e: MessageEvent<RunRequest>) => {
  const { id, code, test, setup } = e.data;
  const executeJson = await ready;
  try {
    // Pass undefined, not null: Pyodide converts undefined to None but null to a JS-null object.
    const result = JSON.parse(executeJson(code, test ?? undefined, setup ?? ""));
    post({ type: "result", id, result });
  } catch (err) {
    post({ type: "result", id, result: { stdout: "", value: null, error: String(err), passed: null, message: null } });
  }
};
