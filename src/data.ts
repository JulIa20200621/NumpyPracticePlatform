import raw from "./data/exercises.json";

export interface Exercise {
  id: number;
  title: string;
  question: string;
  hint: string;
  solution: string;
  difficulty: 1 | 2 | 3;
  tags: string[];
  /** false: numpy is not pre-imported (exercise 1 asks you to import it). */
  prelude: boolean;
  /** Extra instructions for auto-grading (which variable to store the answer in). Markdown. */
  task: string;
  /** Code run before the student's code and shown to them. */
  given: string;
  /** Hidden code run after `given`. */
  setup: string;
  /** Test cases, run in order on Submit. Empty: not auto-graded yet. */
  cases: TestCase[];
}

export interface TestCase {
  name: string;
  code: string;
}

export const exercises = raw as Exercise[];

export const DIFFICULTY_LABEL = { 1: "Easy", 2: "Medium", 3: "Hard" } as const;

export function getExercise(id: number): Exercise | undefined {
  return exercises.find((e) => e.id === id);
}
