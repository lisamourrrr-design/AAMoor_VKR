from app.algorithms.topsis import calculate_topsis


def test_topsis_returns_scores_between_zero_and_one():
    result = calculate_topsis(
        alternatives=["A1", "A2", "A3"],
        criteria=["cost", "quality", "time"],
        matrix=[[120, 8, 5], [100, 7, 4], [140, 9, 6]],
        weights=[0.4, 0.4, 0.2],
        criterion_types=["min", "max", "min"],
    )

    assert result[0]["rank"] == 1
    assert all(0 <= item["score"] <= 1 for item in result)
    assert result[0]["score"] >= result[-1]["score"]
