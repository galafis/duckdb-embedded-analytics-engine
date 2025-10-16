#!/usr/bin/env python3
"""
Setup script for DuckDB Embedded Analytics Engine
Creates necessary directories and downloads sample data
"""

import os
import sys

def create_directories():
    """Create necessary project directories"""
    directories = [
        'data',
        'data/examples',
        'data/output',
        'docs',
        'scripts',
        'logs'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'duckdb',
        'pandas',
        'pyarrow',
        'pytest',
        'faker'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            missing.append(package)
            print(f"✗ {package} is NOT installed")
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("DuckDB Embedded Analytics Engine - Setup")
    print("=" * 60)
    
    print("\n1. Creating directories...")
    create_directories()
    
    print("\n2. Checking dependencies...")
    if check_dependencies():
        print("\n✓ All dependencies are installed!")
    else:
        print("\n✗ Some dependencies are missing. Please install them.")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Check out the examples in docs/getting_started.md")
    print("2. Run the basic example: python src/duckdb_analytics.py")
    print("3. Run the advanced example: python run_advanced_example.py")
    print("4. Run tests: pytest tests/ -v")

if __name__ == "__main__":
    main()
