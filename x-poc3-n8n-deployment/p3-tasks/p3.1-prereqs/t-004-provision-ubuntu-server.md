# Task: Provision Ubuntu Server

**Task ID**: T-004
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Parallel
**Dependencies**: None
**Estimated Duration**: 30-45 minutes

---

## Objective
Provision hx-n8n-server with Ubuntu 22.04/24.04 LTS and apply system updates.

## Commands

```bash
# Connect to server
ssh administrator@192.168.10.215

# Verify Ubuntu version
lsb_release -a

# Update package lists
sudo apt update

# Upgrade all packages
sudo apt upgrade -y

# Apply security updates
sudo apt dist-upgrade -y

# Remove unnecessary packages
sudo apt autoremove -y

# Set hostname
sudo hostnamectl set-hostname hx-n8n-server.hx.dev.local

# Verify
hostname -f
```

## Success Criteria
- [ ] Ubuntu 22.04 or 24.04 LTS installed
- [ ] All system updates applied
- [ ] Hostname set to hx-n8n-server.hx.dev.local
- [ ] Minimum 20GB free disk space
- [ ] Minimum 2GB RAM

## Validation
```bash
lsb_release -a
df -h /
free -h
hostname -f
```

---
**Source**: phase3-execution-plan.md:236-263, agent-william-planning-analysis.md:352-381
