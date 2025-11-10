#!/usr/bin/env python3
"""
Basic tests for test_sample.py

This only tests a few functions, leaving some untested for coverage checks
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from test_sample import missing_types, divide, complex_function


def test_missing_types():
    """Test missing_types function"""
    assert missing_types(1, 2) == 3
    assert missing_types("a", "b") == "ab"


def test_divide():
    """Test divide function"""
    assert divide(10, 2) == 5
    assert divide(20, 4) == 5


def test_complex_function():
    """Test complex_function (partial coverage)"""
    result = complex_function(1, 2, 3, 4, 5, 6, 7)
    assert result == 20  # d * 5 branch


# Note: untested_function() and another_untested_function() are NOT tested
# This will trigger pytest coverage warnings
