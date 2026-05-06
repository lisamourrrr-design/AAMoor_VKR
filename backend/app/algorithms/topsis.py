import numpy as np

from app.utils.normalization import normalize_weights
from app.utils.validation import validate_optimization_input


def calculate_topsis(
    alternatives: list[str],
    criteria: list[str],
    matrix: list[list[float]],
    weights: list[float],
    criterion_types: list[str],
) -> list[dict]:
    validate_optimization_input(alternatives, criteria, matrix, weights, criterion_types)

    values = np.asarray(matrix, dtype=float)
    normalized_weights = normalize_weights(weights)
    denominator = np.sqrt((values**2).sum(axis=0))
    denominator[denominator == 0] = 1.0

    normalized_values = values / denominator
    weighted_values = normalized_values * normalized_weights

    ideal = np.zeros(len(criteria))
    anti_ideal = np.zeros(len(criteria))
    for column_index, criterion_type in enumerate(criterion_types):
        column = weighted_values[:, column_index]
        if criterion_type == "max":
            ideal[column_index] = column.max()
            anti_ideal[column_index] = column.min()
        else:
            ideal[column_index] = column.min()
            anti_ideal[column_index] = column.max()

    distance_to_ideal = np.sqrt(((weighted_values - ideal) ** 2).sum(axis=1))
    distance_to_anti_ideal = np.sqrt(((weighted_values - anti_ideal) ** 2).sum(axis=1))
    scores = distance_to_anti_ideal / (distance_to_ideal + distance_to_anti_ideal)
    scores = np.nan_to_num(scores, nan=0.0)

    ordered_indexes = np.argsort(-scores)
    results: list[dict] = []
    for rank, index in enumerate(ordered_indexes, start=1):
        results.append(
            {
                "alternative_index": int(index),
                "alternative_name": alternatives[index],
                "score": float(scores[index]),
                "rank": rank,
                "is_pareto_optimal": False,
                "details": {
                    "weighted_values": weighted_values[index].round(6).tolist(),
                    "distance_to_ideal": float(distance_to_ideal[index]),
                    "distance_to_anti_ideal": float(distance_to_anti_ideal[index]),
                },
            }
        )

    return results
