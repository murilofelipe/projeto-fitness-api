# /backend/scripts/etl_pipeline.py

import os
import sys

import pandas as pd
from sqlalchemy import create_engine, text, types

# Garante que o script encontre o pacote 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def extract(engine) -> pd.DataFrame | None:
    """Extrai dados do banco OLTP e retorna um DataFrame."""
    print("Iniciando a etapa de Extração...")
    query = """
    SELECT
        sr.id_treino, tr.data_treino, u.id_usuario, u.nome AS nome_usuario,
        u.email AS email_usuario, ex.id_exercicio, ex.nome_exercicio,
        ex.grupo_muscular, sr.numero_serie, sr.repeticoes, sr.carga_kg
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
    """Transforma o DataFrame extraído, criando as dimensões e a tabela fato."""
    if df is None or df.empty:
        return None
    print("Iniciando a etapa de Transformação...")

    df["data_treino"] = pd.to_datetime(df["data_treino"])

    dim_tempo = (
        df[["data_treino"]].drop_duplicates().rename(columns={"data_treino": "id_data"})
    )
    dim_tempo["ano"] = dim_tempo["id_data"].dt.year
    dim_tempo["mes"] = dim_tempo["id_data"].dt.month
    dim_tempo["dia"] = dim_tempo["id_data"].dt.day
    dim_tempo["dia_da_semana"] = dim_tempo["id_data"].dt.day_name()

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
        "fct_treinos": fct_treinos,
    }


def load(dataframes: dict, engine):
    """Carrega os dataframes no Data Warehouse na ordem correta."""
    if dataframes is None:
        return
    print("Iniciando a carga de dados no Data Warehouse...")

    # Define os tipos de dados para o SQLAlchemy, resolvendo o problema do SQLite
    dtype_map = {
        "id_data": types.Date,
        "maior_carga_kg": types.DECIMAL(6, 2),
        "volume_total_carga": types.DECIMAL(10, 2),
    }
    # A ordem importa para respeitar as chaves estrangeiras
    tabelas_para_carregar = ["dim_tempo", "dim_aluno", "dim_exercicio", "fct_treinos"]

    for tabela in tabelas_para_carregar:
        df = dataframes[tabela]
        print(f"Carregando dados na tabela DWH: '{tabela}'...")
        try:
            # Usamos if_exists='append' pois a limpeza é feita antes
            df.to_sql(tabela, engine, if_exists="append", index=False, dtype=dtype_map)
            print(f"Carga de dados na tabela '{tabela}' concluída com sucesso.")
        except Exception as e:
            print(f"Erro ao carregar dados na tabela '{tabela}': {e}")
            raise


def truncate_dwh_tables(engine):
    """Limpa as tabelas do DWH na ordem correta para evitar erros de FK."""
    print("Iniciando limpeza das tabelas do Data Warehouse...")
    try:
        with engine.connect() as connection:
            transaction = connection.begin()
            connection.execute(
                text("TRUNCATE TABLE fct_treinos RESTART IDENTITY CASCADE;")
            )
            connection.execute(
                text("TRUNCATE TABLE dim_tempo RESTART IDENTITY CASCADE;")
            )
            connection.execute(
                text("TRUNCATE TABLE dim_aluno RESTART IDENTITY CASCADE;")
            )
            connection.execute(
                text("TRUNCATE TABLE dim_exercicio RESTART IDENTITY CASCADE;")
            )
            transaction.commit()
            print("Tabelas do DWH limpas com sucesso.")
    except Exception as e:
        # O TRUNCATE não funciona no SQLite, então ignoramos o erro no ambiente de teste
        print(f"Aviso ao limpar tabelas (esperado em SQLite): {e}")


if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("Erro: A variável de ambiente DATABASE_URL não está configurada.")
    else:
        engine = create_engine(db_url)
        df_extraido = extract(engine=engine)

        if df_extraido is not None and not df_extraido.empty:
            dataframes_processados = transform(df_extraido)
            truncate_dwh_tables(engine)
            load(dataframes_processados, engine)
            print("\nProcesso de ETL concluído com sucesso!")
