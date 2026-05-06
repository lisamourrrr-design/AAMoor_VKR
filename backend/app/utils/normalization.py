import numpy as np


def normalize_weights(weights: list[float]) -> np.ndarray:
    weights_array = np.asarray(weights, dtype=float)
    if np.any(weights_array < 0):
        raise ValueError("Веса критериев должны быть неотрицательными")

    total = weights_array.sum()
    if total <= 0:
        raise ValueError("Сумма весов должна быть больше нуля")

    return weights_array / total


def min_max_normalize(values: np.ndarray, criterion_types: list[str]) -> np.ndarray:
    matrix = np.asarray(values, dtype=float)
    result = np.zeros_like(matrix, dtype=float)

    for column_index, criterion_type in enumerate(criterion_types):
        column = matrix[:, column_index]
        minimum = column.min()
        maximum = column.max()

        if maximum == minimum:
            result[:, column_index] = 1.0
            continue

        if criterion_type == "max":
            result[:, column_index] = (column - minimum) / (maximum - minimum)
        elif criterion_type == "min":
            result[:, column_index] = (maximum - column) / (maximum - minimum)
        else:
            raise ValueError("Тип критерия должен быть 'min' или 'max'")

    return result
