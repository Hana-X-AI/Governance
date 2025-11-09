# Task: Start n8n Service

**Task ID**: T-039
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 5-10 minutes |
| **Dependencies** | T-038, Database ready from Quinn |

## Task Overview

Start the n8n service for the first time and monitor startup logs to ensure successful initialization, database connection, and web server start.

## Success Criteria
- [ ] Service starts without errors
- [ ] Process running as n8n user
- [ ] Listening on port 5678
- [ ] Database connection established
- [ ] Web UI initializes
- [ ] No critical errors in logs

## Blocking Dependencies
- [ ] Database n8n_poc3 ready (from @agent-quinn)
- [ ] Database credentials in .env (T-033)

## Execution Steps

### Step 1: Pre-Start Verification
```bash
echo "=== Pre-Start Checks ==="

# Verify database password set
if grep -q '<INSERT_FROM_QUINN>' /opt/n8n/.env; then
  echo "❌ BLOCKER: Database password not set in .env"
  echo "⚠️  Coordinate with @agent-quinn to get password"
  exit 1
fi
echo "✅ Database credentials configured in .env"

# Test actual database connection with credentials (not just port reachability)
echo "Testing database connection with n8n_user credentials..."
export PGPASSWORD=$(grep DB_POSTGRESDB_PASSWORD /opt/n8n/.env | cut -d'=' -f2)

if psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "SELECT 1" >/dev/null 2>&1; then
  echo "✅ Database connection successful - credentials valid"
  echo "✅ User n8n_user has access to database n8n_poc3"
else
  echo "❌ BLOCKER: Database connection FAILED"
  echo "Possible causes:"
  echo "  - Incorrect password in .env file"
  echo "  - User n8n_user does not exist"
  echo "  - Database n8n_poc3 does not exist"
  echo "  - User lacks permissions to access database"
  echo "  - PostgreSQL server not running on hx-postgres-server.hx.dev.local:5432"
  echo ""
  echo "⚠️  Coordinate with @agent-quinn to verify:"
  echo "  1. Database n8n_poc3 exists"
  echo "  2. User n8n_user exists with correct password"
  echo "  3. User has CONNECT and CREATE privileges"
  unset PGPASSWORD
  exit 1
fi

unset PGPASSWORD
echo "✅ Pre-start verification complete"
```

### Step 2: Start Service with Log Monitoring
```bash
echo "=== Starting n8n Service ==="
echo "Start time: $(date)"

# Start in one terminal
sudo systemctl start n8n.service

# Give it a moment to initialize
sleep 5
```

### Step 3: Monitor Startup Logs
```bash
echo "=== Monitoring Startup Logs ==="
# Watch logs for 60 seconds or until "ready"
timeout 60s sudo journalctl -u n8n -f &
TAIL_PID=$!

# Wait for startup completion
for i in {1..60}; do
  if sudo journalctl -u n8n | grep -q "n8n ready"; then
    echo "✅ n8n started successfully"
    kill $TAIL_PID 2>/dev/null
    break
  fi
  sleep 1
done
```

### Step 4: Check Service Status
```bash
echo "=== Service Status ==="
sudo systemctl status n8n.service

# Should show: Active: active (running)
```

### Step 5: Verify Process Running
```bash
echo "=== Process Verification ==="
ps aux | grep '[n]8n'
# Should show node process running as n8n user
```

### Step 6: Verify Port Listening
```bash
echo "=== Port Check ==="
sudo ss -tlnp | grep :5678
# Should show node listening on port 5678
echo "✅ Service listening on port 5678"
```

### Step 7: Check for Errors in Logs
```bash
echo "=== Error Check ==="
if sudo journalctl -u n8n --since "5 minutes ago" | grep -i "error\|fatal\|exception"; then
  echo "⚠️  Errors found in logs - review required"
else
  echo "✅ No critical errors in startup logs"
fi
```

## Validation
```bash
systemctl is-active n8n.service | grep -q "active" && \
sudo ss -tlnp | grep -q ":5678" && \
echo "✅ Service running and accessible" || \
echo "❌ Service not running properly"
```

## Troubleshooting

### If Service Fails to Start
```bash
# Check logs for specific error
sudo journalctl -u n8n -n 50 --no-pager

# Common issues:
# - Database connection: Check credentials in .env
# - Port already in use: Check with 'sudo ss -tlnp | grep 5678'
# - Permission errors: Verify ownership (T-030)
# - Missing dependencies: Check node_modules (T-029)
```

### If Database Connection Fails
```bash
# Test database connection manually
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3
# Coordinate with @agent-quinn if connection fails
```

## Task Metadata
```yaml
task_id: T-039
source: agent-omar-planning-analysis.md:577 (T5.3)
coordination_required:
  - agent: Quinn Davis (@agent-quinn)
    service: Postgres
    info_needed: Confirm database n8n_poc3 ready and accessible
```
