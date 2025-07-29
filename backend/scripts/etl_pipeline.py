import os
import sys
from datetime import date

import pandas as pd
from sqlalchemy import create_engine, text

# Garante que o script encontre o pacote 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def extract(engine) -> pd.DataFrame | None:
    """
    Extrai dados do banco OLTP, unindo tabelas para criar uma base única com todos os status. # noqa: E501
    """
    print("Iniciando a etapa de Extração (todos os status)...")
    query = """
    SELECT
        tr.id_treino,
        tr.data_treino,
        tr.status,
        u.id_usuario,
        u.nome AS nome_usuario,
        u.email AS email_usuario,
        ex.id_exercicio,
        ex.nome_exercicio,
        ex.grupo_muscular,
        sr.numero_serie,
        sr.repeticoes,
        sr.carga_kg
    FROM series_realizadas sr
    JOIN treinos_realizados tr ON sr.id_treino = tr.id_treino
    JOIN usuarios u ON tr.id_usuario = u.id_usuario
    JOIN exercicios ex ON sr.id_exercicio = ex.id_exercicio;
    """
    try:
        with engine.connect() as connection:
            df = pd.read_sql_query(query, connection)
            print(f"Extração concluída. {len(df)} registros de séries encontrados.")
            return df
    except Exception as e:
        print(f"Erro durante a extração: {e}")
        return None


def transform(df: pd.DataFrame):
    """
    Transforma o DataFrame, aplicando a regra de negócio para status de treinos
    e criando as dimensões e a tabela fato.
    """
    if df is None or df.empty:
        print("DataFrame de entrada vazio. A transformação não pode continuar.")
        return None
    print("Iniciando a etapa de Transformação...")

    # --- APLICAÇÃO DA REGRA DE NEGÓCIO DE STATUS ---
    hoje = pd.to_datetime(date.today()).date()
    df["data_treino"] = pd.to_datetime(df["data_treino"]).dt.date

    condicao = (df["data_treino"] < hoje) & (df["status"] == "planejado")
    df.loc[condicao, "status"] = "nao_executado"
    print(
        f"{condicao.sum()} treinos planejados no passado foram atualizados para 'nao_executado'."  # noqa: E501
    )
    # --------------------------------------------------

    dim_tempo = (
        df[["data_treino"]].drop_duplicates().rename(columns={"data_treino": "id_data"})
    )
    dim_tempo["ano"] = pd.to_datetime(dim_tempo["id_data"]).dt.year
    dim_tempo["mes"] = pd.to_datetime(dim_tempo["id_data"]).dt.month
    dim_tempo["dia"] = pd.to_datetime(dim_tempo["id_data"]).dt.day
    dim_tempo["dia_da_semana"] = pd.to_datetime(dim_tempo["id_data"]).dt.day_name()

    dim_aluno = (
        df[["id_usuario", "nome_usuario", "email_usuario"]]
        .drop_duplicates()
        .rename(
            columns={
                "id_usuario": "id_aluno",
                "nome_usuario": "nome_aluno",
                "email_usuario": "email",
            }
        )
    )
    dim_exercicio = df[
        ["id_exercicio", "nome_exercicio", "grupo_muscular"]
    ].drop_duplicates()
    dim_treino = df[["id_treino", "status"]].drop_duplicates()

    df["volume_total_carga"] = df["repeticoes"] * df["carga_kg"]
    fct_treinos = (
        df.groupby(["id_treino", "data_treino", "id_usuario", "id_exercicio"])
        .agg(
            total_series=("numero_serie", "count"),
            total_repeticoes=("repeticoes", "sum"),
            maior_carga_kg=("carga_kg", "max"),
            volume_total_carga=("volume_total_carga", "sum"),
        )
        .reset_index()
        .rename(columns={"data_treino": "id_data", "id_usuario": "id_aluno"})
    )

    print("Transformação concluída.")
    return {
        "dim_tempo": dim_tempo,
        "dim_aluno": dim_aluno,
        "dim_exercicio": dim_exercicio,
        "dim_treino": dim_treino,
        "fct_treinos": fct_treinos,
    }


def load(dataframes: dict, engine):
    """Carrega os dataframes no Data Warehouse na ordem correta."""
    if dataframes is None:
        return
    print("Iniciando a carga de dados no Data Warehouse...")
    try:
        dataframes["dim_tempo"].to_sql(
            "dim_tempo", engine, if_exists="append", index=False
        )
        dataframes["dim_aluno"].to_sql(
            "dim_aluno", engine, if_exists="append", index=False
        )
        dataframes["dim_exercicio"].to_sql(
            "dim_exercicio", engine, if_exists="append", index=False
        )
        dataframes["dim_treino"].to_sql(
            "dim_treino", engine, if_exists="append", index=False
        )
        dataframes["fct_treinos"].to_sql(
            "fct_treinos", engine, if_exists="append", index=False
        )
        print("Carga de dados no DWH concluída com sucesso.")
    except Exception as e:
        print(f"Erro ao carregar dados no DWH: {e}")
        raise


def truncate_dwh_tables(engine):
    """Limpa as tabelas do DWH na ordem correta para evitar erros de FK."""
    print("Iniciando limpeza das tabelas do Data Warehouse...")
    tables_to_truncate = [
        "fct_treinos",
        "dim_treino",
        "dim_tempo",
        "dim_aluno",
        "dim_exercicio",
    ]
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            for table in tables_to_truncate:
                print(f"Limpando tabela: {table}...")
                connection.execute(
                    text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")
                )
            transaction.commit()
            print("Tabelas do DWH limpas com sucesso.")
    except Exception as e:
        print(
            f"Aviso ao limpar tabelas (esperado em SQLite, onde TRUNCATE não é padrão): {e}"  # noqa: E501
        )


if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Erro: A variável de ambiente DATABASE_URL não está configurada.")
    else:
        engine = create_engine(db_url)

        df_extraido = extract(engine=engine)

        if df_extraido is not None and not df_extraido.empty:
            dataframes_processados = transform(df_extraido)
            if dataframes_processados:
                truncate_dwh_tables(engine)
                load(dataframes_processados, engine)
                print("\nProcesso de ETL concluído com sucesso!")
