import type { RankingItem } from "../types/optimization";

interface Props {
  ranking: RankingItem[];
}

export function ResultTable({ ranking }: Props) {
  return (
    <section className="panel">
      <h2>Ранжирование</h2>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Ранг</th>
              <th>Альтернатива</th>
              <th>Score</th>
              <th>Парето</th>
            </tr>
          </thead>
          <tbody>
            {ranking.map((item) => (
              <tr key={item.alternative_id}>
                <td>{item.rank}</td>
                <td>{item.alternative_name}</td>
                <td>{item.score.toFixed(4)}</td>
                <td>{item.is_pareto_optimal ? "Да" : "Нет"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
