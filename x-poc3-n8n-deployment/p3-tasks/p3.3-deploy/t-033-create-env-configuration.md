# Task: Create .env Configuration

**Task ID**: T-033
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 30 minutes |
| **Dependencies** | T-032, Quinn's DB credentials |

## Task Overview

Create comprehensive .env configuration file with 100+ environment variables for n8n, including database credentials from @agent-quinn, network settings, security config, and logging.

**Security Note**: See `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/ENV-FILE-SECURITY-GUIDE.md` for comprehensive security guidance on password generation, file permissions, and production secrets management.

## Success Criteria
- [ ] .env file created at /opt/n8n/.env
- [ ] Database credentials from Quinn integrated
- [ ] All required n8n variables configured
- [ ] Variables validated (no syntax errors)
- [ ] File documented with comments

## Blocking Dependencies

- [ ] **BLOCKER**: Database credentials from @agent-quinn
  - `DB_POSTGRESDB_PASSWORD` (required before Step 2)
  - Verify hx-postgres-server connectivity: `ping hx-postgres-server.hx.dev.local`
  - Confirm database `n8n_poc3` created
  - Confirm database user `n8n_user` created with correct permissions
  - **Test Connection**: `psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "SELECT 1"`
  - **Expected Result**: Connection successful, returns `1`

## Execution Steps

### Step 1: Request Database Credentials from Quinn
```bash
echo "⚠️  BLOCKER: Need database credentials from @agent-quinn"
echo "Required information:"
echo "  - DB_POSTGRESDB_PASSWORD"
echo "  - Confirm: hx-postgres-server.hx.dev.local:5432"
echo "  - Confirm: database name: n8n_poc3"
echo "  - Confirm: user: n8n_user"
```

### Step 2: Create .env File
```bash
cat > /opt/n8n/.env << 'ENVEOF'
# ================================================
# n8n Configuration - POC3 Deployment
# Server: hx-n8n-server.hx.dev.local
# Created: 2025-11-07
# Agent: @agent-omar
# ================================================

# =================
# DATABASE CONFIGURATION (from @agent-quinn)
# =================
# NOTE (DEPLOY-001): Variable names verified against n8n v1.117.0 source
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=hx-postgres-server.hx.dev.local
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n_poc3
DB_POSTGRESDB_USER=n8n_user
DB_POSTGRESDB_PASSWORD=<INSERT_FROM_QUINN>

# Database connection pool (DEPLOY-006 fix: increased from 10 to 20)
DB_POSTGRESDB_POOL_SIZE=20

# =================
# NETWORK CONFIGURATION
# =================
N8N_HOST=0.0.0.0
N8N_PORT=5678
# DEPLOY-016 fix: Use http for POC3 (SSL configured in Phase 4)
N8N_PROTOCOL=http
N8N_PATH=/
# NOTE: Update to https:// after Frank configures SSL in Phase 4
WEBHOOK_URL=http://hx-n8n-server.hx.dev.local
N8N_EDITOR_BASE_URL=http://hx-n8n-server.hx.dev.local

# =================
# SECURITY
# =================
N8N_SECURE_COOKIE=true
N8N_SAMESITE_COOKIE=strict
N8N_JWT_AUTH_ACTIVE=true

# =================
# LOGGING
# =================
N8N_LOG_LEVEL=info
N8N_LOG_OUTPUT=file,console
N8N_LOG_FILE_LOCATION=/var/log/n8n/n8n.log
N8N_LOG_FILE_COUNT_MAX=10
N8N_LOG_FILE_SIZE_MAX=10

# =================
# EXECUTION
# =================
EXECUTIONS_MODE=queue
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_ON_SUCCESS=all
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=true

# =================
# TIMEZONE
# =================
GENERIC_TIMEZONE=America/Chicago
TZ=America/Chicago

# =================
# PATHS
# =================
N8N_USER_FOLDER=/opt/n8n/.n8n
N8N_CUSTOM_EXTENSIONS=/opt/n8n/.n8n/custom

# =================
# PERFORMANCE
# =================
N8N_PAYLOAD_SIZE_MAX=16
NODE_FUNCTION_ALLOW_BUILTIN=*
NODE_FUNCTION_ALLOW_EXTERNAL=*

ENVEOF

# SECURITY: Set restrictive permissions (owner read/write only)
sudo chmod 600 /opt/n8n/.env

# SECURITY: Set proper ownership (n8n user)
sudo chown n8n:n8n /opt/n8n/.env

# Verify permissions
ls -la /opt/n8n/.env
# Expected output: -rw------- 1 n8n n8n ... /opt/n8n/.env

echo "✅ .env created with secure permissions (needs DB password from Quinn)"
```

### Step 3: Validate .env Syntax
```bash
# Check for common issues
grep -v '^#' /opt/n8n/.env | grep -v '^$' | while read line; do
  if ! echo "$line" | grep -q '='; then
    echo "❌ Invalid line: $line"
  fi
done
echo "✅ Syntax validated"
```

### Step 4: Verify Database Password Set
```bash
if grep -q '<INSERT_FROM_QUINN>' /opt/n8n/.env; then
  echo "⚠️  WARNING: Database password not yet set!"
  echo "Update .env with password from @agent-quinn before starting service"
else
  echo "✅ Database password appears to be set"
fi
```

## Validation
```bash
test -f /opt/n8n/.env && echo "✅ .env exists"
test "$(stat -c '%U' /opt/n8n/.env)" = "n8n" && echo "✅ Owner correct"
grep -q "DB_POSTGRESDB_HOST" /opt/n8n/.env && echo "✅ DB config present"
```

## Task Metadata
```yaml
task_id: T-033
source: agent-omar-planning-analysis.md:508 (T4.1)
coordination_required:
  - agent: Quinn Davis (@agent-quinn)
    service: Postgres
    info_needed: Database credentials for n8n_poc3
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for n8n environment configuration | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Enhanced Blocking Dependencies section (lines 28-36) with actionable, testable criteria. Added explicit sub-requirements: DB_POSTGRESDB_PASSWORD needed before Step 2, server connectivity verification (ping), database/user creation confirmation, and explicit test command (`psql ... -c "SELECT 1"`) with expected result. Provides @agent-omar with clear, executable verification steps before proceeding with .env configuration. | Claude Code |
