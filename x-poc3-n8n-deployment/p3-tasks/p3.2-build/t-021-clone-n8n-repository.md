# Task: Clone n8n Repository

**Task ID**: T-021
**Parent Work Item**: POC3 n8n Deployment - Phase 3.2 Build
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

---

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Execution Type** | Sequential |
| **Dependencies** | T-020 |
| **Estimated Duration** | 10 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | Yes |

---

## Task Overview

### Objective
Clone n8n-master repository (v1.117.0) from local source at `/srv/knowledge/vault/n8n-master/` to build location `/opt/n8n/build/` on hx-n8n-server.

### Context
The n8n source code is pre-staged in the knowledge vault at `/srv/knowledge/vault/n8n-master/` (v1.117.0). This task copies the repository to the build location where the compilation will occur. Using a local copy instead of git clone from GitHub ensures consistent source version and faster setup.

### Success Criteria
- [ ] Build directory `/opt/n8n/build/` created
- [ ] n8n source code copied to `/opt/n8n/build/`
- [ ] Repository structure verified (packages/, package.json, etc.)
- [ ] Source code owned by n8n:n8n
- [ ] Repository version confirmed as 1.117.0

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local (192.168.10.215)
- [ ] Sudo privileges on hx-n8n-server
- [ ] Read access to `/srv/knowledge/vault/n8n-master/`

### Required Resources
- [ ] n8n source repository at `/srv/knowledge/vault/n8n-master/` (v1.117.0)
- [ ] Sufficient disk space on hx-n8n-server (≥20GB free)
- [ ] n8n system user created (from T-011)

### Required Knowledge
- [ ] Linux file operations (cp, rsync)
- [ ] File permissions and ownership
- [ ] n8n repository structure

### Blocking Dependencies
- [ ] T-020 - Verify Build Prerequisites (all prerequisites must pass)

---

## Detailed Execution Steps

### Step 1: Create Build Directory

**Command/Action**:
```bash
# Create build directory
sudo mkdir -p /opt/n8n/build

# Set ownership to n8n user
sudo chown n8n:n8n /opt/n8n/build

# Verify directory created
ls -ld /opt/n8n/build
```

**Expected Output**:
```
drwxr-xr-x 2 n8n n8n 4096 Nov  7 HH:MM /opt/n8n/build
```

**Validation**:
```bash
# Verify directory exists and has correct ownership
test -d /opt/n8n/build && \
stat -c '%U:%G' /opt/n8n/build | grep -q 'n8n:n8n' && \
echo "✅ Build directory ready" || \
echo "❌ Build directory issues"
```

**If This Fails**:
- Check if /opt/n8n exists: `ls -ld /opt/n8n`
- Verify n8n user exists: `id n8n`
- Create parent directory if needed: `sudo mkdir -p /opt/n8n`
- Re-run ownership command: `sudo chown n8n:n8n /opt/n8n/build`

---

### Step 2: Verify Source Repository Exists

**Command/Action**:
```bash
# Verify source repository exists
ls -la /srv/knowledge/vault/n8n-master/

# Check for key repository files
ls -1 /srv/knowledge/vault/n8n-master/ | grep -E 'package.json|packages|pnpm-workspace.yaml'
```

**Expected Output**:
```
package.json
packages
pnpm-workspace.yaml
```

**Validation**:
```bash
# Verify repository has required structure
test -f /srv/knowledge/vault/n8n-master/package.json && \
test -d /srv/knowledge/vault/n8n-master/packages && \
test -f /srv/knowledge/vault/n8n-master/pnpm-workspace.yaml && \
echo "✅ Source repository structure valid" || \
echo "❌ Source repository incomplete"
```

**If This Fails**:
- Verify mount point: `mount | grep /srv/knowledge`
- Check file permissions: `ls -la /srv/knowledge/vault/`
- Verify n8n-master directory exists: `ls -la /srv/knowledge/vault/ | grep n8n`
- Escalate to @agent-zero if source repository missing or corrupted

---

### Step 3: Copy Repository to Build Location

**Command/Action**:
```bash
# Copy repository with automatic tool detection
# Prefers rsync for progress reporting and efficiency, falls back to cp if unavailable
if command -v rsync &> /dev/null; then
  echo "Using rsync for repository copy (with progress reporting)..."
  sudo rsync -av --progress \
    /srv/knowledge/vault/n8n-master/ \
    /opt/n8n/build/ \
    2>&1 | tee /tmp/n8n-repo-copy.log
else
  echo "rsync not available, using cp for repository copy..."
  sudo cp -r /srv/knowledge/vault/n8n-master/* /opt/n8n/build/
  echo "✅ Copy completed (no progress reporting available with cp)"
fi
```

**Expected Output**:

**If using rsync** (preferred):
```
Using rsync for repository copy (with progress reporting)...
sending incremental file list
./
package.json
pnpm-workspace.yaml
packages/
packages/cli/
[... many more files ...]

sent XXX bytes  received XXX bytes  XXX bytes/sec
total size is XXX  speedup is XXX
```

**If using cp** (fallback):
```
rsync not available, using cp for repository copy...
✅ Copy completed (no progress reporting available with cp)
```

**Note**: Automatic tool detection eliminates manual decision-making during execution. Rsync is preferred for:
- Progress reporting (visual feedback for long copy operations)
- Incremental copy support (only copies changed files on re-runs)
- Preserve file attributes and timestamps
- Better error handling

Fallback to cp ensures task completion even on minimal systems without rsync installed.

**Validation**:
```bash
# Verify copy completed (same validation regardless of copy method used)
test -f /opt/n8n/build/package.json && \
test -d /opt/n8n/build/packages && \
echo "✅ Repository copied successfully" || \
echo "❌ Repository copy incomplete"

# Count packages directory
ls -1 /opt/n8n/build/packages/ | wc -l
# Should show 30+ directories
```

**If This Fails**:
- Check disk space: `df -h /opt`
- Check for error messages in `/tmp/n8n-repo-copy.log`
- Verify source repository integrity: `ls -laR /srv/knowledge/vault/n8n-master/ | wc -l`
- Remove partial copy and retry: `sudo rm -rf /opt/n8n/build/* && [re-run rsync]`
- Use cp as alternative if rsync fails

---

### Step 4: Set Correct Ownership

**Command/Action**:
```bash
# Set ownership to n8n user recursively
sudo chown -R n8n:n8n /opt/n8n/build/

# Verify ownership
ls -la /opt/n8n/build/ | head -20
```

**Expected Output**:
```
total XXX
drwxr-xr-x  X n8n n8n  4096 Nov  7 HH:MM .
drwxr-xr-x  X n8n n8n  4096 Nov  7 HH:MM ..
-rw-r--r--  1 n8n n8n  XXXX Nov  7 HH:MM package.json
drwxr-xr-x  X n8n n8n  4096 Nov  7 HH:MM packages
-rw-r--r--  1 n8n n8n  XXXX Nov  7 HH:MM pnpm-workspace.yaml
```

**Validation**:
```bash
# Verify all files owned by n8n
find /opt/n8n/build -not -user n8n -o -not -group n8n | wc -l
# Expected: 0 (no files with incorrect ownership)
```

**If This Fails**:
- Re-run chown command with verbose: `sudo chown -Rv n8n:n8n /opt/n8n/build/`
- Check for immutable files: `lsattr /opt/n8n/build/`
- Escalate if ownership cannot be changed

---

### Step 5: Verify Repository Version

**Command/Action**:
```bash
# Check package.json for version
grep '"version"' /opt/n8n/build/package.json | head -1

# Check CLI package version
grep '"version"' /opt/n8n/build/packages/cli/package.json | head -1
```

**Expected Output**:
```
  "version": "1.117.0",
  "version": "1.117.0",
```

**Validation**:
```bash
# Verify version is 1.117.0
grep -q '"version": "1.117.0"' /opt/n8n/build/package.json && \
echo "✅ Repository version confirmed: 1.117.0" || \
echo "❌ Version mismatch or not found"
```

**If This Fails**:
- Check actual version in package.json: `cat /opt/n8n/build/package.json | grep version`
- Verify source repository version: `grep version /srv/knowledge/vault/n8n-master/package.json`
- Document version discrepancy and escalate to @agent-zero
- Confirm if different version is acceptable for POC3

---

### Step 6: Verify Repository Structure

**Command/Action**:
```bash
# Create verification report
cat > /tmp/n8n-repo-structure.txt << 'EOF'
==============================================
n8n Repository Structure Verification
Location: /opt/n8n/build/
Date: $(date)
==============================================

Root Files:
$(ls -1 /opt/n8n/build/*.json /opt/n8n/build/*.yaml 2>/dev/null)

Packages Count:
$(ls -1d /opt/n8n/build/packages/*/ 2>/dev/null | wc -l) directories

Key Packages:
$(ls -1 /opt/n8n/build/packages/ | grep -E 'cli|core|workflow|nodes-base|editor-ui' | head -10)

Repository Size:
$(du -sh /opt/n8n/build/)

Version:
$(grep '"version"' /opt/n8n/build/package.json | head -1)

==============================================
EOF

# Execute and expand variables
bash -c "cat > /tmp/n8n-repo-structure.txt" << EOF
==============================================
n8n Repository Structure Verification
Location: /opt/n8n/build/
Date: $(date)
==============================================

Root Files:
$(ls -1 /opt/n8n/build/*.json /opt/n8n/build/*.yaml 2>/dev/null)

Packages Count:
$(ls -1d /opt/n8n/build/packages/*/ 2>/dev/null | wc -l) directories

Key Packages:
$(ls -1 /opt/n8n/build/packages/ | grep -E 'cli|core|workflow|nodes-base|editor-ui')

Repository Size:
$(du -sh /opt/n8n/build/)

Version:
$(grep '"version"' /opt/n8n/build/package.json | head -1)

==============================================
EOF

# Display report
cat /tmp/n8n-repo-structure.txt
```

**Expected Output**:
```
Repository structure report showing:
- 30+ packages
- Key packages present (cli, core, workflow, nodes-base, editor-ui)
- Version 1.117.0
- Repository size ~500MB-1GB
```

**Validation**:
```bash
# Save to documentation
sudo mkdir -p /opt/n8n/docs
sudo cp /tmp/n8n-repo-structure.txt /opt/n8n/docs/repo-structure-$(date +%Y%m%d).txt
sudo chown n8n:n8n /opt/n8n/docs/repo-structure-*.txt
```

**If This Fails**:
- Review structure manually: `tree -L 2 /opt/n8n/build/`
- Compare with source: `diff -rq /srv/knowledge/vault/n8n-master/ /opt/n8n/build/`
- Document any missing packages or files
- Escalate if critical packages missing (cli, core, workflow)

---

## Validation & Testing

### Functional Validation

**Test 1**: Repository structure complete
```bash
# Verify required directories and files exist
test -f /opt/n8n/build/package.json && \
test -f /opt/n8n/build/pnpm-workspace.yaml && \
test -d /opt/n8n/build/packages/cli && \
test -d /opt/n8n/build/packages/core && \
test -d /opt/n8n/build/packages/workflow && \
echo "✅ Repository structure valid" || \
echo "❌ Repository structure incomplete"
```
**Expected Result**: Repository structure valid
**Actual Result**: _[Fill in during execution]_

---

**Test 2**: Package count verification
```bash
# Count packages (should be 30+)
package_count=$(ls -1d /opt/n8n/build/packages/*/ 2>/dev/null | wc -l)
if [ "$package_count" -ge 30 ]; then
  echo "✅ Package count: $package_count (expected 30+)"
else
  echo "❌ Package count: $package_count (expected 30+)"
fi
```
**Expected Result**: 30+ packages found
**Actual Result**: _[Fill in during execution]_

---

### Integration Validation

**Test 1**: n8n user can read repository
```bash
# Test as n8n user
sudo -u n8n test -r /opt/n8n/build/package.json && \
echo "✅ n8n user can read repository" || \
echo "❌ n8n user cannot read repository"
```
**Expected Result**: n8n user can read all files
**Actual Result**: _[Fill in during execution]_

---

## Rollback Procedure

**When to Rollback**: If repository copy is incomplete, corrupted, or wrong version

### Rollback Steps

**Step R1**: Remove incomplete build directory
```bash
sudo rm -rf /opt/n8n/build/*
```
**Validation**: `ls -la /opt/n8n/build/` shows empty directory

**Step R2**: Re-create clean build directory
```bash
sudo mkdir -p /opt/n8n/build
sudo chown n8n:n8n /opt/n8n/build
```
**Validation**: Directory exists with correct ownership

**Step R3**: Document failure reason
```bash
echo "Repository clone failed: [reason]" | sudo tee /opt/n8n/docs/clone-failure-$(date +%Y%m%d-%H%M%S).txt
```

**Step R4**: Retry task from Step 1

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
| Build directory created | _[✅/❌]_ | _[ls -ld /opt/n8n/build]_ |
| Source code copied | _[✅/❌]_ | _[package count]_ |
| Repository structure verified | _[✅/❌]_ | _[key packages present]_ |
| Ownership correct | _[✅/❌]_ | _[stat output]_ |
| Version 1.117.0 confirmed | _[✅/❌]_ | _[package.json version]_ |

---

## Knowledge Transfer

### Key Learnings
1. _[Document any issues encountered during copy]_
2. _[Note actual copy duration and method used]_
3. _[Record repository size and package count]_

### Tips for Next Time
- Use rsync for faster copy with progress indication
- Verify source repository integrity before copying
- Always check ownership after bulk file operations
- Save structure verification report for troubleshooting

### Related Resources
- Source repository: `/srv/knowledge/vault/n8n-master/`
- Build location: `/opt/n8n/build/`
- Planning document: `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md`

---

## Task Metadata

```yaml
task_id: T-021
task_type: Repository Setup
parent_work_item: POC3 n8n Deployment - Phase 3.2 Build
assigned_agent: @agent-omar
created_date: 2025-11-07
completed_date: [YYYY-MM-DD]
status: NOT STARTED
priority: P1 - Critical
execution_type: Sequential
estimated_duration: 10 minutes
actual_duration: [X minutes]
systems_affected: [hx-n8n-server.hx.dev.local (192.168.10.215)]
rollback_performed: [yes/no]
source_documents:
  - /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:461
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for n8n repository cloning | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Automated repository copy method selection with `command -v rsync` detection. Eliminates manual decision-making by automatically falling back from rsync to cp if rsync unavailable. Added benefits explanation (progress reporting, incremental copy, attribute preservation) and separate expected output for both tools (lines 144-178). | Claude Code |

---

**Source**: agent-omar-planning-analysis.md:461 (T1.2)
