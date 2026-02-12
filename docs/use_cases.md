# Real-World Use Cases

## 📊 Business Intelligence Dashboard

### Scenario
Create a lightweight BI dashboard for sales analysis without setting up a full database server.

### Implementation

```python
from src.duckdb_analytics import DuckDBAnalytics
import pandas as pd

class SalesDashboard:
    def __init__(self):
        self.analytics = DuckDBAnalytics(":memory:")
        self.analytics.connect()
    
    def load_data(self, sales_csv, customers_csv):
        """Load sales and customer data"""
        self.analytics.ingest_csv(sales_csv, "sales")
        self.analytics.ingest_csv(customers_csv, "customers")
    
    def get_daily_summary(self):
        """Get daily sales summary"""
        return self.analytics.fetch_data("""
            SELECT 
                DATE_TRUNC('day', sale_date) as day,
                COUNT(*) as num_transactions,
                SUM(amount) as total_revenue,
                AVG(amount) as avg_transaction
            FROM sales
            GROUP BY day
            ORDER BY day DESC
            LIMIT 30
        """)
    
    def get_top_customers(self, limit=10):
        """Get top customers by revenue"""
        return self.analytics.fetch_data(f"""
            SELECT 
                c.name,
                c.city,
                COUNT(s.transaction_id) as num_purchases,
                SUM(s.amount) as total_spent
            FROM sales s
            JOIN customers c ON s.customer_id = c.customer_id
            GROUP BY c.name, c.city
            ORDER BY total_spent DESC
            LIMIT {limit}
        """)
    
    def get_product_performance(self):
        """Get product performance metrics"""
        return self.analytics.fetch_data("""
            SELECT 
                product,
                COUNT(*) as units_sold,
                SUM(amount) as revenue,
                AVG(amount) as avg_price
            FROM sales
            GROUP BY product
            ORDER BY revenue DESC
        """)

# Usage
dashboard = SalesDashboard()
dashboard.load_data("data/examples/sample_sales.csv", 
                   "data/examples/sample_customers.json")

print("Daily Summary:")
print(dashboard.get_daily_summary())

print("\nTop Customers:")
print(dashboard.get_top_customers())

print("\nProduct Performance:")
print(dashboard.get_product_performance())
```

---

## 🔬 Data Science Notebook Integration

### Scenario
Quick data exploration and analysis in Jupyter notebooks.

### Implementation

```python
# In a Jupyter notebook
from src.duckdb_analytics import DuckDBAnalytics
import matplotlib.pyplot as plt

analytics = DuckDBAnalytics(":memory:")
analytics.connect()

# Load data
analytics.ingest_csv("large_dataset.csv", "data")

# Quick aggregation
summary = analytics.fetch_data("""
    SELECT 
        category,
        COUNT(*) as count,
        AVG(value) as avg_value,
        PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY value) as median
    FROM data
    GROUP BY category
""")

# Visualize
summary.plot(x='category', y='avg_value', kind='bar')
plt.title('Average Value by Category')
plt.show()
```

---

## 📁 ETL Pipeline for Data Warehousing

### Scenario
Extract data from multiple sources, transform it, and load into a data warehouse.

### Implementation

```python
from src.duckdb_analytics import DuckDBAnalytics
from datetime import datetime

class ETLPipeline:
    def __init__(self, warehouse_db):
        self.analytics = DuckDBAnalytics(warehouse_db)
        self.analytics.connect()
    
    def extract(self, sources):
        """Extract data from multiple sources"""
        for source_type, path, table_name in sources:
            if source_type == 'csv':
                self.analytics.ingest_csv(path, f"raw_{table_name}")
            elif source_type == 'json':
                self.analytics.ingest_json(path, f"raw_{table_name}")
            elif source_type == 'parquet':
                self.analytics.ingest_parquet(path, f"raw_{table_name}")
    
    def transform(self):
        """Transform raw data into clean format"""
        # Create cleaned sales table
        self.analytics.create_table_from_query("clean_sales", """
            SELECT 
                transaction_id,
                UPPER(product) as product,
                CAST(amount as DECIMAL(10,2)) as amount,
                customer_id,
                CAST(sale_date as DATE) as sale_date,
                region,
                CURRENT_TIMESTAMP as processed_at
            FROM raw_sales
            WHERE amount > 0
        """)
        
        # Create customer dimension
        self.analytics.create_table_from_query("dim_customers", """
            SELECT DISTINCT
                customer_id,
                name,
                city,
                state,
                registration_date
            FROM raw_customers
        """)
        
        # Create fact table
        self.analytics.create_table_from_query("fact_sales", """
            SELECT 
                s.transaction_id,
                s.customer_id,
                s.product,
                s.amount,
                s.sale_date,
                s.region,
                c.state as customer_state
            FROM clean_sales s
            LEFT JOIN dim_customers c ON s.customer_id = c.customer_id
        """)
    
    def load_analytics(self):
        """Create analytical views"""
        self.analytics.create_view("vw_monthly_sales", """
            SELECT 
                DATE_TRUNC('month', sale_date) as month,
                region,
                customer_state,
                SUM(amount) as total_sales,
                COUNT(DISTINCT customer_id) as unique_customers
            FROM fact_sales
            GROUP BY month, region, customer_state
        """)
    
    def run(self, sources):
        """Run full ETL pipeline"""
        print("Starting ETL Pipeline...")
        self.extract(sources)
        print("Extraction complete")
        self.transform()
        print("Transformation complete")
        self.load_analytics()
        print("Loading complete")
        self.analytics.vacuum_database()
        print("ETL Pipeline finished!")

# Usage
pipeline = ETLPipeline("warehouse.duckdb")
sources = [
    ('csv', 'raw_data/sales.csv', 'sales'),
    ('json', 'raw_data/customers.json', 'customers'),
]
pipeline.run(sources)
```

---

## 📱 Embedded Mobile App Analytics

### Scenario
Local analytics for a mobile app that works offline.

### Implementation

```python
from src.duckdb_analytics import DuckDBAnalytics
import json

class MobileAppAnalytics:
    def __init__(self, app_data_dir):
        db_path = f"{app_data_dir}/analytics.duckdb"
        self.analytics = DuckDBAnalytics(db_path)
        self.analytics.connect()
        self._setup_schema()
    
    def _setup_schema(self):
        """Setup analytics schema"""
        self.analytics.execute_query("""
            CREATE TABLE IF NOT EXISTS user_events (
                event_id VARCHAR,
                user_id VARCHAR,
                event_type VARCHAR,
                event_data JSON,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def log_event(self, user_id, event_type, event_data):
        """Log a user event"""
        import uuid
        event_id = str(uuid.uuid4())
        event_json = json.dumps(event_data)
        
        self.analytics.execute_query(f"""
            INSERT INTO user_events (event_id, user_id, event_type, event_data)
            VALUES ('{event_id}', '{user_id}', '{event_type}', '{event_json}')
        """)
    
    def get_user_stats(self, user_id):
        """Get statistics for a specific user"""
        return self.analytics.fetch_data(f"""
            SELECT 
                event_type,
                COUNT(*) as event_count,
                MIN(timestamp) as first_occurrence,
                MAX(timestamp) as last_occurrence
            FROM user_events
            WHERE user_id = '{user_id}'
            GROUP BY event_type
            ORDER BY event_count DESC
        """)
    
    def get_daily_active_users(self, days=7):
        """Get daily active users"""
        return self.analytics.fetch_data(f"""
            SELECT 
                DATE_TRUNC('day', timestamp) as day,
                COUNT(DISTINCT user_id) as active_users
            FROM user_events
            WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '{days} days'
            GROUP BY day
            ORDER BY day
        """)

# Usage
analytics = MobileAppAnalytics("/app/data")
analytics.log_event("user123", "page_view", {"page": "home"})
analytics.log_event("user123", "button_click", {"button": "submit"})

print(analytics.get_user_stats("user123"))
print(analytics.get_daily_active_users())
```

---

## 🎮 Game Analytics

### Scenario
Track player behavior and game metrics.

### Implementation

```python
from src.duckdb_analytics import DuckDBAnalytics
from datetime import datetime, timedelta

class GameAnalytics:
    def __init__(self):
        self.analytics = DuckDBAnalytics("game_analytics.duckdb")
        self.analytics.connect()
        self._init_tables()
    
    def _init_tables(self):
        """Initialize game analytics tables"""
        self.analytics.execute_query("""
            CREATE TABLE IF NOT EXISTS player_sessions (
                session_id VARCHAR,
                player_id VARCHAR,
                start_time TIMESTAMP,
                end_time TIMESTAMP,
                level_reached INTEGER,
                score INTEGER
            )
        """)
    
    def track_session(self, player_id, session_data):
        """Track a game session"""
        self.analytics.execute_query(f"""
            INSERT INTO player_sessions VALUES (
                '{session_data['session_id']}',
                '{player_id}',
                '{session_data['start_time']}',
                '{session_data['end_time']}',
                {session_data['level_reached']},
                {session_data['score']}
            )
        """)
    
    def get_player_progression(self, player_id):
        """Get player progression over time"""
        return self.analytics.fetch_data(f"""
            SELECT 
                DATE_TRUNC('day', start_time) as day,
                MAX(level_reached) as max_level,
                MAX(score) as best_score,
                COUNT(*) as sessions_played
            FROM player_sessions
            WHERE player_id = '{player_id}'
            GROUP BY day
            ORDER BY day
        """)
    
    def get_retention_metrics(self):
        """Calculate player retention"""
        return self.analytics.fetch_data("""
            WITH first_session AS (
                SELECT 
                    player_id,
                    MIN(DATE_TRUNC('day', start_time)) as first_day
                FROM player_sessions
                GROUP BY player_id
            ),
            daily_sessions AS (
                SELECT 
                    player_id,
                    DATE_TRUNC('day', start_time) as session_day
                FROM player_sessions
            )
            SELECT 
                DATEDIFF('day', fs.first_day, ds.session_day) as days_since_install,
                COUNT(DISTINCT ds.player_id) as active_players
            FROM first_session fs
            JOIN daily_sessions ds ON fs.player_id = ds.player_id
            GROUP BY days_since_install
            ORDER BY days_since_install
            LIMIT 30
        """)

# Usage
game = GameAnalytics()
game.track_session("player001", {
    'session_id': 'sess123',
    'start_time': datetime.now() - timedelta(hours=1),
    'end_time': datetime.now(),
    'level_reached': 5,
    'score': 1250
})

print(game.get_player_progression("player001"))
print(game.get_retention_metrics())
```

---

## 🏭 IoT Sensor Data Analysis

### Scenario
Analyze sensor data from IoT devices locally before sending to cloud.

### Implementation

```python
from src.duckdb_analytics import DuckDBAnalytics
import pandas as pd
import numpy as np
from datetime import datetime

class IoTAnalytics:
    def __init__(self):
        self.analytics = DuckDBAnalytics(":memory:")
        self.analytics.connect()
        self._setup()
    
    def _setup(self):
        """Setup sensor data table"""
        self.analytics.execute_query("""
            CREATE TABLE sensor_readings (
                sensor_id VARCHAR,
                reading_time TIMESTAMP,
                temperature DOUBLE,
                humidity DOUBLE,
                pressure DOUBLE
            )
        """)
    
    def ingest_sensor_data(self, readings_df):
        """Ingest sensor readings from DataFrame"""
        # Convert DataFrame to DuckDB table
        self.analytics.conn.register('temp_readings', readings_df)
        self.analytics.execute_query("""
            INSERT INTO sensor_readings 
            SELECT * FROM temp_readings
        """)
        self.analytics.conn.unregister('temp_readings')
    
    def detect_anomalies(self, threshold_std=2):
        """Detect anomalous readings"""
        return self.analytics.fetch_data(f"""
            WITH stats AS (
                SELECT 
                    sensor_id,
                    AVG(temperature) as avg_temp,
                    STDDEV(temperature) as std_temp
                FROM sensor_readings
                GROUP BY sensor_id
            )
            SELECT 
                sr.sensor_id,
                sr.reading_time,
                sr.temperature,
                s.avg_temp,
                ABS(sr.temperature - s.avg_temp) / s.std_temp as z_score
            FROM sensor_readings sr
            JOIN stats s ON sr.sensor_id = s.sensor_id
            WHERE ABS(sr.temperature - s.avg_temp) / s.std_temp > {threshold_std}
            ORDER BY z_score DESC
        """)
    
    def get_hourly_averages(self):
        """Get hourly average readings"""
        return self.analytics.fetch_data("""
            SELECT 
                sensor_id,
                DATE_TRUNC('hour', reading_time) as hour,
                AVG(temperature) as avg_temperature,
                AVG(humidity) as avg_humidity,
                AVG(pressure) as avg_pressure,
                COUNT(*) as num_readings
            FROM sensor_readings
            GROUP BY sensor_id, hour
            ORDER BY sensor_id, hour
        """)

# Usage
iot = IoTAnalytics()

# Simulate sensor data
sensor_data = pd.DataFrame({
    'sensor_id': ['S001'] * 100,
    'reading_time': pd.date_range(start='2025-01-01', periods=100, freq='1min'),
    'temperature': np.random.normal(20, 2, 100),
    'humidity': np.random.normal(60, 5, 100),
    'pressure': np.random.normal(1013, 10, 100)
})

iot.ingest_sensor_data(sensor_data)
print(iot.detect_anomalies())
print(iot.get_hourly_averages())
```

---

## 💡 Key Takeaways

1. **DuckDB is perfect for embedded analytics** - No server setup required
2. **Works great with Pandas** - Easy integration with Python data science ecosystem
3. **Fast for analytical workloads** - Columnar storage and vectorized execution
4. **SQL-based** - Use familiar SQL syntax for complex queries
5. **Lightweight** - Minimal dependencies and resource usage
