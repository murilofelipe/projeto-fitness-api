# /backend/tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.database import Base, get_db
from src.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fixture para garantir que as tabelas sejam criadas e limpas para cada teste
@pytest.fixture(scope="function")
def db_session() -> Session:
    # Limpa dados de execuções anteriores
    Base.metadata.drop_all(bind=engine)
    # Cria as tabelas
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture que cria o cliente de API e sobrescreve a dependência do banco
@pytest.fixture(scope="function")
def client(db_session: Session):
    def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    del app.dependency_overrides[get_db]