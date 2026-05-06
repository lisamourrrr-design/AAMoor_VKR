import Plot from "react-plotly.js";
import type { MethodComparison } from "../types/optimization";

interface Props {
  comparison: MethodComparison;
}

export function MethodComparisonChart({ comparison }: Props) {
  const alternatives = Array.from(
    new Set(comparison.runs.flatMap((run) => run.ranking.map((item) => item.alternative_name))),
  );

  return (
    <section className="panel">
      <h2>Сравнение методов</h2>
      <Plot
        data={comparison.runs.map((run) => ({
          type: "bar",
          name: run.method,
          x: alternatives,
          y: alternatives.map(
            (name) => run.ranking.find((item) => item.alternative_name === name)?.score ?? 0,
          ),
        }))}
        layout={{
          barmode: "group",
          autosize: true,
          height: 380,
          margin: { l: 45, r: 20, t: 20, b: 55 },
          paper_bgcolor: "rgba(0,0,0,0)",
          plot_bgcolor: "rgba(0,0,0,0)",
        }}
        style={{ width: "100%" }}
        useResizeHandler
        config={{ displayModeBar: false, responsive: true }}
      />
    </section>
  );
}
