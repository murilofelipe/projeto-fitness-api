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
RUN addgroup --system appgroup && adduser --system --group appuser
COPY --from=base /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . .
RUN pip install -e .
RUN chown -R appuser:appgroup /code
USER appuser
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]