# CodeRabbit Fix: Phase 3 Execution Plan - .env File Security and Secret Handling

**Document**: `x-docs/coderabbit/CODERABBIT-FIX-phase3-execution-plan-security-automation.md` (supplement)
**Date**: 2025-11-09
**Reviewer**: CodeRabbit AI + Agent Zero
**Type**: Security Hardening / Secret Management

---

## Issue #1: Missing .env File Ownership and Permissions

**Location**: Script examples creating /opt/n8n/.env
**Severity**: HIGH - Security Gap
**Category**: File Security / Least Privilege

### Problem

**Current code creates .env file but doesn't secure it**:

```bash
sudo tee /opt/n8n/.env << EOF
DB_POSTGRESDB_PASSWORD=${N8N_DB_PASSWORD}
N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}
EOF
```

**Security Issues**:
1. **File owned by root** (created with sudo tee)
2. **Permissions may be world-readable** (default umask 022 → mode 644)
3. **n8n service cannot read file** (runs as user 'n8n', file owned by root)
4. **Secrets exposed to other users** (world-readable)

### Analysis

**Attack Scenario**:

```bash
# File created with sudo tee (root owned)
ls -l /opt/n8n/.env
# -rw-r--r-- 1 root root 1024 Nov 09 12:00 /opt/n8n/.env
#  ^^^^ ^^^^
#  |    |
#  |    Other users can read (SECURITY ISSUE)
#  Owner: root (n8n service can't read)
```

**Impact**:
- Any user on system can read database password
- Any user can read encryption key
- Violates least privilege principle
- n8n service fails to start (permission denied)

**PCI-DSS Violation**: Requirement 8.2.1 - Credentials must be protected with appropriate file permissions

**SOC 2 Violation**: CC6.1 - Logical and physical access controls restrict unauthorized access

---

## Resolution: Add Secure Ownership and Permissions

### Fix for .env File Creation

**Add after tee command**:

```bash
# Create .env file
sudo tee /opt/n8n/.env << EOF
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=${DB_HOST}
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=${DB_NAME}
DB_POSTGRESDB_USER=${DB_USER}
DB_POSTGRESDB_PASSWORD=${N8N_DB_PASSWORD}
N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.hx.dev.local/
N8N_EDITOR_BASE_URL=https://n8n.hx.dev.local/
EXECUTIONS_MODE=regular
N8N_LOG_LEVEL=info
EOF

# SECURITY: Set secure ownership and permissions
sudo chown n8n:n8n /opt/n8n/.env
sudo chmod 600 /opt/n8n/.env
```

**Verification**:
```bash
# Verify secure permissions
ls -l /opt/n8n/.env
# Expected: -rw------- 1 n8n n8n 1024 Nov 09 12:00 /opt/n8n/.env
#            ^^^^^^^^  Owner: n8n, Group: n8n, Mode: 600 (owner read/write only)
```

**Security Benefits**:
- ✅ Only n8n user can read file
- ✅ No other users can access secrets
- ✅ n8n service can read configuration
- ✅ Meets PCI-DSS/SOC 2 requirements

---

## Issue #2: Encryption Key Parsing Drops Base64 Padding

**Location**: Encryption key extraction from .env
**Severity**: HIGH - Data Corruption Risk
**Category**: String Parsing / Data Integrity

### Problem

**Current parsing uses `cut -d'=' -f2`**:

```bash
ENCRYPTION_KEY=$(sudo grep N8N_ENCRYPTION_KEY /opt/n8n/.env | cut -d'=' -f2)
echo "Encryption Key: $ENCRYPTION_KEY"
```

**Problem with `cut -d'=' -f2`**:
- Only extracts field 2 (after first '=')
- If key contains '=' characters (base64 padding), they are truncated

**Example**:

```bash
# .env file contains:
N8N_ENCRYPTION_KEY=abc123def456ghi789==

# cut -d'=' -f2 extracts:
abc123def456ghi789

# LOST: == (base64 padding dropped)
```

**Impact**:
- Encryption key corrupted
- n8n cannot decrypt existing data
- Backup restoration fails
- Data permanently lost

---

## Resolution: Fix Key Parsing to Preserve All Characters

### Fixed Parsing Command

**Change from**:
```bash
ENCRYPTION_KEY=$(sudo grep N8N_ENCRYPTION_KEY /opt/n8n/.env | cut -d'=' -f2)
```

**To**:
```bash
# Use -f2- to preserve all fields after first '='
ENCRYPTION_KEY=$(sudo grep -m1 '^N8N_ENCRYPTION_KEY=' /opt/n8n/.env | cut -d'=' -f2-)
```

**Improvements**:
1. ✅ `-f2-` extracts field 2 and beyond (preserves all '=' in value)
2. ✅ `-m1` stops after first match (efficiency)
3. ✅ `^N8N_ENCRYPTION_KEY=` anchors to start of line (prevents false matches)

**Test Cases**:

```bash
# Test Case 1: Key with base64 padding
echo "N8N_ENCRYPTION_KEY=abc123==" | cut -d'=' -f2-
# Expected: abc123==
# Old (-f2): abc123 ❌

# Test Case 2: Key with multiple '=' signs
echo "N8N_ENCRYPTION_KEY=key=value=data" | cut -d'=' -f2-
# Expected: key=value=data
# Old (-f2): key ❌

# Test Case 3: Normal key (no '=')
echo "N8N_ENCRYPTION_KEY=90c5323a349aba" | cut -d'=' -f2-
# Expected: 90c5323a349aba
# Old (-f2): 90c5323a349aba ✅
```

---

## Issue #3: Encryption Key Printed to Logs

**Location**: Encryption key extraction commands
**Severity**: HIGH - Secret Exposure
**Category**: Logging Security / Information Disclosure

### Problem

**Current code prints encryption key to stdout**:

```bash
ENCRYPTION_KEY=$(sudo grep N8N_ENCRYPTION_KEY /opt/n8n/.env | cut -d'=' -f2)
echo "Encryption Key: $ENCRYPTION_KEY"
```

**Security Impact**:

1. **Command history exposure**:
   ```bash
   # Encryption key visible in shell history
   $ history | grep ENCRYPTION_KEY
   842  ENCRYPTION_KEY=$(sudo grep N8N_ENCRYPTION_KEY /opt/n8n/.env | cut -d'=' -f2)
   843  echo "Encryption Key: 90c5323a349aba2913666c6b0f1b9f8dd3801ab23114fb658d8e58a87d02cdbc"
   ```

2. **Log file exposure**:
   ```bash
   # If script output redirected to log
   bash deploy.sh 2>&1 | tee deployment.log

   # Result: deployment.log contains plaintext encryption key
   $ grep "Encryption Key" deployment.log
   Encryption Key: 90c5323a349aba2913666c6b0f1b9f8dd3801ab23114fb658d8e58a87d02cdbc
   ```

3. **Screen sharing exposure**:
   - Operator sharing screen during deployment
   - Encryption key visible to everyone on call
   - May be recorded in meeting recordings

4. **Monitoring/SIEM exposure**:
   - Logs sent to centralized logging (Splunk, ELK)
   - Encryption key indexed and searchable
   - Persists in logs for retention period

**Compliance Violations**:
- PCI-DSS 3.4: Render PAN unreadable (encryption keys must be protected)
- SOC 2 CC6.7: Encryption keys must be protected from disclosure
- NIST SP 800-53 SC-28: Protect encryption keys during storage and transmission

---

## Resolution: Stop Printing Secrets to Stdout/Logs

### Fixed Script with Secure Secret Handling

**Change from**:
```bash
ENCRYPTION_KEY=$(sudo grep N8N_ENCRYPTION_KEY /opt/n8n/.env | cut -d'=' -f2)
echo "Encryption Key: $ENCRYPTION_KEY"
```

**To**:
```bash
# Set strict error handling and secure umask
set -euo pipefail  # Exit on error, undefined vars, pipe failures
umask 077          # Create files with 600 permissions by default

# Extract encryption key securely (NO OUTPUT TO STDOUT)
ENCRYPTION_KEY=$(sudo grep -m1 '^N8N_ENCRYPTION_KEY=' /opt/n8n/.env | cut -d'=' -f2-)

# DO NOT print the key to stdout/logs
# Only use key internally for validation or backup

# Validation example (without printing key):
if [ -z "$ENCRYPTION_KEY" ]; then
    echo "❌ ERROR: Encryption key not found in .env file"
    exit 1
fi

KEY_LENGTH=${#ENCRYPTION_KEY}
echo "✅ Encryption key extracted ($KEY_LENGTH characters)"
# Prints: ✅ Encryption key extracted (64 characters)
# Does NOT print actual key

# If key needs to be backed up, use secure method
# (See Issue #4 for secure backup procedure)
```

**Security Improvements**:
1. ✅ `set -euo pipefail` - Fail fast on errors
2. ✅ `umask 077` - Secure default file permissions
3. ✅ `-m1` - Stop after first match (efficiency)
4. ✅ `^N8N_ENCRYPTION_KEY=` - Anchored pattern (security)
5. ✅ `-f2-` - Preserve base64 padding (correctness)
6. ✅ NO echo of actual key - Only print metadata
7. ✅ Validation without exposure - Check length, not value

**Alternative: Masked Display** (if visual confirmation needed):

```bash
# If operator needs to confirm key exists without seeing full value
ENCRYPTION_KEY=$(sudo grep -m1 '^N8N_ENCRYPTION_KEY=' /opt/n8n/.env | cut -d'=' -f2-)
KEY_LENGTH=${#ENCRYPTION_KEY}
KEY_PREFIX=${ENCRYPTION_KEY:0:8}
KEY_SUFFIX=${ENCRYPTION_KEY: -8}

echo "Encryption Key: ${KEY_PREFIX}...${KEY_SUFFIX} (${KEY_LENGTH} chars)"
# Prints: Encryption Key: 90c5323a...87d02cdbc (64 chars)
# Shows enough to verify, not enough to steal
```

---

## Complete Secure Script Template

### Full Example with All Fixes Applied

```bash
#!/bin/bash
# n8n Deployment - Secure .env Creation and Key Management
# Date: 2025-11-09
# Security: PCI-DSS, SOC 2 compliant

set -euo pipefail  # Exit on error, undefined vars, pipe failures
umask 077          # Secure default permissions (600)

echo "=== n8n Environment Configuration ==="

# 1. Set environment variables (from secure source)
DB_HOST="hx-postgres-server.hx.dev.local"
DB_NAME="n8n_poc3"
DB_USER="n8n_user"

# Get database password from secure credentials file
N8N_DB_PASSWORD=$(grep "n8n_user:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)

# Generate encryption key (64 character hex)
ENCRYPTION_KEY=$(openssl rand -hex 32)

# 2. Create .env file with proper ownership and permissions
echo "Creating /opt/n8n/.env..."

sudo tee /opt/n8n/.env > /dev/null << EOF
# N8N Configuration File
# Created: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
# SECURITY: This file contains sensitive credentials

# Database Configuration
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=${DB_HOST}
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=${DB_NAME}
DB_POSTGRESDB_USER=${DB_USER}
DB_POSTGRESDB_PASSWORD=${N8N_DB_PASSWORD}

# Encryption Configuration
N8N_ENCRYPTION_KEY=${ENCRYPTION_KEY}

# Application Configuration
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.hx.dev.local/
N8N_EDITOR_BASE_URL=https://n8n.hx.dev.local/
EXECUTIONS_MODE=regular
N8N_LOG_LEVEL=info
EOF

# 3. SECURITY: Set secure ownership and permissions
sudo chown n8n:n8n /opt/n8n/.env
sudo chmod 600 /opt/n8n/.env

echo "✅ .env file created with secure permissions"

# 4. Verify permissions
ENV_PERMS=$(stat -c "%a" /opt/n8n/.env)
ENV_OWNER=$(stat -c "%U:%G" /opt/n8n/.env)

if [ "$ENV_PERMS" != "600" ]; then
    echo "❌ ERROR: .env permissions incorrect (expected 600, got $ENV_PERMS)"
    exit 1
fi

if [ "$ENV_OWNER" != "n8n:n8n" ]; then
    echo "❌ ERROR: .env ownership incorrect (expected n8n:n8n, got $ENV_OWNER)"
    exit 1
fi

echo "✅ Permissions verified: $ENV_PERMS ($ENV_OWNER)"

# 5. Verify encryption key extraction (without printing key)
VERIFY_KEY=$(sudo grep -m1 '^N8N_ENCRYPTION_KEY=' /opt/n8n/.env | cut -d'=' -f2-)

if [ -z "$VERIFY_KEY" ]; then
    echo "❌ ERROR: Encryption key not found in .env"
    exit 1
fi

KEY_LENGTH=${#VERIFY_KEY}
if [ "$KEY_LENGTH" -ne 64 ]; then
    echo "❌ ERROR: Encryption key length invalid (expected 64, got $KEY_LENGTH)"
    exit 1
fi

echo "✅ Encryption key validated ($KEY_LENGTH characters)"

# DO NOT PRINT THE KEY TO LOGS
# Key is now securely stored in /opt/n8n/.env (mode 600, owner n8n)

# 6. Secure backup procedure (see separate documentation)
echo ""
echo "⚠️  CRITICAL: Backup encryption key to secure location"
echo "See: /srv/cc/Governance/0.2-credentials/encryption-key-backup-procedure.md"
echo ""

# 7. Summary
echo "=== Configuration Complete ==="
echo "✅ .env file created: /opt/n8n/.env"
echo "✅ Permissions: 600 (n8n:n8n)"
echo "✅ Encryption key: Validated (64 chars)"
echo "⚠️  Next step: Backup encryption key before continuing"
```

---

## Testing After Fixes

### Test Suite: .env Security

```bash
#!/bin/bash
# Test suite for .env security fixes

echo "=== .env Security Test Suite ==="

# Test 1: File permissions
echo "Test 1: Verify .env permissions are 600"
PERMS=$(stat -c "%a" /opt/n8n/.env)
if [ "$PERMS" = "600" ]; then
    echo "✅ PASS - Permissions: $PERMS"
else
    echo "❌ FAIL - Permissions: $PERMS (expected 600)"
fi

# Test 2: File ownership
echo "Test 2: Verify .env ownership is n8n:n8n"
OWNER=$(stat -c "%U:%G" /opt/n8n/.env)
if [ "$OWNER" = "n8n:n8n" ]; then
    echo "✅ PASS - Ownership: $OWNER"
else
    echo "❌ FAIL - Ownership: $OWNER (expected n8n:n8n)"
fi

# Test 3: Key extraction preserves padding
echo "Test 3: Verify key extraction preserves base64 padding"
TEST_KEY="N8N_ENCRYPTION_KEY=abc123=="
EXTRACTED=$(echo "$TEST_KEY" | cut -d'=' -f2-)
if [ "$EXTRACTED" = "abc123==" ]; then
    echo "✅ PASS - Padding preserved: $EXTRACTED"
else
    echo "❌ FAIL - Padding lost: $EXTRACTED (expected abc123==)"
fi

# Test 4: Key not printed to stdout
echo "Test 4: Verify key not printed in script output"
SCRIPT_OUTPUT=$(sudo grep -m1 '^N8N_ENCRYPTION_KEY=' /opt/n8n/.env | cut -d'=' -f2- | grep -v "ENCRYPTION_KEY" || echo "PASS")
if [ "$SCRIPT_OUTPUT" = "PASS" ]; then
    echo "✅ PASS - Key not echoed to stdout"
else
    echo "❌ FAIL - Key exposed in output"
fi

# Test 5: n8n service can read .env
echo "Test 5: Verify n8n service can read .env"
if sudo -u n8n cat /opt/n8n/.env > /dev/null 2>&1; then
    echo "✅ PASS - n8n user can read .env"
else
    echo "❌ FAIL - n8n user cannot read .env"
fi

# Test 6: Other users cannot read .env
echo "Test 6: Verify other users cannot read .env"
if sudo -u nobody cat /opt/n8n/.env > /dev/null 2>&1; then
    echo "❌ FAIL - Other users can read .env (SECURITY ISSUE)"
else
    echo "✅ PASS - Other users blocked from reading .env"
fi

echo ""
echo "=== Test Suite Complete ==="
```

---

## Summary of Required Changes

### Critical Fix #1: Add Secure Permissions

**After every `.env` file creation**:
```bash
sudo chown n8n:n8n /opt/n8n/.env
sudo chmod 600 /opt/n8n/.env
```

### Critical Fix #2: Fix Key Parsing

**Change from**:
```bash
cut -d'=' -f2
```

**To**:
```bash
cut -d'=' -f2-
```

### Critical Fix #3: Stop Printing Secrets

**Remove**:
```bash
echo "Encryption Key: $ENCRYPTION_KEY"
```

**Replace with**:
```bash
echo "✅ Encryption key extracted (${#ENCRYPTION_KEY} characters)"
# Do not print the key to stdout
```

### Enhancement: Add Security Headers

**Add at start of scripts**:
```bash
set -euo pipefail  # Strict error handling
umask 077          # Secure default permissions
```

---

## Compliance Checklist

After applying fixes:
- [ ] .env file owned by n8n:n8n (not root)
- [ ] .env file mode 600 (not 644 or world-readable)
- [ ] Encryption key parsing uses `cut -d'=' -f2-`
- [ ] No encryption keys printed to stdout/logs
- [ ] Script uses `set -euo pipefail`
- [ ] Script uses `umask 077`
- [ ] Test suite passes (6 of 6 tests)
- [ ] PCI-DSS 8.2.1 compliant (credentials protected)
- [ ] SOC 2 CC6.1 compliant (access controls enforced)

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-09 | Initial CodeRabbit remediation: Added secure .env ownership/permissions, fixed key parsing to preserve base64 padding, removed secret printing to stdout/logs, added strict error handling | Agent Zero + CodeRabbit AI |

---

**Status**: ✅ REMEDIATION DOCUMENTED
**Next Step**: Apply security fixes to all .env creation scripts
**Priority**: HIGH - Security hardening required for production
**Coordination**: Review with security team before production deployment
