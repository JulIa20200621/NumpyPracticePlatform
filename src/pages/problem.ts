import type { EditorView } from "@codemirror/view";
import { DIFFICULTY_LABEL, exercises, getExercise } from "../data";
import { createEditor } from "../editor";
import { escapeHtml, renderMarkdown } from "../markdown";
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
  const gradable = ex.cases.length > 0;
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
        ${
          ex.task || ex.given
            ? `<div class="task">
                ${ex.task ? `<div class="task-label">Your task</div>${renderMarkdown(ex.task)}` : ""}
                ${ex.given ? `<div class="task-label">Already defined for you</div><pre class="code-block">${escapeHtml(ex.given)}</pre>` : ""}
              </div>`
            : ""
        }
        <div class="tags">${ex.tags.map((t) => `<span class="tag">${t}</span>`).join("")}</div>
      </div>
      <div class="pane pane-right">
        <div class="editor-host"></div>
        <div class="toolbar">
          <button class="btn" data-action="run" title="Ctrl+Enter">Run</button>
          <button class="btn btn-primary" data-action="submit" title="Ctrl+Shift+Enter"${gradable ? "" : " disabled"}>Submit</button>
          <span class="spacer"></span>
          <span class="kbd-hint">${gradable ? "Ctrl+Enter run · Ctrl+Shift+Enter submit" : "Auto-grading for this problem is coming soon"}</span>
        </div>
        <div class="output" aria-live="polite"><p class="out-note">Output will appear here.</p></div>
      </div>
    </section>`;

  const output = root.querySelector<HTMLElement>(".output")!;
  const runBtn = root.querySelector<HTMLButtonElement>('[data-action="run"]')!;
  const submitBtn = root.querySelector<HTMLButtonElement>('[data-action="submit"]')!;
  let busy = false;

  const execute = async (submit: boolean) => {
    if (busy || (submit && !gradable)) return;
    busy = true;
    runBtn.disabled = submitBtn.disabled = true;
    output.innerHTML =
      runner.status.state === "loading"
        ? `<p class="out-note">Waiting for Python to load…</p>`
        : `<p class="out-note">${submit ? "Checking your answer…" : "Running…"}</p>`;
    const outcome = await runner.run({
      code: editor.state.doc.toString(),
      given: ex.given,
      setup: ex.setup,
      cases: submit ? ex.cases : undefined,
      prelude: ex.prelude,
    });
    output.innerHTML = renderOutcome(outcome);
    busy = false;
    runBtn.disabled = false;
    submitBtn.disabled = !gradable;
  };
  const run = () => execute(false);
  const submit = () => execute(true);

  const editor: EditorView = createEditor(root.querySelector(".editor-host")!, {
    doc: starterCode(ex.prelude),
    dark: document.documentElement.dataset.theme === "dark",
    onRun: run,
    onSubmit: submit,
  });
  runBtn.addEventListener("click", run);
  submitBtn.addEventListener("click", submit);
  editor.focus();

  return () => editor.destroy();
}
