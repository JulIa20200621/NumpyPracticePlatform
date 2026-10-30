import { escapeHtml } from "./markdown";
import { TIME_LIMIT_MS, type RunOutcome } from "./runner";

function block(label: string, body: string, cls = ""): string {
  return `<div class="out-block ${cls}"><div class="out-label">${label}</div><pre>${escapeHtml(body)}</pre></div>`;
}

export function renderOutcome(outcome: RunOutcome): string {
  if (outcome.kind === "unavailable") return block("Error", outcome.text, "out-error");
  if (outcome.kind === "timeout") {
    return `<div class="verdict verdict-fail">Time limit exceeded</div>
      <p class="out-note">Your code ran for more than ${TIME_LIMIT_MS / 1000} s and was stopped. Check for infinite loops.
      Python is restarting…</p>`;
  }
  const { result, ms } = outcome;
  let html = "";
  if (result.passed === true) html += `<div class="verdict verdict-pass">✅ Accepted</div>`;
  else if (result.passed === false) {
    html += `<div class="verdict verdict-fail">❌ Wrong answer</div>`;
    if (result.message) html += `<p class="out-message">${escapeHtml(result.message)}</p>`;
  }
  if (result.stdout) html += block("Output", result.stdout);
  if (result.value !== null) html += block("Value of last expression", result.value);
  if (result.error) html += block("Error", result.error, "out-error");
  if (!result.stdout && result.value === null && !result.error && result.passed === null) {
    html += `<p class="out-note">Ran with no output. Use <code>print(...)</code> or end with an expression to see a value.</p>`;
  }
  html += `<p class="out-time">${ms.toFixed(0)} ms</p>`;
  return html;
}
