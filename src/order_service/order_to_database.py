from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
pne="pedido no encontrado"

uri = "mongodb+srv://mareyes:Mateo123@restaurantchaindb.5obzjql.mongodb.net/?retryWrites=true&w=majority&appName=RestaurantChainDBy"
client = MongoClient(uri)
db = client["Restaurant"]
orders = db["Orders"]

#Crear un Pedido
def create_order(customer_name, items, total_price, status="Pendiente"):
    order = {
        "customer_name": customer_name,
        "items": items,  # Lista de productos en el pedido
        "total_price": total_price,
        "status": status,
        "order_date": datetime.utcnow()
    }
    result = orders.insert_one(order)
    return f"Pedido creado con ID: {result.inserted_id}"

#Obtener un Pedido por ID
def get_order_by_id(order_id):
    try:
        order = orders.find_one({"_id": ObjectId(order_id)})
        return order if order else " Pedido no encontrado"
    except Exception as e:
        return f" Error: {e}"

#Obtener Todos los Pedidos
def get_all_orders():
    return list(orders.find({}, {"_id": 0}))

#Actualizar el Estado de un Pedido(por id)
def update_order_status(order_id, new_status):
    result = orders.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": new_status}})
    return " Pedido actualizado" if result.modified_count > 0 else "Pedido no encontrado"

#Eliminar un Pedido(usar la id)
def delete_order(order_id):   
    result = orders.delete_one({"_id": ObjectId(order_id)})
    return " Pedido eliminado" if result.deleted_count > 0 else "Pedido no encontrado"
