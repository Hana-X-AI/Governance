# Task: Configure System Performance Tuning

**Task ID**: T-014
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P2 - High
**Execution Type**: Parallel
**Dependencies**: T-012
**Estimated Duration**: 10 minutes

---

## Objective
Apply sysctl and ulimit tuning for Node.js performance.

## Commands

```bash
# Create sysctl configuration
sudo tee /etc/sysctl.d/99-n8n.conf <<'EOF'
# N8N Performance Tuning
fs.file-max = 2097152
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 600
vm.swappiness = 10
EOF

# Apply sysctl settings
sudo sysctl -p /etc/sysctl.d/99-n8n.conf

# Create user limits configuration
sudo tee /etc/security/limits.d/n8n.conf <<'EOF'
n8n soft nofile 65536
n8n hard nofile 65536
n8n soft nproc 4096
n8n hard nproc 4096
EOF

# Verify
sudo sysctl fs.file-max
sudo sysctl net.core.somaxconn
```

## Success Criteria
- [ ] All tuning parameters applied
- [ ] sysctl settings verified
- [ ] User limits configured

## Validation
```bash
sudo sysctl fs.file-max
cat /etc/security/limits.d/n8n.conf
```

---
**Source**: agent-william-planning-analysis.md:606-645
