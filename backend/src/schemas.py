from datetime import date
from typing import List

from pydantic import BaseModel


# Define como os dados devem ser recebidos e enviados pela API
class SerieBase(BaseModel):
    numero_serie: int
    repeticoes: int
    carga_kg: float


class ExercicioRealizadoBase(BaseModel):
    id_exercicio: int
    series: List[SerieBase]


class TreinoCreate(BaseModel):
    id_usuario: int
    data_treino: date
    exercicios: List[ExercicioRealizadoBase]


# --- Schemas para Leitura/Resposta ---


# Schema para uma série individual na resposta
class Serie(BaseModel):
    id_serie: int
    id_exercicio: int
    numero_serie: int
    repeticoes: int
    carga_kg: float

    class Config:
        orm_mode = True


# Schema para um treino completo na resposta
class Treino(BaseModel):
    id_treino: int
    id_usuario: int
    data_treino: date
    series: List[Serie] = []  # Incluiremos as séries na resposta

    class Config:
        from_attributes = True


# --- Schema de Resposta para o endpoint de criação (Já existente) ---
class TreinoResponse(BaseModel):
    message: str
    id_treino: int

    class Config:
        orm_mode = True
