"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-05-03
"""
from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "optimization_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "criteria",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("optimization_tasks.id")),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.String(length=3), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False),
        sa.CheckConstraint("type in ('min', 'max')", name="ck_criteria_type"),
        sa.CheckConstraint("weight >= 0", name="ck_criteria_weight_non_negative"),
    )
    op.create_table(
        "alternatives",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("optimization_tasks.id")),
        sa.Column("name", sa.String(length=255), nullable=False),
    )
    op.create_table(
        "alternative_values",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("alternative_id", sa.Integer(), sa.ForeignKey("alternatives.id")),
        sa.Column("criterion_id", sa.Integer(), sa.ForeignKey("criteria.id")),
        sa.Column("value", sa.Float(), nullable=False),
        sa.UniqueConstraint(
            "alternative_id", "criterion_id", name="uq_alternative_criterion_value"
        ),
    )
    op.create_table(
        "optimization_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("optimization_tasks.id")),
        sa.Column("method", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("execution_time_ms", sa.Float(), nullable=False),
    )
    op.create_table(
        "optimization_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("optimization_runs.id")),
        sa.Column("alternative_id", sa.Integer(), sa.ForeignKey("alternatives.id")),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("is_pareto_optimal", sa.Boolean(), nullable=False),
        sa.Column("details_json", sa.JSON(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("optimization_results")
    op.drop_table("optimization_runs")
    op.drop_table("alternative_values")
    op.drop_table("alternatives")
    op.drop_table("criteria")
    op.drop_table("optimization_tasks")
