import numpy as np

from app.utils.normalization import min_max_normalize, normalize_weights
from app.utils.validation import validate_optimization_input


def calculate_weighted_sum(
    alternatives: list[str],
    criteria: list[str],
    matrix: list[list[float]],
    weights: list[float],
    criterion_types: list[str],
) -> list[dict]:
    validate_optimization_input(alternatives, criteria, matrix, weights, criterion_types)

    values = np.asarray(matrix, dtype=float)
    normalized_weights = normalize_weights(weights)
    normalized_values = min_max_normalize(values, criterion_types)
    scores = normalized_values @ normalized_weights

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
                    "normalized_values": normalized_values[index].round(6).tolist(),
                    "normalized_weights": normalized_weights.round(6).tolist(),
                },
            }
        )

    return results
