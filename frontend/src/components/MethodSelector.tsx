import type { OptimizationMethod } from "../types/optimization";

const methods: Array<{ value: OptimizationMethod; label: string }> = [
  { value: "weighted_sum", label: "Взвешенные коэффициенты" },
  { value: "pareto", label: "Парето" },
  { value: "topsis", label: "TOPSIS" },
];

interface Props {
  value: OptimizationMethod;
  onChange: (method: OptimizationMethod) => void;
}

export function MethodSelector({ value, onChange }: Props) {
  return (
    <div className="method-selector">
      {methods.map((method) => (
        <button
          className={value === method.value ? "active" : ""}
          key={method.value}
          onClick={() => onChange(method.value)}
          type="button"
        >
          {method.label}
        </button>
      ))}
    </div>
  );
}
