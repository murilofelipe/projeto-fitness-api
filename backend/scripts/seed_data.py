import os
import random
from datetime import date, timedelta

import requests
from sqlalchemy import create_engine, text

# --- CONFIGURAÇÃO DO BANCO ---
# URL para acesso da sua máquina local ao contêiner Docker
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/fitness_db"
)
engine = create_engine(DATABASE_URL)

# --- DADOS INICIAIS ---
USUARIOS_INICIAIS = [
    {
        "id_usuario": 1,
        "nome": "Bruno Alves",
        "email": "bruno@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "aluno",
        "data_nascimento": "1995-04-10",
    },
    {
        "id_usuario": 2,
        "nome": "Carla Medeiros",
        "email": "carla@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "profissional",
        "data_nascimento": "1988-08-20",
    },
    {
        "id_usuario": 3,
        "nome": "Mariana Costa",
        "email": "mariana@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "aluno",
        "data_nascimento": "2000-01-15",
    },
    {
        "id_usuario": 4,
        "nome": "Ricardo Mendes",
        "email": "ricardo@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "profissional",
        "data_nascimento": "1976-11-05",
    },
    {
        "id_usuario": 5,
        "nome": "Fernanda Lima",
        "email": "fernanda@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "profissional",
        "data_nascimento": "1990-02-25",
    },
    {
        "id_usuario": 6,
        "nome": "Ana Souza",
        "email": "ana.s@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "aluno",
        "data_nascimento": "1998-07-30",
    },
    {
        "id_usuario": 7,
        "nome": "Lucas Pereira",
        "email": "lucas.p@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "aluno",
        "data_nascimento": "1993-09-01",
    },
    {
        "id_usuario": 8,
        "nome": "Beatriz Oliveira",
        "email": "bia.oli@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "aluno",
        "data_nascimento": "2001-12-12",
    },
    {
        "id_usuario": 9,
        "nome": "Gabriel Santos",
        "email": "gabriel.s@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "aluno",
        "data_nascimento": "1999-03-08",
    },
    {
        "id_usuario": 10,
        "nome": "Julia Martins",
        "email": "julia.m@email.com",
        "senha_hash": "hash_fake_123",
        "tipo_usuario": "aluno",
        "data_nascimento": "2002-05-21",
    },
]

EXERCICIOS_INICIAIS = [
    (1, "Supino Reto", "Peitoral"),
    (2, "Agachamento Livre", "Pernas"),
    (3, "Levantamento Terra", "Costas"),
    (4, "Desenvolvimento com Halteres", "Ombros"),
    (5, "Rosca Direta", "Bíceps"),
    (6, "Tríceps na Polia", "Tríceps"),
    (7, "Puxada Frontal", "Costas"),
    (8, "Leg Press 45", "Pernas"),
    (9, "Elevação Lateral", "Ombros"),
    (10, "Cadeira Extensora", "Pernas"),
]

ACOMPANHAMENTOS_INICIAIS = [
    {"id_profissional": 2, "id_aluno": 1, "data_inicio": "2025-05-10"},
    {"id_profissional": 2, "id_aluno": 3, "data_inicio": "2025-06-01"},
    {"id_profissional": 5, "id_aluno": 7, "data_inicio": "2025-04-20"},
    {"id_profissional": 5, "id_aluno": 8, "data_inicio": "2025-07-01"},
]


def criar_dados_base():
    """Cria os usuários, exercícios e acompanhamentos iniciais diretamente no banco."""
    print("Verificando e inserindo dados de base...")
    try:
        with engine.connect() as connection:
            for user in USUARIOS_INICIAIS:
                stmt_user = text(
                    "INSERT INTO usuarios (id_usuario, nome, email, senha_hash, data_nascimento, tipo_usuario) VALUES (:id, :nome, :email, :senha, :data_nasc, :tipo) ON CONFLICT (id_usuario) DO NOTHING;"  # noqa: E501
                )
                connection.execute(
                    stmt_user,
                    {
                        "id": user["id_usuario"],
                        "nome": user["nome"],
                        "email": user["email"],
                        "senha": user["senha_hash"],
                        "data_nasc": user["data_nascimento"],
                        "tipo": user["tipo_usuario"],
                    },
                )
                if user["tipo_usuario"] == "aluno":
                    connection.execute(
                        text(
                            "INSERT INTO alunos (id_usuario) VALUES (:id) ON CONFLICT (id_usuario) DO NOTHING;"  # noqa: E501
                        ),
                        {"id": user["id_usuario"]},
                    )
                elif user["tipo_usuario"] == "profissional":
                    connection.execute(
                        text(
                            "INSERT INTO profissionais (id_usuario) VALUES (:id) ON CONFLICT (id_usuario) DO NOTHING;"  # noqa: E501
                        ),
                        {"id": user["id_usuario"]},
                    )

            for id_exercicio, nome, grupo in EXERCICIOS_INICIAIS:
                stmt_ex = text(
                    "INSERT INTO exercicios (id_exercicio, nome_exercicio, grupo_muscular) VALUES (:id, :nome, :grupo) ON CONFLICT (id_exercicio) DO NOTHING;"  # noqa: E501
                )
                connection.execute(
                    stmt_ex, {"id": id_exercicio, "nome": nome, "grupo": grupo}
                )

            for acomp in ACOMPANHAMENTOS_INICIAIS:
                stmt_acomp = text(
                    "INSERT INTO acompanhamentos (id_profissional, id_aluno, data_inicio, status) VALUES (:id_prof, :id_aluno, :data_inicio, 'ativo');"  # noqa: E501
                )
                connection.execute(
                    stmt_acomp,
                    {
                        "id_prof": acomp["id_profissional"],
                        "id_aluno": acomp["id_aluno"],
                        "data_inicio": acomp["data_inicio"],
                    },
                )

            connection.commit()
            print(
                "Dados de base (usuários, exercícios e acompanhamentos) inseridos com sucesso."  # noqa: E501
            )
    except Exception as e:
        print(f"Erro ao inserir dados de base: {e}")
        raise


def popular_treinos(num_treinos=500):
    """Envia N treinos para a API para popular as tabelas de fatos."""
    print(f"\nIniciando o povoamento com {num_treinos} treinos através da API...")
    API_URL = "http://localhost:8000"
    ids_alunos = [
        u["id_usuario"] for u in USUARIOS_INICIAIS if u["tipo_usuario"] == "aluno"
    ]

    for i in range(num_treinos):
        id_usuario_aluno = random.choice(ids_alunos)
        id_exercicio = random.choice([e[0] for e in EXERCICIOS_INICIAIS])
        data_treino = date.today() - timedelta(days=random.randint(0, 90))

        series = []
        for j in range(1, random.randint(3, 5) + 1):
            series.append(
                {
                    "numero_serie": j,
                    "repeticoes": random.randint(8, 15),
                    "carga_kg": round(random.uniform(10.0, 100.0), 1),
                }
            )

        payload = {
            "id_usuario": id_usuario_aluno,
            "data_treino": data_treino.isoformat(),
            "exercicios": [{"id_exercicio": id_exercicio, "series": series}],
        }

        try:
            response = requests.post(f"{API_URL}/treinos/", json=payload)
            response.raise_for_status()
            print(
                f"Treino {i+1}/{num_treinos} para o aluno ID {id_usuario_aluno} registrado com sucesso."  # noqa: E501
            )
        except requests.exceptions.RequestException as e:
            print(f"Erro ao registrar treino {i+1}: {e}")
            if e.response is not None:
                print(f"Resposta da API: {e.response.text}")
            break


if __name__ == "__main__":
    try:
        criar_dados_base()
        popular_treinos(num_treinos=500)
    except Exception as e:
        print(f"Processo de seeding interrompido devido a um erro: {e}")
