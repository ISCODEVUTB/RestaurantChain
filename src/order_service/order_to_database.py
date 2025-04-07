from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
pne= "pedido no encontrado"
uri = "mongodb+srv://mareyes:Mateo123@restaurantchaindb.5obzjql.mongodb.net/?retryWrites=true&w=majority&appName=RestaurantChainDBy"
client = MongoClient(uri)
db = client["Restaurant"]
orders = db["Orders"]

app = FastAPI()

class Item(BaseModel):
    ProductName: str
    Price: float
    Quantity: int
    Aviable: str

class Order(BaseModel):
    customer_name: str
    items: List[Item]
    total_price: float
    status: str = "Pendiente"


# Endpoint: Crear pedido
@app.post("/orders")
def create_order(order: Order):
    data = order.dict()
    data["order_date"] = datetime.utcnow()
    result = orders.insert_one(data)
    return {"message": "Pedido creado", "order_id": str(result.inserted_id)}

# Endpoint: Obtener todos los pedidos
@app.get("/orders")
def get_all_orders():
    all_orders = list(orders.find())
    for order in all_orders:
        order["_id"] = str(order["_id"])
    return all_orders

# Endpoint: Obtener pedido por ID
@app.get("/orders/{order_id}")
def get_order(order_id: str):
    order = orders.find_one({"_id": ObjectId(order_id)})
    if order:
        order["_id"] = str(order["_id"])
        return order
    raise HTTPException(status_code=404, detail= pne)

# Endpoint: Actualizar estado del pedido
@app.put("/orders/{order_id}")
def update_order_status(order_id: str, status: str):
    result = orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": status}})
    if result.modified_count:
        return {"message": "Pedido actualizado"}
    raise HTTPException(status_code=404, detail= pne)

# Endpoint: Eliminar pedido
@app.delete("/orders/{order_id}")
def delete_order(order_id: str):
    result = orders.delete_one({"_id": ObjectId(order_id)})
    if result.deleted_count:
        return {"message": "Pedido eliminado"}
    raise HTTPException(status_code=404, detail= pne)
