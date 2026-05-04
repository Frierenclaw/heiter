FROM ghcr.io/astral-sh/uv:python3.14-trixie

WORKDIR /app
ENV UV_NO_DEV=1

RUN groupadd --system --gid 999 heiter \
 && useradd --system --gid 999 --uid 999 --create-home heiter

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked

COPY . /app
RUN chown -R heiter:heiter /app

USER heiter

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]