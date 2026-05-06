import Plot from "react-plotly.js";
import type { RankingItem } from "../types/optimization";

interface Props {
  ranking: RankingItem[];
}

export function RankingChart({ ranking }: Props) {
  const sorted = [...ranking].sort((a, b) => a.rank - b.rank);
  return (
    <section className="panel">
      <h2>Score альтернатив</h2>
      <Plot
        data={[
          {
            type: "bar",
            x: sorted.map((item) => item.alternative_name),
            y: sorted.map((item) => item.score),
            marker: { color: "#2563eb" },
          },
        ]}
        layout={{
          autosize: true,
          height: 360,
          margin: { l: 45, r: 20, t: 20, b: 45 },
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
