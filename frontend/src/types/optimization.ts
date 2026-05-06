export type CriterionType = "min" | "max";
export type OptimizationMethod = "weighted_sum" | "pareto" | "topsis";

export interface Criterion {
  id?: number;
  name: string;
  type: CriterionType;
  weight: number;
}

export interface AlternativeValue {
  criterion_name?: string;
  criterion_id?: number;
  value: number;
}

export interface Alternative {
  id?: number;
  name: string;
  values: AlternativeValue[];
}

export interface OptimizationTask {
  id?: number;
  title: string;
  description?: string;
  criteria: Criterion[];
  alternatives: Alternative[];
  created_at?: string;
  updated_at?: string;
}

export interface TaskListItem {
  id: number;
  title: string;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface RankingItem {
  alternative_id: number;
  alternative_name: string;
  score: number;
  rank: number;
  is_pareto_optimal: boolean;
  details: Record<string, unknown>;
}

export interface ChartData {
  criteria: string[];
  alternatives: string[];
  values: number[][];
  pareto_points: Array<{ alternative_name: string; x: number; y: number }>;
}

export interface OptimizationResult {
  task_id: number;
  run_id: number;
  method: string;
  execution_time_ms: number;
  ranking: RankingItem[];
  chart_data: ChartData;
}

export interface RunHistoryItem {
  id: number;
  task_id: number;
  method: string;
  created_at: string;
  execution_time_ms: number;
}

export interface MethodComparison {
  task_id: number;
  runs: OptimizationResult[];
  summary: Array<{
    method: string;
    best_alternative: string;
    best_score: number;
    run_id: number;
  }>;
}
