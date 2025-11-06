#!/bin/bash
#
# POC-002 Test Environment Setup Script
#
# This script sets up the test environment for POC-002 testing.
# Test Owner: Julia Santos
#

set -e  # Exit on error

echo "=========================================="
echo "POC-002 Test Environment Setup"
echo "=========================================="
echo ""

# ============================================================================
# CONFIGURATION
# ============================================================================

TEST_DIR="/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test"
VENV_DIR="$TEST_DIR/venv"
MCP_SERVER_URL="${N8N_MCP_SERVER_URL:-http://192.168.10.194:3000}"
N8N_SERVER_URL="${N8N_SERVER_URL:-http://192.168.10.20:5678}"

# ============================================================================
# STEP 1: VERIFY PREREQUISITES
# ============================================================================

echo "Step 1: Verifying prerequisites..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "  ✓ Python version: $PYTHON_VERSION"

# Check network access to servers
echo "  Checking server connectivity..."

if ping -c 1 192.168.10.194 &> /dev/null; then
    echo "  ✓ hx-n8n-mcp-server (192.168.10.194) is reachable"
else
    echo "  ⚠ WARNING: hx-n8n-mcp-server (192.168.10.194) is NOT reachable"
fi

if ping -c 1 192.168.10.20 &> /dev/null; then
    echo "  ✓ hx-n8n-server (192.168.10.20) is reachable"
else
    echo "  ⚠ WARNING: hx-n8n-server (192.168.10.20) is NOT reachable (Phase 2 tests will fail)"
fi

echo ""

# ============================================================================
# STEP 2: CREATE VIRTUAL ENVIRONMENT
# ============================================================================

echo "Step 2: Creating Python virtual environment..."

if [ -d "$VENV_DIR" ]; then
    echo "  Virtual environment already exists at $VENV_DIR"
    echo "  Remove it to recreate: rm -rf $VENV_DIR"
else
    python3 -m venv "$VENV_DIR"
    echo "  ✓ Virtual environment created at $VENV_DIR"
fi

echo ""

# ============================================================================
# STEP 3: ACTIVATE VIRTUAL ENVIRONMENT
# ============================================================================

echo "Step 3: Activating virtual environment..."
source "$VENV_DIR/bin/activate"
echo "  ✓ Virtual environment activated"
echo ""

# ============================================================================
# STEP 4: UPGRADE PIP
# ============================================================================

echo "Step 4: Upgrading pip..."
pip install --upgrade pip --quiet
echo "  ✓ pip upgraded to $(pip --version | cut -d' ' -f2)"
echo ""

# ============================================================================
# STEP 5: INSTALL DEPENDENCIES
# ============================================================================

echo "Step 5: Installing test dependencies..."

# Core testing dependencies
pip install pytest==8.0.0 --quiet
pip install pytest-asyncio==0.23.0 --quiet
pip install pytest-cov==4.1.0 --quiet

# HTTP client
pip install httpx==0.24.1 --quiet

# Data validation
pip install pydantic==2.0.3 --quiet

echo "  ✓ Dependencies installed:"
echo "    - pytest $(pytest --version | cut -d' ' -f2)"
echo "    - pytest-asyncio"
echo "    - pytest-cov"
echo "    - httpx"
echo "    - pydantic"
echo ""

# ============================================================================
# STEP 6: CREATE TEST DATA DIRECTORIES
# ============================================================================

echo "Step 6: Creating test data directories..."

mkdir -p "$TEST_DIR/test-data/fixtures"
mkdir -p "$TEST_DIR/test-data/mocks"
mkdir -p "$TEST_DIR/test-data/datasets"
mkdir -p "$TEST_DIR/test-reports/coverage"
mkdir -p "$TEST_DIR/test-reports/results"
mkdir -p "$TEST_DIR/test-reports/metrics"

echo "  ✓ Test data directories created"
echo ""

# ============================================================================
# STEP 7: CREATE PYTEST CONFIGURATION
# ============================================================================

echo "Step 7: Creating pytest configuration..."

cat > "$TEST_DIR/pytest.ini" << 'EOF'
[pytest]
testpaths = test-scripts
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    phase1: Phase 1 tests (MCP server only, no N8N integration)
    phase2: Phase 2 tests (with N8N integration)
    critical: Critical priority tests
    high: High priority tests
    medium: Medium priority tests
    low: Low priority tests
    smoke: Smoke test suite (quick validation)
    integration: Integration tests
    performance: Performance tests
    reliability: Reliability tests

asyncio_mode = auto

# Coverage settings
addopts =
    -v
    --strict-markers
    --tb=short
    --disable-warnings
EOF

echo "  ✓ pytest.ini created"
echo ""

# ============================================================================
# STEP 8: SET ENVIRONMENT VARIABLES
# ============================================================================

echo "Step 8: Setting environment variables..."

export N8N_MCP_SERVER_URL="$MCP_SERVER_URL"
export N8N_SERVER_URL="$N8N_SERVER_URL"
export PYTEST_CURRENT_TEST=1

echo "  ✓ Environment variables set:"
echo "    N8N_MCP_SERVER_URL=$N8N_MCP_SERVER_URL"
echo "    N8N_SERVER_URL=$N8N_SERVER_URL"
echo ""

# ============================================================================
# STEP 9: VERIFY CONNECTIVITY
# ============================================================================

echo "Step 9: Verifying server connectivity..."

# Check MCP server health endpoint
if curl -s -f "$MCP_SERVER_URL/health" &> /dev/null; then
    echo "  ✓ MCP server health check passed"
elif curl -s -f "$MCP_SERVER_URL/" &> /dev/null; then
    echo "  ✓ MCP server is responding (no /health endpoint)"
else
    echo "  ⚠ WARNING: MCP server is NOT responding at $MCP_SERVER_URL"
    echo "    Tests will fail. Verify server is running:"
    echo "    ssh admin@192.168.10.194"
    echo "    systemctl status n8n-mcp-server"
fi

echo ""

# ============================================================================
# STEP 10: VERIFY TEST DISCOVERY
# ============================================================================

echo "Step 10: Verifying test discovery..."

cd "$TEST_DIR/test-scripts"

if pytest --collect-only -q &> /dev/null; then
    TEST_COUNT=$(pytest --collect-only -q | tail -n 1 | cut -d' ' -f1)
    echo "  ✓ Test discovery successful"
    echo "    Discovered tests: $TEST_COUNT"
else
    echo "  ⚠ WARNING: Test discovery failed"
    echo "    Run manually: cd $TEST_DIR/test-scripts && pytest --collect-only"
fi

echo ""

# ============================================================================
# SETUP COMPLETE
# ============================================================================

echo "=========================================="
echo "✓ Test Environment Setup Complete"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Activate virtual environment:"
echo "   source $VENV_DIR/bin/activate"
echo ""
echo "2. Navigate to test directory:"
echo "   cd $TEST_DIR/test-scripts"
echo ""
echo "3. Run smoke tests (quick validation):"
echo "   pytest -m smoke -v"
echo ""
echo "4. Run Phase 1 tests (MCP server only):"
echo "   pytest -m phase1 -v"
echo ""
echo "5. Run all tests:"
echo "   pytest -v"
echo ""
echo "6. Run with coverage:"
echo "   pytest --cov=n8n_mcp --cov-report=html -v"
echo ""
echo "For more information, see:"
echo "  - QUICK-START.md"
echo "  - MASTER-TEST-PLAN.md"
echo "  - TEST-EXECUTION-CHECKLIST.md"
echo ""
