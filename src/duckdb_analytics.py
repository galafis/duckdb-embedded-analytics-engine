
"""
DuckDB Embedded Analytics Engine
Author: Gabriel Demetrios Lafis
Year: 2025

Este módulo implementa uma classe para interagir com o DuckDB como um motor de análise embutido,
com funcionalidades aprimoradas para ingestão de dados, consultas avançadas e transformações.
"""

import duckdb
import pandas as pd
import os
from typing import List, Tuple, Any, Optional, Dict
from datetime import datetime

class DuckDBAnalytics:
    """
    Classe para gerenciar interações com um banco de dados DuckDB.
    Oferece funcionalidades para conexão, execução de queries, ingestão de dados
    de diferentes formatos (CSV, Parquet, JSON), criação de views, exportação
    e gerenciamento de metadados básicos.
    """
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.conn: Optional[duckdb.DuckDBPyConnection] = None
        self.metadata: Dict[str, Dict[str, Any]] = {}

    def connect(self):
        """Conecta ao banco de dados DuckDB."""
        if self.conn is None:
            try:
                self.conn = duckdb.connect(database=self.db_path, read_only=False)
                print(f"✓ Conectado ao DuckDB em {self.db_path}")
            except duckdb.Error as e:
                print(f"✗ Erro ao conectar ao DuckDB: {e}")
                self.conn = None

    def disconnect(self):
        """Desconecta do banco de dados DuckDB."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print(f"✓ Desconectado do DuckDB em {self.db_path}")

    def execute_query(self, query: str) -> Optional[List[Tuple[Any, ...]]]:
        """Executa uma query SQL e retorna os resultados, se houver."""
        if not self.conn:
            self.connect()
        if not self.conn:
            return None
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
            self.connect()
        if not self.conn:
            return pd.DataFrame()
        try:
            return self.conn.execute(query).fetchdf()
        except duckdb.Error as e:
            print(f"✗ Erro ao buscar dados: {e}")
            return pd.DataFrame()

    def create_table_from_query(self, table_name: str, query: str) -> bool:
        """
        Cria uma nova tabela a partir dos resultados de uma query.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return False
        try:
            self.conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS {query}")
            self._update_metadata(table_name, "table", query)
            print(f"✓ Tabela \'{table_name}\' criada com sucesso a partir da query.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao criar tabela \'{table_name}\' a partir da query: {e}")
            return False

    def ingest_csv(self, file_path: str, table_name: str, create_table: bool = True) -> bool:
        """
        Ingere dados de um arquivo CSV para uma tabela DuckDB.
        Se create_table for True, cria a tabela. Caso contrário, insere na tabela existente.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return False
        if not os.path.exists(file_path):
            print(f"✗ Erro: Arquivo CSV \'{file_path}\' não encontrado.")
            return False
        try:
            if create_table:
                self.conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM \'{file_path}\'")
                self._update_metadata(table_name, "table", f"Ingestão de CSV: {file_path}")
                print(f"✓ Dados importados de \'{file_path}\' para a nova tabela \'{table_name}\' com sucesso.")
            else:
                self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM \'{file_path}\'")
                print(f"✓ Dados inseridos de \'{file_path}\' na tabela existente \'{table_name}\' com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao ingerir CSV para \'{table_name}\' de \'{file_path}\' : {e}")
            return False

    def ingest_parquet(self, file_path: str, table_name: str, create_table: bool = True) -> bool:
        """
        Ingere dados de um arquivo Parquet para uma tabela DuckDB.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return False
        if not os.path.exists(file_path):
            print(f"✗ Erro: Arquivo Parquet \'{file_path}\' não encontrado.")
            return False
        try:
            if create_table:
                self.conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM \'{file_path}\'")
                self._update_metadata(table_name, "table", f"Ingestão de Parquet: {file_path}")
                print(f"✓ Dados importados de \'{file_path}\' para a nova tabela \'{table_name}\' com sucesso.")
            else:
                self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM \'{file_path}\'")
                print(f"✓ Dados inseridos de \'{file_path}\' na tabela existente \'{table_name}\' com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao ingerir Parquet para \'{table_name}\' de \'{file_path}\' : {e}")
            return False

    def ingest_json(self, file_path: str, table_name: str, create_table: bool = True) -> bool:
        """
        Ingere dados de um arquivo JSON para uma tabela DuckDB.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return False
        if not os.path.exists(file_path):
            print(f"✗ Erro: Arquivo JSON \'{file_path}\' não encontrado.")
            return False
        try:
            if create_table:
                self.conn.execute(f"CREATE OR REPLACE TABLE {table_name} AS SELECT * FROM read_json_auto(\'{file_path}\')")
                self._update_metadata(table_name, "table", f"Ingestão de JSON: {file_path}")
                print(f"✓ Dados importados de \'{file_path}\' para a nova tabela \'{table_name}\' com sucesso.")
            else:
                self.conn.execute(f"INSERT INTO {table_name} SELECT * FROM read_json_auto(\'{file_path}\')")
                print(f"✓ Dados inseridos de \'{file_path}\' na tabela existente \'{table_name}\' com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao ingerir JSON para \'{table_name}\' de \'{file_path}\' : {e}")
            return False

    def create_view(self, view_name: str, query: str) -> bool:
        """
        Cria uma view a partir de uma query.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return False
        try:
            self.conn.execute(f"CREATE OR REPLACE VIEW {view_name} AS {query}")
            self._update_metadata(view_name, "view", query)
            print(f"✓ View \'{view_name}\' criada com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao criar view \'{view_name}\' : {e}")
            return False

    def export_to_csv(self, query: str, output_file: str) -> bool:
        """
        Exporta os resultados de uma query para um arquivo CSV.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return False
        try:
            self.conn.execute(f"COPY ({query}) TO \'{output_file}\' (HEADER, DELIMITER \\',\\')")
            print(f"✓ Dados exportados para \'{output_file}\' com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao exportar para CSV: {e}")
            return False

    def run_sql_script(self, script_path: str) -> bool:
        """
        Executa um script SQL contendo múltiplos comandos.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return False
        if not os.path.exists(script_path):
            print(f"✗ Erro: Arquivo de script SQL \'{script_path}\' não encontrado.")
            return False
        try:
            with open(script_path, 'r') as f:
                sql_script = f.read()
            self.conn.execute(sql_script)
            print(f"✓ Script SQL \'{script_path}\' executado com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao executar script SQL: {e}")
            return False

    def vacuum_database(self) -> bool:
        """
        Otimiza o banco de dados DuckDB, recuperando espaço e melhorando a performance.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return False
        try:
            self.conn.execute("VACUUM;")
            print("✓ Banco de dados DuckDB otimizado (VACUUM) com sucesso.")
            return True
        except duckdb.Error as e:
            print(f"✗ Erro ao otimizar banco de dados: {e}")
            return False

    def get_table_schema(self, table_name: str) -> List[Tuple[str, str]]:
        """
        Retorna o esquema de uma tabela ou view.
        """
        if not self.conn:
            self.connect()
        if not self.conn:
            return []
        try:
            schema_df = self.conn.execute(f"PRAGMA table_info(\'{table_name}\')").fetchdf()
            return [(row["name"], row["type"]) for index, row in schema_df.iterrows()]
        except duckdb.Error as e:
            print(f"✗ Erro ao obter esquema da tabela/view \'{table_name}\' : {e}")
            return []

    def _update_metadata(self, name: str, obj_type: str, source: str):
        """
        Atualiza os metadados de uma tabela ou view.
        """
        self.metadata[name] = {
            "type": obj_type,
            "created_at": datetime.now().isoformat(),
            "source": source,
            "schema": self.get_table_schema(name)
        }

    def list_metadata(self) -> Dict[str, Dict[str, Any]]:
        """
        Lista todos os metadados de tabelas e views gerenciadas.
        """
        return self.metadata


if __name__ == "__main__":
    print("=" * 60)
    print("DuckDB Embedded Analytics Engine - Advanced Example")
    print("=" * 60)

    # Garante que o diretório de dados exista
    data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(data_dir, exist_ok=True)

    # Criar arquivos de dados de exemplo
    sample_csv_path = os.path.join(data_dir, "sample_sales.csv")
    with open(sample_csv_path, "w") as f:
        f.write("transaction_id,product,amount,customer_id,sale_date\n")
        f.write("1,Laptop,1200.00,C001,2025-01-01\n")
        f.write("2,Mouse,25.00,C002,2025-01-02\n")
        f.write("3,Keyboard,75.00,C001,2025-01-03\n")
        f.write("4,Monitor,300.00,C003,2025-01-04\n")

    sample_json_path = os.path.join(data_dir, "sample_customers.json")
    with open(sample_json_path, "w") as f:
        f.write("[
  {\"customer_id\": \"C001\", \"name\": \"Alice\", \"city\": \"NY\"},
  {\"customer_id\": \"C002\", \"name\": \"Bob\", \"city\": \"LA\"},
  {\"customer_id\": \"C003\", \"name\": \"Charlie\", \"city\": \"NY\"}
]")

    # Criar um DataFrame Pandas e salvar como Parquet
    df_products = pd.DataFrame({
        "product_id": ["P1", "P2", "P3"],
        "product_name": ["Laptop", "Mouse", "Keyboard"],
        "category": ["Electronics", "Electronics", "Peripherals"]
    })
    sample_parquet_path = os.path.join(data_dir, "sample_products.parquet")
    df_products.to_parquet(sample_parquet_path, index=False)

    analytics = DuckDBAnalytics(os.path.join(data_dir, "my_analytics.duckdb"))
    analytics.connect()

    # 1. Ingestão de dados de diferentes fontes
    print("\n--- Ingestão de Dados ---")
    analytics.ingest_csv(sample_csv_path, "sales")
    analytics.ingest_json(sample_json_path, "customers")
    analytics.ingest_parquet(sample_parquet_path, "products")

    # 2. Consultas Avançadas (JOINs e Agregações)
    print("\n--- Consultas Avançadas ---")
    print("Total de vendas por cliente e cidade:")
    query_sales_by_customer_city = """
        SELECT
            c.name AS customer_name,
            c.city,
            SUM(s.amount) AS total_spent,
            COUNT(s.transaction_id) AS total_transactions
        FROM sales s
        JOIN customers c ON s.customer_id = c.customer_id
        GROUP BY c.name, c.city
        ORDER BY total_spent DESC
    """
    print(analytics.fetch_data(query_sales_by_customer_city))

    print("\nProdutos mais vendidos por categoria:")
    query_top_products_by_category = """
        SELECT
            p.category,
            p.product_name,
            SUM(s.amount) AS revenue
        FROM sales s
        JOIN products p ON s.product = p.product_name
        GROUP BY p.category, p.product_name
        ORDER BY revenue DESC
    """
    print(analytics.fetch_data(query_top_products_by_category))

    # 3. Data Transformation (CTAS - Create Table As Select)
    print("\n--- Transformação de Dados (CTAS) ---")
    analytics.create_table_from_query("customer_summary", """
        SELECT
            c.customer_id,
            c.name,
            c.city,
            SUM(s.amount) AS total_lifetime_value,
            COUNT(s.transaction_id) AS total_orders
        FROM customers c
        LEFT JOIN sales s ON c.customer_id = s.customer_id
        GROUP BY c.customer_id, c.name, c.city
    """)
    print("Conteúdo da tabela 'customer_summary':")
    print(analytics.fetch_data("SELECT * FROM customer_summary"))

    # 4. Gerenciamento de Metadados
    print("\n--- Metadados Gerenciados ---")
    print(json.dumps(analytics.list_metadata(), indent=2))

    # 5. Exportar dados transformados
    print("\n--- Exportando Dados Transformados ---")
    export_path = os.path.join(data_dir, "customer_summary.csv")
    analytics.export_to_csv("SELECT * FROM customer_summary", export_path)
    if os.path.exists(export_path):
        print(f"Dados de 'customer_summary' exportados para {export_path}")
        with open(export_path, "r") as f:
            print(f.read())

    # 6. Executar script SQL (exemplo de limpeza)
    print("\n--- Executando Script SQL ---")
    script_path = os.path.join(data_dir, "cleanup.sql")
    with open(script_path, "w") as f:
        f.write("DROP TABLE IF EXISTS sales;\n")
        f.write("DROP TABLE IF EXISTS customers;\n")
        f.write("DROP TABLE IF EXISTS products;\n")
        f.write("DROP TABLE IF EXISTS customer_summary;\n")
    analytics.run_sql_script(script_path)
    print("Tabelas limpas.")

    analytics.disconnect()

    # Limpar arquivos de dados de exemplo
    os.remove(sample_csv_path)
    os.remove(sample_json_path)
    os.remove(sample_parquet_path)
    os.remove(export_path)
    os.remove(script_path)
    if os.path.exists(os.path.join(data_dir, "my_analytics.duckdb")):
        os.remove(os.path.join(data_dir, "my_analytics.duckdb"))
    if os.path.exists(os.path.join(data_dir, "my_analytics.duckdb.wal")):
        os.remove(os.path.join(data_dir, "my_analytics.duckdb.wal"))

    print("=" * 60)
    print("Exemplo Concluído")
    print("=" * 60)

