# Task: Set .env Permissions

**Task ID**: T-035
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical (Security) |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-033 |

## Task Overview

Set restrictive permissions (600) on .env file to protect sensitive credentials including database passwords from unauthorized access.

## Success Criteria
- [ ] .env file permissions set to 600 (rw-------)
- [ ] File owned by n8n:n8n
- [ ] Only n8n user can read file
- [ ] File not readable by other users

## Execution Steps

### Step 1: Set Restrictive Permissions
```bash
sudo chmod 600 /opt/n8n/.env
echo "✅ Permissions set to 600"
```

### Step 2: Verify Ownership
```bash
sudo chown n8n:n8n /opt/n8n/.env
owner=$(stat -c '%U:%G' /opt/n8n/.env)
echo "Owner: $owner"
test "$owner" = "n8n:n8n" && echo "✅ Ownership correct"
```

### Step 3: Verify Permissions
```bash
perms=$(stat -c '%a' /opt/n8n/.env)
echo "Permissions: $perms"
test "$perms" = "600" && echo "✅ Permissions correct (rw-------)"
```

### Step 4: Test Access Restrictions
```bash
# Test that other users cannot read (should fail)
sudo -u nobody cat /opt/n8n/.env 2>&1 | grep -q "Permission denied" && \
echo "✅ File protected from other users" || \
echo "⚠️  WARNING: File may be readable by others"
```

## Validation
```bash
ls -la /opt/n8n/.env
# Expected: -rw------- 1 n8n n8n ... /opt/n8n/.env
```

## Task Metadata
```yaml
task_id: T-035
source: agent-omar-planning-analysis.md:510 (T4.3)
```
