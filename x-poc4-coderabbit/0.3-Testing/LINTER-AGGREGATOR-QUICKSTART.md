# Linter Aggregator - Quick Start Guide

**Version**: 1.0
**Date**: 2025-11-10
**For**: Developers using POC4 CodeRabbit Layer 1

---

## What is Linter Aggregator?

**Linter Aggregator** is a production-ready Python tool that runs 6 proven code quality linters in parallel, aggregates results, and provides actionable feedback.

**6 Integrated Linters**:
1. **bandit** - Security scanning (SQL injection, hardcoded passwords, etc.)
2. **pylint** - Code quality (PEP 8, unused variables, bad naming, etc.)
3. **mypy** - Type checking (missing hints, type errors)
4. **radon** - Complexity metrics (cyclomatic complexity > 10)
5. **black** - Code formatting (PEP 8 auto-formatter)
6. **pytest** - Test coverage (target: ≥80%)

**Key Features**:
- ⚡ **Parallel execution** (1.76x faster)
- 🔒 **Security hardening** (path validation)
- 🎯 **Issue deduplication** (no duplicates)
- 🚀 **Fast** (< 2 seconds for small projects)
- 📊 **JSON output** (machine-readable for Roger)

---

## Installation

Already installed on `hx-cc-server.hx.dev.local`:
- **Aggregator**: `/srv/cc/hana-x-infrastructure/.claude/agents/roger/linter_aggregator.py`
- **Wrapper**: `/srv/cc/hana-x-infrastructure/bin/lint-all`

---

## Usage

### Basic Commands

```bash
# Run in current directory
lint-all

# Analyze specific directory
lint-all --path src/backend

# Human-readable output
lint-all --format text

# Auto-fix formatting issues
lint-all --fix

# Verbose output (debugging)
lint-all --verbose
```

### Common Workflows

#### 1. Pre-Commit Check
```bash
# Before committing code
cd /your/project
lint-all --fix --format text

# If issues found, fix them
# Then commit
```

#### 2. CI/CD Integration
```bash
# In GitHub Actions / GitLab CI
lint-all --format json > lint-results.json
```

#### 3. Quick Security Scan
```bash
# Check for security issues only
lint-all --format text | grep "P0\|P1"
```

#### 4. Test Coverage Check
```bash
# See coverage gaps
lint-all --format text | grep "pytest"
```

---

## Understanding Output

### Priority Levels
- **P0 (Critical)** 🔴 - Must fix immediately (security, severe bugs)
- **P1 (High)** 🟡 - Should fix soon (type errors, unused code)
- **P2 (Medium)** 🟠 - Fix when convenient (naming, complexity)
- **P3 (Low)** ⚪ - Nice to fix (formatting)
- **P4 (Info)** ℹ️ - Informational only

### Sample Text Output
```
Found 24 issues: | 🟡 9 high (P1) | 🟠 15 medium (P2) | ⚠️  High-priority issues should be fixed soon.

P1 [bandit] src/auth.py:42
  Possible SQL injection vector through string-based query construction.
  💡 Fix: Use parameterized queries or an ORM to prevent SQL injection

P1 [pytest] Overall:?
  Test coverage is 60.0% (target: ≥80%)
  💡 Fix: Add unit tests for uncovered code

P2 [pylint] src/utils.py:15
  Unused variable 'config'
```

### Sample JSON Output
```json
{
  "status": "completed",
  "total_issues": 24,
  "critical_issues": 0,
  "high_issues": 9,
  "medium_issues": 15,
  "low_issues": 0,
  "info_issues": 0,
  "issues": [
    {
      "id": "BAN-0001",
      "priority": "P1",
      "category": "security",
      "source": "bandit",
      "file": "src/auth.py",
      "line": 42,
      "message": "Possible SQL injection vector",
      "fix": "Use parameterized queries"
    }
  ],
  "execution_time_seconds": 1.35,
  "summary": "Found 24 issues: | 🟡 9 high (P1) | 🟠 15 medium (P2)"
}
```

---

## Exit Codes

- **0** - Success (no critical/high issues)
- **1** - Issues found (critical or high priority)
- **2** - Linter execution failed

### Example
```bash
lint-all --format text
if [ $? -eq 0 ]; then
    echo "Code quality passed!"
    git commit -m "Clean code"
else
    echo "Fix issues before committing"
fi
```

---

## Common Issues & Fixes

### 1. Bandit - Hardcoded Password
**Issue**: `Possible hardcoded password: 'secret123'`
**Fix**:
```python
# Bad
PASSWORD = "secret123"

# Good
import os
PASSWORD = os.getenv("PASSWORD")
```

### 2. Pylint - Unused Import
**Issue**: `Unused import os`
**Fix**: Remove the import or use it

### 3. Mypy - Missing Type Hints
**Issue**: `Function is missing type hints`
**Fix**:
```python
# Bad
def add(a, b):
    return a + b

# Good
def add(a: int, b: int) -> int:
    return a + b
```

### 4. Radon - High Complexity
**Issue**: `Function 'process' has complexity 15 (target: <10)`
**Fix**: Extract sub-functions
```python
# Bad - one large function with complexity 15

# Good - split into smaller functions
def process(data):
    validated = validate_data(data)
    transformed = transform_data(validated)
    return store_data(transformed)
```

### 5. Pytest - Low Coverage
**Issue**: `Test coverage is 60% (target: ≥80%)`
**Fix**: Write tests for uncovered code

### 6. Black - Formatting
**Issue**: `Code formatting does not match Black style`
**Fix**: `lint-all --fix` (auto-fixes)

---

## Advanced Usage

### Programmatic Access (Python)
```python
#!/usr/bin/env python3
import subprocess
import json

def run_linter(path: str) -> dict:
    """Run linter aggregator and return results"""
    result = subprocess.run(
        ['/srv/cc/hana-x-infrastructure/.claude/agents/roger/linter_aggregator.py',
         '--path', path, '--format', 'json'],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

# Usage
results = run_linter('/srv/cc/project')
print(f"Total issues: {results['total_issues']}")
print(f"Critical: {results['critical_issues']}")

# Filter high-priority issues
high_priority = [
    i for i in results['issues']
    if i['priority'] in ['P0', 'P1']
]
```

### CI/CD Integration (GitHub Actions)
```yaml
name: Code Quality

on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install linters
        run: |
          pip install bandit pylint mypy radon black pytest pytest-cov

      - name: Run linter aggregator
        run: |
          lint-all --format json > results.json

      - name: Check for critical issues
        run: |
          if [ $(jq '.critical_issues + .high_issues' results.json) -gt 0 ]; then
            echo "Critical or high-priority issues found"
            exit 1
          fi
```

---

## Configuration

Currently no configuration file support (hardcoded thresholds).

**Default Thresholds**:
- Complexity: > 10 (Radon)
- Coverage: < 80% (Pytest)
- Security: All bandit issues reported

**Planned for Phase 2**: `.linterrc.yaml` support

---

## Troubleshooting

### "Missing linters" Error
```
❌ Error: Missing linters: bandit (/home/agent0/.local/bin/bandit)
```
**Solution**:
```bash
pip install --break-system-packages bandit pylint mypy radon black pytest pytest-cov
```

### "Path outside allowed directories" Error
```
❌ Security Error: Path outside allowed directories: /etc/passwd
```
**Solution**: Only analyze paths in:
- `/srv/cc/*`
- `/home/agent0/*`
- `/tmp/*`

### Slow Execution
**Problem**: Linting takes > 10 seconds
**Solutions**:
1. Use `--no-parallel` to debug which linter is slow
2. Check pytest test suite size (may timeout after 5 minutes)
3. Reduce project size (analyze specific directory with `--path`)

---

## Best Practices

### 1. Run Before Commit
```bash
# Add to pre-commit hook
lint-all --fix --format text
```

### 2. Focus on P0/P1
Prioritize critical and high-priority issues first.

### 3. Auto-Fix Formatting
Always use `--fix` to auto-format with black before manual fixes.

### 4. Track Progress
```bash
# Before fixes
lint-all > before.json

# After fixes
lint-all > after.json

# Compare
jq '.total_issues' before.json after.json
```

### 5. Incremental Fixes
Don't try to fix everything at once:
1. Fix P0 (Critical) issues
2. Fix P1 (High) issues
3. Fix P2 (Medium) issues over time

---

## FAQ

**Q: Can I disable specific linters?**
A: Not yet. Phase 2 will add configuration support.

**Q: Why is black a separate linter?**
A: Black is a code formatter, not a linter. It auto-fixes issues, while others detect them.

**Q: Does it support other languages?**
A: No, Python only. Each language needs its own linter suite.

**Q: Can I run on a single file?**
A: Yes: `lint-all --path myfile.py`

**Q: What if I disagree with a finding?**
A: Some linters support ignore comments:
```python
# pylint: disable=unused-variable
x = 42  # noqa: F841 (flake8 style)
```

**Q: Is it safe to run on production code?**
A: Yes, it's read-only. No code is modified unless you use `--fix`.

---

## Support & Feedback

- **Issues**: Report to Eric Johnson (Senior Developer)
- **Documentation**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/`
- **Source**: `/srv/cc/hana-x-infrastructure/.claude/agents/roger/linter_aggregator.py`

---

**Quick Links**:
- [Full Specification](/srv/cc/Governance/x-poc4-coderabbit/0.2-Delivery/linter-aggregator.md)
- [Phase 1 Completion Report](/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/PHASE-1-COMPLETION-REPORT.md)
- [Test Project](/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/)

---

**Version**: 1.0 | **Date**: 2025-11-10 | **Author**: Eric Johnson
