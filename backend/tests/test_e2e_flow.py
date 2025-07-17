# /backend/tests/test_e2e_flow.py

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from scripts.etl_pipeline import extract, load, transform
from src.models import (
    Aluno,
    Exercicios,
)

from .conftest import engine  # Usamos o engine de teste do conftest


def test_fluxo_completo_ponta_a_ponta(client: TestClient, db_session: Session):
    """
    Testa o fluxo completo:
    1. Cria dados de base (aluno, exercício).
    2. Cria um treino no OLTP via API.
    3. Roda o processo de ETL.
    4. Verifica os dados no DWH via API de analytics.
    """
    # 1. ARRANGE: Cria os dados de base e o treino inicial
    aluno_e2e = Aluno(
        id_usuario=99,
        nome="Aluno E2E",
        email="e2e@teste.com",
        senha_hash="hash123",
        tipo_usuario="aluno",
    )
    exercicio_e2e = Exercicios(
        id_exercicio=99, nome_exercicio="Teste Ponta a Ponta", grupo_muscular="Testes"
    )
    db_session.add(aluno_e2e)
    db_session.add(exercicio_e2e)
    db_session.commit()

    payload_treino = {
        "id_usuario": 99,
        "data_treino": "2025-07-20",
        "exercicios": [
            {
                "id_exercicio": 99,
                "series": [{"numero_serie": 1, "repeticoes": 5, "carga_kg": 100}],
            }
        ],
    }
    response_post = client.post("/treinos/", json=payload_treino)
    assert response_post.status_code == 201

    # 2. ACT: Executa o processo de ETL
    df_extraido = extract(engine=engine)
    dataframes_processados = transform(df_extraido)

    # Chamamos a função load com a nova assinatura, passando o dicionário de dataframes
    load(dataframes_processados, engine)

    # 3. ASSERT: Verifica os dados no DWH através da API de analytics
    response_get = client.get("/analytics/performance/99")

    assert response_get.status_code == 200
    data = response_get.json()
    assert data["id_aluno"] == 99
    assert len(data["performance"]) == 1
    assert data["performance"][0]["volume_total_carga"] == 500.0
