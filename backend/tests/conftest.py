# /backend/tests/conftest.py

from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.database import Base, get_db
from src.main import app

# --- Configuração do Banco de Dados de Teste ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Fixture principal que gerencia o ciclo de vida do banco para os testes
@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    # Antes de cada teste, apaga e recria todas as tabelas
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        # Fornece a sessão para o teste
        yield db
    finally:
        # Fecha a sessão após o teste
        db.close()


# Fixture que cria um cliente de API para fazer as requisições
@pytest.fixture(scope="function")
def client(db_session: Session):
    # Função para sobrescrever a dependência get_db da aplicação
    def override_get_db():
        yield db_session

    # Aplica a sobrescrita
    app.dependency_overrides[get_db] = override_get_db

    # Retorna o cliente de teste
    yield TestClient(app)

    # Limpa a sobrescrita após o teste
    del app.dependency_overrides[get_db]
