# /backend/tests/test_main.py

import pytest
from httpx import ASGITransport, AsyncClient  # <--- 1. IMPORTE O ASGITRANSPORT

from src.main import app


@pytest.mark.asyncio
async def test_read_root():
    """
    Testa se o endpoint raiz ("/") está funcionando e retornando o JSON esperado.
    """
    # 2. A MUDANÇA ESTÁ AQUI:
    # Criamos o transporte com a nossa app e o passamos para o AsyncClient
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/")

    # As asserções continuam as mesmas
    assert response.status_code == 200
    assert response.json() == {"message": "API do Projeto Fitness está no ar!"}
