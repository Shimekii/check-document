FROM python:3.12-slim-trixie

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

COPY pyproject.toml uv.lock pytest.ini ./

RUN uv sync

COPY ./src ./src

ENTRYPOINT [".venv/bin/pytest", "--cov=app", "--cov-report=term-missing"]