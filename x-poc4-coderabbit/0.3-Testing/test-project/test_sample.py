#!/usr/bin/env python3
"""
Test Sample - Intentionally contains various issues for linter testing

This file tests all 6 linters:
1. Bandit - Security issues
2. Pylint - Code quality issues
3. Mypy - Type checking issues
4. Radon - Complexity issues
5. Black - Formatting issues (this file is intentionally not black-formatted)
6. Pytest - Coverage issues (some functions not tested)
"""

import os
import pickle  # Bandit B403 - pickle is potentially unsafe
import yaml  # For unsafe yaml.load() test

# Bandit B105 - Hardcoded password
PASSWORD = "hardcoded_password_123"
API_KEY = "sk-1234567890abcdef"  # Bandit B105


def insecure_function(user_input):
    """Function with security issues (Bandit)"""
    # Bandit B608 - SQL injection vulnerability
    query = f"SELECT * FROM users WHERE username = '{user_input}'"

    # Bandit B301 - Unsafe YAML loading
    config = yaml.load(open("config.yaml"), Loader=yaml.Loader)

    return query


def complex_function(a, b, c, d, e, f, g):  # Pylint: too many arguments
    """
    Highly complex function (Radon - cyclomatic complexity > 10)
    Also has formatting issues for Black
    """
    result = 0  # Black: missing spaces around =

    if a > 10:  # Black: missing spaces
        if b > 20:
            if c > 30:
                if d > 40:
                    if e > 50:
                        if f > 60:
                            if g > 70:
                                result = a + b + c + d + e + f + g
                            else:
                                result = a * b
                        else:
                            result = c * d
                    else:
                        result = e * f
                else:
                    result = g * 2
            else:
                result = f * 3
        else:
            result = e * 4
    else:
        result = d * 5

    return result


def missing_types(x, y):  # Mypy: missing type hints
    """Function missing type hints"""
    return x + y


def unused_variables():  # Pylint: unused variables
    """Function with unused variables"""
    unused_var = 42
    another_unused = "test"
    x = 10
    return x


class PoorlyNamedClass:  # Should be PascalCase (already is, but methods aren't)
    """Class with quality issues"""

    def BadMethodName(self):  # Pylint: method should be snake_case
        """Poorly named method"""
        pass

    def method_without_docstring(self):  # Pylint: missing docstring
        return 42


def divide(a, b):  # Missing error handling for division by zero
    """Division without error handling"""
    return a / b  # Pylint/Mypy: potential division by zero


# Global variable in ALL_CAPS but not actually constant
GLOBAL_VAR = []  # Pylint: constant name for non-constant


def untested_function():
    """This function has no tests - pytest coverage will flag it"""
    return "untested"


def another_untested_function(x):
    """Another function without tests"""
    return x * 2


# Missing main guard
print("This runs on import!")  # Pylint: statement in module scope
