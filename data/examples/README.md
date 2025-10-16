# Example Data Files

Este diretório contém arquivos de dados de exemplo para demonstrar as funcionalidades do DuckDB Embedded Analytics Engine.

## Arquivos Disponíveis

- **sample_sales.csv**: Dados de vendas de exemplo com transações, produtos, valores e regiões
- **sample_customers.json**: Informações de clientes em formato JSON

## Como Usar

```python
from src.duckdb_analytics import DuckDBAnalytics

analytics = DuckDBAnalytics("my_analytics.duckdb")
analytics.connect()

# Importar dados de exemplo
analytics.ingest_csv("data/examples/sample_sales.csv", "sales")
analytics.ingest_json("data/examples/sample_customers.json", "customers")

# Executar consultas
result = analytics.fetch_data("SELECT * FROM sales LIMIT 5")
print(result)

analytics.disconnect()
```

## Formatos Suportados

- CSV
- JSON
- Parquet
