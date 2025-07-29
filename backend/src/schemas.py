from datetime import date as DateType
from datetime import datetime

# from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel

# --- Schemas Operacionais (Relacionados ao OLTP) ---


# -- Para Criação de Treinos --
class SerieBase(BaseModel):
    numero_serie: int
    repeticoes: int
    carga_kg: float


class ExercicioRealizadoBase(BaseModel):
    id_exercicio: int
    series: List[SerieBase]


class TreinoCreate(BaseModel):
    id_usuario: int
    data_treino: DateType
    exercicios: List[ExercicioRealizadoBase]
    status: Optional[str] = "planejado"


# -- Para Respostas de Endpoints --
class Serie(BaseModel):
    id_serie: int
    id_exercicio: int
    numero_serie: int
    repeticoes: int
    carga_kg: float

    class Config:
        from_attributes = True


class Treino(BaseModel):
    id_treino: int
    id_usuario: int
    data_treino: DateType
    status: str
    series: List[Serie] = []

    class Config:
        from_attributes = True


class TreinoResponse(BaseModel):
    message: str
    id_treino: int

    class Config:
        from_attributes = True


# -- Para Listagens Simples --
class AlunoSimples(BaseModel):
    id_usuario: int
    nome: str

    class Config:
        from_attributes = True


class ExercicioSimples(BaseModel):
    id_exercicio: int
    nome_exercicio: str

    class Config:
        from_attributes = True


# --- Schemas de Resumo e Análise (Relacionados ao OLAP e Agregados) ---


# -- Para o Card de Perfil do Usuário --
class UltimoTreino(BaseModel):
    data_treino: DateType

    class Config:
        from_attributes = True


class AlunoSummary(BaseModel):
    nome: str
    ultimo_login: Optional[datetime] = None
    ultimo_treino: Optional[UltimoTreino] = None


# -- Para o Endpoint de Analytics de Performance --
class DailyPerformanceData(BaseModel):
    data_treino: DateType
    volume_total_diario: float

    class Config:
        from_attributes = True


class AnalyticsResponse(BaseModel):
    id_aluno: int
    nome_aluno: str
    performance: List[DailyPerformanceData]


# -- Para o Endpoint de Frequência --
class FrequenciaData(BaseModel):
    periodo: str
    quantidade: int

    class Config:
        from_attributes = True


class FrequenciaResponse(BaseModel):
    aluno_id: int
    dados_frequencia: List[FrequenciaData]


class CalendarEvent(BaseModel):
    data_treino: DateType
    status: str
    exercicios: List[str]  # Uma lista com os nomes dos exercícios do dia

    class Config:
        from_attributes = True


class CalendarResponse(BaseModel):
    eventos: List[CalendarEvent]
