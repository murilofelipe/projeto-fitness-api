import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Pega a URL do banco a partir da variável de ambiente do docker-compose
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Função para obter a sessão do banco de dados, que será usada pelos endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
