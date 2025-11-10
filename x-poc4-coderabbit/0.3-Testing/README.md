# CodeRabbit Parser Test Suite

**Test & QA Specialist**: Julia Santos
**Version**: 1.0
**Created**: 2025-11-10
**Target Coverage**: 85%+

---

## Overview

Comprehensive test suite for the CodeRabbit output parser and wrapper script. This suite validates parser accuracy, exit code behavior, JSON output structure, security pattern detection, SOLID principle detection, and integration with CI/CD workflows.

**Components Under Test**:
1. **Parser** (`parse-coderabbit.py`) - Converts CodeRabbit plain text to structured JSON
2. **Wrapper** (`coderabbit-json`) - CLI wrapper with quality gates
3. **Integration** - End-to-end workflow validation

---

## Quick Start

### Install Dependencies

```bash
cd /srv/cc/Governance/x-poc4-coderabbit/0.3-Testing
pip install -r requirements-test.txt
```

### Run All Tests

```bash
# Full test suite with coverage
pytest --cov=. --cov-report=html --cov-report=term

# Quick run (no coverage)
pytest

# Verbose output
pytest -v

# Run specific test file
pytest test_parser.py
```

### Run Specific Test Categories

```bash
# Security tests only
pytest -k "security"

# SOLID principle tests only
pytest -k "solid"

# Exit code tests only
pytest test_exit_codes.py

# Integration tests only
pytest test_integration.py
```

---

## Test Structure

```
0.3-Testing/
├── README.md                          # This file
├── pytest.ini                         # Pytest configuration
├── conftest.py                        # Shared fixtures
├── requirements-test.txt              # Test dependencies
├── test_parser.py                     # Parser unit tests (TC-001 to TC-003)
├── test_exit_codes.py                 # Exit code validation (TC-004 to TC-006)
├── test_wrapper.py                    # Wrapper integration (TC-008)
├── test_integration.py                # E2E tests (TC-007, TC-009 to TC-012)
├── fixtures/                          # Test data
│   ├── sample_coderabbit_output.txt   # Realistic CodeRabbit output
│   ├── sample_code_with_issues.py     # Code with known issues
│   ├── sample_code_clean.py           # Clean code
│   ├── empty_output.txt               # Empty CodeRabbit output
│   └── malformed_output.txt           # Invalid output for error testing
└── JULIA-TEST-SUITE-DOCUMENTATION.md  # Detailed documentation
```

---

## Test Coverage Plan

### Critical Components (95%+ target)
- Priority detection (P0/P1/P2/P3)
- Issue type classification
- Exit code logic
- Security pattern matching
- SOLID principle detection

### Important Components (85%+ target)
- File/line extraction
- JSON schema compliance
- Error handling
- Wrapper script flags

### Support Components (70%+ target)
- Suggested fix generation
- Reference linking
- Summary generation

---

## Running Tests in CI/CD

This test suite integrates with GitHub Actions and other CI/CD platforms:

```yaml
# Example GitHub Actions workflow
- name: Run CodeRabbit Parser Tests
  run: |
    cd /srv/cc/Governance/x-poc4-coderabbit/0.3-Testing
    pytest --cov=. --cov-report=xml --cov-report=term

- name: Check Coverage Threshold
  run: |
    coverage report --fail-under=85
```

---

## Test Cases Summary

### TC-001: Security Pattern Matching
Tests parser's ability to detect security vulnerabilities:
- Hardcoded secrets (API keys, passwords, tokens)
- SQL injection vulnerabilities
- XSS vulnerabilities

### TC-002: SOLID Principle Detection
Tests SOLID violation detection:
- SRP (Single Responsibility Principle)
- OCP (Open-Closed Principle)
- LSP (Liskov Substitution Principle)
- ISP (Interface Segregation Principle)
- DIP (Dependency Inversion Principle)

### TC-003: Code Quality Detection
Tests code quality issue detection:
- Missing type hints
- Missing docstrings
- High complexity
- Code duplication

### TC-004: Exit Code - No Issues
Tests exit code 0 when:
- No issues found
- Only P2/P3 (non-critical) issues

### TC-005: Exit Code - Critical Issues
Tests exit code 1 when:
- P0 (critical) issues found
- Parser error occurs

### TC-006: Exit Code - Edge Cases
Tests exit code behavior with:
- Empty input
- Malformed input
- Network errors

### TC-007: JSON Schema Compliance
Tests JSON output structure:
- Required fields present
- Field types correct
- Valid JSON format

### TC-008: Wrapper Script Integration
Tests wrapper script functionality:
- `--mode security` flag
- `--mode quality` flag
- `--save-log` flag
- `--path` flag

### TC-009: Error Handling
Tests error scenarios:
- CodeRabbit CLI not found
- Invalid input handling
- Network errors

### TC-010: Pattern Accuracy
Tests pattern matching accuracy:
- File:line extraction
- Priority assignment
- Issue type classification

### TC-011: Edge Cases
Tests boundary conditions:
- Empty CodeRabbit output
- Output with no issues
- Output with 100+ issues
- Unicode and special characters

### TC-012: CI/CD Integration
Tests GitHub Actions integration:
- Pipeline quality gates
- Exit code propagation
- Report generation

---

## Coverage Reports

### Generate Coverage Report

```bash
# HTML report (most detailed)
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# Terminal report
pytest --cov=. --cov-report=term-missing

# XML report (for CI/CD)
pytest --cov=. --cov-report=xml
```

### Coverage Thresholds

```bash
# Fail if coverage below 85%
pytest --cov=. --cov-report=term --cov-fail-under=85
```

---

## Writing New Tests

When adding new test cases, follow pytest conventions:

### Test File Naming
- Prefix with `test_` (e.g., `test_new_feature.py`)
- Place in `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/`

### Test Function Naming
- Prefix with `test_` (e.g., `def test_new_behavior():`)
- Use descriptive names: `test_parser_detects_hardcoded_secrets()`

### Test Structure (AAA Pattern)
```python
def test_example(fixture_name):
    # Arrange - Set up test data
    input_data = "test input"

    # Act - Execute the code under test
    result = function_to_test(input_data)

    # Assert - Verify expected behavior
    assert result == expected_output
```

### Use Fixtures
```python
@pytest.fixture
def sample_data():
    return {"key": "value"}

def test_with_fixture(sample_data):
    assert sample_data["key"] == "value"
```

---

## Troubleshooting

### Tests Not Discovered

**Issue**: `pytest` doesn't find tests

**Solution**:
- Ensure test files start with `test_`
- Ensure test functions start with `test_`
- Check you're in the correct directory

### Import Errors

**Issue**: `ModuleNotFoundError`

**Solution**:
```bash
# Install dependencies
pip install -r requirements-test.txt

# Verify pytest installed
pytest --version
```

### Fixtures Not Found

**Issue**: `fixture 'xyz' not found`

**Solution**:
- Check `conftest.py` contains the fixture
- Verify fixture name matches exactly
- Ensure `conftest.py` is in the same directory or parent

### Coverage Too Low

**Issue**: Coverage below 85%

**Solution**:
- Review coverage report: `pytest --cov=. --cov-report=term-missing`
- Add tests for uncovered lines
- Check if untested code is actually needed

---

## Best Practices

1. **Test Independence**: Each test should run independently
2. **Use Fixtures**: Share setup/teardown code via fixtures
3. **Descriptive Names**: Test names should describe what they test
4. **AAA Pattern**: Arrange, Act, Assert structure
5. **One Assertion Focus**: Each test should focus on one behavior
6. **Fast Tests**: Keep unit tests fast (< 1 second each)
7. **Use Markers**: Tag tests with `@pytest.mark.slow` for slow tests

---

## Integration with Development Workflow

### Pre-Commit Testing
```bash
# Run tests before committing
pytest --cov=. --cov-report=term --cov-fail-under=85
```

### Continuous Integration
```bash
# Full test suite with coverage
pytest --cov=. --cov-report=xml --cov-report=term
```

### Code Review
- All PRs must pass tests
- Coverage must be ≥85%
- No P0 issues from CodeRabbit

---

## Resources

- **pytest Documentation**: https://docs.pytest.org/
- **pytest Knowledge Source**: `/srv/knowledge/vault/pytest/`
- **Hana-X Development Standards**: `/srv/cc/Governance/0.0-governance/0.0.3-Development/development-and-coding-standards.md`
- **Test Plan Template**: `/srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.9-test-plan-template.md`

---

**Quality Gates**:
- All tests must pass ✅
- Coverage ≥85% ✅
- No P0 issues ✅
- Tests run in <30 seconds ✅

---

*Testing is not about finding bugs after the fact - it's about preventing bugs from being written in the first place.*
