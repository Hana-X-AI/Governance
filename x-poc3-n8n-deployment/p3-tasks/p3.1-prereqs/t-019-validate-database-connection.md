# Task: Validate Database Connection

**Task ID**: T-019
**Assigned Agent**: @agent-quinn
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-018, T-007
**Estimated Duration**: 30 minutes

---

## Objective
Test database connectivity from hx-n8n-server and verify privileges.

## Commands

```bash
# From hx-n8n-server
ssh administrator@192.168.10.215

# Test connection
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3

# Test query
SELECT version();

# Test CREATE privilege
CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(100));
INSERT INTO test_table (name) VALUES ('test');
SELECT * FROM test_table;
DROP TABLE test_table;

# Exit
\q
```

## Success Criteria
- [ ] Connection successful from n8n server
- [ ] All privileges verified (CREATE, SELECT, INSERT, DELETE)
- [ ] Test table operations successful

## Validation
```bash
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3 -c "SELECT 1"
```

---
**Source**: phase3-execution-plan.md:376-401
