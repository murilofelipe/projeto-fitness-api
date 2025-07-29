# /backend/scripts/seed_data.py (Versão com Lógica de Treino Profissional)

import os
import random
import sys
from datetime import date, timedelta

import requests
from sqlalchemy import create_engine, text

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://myuser:mypassword@localhost:5432/fitness_db"
)
engine = create_engine(DATABASE_URL)

# --- DADOS INICIAIS ---
# (As listas USUARIOS_INICIAIS, EXERCICIOS_INICIAIS e ACOMPANHAMENTOS_INICIAIS permanecem as mesmas)  # noqa: E501
# ... cole suas listas completas aqui ...
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
    (11, "Remada Curvada", "Costas"),
    (12, "Flexão de Braço", "Peitoral"),
]
ACOMPANHAMENTOS_INICIAIS = [
    {"id_profissional": 2, "id_aluno": 1, "data_inicio": "2025-05-10"},
    {"id_profissional": 2, "id_aluno": 3, "data_inicio": "2025-06-01"},
    {"id_profissional": 5, "id_aluno": 7, "data_inicio": "2025-04-20"},
    {"id_profissional": 5, "id_aluno": 8, "data_inicio": "2025-07-01"},
]


def criar_dados_base():
    """
    Cria os usuários (com seus tipos), exercícios e acompanhamentos
    iniciais diretamente no banco de dados.
    """
    print("Verificando e inserindo dados de base...")
    try:
        # Abre uma conexão e inicia uma transação para garantir que tudo seja salvo
        with engine.connect() as connection:
            transaction = connection.begin()

            # 1. Insere os dados na tabela pai 'usuarios' e depois nas tabelas filhas
            for user in USUARIOS_INICIAIS:
                # Insere na tabela 'usuarios'
                stmt_user = text(
                    "INSERT INTO usuarios (id_usuario, nome, email, senha_hash, data_nascimento, tipo_usuario) "  # noqa: E501
                    "VALUES (:id, :nome, :email, :senha, :data_nasc, :tipo) ON CONFLICT (id_usuario) DO NOTHING;"  # noqa: E501
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

                # Insere na tabela filha correspondente ('alunos' ou 'profissionais')
                if user["tipo_usuario"] == "aluno":
                    stmt_aluno = text(
                        "INSERT INTO alunos (id_usuario) VALUES (:id) ON CONFLICT (id_usuario) DO NOTHING;"  # noqa: E501
                    )
                    connection.execute(stmt_aluno, {"id": user["id_usuario"]})
                elif user["tipo_usuario"] == "profissional":
                    stmt_prof = text(
                        "INSERT INTO profissionais (id_usuario) VALUES (:id) ON CONFLICT (id_usuario) DO NOTHING;"  # noqa: E501
                    )
                    connection.execute(stmt_prof, {"id": user["id_usuario"]})

            # 2. Insere os exercícios
            for id_exercicio, nome, grupo in EXERCICIOS_INICIAIS:
                stmt_ex = text(
                    "INSERT INTO exercicios (id_exercicio, nome_exercicio, grupo_muscular) "  # noqa: E501
                    "VALUES (:id, :nome, :grupo) ON CONFLICT (id_exercicio) DO NOTHING;"
                )
                connection.execute(
                    stmt_ex, {"id": id_exercicio, "nome": nome, "grupo": grupo}
                )

            # 3. Insere os relacionamentos na tabela 'acompanhamentos'
            for acomp in ACOMPANHAMENTOS_INICIAIS:
                stmt_acomp = text(
                    "INSERT INTO acompanhamentos (id_profissional, id_aluno, data_inicio, status) "  # noqa: E501
                    "VALUES (:id_prof, :id_aluno, :data_inicio, 'ativo');"
                )
                connection.execute(
                    stmt_acomp,
                    {
                        "id_prof": acomp["id_profissional"],
                        "id_aluno": acomp["id_aluno"],
                        "data_inicio": acomp["data_inicio"],
                    },
                )

            # Salva todas as alterações no banco de dados
            transaction.commit()
            print(
                "Dados de base (usuários, exercícios e acompanhamentos) inseridos com sucesso."  # noqa: E501
            )

    except Exception as e:
        print(f"Erro ao inserir dados de base: {e}")
        raise


def popular_treinos_realista():
    """
    Popula o banco com treinos passados (executados/não executados) e
    treinos futuros (planejados), em um intervalo de ~4 meses.
    """
    print("\nIniciando o povoamento com uma rotina de treinos realista...")
    API_URL = "http://localhost:8000"
    ids_alunos = [
        u["id_usuario"] for u in USUARIOS_INICIAIS if u["tipo_usuario"] == "aluno"
    ]

    exercicios_por_grupo = {}
    for ex in EXERCICIOS_INICIAIS:
        grupo = ex[2]
        if grupo not in exercicios_por_grupo:
            exercicios_por_grupo[grupo] = []
        exercicios_por_grupo[grupo].append(ex)

    grupos_musculares = list(exercicios_por_grupo.keys())
    total_treinos_criados = 0

    for aluno_id in ids_alunos:
        treinos_por_semana = random.randint(1, 6)
        print(
            f"Gerando rotina para o aluno ID {aluno_id} ({treinos_por_semana}x por semana)..."  # noqa: E501
        )

        # --- MUDANÇA AQUI: Geramos treinos de 12 semanas atrás até 4 semanas no futuro --- # noqa: E501
        for semana in range(-12, 5):
            dias_de_treino_na_semana = sorted(
                random.sample(range(7), treinos_por_semana)
            )

            for dia in dias_de_treino_na_semana:
                # A data do treino agora é relativa à data de hoje
                data_treino = date.today() + timedelta(weeks=semana, days=dia)

                # O resto da lógica de criar um treino realista continua a mesma
                num_grupos = random.randint(1, 3)
                grupos_do_dia = random.sample(grupos_musculares, num_grupos)

                exercicios_do_treino = []
                for grupo in grupos_do_dia:
                    exercicios_disponiveis = exercicios_por_grupo.get(grupo, [])
                    if not exercicios_disponiveis:
                        continue
                    num_exercicios_por_grupo = min(
                        random.randint(2, 5), len(exercicios_disponiveis)
                    )
                    exercicios_selecionados = random.sample(
                        exercicios_disponiveis, num_exercicios_por_grupo
                    )
                    exercicios_do_treino.extend(exercicios_selecionados)

                if not exercicios_do_treino:
                    continue

                exercicios_payload = []
                for ex in exercicios_do_treino:
                    series = []
                    for i in range(1, random.randint(3, 5)):
                        series.append(
                            {
                                "numero_serie": i,
                                "repeticoes": random.randint(8, 15),
                                "carga_kg": round(random.uniform(20.0, 120.0), 1),
                            }
                        )
                    exercicios_payload.append({"id_exercicio": ex[0], "series": series})

                # A lógica de status já funciona para datas futuras
                status = "planejado"
                if data_treino < date.today():
                    status = random.choice(["executado", "executado", "nao_executado"])

                payload = {
                    "id_usuario": aluno_id,
                    "data_treino": data_treino.isoformat(),
                    "exercicios": exercicios_payload,
                    "status": status,
                }

                try:
                    response = requests.post(f"{API_URL}/treinos/", json=payload)
                    response.raise_for_status()
                    total_treinos_criados += 1
                except requests.exceptions.RequestException as e:
                    print(f"Erro ao registrar treino: {e}")
                    if e.response is not None:
                        print(f"Resposta da API: {e.response.text}")
                    break

    print(
        f"\nPovoamento realista concluído. Total de {total_treinos_criados} treinos criados."  # noqa: E501
    )


if __name__ == "__main__":
    try:
        criar_dados_base()
        popular_treinos_realista()
    except Exception as e:
        print(f"Processo de seeding interrompido: {e}")
