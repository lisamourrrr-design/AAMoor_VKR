import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { optimizationApi } from "../api/optimizationApi";
import type { RunHistoryItem, TaskListItem } from "../types/optimization";

export function HistoryPage() {
  const [tasks, setTasks] = useState<TaskListItem[]>([]);
  const [runsByTask, setRunsByTask] = useState<Record<number, RunHistoryItem[]>>({});

  useEffect(() => {
    optimizationApi.getTasks().then(async (loadedTasks) => {
      setTasks(loadedTasks);
      const pairs = await Promise.all(
        loadedTasks.map(async (task) => [task.id, await optimizationApi.getRuns(task.id)] as const),
      );
      setRunsByTask(Object.fromEntries(pairs));
    });
  }, []);

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>История</h1>
          <p className="muted">Сохранённые задачи и выполненные запуски.</p>
        </div>
      </header>
      {tasks.map((task) => (
        <section className="panel" key={task.id}>
          <div className="panel-heading">
            <div>
              <h2>{task.title}</h2>
              <p className="muted">{task.description || "Без описания"}</p>
            </div>
            <Link to={`/tasks/${task.id}/edit`}>Редактировать</Link>
          </div>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Run ID</th>
                  <th>Метод</th>
                  <th>Дата</th>
                  <th>Время, мс</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {(runsByTask[task.id] ?? []).map((run) => (
                  <tr key={run.id}>
                    <td>{run.id}</td>
                    <td>{run.method}</td>
                    <td>{new Date(run.created_at).toLocaleString()}</td>
                    <td>{run.execution_time_ms.toFixed(2)}</td>
                    <td>
                      <Link to={`/results/${run.id}`}>Открыть</Link>
                    </td>
                  </tr>
                ))}
                {(runsByTask[task.id] ?? []).length === 0 && (
                  <tr>
                    <td colSpan={5}>Запусков пока нет</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      ))}
    </div>
  );
}
