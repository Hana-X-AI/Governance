# Task: Create Deployment Directory Structure

**Task ID**: T-027
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

---

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Execution Type** | Sequential |
| **Dependencies** | T-026 (Build verified) |
| **Estimated Duration** | 5 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | Yes |

---

## Task Overview

### Objective
Create the complete production directory structure under `/opt/n8n/` for the n8n workflow automation platform, including application, configuration, data, and log directories with proper ownership and permissions.

### Context
This is the first deployment step after build completion. We need to establish the directory hierarchy that separates the application code (`/opt/n8n/app/`) from user data (`/opt/n8n/.n8n/`), configuration (`/opt/n8n/`), and logs (`/var/log/n8n/`). This structure follows n8n best practices and enables clean separation of concerns for maintenance, backups, and upgrades.

### Success Criteria
- [ ] All required directories created under `/opt/n8n/`
- [ ] Directory ownership set to `n8n:n8n` user
- [ ] Correct permissions applied (755 for app, 700 for data)
- [ ] Log directory created at `/var/log/n8n/`
- [ ] Directory structure documented
- [ ] No permission errors when accessing directories as n8n user

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local (192.168.10.215)
- [ ] Sudo privileges on hx-n8n-server
- [ ] Access to create directories in /opt/ and /var/log/

### Required Resources
- [ ] n8n system user created by @agent-william (T-008)
- [ ] /opt/ filesystem with sufficient space (60GB+ free)
- [ ] Build artifacts ready in /opt/n8n/build/ (T-026 verified)

### Required Knowledge
- [ ] Linux directory structure and permissions
- [ ] n8n directory layout best practices
- [ ] User/group ownership management

### Blocking Dependencies
- [ ] T-008 - Create n8n system user (user n8n:n8n must exist)
- [ ] T-026 - Test build executable (build must be verified)

---

## Detailed Execution Steps

### Step 1: Verify n8n User Exists

**Command/Action**:
```bash
# Verify n8n user and group exist
id n8n 2>&1 | tee /tmp/n8n-user-check.txt

# Capture result
if id n8n >/dev/null 2>&1; then
  echo "✅ n8n user exists"
  echo "UID: $(id -u n8n)"
  echo "GID: $(id -g n8n)"
  echo "Groups: $(id -Gn n8n)"
else
  echo "❌ n8n user does NOT exist - BLOCKER"
  echo "⚠️  Run T-008 first or escalate to @agent-william"
  exit 1
fi
```

**Expected Output**:
```
✅ n8n user exists
UID: 1001
GID: 1001
Groups: n8n
```

**Validation**:
```bash
# Verify user can be used for chown
test "$(id -u n8n)" -gt 999 && \
echo "✅ Valid system user UID" || \
echo "❌ Invalid UID"

# Verify build directory exists (from T-026)
test -d /opt/n8n/build/ && \
echo "✅ Build directory present" || \
echo "❌ Build directory missing - T-026 may not have completed"
```

**If This Fails**:
- User doesn't exist: Escalate to @agent-william - T-008 must be completed first
- User exists but wrong UID/GID: Document and proceed (may need adjustment later)
- Permission denied: Ensure you have sudo access

---

### Step 2: Create Primary Application Directory

**Command/Action**:
```bash
# Create /opt/n8n/ root directory
echo "=== Creating n8n Deployment Directory Structure ==="
echo "Date: $(date)"
echo "Server: $(hostname -f)"
echo ""

# Create root directory
sudo mkdir -p /opt/n8n/
echo "✅ Created: /opt/n8n/"

# Verify creation
test -d /opt/n8n/ && \
echo "✅ Directory verified: /opt/n8n/" || \
(echo "❌ Failed to create /opt/n8n/" && exit 1)
```

**Expected Output**:
```
=== Creating n8n Deployment Directory Structure ===
Date: Thu Nov  7 HH:MM:SS CST 2025
Server: hx-n8n-server.hx.dev.local

✅ Created: /opt/n8n/
✅ Directory verified: /opt/n8n/
```

**Validation**:
```bash
# Verify directory exists and is writable
test -d /opt/n8n/ && test -w /opt/n8n/ && \
echo "✅ Root directory ready" || \
echo "❌ Root directory issues"
```

**If This Fails**:
- Permission denied: Use sudo for all mkdir commands
- /opt doesn't exist: Escalate - filesystem layout issue
- Disk full: Check space with `df -h /opt` - need 60GB+ free

---

### Step 3: Create Application Subdirectories

**Command/Action**:
```bash
# Create application directory (for n8n binaries and code)
sudo mkdir -p /opt/n8n/app/
echo "✅ Created: /opt/n8n/app/ (application binaries)"

# Create configuration directory (already exists as /opt/n8n/)
# We'll place .env here

# Create user data directory (workflows, credentials, etc.)
sudo mkdir -p /opt/n8n/.n8n/
echo "✅ Created: /opt/n8n/.n8n/ (user data and workflows)"

# Create backups directory
sudo mkdir -p /opt/n8n/backups/
echo "✅ Created: /opt/n8n/backups/ (configuration backups)"

# Create scripts directory
sudo mkdir -p /opt/n8n/scripts/
echo "✅ Created: /opt/n8n/scripts/ (utility scripts)"

# Create documentation directory
sudo mkdir -p /opt/n8n/docs/
echo "✅ Created: /opt/n8n/docs/ (deployment documentation)"

# List created directories
echo ""
echo "Directory structure:"
tree -L 2 /opt/n8n/ 2>/dev/null || ls -la /opt/n8n/
```

**Expected Output**:
```
✅ Created: /opt/n8n/app/ (application binaries)
✅ Created: /opt/n8n/.n8n/ (user data and workflows)
✅ Created: /opt/n8n/backups/ (configuration backups)
✅ Created: /opt/n8n/scripts/ (utility scripts)
✅ Created: /opt/n8n/docs/ (deployment documentation)

Directory structure:
/opt/n8n/
├── app/
├── .n8n/
├── backups/
├── scripts/
├── docs/
└── build/ (from previous steps)
```

**Validation**:
```bash
# Verify all required directories exist
for dir in app .n8n backups scripts docs; do
  test -d "/opt/n8n/$dir" && \
  echo "✅ $dir present" || \
  echo "❌ $dir MISSING"
done
```

**If This Fails**:
- Individual directory failed: Retry with explicit sudo
- Permission denied: Check sudo access
- Disk space issues: Check `df -h /opt`

---

### Step 4: Create Log Directory

**Command/Action**:
```bash
# Create log directory in standard location
sudo mkdir -p /var/log/n8n/
echo "✅ Created: /var/log/n8n/ (application logs)"

# Verify creation
test -d /var/log/n8n/ && \
echo "✅ Log directory verified" || \
(echo "❌ Failed to create log directory" && exit 1)

# Document log location
echo "/var/log/n8n/" | sudo tee /opt/n8n/docs/log-location.txt
```

**Expected Output**:
```
✅ Created: /var/log/n8n/ (application logs)
✅ Log directory verified
/var/log/n8n/
```

**Validation**:
```bash
# Verify log directory accessible
test -d /var/log/n8n/ && test -w /var/log/n8n/ && \
echo "✅ Log directory ready" || \
echo "❌ Log directory issues"
```

**If This Fails**:
- Permission denied on /var/log: Use sudo
- /var/log doesn't exist: Critical system issue - escalate to @agent-william
- Cannot write: Will be fixed in permission step

---

### Step 5: Set Directory Ownership

**Command/Action**:
```bash
# Set ownership of entire /opt/n8n/ tree to n8n user
echo "=== Setting Directory Ownership ==="

sudo chown -R n8n:n8n /opt/n8n/
echo "✅ Set ownership: /opt/n8n/ → n8n:n8n"

# Set ownership of log directory
sudo chown -R n8n:n8n /var/log/n8n/
echo "✅ Set ownership: /var/log/n8n/ → n8n:n8n"

# Verify ownership
echo ""
echo "Ownership verification:"
ls -ld /opt/n8n/
ls -ld /opt/n8n/app/
ls -ld /opt/n8n/.n8n/
ls -ld /var/log/n8n/
```

**Expected Output**:
```
=== Setting Directory Ownership ===
✅ Set ownership: /opt/n8n/ → n8n:n8n
✅ Set ownership: /var/log/n8n/ → n8n:n8n

Ownership verification:
drwxr-xr-x 8 n8n n8n 4096 Nov  7 HH:MM /opt/n8n/
drwxr-xr-x 2 n8n n8n 4096 Nov  7 HH:MM /opt/n8n/app/
drwxr-xr-x 2 n8n n8n 4096 Nov  7 HH:MM /opt/n8n/.n8n/
drwxr-xr-x 2 n8n n8n 4096 Nov  7 HH:MM /var/log/n8n/
```

**Validation**:
```bash
# Verify ownership is correct
test "$(stat -c '%U' /opt/n8n/)" = "n8n" && \
test "$(stat -c '%G' /opt/n8n/)" = "n8n" && \
echo "✅ Ownership correct" || \
echo "❌ Ownership incorrect"
```

**If This Fails**:
- chown fails: Verify n8n user exists (`id n8n`)
- Permission denied: Must use sudo
- Wrong user shown: Re-run chown command with sudo

---

### Step 6: Set Directory Permissions

**Command/Action**:
```bash
# Set permissions on directories
echo "=== Setting Directory Permissions ==="

# Application directory - readable and executable by all
sudo chmod 755 /opt/n8n/app/
echo "✅ Set permissions: /opt/n8n/app/ → 755 (rwxr-xr-x)"

# User data directory - private to n8n user only
sudo chmod 700 /opt/n8n/.n8n/
echo "✅ Set permissions: /opt/n8n/.n8n/ → 700 (rwx------)"

# Backups directory - private
sudo chmod 700 /opt/n8n/backups/
echo "✅ Set permissions: /opt/n8n/backups/ → 700 (rwx------)"

# Scripts directory - readable and executable
sudo chmod 755 /opt/n8n/scripts/
echo "✅ Set permissions: /opt/n8n/scripts/ → 755 (rwxr-xr-x)"

# Documentation - readable by all
sudo chmod 755 /opt/n8n/docs/
echo "✅ Set permissions: /opt/n8n/docs/ → 755 (rwxr-xr-x)"

# Log directory - writable by n8n only
sudo chmod 755 /var/log/n8n/
echo "✅ Set permissions: /var/log/n8n/ → 755 (rwxr-xr-x)"

# Root directory
sudo chmod 755 /opt/n8n/
echo "✅ Set permissions: /opt/n8n/ → 755 (rwxr-xr-x)"

# Verify all permissions
echo ""
echo "Permission verification:"
ls -ld /opt/n8n/app/ /opt/n8n/.n8n/ /opt/n8n/backups/ /var/log/n8n/
```

**Expected Output**:
```
=== Setting Directory Permissions ===
✅ Set permissions: /opt/n8n/app/ → 755 (rwxr-xr-x)
✅ Set permissions: /opt/n8n/.n8n/ → 700 (rwx------)
✅ Set permissions: /opt/n8n/backups/ → 700 (rwx------)
✅ Set permissions: /opt/n8n/scripts/ → 755 (rwxr-xr-x)
✅ Set permissions: /opt/n8n/docs/ → 755 (rwxr-xr-x)
✅ Set permissions: /var/log/n8n/ → 755 (rwxr-xr-x)
✅ Set permissions: /opt/n8n/ → 755 (rwxr-xr-x)

Permission verification:
drwxr-xr-x 2 n8n n8n 4096 Nov  7 HH:MM /opt/n8n/app/
drwx------ 2 n8n n8n 4096 Nov  7 HH:MM /opt/n8n/.n8n/
drwx------ 2 n8n n8n 4096 Nov  7 HH:MM /opt/n8n/backups/
drwxr-xr-x 2 n8n n8n 4096 Nov  7 HH:MM /var/log/n8n/
```

**Validation**:
```bash
# Verify specific permissions
test "$(stat -c '%a' /opt/n8n/app/)" = "755" && echo "✅ app/ correct" || echo "❌ app/ wrong"
test "$(stat -c '%a' /opt/n8n/.n8n/)" = "700" && echo "✅ .n8n/ correct" || echo "❌ .n8n/ wrong"
test "$(stat -c '%a' /opt/n8n/backups/)" = "700" && echo "✅ backups/ correct" || echo "❌ backups/ wrong"
```

**If This Fails**:
- chmod fails: Must use sudo
- Wrong permissions shown: Re-run specific chmod command
- Permission denied when testing: Normal if testing as non-n8n user for 700 directories

---

### Step 7: Document Directory Structure

**Command/Action**:
```bash
# Create comprehensive directory structure documentation
# Note: Using EOF (no quotes) allows variable expansion
cat > /tmp/n8n-directory-structure.txt << EOF
==============================================
n8n Directory Structure Documentation
Server: hx-n8n-server.hx.dev.local (192.168.10.215)
Created: $(date)
Owner: n8n:n8n (UID:$(id -u n8n) GID:$(id -g n8n))
==============================================

PRIMARY DIRECTORIES:
====================

/opt/n8n/
├── Purpose: Root directory for n8n deployment
├── Owner: n8n:n8n
├── Permissions: 755 (rwxr-xr-x)
└── Contents:
    ├── app/ - Application binaries and compiled code
    ├── .n8n/ - User data (workflows, credentials, executions)
    ├── backups/ - Configuration and data backups
    ├── scripts/ - Utility and maintenance scripts
    ├── docs/ - Deployment documentation
    ├── build/ - Build artifacts (can be removed post-deployment)
    └── .env - Environment configuration (to be created in T-028)

/opt/n8n/app/
├── Purpose: n8n application code and binaries
├── Owner: n8n:n8n
├── Permissions: 755 (rwxr-xr-x) - readable by all, writable by n8n
├── Contents: Will contain:
│   ├── packages/cli/dist/ - Compiled CLI code
│   ├── packages/core/dist/ - Core workflow engine
│   ├── packages/nodes-base/dist/ - Node implementations
│   ├── node_modules/ - Runtime dependencies
│   └── bin/n8n - CLI executable

/opt/n8n/.n8n/
├── Purpose: User data directory (workflows, credentials, execution logs)
├── Owner: n8n:n8n
├── Permissions: 700 (rwx------) - PRIVATE to n8n user only
├── Security: Contains sensitive data - encrypted credentials
├── Contents: Will be auto-created by n8n on first run:
│   ├── workflows/ - Workflow JSON definitions
│   ├── nodes/ - Custom node code
│   └── .encryption-key - Credential encryption key (auto-generated)

/opt/n8n/backups/
├── Purpose: Configuration and data backups
├── Owner: n8n:n8n
├── Permissions: 700 (rwx------) - PRIVATE
├── Backup Strategy: Daily backups of .env, workflows, credentials
└── Retention: 30 days

/opt/n8n/scripts/
├── Purpose: Utility scripts for maintenance
├── Owner: n8n:n8n
├── Permissions: 755 (rwxr-xr-x)
└── Contents: Backup scripts, health checks, utilities

/opt/n8n/docs/
├── Purpose: Deployment and operational documentation
├── Owner: n8n:n8n
├── Permissions: 755 (rwxr-xr-x)
└── Contents: Task logs, configuration notes, troubleshooting guides

/var/log/n8n/
├── Purpose: Application logs
├── Owner: n8n:n8n
├── Permissions: 755 (rwxr-xr-x)
├── Log Files:
│   ├── n8n.log - Main application log (from N8N_LOG_FILE_LOCATION)
│   ├── error.log - Error-level logs
│   └── access.log - HTTP access logs
├── Rotation: logrotate configured for 30-day retention
└── Size Limit: 100MB per file before rotation

SECURITY NOTES:
===============
- /opt/n8n/.n8n/ is 700 - contains encrypted credentials
- /opt/n8n/backups/ is 700 - contains backup of sensitive configs
- /opt/n8n/.env will be 600 - contains database passwords (T-028)
- All other directories are 755 - readable but not writable by others

DISK USAGE ESTIMATES:
=====================
- /opt/n8n/app/ - ~500MB (application code)
- /opt/n8n/.n8n/ - Grows with workflows/executions (estimate 1-5GB)
- /opt/n8n/backups/ - ~100MB per backup (grows with retention)
- /var/log/n8n/ - ~100MB (with rotation)
- Total estimated: 2-7GB initially, grows with usage

NEXT STEPS:
===========
T-028: Deploy compiled artifacts to /opt/n8n/app/
T-029: Create .env configuration file
T-030: Set file ownership and permissions on deployed artifacts

==============================================
EOF

# Copy to docs directory (variables already expanded in heredoc)
sudo cp /tmp/n8n-directory-structure.txt /opt/n8n/docs/directory-structure.txt
sudo chown n8n:n8n /opt/n8n/docs/directory-structure.txt
sudo chmod 644 /opt/n8n/docs/directory-structure.txt

# Display documentation
echo ""
cat /opt/n8n/docs/directory-structure.txt
```

**Expected Output**:
```
[Complete directory structure documentation]
```

**Validation**:
```bash
# Verify documentation created
test -f /opt/n8n/docs/directory-structure.txt && \
echo "✅ Documentation created" || \
echo "❌ Documentation missing"
```

**If This Fails**:
- Save to /tmp for manual copy later
- Non-critical - proceed with deployment

---

## Validation & Testing

### Functional Validation

**Test 1**: All directories exist
```bash
# Verify complete directory tree
for dir in /opt/n8n/app /opt/n8n/.n8n /opt/n8n/backups \
           /opt/n8n/scripts /opt/n8n/docs /var/log/n8n; do
  test -d "$dir" && echo "✅ $dir exists" || echo "❌ $dir MISSING"
done
```
**Expected Result**: All directories exist
**Actual Result**: _[Fill in during execution]_

---

**Test 2**: Ownership correct
```bash
# Verify n8n user owns all directories
for dir in /opt/n8n /opt/n8n/app /opt/n8n/.n8n /var/log/n8n; do
  owner=$(stat -c '%U:%G' "$dir")
  if [ "$owner" = "n8n:n8n" ]; then
    echo "✅ $dir owned by n8n:n8n"
  else
    echo "❌ $dir owned by $owner (expected n8n:n8n)"
  fi
done
```
**Expected Result**: All directories owned by n8n:n8n
**Actual Result**: _[Fill in during execution]_

---

**Test 3**: Permissions correct
```bash
# Verify security-sensitive permissions
test "$(stat -c '%a' /opt/n8n/.n8n/)" = "700" && \
echo "✅ .n8n/ is private (700)" || \
echo "❌ .n8n/ permissions wrong"

test "$(stat -c '%a' /opt/n8n/backups/)" = "700" && \
echo "✅ backups/ is private (700)" || \
echo "❌ backups/ permissions wrong"

test "$(stat -c '%a' /opt/n8n/app/)" = "755" && \
echo "✅ app/ is public readable (755)" || \
echo "❌ app/ permissions wrong"
```
**Expected Result**: All permissions match requirements
**Actual Result**: _[Fill in during execution]_

---

**Test 4**: n8n user can write to required directories
```bash
# Test write access as n8n user
sudo -u n8n touch /opt/n8n/.n8n/test-write.txt && \
sudo -u n8n rm /opt/n8n/.n8n/test-write.txt && \
echo "✅ n8n user can write to .n8n/" || \
echo "❌ n8n user CANNOT write to .n8n/"

sudo -u n8n touch /var/log/n8n/test-write.log && \
sudo -u n8n rm /var/log/n8n/test-write.log && \
echo "✅ n8n user can write to logs/" || \
echo "❌ n8n user CANNOT write to logs/"
```
**Expected Result**: Write tests succeed
**Actual Result**: _[Fill in during execution]_

---

### Integration Validation

**Test 1**: Disk space sufficient
```bash
# Verify adequate free space
available=$(df -BG /opt | tail -1 | awk '{print $4}' | sed 's/G//')
if [ "$available" -ge 60 ]; then
  echo "✅ Sufficient disk space: ${available}GB available"
else
  echo "⚠️  Low disk space: ${available}GB available (60GB+ recommended)"
fi
```
**Expected Result**: 60GB+ free space on /opt
**Actual Result**: _[Fill in during execution]_

---

**Test 2**: Documentation accessible
```bash
# Verify documentation readable
test -r /opt/n8n/docs/directory-structure.txt && \
cat /opt/n8n/docs/directory-structure.txt | head -20 && \
echo "✅ Documentation accessible" || \
echo "❌ Documentation not accessible"
```
**Expected Result**: Documentation file readable
**Actual Result**: _[Fill in during execution]_

---

## Rollback Procedure

**When to Rollback**: If directories cannot be created with correct permissions, or if disk space insufficient

### Rollback Steps

**Step R1**: Remove created directories
```bash
# Remove deployment directories (DESTRUCTIVE)
sudo rm -rf /opt/n8n/app/
sudo rm -rf /opt/n8n/.n8n/
sudo rm -rf /opt/n8n/backups/
sudo rm -rf /opt/n8n/scripts/
sudo rm -rf /opt/n8n/docs/
sudo rm -rf /var/log/n8n/

# Keep /opt/n8n/build/ and /opt/n8n/logs/ - from previous phases
```
**Validation**: Directories removed, build artifacts intact

**Step R2**: Verify build directory preserved
```bash
test -d /opt/n8n/build/ && \
echo "✅ Build directory preserved" || \
echo "❌ Build directory lost - CRITICAL"
```

**Step R3**: Document rollback reason
```bash
echo "Directory structure rollback at $(date): [REASON]" | \
sudo tee -a /opt/n8n/logs/deployment-failures.log
```

---

## Results

### Task Outcome
- **Status**: _[COMPLETED | FAILED | PARTIALLY COMPLETED]_
- **Start Time**: _[HH:MM]_
- **End Time**: _[HH:MM]_
- **Duration**: _[X minutes]_
- **Rollback Needed**: _[Yes/No]_

### Success Criteria Results

| Criterion | Met? | Evidence |
|-----------|------|----------|
| All directories created | _[✅/❌]_ | _[ls output]_ |
| Ownership n8n:n8n | _[✅/❌]_ | _[stat output]_ |
| Permissions correct | _[✅/❌]_ | _[chmod verification]_ |
| Log directory created | _[✅/❌]_ | _[/var/log/n8n/ exists]_ |
| Documentation created | _[✅/❌]_ | _[docs/directory-structure.txt]_ |
| n8n user can write | _[✅/❌]_ | _[write tests passed]_ |

---

## Documentation Updates

### Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| /opt/n8n/app/ | Created | Application directory |
| /opt/n8n/.n8n/ | Created | User data directory |
| /opt/n8n/backups/ | Created | Backup directory |
| /opt/n8n/scripts/ | Created | Scripts directory |
| /opt/n8n/docs/ | Created | Documentation directory |
| /var/log/n8n/ | Created | Log directory |
| /opt/n8n/docs/directory-structure.txt | Created | Structure documentation |

---

## Knowledge Transfer

### Key Learnings
1. _[Record any permission issues encountered]_
2. _[Note if n8n user had issues]_
3. _[Document disk space status]_

### Tips for Next Time
- Verify n8n user exists before starting (T-008 must be complete)
- Check disk space first - need 60GB+ free
- .n8n/ and backups/ directories must be 700 for security
- Log directory can be 755 since logs are non-sensitive
- Keep build directory separate from deployment for clean rollback

### Related Resources
- Directory structure documentation: `/opt/n8n/docs/directory-structure.txt`
- n8n installation guide: `/srv/knowledge/vault/n8n-master/docker/compose/README.md`
- Linux permissions guide: `man chmod`

---

## Coordination & Communication

### Notifications Sent

| Time | Recipient | Message |
|------|-----------|---------|
| _[HH:MM]_ | @agent-william | Directory structure created, ready for artifact deployment |

---

## Task Metadata

```yaml
task_id: T-027
task_type: Deployment - Directory Setup
parent_work_item: POC3 n8n Deployment - Phase 3.3 Deployment
assigned_agent: @agent-omar
created_date: 2025-11-07
completed_date: [YYYY-MM-DD]
status: NOT STARTED
priority: P1 - Critical
execution_type: Sequential
estimated_duration: 5 minutes
actual_duration: [X minutes]
systems_affected: [hx-n8n-server.hx.dev.local (192.168.10.215)]
rollback_performed: [yes/no]
source_documents:
  - /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:493
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for deployment directory structure setup | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: (1) Added explicit build directory verification to Step 1 prerequisites (lines 103-106) to prevent silent failures when /opt/n8n/build/ is missing from incomplete T-026 execution. (2) Simplified documentation generation (lines 399-500) by removing fragile eval-based variable substitution; changed heredoc delimiter from `<< 'EOF'` to `<< EOF` to allow natural command substitution expansion, eliminating 5 lines of complex eval code that could fail silently. | Claude Code |

---

**Source**: agent-omar-planning-analysis.md:493 (T3.1)
