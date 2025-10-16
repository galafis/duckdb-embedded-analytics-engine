# API Reference

## DuckDBAnalytics Class

The main class for interacting with DuckDB.

### Constructor

```python
DuckDBAnalytics(db_path: str = ":memory:")
```

**Parameters:**
- `db_path` (str): Path to the DuckDB database file. Use `:memory:` for an in-memory database.

**Example:**
```python
# Persistent database
analytics = DuckDBAnalytics("my_analytics.duckdb")

# In-memory database
analytics = DuckDBAnalytics(":memory:")
```

---

### Connection Methods

#### `connect()`

Connects to the DuckDB database.

**Returns:** None

**Example:**
```python
analytics.connect()
```

#### `disconnect()`

Disconnects from the DuckDB database.

**Returns:** None

**Example:**
```python
analytics.disconnect()
```

---

### Query Execution Methods

#### `execute_query(query: str) -> Optional[List[Tuple[Any, ...]]]`

Executes a SQL query and returns the results.

**Parameters:**
- `query` (str): SQL query to execute

**Returns:** List of tuples with query results, or None if no results

**Example:**
```python
result = analytics.execute_query("SELECT * FROM sales")
```

#### `fetch_data(query: str) -> pd.DataFrame`

Executes a query and returns results as a Pandas DataFrame.

**Parameters:**
- `query` (str): SQL query to execute

**Returns:** Pandas DataFrame with query results

**Example:**
```python
df = analytics.fetch_data("SELECT * FROM sales WHERE amount > 100")
print(df.head())
```

---

### Data Ingestion Methods

#### `ingest_csv(file_path: str, table_name: str, create_table: bool = True) -> bool`

Ingests data from a CSV file into DuckDB.

**Parameters:**
- `file_path` (str): Path to the CSV file
- `table_name` (str): Name of the table to create/insert into
- `create_table` (bool): If True, creates a new table. If False, appends to existing table

**Returns:** True if successful, False otherwise

**Example:**
```python
analytics.ingest_csv("data/sales.csv", "sales")
```

#### `import_from_csv(file_path: str, table_name: str, create_table: bool = True) -> bool`

Alias for `ingest_csv()`.

#### `ingest_json(file_path: str, table_name: str, create_table: bool = True) -> bool`

Ingests data from a JSON file into DuckDB.

**Parameters:**
- `file_path` (str): Path to the JSON file
- `table_name` (str): Name of the table to create/insert into
- `create_table` (bool): If True, creates a new table. If False, appends to existing table

**Returns:** True if successful, False otherwise

**Example:**
```python
analytics.ingest_json("data/customers.json", "customers")
```

#### `ingest_parquet(file_path: str, table_name: str, create_table: bool = True) -> bool`

Ingests data from a Parquet file into DuckDB.

**Parameters:**
- `file_path` (str): Path to the Parquet file
- `table_name` (str): Name of the table to create/insert into
- `create_table` (bool): If True, creates a new table. If False, appends to existing table

**Returns:** True if successful, False otherwise

**Example:**
```python
analytics.ingest_parquet("data/products.parquet", "products")
```

---

### Table and View Management

#### `create_table_from_query(table_name: str, query: str) -> bool`

Creates a new table from a query result.

**Parameters:**
- `table_name` (str): Name of the new table
- `query` (str): SQL query to generate table data

**Returns:** True if successful, False otherwise

**Example:**
```python
analytics.create_table_from_query("high_value_sales", 
    "SELECT * FROM sales WHERE amount > 1000")
```

#### `create_view(view_name: str, query: str) -> bool`

Creates a view from a query.

**Parameters:**
- `view_name` (str): Name of the view
- `query` (str): SQL query for the view

**Returns:** True if successful, False otherwise

**Example:**
```python
analytics.create_view("sales_summary",
    "SELECT product, SUM(amount) as total FROM sales GROUP BY product")
```

---

### Data Export Methods

#### `export_to_csv(query: str, output_file: str) -> bool`

Exports query results to a CSV file.

**Parameters:**
- `query` (str): SQL query to execute
- `output_file` (str): Path to the output CSV file

**Returns:** True if successful, False otherwise

**Example:**
```python
analytics.export_to_csv("SELECT * FROM sales", "output/sales.csv")
```

---

### Metadata and Schema Methods

#### `get_table_schema(table_name: str) -> List[Tuple[str, str]]`

Returns the schema of a table or view.

**Parameters:**
- `table_name` (str): Name of the table or view

**Returns:** List of tuples with (column_name, data_type)

**Example:**
```python
schema = analytics.get_table_schema("sales")
for column_name, data_type in schema:
    print(f"{column_name}: {data_type}")
```

#### `list_metadata() -> Dict[str, Dict[str, Any]]`

Lists all metadata of managed tables and views.

**Returns:** Dictionary with metadata information

**Example:**
```python
metadata = analytics.list_metadata()
print(metadata)
```

---

### Utility Methods

#### `run_sql_script(script_path: str) -> bool`

Executes a SQL script file containing multiple commands.

**Parameters:**
- `script_path` (str): Path to the SQL script file

**Returns:** True if successful, False otherwise

**Example:**
```python
analytics.run_sql_script("scripts/setup_schema.sql")
```

#### `vacuum_database() -> bool`

Optimizes the database by reclaiming space and improving performance.

**Returns:** True if successful, False otherwise

**Example:**
```python
analytics.vacuum_database()
```

---

## AdvancedDuckDBAnalytics Class

Extended class with synthetic data generation capabilities.

### Additional Methods

#### `generate_synthetic_data(num_customers: int = 100, num_products: int = 50, num_transactions: int = 1000)`

Generates synthetic data for testing and demonstration.

**Parameters:**
- `num_customers` (int): Number of customers to generate
- `num_products` (int): Number of products to generate
- `num_transactions` (int): Number of transactions to generate

**Example:**
```python
from src.advanced_example import AdvancedDuckDBAnalytics

analytics = AdvancedDuckDBAnalytics("test.duckdb")
analytics.connect()
analytics.generate_synthetic_data(num_customers=50, num_products=25, num_transactions=500)
```

#### `perform_advanced_analytics()`

Performs pre-configured advanced analytical queries.

**Example:**
```python
analytics.perform_advanced_analytics()
```

---

## Best Practices

1. **Always use context managers or try-finally**: Ensure `disconnect()` is called
2. **Check return values**: Many methods return boolean success indicators
3. **Use parameterized queries**: For dynamic data (though DuckDB handles this well)
4. **Monitor memory**: In-memory databases are fast but limited by RAM
5. **Use appropriate data types**: Let DuckDB infer types or specify them explicitly
