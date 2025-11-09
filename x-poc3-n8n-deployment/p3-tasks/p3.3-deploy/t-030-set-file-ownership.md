# Task: Set File Ownership

**Task ID**: T-030
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
| **Dependencies** | T-029 |
| **Estimated Duration** | 5 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | No (can re-apply) |

---

## Task Overview

### Objective
Set ownership of all deployed n8n files and directories to the n8n system user (n8n:n8n) to ensure the service can read and execute application code.

### Context
After deploying artifacts and node_modules, files are owned by root or the build user. The n8n systemd service runs as the 'n8n' user, so all application files must be readable and executable by this user. This task recursively sets ownership on the entire /opt/n8n/ directory tree.

### Success Criteria
- [ ] All files in /opt/n8n/app/ owned by n8n:n8n
- [ ] All files in /opt/n8n/.n8n/ owned by n8n:n8n  
- [ ] Log directory /var/log/n8n/ owned by n8n:n8n
- [ ] No permission denied errors when testing as n8n user
- [ ] Ownership verified with stat commands

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server
- [ ] Sudo privileges (required for chown)

### Required Resources
- [ ] n8n system user exists (from T-008)
- [ ] Deployment files present (T-028, T-029)

### Required Knowledge
- [ ] Linux file ownership (chown command)
- [ ] Understanding of user:group syntax

### Blocking Dependencies
- [ ] T-029 - Deploy node_modules (all files deployed)

---

## Detailed Execution Steps

### Step 1: Verify n8n User Exists

**Command/Action**:
```bash
echo "=== Verifying n8n User ==="

if id n8n >/dev/null 2>&1; then
  echo "✅ n8n user exists"
  echo "UID: $(id -u n8n)"
  echo "GID: $(id -g n8n)"
else
  echo "❌ n8n user does NOT exist"
  echo "⚠️  Run T-008 first or escalate to @agent-william"
  exit 1
fi
```

**Expected Output**:
```
✅ n8n user exists
UID: 1001
GID: 1001
```

**Validation**:
```bash
id n8n && echo "✅ User ready" || echo "❌ User missing"
```

**If This Fails**:
- Escalate to @agent-william - T-008 must complete first

---

### Step 2: Set Ownership on Application Directory

**Command/Action**:
```bash
echo "=== Setting Ownership on /opt/n8n/app/ ==="

# Set ownership recursively
sudo chown -R n8n:n8n /opt/n8n/app/

# Verify
owner=$(stat -c '%U:%G' /opt/n8n/app/)
echo "Current owner: $owner"

if [ "$owner" = "n8n:n8n" ]; then
  echo "✅ Ownership set on /opt/n8n/app/"
else
  echo "❌ Ownership incorrect: $owner"
  exit 1
fi
```

**Expected Output**:
```
=== Setting Ownership on /opt/n8n/app/ ===
Files to update: 10000+
Current owner: n8n:n8n
✅ Ownership set on /opt/n8n/app/
```

**Validation**:
```bash
test "$(stat -c '%U' /opt/n8n/app/)" = "n8n" && \
echo "✅ Correct owner" || echo "❌ Wrong owner"
```

**If This Fails**:
- Permission denied: Must use sudo
- Wrong owner: Re-run chown command
- n8n user doesn't exist: Fix T-008 first

---

### Step 3: Set Ownership on Data Directory

**Command/Action**:
```bash
echo "=== Setting Ownership on /opt/n8n/.n8n/ ==="

sudo chown -R n8n:n8n /opt/n8n/.n8n/

owner=$(stat -c '%U:%G' /opt/n8n/.n8n/)
echo "Current owner: $owner"

if [ "$owner" = "n8n:n8n" ]; then
  echo "✅ Ownership set on /opt/n8n/.n8n/"
else
  echo "❌ Ownership incorrect"
  exit 1
fi
```

**Expected Output**:
```
✅ Ownership set on /opt/n8n/.n8n/
```

**Validation**:
```bash
test "$(stat -c '%U' /opt/n8n/.n8n/)" = "n8n" && echo "✅ OK"
```

**If This Fails**:
- Re-run chown command with sudo

---

### Step 4: Set Ownership on Log Directory

**Prerequisite Check**:
```bash
if [ ! -d /var/log/n8n ]; then
  echo "❌ /var/log/n8n does not exist (required from T-027)"
  exit 1
fi
```

**Command/Action**:
```bash
echo "=== Setting Ownership on /var/log/n8n/ ==="

sudo chown -R n8n:n8n /var/log/n8n/

owner=$(stat -c '%U:%G' /var/log/n8n/)
echo "Current owner: $owner"

if [ "$owner" = "n8n:n8n" ]; then
  echo "✅ Ownership set on /var/log/n8n/"
else
  echo "❌ Ownership incorrect"
  exit 1
fi
```

**Expected Output**:
```
✅ Ownership set on /var/log/n8n/
```

**Validation**:
```bash
test "$(stat -c '%U' /var/log/n8n/)" = "n8n" && echo "✅ OK"
```

**If This Fails**:
- Use sudo
- Verify directory exists (from T-027)

---

### Step 5: Set Ownership on Root Directory

**Command/Action**:
```bash
echo "=== Setting Ownership on /opt/n8n/ Root ==="

# Set ownership on root and all subdirectories
sudo chown -R n8n:n8n /opt/n8n/

echo "✅ Ownership set on entire /opt/n8n/ tree"
```

**Expected Output**:
```
✅ Ownership set on entire /opt/n8n/ tree
```

**Validation**:
```bash
test "$(stat -c '%U' /opt/n8n/)" = "n8n" && echo "✅ Root OK"
```

**If This Fails**:
- Use sudo and retry

---

### Step 6: Verify Ownership Comprehensively

**Command/Action**:
```bash
echo "=== Comprehensive Ownership Verification ==="

# Check all key directories
for dir in /opt/n8n /opt/n8n/app /opt/n8n/.n8n /opt/n8n/backups \
           /opt/n8n/scripts /opt/n8n/docs /var/log/n8n; do
  if [ -d "$dir" ]; then
    owner=$(stat -c '%U:%G' "$dir")
    if [ "$owner" = "n8n:n8n" ]; then
      echo "✅ $dir → $owner"
    else
      echo "❌ $dir → $owner (expected n8n:n8n)"
    fi
  fi
done

# Sample check of files in app directory
echo ""
echo "Sample file ownership:"
ls -lh /opt/n8n/app/packages/cli/bin/n8n 2>/dev/null | head -1
ls -lh /opt/n8n/app/packages/cli/dist/index.js 2>/dev/null | head -1
```

**Expected Output**:
```
=== Comprehensive Ownership Verification ===
✅ /opt/n8n → n8n:n8n
✅ /opt/n8n/app → n8n:n8n
✅ /opt/n8n/.n8n → n8n:n8n
✅ /opt/n8n/backups → n8n:n8n
✅ /opt/n8n/scripts → n8n:n8n
✅ /opt/n8n/docs → n8n:n8n
✅ /var/log/n8n → n8n:n8n

Sample file ownership:
-rwxr-xr-x 1 n8n n8n 250 Nov  7 HH:MM /opt/n8n/app/packages/cli/bin/n8n
-rw-r--r-- 1 n8n n8n 15K Nov  7 HH:MM /opt/n8n/app/packages/cli/dist/index.js
```

**Validation**:
```bash
# Verify no files owned by other users
other_owned=$(find /opt/n8n/app -not -user n8n 2>/dev/null | wc -l)

if [ "$other_owned" -eq 0 ]; then
  echo "✅ All files owned by n8n"
else
  echo "⚠️  $other_owned files not owned by n8n"
  find /opt/n8n/app -not -user n8n 2>/dev/null | head -10
fi
```

**If This Fails**:
- Files still owned by others: Re-run chown -R
- Permission denied checking: Normal for restricted directories

---

### Step 7: Test Write Access as n8n User

**Command/Action**:
```bash
echo "=== Testing Write Access as n8n User ==="

# Test write to data directory
sudo -u n8n touch /opt/n8n/.n8n/test-write.txt
if [ $? -eq 0 ]; then
  echo "✅ n8n can write to .n8n/"
  sudo -u n8n rm /opt/n8n/.n8n/test-write.txt
else
  echo "❌ n8n CANNOT write to .n8n/"
fi

# Test write to log directory
sudo -u n8n touch /var/log/n8n/test-write.log
if [ $? -eq 0 ]; then
  echo "✅ n8n can write to logs/"
  sudo -u n8n rm /var/log/n8n/test-write.log
else
  echo "❌ n8n CANNOT write to logs/"
fi

# Test read of application files
sudo -u n8n test -r /opt/n8n/app/packages/cli/bin/n8n
if [ $? -eq 0 ]; then
  echo "✅ n8n can read application files"
else
  echo "❌ n8n CANNOT read application files"
fi
```

**Expected Output**:
```
=== Testing Write Access as n8n User ===
✅ n8n can write to .n8n/
✅ n8n can write to logs/
✅ n8n can read application files
```

**Validation**:
```bash
sudo -u n8n test -r /opt/n8n/app/packages/cli/bin/n8n && \
sudo -u n8n test -w /opt/n8n/.n8n/ && \
echo "✅ Access verified" || echo "❌ Access issues"
```

**If This Fails**:
- Cannot write to .n8n/: Check permissions in T-031
- Cannot read app files: Re-run chown
- Permission denied: Verify n8n user exists

---

## Validation & Testing

### Functional Validation

**Test 1**: All directories owned by n8n
```bash
for dir in /opt/n8n/app /opt/n8n/.n8n /var/log/n8n; do
  owner=$(stat -c '%U' "$dir")
  echo "$dir: $owner"
done
```
**Expected Result**: All show 'n8n'
**Actual Result**: _[Fill in]_

---

**Test 2**: No files owned by other users
```bash
find /opt/n8n/app -not -user n8n 2>/dev/null | wc -l
```
**Expected Result**: 0 files
**Actual Result**: _[Fill in]_

---

**Test 3**: n8n user can execute CLI
```bash
sudo -u n8n test -x /opt/n8n/app/packages/cli/bin/n8n && \
echo "✅ Executable by n8n" || echo "❌ Not executable"
```
**Expected Result**: Executable
**Actual Result**: _[Fill in]_

---

## Rollback Procedure

**When to Rollback**: Generally not needed - can re-apply ownership anytime

**Pre-task Backup (optional)**: Capture current ownership before making changes
```bash
# Save current ownership state for all files
echo "=== Capturing Pre-Task Ownership State ==="
find /opt/n8n -exec stat -c '%U:%G %n' {} \; > /tmp/ownership-backup-$(date +%Y%m%d-%H%M%S).txt

echo "✅ Ownership state saved to /tmp/ownership-backup-*.txt"
echo "To restore later, parse this file and apply chown commands"
```

**Step R1**: Revert ownership if needed
```bash
# Option A: Revert to root ownership (simple)
sudo chown -R root:root /opt/n8n/app/

# Option B: Restore from backup file (preserves original owners)
# If you captured pre-task state, you can restore specific ownership:
# 1. Review backup: cat /tmp/ownership-backup-*.txt
# 2. For each file, extract owner and apply:
#    while IFS=' ' read -r owner path; do sudo chown "$owner" "$path"; done < /tmp/ownership-backup-*.txt
```

---

## Results

### Task Outcome
- **Status**: _[COMPLETED/FAILED]_
- **Duration**: _[X min]_

### Success Criteria Results

| Criterion | Met? | Evidence |
|-----------|------|----------|
| /opt/n8n/app/ owned by n8n | _[✅/❌]_ | _[stat]_ |
| /opt/n8n/.n8n/ owned by n8n | _[✅/❌]_ | _[stat]_ |
| /var/log/n8n/ owned by n8n | _[✅/❌]_ | _[stat]_ |
| No permission errors | _[✅/❌]_ | _[test]_ |
| Ownership verified | _[✅/❌]_ | _[find]_ |

---

## Documentation Updates

### Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| /opt/n8n/* (all) | Modified | Ownership changed to n8n:n8n |

---

## Knowledge Transfer

### Key Learnings
1. _[Record any ownership issues]_
2. _[Note file count]_

### Tips for Next Time
- Always verify n8n user exists first
- Use -R for recursive ownership change
- Test write access as n8n user to verify
- chown is idempotent - safe to re-run

### Related Resources
- chown man page: `man chown`
- n8n user creation: T-008 documentation

---

## Document Structure Note

**Document Length**: This task file is 480+ lines, significantly longer than the average task file (57-60 lines).

**Rationale for Length**:
- **Comprehensive Validation**: 7 detailed execution steps with extensive verification commands
- **Ownership Scope**: Multiple directories (/opt/n8n/app/, /opt/n8n/.n8n/, /var/log/n8n/) requiring separate verification
- **Access Testing**: User permission tests (write tests, read tests) to ensure operational readiness
- **Troubleshooting Guidance**: Detailed "If This Fails" sections for each step to prevent executor blockers

**Modularity Consideration**: While this file could be split into sub-tasks (e.g., "Set App Ownership", "Set Data Ownership", "Verify Access"), the ownership operation is inherently atomic (single chown -R /opt/n8n/ command). Splitting would create artificial task boundaries for what is logically a single operation with comprehensive verification. The length primarily reflects thoroughness in validation and troubleshooting guidance rather than multiple discrete operations.

**For Future Refactoring**: If template standardization requires shorter files, consider extracting verification commands into a separate "T-030-verify-ownership.md" task, keeping core ownership setting in T-030 (would reduce to ~150 lines).

---

## Task Metadata

```yaml
task_id: T-030
task_type: Deployment - Ownership
parent_work_item: POC3 n8n Deployment - Phase 3.3
assigned_agent: @agent-omar
created_date: 2025-11-07
priority: P1
estimated_duration: 5 minutes
source_documents:
  - agent-omar-planning-analysis.md:496
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

**Source**: agent-omar-planning-analysis.md:496 (T3.4)

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for file ownership configuration | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: (1) Removed non-essential file count operation (lines 104-105 deleted) - eliminates noisy output that doesn't affect ownership setting. (2) Added prerequisite check for /var/log/n8n directory (lines 175-181 added) - prevents Step 4 failure if T-027 incomplete. (3) Enhanced rollback procedure (lines 398-418) with pre-task backup option using `find ... stat` to capture ownership state and restore original owners instead of only root. (4) Added Document Structure Note (lines 468-480) explaining 480+ line length rationale (comprehensive validation, multiple directories, access testing) and modularity considerations (atomic operation, future refactoring option). | Claude Code |
