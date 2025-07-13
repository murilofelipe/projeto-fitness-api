# /backend/scripts/init_db.py

import sys
import os
from sqlalchemy import create_engine

# Adiciona o diretório 'backend' ao path do Python
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database import Base
from src import models

# Pega a URL do banco da variável de ambiente (que aponta para o host 'db' dentro do Docker)
# ou usa 'localhost' como padrão se a variável não existir (para rodar o script fora do contêiner)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/fitness_db")

def create_database_tables():
    # Usamos a URL obtida para criar o engine de conexão
    engine = create_engine(DATABASE_URL)
    
    # Imprime uma mensagem útil para sabermos onde está tentando conectar
    print(f"Tentando criar tabelas no banco de dados em: {engine.url.host}")
    
    try:
        # O comando para criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao conectar ou criar as tabelas: {e}")

if __name__ == "__main__":
    create_database_tables()