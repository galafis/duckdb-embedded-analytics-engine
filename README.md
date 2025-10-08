# Embedded Analytics Engine with DuckDB

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![DuckDB](https://img.shields.io/badge/Database-DuckDB-orange?style=for-the-badge&logo=duckdb&logoColor=white)
![Pandas](https://img.shields.io/badge/DataFrames-Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Mermaid](https://img.shields.io/badge/Diagrams-Mermaid-orange?style=for-the-badge&logo=mermaid&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

---

## 🇧🇷 Motor de Analytics Embarcado com DuckDB

Este repositório explora e demonstra o uso do **DuckDB como um motor de analytics embarcado**, ideal para cenários onde a análise de dados precisa ser realizada diretamente na aplicação, sem a necessidade de um servidor de banco de dados separado. O DuckDB é um banco de dados OLAP (Online Analytical Processing) in-process, otimizado para consultas analíticas rápidas em grandes volumes de dados, tornando-o perfeito para **aplicações de desktop, notebooks Jupyter, ferramentas de BI leves e processamento de dados local**.

### 🎯 Objetivo

O principal objetivo deste projeto é **fornecer exemplos práticos, código funcional e documentação detalhada** para desenvolvedores e cientistas de dados que desejam integrar capacidades analíticas de alta performance diretamente em suas aplicações. Serão abordados desde a instalação e configuração básica até o uso avançado de SQL para análise de dados, integração com Python e otimização de performance, com foco em **ingestão de dados de múltiplas fontes, consultas complexas e gerenciamento de metadados**.

### ✨ Destaques

- **Ingestão de Dados Multifonte**: Demonstração de como ingerir dados de diversas fontes, como arquivos CSV, JSON e Parquet, diretamente no DuckDB, facilitando a consolidação e análise de dados heterogêneos.
- **Consultas Analíticas Avançadas**: Implementação de exemplos de consultas SQL complexas, incluindo agregações, joins, subconsultas e funções de janela, para extrair insights profundos dos dados.
- **Gerenciamento de Metadados e Esquemas**: Funcionalidades para inspecionar e gerenciar o esquema de tabelas, criar e manipular views, e otimizar o banco de dados, oferecendo controle granular sobre o ambiente analítico.
- **Integração com Pandas**: Exemplos de como o DuckDB se integra perfeitamente com o Pandas, permitindo a conversão eficiente de resultados de consultas para DataFrames e vice-versa, para análise e manipulação de dados em Python.
- **Performance Otimizada**: DuckDB é projetado para consultas analíticas rápidas, aproveitando ao máximo os recursos locais da máquina, ideal para processamento de dados local.
- **Fácil Integração**: Pode ser facilmente incorporado em aplicações Python, Java, C++, R, entre outras, sem dependências de servidor.
- **Código Profissional**: Exemplos de código bem estruturados, seguindo as melhores práticas da indústria, com foco em modularidade, reusabilidade e manutenibilidade.
- **Documentação Completa**: Cada exemplo é acompanhado de documentação detalhada, diagramas explicativos e casos de uso práticos para facilitar a compreensão e a aplicação.
- **Testes Incluídos**: Módulos de código validados através de testes unitários e de integração, garantindo a robustez e a confiabilidade das soluções propostas.

### 🚀 Benefícios do DuckDB em Ação

O DuckDB oferece uma série de vantagens que o tornam uma escolha excelente para analytics embarcado e processamento de dados local. Este projeto ilustra como esses benefícios são explorados:

1.  **Performance In-Process:** A arquitetura in-process do DuckDB elimina a sobrecarga de comunicação de rede, resultando em consultas analíticas extremamente rápidas, especialmente visível em operações complexas e grandes volumes de dados.

2.  **SQL Padrão e Extensível:** Suporta SQL padrão ANSI, facilitando a migração e a integração. Além disso, a capacidade de criar views e executar scripts SQL complexos demonstra sua flexibilidade para cenários analíticos avançados.

3.  **Processamento Colunar Eficiente:** Utiliza um modelo de armazenamento e processamento colunar, otimizado para cargas de trabalho analíticas, o que acelera significativamente as consultas que agregam grandes volumes de dados, como demonstrado nas funções de agregação e percentil.

4.  **Zero-Copy com Formatos de Arquivo:** A capacidade de ler diretamente de arquivos Parquet, CSV, JSON e outros formatos populares sem ingestão prévia é crucial para a eficiência, minimizando o uso de memória e o tempo de processamento, e é um destaque na função `import_from_csv`.

5.  **Leve e Sem Servidor:** Não requer configuração de servidor, tornando-o ideal para aplicações embarcadas e desenvolvimento local, como visto na inicialização simples da classe `DuckDBAnalytics`.

6.  **Integração Profunda com Python:** A API Python robusta e fácil de usar se integra perfeitamente com bibliotecas como Pandas, permitindo fluxos de trabalho de análise de dados eficientes e a manipulação de resultados como DataFrames.

---

## 🇬🇧 Embedded Analytics Engine with DuckDB

This repository explores and demonstrates the use of **DuckDB as an embedded analytics engine**, ideal for scenarios where data analysis needs to be performed directly within the application, without the need for a separate database server. DuckDB is an in-process OLAP (Online Analytical Processing) database, optimized for fast analytical queries on large volumes of data, making it perfect for **desktop applications, Jupyter notebooks, lightweight BI tools, and local data processing**.

### 🎯 Objective

The main objective of this project is to **provide practical examples, functional code, and detailed documentation** for developers and data scientists who want to integrate high-performance analytical capabilities directly into their applications. It will cover everything from basic installation and configuration to advanced SQL usage for data analysis, Python integration, and performance optimization, with a focus on **multi-source data ingestion, complex queries, and metadata management**.

### ✨ Highlights

- **Multi-Source Data Ingestion**: Demonstration of how to ingest data from various sources, such as CSV, JSON, and Parquet files, directly into DuckDB, facilitating the consolidation and analysis of heterogeneous data.
- **Advanced Analytical Queries**: Implementation of examples of complex SQL queries, including aggregations, joins, subqueries, and window functions, to extract deep insights from data.
- **Metadata and Schema Management**: Functionalities to inspect and manage table schemas, create and manipulate views, and optimize the database, offering granular control over the analytical environment.
- **Pandas Integration**: Examples of how DuckDB seamlessly integrates with Pandas, allowing efficient conversion of query results to DataFrames and vice-versa, for data analysis and manipulation in Python.
- **Optimized Performance**: DuckDB is designed for fast analytical queries, making the most of local machine resources, ideal for local data processing.
- **Easy Integration**: Can be easily embedded into Python, Java, C++, R, and other applications, without server dependencies.
- **Professional Code**: Well-structured code examples, following industry best practices, with a focus on modularity, reusability, and maintainability.
- **Complete Documentation**: Each example is accompanied by detailed documentation, explanatory diagrams, and practical use cases to facilitate understanding and application.
- **Tests Included**: Code modules validated through unit and integration tests, ensuring the robustness and reliability of the proposed solutions.

### 📊 Visualization

![DuckDB Analytics Architecture](diagrams/duckdb_analytics_architecture.png)

*Diagrama ilustrativo da arquitetura do motor de analytics embarcado DuckDB, mostrando a integração com diferentes fontes de dados e o fluxo de processamento.*


---

## 🛠️ Tecnologias Utilizadas / Technologies Used

| Categoria         | Tecnologia      | Descrição                                                                 |
| :---------------- | :-------------- | :------------------------------------------------------------------------ |
| **Linguagem**     | Python          | Linguagem principal para desenvolvimento da interface com DuckDB.         |
| **Banco de Dados**| DuckDB          | Motor de banco de dados OLAP embarcado de alta performance.               |
| **DataFrames**    | Pandas          | Biblioteca para manipulação e análise de dados em Python.                 |
| **Serialização**  | CSV, JSON, Parquet | Formatos de arquivo suportados para ingestão e exportação de dados.       |
| **Testes**        | `unittest`      | Framework de testes padrão do Python para validação de funcionalidades.   |
| **Diagramação**   | Mermaid         | Para criação de diagramas de arquitetura e fluxo de dados no README.      |

---

## 📁 Repository Structure

```
duckdb-embedded-analytics-engine/
├── src/
│   ├── __init__.py
│   └── duckdb_analytics.py      # Lógica principal para interação com DuckDB
├── data/                        # Dados de exemplo (CSV, JSON, Parquet) para análise
├── images/                      # Imagens e diagramas para o README e documentação
├── tests/                       # Testes unitários e de integração
├── docs/                        # Documentação adicional, tutoriais e guias de uso
├── scripts/                     # Scripts utilitários para automação e configuração
├── requirements.txt             # Dependências Python
└── README.md                    # Este arquivo
```

---

## 🚀 Getting Started

Para começar, clone o repositório e explore os diretórios `src/` e `docs/` para exemplos detalhados e instruções de uso. Certifique-se de ter as dependências necessárias instaladas.

### Pré-requisitos

- Python 3.9+
- `pip` (gerenciador de pacotes Python)

### Instalação

```bash
git clone https://github.com/GabrielDemetriosLafis/duckdb-embedded-analytics-engine.git
cd duckdb-embedded-analytics-engine

# Instalar dependências Python
pip install -r requirements.txt
```

### Exemplo de Uso Avançado (Python)

O exemplo abaixo demonstra a inicialização da classe `DuckDBAnalytics`, a conexão com um banco de dados DuckDB, a ingestão de dados de diferentes fontes, a execução de consultas analíticas complexas, o gerenciamento de views e a exportação de resultados. Este código ilustra a flexibilidade e o poder do DuckDB como um motor de analytics embarcado.

```python
from src.duckdb_analytics import DuckDBAnalytics
import os
import pandas as pd
import json

if __name__ == "__main__":
    print("=" * 60)
    print("DuckDB Embedded Analytics Engine - Example")
    print("=" * 60)

    db_path = "my_analytics.duckdb"
    # Limpar o banco de dados anterior se existir
    if os.path.exists(db_path):
        os.remove(db_path)

    analytics = DuckDBAnalytics(db_path)
    analytics.connect()

    # --- 1. Criar e Ingerir Dados de Exemplo ---
    print("\n--- 1. Criando e Ingerindo Dados de Exemplo ---")
    # Criar tabela de vendas diretamente
    analytics.execute_query("""
        CREATE TABLE sales (
            id INTEGER,
            product VARCHAR,
            amount DOUBLE,
            sale_date DATE,
            region VARCHAR
        )
    """)
    analytics.execute_query("""
        INSERT INTO sales VALUES 
        (1, 'Laptop', 1200.00, '2025-01-01', 'North'), 
        (2, 'Mouse', 25.00, '2025-01-02', 'South'), 
        (3, 'Keyboard', 75.00, '2025-01-03', 'East'), 
        (4, 'Laptop', 1500.00, '2025-01-04', 'North'),
        (5, 'Monitor', 300.00, '2025-01-05', 'West'),
        (6, 'Mouse', 30.00, '2025-01-05', 'North')
    """)
    print("  Tabela 'sales' criada e populada.")

    # Ingerir dados de um CSV (simulado)
    csv_data = "id,customer_name,age,city\n101,Alice,30,New York\n102,Bob,24,Los Angeles"
    with open("data/customers.csv", "w") as f:
        f.write(csv_data)
    analytics.import_from_csv("data/customers.csv", "customers_from_csv")
    print("  Dados de 'customers.csv' ingeridos na tabela 'customers_from_csv'.")

    # Ingerir dados de um JSON (simulado)
    json_data = [
        {"order_id": 1001, "customer_id": 101, "total": 150.00, "order_date": "2025-01-01"},
        {"order_id": 1002, "customer_id": 102, "total": 200.50, "order_date": "2025-01-02"}
    ]
    with open("data/orders.json", "w") as f:
        json.dump(json_data, f)
    analytics.execute_query("CREATE TABLE orders AS SELECT * FROM read_json_auto('data/orders.json');")
    print("  Dados de 'orders.json' ingeridos na tabela 'orders'.")

    # --- 2. Consultas Analíticas Avançadas ---
    print("\n--- 2. Consultas Analíticas Avançadas ---")
    print("\nTop 3 Produtos por Receita e Média de Vendas por Região:")
    result_df = analytics.fetch_data("""
        WITH ProductRevenue AS (
            SELECT 
                product,
                SUM(amount) as total_revenue
            FROM sales
            GROUP BY product
        ),
        RegionalSales AS (
            SELECT
                region,
                product,
                AVG(amount) as avg_regional_sale
            FROM sales
            GROUP BY region, product
        )
        SELECT 
            pr.product,
            pr.total_revenue,
            rs.region,
            rs.avg_regional_sale
        FROM ProductRevenue pr
        JOIN RegionalSales rs ON pr.product = rs.product
        ORDER BY pr.total_revenue DESC, rs.region
        LIMIT 5
    """)
    print(result_df)

    print("\nClientes com mais de uma compra (usando JOIN com orders):")
    customers_with_multiple_orders = analytics.fetch_data("""
        SELECT
            c.customer_name,
            COUNT(o.order_id) as total_orders
        FROM customers_from_csv c
        JOIN orders o ON c.id = o.customer_id
        GROUP BY c.customer_name
        HAVING COUNT(o.order_id) > 1
    """)
    print(customers_with_multiple_orders)

    # --- 3. Gerenciamento de Metadados e Esquemas ---
    print("\n--- 3. Gerenciamento de Metadados e Esquemas ---")
    # Criar e usar uma view
    analytics.create_view("sales_summary_view", "SELECT product, SUM(amount) as total_revenue FROM sales GROUP BY product")
    print("\nDados da View 'sales_summary_view':")
    print(analytics.fetch_data("SELECT * FROM sales_summary_view"))

    # Obter esquema da tabela
    print("\nEsquema da tabela 'sales':")
    print(analytics.get_table_schema("sales"))

    # --- 4. Exportar Dados ---
    print("\n--- 4. Exportando Dados ---")
    output_csv_path = "data/sales_output.csv"
    analytics.export_to_csv("SELECT * FROM sales WHERE region = 'North'", output_csv_path)
    if os.path.exists(output_csv_path):
        print(f"  Dados da região 'North' exportados para '{output_csv_path}'. Conteúdo:\n")
        with open(output_csv_path, "r") as f:
            print(f.read())
        os.remove(output_csv_path)

    # --- 5. Otimizar Banco de Dados ---
    print("\n--- 5. Otimizando Banco de Dados ---")
    analytics.vacuum_database()
    print("  Banco de dados otimizado (VACUUM executado).")

    analytics.disconnect()

    # Limpar arquivos gerados
    if os.path.exists(db_path):
        os.remove(db_path)
    if os.path.exists("data/customers.csv"):
        os.remove("data/customers.csv")
    if os.path.exists("data/orders.json"):
        os.remove("data/orders.json")

    print("\n==================================================")
    print("Demonstração Concluída.")
    print("==================================================")
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou sugerir melhorias. Por favor, siga as diretrizes de contribuição.

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Autor:** Gabriel Demetrios Lafis  \n**Ano:** 2025