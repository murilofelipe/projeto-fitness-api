from sqlalchemy.orm import Session, selectinload

from . import models, schemas


def create_treino(db: Session, treino_data: schemas.TreinoCreate):
    # 1. Cria o "cabeçalho" do treino
    novo_treino = models.TreinoRealizado(
        id_usuario=treino_data.id_usuario, data_treino=treino_data.data_treino
    )
    db.add(novo_treino)
    db.commit()
    db.refresh(novo_treino)  # Pega o ID do treino que acabou de ser criado

    # 2. Itera sobre cada exercício e suas séries para salvá-los
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


def get_treinos(db: Session, skip: int = 0, limit: int = 100):
    """
    Função para buscar uma lista de treinos do banco de dados com paginação,
    já carregando as séries relacionadas para evitar consultas extras (eager loading).
    """
    return (
        db.query(models.TreinoRealizado)
        .options(selectinload(models.TreinoRealizado.series))
        .offset(skip)
        .limit(limit)
        .all()
    )
