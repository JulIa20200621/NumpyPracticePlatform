export interface RunRequest {
  id: number;
  code: string;
  test?: string;
  setup?: string;
}

export interface RunResult {
  stdout: string;
  value: string | null;
  error: string | null;
  passed: boolean | null;
  message: string | null;
}

export type WorkerMessage =
  | { type: "progress"; text: string }
  | { type: "ready" }
  | { type: "init-error"; text: string }
  | { type: "result"; id: number; result: RunResult };
