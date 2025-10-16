import unittest
import sys
import os
import duckdb
import pandas as pd
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from duckdb_analytics import DuckDBAnalytics

class TestDuckDBAnalyticsIntegration(unittest.TestCase):
    def setUp(self):
        self.test_db_path = "test_analytics_integration.duckdb"
        self.test_data_dir = "test_data_integration"
        os.makedirs(self.test_data_dir, exist_ok=True)

        self.analytics = DuckDBAnalytics(self.test_db_path)
        self.analytics.connect()

        # Criar arquivos de dados de exemplo para ingestão
        self.sample_csv_path = os.path.join(self.test_data_dir, "sample_sales_integration.csv")
        with open(self.sample_csv_path, "w") as f:
            f.write("transaction_id,product,amount,customer_id,sale_date\n")
            f.write("1,Laptop,1200.00,C001,2025-01-01\n")
            f.write("2,Mouse,25.00,C002,2025-01-02\n")
            f.write("3,Keyboard,75.00,C001,2025-01-03\n")
            f.write("4,Monitor,300.00,C003,2025-01-04\n")

        self.sample_json_path = os.path.join(self.test_data_dir, "sample_customers_integration.json")
        with open(self.sample_json_path, "w") as f:
            f.write('[{"customer_id": "C001", "name": "Alice", "city": "NY"}, {"customer_id": "C002", "name": "Bob", "city": "LA"}, {"customer_id": "C003", "name": "Charlie", "city": "NY"}]')

        self.sample_parquet_path = os.path.join(self.test_data_dir, "sample_products_integration.parquet")
        df_products = pd.DataFrame({
            "product_id": ["P1", "P2", "P3", "P4"],
            "product_name": ["Laptop", "Mouse", "Keyboard", "Monitor"],
            "category": ["Electronics", "Electronics", "Peripherals", "Electronics"]
        })
        df_products.to_parquet(self.sample_parquet_path, index=False)

    def tearDown(self):
        self.analytics.disconnect()
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        if os.path.exists(f"{self.test_db_path}.wal"):
            os.remove(f"{self.test_db_path}.wal")
        
        for f in os.listdir(self.test_data_dir):
            os.remove(os.path.join(self.test_data_dir, f))
        os.rmdir(self.test_data_dir)

    def test_full_ingestion_query_workflow(self):
        """Testa o fluxo completo de ingestão de dados de diferentes fontes e consultas"""
        # 1. Ingestão de CSV
        self.assertTrue(self.analytics.ingest_csv(self.sample_csv_path, "sales_data"))
        self.assertIn("sales_data", self.analytics.list_metadata())

        # 2. Ingestão de JSON
        self.assertTrue(self.analytics.ingest_json(self.sample_json_path, "customers_data"))
        self.assertIn("customers_data", self.analytics.list_metadata())

        # 3. Ingestão de Parquet
        self.assertTrue(self.analytics.ingest_parquet(self.sample_parquet_path, "products_data"))
        self.assertIn("products_data", self.analytics.list_metadata())

        # 4. Criar uma view complexa unindo as tabelas
        join_query = """
            SELECT
                s.transaction_id,
                s.product,
                s.amount,
                s.sale_date,
                c.name AS customer_name,
                c.city AS customer_city,
                p.category AS product_category
            FROM sales_data AS s
            JOIN customers_data AS c ON s.customer_id = c.customer_id
            JOIN products_data AS p ON s.product = p.product_name
        """
        self.assertTrue(self.analytics.create_view("sales_customer_product_view", join_query))
        self.assertIn("sales_customer_product_view", self.analytics.list_metadata())

        # 5. Consultar a view e verificar os resultados
        result_df = self.analytics.fetch_data("SELECT * FROM sales_customer_product_view WHERE customer_city = 'NY'")
        self.assertIsInstance(result_df, pd.DataFrame)
        self.assertEqual(len(result_df), 3) # C001 (Laptop, Keyboard) and C003 (Monitor)
        self.assertTrue(all(result_df["customer_city"] == "NY"))
        self.assertIn("Laptop", result_df["product"].values)
        self.assertIn("Keyboard", result_df["product"].values)
        self.assertIn("Monitor", result_df["product"].values)

        # 6. Criar uma tabela a partir de uma query agregada
        agg_query = """
            SELECT
                sale_date,
                SUM(amount) AS total_daily_sales,
                COUNT(DISTINCT transaction_id) AS num_transactions
            FROM sales_data
            GROUP BY sale_date
            ORDER BY sale_date
        """
        self.assertTrue(self.analytics.create_table_from_query("daily_sales_summary", agg_query))
        self.assertIn("daily_sales_summary", self.analytics.list_metadata())

        # 7. Verificar o conteúdo da tabela agregada
        summary_df = self.analytics.fetch_data("SELECT * FROM daily_sales_summary WHERE sale_date = '2025-01-01'")
        self.assertEqual(summary_df["total_daily_sales"].iloc[0], 1200.00)
        self.assertEqual(summary_df["num_transactions"].iloc[0], 1)

        # 8. Exportar dados para CSV
        output_csv = os.path.join(self.test_data_dir, "exported_summary.csv")
        self.assertTrue(self.analytics.export_to_csv("SELECT * FROM daily_sales_summary", output_csv))
        self.assertTrue(os.path.exists(output_csv))
        with open(output_csv, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 5) # Header + 4 rows

if __name__ == '__main__':
    unittest.main(verbosity=2)

