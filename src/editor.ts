import { autocompletion } from "@codemirror/autocomplete";
import { indentWithTab } from "@codemirror/commands";
import { python } from "@codemirror/lang-python";
import { indentUnit } from "@codemirror/language";
import { Compartment, EditorState } from "@codemirror/state";
import { oneDark } from "@codemirror/theme-one-dark";
import { EditorView, keymap } from "@codemirror/view";
import { basicSetup } from "codemirror";

const themeCompartment = new Compartment();

export interface EditorOptions {
  doc: string;
  dark: boolean;
  onChange?: (doc: string) => void;
  onRun?: () => void;
  onSubmit?: () => void;
}

export function createEditor(parent: HTMLElement, opts: EditorOptions): EditorView {
  const runKeys = keymap.of([
    { key: "Mod-Enter", run: () => (opts.onRun?.(), true) },
    { key: "Mod-Shift-Enter", run: () => (opts.onSubmit?.(), true) },
  ]);
  return new EditorView({
    parent,
    state: EditorState.create({
      doc: opts.doc,
      extensions: [
        runKeys,
        basicSetup,
        // Completions only on Ctrl+Space: popping up on every keystroke is noisy for beginners.
        autocompletion({ activateOnTyping: false }),
        keymap.of([indentWithTab]),
        python(),
        indentUnit.of("    "),
        EditorState.tabSize.of(4),
        themeCompartment.of(opts.dark ? oneDark : []),
        EditorView.updateListener.of((u) => {
          if (u.docChanged) opts.onChange?.(u.state.doc.toString());
        }),
      ],
    }),
  });
}

export function setEditorDark(view: EditorView, dark: boolean): void {
  view.dispatch({ effects: themeCompartment.reconfigure(dark ? oneDark : []) });
}

export function setEditorDoc(view: EditorView, doc: string): void {
  view.dispatch({ changes: { from: 0, to: view.state.doc.length, insert: doc } });
}
