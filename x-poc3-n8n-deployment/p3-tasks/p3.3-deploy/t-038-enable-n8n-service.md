# Task: Enable n8n Service

**Task ID**: T-038
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 1 minute |
| **Dependencies** | T-037 |

## Task Overview

Enable n8n service to start automatically on system boot using systemctl enable.

## Success Criteria
- [ ] Service enabled successfully
- [ ] Symlink created in /etc/systemd/system/multi-user.target.wants/
- [ ] Service will start on next boot
- [ ] No errors during enable

## Execution Steps

### Step 1: Enable Service
```bash
echo "=== Enabling n8n Service for Boot ==="
sudo systemctl enable n8n.service
echo "✅ Service enabled"
```

### Step 2: Verify Enabled
```bash
systemctl is-enabled n8n.service
# Expected output: "enabled" (literal string, no additional text)
# Note: Output is ONLY the word "enabled" - no "Service is" prefix or status details
# Any other output (disabled, masked, static) means service not properly enabled
```

### Step 3: Check Symlink Created
```bash
ls -l /etc/systemd/system/multi-user.target.wants/n8n.service
# Expected: symlink to /etc/systemd/system/n8n.service
```

## Validation
```bash
systemctl is-enabled n8n.service | grep -q "enabled" && \
echo "✅ Service will start on boot" || \
echo "❌ Service not enabled"
```

## Task Metadata
```yaml
task_id: T-038
source: agent-omar-planning-analysis.md:576 (T5.2)
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for service enablement | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Clarified expected output format for `systemctl is-enabled` in Step 2 (lines 39-41). Changed comment from generic "Expected output: enabled" to explicit "Expected output: 'enabled' (literal string, no additional text)" with note that output is ONLY the word "enabled" without any prefix like "Service is" or additional status details. Added clarification that any other output (disabled, masked, static) indicates improper enablement. This helps executor distinguish between literal command output vs. descriptive status message. | Claude Code |
