from app.algorithms.pareto import calculate_pareto


def test_pareto_marks_non_dominated_alternatives():
    result = calculate_pareto(
        alternatives=["A1", "A2", "A3"],
        criteria=["cost", "quality"],
        matrix=[[100, 8], [120, 7], [90, 9]],
        weights=[0.5, 0.5],
        criterion_types=["min", "max"],
    )

    flags = {item["alternative_name"]: item["is_pareto_optimal"] for item in result}
    assert flags["A3"] is True
    assert flags["A1"] is False
    assert flags["A2"] is False
