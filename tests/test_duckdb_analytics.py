
import unittest
import sys
import os
import duckdb

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duckdb_analytics import DuckDBAnalytics

class TestDuckDBAnalytics(unittest.TestCase):
    def setUp(self):
        self.db_path = ":memory:"  # Usar banco de dados em memória para testes
        self.analytics = DuckDBAnalytics(self.db_path)
        self.analytics.connect()
        self.analytics.execute_query("CREATE TABLE sales (id INTEGER, product VARCHAR, amount DOUBLE)")
        self.analytics.execute_query("INSERT INTO sales VALUES (1, 'Laptop', 1200.00), (2, 'Mouse', 25.00), (3, 'Keyboard', 75.00), (4, 'Laptop', 1500.00)")

    def tearDown(self):
        self.analytics.disconnect()

    def test_connect_and_disconnect(self):
        # Já conectado no setUp, testar desconexão e reconexão
        self.analytics.disconnect()
        self.assertIsNone(self.analytics.conn)
        self.analytics.connect()
        self.assertIsNotNone(self.analytics.conn)

    def test_execute_query(self):
        result = self.analytics.execute_query("SELECT COUNT(*) FROM sales")
        self.assertEqual(result[0][0], 4)

    def test_fetch_data(self):
        data = self.analytics.fetch_data("SELECT * FROM sales WHERE product = 'Laptop'")
        self.assertEqual(len(data), 2)
        self.assertEqual(data['product'].iloc[0], 'Laptop')

    def test_create_view(self):
        self.analytics.create_view("top_sales", "SELECT product, SUM(amount) as total_amount FROM sales GROUP BY product ORDER BY total_amount DESC")
        result = self.analytics.fetch_data("SELECT * FROM top_sales")
        self.assertEqual(len(result), 3)
        self.assertEqual(result['product'].iloc[0], 'Laptop')

    def test_export_to_csv(self):
        output_file = "test_sales.csv"
        self.analytics.export_to_csv("SELECT * FROM sales", output_file)
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 5) # Header + 4 rows
        os.remove(output_file)

    def test_import_from_csv(self):
        # Criar um CSV de teste
        with open("new_sales.csv", "w") as f:
            f.write("id,product,amount\n")
            f.write("5,Monitor,300.00\n")
        
        self.analytics.execute_query("DROP TABLE IF EXISTS new_sales")
        self.analytics.import_from_csv("new_sales.csv", "new_sales")
        result = self.analytics.execute_query("SELECT COUNT(*) FROM new_sales")
        self.assertEqual(result[0][0], 1)

        os.remove("new_sales.csv")

    def test_get_table_schema(self):
        schema = self.analytics.get_table_schema("sales")
        self.assertIn(("id", "INTEGER"), schema)
        self.assertIn(("product", "VARCHAR"), schema)
        self.assertIn(("amount", "DOUBLE"), schema)

if __name__ == '__main__':
    unittest.main(verbosity=2)

