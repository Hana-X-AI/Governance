# Task: Transfer SSL Certificate to hx-n8n-server

**Task ID**: T-003
**Assigned Agent**: @agent-frank
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-002, T-004
**Estimated Duration**: 30 minutes

---

## Objective
Transfer SSL certificate files from hx-freeipa-server to hx-n8n-server.

## Commands

```bash
# From hx-freeipa-server
scp /etc/ssl/private/n8n.hx.dev.local.key administrator@192.168.10.215:/tmp/
scp /etc/ssl/certs/n8n.hx.dev.local.crt administrator@192.168.10.215:/tmp/
scp /etc/ssl/certs/hx-dev-ca.crt administrator@192.168.10.215:/tmp/

# On hx-n8n-server
ssh administrator@192.168.10.215

sudo mkdir -p /etc/ssl/private /etc/ssl/certs
sudo mv /tmp/n8n.hx.dev.local.key /etc/ssl/private/
sudo mv /tmp/n8n.hx.dev.local.crt /etc/ssl/certs/
sudo mv /tmp/hx-dev-ca.crt /etc/ssl/certs/

sudo chown root:root /etc/ssl/private/n8n.hx.dev.local.key
sudo chmod 600 /etc/ssl/private/n8n.hx.dev.local.key
sudo chown root:root /etc/ssl/certs/n8n.hx.dev.local.crt
sudo chmod 644 /etc/ssl/certs/n8n.hx.dev.local.crt
```

## Success Criteria
- [ ] Certificate files transferred securely
- [ ] Correct ownership (root:root)
- [ ] Correct permissions (key: 600, cert: 644)

## Validation
```bash
ls -la /etc/ssl/private/n8n.hx.dev.local.key
ls -la /etc/ssl/certs/n8n.hx.dev.local.crt
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -subject
```

---
**Source**: phase3-execution-plan.md:440-470, agent-frank-planning-analysis.md:124-135
