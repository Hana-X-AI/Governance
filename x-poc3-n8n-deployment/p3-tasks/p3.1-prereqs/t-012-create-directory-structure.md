# Task: Create Directory Structure

**Task ID**: T-012
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-011
**Estimated Duration**: 15 minutes

---

## Objective
Create all required directories for n8n with proper permissions.

## Commands

```bash
# Create application directories
sudo mkdir -p /opt/n8n/{.n8n,app,backups}
sudo mkdir -p /opt/n8n/.n8n/{config,nodes,static}

# Create log directory
sudo mkdir -p /var/log/n8n

# Create backup directory
sudo mkdir -p /srv/n8n/backups

# Set ownership
sudo chown -R n8n:n8n /opt/n8n
sudo chown -R n8n:n8n /var/log/n8n
sudo chown -R n8n:n8n /srv/n8n

# Set permissions
sudo chmod 755 /opt/n8n
sudo chmod 700 /opt/n8n/.n8n  # CRITICAL: Encryption key security
sudo chmod 755 /opt/n8n/.n8n/config
sudo chmod 755 /opt/n8n/.n8n/nodes
sudo chmod 755 /opt/n8n/.n8n/static
sudo chmod 700 /opt/n8n/backups  # CRITICAL: Encryption key backup security
sudo chmod 755 /var/log/n8n
sudo chmod 755 /srv/n8n
```

## Success Criteria
- [ ] All directories created
- [ ] Correct ownership (n8n:n8n)
- [ ] Correct permissions (/opt/n8n/.n8n = 700, /opt/n8n/backups = 700)

## Validation
```bash
tree -L 3 -p /opt/n8n
ls -ld /opt/n8n/backups  # Should show drwx------ (700) n8n:n8n
ls -la /var/log/n8n
ls -la /srv/n8n
```

---
**Source**: phase3-execution-plan.md:283-313, agent-william-planning-analysis.md:533-569
