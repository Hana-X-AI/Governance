# Task: Create Systemd Service File

**Task ID**: T-034
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 20 minutes |
| **Dependencies** | T-033 |

## Task Overview

Create systemd service unit file for n8n at /etc/systemd/system/n8n.service to enable automatic startup, process management, and service control.

## Success Criteria
- [ ] Service file created at /etc/systemd/system/n8n.service
- [ ] Correct User=n8n and Group=n8n
- [ ] Environment file reference correct
- [ ] ExecStart command points to deployed n8n
- [ ] Restart policy configured
- [ ] Dependencies on postgresql.service set

## Execution Steps

### Step 1: Create Service File
```bash
sudo cat > /etc/systemd/system/n8n.service << 'SERVICEEOF'
[Unit]
Description=n8n Workflow Automation Platform - POC3
Documentation=https://docs.n8n.io
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n
EnvironmentFile=/opt/n8n/.env
ExecStart=/usr/bin/node /opt/n8n/app/packages/cli/bin/n8n start
ExecReload=/bin/kill -HUP $MAINPID
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=n8n

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/n8n/.n8n /var/log/n8n

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
SERVICEEOF

echo "✅ Service file created"
```

### Step 2: Set Permissions
```bash
sudo chmod 644 /etc/systemd/system/n8n.service
sudo chown root:root /etc/systemd/system/n8n.service
echo "✅ Permissions set"
```

### Step 3: Verify File Contents
```bash
cat /etc/systemd/system/n8n.service
```

## Validation
```bash
# Basic file checks
test -f /etc/systemd/system/n8n.service && echo "✅ Service file exists"
grep -q "User=n8n" /etc/systemd/system/n8n.service && echo "✅ User configured"
grep -q "EnvironmentFile=/opt/n8n/.env" /etc/systemd/system/n8n.service && echo "✅ Env file configured"

# Systemd syntax validation (catch configuration errors before service start)
echo "Validating systemd service file syntax..."
if sudo systemd-analyze verify /etc/systemd/system/n8n.service; then
  echo "✅ Service file syntax valid"
else
  echo "❌ Service file has syntax errors - review configuration"
  exit 1
fi
```

## Task Metadata
```yaml
task_id: T-034
source: x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:509 (T4.2)
```
