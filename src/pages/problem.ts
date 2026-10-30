import type { EditorView } from "@codemirror/view";
import { DIFFICULTY_LABEL, exercises, getExercise } from "../data";
import { createEditor } from "../editor";
import { renderMarkdown } from "../markdown";
import { renderOutcome } from "../output";
import { runner } from "../runner";

function starterCode(prelude: boolean): string {
  return prelude ? "# numpy is already imported as np\n\n" : "";
}

export function renderProblem(root: HTMLElement, id: number): () => void {
  const ex = getExercise(id);
  if (!ex) {
    root.innerHTML = `<p class="notice">Problem ${id} not found. <a href="#/">Back to the list</a></p>`;
    return () => {};
  }
  const prev = exercises.find((e) => e.id === id - 1);
  const next = exercises.find((e) => e.id === id + 1);

  root.innerHTML = `
    <section class="problem-page">
      <div class="pane pane-left">
        <nav class="problem-nav">
          <a href="#/">&larr; All problems</a>
          <span class="spacer"></span>
          ${prev ? `<a href="#/problem/${prev.id}">&lsaquo; Prev</a>` : ""}
          ${next ? `<a href="#/problem/${next.id}">Next &rsaquo;</a>` : ""}
        </nav>
        <h1>${ex.id}. <span class="diff diff-${ex.difficulty}">${DIFFICULTY_LABEL[ex.difficulty]}</span></h1>
        <div class="question">${renderMarkdown(ex.question)}</div>
        <div class="tags">${ex.tags.map((t) => `<span class="tag">${t}</span>`).join("")}</div>
      </div>
      <div class="pane pane-right">
        <div class="editor-host"></div>
        <div class="toolbar">
          <button class="btn" data-action="run" title="Ctrl+Enter">Run</button>
          <span class="spacer"></span>
          <span class="kbd-hint">Ctrl+Enter to run</span>
        </div>
        <div class="output" aria-live="polite"><p class="out-note">Output will appear here.</p></div>
      </div>
    </section>`;

  const output = root.querySelector<HTMLElement>(".output")!;
  const runBtn = root.querySelector<HTMLButtonElement>('[data-action="run"]')!;
  let busy = false;

  const run = async () => {
    if (busy) return;
    busy = true;
    runBtn.disabled = true;
    output.innerHTML =
      runner.status.state === "loading"
        ? `<p class="out-note">Waiting for Python to load…</p>`
        : `<p class="out-note">Running…</p>`;
    const outcome = await runner.run({ code: editor.state.doc.toString(), prelude: ex.prelude });
    output.innerHTML = renderOutcome(outcome);
    busy = false;
    runBtn.disabled = false;
  };

  const editor: EditorView = createEditor(root.querySelector(".editor-host")!, {
    doc: starterCode(ex.prelude),
    dark: document.documentElement.dataset.theme === "dark",
    onRun: run,
  });
  runBtn.addEventListener("click", run);
  editor.focus();

  return () => editor.destroy();
}
