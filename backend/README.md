# Backend

FastAPI-сервис для учебного программного комплекса многокритериальной оптимизации.

## Локальный запуск

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

По умолчанию API ожидает PostgreSQL по адресу из `DATABASE_URL`.

## Тесты

```bash
pytest
```

## Методы

- `weighted_sum` — min-max нормализация с учётом направления критерия и взвешенная сумма.
- `pareto` — поиск недоминируемых альтернатив.
- `topsis` — векторная нормализация, веса, идеальное и антиидеальное решения.
