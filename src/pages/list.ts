import { DIFFICULTY_LABEL, exercises } from "../data";
import { renderInline } from "../markdown";

export function renderList(root: HTMLElement): void {
  const rows = exercises
    .map(
      (e) => `
      <tr>
        <td class="num">${e.id}</td>
        <td><a href="#/problem/${e.id}">${renderInline(e.title)}</a></td>
        <td><span class="diff diff-${e.difficulty}">${DIFFICULTY_LABEL[e.difficulty]}</span></td>
        <td>${e.tags.map((t) => `<span class="tag">${t}</span>`).join("")}</td>
      </tr>`,
    )
    .join("");

  root.innerHTML = `
    <section class="list-page">
      <h1>Problems</h1>
      <table class="problem-table">
        <thead><tr><th>#</th><th>Title</th><th>Difficulty</th><th>Tags</th></tr></thead>
        <tbody>${rows}</tbody>
      </table>
    </section>`;
}
