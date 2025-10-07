"""
DuckDB Embedded Analytics Engine
Author: Gabriel Demetrios Lafis
Year: 2025
"""

import duckdb

def create_analytics_engine():
    """Cria engine de analytics com DuckDB"""
    conn = duckdb.connect(':memory:')
    
    # Criar tabela de exemplo
    conn.execute("""
        CREATE TABLE sales AS
        SELECT 
            'PROD' || (i % 10)::VARCHAR AS product_id,
            100 + (random() * 900)::INTEGER AS amount,
            DATE '2025-01-01' + (i % 365)::INTEGER AS sale_date
        FROM range(1000) t(i)
    """)
    
    # Analytics query
    result = conn.execute("""
        SELECT 
            product_id,
            COUNT(*) as total_sales,
            SUM(amount) as revenue,
            AVG(amount) as avg_sale
        FROM sales
        GROUP BY product_id
        ORDER BY revenue DESC
        LIMIT 5
    """).fetchall()
    
    print("Top 5 Products by Revenue:")
    for row in result:
        print(f"  {row[0]}: ${row[2]:,.2f} ({row[1]} sales)")
    
    conn.close()

if __name__ == "__main__":
    print("=" * 60)
    print("DuckDB Embedded Analytics Engine")
    print("=" * 60)
    create_analytics_engine()
