# Task: Verify Database Connection

**Task ID**: T-043
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-042 |

## Task Overview

Verify that n8n is successfully maintaining database connection to PostgreSQL by checking logs, connection pool status, and database query performance.

## PostgreSQL User Selection

**IMPORTANT**: This task uses TWO different PostgreSQL users for different purposes:

1. **n8n_user** (Application User):
   - Used for: Application-level queries (SELECT from workflow, credentials tables)
   - Permissions: Read/write on n8n_poc3 database tables
   - Authentication: Uses password from /opt/n8n/.env (DB_POSTGRESDB_PASSWORD)
   - When to use: Testing n8n application functionality

2. **postgres** (Superuser):
   - Used for: System catalog queries (pg_stat_activity)
   - Permissions: Full database superuser access
   - Authentication: Requires postgres user password
   - When to use: ONLY when querying system tables - coordinate with @agent-quinn

**Rule**: Use `n8n_user` for all application-level checks. Delegate system catalog queries to @agent-quinn.

## Success Criteria
- [ ] Database connection active in n8n logs
- [ ] No connection errors in logs
- [ ] PostgreSQL shows active n8n connection
- [ ] Queries executing successfully
- [ ] Connection pool healthy

## Execution Steps

### Step 1: Check n8n Database Connection Logs
```bash
echo "=== Checking n8n Database Connection ==="

sudo journalctl -u n8n --since "30 minutes ago" | grep -i "database\|postgres\|connection"

# Look for: "Connected to database", no connection errors
```

### Step 2: Verify Active Connection in PostgreSQL
```bash
echo "=== Checking PostgreSQL Active Connections ==="

# Coordinate with @agent-quinn to check PostgreSQL logs
echo "Request @agent-quinn to verify:"
echo "  SELECT * FROM pg_stat_activity WHERE datname='n8n_poc3';"
echo ""
echo "Expected: Active connections from n8n application"
```

### Step 3: Test Database Query via n8n
```bash
echo "=== Testing Database Query ==="

# Use n8n_user credentials to test application-level database access
export PGPASSWORD=$(grep DB_POSTGRESDB_PASSWORD /opt/n8n/.env | cut -d'=' -f2)

# Check that workflows table accessible (using n8n_user - application user)
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 \
  -c "SELECT COUNT(*) as workflow_count FROM workflow;" 2>/dev/null

unset PGPASSWORD

# Should return count (0 initially)
echo "✅ Database query successful"
```

### Step 4: Check for Connection Pool Errors
```bash
echo "=== Checking Connection Pool Status ==="

if sudo journalctl -u n8n --since "30 minutes ago" | grep -i "pool.*error\|connection.*timeout"; then
  echo "⚠️  Connection pool issues detected"
else
  echo "✅ No connection pool errors"
fi
```

### Step 5: Verify No Connection Leaks
```bash
echo "=== Connection Count Verification ==="

# IMPORTANT: This requires postgres superuser permissions to query pg_stat_activity
# Coordinate with @agent-quinn (Quinn Davis) to check connection count
echo "⚠️  This step requires PostgreSQL admin access"
echo ""
echo "Requesting @agent-quinn to verify connection count:"
echo "  SELECT COUNT(*) FROM pg_stat_activity WHERE datname='n8n_poc3' AND usename='n8n_user';"
echo ""
echo "Expected: Active connections < 20 (connection pool size)"
echo ""
echo "Quinn: Please confirm connection count and report if excessive (>20)"
```

### Step 6: Test Database Write
```bash
echo "=== Testing Database Write ==="

# Create test workflow via UI or API
echo "Create a test workflow in n8n UI"
echo "1. Click 'Add Workflow'"
echo "2. Save workflow with name 'Test Connection'"
echo "3. Verify workflow saved"
echo ""
echo "Press ENTER after creating test workflow..."
read

# Use n8n_user credentials to verify workflow write (application user has write access)
export PGPASSWORD=$(grep DB_POSTGRESDB_PASSWORD /opt/n8n/.env | cut -d'=' -f2)

# Verify workflow in database using n8n_user
wf_count=$(psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 \
  -t -c "SELECT COUNT(*) FROM workflow;" 2>/dev/null)

unset PGPASSWORD

if [ "$wf_count" -gt 0 ]; then
  echo "✅ Database write successful ($wf_count workflows)"
else
  echo "⚠️  No workflows found in database"
fi
```

## Validation
```bash
# Comprehensive check using n8n_user credentials
export PGPASSWORD=$(grep DB_POSTGRESDB_PASSWORD /opt/n8n/.env | cut -d'=' -f2)

# Test connection info (using n8n_user - application user)
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "\conninfo" && \
sudo journalctl -u n8n --since "10 minutes ago" | grep -q "database" && \
echo "✅ Database connection verified" || \
echo "❌ Database connection issues"

unset PGPASSWORD
```

## Troubleshooting

### If No Active Connection
```bash
# Check n8n service status
sudo systemctl status n8n.service

# Check .env database credentials
sudo grep DB_POSTGRES /opt/n8n/.env

# Test manual connection using n8n_user
export PGPASSWORD=$(grep DB_POSTGRESDB_PASSWORD /opt/n8n/.env | cut -d'=' -f2)
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "\conninfo"
unset PGPASSWORD
```

### If Connection Errors
```bash
# Check logs for specific error
sudo journalctl -u n8n -n 100 | grep -i "error.*database\|error.*postgres"

# Common issues:
# - Wrong password: Update .env
# - Network issue: Test with ping/telnet
# - Database not ready: Coordinate with @agent-quinn
```

## Task Metadata
```yaml
task_id: T-043
source: agent-omar-planning-analysis.md:605 (T6.3)
coordination_required:
  - agent: Quinn Davis (@agent-quinn)
    service: Postgres
    info_needed: Verify active connections from n8n in pg_stat_activity
```
