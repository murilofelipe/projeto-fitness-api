# /backend/Dockerfile

# Use uma imagem base oficial do Python
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de dependências primeiro (para otimizar o cache do Docker)
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o resto do código da sua aplicação para o diretório de trabalho
COPY . .

# O comando para iniciar a aplicação (será sobrescrito pelo docker-compose, mas é uma boa prática)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]