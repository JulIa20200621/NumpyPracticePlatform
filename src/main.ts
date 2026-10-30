import "./style.css";
import { renderList } from "./pages/list";
import { renderProblem } from "./pages/problem";

const app = document.getElementById("app")!;

function route(): void {
  const m = location.hash.match(/^#\/problem\/(\d+)/);
  if (m) renderProblem(app, Number(m[1]));
  else renderList(app);
  window.scrollTo(0, 0);
}

window.addEventListener("hashchange", route);
route();
