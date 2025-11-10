# Task: Install PostgreSQL Client

**Task ID**: T-007
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Parallel
**Dependencies**: T-004
**Estimated Duration**: 10 minutes

---

## Objective
Install PostgreSQL client tools for database connectivity testing.

**Target OS**: Ubuntu 24.04 LTS

## Commands

```bash
# Install PostgreSQL client 16 (Ubuntu 24.04 default)
sudo apt install -y postgresql-client-16

# Verify installation
psql --version
# Expected: psql (PostgreSQL) 16.x
```

## Success Criteria
- [ ] PostgreSQL client installed
- [ ] psql command functional

## Validation
```bash
psql --version
which psql
```

---
**Source**: agent-william-planning-analysis.md:431-447
