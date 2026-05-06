# Программный комплекс многокритериальной оптимизации

Учебный проект для ВКР: клиент-серверное веб-приложение, где пользователь создаёт задачу, задаёт критерии, альтернативы и значения, запускает методы оптимизации и смотрит результаты в таблицах и графиках.

## Стек

- Backend: Python, FastAPI, SQLAlchemy, Pydantic, PostgreSQL, Alembic, NumPy, Pandas, Uvicorn.
- Frontend: React, TypeScript, Vite, Axios, Plotly.
- Инфраструктура: Docker Compose.

## Запуск через Docker Compose

1. Запустите Docker Desktop и дождитесь статуса `Docker Desktop is running`.
2. Откройте PowerShell.
3. Перейдите в папку проекта:

```powershell
cd C:\Users\Username\source\repos\VKR_Moor
```

4. Проверьте, что Docker отвечает:

```powershell
docker --version
docker compose version
docker info
```

5. Соберите и запустите контейнеры:

```bash
docker compose up --build
```

Если нужно запустить в фоне:

```powershell
docker compose up --build -d
```

После запуска:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- PostgreSQL: `localhost:5432`

Полезные команды:

```powershell
# посмотреть состояние контейнеров
docker compose ps

# посмотреть логи всех сервисов
docker compose logs -f

# посмотреть только backend
docker compose logs -f backend

# остановить контейнеры
docker compose down

# остановить и удалить данные PostgreSQL
docker compose down -v
```

## Проверка после запуска

1. Откройте `http://localhost:8000/docs`.
2. Убедитесь, что Swagger показывает endpoints `/api/tasks`, `/api/tasks/{task_id}/optimize`, `/api/tasks/{task_id}/compare`.
3. Откройте `http://localhost:5173`.
4. На странице редактора нажмите `Рассчитать`.
5. Должна открыться страница результата с таблицей ранжирования и графиками.
6. Вернитесь в `История` и проверьте, что запуск сохранился.

## Возможности проекта

- создание и редактирование задачи оптимизации;
- добавление критериев `min/max` с весами;
- добавление альтернатив и матрицы значений;
- автоматическая нормализация весов на backend;
- запуск методов `weighted_sum`, `pareto`, `topsis`;
- сравнение всех методов;
- сохранение запусков и результатов в PostgreSQL;
- просмотр истории запусков;
- таблица ранжирования, bar chart score, график Парето для двух критериев.

## Основные API endpoints

- `POST /api/tasks`
- `GET /api/tasks`
- `GET /api/tasks/{task_id}`
- `PUT /api/tasks/{task_id}`
- `DELETE /api/tasks/{task_id}`
- `POST /api/tasks/{task_id}/optimize`
- `POST /api/tasks/{task_id}/compare`
- `GET /api/tasks/{task_id}/runs`
- `GET /api/runs/{run_id}`

## Проверка backend

```bash
cd backend
pytest
```
