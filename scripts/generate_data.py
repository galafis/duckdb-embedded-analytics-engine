#!/usr/bin/env python3
"""
Generate sample data for testing and examples
"""

import os
import json
import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')

def generate_customers(num_customers=100):
    """Generate sample customer data"""
    customers = []
    for i in range(num_customers):
        customers.append({
            'customer_id': f'C{i+1:04d}',
            'name': fake.name(),
            'email': fake.email(),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'registration_date': fake.date_between(start_date='-2y', end_date='today').isoformat()
        })
    return customers

def generate_products(num_products=50):
    """Generate sample product data"""
    categories = ['Eletrônicos', 'Livros', 'Roupas', 'Alimentos', 'Casa e Jardim', 'Esportes']
    products = []
    
    for i in range(num_products):
        products.append({
            'product_id': f'P{i+1:04d}',
            'product_name': f'{fake.word().capitalize()} {fake.word()}',
            'category': random.choice(categories),
            'price': round(random.uniform(10.0, 1000.0), 2),
            'stock_quantity': random.randint(0, 500)
        })
    
    return products

def generate_sales(num_sales=1000, num_customers=100, num_products=50):
    """Generate sample sales data"""
    regions = ['North', 'South', 'East', 'West', 'Central']
    sales = []
    
    start_date = datetime.now() - timedelta(days=365)
    
    for i in range(num_sales):
        sale_date = fake.date_time_between(start_date=start_date, end_date='now')
        sales.append({
            'transaction_id': i + 1,
            'customer_id': f'C{random.randint(1, num_customers):04d}',
            'product_id': f'P{random.randint(1, num_products):04d}',
            'quantity': random.randint(1, 5),
            'amount': round(random.uniform(10.0, 2000.0), 2),
            'sale_date': sale_date.date().isoformat(),
            'region': random.choice(regions)
        })
    
    return sales

def main():
    """Generate all sample data files"""
    print("Generating sample data...")
    
    # Create output directory
    output_dir = 'data/generated'
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate customers
    print("Generating customers...")
    customers = generate_customers(100)
    with open(f'{output_dir}/customers.json', 'w', encoding='utf-8') as f:
        json.dump(customers, f, indent=2, ensure_ascii=False)
    
    customers_df = pd.DataFrame(customers)
    customers_df.to_csv(f'{output_dir}/customers.csv', index=False)
    customers_df.to_parquet(f'{output_dir}/customers.parquet', index=False)
    print(f"  ✓ Generated {len(customers)} customers")
    
    # Generate products
    print("Generating products...")
    products = generate_products(50)
    products_df = pd.DataFrame(products)
    products_df.to_csv(f'{output_dir}/products.csv', index=False)
    products_df.to_parquet(f'{output_dir}/products.parquet', index=False)
    print(f"  ✓ Generated {len(products)} products")
    
    # Generate sales
    print("Generating sales...")
    sales = generate_sales(1000, 100, 50)
    sales_df = pd.DataFrame(sales)
    sales_df.to_csv(f'{output_dir}/sales.csv', index=False)
    sales_df.to_parquet(f'{output_dir}/sales.parquet', index=False)
    print(f"  ✓ Generated {len(sales)} sales transactions")
    
    print(f"\nAll data generated in '{output_dir}/' directory!")
    print("\nGenerated files:")
    print("  - customers.json, customers.csv, customers.parquet")
    print("  - products.csv, products.parquet")
    print("  - sales.csv, sales.parquet")

if __name__ == "__main__":
    main()
