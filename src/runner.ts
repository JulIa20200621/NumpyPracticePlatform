import type { RunRequest, RunResult, WorkerMessage } from "./worker/protocol";

export const TIME_LIMIT_MS = 5000;

export type RunnerStatus =
  | { state: "loading"; text: string }
  | { state: "ready" }
  | { state: "running" }
  | { state: "error"; text: string };

export type RunOutcome = { kind: "done"; result: RunResult; ms: number } | { kind: "timeout" } | { kind: "unavailable"; text: string };

type Listener = (s: RunnerStatus) => void;

/** Owns the Pyodide worker. Restarts it when a run exceeds the time limit. */
class Runner {
  private worker!: Worker;
  private ready!: Promise<boolean>;
  private nextId = 1;
  private listeners = new Set<Listener>();
  status: RunnerStatus = { state: "loading", text: "Loading Python…" };

  constructor() {
    this.start();
  }

  onStatus(fn: Listener): () => void {
    this.listeners.add(fn);
    fn(this.status);
    return () => this.listeners.delete(fn);
  }

  private setStatus(s: RunnerStatus): void {
    this.status = s;
    this.listeners.forEach((fn) => fn(s));
  }

  private start(): void {
    this.setStatus({ state: "loading", text: "Loading Python…" });
    this.worker = new Worker(new URL("./worker/pyodide-worker.ts", import.meta.url), { type: "module" });
    this.ready = new Promise((resolve) => {
      const onMessage = (e: MessageEvent<WorkerMessage>) => {
        const msg = e.data;
        if (msg.type === "progress") this.setStatus({ state: "loading", text: msg.text });
        else if (msg.type === "ready" || msg.type === "init-error") {
          this.worker.removeEventListener("message", onMessage);
          if (msg.type === "ready") this.setStatus({ state: "ready" });
          else this.setStatus({ state: "error", text: `Could not load Python: ${msg.text}` });
          resolve(msg.type === "ready");
        }
      };
      this.worker.addEventListener("message", onMessage);
    });
  }

  async run(req: Omit<RunRequest, "id">): Promise<RunOutcome> {
    if (!(await this.ready)) {
      return { kind: "unavailable", text: this.status.state === "error" ? this.status.text : "Python is not available." };
    }
    const id = this.nextId++;
    const worker = this.worker;
    this.setStatus({ state: "running" });
    const started = performance.now();

    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        worker.removeEventListener("message", onMessage);
        worker.terminate();
        this.start();
        resolve({ kind: "timeout" });
      }, TIME_LIMIT_MS);

      const onMessage = (e: MessageEvent<WorkerMessage>) => {
        const msg = e.data;
        if (msg.type !== "result" || msg.id !== id) return;
        clearTimeout(timer);
        worker.removeEventListener("message", onMessage);
        this.setStatus({ state: "ready" });
        resolve({ kind: "done", result: msg.result, ms: performance.now() - started });
      };
      worker.addEventListener("message", onMessage);
      worker.postMessage({ id, ...req } satisfies RunRequest);
    });
  }
}

export const runner = new Runner();
