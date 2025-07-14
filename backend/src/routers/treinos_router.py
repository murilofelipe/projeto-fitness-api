from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/treinos", tags=["Treinos"])


# --- Endpoint de Criação (POST) ---
@router.post("/", response_model=schemas.TreinoResponse, status_code=201)
def criar_novo_treino(treino_data: schemas.TreinoCreate, db: Session = Depends(get_db)):
    """
    Endpoint para criar um novo registro de treino completo.
    """
    treino_criado = services.create_treino(db=db, treino_data=treino_data)
    return {
        "message": "Treino registrado com sucesso!",
        "id_treino": treino_criado.id_treino,
    }


# --- Endpoint de Listagem (GET) ---
@router.get("/", response_model=List[schemas.Treino])
def listar_treinos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Endpoint para listar todos os treinos registrados.
    """
    treinos = services.get_treinos(db, skip=skip, limit=limit)
    return treinos
