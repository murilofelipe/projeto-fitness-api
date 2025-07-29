from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/performance/{aluno_id}", response_model=schemas.AnalyticsResponse)
def get_performance_data(
    aluno_id: int, exercicio_id: Optional[int] = None, db: Session = Depends(get_db)
):
    """
    Endpoint para buscar os dados de performance de um aluno específico,
    agregados por dia a partir do Data Warehouse. Pode ser filtrado por exercício.
    """
    dados_agregados = services.get_aluno_performance(
        db=db, aluno_id=aluno_id, exercicio_id=exercicio_id
    )

    if not dados_agregados:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado de performance encontrado para o aluno com ID {aluno_id}.",  # noqa: E501
        )

    # Converte cada 'Row' do resultado da consulta para um dicionário
    # antes de passá-lo para a validação do Pydantic.
    performance_list = [
        schemas.DailyPerformanceData.model_validate(linha._asdict())
        for linha in dados_agregados
    ]

    # Pega o nome do aluno do primeiro registro (será o mesmo para todos)
    nome_aluno_encontrado = dados_agregados[0].nome_aluno

    return schemas.AnalyticsResponse(
        id_aluno=aluno_id,
        nome_aluno=nome_aluno_encontrado,
        performance=performance_list,
    )


@router.get("/frequencia/{aluno_id}", response_model=schemas.FrequenciaResponse)
def get_frequencia_data(
    aluno_id: int, periodo: str = "mensal", db: Session = Depends(get_db)
):
    """
    Endpoint para buscar os dados de frequência de treino de um aluno,
    já agregados por período (semanal, mensal, anual).
    """
    dados = services.get_frequencia_treinos(db=db, aluno_id=aluno_id, periodo=periodo)

    return schemas.FrequenciaResponse(aluno_id=aluno_id, dados_frequencia=dados)
