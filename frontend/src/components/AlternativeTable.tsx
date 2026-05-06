import type { Alternative, Criterion } from "../types/optimization";

interface Props {
  alternatives: Alternative[];
  criteria: Criterion[];
  onChange: (alternatives: Alternative[]) => void;
}

export function AlternativeTable({ alternatives, criteria, onChange }: Props) {
  const ensureValues = (alternative: Alternative) => ({
    ...alternative,
    values: criteria.map((criterion) => {
      const existing = alternative.values.find((value) => value.criterion_name === criterion.name);
      return existing ?? { criterion_name: criterion.name, value: 0 };
    }),
  });

  const prepared = alternatives.map(ensureValues);

  const updateValue = (alternativeIndex: number, criterionName: string, value: number) => {
    onChange(
      prepared.map((alternative, index) =>
        index === alternativeIndex
          ? {
              ...alternative,
              values: alternative.values.map((item) =>
                item.criterion_name === criterionName ? { ...item, value } : item,
              ),
            }
          : alternative,
      ),
    );
  };

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Альтернативы</h2>
        <button
          type="button"
          onClick={() =>
            onChange([
              ...prepared,
              {
                name: `A${prepared.length + 1}`,
                values: criteria.map((criterion) => ({ criterion_name: criterion.name, value: 0 })),
              },
            ])
          }
        >
          Добавить
        </button>
      </div>
      <div className="table-wrap wide">
        <table>
          <thead>
            <tr>
              <th>Альтернатива</th>
              {criteria.map((criterion) => (
                <th key={criterion.name}>{criterion.name}</th>
              ))}
              <th></th>
            </tr>
          </thead>
          <tbody>
            {prepared.map((alternative, alternativeIndex) => (
              <tr key={alternativeIndex}>
                <td>
                  <input
                    value={alternative.name}
                    onChange={(event) =>
                      onChange(
                        prepared.map((item, index) =>
                          index === alternativeIndex ? { ...item, name: event.target.value } : item,
                        ),
                      )
                    }
                  />
                </td>
                {criteria.map((criterion) => (
                  <td key={criterion.name}>
                    <input
                      type="number"
                      value={
                        alternative.values.find((value) => value.criterion_name === criterion.name)?.value ?? 0
                      }
                      onChange={(event) =>
                        updateValue(alternativeIndex, criterion.name, Number(event.target.value))
                      }
                    />
                  </td>
                ))}
                <td>
                  <button
                    type="button"
                    onClick={() => onChange(prepared.filter((_, index) => index !== alternativeIndex))}
                  >
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
