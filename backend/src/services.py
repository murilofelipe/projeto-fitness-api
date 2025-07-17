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


def get_aluno_performance(db: Session, aluno_id: int):
    """
    Busca os dados de performance de um aluno no Data Warehouse,
    unindo a tabela fato com as dimensões e retornando colunas específicas.
    """
    query = (
        db.query(
            models.DimAluno.nome_aluno,
            models.FctTreinos.id_data.label("data_treino"),
            models.DimExercicio.nome_exercicio,
            models.DimExercicio.grupo_muscular,
            models.FctTreinos.total_series,
            models.FctTreinos.total_repeticoes,
            models.FctTreinos.maior_carga_kg,
            models.FctTreinos.volume_total_carga,
        )
        .join(models.DimAluno, models.FctTreinos.id_aluno == models.DimAluno.id_aluno)
        .join(
            models.DimExercicio,
            models.FctTreinos.id_exercicio == models.DimExercicio.id_exercicio,
        )
        .filter(models.FctTreinos.id_aluno == aluno_id)
    )

    return query.all()
