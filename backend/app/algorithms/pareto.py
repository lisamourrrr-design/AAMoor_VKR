import numpy as np

from app.utils.validation import validate_optimization_input


def _dominates(first: np.ndarray, second: np.ndarray, criterion_types: list[str]) -> bool:
    """Проверка доминирования: не хуже по всем критериям и лучше хотя бы по одному."""
    comparisons = []
    strict_improvements = []

    for left, right, criterion_type in zip(first, second, criterion_types):
        if criterion_type == "max":
            comparisons.append(left >= right)
            strict_improvements.append(left > right)
        else:
            comparisons.append(left <= right)
            strict_improvements.append(left < right)

    return all(comparisons) and any(strict_improvements)


def calculate_pareto(
    alternatives: list[str],
    criteria: list[str],
    matrix: list[list[float]],
    weights: list[float],
    criterion_types: list[str],
) -> list[dict]:
    validate_optimization_input(alternatives, criteria, matrix, weights, criterion_types)

    values = np.asarray(matrix, dtype=float)
    is_optimal = np.ones(len(alternatives), dtype=bool)

    for candidate_index, candidate in enumerate(values):
        for other_index, other in enumerate(values):
            if candidate_index == other_index:
                continue
            if _dominates(other, candidate, criterion_types):
                is_optimal[candidate_index] = False
                break

    # Для Парето score учебно трактуем как 1/0, чтобы можно было строить общий график.
    scores = is_optimal.astype(float)
    ordered_indexes = np.argsort(-scores)
    results: list[dict] = []
    for rank, index in enumerate(ordered_indexes, start=1):
        results.append(
            {
                "alternative_index": int(index),
                "alternative_name": alternatives[index],
                "score": float(scores[index]),
                "rank": rank,
                "is_pareto_optimal": bool(is_optimal[index]),
                "details": {"values": values[index].tolist()},
            }
        )

    return results
