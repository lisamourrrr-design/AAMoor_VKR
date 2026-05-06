from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.history_routes import router as history_router
from app.api.optimization_routes import router as optimization_router
from app.api.task_routes import router as task_router

app = FastAPI(
    title="Multi-Criteria Optimization API",
    description="Учебный API для решения задач многокритериальной оптимизации",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task_router)
app.include_router(optimization_router)
app.include_router(history_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
