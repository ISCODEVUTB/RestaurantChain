from pymongo import MongoClient

uri = "mongodb+srv://mareyes:Mateo123@restaurantchaindb.5obzjql.mongodb.net/?retryWrites=true&w=majority&appName=RestaurantChainDBy"

client = MongoClient(uri)
db = client["Restaurant"] 
menu = db["Menu"]

productos = {
    "ProductName": "Hamburguesa sencilla",
    "Price": 12000,
    "Desc": "Hamburguesa sencilla con lechuga y tomate",
    "Points": 12
}

resultado = menu.insert_one(productos)
print("Producto insertado con ID:", resultado.inserted_id)