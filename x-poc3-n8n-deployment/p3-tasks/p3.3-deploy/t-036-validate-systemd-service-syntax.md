# Task: Validate Systemd Service Syntax

**Task ID**: T-036
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-034, T-035 |

## Task Overview

Validate systemd service file syntax using systemd-analyze verify to catch configuration errors before attempting service start.

## Success Criteria
- [ ] systemd-analyze verify passes with no errors
- [ ] Service file loads without warnings
- [ ] All referenced files exist (EnvironmentFile, ExecStart)
- [ ] User and Group references valid

## Execution Steps

### Step 1: Verify Referenced Files Exist
```bash
echo "=== Verifying Service File References ==="

# Check environment file
test -f /opt/n8n/.env && echo "✅ Environment file exists" || echo "❌ .env missing"

# Check n8n executable
test -f /opt/n8n/app/packages/cli/bin/n8n && echo "✅ n8n executable exists" || echo "❌ Executable missing"

# Check Node.js binary (flexible - works with apt, nvm, nodenv, etc.)
if which node >/dev/null 2>&1; then
  NODE_PATH=$(which node)
  NODE_VERSION=$(node --version)
  echo "✅ Node.js in PATH: $NODE_PATH ($NODE_VERSION)"
else
  echo "❌ Node.js not found in PATH"
fi

# Verify the ExecStart command from service file will work
EXEC_START=$(grep "^ExecStart=" /etc/systemd/system/n8n.service | cut -d'=' -f2)
NODE_BIN=$(echo "$EXEC_START" | awk '{print $1}')
if [ -f "$NODE_BIN" ] || which "$(basename $NODE_BIN)" >/dev/null 2>&1; then
  echo "✅ ExecStart Node.js binary accessible: $NODE_BIN"
else
  echo "⚠️  WARNING: ExecStart references $NODE_BIN which may not exist"
  echo "   Actual Node.js location: $(which node)"
  echo "   Consider updating service file ExecStart to use: $(which node)"
fi

# Check user exists
id n8n >/dev/null 2>&1 && echo "✅ n8n user exists" || echo "❌ User missing"
```

### Step 2: Run systemd-analyze verify
```bash
echo "=== Running systemd-analyze verify ==="

sudo systemd-analyze verify /etc/systemd/system/n8n.service

if [ $? -eq 0 ]; then
  echo "✅ Service file syntax valid"
else
  echo "❌ Service file has errors"
  exit 1
fi
```

### Step 3: Check for Warnings
```bash
# Check service file for common issues
echo "=== Checking for Common Issues ==="

grep -q "^User=" /etc/systemd/system/n8n.service && echo "✅ User directive present"
grep -q "^EnvironmentFile=" /etc/systemd/system/n8n.service && echo "✅ EnvironmentFile present"
grep -q "^ExecStart=" /etc/systemd/system/n8n.service && echo "✅ ExecStart present"
```

## Validation
```bash
systemd-analyze verify /etc/systemd/system/n8n.service && \
echo "✅ Validation passed" || \
echo "❌ Validation failed"
```

## Task Metadata
```yaml
task_id: T-036
source: agent-omar-planning-analysis.md:512 (T4.5)
```
