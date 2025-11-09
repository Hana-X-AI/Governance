# Task: Create PostgreSQL Database

**Task ID**: T-017
**Assigned Agent**: @agent-quinn
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Parallel
**Dependencies**: None
**Estimated Duration**: 15 minutes

---

## Objective
Create PostgreSQL database n8n_poc3 with UTF8 encoding.

## Commands

```bash
# Connect to hx-postgres-server
ssh administrator@192.168.10.209

# Switch to postgres user
sudo -u postgres psql

# Create database
CREATE DATABASE n8n_poc3
  WITH ENCODING='UTF8'
  LC_COLLATE='en_US.UTF-8'
  LC_CTYPE='en_US.UTF-8'
  TEMPLATE=template0;  -- Use template0 for clean, reproducible database

# Verify
\l n8n_poc3
```

**Note**: `TEMPLATE=template0` is PostgreSQL best practice for production deployments:
- `template0` is the unmodified PostgreSQL template (guaranteed clean state)
- `template1` may contain custom objects from prior configurations
- Ensures consistent, reproducible database creation across environments
- Required when specifying non-default encoding (UTF8) or locale settings

## Success Criteria
- [ ] Database n8n_poc3 created
- [ ] UTF8 encoding configured
- [ ] Database visible in listing

## Validation
```bash
sudo -u postgres psql -c "\l n8n_poc3"
```

---
**Source**: phase3-execution-plan.md:315-357, agent-quinn-planning-analysis.md:49-53
