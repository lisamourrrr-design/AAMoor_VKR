import type { Criterion } from "../types/optimization";

interface Props {
  criteria: Criterion[];
  onChange: (criteria: Criterion[]) => void;
}

export function CriteriaTable({ criteria, onChange }: Props) {
  const update = (index: number, patch: Partial<Criterion>) => {
    onChange(criteria.map((item, i) => (i === index ? { ...item, ...patch } : item)));
  };

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Критерии</h2>
        <button
          type="button"
          onClick={() =>
            onChange([...criteria, { name: `Критерий ${criteria.length + 1}`, type: "max", weight: 0 }])
          }
        >
          Добавить
        </button>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Название</th>
              <th>Тип</th>
              <th>Вес</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {criteria.map((criterion, index) => (
              <tr key={index}>
                <td>
                  <input
                    value={criterion.name}
                    onChange={(event) => update(index, { name: event.target.value })}
                  />
                </td>
                <td>
                  <select
                    value={criterion.type}
                    onChange={(event) => update(index, { type: event.target.value as Criterion["type"] })}
                  >
                    <option value="max">max</option>
                    <option value="min">min</option>
                  </select>
                </td>
                <td>
                  <input
                    min="0"
                    step="0.01"
                    type="number"
                    value={criterion.weight}
                    onChange={(event) => update(index, { weight: Number(event.target.value) })}
                  />
                </td>
                <td>
                  <button type="button" onClick={() => onChange(criteria.filter((_, i) => i !== index))}>
                    Удалить
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
