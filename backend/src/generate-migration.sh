echo "Generating migrations"

alembic revision --autogenerate

echo "Apply migrations"

alembic upgrade head