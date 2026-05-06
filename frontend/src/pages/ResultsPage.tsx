import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { optimizationApi } from "../api/optimizationApi";
import { MethodComparisonChart } from "../charts/MethodComparisonChart";
import { ParetoChart } from "../charts/ParetoChart";
import { RankingChart } from "../charts/RankingChart";
import { ResultTable } from "../components/ResultTable";
import type { MethodComparison, OptimizationResult, RankingItem } from "../types/optimization";

const detailLabels: Record<string, string> = {
  normalized_values: "Нормализованные значения",
  normalized_weights: "Нормализованные веса критериев",
  weighted_values: "Взвешенные нормализованные значения",
  distance_to_ideal: "Расстояние до идеального решения",
  distance_to_anti_ideal: "Расстояние до антиидеального решения",
  values: "Исходные значения критериев",
};

function formatDetailValue(value: unknown) {
  if (Array.isArray(value)) {
    return value.map((item) => (typeof item === "number" ? item.toFixed(6) : String(item))).join("; ");
  }
  if (typeof value === "number") {
    return value.toFixed(6);
  }
  return JSON.stringify(value);
}

function CalculationDetails({ ranking }: { ranking: RankingItem[] }) {
  return (
    <section className="panel">
      <h2>Детали расчёта</h2>
      <div className="details-list">
        {ranking.map((item) => (
          <article className="details-item" key={item.alternative_id}>
            <h3>
              {item.rank}. {item.alternative_name}
            </h3>
            <dl>
              {Object.entries(item.details).map(([key, value]) => (
                <div key={key}>
                  <dt>{detailLabels[key] ?? key}</dt>
                  <dd>{formatDetailValue(value)}</dd>
                </div>
              ))}
            </dl>
          </article>
        ))}
      </div>
    </section>
  );
}

export function ResultsPage() {
  const { runId, taskId } = useParams();
  const [result, setResult] = useState<OptimizationResult | null>(null);
  const [comparison, setComparison] = useState<MethodComparison | null>(null);

  useEffect(() => {
    if (runId) {
      const cached = sessionStorage.getItem("lastResult");
      if (cached) setResult(JSON.parse(cached));
      optimizationApi.getRun(Number(runId)).then(setResult).catch(() => undefined);
    }
    if (taskId) {
      const cached = sessionStorage.getItem("lastComparison");
      if (cached) setComparison(JSON.parse(cached));
    }
  }, [runId, taskId]);

  if (comparison) {
    return (
      <div className="page-stack">
        <header className="page-header">
          <div>
            <h1>Сравнение методов</h1>
            <p className="muted">Запуски сохранены в истории задачи #{comparison.task_id}.</p>
          </div>
        </header>
        <MethodComparisonChart comparison={comparison} />
        <section className="panel">
          <h2>Лучшие альтернативы</h2>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Метод</th>
                  <th>Лучшая альтернатива</th>
                  <th>Score</th>
                  <th>Run ID</th>
                </tr>
              </thead>
              <tbody>
                {comparison.summary.map((item) => (
                  <tr key={item.method}>
                    <td>{item.method}</td>
                    <td>{item.best_alternative}</td>
                    <td>{item.best_score.toFixed(4)}</td>
                    <td>{item.run_id}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    );
  }

  if (!result) {
    return <div className="panel">Загрузка результата...</div>;
  }

  return (
    <div className="page-stack">
      <header className="page-header">
        <div>
          <h1>Результат: {result.method}</h1>
          <p className="muted">
            Запуск #{result.run_id}, время выполнения {result.execution_time_ms.toFixed(2)} мс
          </p>
        </div>
      </header>
      <ResultTable ranking={result.ranking} />
      <RankingChart ranking={result.ranking} />
      <ParetoChart chartData={result.chart_data} ranking={result.ranking} />
      <CalculationDetails ranking={result.ranking} />
    </div>
  );
}
