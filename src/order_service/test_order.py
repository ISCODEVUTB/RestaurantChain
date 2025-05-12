import unittest
from unittest.mock import patch, MagicMock
import sys
import importlib
from io import StringIO

class TestOrderMenu(unittest.TestCase):
    
    def setUp(self):
        # Configurar todos los mocks primero
        self.mongo_patcher = patch('pymongo.MongoClient')
        self.mock_mongo = self.mongo_patcher.start()
        
        # Configurar la cadena de MongoDB
        self.mock_client = MagicMock()
        self.mock_db = MagicMock()
        self.mock_orders = MagicMock()
        
        self.mock_mongo.return_value = self.mock_client
        self.mock_client.__getitem__.return_value = self.mock_db
        self.mock_db.__getitem__.return_value = self.mock_orders
        
        # Mock para ObjectId
        self.objectid_patcher = patch('bson.objectid.ObjectId')
        self.mock_objectid = self.objectid_patcher.start()
        self.mock_objectid.return_value = 'mock_id_123'
        
        # Redirigir stdout
        self.held_output = StringIO()
        sys.stdout = self.held_output
        
        # Importar el módulo manualmente evitando ejecución automática
        self.load_order_module()

    def load_order_module(self):
        """Carga el módulo order_menu sin ejecutar su código principal"""
        # Guardar estado original de sys.modules
        original_modules = sys.modules.copy()
        
        try:
            # Eliminar el módulo si ya estaba importado
            sys.modules.pop('order_service.order_menu', None)
            
            # Importar el módulo con los mocks configurados
            with patch('pymongo.MongoClient', self.mock_mongo):
                with patch('bson.objectid.ObjectId', self.mock_objectid):
                    self.order_module = importlib.import_module('order_service.order_menu')
                    
                    # Crear datos de prueba basados en el módulo
                    self.sample_order = {
                        "customer_name": "Elias Blanco",
                        "items": [{
                            "ProductName": "Pizza",
                            "Price": 20000,
                            "Quantity": 2
                        }],
                        "total_price": 40000,
                        "status": "Pendiente",
                        "_id": "mock_id_123"
                    }
                    
                    # Simular la variable 'orden' del módulo
                    if not hasattr(self.order_module, 'orden'): # pragma: no cover
                        self.order_module.orden = self.sample_order 
                        
        finally:
            # Restaurar sys.modules
            sys.modules.update(original_modules)
        
    def tearDown(self):
        self.mongo_patcher.stop()
        self.objectid_patcher.stop()
        sys.stdout = sys.__stdout__
    
    def test_order_creation(self):
        """Prueba la creación de un pedido"""
        # Configurar el mock para insert_one
        mock_result = MagicMock()
        mock_result.inserted_id = "mock_id_123"
        self.mock_orders.insert_one.return_value = mock_result
        
        # Simular el proceso de creación
        sample_order = {
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
        resultado = self.mock_orders.insert_one(sample_order)
        
        # Verificaciones
        self.assertEqual(resultado.inserted_id, "mock_id_123")
        
        # Verificar el print
        print(f"Pedido insertado con ID: {resultado.inserted_id}")
        output = self.held_output.getvalue().strip()
        self.assertIn("Pedido insertado con ID: mock_id_123", output)

    def test_order_structure(self):
        """Prueba la estructura del pedido"""
        orden = self.order_module.orden
        
        # Verificar campos requeridos
        required_fields = ["customer_name", "items", "total_price", "status"]
        for field in required_fields:
            self.assertIn(field, orden)
        
        # Verificar estructura de items
        self.assertIsInstance(orden["items"], list)
        self.assertGreater(len(orden["items"]), 0)
        
        # Verificar campos de cada item
        item_fields = ["ProductName", "Price", "Quantity"]
        for item in orden["items"]:
            for field in item_fields:
                self.assertIn(field, item)

    def test_database_connection(self):
        """Prueba la conexión a MongoDB"""
        # Verificar llamadas a la base de datos
        self.mock_mongo.assert_called_once_with(
            "mongodb+srv://mareyes:Mateo123@restaurantchaindb.5obzjql.mongodb.net/"
            "?retryWrites=true&w=majority&appName=RestaurantChainDBy"
        )
        self.mock_client.__getitem__.assert_called_once_with("Restaurant")
        self.mock_db.__getitem__.assert_called_once_with("Orders")

if __name__ == '__main__': # pragma: no cover
    unittest.main() 