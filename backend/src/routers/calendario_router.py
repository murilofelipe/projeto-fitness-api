# /backend/src/routers/calendario_router.py

# from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/calendario", tags=["Calendario"])


@router.get("/{aluno_id}", response_model=schemas.CalendarResponse)
def get_calendario_aluno(aluno_id: int, db: Session = Depends(get_db)):
    eventos = services.get_calendar_data(db=db, aluno_id=aluno_id)
    return {"eventos": eventos}
