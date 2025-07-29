# /backend/scripts/init_db.py

import os
import sys

# IMPORTANTE: Importa o módulo de modelos para que o SQLAlchemy os "conheça"
from src import models  # noqa: F401

# Importa o Base e o engine do nosso módulo de banco de dados
from src.database import Base, engine

# Adiciona a pasta 'backend' ao path do Python para que possamos importar de 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def create_database_tables():
    """
    Cria todas as tabelas no banco de dados que herdam da nossa Base declarativa.
    """
    print("Iniciando a criação de todas as tabelas no banco de dados...")
    try:
        # O comando para criar todas as tabelas
        Base.metadata.create_all(bind=engine)
        print("Tabelas criadas com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao criar as tabelas: {e}")


if __name__ == "__main__":
    create_database_tables()
