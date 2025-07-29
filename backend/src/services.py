# /backend/src/services.py

from typing import Any, Dict, List, Optional

from sqlalchemy import func, literal_column
from sqlalchemy.orm import Query, Session

from . import models, schemas


# --- Funções do Roteador de Treinos (OLTP) ---
def create_treino(
    db: Session, treino_data: schemas.TreinoCreate
) -> models.TreinoRealizado:
    novo_treino = models.TreinoRealizado(
        id_usuario=treino_data.id_usuario,
        data_treino=treino_data.data_treino,
        status=treino_data.status,
    )
    db.add(novo_treino)
    db.commit()
    db.refresh(novo_treino)
    for exercicio in treino_data.exercicios:
        for serie in exercicio.series:
            nova_serie = models.SerieRealizada(
                id_treino=novo_treino.id_treino,
                id_exercicio=exercicio.id_exercicio,
                numero_serie=serie.numero_serie,
                repeticoes=serie.repeticoes,
                carga_kg=serie.carga_kg,
            )
            db.add(nova_serie)
    db.commit()
    return novo_treino


def get_treinos(
    db: Session, skip: int = 0, limit: int = 100
) -> List[models.TreinoRealizado]:
    return db.query(models.TreinoRealizado).offset(skip).limit(limit).all()


# --- Funções do Roteador de Alunos (OLTP & OLAP) ---
def get_alunos(db: Session) -> List[models.Aluno]:
    return db.query(models.Aluno).all()


def get_aluno_summary(db: Session, aluno_id: int):
    aluno = db.query(models.Aluno).filter(models.Aluno.id_usuario == aluno_id).first()
    if not aluno:
        return None
    ultimo_treino = (
        db.query(models.TreinoRealizado)
        .filter(models.TreinoRealizado.id_usuario == aluno_id)
        .order_by(models.TreinoRealizado.data_treino.desc())
        .first()
    )
    return {"aluno": aluno, "ultimo_treino": ultimo_treino}


def get_exercicios_by_aluno(db: Session, aluno_id: int) -> List[models.DimExercicio]:
    return (
        db.query(models.DimExercicio)
        .join(
            models.FctTreinos,
            models.DimExercicio.id_exercicio == models.FctTreinos.id_exercicio,
        )
        .filter(models.FctTreinos.id_aluno == aluno_id)
        .distinct()
        .all()
    )


# --- Funções do Roteador de Usuários (OLTP) ---
def update_user_photo(db: Session, user_id: int, photo_url: str):
    user = db.query(models.Usuario).filter(models.Usuario.id_usuario == user_id).first()
    if user:
        user.foto_perfil_url = photo_url
        db.commit()
        db.refresh(user)
    return user


def get_aluno_performance(
    db: Session, aluno_id: int, exercicio_id: Optional[int] = None
):
    """
    Busca os dados de performance de um aluno no DWH, AGREGADOS POR DIA.
    Se um exercicio_id for fornecido, a agregação será apenas para aquele exercício.
    """
    query: Query = (
        db.query(
            models.DimAluno.nome_aluno,
            models.FctTreinos.id_data.label("data_treino"),
            func.sum(models.FctTreinos.volume_total_carga).label("volume_total_diario"),
            func.max(models.FctTreinos.maior_carga_kg).label("maior_carga_diaria"),
        )
        .join(models.DimAluno, models.FctTreinos.id_aluno == models.DimAluno.id_aluno)
        .filter(
            models.FctTreinos.id_aluno == aluno_id,
            models.DimTreino.status
            == "executado",  # Garante que só performance executada seja mostrada
        )
        .join(
            models.DimTreino, models.FctTreinos.id_treino == models.DimTreino.id_treino
        )
    )

    if exercicio_id:
        query = query.filter(models.FctTreinos.id_exercicio == exercicio_id)

    query = query.group_by(
        models.DimAluno.nome_aluno, models.FctTreinos.id_data
    ).order_by(models.FctTreinos.id_data.asc())

    return query.all()


def get_frequencia_treinos(db: Session, aluno_id: int, periodo: str):
    """Busca e agrega a frequência de treinos de um aluno por período."""
    period_sql: str
    if periodo == "semanal":
        period_sql = "TO_CHAR(id_data, 'YYYY-\"W\"WW')"
    elif periodo == "mensal":
        period_sql = "TO_CHAR(id_data, 'YYYY-MM')"
    elif periodo == "anual":
        period_sql = "TO_CHAR(id_data, 'YYYY')"
    else:
        return []

    # Usamos literal_column para tratar a string SQL como uma coluna selecionável
    period_col: Any = literal_column(period_sql).label("periodo")

    query: Query = (
        db.query(
            period_col,
            func.count(func.distinct(models.FctTreinos.id_data)).label("quantidade"),
        )
        .select_from(models.FctTreinos)
        .filter(models.FctTreinos.id_aluno == aluno_id)
        .group_by(period_col)
        .order_by(period_col.asc())
    )
    return query.all()


def get_calendar_data(db: Session, aluno_id: int):
    """
    Busca todos os treinos (passados e futuros) de um aluno
    diretamente do banco de dados operacional (OLTP).
    """
    treinos = (
        db.query(models.TreinoRealizado)
        .filter(models.TreinoRealizado.id_usuario == aluno_id)
        .order_by(models.TreinoRealizado.data_treino.asc())
        .all()
    )

    # Agrupa os exercícios por data
    eventos: Dict[str, Dict[str, Any]] = {}

    for treino in treinos:
        date_key = treino.data_treino.isoformat()
        if date_key not in eventos:
            eventos[date_key] = {
                "data_treino": treino.data_treino,
                "status": treino.status,
                "exercicios": [],
            }

        for serie in treino.series:
            # Busca o nome do exercício (evita N+1 fazendo uma query só)
            exercicio = (
                db.query(models.Exercicios)
                .filter(models.Exercicios.id_exercicio == serie.id_exercicio)
                .first()
            )
            if (
                exercicio
                and exercicio.nome_exercicio not in eventos[date_key]["exercicios"]
            ):
                eventos[date_key]["exercicios"].append(exercicio.nome_exercicio)

    return list(eventos.values())
