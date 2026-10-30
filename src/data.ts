import raw from "./data/exercises.json";

export interface Exercise {
  id: number;
  title: string;
  question: string;
  hint: string;
  solution: string;
  difficulty: 1 | 2 | 3;
  tags: string[];
}

export const exercises = raw as Exercise[];

export const DIFFICULTY_LABEL = { 1: "Easy", 2: "Medium", 3: "Hard" } as const;

export function getExercise(id: number): Exercise | undefined {
  return exercises.find((e) => e.id === id);
}
