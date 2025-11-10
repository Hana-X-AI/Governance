"""
Shared Pytest Fixtures for CodeRabbit Parser Test Suite

This module provides reusable fixtures for testing the CodeRabbit parser
and wrapper script. Fixtures follow pytest best practices with clear scopes
and dependency injection.

Author: Julia Santos - Testing & QA Specialist
Date: 2025-11-10
Version: 1.0
"""

import pytest
from pathlib import Path


# ==============================================================================
# FIXTURE: Test Data Directory
# ==============================================================================

@pytest.fixture(scope="session")
def fixtures_dir() -> Path:
    """
    Provides path to fixtures directory containing test data files.

    Scope: session (shared across all tests, created once)

    Returns:
        Path: Absolute path to fixtures/ directory
    """
    return Path(__file__).parent / "fixtures"


# ==============================================================================
# FIXTURE: Sample CodeRabbit Output
# ==============================================================================

@pytest.fixture
def sample_coderabbit_output(fixtures_dir: Path) -> str:
    """
    Loads realistic sample CodeRabbit output for testing.

    Contains multiple issue types (security, SOLID, quality) with
    various priorities (P0, P1, P2, P3).

    Args:
        fixtures_dir: Path to fixtures directory

    Returns:
        str: Sample CodeRabbit plain text output
    """
    output_file = fixtures_dir / "sample_coderabbit_output.txt"
    return output_file.read_text()


@pytest.fixture
def empty_coderabbit_output(fixtures_dir: Path) -> str:
    """
    Loads empty CodeRabbit output (no issues found).

    Args:
        fixtures_dir: Path to fixtures directory

    Returns:
        str: Empty CodeRabbit output
    """
    output_file = fixtures_dir / "empty_output.txt"
    return output_file.read_text()


@pytest.fixture
def malformed_coderabbit_output(fixtures_dir: Path) -> str:
    """
    Loads malformed CodeRabbit output for error testing.

    Args:
        fixtures_dir: Path to fixtures directory

    Returns:
        str: Invalid CodeRabbit output
    """
    output_file = fixtures_dir / "malformed_output.txt"
    return output_file.read_text()


# ==============================================================================
# FIXTURE: Sample Code Files
# ==============================================================================

@pytest.fixture
def sample_code_with_issues(fixtures_dir: Path) -> str:
    """
    Loads Python code with known issues for testing.

    Contains:
    - Hardcoded secrets (security)
    - SOLID violations
    - Missing type hints
    - Missing docstrings

    Args:
        fixtures_dir: Path to fixtures directory

    Returns:
        str: Python code with issues
    """
    code_file = fixtures_dir / "sample_code_with_issues.py"
    return code_file.read_text()


@pytest.fixture
def sample_code_clean(fixtures_dir: Path) -> str:
    """
    Loads clean Python code with no issues.

    Follows all Hana-X standards:
    - No security issues
    - SOLID compliant
    - Type hints present
    - Docstrings present

    Args:
        fixtures_dir: Path to fixtures directory

    Returns:
        str: Clean Python code
    """
    code_file = fixtures_dir / "sample_code_clean.py"
    return code_file.read_text()


# ==============================================================================
# FIXTURE: Expected JSON Structures
# ==============================================================================

@pytest.fixture
def expected_json_schema() -> dict:
    """
    Provides expected JSON schema for parser output.

    Used for validating JSON structure compliance (TC-007).

    Returns:
        dict: JSON schema definition
    """
    return {
        "type": "object",
        "required": [
            "status",
            "total_issues",
            "critical_issues",
            "high_issues",
            "medium_issues",
            "low_issues",
            "issues",
            "summary"
        ],
        "properties": {
            "status": {"type": "string", "enum": ["completed", "error"]},
            "total_issues": {"type": "integer", "minimum": 0},
            "critical_issues": {"type": "integer", "minimum": 0},
            "high_issues": {"type": "integer", "minimum": 0},
            "medium_issues": {"type": "integer", "minimum": 0},
            "low_issues": {"type": "integer", "minimum": 0},
            "issues": {"type": "array"},
            "summary": {"type": "string"}
        }
    }


@pytest.fixture
def expected_issue_schema() -> dict:
    """
    Provides expected JSON schema for individual issue objects.

    Returns:
        dict: Issue object schema definition
    """
    return {
        "type": "object",
        "required": [
            "id",
            "priority",
            "type",
            "file",
            "line",
            "message",
            "description"
        ],
        "properties": {
            "id": {"type": "string", "pattern": "^DEF-\\d{3}$"},
            "priority": {"type": "string", "enum": ["P0", "P1", "P2", "P3"]},
            "type": {
                "type": "string",
                "enum": [
                    "security",
                    "solid_violation",
                    "code_quality",
                    "performance",
                    "documentation",
                    "testing",
                    "style",
                    "bug",
                    "other"
                ]
            },
            "file": {"type": "string"},
            "line": {"type": ["integer", "null"]},
            "message": {"type": "string"},
            "description": {"type": "string"},
            "suggested_fix": {"type": ["string", "null"]},
            "reference": {"type": ["string", "null"]}
        }
    }


# ==============================================================================
# FIXTURE: Issue Type Test Data
# ==============================================================================

@pytest.fixture
def security_patterns() -> dict:
    """
    Provides test patterns for security issue detection (TC-001).

    Returns:
        dict: Security patterns with expected detection results
    """
    return {
        "hardcoded_secret": {
            "pattern": "API_KEY = 'sk-1234567890abcdef'",
            "should_detect": True,
            "expected_type": "security",
            "expected_priority": "P0"
        },
        "sql_injection": {
            "pattern": "cursor.execute('SELECT * FROM users WHERE id = ' + user_id)",
            "should_detect": True,
            "expected_type": "security",
            "expected_priority": "P0"
        },
        "xss_vulnerability": {
            "pattern": "return f'<div>{user_input}</div>'",
            "should_detect": True,
            "expected_type": "security",
            "expected_priority": "P0"
        },
        "safe_code": {
            "pattern": "api_key = os.getenv('API_KEY')",
            "should_detect": False,
            "expected_type": None,
            "expected_priority": None
        }
    }


@pytest.fixture
def solid_patterns() -> dict:
    """
    Provides test patterns for SOLID principle detection (TC-002).

    Returns:
        dict: SOLID violation patterns with expected detection results
    """
    return {
        "srp_violation": {
            "pattern": "class UserManager handles database, email, and validation",
            "should_detect": True,
            "expected_type": "solid_violation",
            "principle": "SRP"
        },
        "ocp_violation": {
            "pattern": "if isinstance(shape, Circle): calculate_circle_area()",
            "should_detect": True,
            "expected_type": "solid_violation",
            "principle": "OCP"
        },
        "lsp_violation": {
            "pattern": "Subclass changes contract by raising exception",
            "should_detect": True,
            "expected_type": "solid_violation",
            "principle": "LSP"
        },
        "isp_violation": {
            "pattern": "Interface has 20 methods, only 3 used",
            "should_detect": True,
            "expected_type": "solid_violation",
            "principle": "ISP"
        },
        "dip_violation": {
            "pattern": "High-level module directly instantiates concrete class",
            "should_detect": True,
            "expected_type": "solid_violation",
            "principle": "DIP"
        }
    }


@pytest.fixture
def quality_patterns() -> dict:
    """
    Provides test patterns for code quality detection (TC-003).

    Returns:
        dict: Quality issue patterns with expected detection results
    """
    return {
        "missing_type_hints": {
            "pattern": "def process_data(input, config):",
            "should_detect": True,
            "expected_type": "code_quality",
            "issue": "type_hints"
        },
        "missing_docstring": {
            "pattern": "def complex_function(): pass",
            "should_detect": True,
            "expected_type": "documentation",
            "issue": "docstring"
        },
        "high_complexity": {
            "pattern": "Function has cyclomatic complexity of 15",
            "should_detect": True,
            "expected_type": "performance",
            "issue": "complexity"
        },
        "clean_code": {
            "pattern": 'def add(a: int, b: int) -> int:\n    """Add two numbers."""\n    return a + b',
            "should_detect": False,
            "expected_type": None,
            "issue": None
        }
    }


# ==============================================================================
# FIXTURE: Exit Code Test Data
# ==============================================================================

@pytest.fixture
def exit_code_scenarios() -> dict:
    """
    Provides test scenarios for exit code validation (TC-004 to TC-006).

    Returns:
        dict: Exit code test scenarios
    """
    return {
        "no_issues": {
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 0,
            "low_count": 0,
            "expected_exit_code": 0
        },
        "only_low_issues": {
            "critical_count": 0,
            "high_count": 0,
            "medium_count": 2,
            "low_count": 3,
            "expected_exit_code": 0
        },
        "critical_issues": {
            "critical_count": 1,
            "high_count": 2,
            "medium_count": 3,
            "low_count": 0,
            "expected_exit_code": 1
        },
        "parser_error": {
            "error": "Parser failed to parse output",
            "expected_exit_code": 1
        }
    }


# ==============================================================================
# FIXTURE: Temporary Working Directory
# ==============================================================================

@pytest.fixture
def temp_work_dir(tmp_path: Path) -> Path:
    """
    Provides temporary working directory for file operations.

    Uses pytest's builtin tmp_path fixture (function-scoped).
    Automatically cleaned up after test completion.

    Args:
        tmp_path: Pytest's temporary path fixture

    Returns:
        Path: Temporary directory path
    """
    work_dir = tmp_path / "work"
    work_dir.mkdir()
    return work_dir


# ==============================================================================
# FIXTURE: Mock Parser Instance
# ==============================================================================

@pytest.fixture
def mock_parser_class():
    """
    Provides mock parser class for dependency injection testing.

    Used for testing parser behavior without running actual parser.
    Follows DIP (Dependency Inversion Principle).

    Returns:
        class: Mock parser class
    """
    class MockCodeRabbitParser:
        def __init__(self):
            self.issue_counter = 0

        def parse(self, text: str) -> dict:
            """Mock parse method"""
            return {
                "status": "completed",
                "total_issues": 0,
                "critical_issues": 0,
                "high_issues": 0,
                "medium_issues": 0,
                "low_issues": 0,
                "issues": [],
                "summary": "Mock parse result"
            }

    return MockCodeRabbitParser


# ==============================================================================
# FIXTURE: Integration Test Environment
# ==============================================================================

@pytest.fixture
def integration_env(tmp_path: Path, monkeypatch) -> dict:
    """
    Sets up complete environment for integration testing (TC-012).

    Creates:
    - Temporary project directory
    - Mock CodeRabbit CLI
    - Environment variables

    Args:
        tmp_path: Pytest's temporary path fixture
        monkeypatch: Pytest's monkeypatch fixture

    Returns:
        dict: Environment configuration
    """
    # Create project structure
    project_dir = tmp_path / "project"
    project_dir.mkdir()

    src_dir = project_dir / "src"
    src_dir.mkdir()

    # Set environment variables
    monkeypatch.setenv("CODERABBIT_TEST_MODE", "1")

    return {
        "project_dir": project_dir,
        "src_dir": src_dir,
        "temp_path": tmp_path
    }


# ==============================================================================
# PYTEST CONFIGURATION HOOKS
# ==============================================================================

def pytest_configure(config):
    """
    Pytest configuration hook - runs once before test collection.

    Registers custom markers and configuration.
    """
    # Markers already defined in pytest.ini, this is for documentation
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests (fast, isolated)"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )


def pytest_collection_modifyitems(config, items):
    """
    Pytest hook to modify test collection.

    Automatically adds markers based on test file names.
    """
    for item in items:
        # Add unit marker to test_parser.py and test_exit_codes.py
        if "test_parser.py" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "test_exit_codes.py" in str(item.fspath):
            item.add_marker(pytest.mark.unit)

        # Add integration marker to test_integration.py
        elif "test_integration.py" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Add integration marker to test_wrapper.py
        elif "test_wrapper.py" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
