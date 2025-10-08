
import unittest
import sys
import os
import duckdb
import pandas as pd
import json

# Adicionar o diretório src ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duckdb_analytics import DuckDBAnalytics

class TestDuckDBAnalytics(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_analytics.duckdb"
        self.test_data_dir = "test_data"
        os.makedirs(self.test_data_dir, exist_ok=True)

        self.analytics = DuckDBAnalytics(self.test_db_path)
        self.analytics.connect()

        # Criar arquivos de dados de exemplo para ingestão
        self.sample_csv_path = os.path.join(self.test_data_dir, "sample_sales.csv")
        with open(self.sample_csv_path, "w") as f:
            f.write("transaction_id,product,amount,customer_id,sale_date\n")
            f.write("1,Laptop,1200.00,C001,2025-01-01\n")
            f.write("2,Mouse,25.00,C002,2025-01-02\n")
            f.write("3,Keyboard,75.00,C001,2025-01-03\n")

        self.sample_json_path = os.path.join(self.test_data_dir, "sample_customers.json")
        with open(self.sample_json_path, "w") as f:
            f.write("[
  {\"customer_id\": \"C001\", \"name\": \"Alice\", \"city\": \"NY\"},
  {\"customer_id\": \"C002\", \"name\": \"Bob\", \"city\": \"LA\"}
]")

        self.sample_parquet_path = os.path.join(self.test_data_dir, "sample_products.parquet")
        df_products = pd.DataFrame({
            "product_id": ["P1", "P2"],
            "product_name": ["Laptop", "Mouse"],
            "category": ["Electronics", "Electronics"]
        })
        df_products.to_parquet(self.sample_parquet_path, index=False)

        # Ingestão inicial para testes que dependem de dados existentes
        self.analytics.ingest_csv(self.sample_csv_path, "sales_initial")

    def tearDown(self):
        self.analytics.disconnect()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        if os.path.exists(f"{self.test_db_path}.wal"):
            os.remove(f"{self.test_db_path}.wal")
        
        # Limpar arquivos de dados de exemplo
        for f in os.listdir(self.test_data_dir):
            os.remove(os.path.join(self.test_data_dir, f))
        os.rmdir(self.test_data_dir)

    def test_connect_and_disconnect(self):
        self.analytics.disconnect()
        self.assertIsNone(self.analytics.conn)
        self.analytics.connect()
        self.assertIsNotNone(self.analytics.conn)

    def test_execute_query(self):
        result = self.analytics.execute_query("SELECT COUNT(*) FROM sales_initial")
        self.assertEqual(result[0][0], 3)

    def test_fetch_data(self):
        data = self.analytics.fetch_data("SELECT * FROM sales_initial WHERE product = 'Laptop'")
        self.assertEqual(len(data), 1)
        self.assertEqual(data['product'].iloc[0], 'Laptop')

    def test_create_table_from_query(self):
        self.assertTrue(self.analytics.create_table_from_query("high_value_sales", "SELECT * FROM sales_initial WHERE amount > 100"))
        result = self.analytics.fetch_data("SELECT COUNT(*) FROM high_value_sales")
        self.assertEqual(result[0][0], 1)
        self.assertIn("high_value_sales", self.analytics.list_metadata())

    def test_ingest_csv_create_table(self):
        new_csv_path = os.path.join(self.test_data_dir, "new_sales.csv")
        with open(new_csv_path, "w") as f:
            f.write("id,item,price\n")
            f.write("1,Book,20.00\n")
        self.assertTrue(self.analytics.ingest_csv(new_csv_path, "new_sales_table", create_table=True))
        result = self.analytics.fetch_data("SELECT COUNT(*) FROM new_sales_table")
        self.assertEqual(result[0][0], 1)
        self.assertIn("new_sales_table", self.analytics.list_metadata())

    def test_ingest_csv_append_data(self):
        # Ingestar no sales_initial (já criado no setUp)
        append_csv_path = os.path.join(self.test_data_dir, "append_sales.csv")
        with open(append_csv_path, "w") as f:
            f.write("transaction_id,product,amount,customer_id,sale_date\n")
            f.write("4,Tablet,500.00,C003,2025-01-04\n")
        self.assertTrue(self.analytics.ingest_csv(append_csv_path, "sales_initial", create_table=False))
        result = self.analytics.fetch_data("SELECT COUNT(*) FROM sales_initial")
        self.assertEqual(result[0][0], 4)

    def test_ingest_parquet(self):
        self.assertTrue(self.analytics.ingest_parquet(self.sample_parquet_path, "products_table"))
        result = self.analytics.fetch_data("SELECT COUNT(*) FROM products_table")
        self.assertEqual(result[0][0], 2)
        self.assertIn("products_table", self.analytics.list_metadata())

    def test_ingest_json(self):
        self.assertTrue(self.analytics.ingest_json(self.sample_json_path, "customers_table"))
        result = self.analytics.fetch_data("SELECT COUNT(*) FROM customers_table")
        self.assertEqual(result[0][0], 2)
        self.assertIn("customers_table", self.analytics.list_metadata())

    def test_create_view(self):
        self.assertTrue(self.analytics.create_view("product_summary", "SELECT product, SUM(amount) as total_amount FROM sales_initial GROUP BY product"))
        result = self.analytics.fetch_data("SELECT * FROM product_summary")
        self.assertEqual(len(result), 3)
        self.assertIn("product_summary", self.analytics.list_metadata())

    def test_export_to_csv(self):
        output_file = os.path.join(self.test_data_dir, "exported_sales.csv")
        self.assertTrue(self.analytics.export_to_csv("SELECT * FROM sales_initial", output_file))
        self.assertTrue(os.path.exists(output_file))
        with open(output_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 4) # Header + 3 rows

    def test_run_sql_script(self):
        script_path = os.path.join(self.test_data_dir, "test_script.sql")
        with open(script_path, "w") as f:
            f.write("CREATE TABLE test_script_table (col1 INTEGER);\n")
            f.write("INSERT INTO test_script_table VALUES (100);\n")
        self.assertTrue(self.analytics.run_sql_script(script_path))
        result = self.analytics.fetch_data("SELECT * FROM test_script_table")
        self.assertEqual(result['col1'].iloc[0], 100)
        self.assertIn("test_script_table", self.analytics.list_metadata())

    def test_vacuum_database(self):
        self.assertTrue(self.analytics.vacuum_database())
        # Não há um resultado direto para verificar, mas a execução sem erro é o suficiente

    def test_get_table_schema(self):
        schema = self.analytics.get_table_schema("sales_initial")
        self.assertIn(("transaction_id", "VARCHAR"), schema)
        self.assertIn(("product", "VARCHAR"), schema)
        self.assertIn(("amount", "DOUBLE"), schema)

    def test_list_metadata(self):
        metadata = self.analytics.list_metadata()
        self.assertIn("sales_initial", metadata)
        self.assertEqual(metadata["sales_initial"]["type"], "table")
        self.assertIsNotNone(metadata["sales_initial"]["schema"])

if __name__ == '__main__':
    unittest.main(verbosity=2)

