from app.algorithms.weighted_sum import calculate_weighted_sum


def test_weighted_sum_ranks_best_normalized_alternative():
    result = calculate_weighted_sum(
        alternatives=["A1", "A2", "A3"],
        criteria=["cost", "quality"],
        matrix=[[100, 7], [120, 9], [90, 6]],
        weights=[0.3, 0.7],
        criterion_types=["min", "max"],
    )

    assert result[0]["alternative_name"] == "A2"
    assert result[0]["rank"] == 1
    assert result[0]["score"] > result[-1]["score"]


def test_weighted_sum_normalizes_weights():
    result = calculate_weighted_sum(
        alternatives=["A1", "A2"],
        criteria=["cost", "quality"],
        matrix=[[100, 7], [120, 9]],
        weights=[2, 2],
        criterion_types=["min", "max"],
    )

    assert result[0]["details"]["normalized_weights"] == [0.5, 0.5]
