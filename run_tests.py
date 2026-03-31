"""
Test runner for the congressional-record package.

This script discovers and runs all unit tests in the tests/ directory.
Individual test files should be named test_*.py and contain unittest.TestCase classes.
"""

import sys
import unittest

if __name__ == "__main__":
    # Discover all tests in tests/ directory
    loader = unittest.TestLoader()
    suite = loader.discover("tests")

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
