# /backend/src/routers/alunos_router.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/alunos", tags=["Alunos"])


@router.get("/", response_model=List[schemas.AlunoSimples])
def listar_todos_alunos(db: Session = Depends(get_db)):
    return services.get_alunos(db=db)


@router.get("/{aluno_id}/summary", response_model=schemas.AlunoSummary)
def get_aluno_summary_data(aluno_id: int, db: Session = Depends(get_db)):
    summary_data = services.get_aluno_summary(db=db, aluno_id=aluno_id)
    if not summary_data:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    return {
        "nome": summary_data["aluno"].nome,
        "ultimo_login": summary_data["aluno"].ultimo_login,
        "ultimo_treino": summary_data["ultimo_treino"],
    }


@router.get("/{aluno_id}/exercicios", response_model=List[schemas.ExercicioSimples])
def listar_exercicios_do_aluno(aluno_id: int, db: Session = Depends(get_db)):
    """Lista todos os exercícios únicos que um aluno já realizou."""
    exercicios = services.get_exercicios_by_aluno(db=db, aluno_id=aluno_id)
    if not exercicios:
        return []
    return exercicios
