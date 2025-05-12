from pymongo import MongoClient
import os

# Conexión a MongoDB
MONGODB_URL = os.getenv("MONGODB_URL")
client = MongoClient(MONGODB_URL)
db = client["Restaurant"]
menu = db["Menu"]


def create_promo():
    name = input("Nombre de la promocion: ")
    desc = input("Descripción: ")
    price = float(input("Precio: "))
    if price < 1000:
        points = 0
    else:
        points = price / 1000
    p_price = input("Valor en puntos: ")
    promo = {
        "Name": name,
        "Category": "Promotion",
        "Description": desc,
        "Price": price,
        "Points": points,
        "Points Price": p_price,
        "Aviability": "Si"
    }
    menu.insert_one(promo)
    print("Promocion agregada.")


def update_promo():
    edpr = "Promocion editada."
    name = input("Nombre de la promocion a editar: ")
    promo = menu.find_one({"Name": name})
    if not promo:
        print("Promocion Inexistente.")
        return
    op = 0
    while op not in ["1", "2", "3", "4", "5", "6"]:
        op = input(
            "¿Qué deseas editar? \n"
            "1. Nombre \n"
            "2. Descripción \n"
            "3. Precio \n"
            "4. Valor en puntos \n"
            "5. Disponibilidad \n"
            "6. Salir\n"
            "Ingrese la opción: "
        )
        if op == "1":
            new_name = input("Nuevo nombre: ")
            menu.update_one({"Name": name}, {"$set": {"Name": new_name}})
            print(edpr)
        elif op == "2":
            new_desc = input("Nueva descripción: ")
            menu.update_one(
                {"Name": name}, {"$set": {"Description": new_desc}}
            )
            print(edpr)
        elif op == "3":
            new_price = float(input("Nuevo precio: "))
            menu.update_one({"Name": name}, {"$set": {"Price": new_price}})
            if new_price < 1000:
                points = 0
            else:
                points = new_price / 1000
            menu.update_one({"Name": name}, {"$set": {"Points": points}})
            print(edpr)
        elif op == "4":
            new_points = float(input("Nuevo valor en puntos: "))
            menu.update_one(
                {"Name": name},
                {"$set": {"Points Price": new_points}}
            )
            print(edpr)
        elif op == "5":
            new_availability = input("¿Disponible? (Si/No): ")
            menu.update_one(
                {"Name": name},
                {"$set": {"Aviability": new_availability}}
            )
            print(edpr)
        elif op == "6":
            print("Saliendo de la edición.")
            break
        else:
            print("Opción inválida.")


def delete_promo():
    name = input("Nombre de la promocion a eliminar: ")
    result = menu.delete_one({"Name": name})
    if result.deleted_count > 0:
        print("Promocion eliminada.")
    else:
        print("Promocion no encontrada.")


def read_promos():
    for product in menu.find():
        if product["Category"] == "Promotion":
            print(f"Nombre: {product['Name']}\n"
                  f"Descripcion: {product['Description']}\n"
                  f"Precio: {product['Price']}$ \n"
                  f"Puntos: {product['Points']} \n"
                  f"Valor en puntos: {product['Points Price']}\n"
                  f"Disponibilidad: {product['Aviability']}\n")
            print("--------------------------------------------------")


def search_promo():
    name = input("Nombre de la promocion a buscar: ")
    product = menu.find_one({"Name": name})
    if product:
        print(f"Nombre: {product['Name']}\n"
              f"Descripcion: {product['Description']}\n"
              f"Precio: {product['Price']}$ \n"
              f"Puntos: {product['Points']} \n"
              f"Valor en puntos: {product['Points Price']}\n"
              f"Disponibilidad: {product['Aviability']}\n")
    else:
        print("Producto no encontrado.")


def show_proms_admin():
    while True:
        print("\n--- Gestion de Promociones ---")
        print("1. Crear promocion")
        print("2. Editar promocion")
        print("3. Eliminar promocion")
        print("4. Listar promociones")
        print("5. Buscar promocion")
        print("6. Salir")
        opcion = input("Selecciona una opcion: ")
        if opcion == "1":
            create_promo()
        elif opcion == "2":
            update_promo()
        elif opcion == "3":
            delete_promo()
        elif opcion == "4":
            read_promos()
        elif opcion == "5":
            search_promo()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


show_proms_admin()
