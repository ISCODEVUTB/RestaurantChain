from pymongo import MongoClient

uri = "mongodb+srv://mareyes:Mateo123@restaurantchaindb.5obzjql.mongodb.net/?retryWrites=true&w=majority&appName=RestaurantChainDBy"
client = MongoClient(uri)
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
