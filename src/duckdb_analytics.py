
"""
DuckDB Embedded Analytics Engine
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo implementa uma classe para interagir com o DuckDB como um motor de análise embutido.
"""

import duckdb
import pandas as pd
import os
from typing import List, Tuple, Any, Optional

class DuckDBAnalytics:
    """
    Classe para gerenciar interações com um banco de dados DuckDB.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn: Optional[duckdb.DuckDBPyConnection] = None

    def connect(self):
        """Conecta ao banco de dados DuckDB."""
        if self.conn is None:
            self.conn = duckdb.connect(database=self.db_path, read_only=False)
            print(f"✓ Conectado ao DuckDB em {self.db_path}")

    def disconnect(self):
        """Desconecta do banco de dados DuckDB."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print(f"✓ Desconectado do DuckDB em {self.db_path}")

    def execute_query(self, query: str) -> Optional[List[Tuple[Any, ...]]]:
        """Executa uma query SQL e retorna os resultados, se houver."""
        if not self.conn:
            raise ConnectionError("Não conectado ao DuckDB. Chame connect() primeiro.")
        try:
            result = self.conn.execute(query)
            if result.description:
                return result.fetchall()
            return None
        except duckdb.Error as e:
            print(f"✗ Erro ao executar query: {e}")
            return None

    def fetch_data(self, query: str) -> pd.DataFrame:
        """Executa uma query e retorna os resultados como um DataFrame Pandas."""
        if not self.conn:
            raise ConnectionError("Não conectado ao DuckDB. Chame connect() primeiro.")
        try:
            return self.conn.execute(query).fetchdf()
        except duckdb.Error as e:
            print(f"✗ Erro ao buscar dados: {e}")
            return pd.DataFrame()

    def create_view(self, view_name: str, query: str) -> bool:
        """Cria uma view a partir de uma query."""
        if not self.conn:
            raise ConnectionError("Não conectado ao DuckDB. Chame connect() primeiro.")
        try:
            self.conn.execute(f"CREATE OR REPLACE VIEW {view_name} AS {query}")
            print(f"✓ View \'{view_name}\' criada com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao criar view \'{view_name}\': {e}")
            return False

    def export_to_csv(self, query: str, output_file: str) -> bool:
        """Exporta os resultados de uma query para um arquivo CSV."""
        if not self.conn:
            raise ConnectionError("Não conectado ao DuckDB. Chame connect() primeiro.")
        try:
            self.conn.execute(f"COPY ({query}) TO \'{output_file}\' (HEADER, DELIMITER ',')")
            print(f"✓ Dados exportados para \'{output_file}\' com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao exportar para CSV: {e}")
            return False

    def import_from_csv(self, input_file: str, table_name: str) -> bool:
        """Importa dados de um arquivo CSV para uma tabela."""
        if not self.conn:
            raise ConnectionError("Não conectado ao DuckDB. Chame connect() primeiro.")
        if not os.path.exists(input_file):
            print(f"✗ Erro: Arquivo CSV \'{input_file}\' não encontrado.")
            return False
        try:
            self.conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM '{input_file}'")
            print(f"✓ Dados importados de \'{input_file}\' para a tabela '{table_name}\' com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao importar de CSV: {e}")
            return False

    def get_table_schema(self, table_name: str) -> List[Tuple[str, str]]:
        """Retorna o esquema de uma tabela."""
        if not self.conn:
            raise ConnectionError("Não conectado ao DuckDB. Chame connect() primeiro.")
        try:
            schema_df = self.conn.execute(f"PRAGMA table_info('{table_name}')").fetchdf()
            return [(row["name"], row["type"]) for index, row in schema_df.iterrows()]
        except duckdb.Error as e:
            print(f"✗ Erro ao obter esquema da tabela '{table_name}\': {e}")
            return []


if __name__ == "__main__":
    print("=" * 60)
    print("DuckDB Embedded Analytics Engine - Example")
    print("=" * 60)

    analytics = DuckDBAnalytics("my_analytics.duckdb")
    analytics.connect()

    # Criar tabela de exemplo
    analytics.execute_query("DROP TABLE IF EXISTS sales")
    analytics.execute_query("""
        CREATE TABLE sales (
            id INTEGER,
            product VARCHAR,
            amount DOUBLE,
            sale_date DATE
        )
    """)
    analytics.execute_query("""
        INSERT INTO sales VALUES 
        (1, 'Laptop', 1200.00, '2025-01-01'), 
        (2, 'Mouse', 25.00, '2025-01-02'), 
        (3, 'Keyboard', 75.00, '2025-01-03'), 
        (4, 'Laptop', 1500.00, '2025-01-04')
    """)

    # Analytics query
    print("\nTop 5 Products by Revenue:")
    result_df = analytics.fetch_data("""
        SELECT 
            product,
            COUNT(*) as total_sales,
            SUM(amount) as revenue,
            AVG(amount) as avg_sale
        FROM sales
        GROUP BY product
        ORDER BY revenue DESC
        LIMIT 5
    """)
    print(result_df)

    # Criar e usar uma view
    analytics.create_view("product_summary", "SELECT product, SUM(amount) as total_revenue FROM sales GROUP BY product")
    print("\nDados da View 'product_summary':")
    print(analytics.fetch_data("SELECT * FROM product_summary"))

    # Exportar para CSV
    analytics.export_to_csv("SELECT * FROM sales", "sales_data.csv")
    if os.path.exists("sales_data.csv"):
        print("Conteúdo de sales_data.csv:")
        with open("sales_data.csv", "r") as f:
            print(f.read())
        os.remove("sales_data.csv")

    # Importar de CSV
    with open("new_products.csv", "w") as f:
        f.write("id,product,amount,sale_date\n")
        f.write("5,Monitor,300.00,2025-01-05\n")
    analytics.import_from_csv("new_products.csv", "new_sales_table")
    print("\nDados da tabela 'new_sales_table':")
    print(analytics.fetch_data("SELECT * FROM new_sales_table"))
    if os.path.exists("new_products.csv"):
        os.remove("new_products.csv")

    # Obter esquema da tabela
    print("\nEsquema da tabela 'sales':")
    print(analytics.get_table_schema("sales"))

    analytics.disconnect()

