
import duckdb
import pandas as pd
import os
from faker import Faker
import random
from datetime import datetime, timedelta

class AdvancedDuckDBAnalytics:
    def __init__(self, db_path=":memory:"):
        self.db_path = db_path
        self.conn = None
        self.fake = Faker("pt_BR") # Usar Faker para dados em português do Brasil

    def connect(self):
        """Conecta ao banco de dados DuckDB."""
        self.conn = duckdb.connect(database=self.db_path, read_only=False)
        print(f"Conectado ao DuckDB em: {self.db_path}")

    def disconnect(self):
        """Desconecta do banco de dados DuckDB."""
        if self.conn:
            self.conn.close()
            print("Desconectado do DuckDB.")

    def execute_query(self, query):
        """Executa uma consulta SQL e retorna o resultado como DataFrame do Pandas."""
        if not self.conn:
            self.connect()
        return self.conn.execute(query).fetchdf()

    def generate_synthetic_data(self, num_customers=100, num_products=50, num_transactions=1000):
        """Gera dados sintéticos para clientes, produtos e transações."""
        print("Gerando dados sintéticos...")

        # Clientes
        customers_data = []
        for i in range(num_customers):
            customers_data.append({
                "customer_id": i + 1,
                "name": self.fake.name(),
                "email": self.fake.email(),
                "city": self.fake.city(),
                "state": self.fake.state_abbr(),
                "registration_date": self.fake.date_between(start_date="-5y", end_date="today").isoformat()
            })
        customers_df = pd.DataFrame(customers_data)
        self.conn.from_df(customers_df).create("customers")
        print(f"  {num_customers} clientes gerados e inseridos.")

        # Produtos
        products_data = []
        product_names = [self.fake.word().capitalize() + " " + self.fake.word() for _ in range(num_products)]
        for i in range(num_products):
            products_data.append({
                "product_id": i + 1,
                "product_name": product_names[i],
                "category": self.fake.random_element(elements=("Eletrônicos", "Livros", "Roupas", "Alimentos", "Casa")),
                "price": round(random.uniform(10.0, 1000.0), 2),
                "stock_quantity": random.randint(0, 500)
            })
        products_df = pd.DataFrame(products_data)
        self.conn.from_df(products_df).create("products")
        print(f"  {num_products} produtos gerados e inseridos.")

        # Transações
        transactions_data = []
        start_date = datetime.now() - timedelta(days=365)
        for i in range(num_transactions):
            transaction_date = self.fake.date_time_between(start_date=start_date, end_date="now")
            transactions_data.append({
                "transaction_id": i + 1,
                "customer_id": random.randint(1, num_customers),
                "product_id": random.randint(1, num_products),
                "quantity": random.randint(1, 5),
                "transaction_date": transaction_date.isoformat(),
                "payment_method": self.fake.random_element(elements=("Cartão de Crédito", "Boleto", "Pix", "Débito"))
            })
        transactions_df = pd.DataFrame(transactions_data)
        self.conn.from_df(transactions_df).create("transactions")
        print(f"  {num_transactions} transações geradas e inseridas.")

        print("Geração de dados sintéticos concluída.")

    def perform_advanced_analytics(self):
        """Executa consultas analíticas avançadas e demonstra funcionalidades do DuckDB."""
        print("\nExecutando análises avançadas...")

        # 1. Vendas totais por categoria de produto
        print("\n1. Vendas totais por categoria de produto:")
        query_sales_by_category = """
            SELECT
                p.category,
                SUM(t.quantity * p.price) AS total_sales_value
            FROM transactions t
            JOIN products p ON t.product_id = p.product_id
            GROUP BY p.category
            ORDER BY total_sales_value DESC
        """
        result = self.execute_query(query_sales_by_category)
        print(result)

        # 2. Clientes que mais gastaram (Top 10)
        print("\n2. Clientes que mais gastaram (Top 10):")
        query_top_customers = """
            SELECT
                c.name,
                c.city,
                SUM(t.quantity * p.price) AS total_spent
            FROM transactions t
            JOIN customers c ON t.customer_id = c.customer_id
            JOIN products p ON t.product_id = p.product_id
            GROUP BY c.name, c.city
            ORDER BY total_spent DESC
            LIMIT 10
        """
        result = self.execute_query(query_top_customers)
        print(result)

        # 3. Média de transações por cliente por cidade (usando Window Functions)
        print("\n3. Média de transações por cliente por cidade (usando Window Functions):")
        query_avg_transactions_per_customer_city = """
            WITH CustomerTransactions AS (
                SELECT
                    c.customer_id,
                    c.name,
                    c.city,
                    COUNT(t.transaction_id) AS num_transactions
                FROM customers c
                JOIN transactions t ON c.customer_id = t.customer_id
                GROUP BY c.customer_id, c.name, c.city
            )
            SELECT
                city,
                AVG(num_transactions) AS avg_transactions_per_customer
            FROM CustomerTransactions
            GROUP BY city
            ORDER BY avg_transactions_per_customer DESC
            LIMIT 5
        """
        result = self.execute_query(query_avg_transactions_per_customer_city)
        print(result)

        # 4. Produtos com baixo estoque e alta demanda (exemplo de subconsulta e JOIN)
        print("\n4. Produtos com baixo estoque e alta demanda:")
        query_low_stock_high_demand = """
            SELECT
                p.product_name,
                p.category,
                p.stock_quantity,
                SUM(t.quantity) AS total_quantity_sold
            FROM products p
            JOIN transactions t ON p.product_id = t.product_id
            WHERE p.stock_quantity < 100 -- Exemplo de 'baixo estoque'
            GROUP BY p.product_name, p.category, p.stock_quantity
            HAVING SUM(t.quantity) > 50 -- Exemplo de 'alta demanda'
            ORDER BY total_quantity_sold DESC
            LIMIT 5
        """
        result = self.execute_query(query_low_stock_high_demand)
        print(result)

        print("Análises avançadas concluídas.")

    def run_example(self):
        """Executa o fluxo completo do exemplo avançado."""
        db_file = "advanced_analytics.duckdb"
        if os.path.exists(db_file):
            os.remove(db_file)

        self.db_path = db_file
        self.connect()
        self.generate_synthetic_data()
        self.perform_advanced_analytics()
        self.disconnect()

        if os.path.exists(db_file):
            os.remove(db_file)

if __name__ == "__main__":
    advanced_analytics_example = AdvancedDuckDBAnalytics()
    advanced_analytics_example.run_example()

