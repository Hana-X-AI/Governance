# Task: Set File Permissions

**Task ID**: T-031
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-030 |

## Task Overview

Set appropriate file permissions on n8n deployment directories: 755 for app/, 700 for .n8n/ and backups/, ensuring security while allowing n8n service execution.

## Success Criteria
- [ ] /opt/n8n/app/ set to 755 (rwxr-xr-x)
- [ ] /opt/n8n/.n8n/ set to 700 (rwx------)
- [ ] /opt/n8n/backups/ set to 700
- [ ] CLI executable has execute bit set
- [ ] Permissions verified with stat commands

## Execution Steps

### Step 1: Set Application Directory Permissions
```bash
# Set directory itself to 755 (rwxr-xr-x)
sudo chmod 755 /opt/n8n/app/

# Recursively set permissions for all contents:
# - u+rX,go+rX means: owner read+execute(dirs only), group/others read+execute(dirs only)
# - Capital 'X' only adds execute to directories, NOT regular files
# - This ensures .js/.json files remain 644 (rw-r--r--), directories become 755 (rwxr-xr-x)
sudo chmod -R u+rX,go+rX /opt/n8n/app/

echo "✅ Application directory: 755 (files readable, dirs executable)"
```

**Why Two Commands?**
- **Line 32**: Sets /opt/n8n/app/ directory itself to 755
- **Line 33**: Recursively sets contents (subdirectories and files) with smart execute handling
- **Capital X**: Only adds execute (+x) to directories, preserving file execute bits (n8n CLI keeps +x, .js files remain -x)

### Step 2: Set Data Directory Permissions (Private)
```bash
sudo chmod 700 /opt/n8n/.n8n/
sudo chmod 700 /opt/n8n/backups/
echo "✅ Private directories: 700"
```

### Step 3: Ensure CLI Executable
```bash
sudo chmod +x /opt/n8n/app/packages/cli/bin/n8n
test -x /opt/n8n/app/packages/cli/bin/n8n && echo "✅ CLI executable"
```

### Step 4: Verify Permissions
```bash
stat -c '%a %n' /opt/n8n/app/ /opt/n8n/.n8n/ /opt/n8n/backups/
# Expected: 755, 700, 700
```

## Validation
```bash
test "$(stat -c '%a' /opt/n8n/app/)" = "755" && echo "✅ app/ correct"
test "$(stat -c '%a' /opt/n8n/.n8n/)" = "700" && echo "✅ .n8n/ correct"
```

## Task Metadata
```yaml
task_id: T-031
source: agent-omar-planning-analysis.md:497 (T3.5)
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for file permissions configuration | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Clarified recursive chmod intent in Step 1 (lines 32-47). Added detailed inline comments explaining why two chmod commands are needed: (1) Line 33 sets directory itself to 755, (2) Line 39 recursively sets contents with capital 'X' flag (only adds execute to directories, NOT files). Added "Why Two Commands?" explanation documenting that capital X preserves file execute bits (n8n CLI keeps +x, .js files remain -x without execute). This prevents executor confusion about why both commands are necessary and clarifies the smart execute handling behavior. | Claude Code |
