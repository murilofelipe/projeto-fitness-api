# /backend/main.py

from fastapi import FastAPI

# Cria a instância da aplicação FastAPI
app = FastAPI(title="API do Projeto Fitness")

# Cria um endpoint de teste na raiz da API
@app.get("/")
def read_root():
    """
    Endpoint raiz para verificar se a API está funcionando.
    """
    return {"message": "API do Projeto Fitness está no ar!"}