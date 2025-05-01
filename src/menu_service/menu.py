from pymongo import MongoClient

# Conexión a MongoDB
client = MongoClient(
    "mongodb+srv://mareyes:Mateo123@restaurantchaindb.5obzjql.mongodb.net/"
    "?retryWrites=true&w=majority&appName=RestaurantChainDBy"
)
db = client["Restaurant"]
menu = db["Menu"]


def create_product():
    name = input("Nombre del producto: ")
    desc = input("Descripción: ")
    price = float(input("Precio: "))
    if price < 1000:
        points = 0
    else:
        points = price / 1000
    p_price = input("Valor en puntos: ")
    product = {"Name": name,
               "Category": "Product",
               "Description": desc,
               "Price": price,
               "Points": points,
               "Points Price": p_price,
               "Aviability": "Si"}
    menu.insert_one(product)
    print("Producto agregado.")


def update_product():
    edp = "Producto editado."
    name = input("Nombre del producto a editar: ")
    product = menu.find_one({"Name": name})
    if not product:
        print("Producto Inexistente.")
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
            print(edp)
        elif op == "2":
            new_desc = input("Nueva descripción: ")
            menu.update_one(
                {"Name": name}, {"$set": {"Description": new_desc}}
            )
            print(edp)
        elif op == "3":
            new_price = float(input("Nuevo precio: "))
            menu.update_one({"Name": name}, {"$set": {"Price": new_price}})
            if new_price < 1000:
                points = 0
            else:
                points = new_price / 1000
            menu.update_one({"Name": name}, {"$set": {"Points": points}})
            print(edp)
        elif op == "4":
            new_points = float(input("Nuevo valor en puntos: "))
            menu.update_one(
                {"Name": name},
                {"$set": {"Points Price": new_points}}
            )
            print(edp)
        elif op == "5":
            new_availability = input("¿Disponible? (Si/No): ")
            menu.update_one(
                {"Name": name},
                {"$set": {"Aviability": new_availability}}
            )
            print(edp)
        elif op == "6":
            print("Saliendo de la edición.")
            break
        else:
            print("Opción inválida.")


def delete_product():
    name = input("Nombre del producto a eliminar: ")
    result = menu.delete_one({"Name": name})
    if result.deleted_count > 0:
        print("Producto eliminado.")
    else:
        print("Producto no encontrado.")


def read_menu():
    for product in menu.find():
        print(f"Nombre: {product['Name']}\n"
              f"Descripcion: {product['Description']}\n"
              f"Precio: {product['Price']}$ \n"
              f"Puntos: {product['Points']} \n"
              f"Valor en puntos: {product['Points Price']}\n"
              f"Disponibilidad: {product['Aviability']}\n")
        print("--------------------------------------------------")


def search_product():
    name = input("Nombre del producto a buscar: ")
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


def mostrar_menu_desarrollador():
    while True:
        print("\n--- Gestion de Menu ---")
        print("1. Crear producto")
        print("2. Editar producto")
        print("3. Eliminar producto")
        print("4. Listar menu")
        print("5. Buscar producto")
        print("6. Salir")
        opcion = input("Selecciona una opcion: ")
        if opcion == "1":
            create_product()
        elif opcion == "2":
            update_product()
        elif opcion == "3":
            delete_product()
        elif opcion == "4":
            read_menu()
        elif opcion == "5":
            search_product()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    mostrar_menu_desarrollador()