#!/usr/bin/env python3
"""
Run all tests with coverage report
"""

import subprocess
import sys

def run_tests():
    """Run pytest with coverage"""
    cmd = [
        'pytest',
        'tests/',
        '-v',
        '--cov=src',
        '--cov-report=term-missing',
        '--cov-report=html',
        '--cov-report=xml'
    ]
    
    print("Running tests with coverage...")
    print("=" * 60)
    
    result = subprocess.run(cmd)
    
    print("\n" + "=" * 60)
    if result.returncode == 0:
        print("✓ All tests passed!")
        print("\nCoverage reports generated:")
        print("  - Terminal output (above)")
        print("  - HTML: htmlcov/index.html")
        print("  - XML: coverage.xml")
    else:
        print("✗ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()
