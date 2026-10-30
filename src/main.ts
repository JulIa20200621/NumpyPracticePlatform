import "./style.css";
import { renderList } from "./pages/list";
import { runner } from "./runner";

const app = document.getElementById("app")!;
const statusEl = document.getElementById("py-status")!;
let cleanup: (() => void) | undefined;
let navId = 0;

async function route(): Promise<void> {
  const nav = ++navId;
  cleanup?.();
  cleanup = undefined;
  const m = location.hash.match(/^#\/problem\/(\d+)/);
  if (m) {
    // The problem page pulls in CodeMirror, so load it on demand.
    const { renderProblem } = await import("./pages/problem");
    if (nav !== navId) return;
    cleanup = renderProblem(app, Number(m[1]));
  } else {
    renderList(app);
  }
  window.scrollTo(0, 0);
}

runner.onStatus((s) => {
  statusEl.className = `py-status py-${s.state}`;
  statusEl.textContent =
    s.state === "loading" ? s.text : s.state === "ready" ? "Python ready" : s.state === "running" ? "Running…" : "Python failed to load";
  statusEl.title = s.state === "error" ? s.text : "";
});

window.addEventListener("hashchange", route);
route();
