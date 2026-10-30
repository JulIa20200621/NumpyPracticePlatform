import { DIFFICULTY_LABEL, getExercise } from "../data";
import { renderMarkdown } from "../markdown";

export function renderProblem(root: HTMLElement, id: number): void {
  const ex = getExercise(id);
  if (!ex) {
    root.innerHTML = `<p class="notice">Problem ${id} not found. <a href="#/">Back to the list</a></p>`;
    return;
  }
  root.innerHTML = `
    <section class="problem-page">
      <p><a href="#/">&larr; All problems</a></p>
      <h1>${ex.id}. <span class="diff diff-${ex.difficulty}">${DIFFICULTY_LABEL[ex.difficulty]}</span></h1>
      <div class="question">${renderMarkdown(ex.question)}</div>
      <div>${ex.tags.map((t) => `<span class="tag">${t}</span>`).join("")}</div>
    </section>`;
}
