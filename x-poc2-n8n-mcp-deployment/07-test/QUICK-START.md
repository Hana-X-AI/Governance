# POC-002 Testing Quick Start Guide

## 5-Minute Setup

### 1. Prerequisites Check

```bash
# Verify Python version (3.11+ required)
python3 --version

# Verify server accessibility
ping -c 1 192.168.10.194  # hx-n8n-mcp-server
ping -c 1 192.168.10.20   # hx-n8n-server

# Check MCP server health
curl http://192.168.10.194:3000/health
```

### 2. Environment Setup

```bash
# Navigate to test directory
cd /srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pytest pytest-asyncio pytest-cov httpx pydantic

# Run setup script
cd test-scripts
./setup_test_environment.sh
```

### 3. Run Tests

```bash
# Quick smoke test (2-3 minutes)
pytest -m "smoke" -v

# Run Phase 1 tests (MCP server only, 15-20 minutes)
pytest -m "phase1" -v

# Run all tests (30-40 minutes)
pytest -v

# Run with coverage
pytest --cov=n8n_mcp --cov-report=html -v
```

### 4. View Results

```bash
# View coverage report
open ../test-reports/coverage/index.html

# View test results
cat ../test-reports/results/report.html
```

---

## Test Suite Quick Reference

| Command | Purpose | Duration |
|---------|---------|----------|
| `pytest -m "smoke" -v` | Quick validation | 2-3 min |
| `pytest test_mcp_protocol.py -v` | MCP protocol tests | 5 min |
| `pytest test_documentation_tools.py -v` | Documentation tools | 5 min |
| `pytest test_management_tools.py -v` | Management tools | 5 min |
| `pytest test_integration.py -v` | Integration tests | 8 min |
| `pytest test_performance.py -v` | Performance tests | 5 min |
| `pytest test_data_integrity.py -v` | Data integrity tests | 4 min |
| `pytest test_reliability.py -v` | Reliability tests | 6 min |
| `pytest -v` | All tests | 30-40 min |

---

## Common Tasks

### Run Specific Test Case

```bash
# Run single test function
pytest test_mcp_protocol.py::test_protocol_initialization -v

# Run test class
pytest test_documentation_tools.py::TestListWorkflows -v
```

### Run Tests by Priority

```bash
# Critical tests only
pytest -m "critical" -v

# High priority tests
pytest -m "high" -v

# Exclude low priority
pytest -m "not low" -v
```

### Run Tests by Phase

```bash
# Phase 1 only (no N8N integration)
pytest -m "phase1" -v

# Phase 2 only (with N8N integration)
pytest -m "phase2" -v
```

### Generate Reports

```bash
# HTML coverage report
pytest --cov=n8n_mcp --cov-report=html

# Terminal coverage report
pytest --cov=n8n_mcp --cov-report=term

# JUnit XML (for CI/CD)
pytest --junitxml=../test-reports/results/junit.xml

# Combined
pytest --cov=n8n_mcp --cov-report=html --junitxml=../test-reports/results/junit.xml -v
```

---

## Troubleshooting

### Connection Refused

```bash
# Problem: Cannot connect to MCP server
# Solution: Verify server is running
curl http://192.168.10.194:3000/health

# Check server status (on hx-n8n-mcp-server)
ssh admin@192.168.10.194
systemctl status n8n-mcp-server
```

### Authentication Errors

```bash
# Problem: Authentication failed
# Solution: Verify credentials in environment
echo $N8N_MCP_SERVER_URL
echo $N8N_SERVER_URL

# Re-export credentials
export N8N_MCP_SERVER_URL="http://192.168.10.194:3000"
export N8N_SERVER_URL="http://192.168.10.20:5678"
```

### Import Errors

```bash
# Problem: Module not found
# Solution: Reinstall dependencies
pip install -r requirements.txt

# Or install individually
pip install pytest pytest-asyncio pytest-cov httpx pydantic
```

### Test Failures

```bash
# Run with verbose output
pytest -vv --tb=long

# Run with debugging
pytest --pdb  # Drops into debugger on failure

# Run single failing test
pytest test_file.py::test_function -vv
```

---

## Environment Variables

```bash
# Required
export N8N_MCP_SERVER_URL="http://192.168.10.194:3000"

# Optional (Phase 2)
export N8N_SERVER_URL="http://192.168.10.20:5678"

# Test configuration
export PYTEST_CURRENT_TEST=1
export LOG_LEVEL="INFO"
```

---

## Directory Structure Quick View

```
07-test/
├── README.md                    # Overview
├── MASTER-TEST-PLAN.md          # Detailed plan
├── TEST-EXECUTION-CHECKLIST.md  # Checklist
├── QUICK-START.md               # This guide
├── DEFECT-LOG-TEMPLATE.md       # Issue tracking
├── test-cases/                  # Test case docs
├── test-scripts/                # Pytest scripts
│   ├── conftest.py              # Fixtures
│   ├── test_*.py                # Test suites
│   └── setup_test_environment.sh
├── test-data/                   # Test data
└── test-reports/                # Results
```

---

## Next Steps

1. **Review Documentation**:
   - `README.md` - Full overview
   - `MASTER-TEST-PLAN.md` - Complete test strategy

2. **Review Test Cases**:
   - Browse `test-cases/` directory
   - Understand test coverage

3. **Execute Tests**:
   - Start with smoke tests
   - Run Phase 1 tests
   - Progress to Phase 2

4. **Report Issues**:
   - Log defects in `DEFECT-LOG-TEMPLATE.md`
   - Escalate to Olivia Thompson (N8N MCP Agent)

---

## Support

**Test Owner**: Julia Santos (Test & QA Specialist)
**POC Owner**: Olivia Thompson (N8N MCP Agent)
**CI/CD Integration**: Isaac Morgan (CI/CD Agent)

**Documentation**:
- Full Test Plan: `MASTER-TEST-PLAN.md`
- Execution Checklist: `TEST-EXECUTION-CHECKLIST.md`
- POC Specification: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/01-spec/POC-002-SPEC.md`

---

**Document Type**: Quick Start Guide
**Version**: 1.0
**Created**: 2025-11-06
**Location**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test/QUICK-START.md`
