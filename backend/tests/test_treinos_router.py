# /backend/tests/test_treinos_router.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models import Aluno, Exercicios, TreinoRealizado


def test_criar_treino_com_sucesso(client: TestClient, db_session: Session):
    # ARRANGE
    aluno_teste = Aluno(
        id_usuario=1,
        nome="Aluno Teste",
        email="aluno.teste@email.com",
        senha_hash="hash123",
        tipo_usuario="aluno",
    )
    exercicio_teste = Exercicios(
        id_exercicio=1, nome_exercicio="Teste de Supino", grupo_muscular="Peitoral"
    )
    db_session.add(aluno_teste)
    db_session.add(exercicio_teste)
    db_session.commit()

    payload = {
        "id_usuario": 1,
        "data_treino": "2025-07-15",
        "exercicios": [
            {
                "id_exercicio": 1,
                "series": [{"numero_serie": 1, "repeticoes": 10, "carga_kg": 50}],
            }
        ],
    }

    # ACT
    response = client.post("/treinos/", json=payload)

    # ASSERT
    assert response.status_code == 201
    assert db_session.query(TreinoRealizado).count() == 1


def test_listar_treinos_retorna_lista_vazia(client: TestClient):
    # O banco já está limpo graças à fixture que rodou antes deste teste
    response = client.get("/treinos/")
    assert response.status_code == 200
    assert response.json() == []
