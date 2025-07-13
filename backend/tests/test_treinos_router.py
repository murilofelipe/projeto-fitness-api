# /backend/tests/test_treinos_router.py

from sqlalchemy.orm import Session
from src.models import Aluno, Exercicios, TreinoRealizado
from fastapi.testclient import TestClient

# Teste 1: Testando o GET em um banco de dados limpo
def test_listar_treinos_retorna_lista_vazia(client: TestClient):
    # A fixture 'client' já garante que o banco está limpo antes deste teste rodar.
    
    # ACT: Faz a requisição GET
    response = client.get("/treinos/")
    
    # ASSERT: Verifica se a resposta é 200 OK e a lista está vazia
    assert response.status_code == 200
    assert response.json() == []

# Teste 2: Testando o fluxo de POST
def test_criar_treino_com_sucesso(client: TestClient, db_session: Session):
    # ARRANGE: Usa a sessão fornecida pela fixture para preparar o banco
    aluno_teste = Aluno(id_usuario=1, nome="Aluno Teste", email="aluno.teste@email.com", senha_hash="hash123", tipo_usuario="aluno")
    exercicio_teste = Exercicios(id_exercicio=1, nome_exercicio="Teste de Supino", grupo_muscular="Peitoral")
    db_session.add(aluno_teste)
    db_session.add(exercicio_teste)
    db_session.commit()
    
    payload_do_treino = {
        "id_usuario": 1,
        "data_treino": "2025-07-15",
        "exercicios": [{"id_exercicio": 1, "series": [{"numero_serie": 1, "repeticoes": 10, "carga_kg": 50}]}]
    }
    
    # ACT: Faz a requisição POST
    response_post = client.post("/treinos/", json=payload_do_treino)
    
    # ASSERT
    assert response_post.status_code == 201
    assert "id_treino" in response_post.json()

    # Verifica se o dado foi realmente salvo no banco
    assert db_session.query(TreinoRealizado).count() == 1