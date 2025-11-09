# Task: Create Systemd Service Template

**Task ID**: T-015
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Parallel
**Dependencies**: T-011
**Estimated Duration**: 10 minutes

---

## Objective
Create base systemd unit file for n8n.service.

## Commands

```bash
sudo tee /etc/systemd/system/n8n.service <<'EOF'
[Unit]
Description=n8n Workflow Automation Platform
Documentation=https://docs.n8n.io
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=n8n
Group=n8n
# WorkingDirectory: Set to /opt/n8n (root) rather than /opt/n8n/app
# Rationale: n8n uses N8N_USER_FOLDER env var (from EnvironmentFile) to determine data paths
# The working directory doesn't need to match the executable location
# Setting to /opt/n8n allows relative paths in logs to reference .n8n/, app/, backups/
WorkingDirectory=/opt/n8n
EnvironmentFile=/opt/n8n/.env
ExecStart=/usr/bin/node /opt/n8n/app/packages/cli/bin/n8n start
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
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
EOF

# Reload systemd
sudo systemctl daemon-reload

# Verify service file syntax
sudo systemd-analyze verify n8n.service
```

## Success Criteria
- [ ] Service file created
- [ ] Systemd reloaded
- [ ] No syntax errors

## Validation
```bash
systemctl status n8n.service
sudo systemd-analyze verify n8n.service
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for systemd service template | @agent-william |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Added WorkingDirectory rationale (lines 30-33). Clarified why WorkingDirectory=/opt/n8n instead of /opt/n8n/app despite executable being at /opt/n8n/app/packages/cli/bin/n8n. Documented that n8n uses N8N_USER_FOLDER env var (from EnvironmentFile) to determine data paths, so working directory doesn't need to match executable location. Setting to /opt/n8n allows relative paths in logs to reference .n8n/, app/, backups/ subdirectories. This is intentional design aligned with n8n's configuration expectations. | Claude Code |

---
**Source**: phase3-execution-plan.md:746-791, agent-william-planning-analysis.md:647-699
