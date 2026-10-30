import type { TestCase } from "../data";

export interface RunRequest {
  id: number;
  code: string;
  given?: string;
  setup?: string;
  /** Test cases to run after the code (Submit). Omit for Run. */
  cases?: TestCase[];
  /** Run `import numpy as np` before the student's code (default true). */
  prelude?: boolean;
}

export interface CaseResult {
  name: string;
  status: "pass" | "fail" | "skipped";
  message: string | null;
}

export interface RunResult {
  stdout: string;
  value: string | null;
  error: string | null;
  /** Run time of the student's code. */
  time_ms: number | null;
  /** Peak bytes allocated by the student's code. */
  memory: number | null;
  passed: boolean | null;
  cases: CaseResult[] | null;
}

export type WorkerMessage =
  | { type: "progress"; text: string }
  | { type: "ready" }
  | { type: "init-error"; text: string }
  | { type: "result"; id: number; result: RunResult };
