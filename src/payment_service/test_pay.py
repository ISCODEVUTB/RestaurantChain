import sys
import os
import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient
from fastapi import status
from bson import ObjectId

# Ajuste para reconocer correctamente `payment_service`
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar `pay.py`
from payment_service.pay import app, payment_methods

# Cliente de prueba para la API
client = TestClient(app)

# Simulación de la base de datos MongoDB
@pytest.fixture(autouse=True)
def mock_db():
    with patch("payment_service.pay.payment_methods", AsyncMock()) as mock:
        mock.insert_one.return_value.inserted_id = ObjectId("000000000000000000000000")
        mock.find_one.return_value = None
        mock.update_one.return_value.matched_count = 0
        mock.delete_one.return_value.deleted_count = 0
        mock.find.return_value.to_list = AsyncMock(return_value=[
            {"_id": ObjectId("000000000000000000000000"), "name": "Tarjeta", "description": "Pago con tarjeta", "is_active": True}
        ])
        yield mock

def test_root():
    """Verifica que el endpoint raíz devuelve el mensaje correcto."""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Bienvenido a la API"}

@pytest.mark.asyncio
async def test_get_nonexistent_payment_method(mock_db):
    """Intenta obtener un método de pago inexistente."""
    response = client.get(f"/payment-methods/{ObjectId('000000000000000000000000')}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Metodo de pago no encontrado"

@pytest.mark.asyncio
async def test_delete_nonexistent_payment_method(mock_db):
    """Intenta eliminar un método de pago inexistente."""
    response = client.delete(f"/payment-methods/{ObjectId('000000000000000000000000')}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Metodo de pago no encontrado"