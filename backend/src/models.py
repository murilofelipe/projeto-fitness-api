# /backend/src/models.py

from datetime import date as DateType  # <-- MUDANÇA AQUI: importamos datetime
from datetime import datetime
from decimal import Decimal
from typing import List  # <-- MUDANÇA AQUI: importamos List

from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    Column,
    Date,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

# --- MODELO DE USUÁRIO COM HERANÇA E AUDITORIA DE LOGIN ---

class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    telefone: Mapped[str] = mapped_column(String(20), nullable=True)
    data_nascimento: Mapped[DateType] = mapped_column(Date, nullable=True)
    tipo_usuario: Mapped[str] = mapped_column(String(50))
    ultimo_login: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = {"extend_existing": True}
    __mapper_args__ = {
        "polymorphic_on": tipo_usuario,
        "polymorphic_identity": "usuario",
    }


class Aluno(Usuario):
    __tablename__ = "alunos"
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"), primary_key=True
    )
    laudo_medico_url: Mapped[str] = mapped_column(String(255), nullable=True)
    __mapper_args__ = {"polymorphic_identity": "aluno"}


class Profissional(Usuario):
    __tablename__ = "profissionais"
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"), primary_key=True
    )
    registro_conselho: Mapped[str] = mapped_column(String(50), nullable=True)
    __mapper_args__ = {"polymorphic_identity": "profissional"}


class Acompanhamento(Base):
    __tablename__ = "acompanhamentos"
    id_acompanhamento: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_profissional: Mapped[int] = mapped_column(ForeignKey("profissionais.id_usuario"))
    id_aluno: Mapped[int] = mapped_column(ForeignKey("alunos.id_usuario"))
    data_inicio: Mapped[DateType] = mapped_column(Date, default=datetime.utcnow)
    data_fim: Mapped[DateType] = mapped_column(Date, nullable=True)
    motivo_encerramento: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="ativo")
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = {"extend_existing": True}


class Exercicios(Base):
    __tablename__ = "exercicios"
    id_exercicio: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome_exercicio: Mapped[str] = mapped_column(String(100), unique=True)
    grupo_muscular: Mapped[str] = mapped_column(String(50))
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = {"extend_existing": True}


class TreinoRealizado(Base):
    __tablename__ = "treinos_realizados"
    id_treino: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_usuario: Mapped[int] = mapped_column(ForeignKey("usuarios.id_usuario"))
    data_treino: Mapped[DateType] = mapped_column(Date)
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    series: Mapped[List["SerieRealizada"]] = relationship()
    __table_args__ = {"extend_existing": True}


class SerieRealizada(Base):
    __tablename__ = "series_realizadas"
    id_serie: Mapped[int] = mapped_column(primary_key=True, index=True)
    id_treino: Mapped[int] = mapped_column(ForeignKey("treinos_realizados.id_treino"))
    id_exercicio: Mapped[int] = mapped_column(ForeignKey("exercicios.id_exercicio"))
    numero_serie: Mapped[int] = mapped_column()
    repeticoes: Mapped[int] = mapped_column()
    carga_kg: Mapped[Decimal] = mapped_column(DECIMAL(6, 2))
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = {"extend_existing": True}


# --- MODELOS OLAP (Data Warehouse) ---

class DimAluno(Base):
    __tablename__ = "dim_aluno"
    id_aluno: Mapped[int] = mapped_column(primary_key=True)
    nome_aluno: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = {"extend_existing": True}


class DimExercicio(Base):
    __tablename__ = "dim_exercicio"
    id_exercicio: Mapped[int] = mapped_column(primary_key=True)
    nome_exercicio: Mapped[str] = mapped_column(String(100))
    grupo_muscular: Mapped[str] = mapped_column(String(50))
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = {"extend_existing": True}


class DimTempo(Base):
    __tablename__ = "dim_tempo"
    id_data: Mapped[DateType] = mapped_column(Date, primary_key=True)
    ano: Mapped[int] = mapped_column(Integer)
    mes: Mapped[int] = mapped_column(Integer)
    dia: Mapped[int] = mapped_column(Integer)
    dia_da_semana: Mapped[str] = mapped_column(String(20))
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = {"extend_existing": True}


class FctTreinos(Base):
    __tablename__ = "fct_treinos"
    id_treino: Mapped[int] = mapped_column(Integer)
    id_data: Mapped[DateType] = mapped_column(Date, ForeignKey("dim_tempo.id_data"))
    id_aluno: Mapped[int] = mapped_column(Integer, ForeignKey("dim_aluno.id_aluno"))
    id_exercicio: Mapped[int] = mapped_column(
        Integer, ForeignKey("dim_exercicio.id_exercicio")
    )
    total_series: Mapped[int] = mapped_column(Integer)
    total_repeticoes: Mapped[int] = mapped_column(Integer)
    maior_carga_kg: Mapped[Decimal] = mapped_column(DECIMAL(6, 2))
    volume_total_carga: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    data_criacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    data_modificacao: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    __table_args__ = (
        PrimaryKeyConstraint("id_treino", "id_data", "id_aluno", "id_exercicio"),
        {"extend_existing": True},
    )
