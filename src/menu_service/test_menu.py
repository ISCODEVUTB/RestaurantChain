import unittest
from unittest.mock import patch, MagicMock, call
from menu_service.menu import (
    create_product,
    update_product,
    delete_product,
    read_menu,
    mostrar_menu_desarrollador
)

class TestMenuFunctions(unittest.TestCase):
    
    def setUp(self):
        """ Configurar mocks antes de cada prueba. """
        self.menu_patcher = patch('menu_service.menu.menu', MagicMock())
        self.mock_menu = self.menu_patcher.start()
        
        self.sample_product = {
            "Name": "Pasta Carbonara",
            "Description": "Pasta con salsa cremosa",
            "Price": 15.99,
            "Points": 0,
            "Points Price": "1000",
            "Aviability": "Si"
        }
        
    def tearDown(self):
        """ Detener los mocks después de cada prueba. """
        self.menu_patcher.stop()

    @patch('builtins.input')
    @patch('builtins.print')
    def test_create_product(self, mock_print, mock_input):
        """ Prueba la creación de un producto con precio bajo. """
        mock_input.side_effect = ["Ensalada", "Verde", "8.99", "500"]
        create_product()
        
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

    @patch('builtins.input')
    @patch('builtins.print')
    def test_update_product(self, mock_print, mock_input):
        """ Prueba la actualización de precio y puntos. """
        self.mock_menu.find_one.return_value = self.sample_product
        mock_input.side_effect = ["Pasta Carbonara", "3", "2500", "6"]
        
        update_product()
        
        expected_calls = [
            call({"Name": "Pasta Carbonara"}, {"$set": {"Price": 2500}}),
            call({"Name": "Pasta Carbonara"}, {"$set": {"Points": 2.5}})
        ]
        self.mock_menu.update_one.assert_has_calls(expected_calls, any_order=True)
        mock_print.assert_called_with("Producto editado.")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_delete_product(self, mock_print, mock_input):
        """ Prueba la eliminación de un producto existente. """
        self.mock_menu.delete_one.return_value.deleted_count = 1
        mock_input.return_value = "Pasta Carbonara"
        
        delete_product()
        
        self.mock_menu.delete_one.assert_called_once_with({"Name": "Pasta Carbonara"})
        mock_print.assert_called_with("Producto eliminado.")

    @patch('builtins.print')
    def test_read_menu(self, mock_print):
        """ Verifica que la función `read_menu` muestra los productos. """
        self.mock_menu.find.return_value = [self.sample_product]
        
        read_menu()
        
        output = "\n".join([str(args[0]) for args, _ in mock_print.call_args_list])
        self.assertIn("Nombre: Pasta Carbonara", output)
        self.assertIn("Precio: 15.99$", output)
        self.assertIn("Disponibilidad: Si", output)

    @patch('builtins.input', side_effect=["6"])  # Simula la opción "6" para salir
    @patch('builtins.print')
    def test_mostrar_menu_desarrollador_exit(self, mock_print, mock_input):
        """Verifica que el menú se muestra y permite salir correctamente."""
        mostrar_menu_desarrollador()
        
        # Capturar la salida de `print()`
        output = "\n".join([call[0][0] for call in mock_print.call_args_list])
        self.assertIn("--- Gestion de Menu ---", output)
        self.assertIn("Salir", output)

    @patch('builtins.input', side_effect=["1", "Ensalada", "Verde", "8.99", "500", "6"])
    @patch('builtins.print')
    @patch('menu_service.menu.create_product')
    def test_mostrar_menu_desarrollador_create_product(self, mock_create_product, mock_print, mock_input):
        """Verifica que se ejecuta `create_product` cuando el usuario elige la opción."""
        mostrar_menu_desarrollador()
        
        mock_create_product.assert_called_once()  # Se debe haber llamado `create_product`

    @patch('builtins.input', side_effect=["3", "Pizza", "6"])
    @patch('builtins.print')
    @patch('menu_service.menu.delete_product')
    def test_mostrar_menu_desarrollador_delete_product(self, mock_delete_product, mock_print, mock_input):
        """Verifica que se ejecuta `delete_product` cuando el usuario elige la opción."""
        mostrar_menu_desarrollador()
        
        mock_delete_product.assert_called_once()  # Se debe haber llamado `delete_product`

if __name__ == '__main__':
    unittest.main()
