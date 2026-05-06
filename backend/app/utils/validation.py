import numpy as np


def validate_optimization_input(
    alternatives: list[str],
    criteria: list[str],
    matrix: list[list[float]],
    weights: list[float],
    criterion_types: list[str],
) -> None:
    if not alternatives:
        raise ValueError("Нужна хотя бы одна альтернатива")
    if not criteria:
        raise ValueError("Нужен хотя бы один критерий")
    if len(weights) != len(criteria):
        raise ValueError("Количество весов должно совпадать с количеством критериев")
    if len(criterion_types) != len(criteria):
        raise ValueError("Количество типов должно совпадать с количеством критериев")
    if any(weight < 0 for weight in weights):
        raise ValueError("Веса критериев должны быть неотрицательными")
    if any(criterion_type not in {"min", "max"} for criterion_type in criterion_types):
        raise ValueError("Тип критерия должен быть 'min' или 'max'")
    if len(matrix) != len(alternatives):
        raise ValueError("У каждой альтернативы должна быть строка значений")
    if any(len(row) != len(criteria) for row in matrix):
        raise ValueError("У каждой альтернативы должны быть значения по всем критериям")

    try:
        numeric_matrix = np.asarray(matrix, dtype=float)
    except ValueError as exc:
        raise ValueError("Значения критериев должны быть числовыми") from exc

    if not np.isfinite(numeric_matrix).all():
        raise ValueError("Значения критериев должны быть конечными числами")
