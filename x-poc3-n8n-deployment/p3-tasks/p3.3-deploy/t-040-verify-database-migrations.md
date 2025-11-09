# Task: Verify Database Migrations

**Task ID**: T-040
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-039 |

## Task Overview

Verify that n8n's TypeORM database migrations executed successfully during first startup, creating all required tables and schema in the n8n_poc3 database.

## Success Criteria
- [ ] TypeORM migrations completed without errors
- [ ] Database schema created (tables, indexes, constraints)
- [ ] Migration log shows successful execution
- [ ] Key tables present (workflow, credentials, execution, user)
- [ ] No migration errors in logs

## Execution Steps

### Step 1: Check Migration Logs
```bash
echo "=== Checking Migration Logs ==="
sudo journalctl -u n8n --since "10 minutes ago" | grep -i "migration\|typeorm"
# Look for: "migration", "schema", "table created"
```

### Step 2: Verify Database Tables Created
```bash
echo "=== Verifying Database Schema ==="

# List tables (coordinate with Quinn for psql access if needed)
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "\dt" 2>/dev/null

# Expected tables include:
# - workflow
# - credentials_entity
# - execution_entity
# - user
# - settings
# - tag_entity
# - webhook_entity
```

### Step 3: Count Tables
```bash
table_count=$(psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 \
  -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null)

echo "Tables created: $table_count"

if [ "$table_count" -gt 10 ]; then
  echo "✅ Database schema initialized ($table_count tables)"
else
  echo "⚠️  Fewer tables than expected ($table_count)"
fi
```

### Step 4: Check for Migration Errors
```bash
echo "=== Checking for Migration Errors ==="

if sudo journalctl -u n8n --since "10 minutes ago" | grep -i "migration.*error\|migration.*failed"; then
  echo "❌ Migration errors found"
  exit 1
else
  echo "✅ No migration errors"
fi
```

### Step 5: Verify Key Tables
```bash
echo "=== Verifying Key Tables ==="

key_tables=("workflow" "credentials_entity" "execution_entity" "user")

for table in "${key_tables[@]}"; do
  if psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 \
    -t -c "SELECT 1 FROM information_schema.tables WHERE table_name='$table';" 2>/dev/null | grep -q 1; then
    echo "✅ Table exists: $table"
  else
    echo "❌ Table missing: $table"
  fi
done
```

## Validation
```bash
# Quick validation
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 \
  -c "SELECT tablename FROM pg_tables WHERE schemaname='public';" 2>/dev/null | wc -l

# Should show 15-20 tables
```

## Troubleshooting

### If Migrations Failed
```bash
# Check full logs
sudo journalctl -u n8n --since "15 minutes ago" --no-pager | grep -A 10 -B 10 migration

# Common issues:
# - Database permissions: Coordinate with @agent-quinn
# - Schema already exists: May need to drop and recreate database
# - Connection timeout: Check network/firewall
```

### If Tables Missing
```bash
# Restart service to re-run migrations
sudo systemctl restart n8n.service
sleep 10
# Re-check tables
```

## Task Metadata
```yaml
task_id: T-040
source: agent-omar-planning-analysis.md:578 (T5.4)
coordination_required:
  - agent: Quinn Davis (@agent-quinn)
    service: Postgres
    info_needed: Database access to verify schema creation
```
