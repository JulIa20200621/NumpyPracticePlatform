import { escapeHtml } from "./markdown";
import { TIME_LIMIT_MS, type RunOutcome } from "./runner";
import type { CaseResult, RunResult } from "./worker/protocol";

function block(label: string, body: string, cls = ""): string {
  return `<div class="out-block ${cls}"><div class="out-label">${label}</div><pre>${escapeHtml(body)}</pre></div>`;
}

export function formatBytes(n: number): string {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(2)} MB`;
}

function formatMs(ms: number): string {
  return ms < 10 ? `${ms.toFixed(2)} ms` : `${ms.toFixed(0)} ms`;
}

function stats(r: RunResult): string {
  if (r.time_ms === null) return "";
  return `<div class="stats">
      <div class="stat"><span class="stat-label">Runtime</span><span class="stat-value">${formatMs(r.time_ms)}</span></div>
      <div class="stat"><span class="stat-label">Memory</span><span class="stat-value">${formatBytes(r.memory ?? 0)}</span></div>
    </div>`;
}

const CASE_ICON = { pass: "✓", fail: "✗", skipped: "·" } as const;

function caseList(cases: CaseResult[]): string {
  const items = cases
    .map(
      (c, i) => `
      <li class="case case-${c.status}">
        <span class="case-icon">${CASE_ICON[c.status]}</span>
        <div class="case-body">
          <div class="case-name">Case ${i + 1}: ${escapeHtml(c.name).replace(/`([^`]+)`/g, "<code>$1</code>")}</div>
          ${c.message ? `<pre class="case-message">${escapeHtml(c.message)}</pre>` : ""}
          ${c.status === "skipped" ? `<div class="case-note">not run</div>` : ""}
        </div>
      </li>`,
    )
    .join("");
  return `<div class="out-label">Test cases</div><ul class="cases">${items}</ul>`;
}

export function renderOutcome(outcome: RunOutcome): string {
  if (outcome.kind === "unavailable") return block("Error", outcome.text, "out-error");
  if (outcome.kind === "timeout") {
    return `<div class="verdict verdict-fail">Time limit exceeded</div>
      <p class="out-note">Your code ran for more than ${TIME_LIMIT_MS / 1000} s and was stopped. Check for infinite loops.
      Python is restarting…</p>`;
  }
  const r = outcome.result;
  let html = "";

  if (r.cases) {
    const passed = r.cases.filter((c) => c.status === "pass").length;
    const verdict = r.passed ? "Accepted" : r.error ? "Runtime error" : "Wrong answer";
    html += `<div class="verdict-row">
        <div class="verdict ${r.passed ? "verdict-pass" : "verdict-fail"}">${r.passed ? "✅" : "❌"} ${verdict}</div>
        <span class="verdict-count">${passed} / ${r.cases.length} test cases passed</span>
      </div>`;
    if (r.error) html += block("Error", r.error, "out-error");
    html += stats(r);
    html += caseList(r.cases);
    if (r.stdout) html += block("Output", r.stdout);
    if (r.value !== null) html += block("Value of last expression", r.value);
    return html;
  }

  if (r.stdout) html += block("Output", r.stdout);
  if (r.value !== null) html += block("Value of last expression", r.value);
  if (r.error) html += block("Error", r.error, "out-error");
  if (!r.stdout && r.value === null && !r.error) {
    html += `<p class="out-note">Ran with no output. Use <code>print(...)</code> or end with an expression to see a value.</p>`;
  }
  html += stats(r);
  return html;
}
