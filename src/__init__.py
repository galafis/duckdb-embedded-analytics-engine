"""
DuckDB Embedded Analytics Engine
Author: Gabriel Demetrios Lafis
Year: 2025

Este pacote fornece ferramentas para trabalhar com DuckDB como um motor de analytics embarcado.
"""

from .duckdb_analytics import DuckDBAnalytics
from .advanced_example import AdvancedDuckDBAnalytics

__all__ = ['DuckDBAnalytics', 'AdvancedDuckDBAnalytics']
__version__ = '1.0.0'
