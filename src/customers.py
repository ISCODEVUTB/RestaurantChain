from pymongo import MongoClient

uri = "mongodb+srv://mareyes:Mateo123@restaurantdb.pnenkdn.mongodb.net/?retryWrites=true&w=majority&appName=RestaurantDB"

client = MongoClient(uri)
db = client["RestaurantDB"]
coleccion = db["customers"]

doc = {"nombre": "Elias", "edad": 18, "ciudad": "Corozal"}
coleccion.insert_one(doc)

