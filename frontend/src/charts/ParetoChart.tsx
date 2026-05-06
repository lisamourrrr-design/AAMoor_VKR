import Plot from "react-plotly.js";
import type { ChartData, RankingItem } from "../types/optimization";

interface Props {
  chartData: ChartData;
  ranking: RankingItem[];
}

export function ParetoChart({ chartData, ranking }: Props) {
  if (chartData.criteria.length !== 2) {
    return (
      <section className="panel">
        <h2>Парето-оптимальные решения</h2>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Альтернатива</th>
                <th>Score</th>
              </tr>
            </thead>
            <tbody>
              {ranking
                .filter((item) => item.is_pareto_optimal)
                .map((item) => (
                  <tr key={item.alternative_id}>
                    <td>{item.alternative_name}</td>
                    <td>{item.score.toFixed(4)}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </section>
    );
  }

  const paretoNames = new Set(chartData.pareto_points.map((point) => point.alternative_name));
  return (
    <section className="panel">
      <h2>Фронт Парето</h2>
      <Plot
        data={[
          {
            type: "scatter",
            mode: "markers+text",
            x: chartData.values.map((row) => row[0]),
            y: chartData.values.map((row) => row[1]),
            text: chartData.alternatives,
            textposition: "top center",
            marker: {
              color: chartData.alternatives.map((name) => (paretoNames.has(name) ? "#16a34a" : "#64748b")),
              size: 12,
            },
          },
        ]}
        layout={{
          autosize: true,
          height: 380,
          xaxis: { title: chartData.criteria[0] },
          yaxis: { title: chartData.criteria[1] },
          margin: { l: 55, r: 20, t: 20, b: 55 },
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
