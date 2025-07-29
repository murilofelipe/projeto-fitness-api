# /backend/Dockerfile

# --- Estágio 1: Imagem Base e Dependências ---
FROM python:3.10-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# --- Estágio 2: Imagem Final ---
FROM base AS final

ARG UID=1000
ARG GID=999

RUN addgroup --gid ${GID} --system appgroup || true && \
    adduser --uid ${UID} --system --ingroup appgroup --no-create-home appuser

COPY --from=base /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .
RUN pip install -e .
RUN chown -R appuser:appgroup /code
USER appuser
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]