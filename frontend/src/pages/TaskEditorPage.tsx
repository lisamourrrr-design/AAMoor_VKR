import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { optimizationApi } from "../api/optimizationApi";
import { AlternativeTable } from "../components/AlternativeTable";
import { CriteriaTable } from "../components/CriteriaTable";
import { MethodSelector } from "../components/MethodSelector";
import type { OptimizationMethod, OptimizationTask } from "../types/optimization";

const initialTask: OptimizationTask = {
  title: "Выбор поставщика",
  description: "Демонстрационная задача для ВКР",
  criteria: [
    { name: "Стоимость", type: "min", weight: 0.4 },
    { name: "Качество", type: "max", weight: 0.4 },
    { name: "Срок", type: "min", weight: 0.2 },
  ],
  alternatives: [
    {
      name: "A1",
      values: [
        { criterion_name: "Стоимость", value: 120 },
        { criterion_name: "Качество", value: 8 },
        { criterion_name: "Срок", value: 5 },
      ],
    },
    {
      name: "A2",
      values: [
        { criterion_name: "Стоимость", value: 100 },
        { criterion_name: "Качество", value: 7 },
        { criterion_name: "Срок", value: 4 },
      ],
    },
    {
      name: "A3",
      values: [
        { criterion_name: "Стоимость", value: 140 },
        { criterion_name: "Качество", value: 9 },
        { criterion_name: "Срок", value: 6 },
      ],
    },
  ],
};

export function TaskEditorPage() {
  const [task, setTask] = useState<OptimizationTask>(initialTask);
  const [method, setMethod] = useState<OptimizationMethod>("topsis");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  const navigate = useNavigate();
  const { taskId } = useParams();

  useEffect(() => {
    if (!taskId) return;
    optimizationApi.getTask(Number(taskId)).then(setTask).catch(() => {
      setError("Не удалось загрузить задачу для редактирования");
    });
  }, [taskId]);

  const weightSum = useMemo(
    () => task.criteria.reduce((sum, criterion) => sum + Number(criterion.weight || 0), 0),
    [task.criteria],
  );

  const prepareTask = (): OptimizationTask => ({
    ...task,
    alternatives: task.alternatives.map((alternative) => ({
      ...alternative,
      values: task.criteria.map((criterion) => {
        const value = alternative.values.find((item) => item.criterion_name === criterion.name);
        return { criterion_name: criterion.name, value: Number(value?.value ?? 0) };
      }),
    })),
  });

  const saveAndRun = async (mode: "single" | "compare") => {
    setError("");
    setSaving(true);
    try {
      const payload = prepareTask();
      const saved = task.id
        ? await optimizationApi.updateTask(task.id, payload)
        : await optimizationApi.createTask(payload);
      if (!saved.id) return;
      if (mode === "compare") {
        const comparison = await optimizationApi.compare(saved.id);
        sessionStorage.setItem("lastComparison", JSON.stringify(comparison));
        navigate(`/results/compare/${saved.id}`);
      } else {
        const result = await optimizationApi.optimize(saved.id, method);
        sessionStorage.setItem("lastResult", JSON.stringify(result));
        navigate(`/results/${result.run_id}`);
      }
    } catch (requestError: any) {
      setError(requestError.response?.data?.detail ?? "Не удалось выполнить расчёт");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>{task.id ? "Редактирование задачи" : "Задача оптимизации"}</h1>
          <p className="muted">Введите критерии, альтернативы и запустите расчёт.</p>
        </div>
        <div className="actions">
          <button type="button" onClick={() => saveAndRun("compare")} disabled={saving}>
            Сравнить методы
          </button>
          <button className="primary" type="button" onClick={() => saveAndRun("single")} disabled={saving}>
            Рассчитать
          </button>
        </div>
      </header>

      <section className="panel grid-two">
        <label>
          Название
          <input value={task.title} onChange={(event) => setTask({ ...task, title: event.target.value })} />
        </label>
        <label>
          Сумма весов
          <input value={weightSum.toFixed(4)} readOnly />
        </label>
        <label className="span-two">
          Описание
          <textarea
            value={task.description}
            onChange={(event) => setTask({ ...task, description: event.target.value })}
          />
        </label>
        <div className="span-two">
          <MethodSelector value={method} onChange={setMethod} />
        </div>
      </section>

      {error && <div className="error">{error}</div>}
      <CriteriaTable criteria={task.criteria} onChange={(criteria) => setTask({ ...task, criteria })} />
      <AlternativeTable
        alternatives={task.alternatives}
        criteria={task.criteria}
        onChange={(alternatives) => setTask({ ...task, alternatives })}
      />
    </div>
  );
}
