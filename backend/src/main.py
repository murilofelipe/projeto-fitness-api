# /backend/src/main.py

# 1. Imports
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, ProgrammingError

# from . import models
# from .database import engine
from .routers import alunos_router, analytics_router, calendario_router, treinos_router

# 2. Cria a instância da aplicação
app = FastAPI(
    title="API do Projeto Fitness",
    description="API para gerenciar dados de treinos e performance de alunos.",
    version="1.0.0",
)

# 3. Cria as tabelas no banco de dados (se não existirem)
# models.Base.metadata.create_all(bind=engine)

# --- 2. ADICIONE A CONFIGURAÇÃO DO CORS AQUI ---
# Define de quais origens o frontend pode fazer requisições
origins = [
    "http://localhost:5173",  # Endereço do nosso app Vue.js
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, etc)
    allow_headers=["*"],  # Permite todos os cabeçalhos
)
# -----------------------------------------------


# 4. Registra o manipulador de exceção na 'app' que já existe
@app.exception_handler(ProgrammingError)
@app.exception_handler(OperationalError)
async def database_exception_handler(request: Request, exc: Exception):
    """
    Manipulador de exceção para erros comuns de banco de dados.
    Retorna uma resposta 503 Service Unavailable com uma mensagem amigável.
    """
    return JSONResponse(
        status_code=503,
        content={
            "message": "Erro de infraestrutura no banco de dados. Verifique se o banco está no ar e se as tabelas foram criadas com 'make db-init'.",  # noqa: E501
            "error_type": type(exc).__name__,
            "details": str(exc),
        },
    )


# 5. Rotas
app.include_router(treinos_router.router)
app.include_router(analytics_router.router)
app.include_router(alunos_router.router)
app.include_router(calendario_router.router)


# 6. Endpoint raiz
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API do Projeto Fitness está no ar!"}
