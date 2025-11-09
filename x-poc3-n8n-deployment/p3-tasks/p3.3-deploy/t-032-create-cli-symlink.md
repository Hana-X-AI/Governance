# Task: Create CLI Symlink

**Task ID**: T-032
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P2 - Optional |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-031 |

## Task Overview

Create optional symbolic link from /usr/local/bin/n8n to the n8n CLI executable to allow running 'n8n' command from any directory.

## Success Criteria
- [ ] Symlink created: /usr/local/bin/n8n → /opt/n8n/app/packages/cli/bin/n8n
- [ ] Symlink executable and functional
- [ ] Can run 'n8n --version' from any directory

## Execution Steps

### Step 1: Create Symlink
```bash
sudo ln -sf /opt/n8n/app/packages/cli/bin/n8n /usr/local/bin/n8n
echo "✅ Symlink created"
```

### Step 2: Verify Symlink
```bash
ls -l /usr/local/bin/n8n
# Expected: lrwxrwxrwx ... /usr/local/bin/n8n -> /opt/n8n/app/packages/cli/bin/n8n
```

### Step 3: Test Command
```bash
/usr/local/bin/n8n --version
# Expected: n8n version output
```

## Validation
```bash
test -L /usr/local/bin/n8n && echo "✅ Symlink exists"
test -x /usr/local/bin/n8n && echo "✅ Symlink executable"
```

## Task Metadata
```yaml
task_id: T-032
source: agent-omar-planning-analysis.md:498 (T3.6)
```
