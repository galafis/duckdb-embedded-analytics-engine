# Contributing to DuckDB Embedded Analytics Engine

First off, thank you for considering contributing to this project! 🎉

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include Python version and OS details**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear and descriptive title**
- **Provide a detailed description of the proposed functionality**
- **Explain why this enhancement would be useful**
- **List any similar features in other projects**

### Contributing Code

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/ -v`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 🔧 Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/galafis/duckdb-embedded-analytics-engine.git
   cd duckdb-embedded-analytics-engine
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run setup script:**
   ```bash
   python scripts/setup.py
   ```

5. **Run tests to verify setup:**
   ```bash
   pytest tests/ -v
   ```

## 📝 Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Write docstrings for all public methods and classes
- Keep functions focused and small

### Example:

```python
def calculate_total_sales(sales_data: pd.DataFrame) -> float:
    """
    Calculate the total sales amount from a DataFrame.
    
    Args:
        sales_data (pd.DataFrame): DataFrame containing sales data with 'amount' column
        
    Returns:
        float: Total sales amount
        
    Raises:
        KeyError: If 'amount' column is not found in DataFrame
    """
    if 'amount' not in sales_data.columns:
        raise KeyError("'amount' column not found in sales data")
    
    return sales_data['amount'].sum()
```

### Code Organization

- Keep related functionality together
- Separate concerns into different modules
- Use meaningful file and directory names
- Avoid circular imports

## 🧪 Testing

### Writing Tests

- Write tests for all new features
- Ensure tests are independent and can run in any order
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

### Example Test:

```python
def test_ingest_csv_creates_table(self):
    """Test that ingesting CSV creates a new table"""
    # Arrange
    csv_path = "test_data/sample.csv"
    table_name = "test_table"
    
    # Act
    result = self.analytics.ingest_csv(csv_path, table_name)
    
    # Assert
    self.assertTrue(result)
    self.assertIn(table_name, self.analytics.list_metadata())
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_duckdb_analytics.py -v

# Run with coverage
pytest tests/ -v --cov=src --cov-report=term-missing

# Run specific test
pytest tests/test_duckdb_analytics.py::TestDuckDBAnalytics::test_connect -v
```

## 🔀 Pull Request Process

1. **Update documentation** - If you're adding new features, update the relevant documentation
2. **Add tests** - Ensure your changes are covered by tests
3. **Update README** - If necessary, update the README.md
4. **Run all tests** - Make sure all tests pass
5. **Update CHANGELOG** - Add a note about your changes (if applicable)
6. **Request review** - Request review from maintainers

### PR Title Format

Use conventional commits format:
- `feat: Add new feature`
- `fix: Fix bug in export function`
- `docs: Update API documentation`
- `test: Add tests for ingestion methods`
- `refactor: Improve query performance`
- `chore: Update dependencies`

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
- [ ] All tests pass
- [ ] Added new tests for new features
- [ ] Manual testing completed

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
```

## 📚 Additional Resources

- [DuckDB Documentation](https://duckdb.org/docs/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Python Testing with pytest](https://docs.pytest.org/)

## ❓ Questions?

Feel free to open an issue with your question, or reach out to the maintainers directly.

---

Thank you for contributing! 🙏
