# /backend/src/routers/analytics_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/performance/{aluno_id}", response_model=schemas.AnalyticsResponse)
def get_performance_data(aluno_id: int, db: Session = Depends(get_db)):
    """
    Endpoint para buscar os dados de performance de um aluno específico
    a partir do Data Warehouse.
    """
    dados_do_banco = services.get_aluno_performance(db=db, aluno_id=aluno_id)

    if not dados_do_banco:
        raise HTTPException(
            status_code=404,
            detail=f"Nenhum dado de performance encontrado para o aluno com ID {aluno_id}.",  # noqa: E501
        )

    # Agora, cada 'linha' no resultado tem os nomes das colunas que definimos na query
    nome_aluno_encontrado = dados_do_banco[0].nome_aluno

    # Usamos uma list comprehension para montar a lista de forma mais eficiente
    performance_list = [
        schemas.PerformanceData.from_orm(linha) for linha in dados_do_banco
    ]

    return schemas.AnalyticsResponse(
        id_aluno=aluno_id,
        nome_aluno=nome_aluno_encontrado,
        performance=performance_list,
    )
