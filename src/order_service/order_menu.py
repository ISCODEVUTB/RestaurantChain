from pymongo import MongoClient
import os

MONGODB_URL = os.getenv("MONGODB_URL")
client = MongoClient(MONGODB_URL)
db = client["Restaurant"]
orders = db["Orders"]

orden = {
  "customer_name": "Elias Blanco",
  "items": [
    {
      "ProductName": "Pizza",
      "Price": 20000,
      "Quantity": 2
    }
  ],
  "total_price": 40000,
  "status": "Pendiente"
}

resultado = orders.insert_one(orden)
print("Pedido insertado con ID:", resultado.inserted_id)
