import unittest
from unittest.mock import patch, MagicMock, call
from menu_service.menu import (
    create_product,
    update_product,
    delete_product,
    read_menu,
    search_product,
    mostrar_menu_desarrollador
)

class TestMenuFunctions(unittest.TestCase):
    
    def setUp(self):
        # Mock de la colección 'menu' (simula MongoDB)
        self.menu_patcher = patch('menu_service.menu.menu', MagicMock())
        self.mock_menu = self.menu_patcher.start()
        
        # Datos de prueba
        self.sample_product = {
            "Name": "Pasta Carbonara",
            "Description": "Pasta con salsa cremosa",
            "Price": 15.99,
            "Points": 0,
            "Points Price": "1000",
            "Aviability": "Si"
        }
        
    def tearDown(self):
        self.menu_patcher.stop()

    # --- Pruebas para create_product ---
    @patch('builtins.input')
    @patch('builtins.print')
    def test_create_product_cheap(self, mock_print, mock_input):
        """Productos con precio < 1000 deben dar 0 puntos"""
        mock_input.side_effect = ["Ensalada", "Verde", "8.99", "500"]
        create_product()
        
        # Verifica que se insertó el producto con los datos correctos
        self.mock_menu.insert_one.assert_called_once_with({
            "Name": "Ensalada",
            "Category": "Product",
            "Description": "Verde",
            "Price": 8.99,
            "Points": 0,
            "Points Price": "500",
            "Aviability": "Si"
        })
        mock_print.assert_called_with("Producto agregado.")

    # --- Pruebas para update_product ---
    @patch('builtins.input')
    @patch('builtins.print')
    def test_update_product_price(self, mock_print, mock_input):
        """Actualizar precio debe recalcular puntos"""
        self.mock_menu.find_one.return_value = self.sample_product
        mock_input.side_effect = ["Pasta Carbonara", "3", "2500", "6"]  # Opción 3 (precio)
        
        update_product()
        
        # Verifica que se actualizó el precio y los puntos
        expected_calls = [
            call({"Name": "Pasta Carbonara"}, {"$set": {"Price": 2500}}),
            call({"Name": "Pasta Carbonara"}, {"$set": {"Points": 2.5}})
        ]
        self.mock_menu.update_one.assert_has_calls(expected_calls, any_order=True)
        mock_print.assert_called_with("Producto editado.")

    # --- Pruebas para delete_product ---
    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_existing_product(self, mock_print, mock_input):
        """Eliminar producto existente debe llamar a delete_one"""
        self.mock_menu.delete_one.return_value.deleted_count = 1
        mock_input.return_value = "Pasta Carbonara"
        
        delete_product()
        
        self.mock_menu.delete_one.assert_called_once_with({"Name": "Pasta Carbonara"})
        mock_print.assert_called_with("Producto eliminado.")

    # --- Pruebas para read_menu ---
    @patch('builtins.print')
    def test_read_menu_with_items(self, mock_print):
        """read_menu debe imprimir los productos"""
        self.mock_menu.find.return_value = [self.sample_product]
        
        read_menu()
        
        # Verifica que se imprimió la información del producto
        output = "\n".join([str(args[0]) for args, _ in mock_print.call_args_list])
        self.assertIn("Nombre: Pasta Carbonara", output)
        self.assertIn("Precio: 15.99$", output)
        self.assertIn("Disponibilidad: Si", output)

    # --- Pruebas para search_product ---
    @patch('builtins.input')
    @patch('builtins.print')
    def test_search_product_found(self, mock_print, mock_input):
        """Buscar producto existente debe mostrar sus datos"""
        self.mock_menu.find_one.return_value = self.sample_product
        mock_input.return_value = "Pasta Carbonara"
        
        search_product()
        
        # Verifica que se mostró la información del producto
        output = "\n".join([str(args[0]) for args, _ in mock_print.call_args_list])
        self.assertIn("Nombre: Pasta Carbonara", output)
        self.assertIn("Descripcion: Pasta con salsa cremosa", output)

    # --- Pruebas para el menú principal ---
    @patch('menu_service.menu.create_product')
    @patch('builtins.input')
    def test_mostrar_menu_desarrollador(self, mock_input, mock_create):
        """El menú debe llamar a create_product al elegir opción 1"""
        mock_input.side_effect = ["1", "6"]  # Opción 1 (crear) y luego 6 (salir)
        
        mostrar_menu_desarrollador()
        
        mock_create.assert_called_once()

if __name__ == '__main__':
    unittest.main()