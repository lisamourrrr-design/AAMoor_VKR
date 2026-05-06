import axios from "axios";
import type {
  MethodComparison,
  OptimizationMethod,
  OptimizationResult,
  OptimizationTask,
  RunHistoryItem,
  TaskListItem,
} from "../types/optimization";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
});

export const optimizationApi = {
  createTask: async (task: OptimizationTask) => {
    const { data } = await api.post<OptimizationTask>("/api/tasks", task);
    return data;
  },
  updateTask: async (taskId: number, task: OptimizationTask) => {
    const { data } = await api.put<OptimizationTask>(`/api/tasks/${taskId}`, task);
    return data;
  },
  getTasks: async () => {
    const { data } = await api.get<TaskListItem[]>("/api/tasks");
    return data;
  },
  getTask: async (taskId: number) => {
    const { data } = await api.get<OptimizationTask>(`/api/tasks/${taskId}`);
    return data;
  },
  deleteTask: async (taskId: number) => {
    await api.delete(`/api/tasks/${taskId}`);
  },
  optimize: async (taskId: number, method: OptimizationMethod) => {
    const { data } = await api.post<OptimizationResult>(
      `/api/tasks/${taskId}/optimize`,
      { method },
    );
    return data;
  },
  compare: async (taskId: number) => {
    const { data } = await api.post<MethodComparison>(`/api/tasks/${taskId}/compare`);
    return data;
  },
  getRuns: async (taskId: number) => {
    const { data } = await api.get<RunHistoryItem[]>(`/api/tasks/${taskId}/runs`);
    return data;
  },
  getRun: async (runId: number) => {
    const { data } = await api.get<OptimizationResult>(`/api/runs/${runId}`);
    return data;
  },
};
