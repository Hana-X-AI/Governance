# Task: Create DNS A Record for n8n.hx.dev.local

**Task ID**: T-001
**Assigned Agent**: @agent-frank
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Parallel
**Dependencies**: None
**Estimated Duration**: 15 minutes

---

## Objective
Create DNS A record `n8n.hx.dev.local` → `192.168.10.215` in Samba AD DC.

## Commands

```bash
# Connect to Samba server
ssh administrator@192.168.10.200

# Create DNS A record
samba-tool dns add 192.168.10.200 hx.dev.local n8n A 192.168.10.215 \
  -U administrator --password='Major3059!'

# Verify
samba-tool dns query 192.168.10.200 hx.dev.local n8n A \
  -U administrator --password='Major3059!'

nslookup n8n.hx.dev.local 192.168.10.200
```

## Success Criteria
- [ ] DNS record created
- [ ] Resolution returns 192.168.10.215
- [ ] Resolution time < 100ms

## Validation
```bash
dig @192.168.10.200 n8n.hx.dev.local +short
# Expected: 192.168.10.215
```

---
**Source**: phase3-execution-plan.md:159-179, agent-frank-planning-analysis.md:23-56
