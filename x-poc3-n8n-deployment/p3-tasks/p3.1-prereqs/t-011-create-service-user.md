# Task: Create n8n Service User

**Task ID**: T-011
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-004
**Estimated Duration**: 10 minutes

---

## Objective
Create dedicated system user `n8n` for running n8n service.

## Commands

```bash
# Create system user with no login shell
sudo useradd -r -m -s /usr/sbin/nologin -d /opt/n8n -U n8n

# Verify user creation
id n8n
grep n8n /etc/passwd
grep n8n /etc/group

# Verify home directory
ls -ld /opt/n8n
```

## Success Criteria
- [ ] User `n8n` created (system user)
- [ ] Group `n8n` exists
- [ ] Home directory `/opt/n8n` exists
- [ ] No login shell configured

## Validation
```bash
id n8n
getent passwd n8n
ls -ld /opt/n8n
```

---
**Source**: phase3-execution-plan.md:283-313, agent-william-planning-analysis.md:513-531
