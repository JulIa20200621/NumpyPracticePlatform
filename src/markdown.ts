// Just enough Markdown for numpy-100 questions: ``` fences and `inline code`.

export function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function inline(s: string): string {
  return escapeHtml(s)
    .replace(/`([^`]+)`/g, "<code>$1</code>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
}

export function renderMarkdown(src: string): string {
  const parts = src.split(/```[a-z]*\n?/);
  return parts
    .map((part, i) => {
      if (i % 2 === 1) return `<pre class="code-block">${escapeHtml(part.replace(/\n$/, ""))}</pre>`;
      const text = part.trim();
      return text ? `<p>${inline(text).replace(/\n/g, "<br>")}</p>` : "";
    })
    .join("");
}

export function renderInline(src: string): string {
  return inline(src);
}
