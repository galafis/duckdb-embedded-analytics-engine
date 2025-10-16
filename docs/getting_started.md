# Getting Started with DuckDB Embedded Analytics Engine

## 🚀 Quick Start Guide

### Installation

1. Clone the repository:
```bash
git clone https://github.com/galafis/duckdb-embedded-analytics-engine.git
cd duckdb-embedded-analytics-engine
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Your First Query

Create a simple Python script to get started:

```python
from src.duckdb_analytics import DuckDBAnalytics

# Create an in-memory database
analytics = DuckDBAnalytics(":memory:")
analytics.connect()

# Create a simple table
analytics.execute_query("""
    CREATE TABLE users (
        id INTEGER,
        name VARCHAR,
        age INTEGER
    )
""")

# Insert data
analytics.execute_query("""
    INSERT INTO users VALUES 
    (1, 'Alice', 30),
    (2, 'Bob', 25),
    (3, 'Charlie', 35)
""")

# Query data
result = analytics.fetch_data("SELECT * FROM users WHERE age > 25")
print(result)

analytics.disconnect()
```

## 📊 Working with Different Data Formats

### CSV Files

```python
# Import CSV data
analytics.ingest_csv("data/examples/sample_sales.csv", "sales")

# Query the imported data
sales_summary = analytics.fetch_data("""
    SELECT region, SUM(amount) as total_sales
    FROM sales
    GROUP BY region
    ORDER BY total_sales DESC
""")
print(sales_summary)
```

### JSON Files

```python
# Import JSON data
analytics.ingest_json("data/examples/sample_customers.json", "customers")

# Query JSON data
customers = analytics.fetch_data("SELECT * FROM customers WHERE state = 'NY'")
print(customers)
```

### Parquet Files

```python
# Import Parquet data
analytics.ingest_parquet("path/to/data.parquet", "products")

# Query Parquet data
products = analytics.fetch_data("SELECT * FROM products LIMIT 10")
print(products)
```

## 🔍 Advanced Queries

### Joins

```python
# Join multiple tables
query = """
    SELECT 
        s.transaction_id,
        s.product,
        s.amount,
        c.name as customer_name,
        c.city
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    ORDER BY s.amount DESC
"""
result = analytics.fetch_data(query)
print(result)
```

### Aggregations

```python
# Complex aggregations
query = """
    SELECT 
        region,
        product,
        COUNT(*) as num_sales,
        SUM(amount) as total_revenue,
        AVG(amount) as avg_sale
    FROM sales
    GROUP BY region, product
    ORDER BY total_revenue DESC
"""
result = analytics.fetch_data(query)
print(result)
```

### Window Functions

```python
# Window functions for ranking
query = """
    SELECT 
        product,
        amount,
        sale_date,
        ROW_NUMBER() OVER (PARTITION BY product ORDER BY amount DESC) as rank
    FROM sales
"""
result = analytics.fetch_data(query)
print(result)
```

## 💾 Creating Views

```python
# Create a view for frequently used queries
analytics.create_view("high_value_sales", """
    SELECT * FROM sales WHERE amount > 500
""")

# Query the view
high_value = analytics.fetch_data("SELECT * FROM high_value_sales")
print(high_value)
```

## 📤 Exporting Data

```python
# Export query results to CSV
analytics.export_to_csv(
    "SELECT * FROM sales WHERE region = 'North'",
    "output/north_sales.csv"
)
```

## 🔧 Metadata Management

```python
# Get table schema
schema = analytics.get_table_schema("sales")
print("Table Schema:", schema)

# List all managed metadata
metadata = analytics.list_metadata()
print("Metadata:", metadata)
```

## 🏃 Running Examples

The repository includes complete examples:

```bash
# Run the basic example
python src/duckdb_analytics.py

# Run the advanced example with synthetic data
python run_advanced_example.py
```

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## 📚 Next Steps

- Read the [API Reference](api_reference.md) for detailed documentation
- Check out the [Use Cases](use_cases.md) for real-world examples
- Learn about [Performance Optimization](performance.md)

## 💡 Tips

1. **Use in-memory databases for testing**: `DuckDBAnalytics(":memory:")`
2. **Always disconnect**: Call `analytics.disconnect()` when done
3. **Leverage DuckDB's SQL**: Full SQL support with extensions
4. **Check schemas**: Use `get_table_schema()` to verify data types
5. **Use views**: Create views for complex, reusable queries
