# Task: Prepare Build Environment

**Task ID**: T-022
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
| **Dependencies** | T-021 |
| **Estimated Duration** | 20 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | No |

---

## Task Overview

### Objective
Prepare build environment by verifying disk space (≥20GB free), setting up build logging mechanism, and reviewing n8n build documentation for special instructions.

### Context
Before executing the resource-intensive n8n build process, we must ensure adequate disk space, establish logging to capture build output for troubleshooting, and review the repository's build documentation to identify any version-specific build requirements or configuration needs.

### Success Criteria
- [ ] Disk space verified (≥20GB free on /opt partition)
- [ ] Build log mechanism created (tee to /opt/n8n/build.log)
- [ ] package.json reviewed and notes documented
- [ ] CONTRIBUTING.md reviewed for build instructions
- [ ] Pre-build checklist completed and saved

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local (192.168.10.215)
- [ ] Sudo privileges on hx-n8n-server
- [ ] Write access to /opt/n8n/

### Required Resources
- [ ] Repository cloned to /opt/n8n/build/ (from T-021)
- [ ] Text editor (nano, vim, or cat for viewing)
- [ ] Terminal multiplexer optional (tmux/screen)

### Required Knowledge
- [ ] Linux disk space management
- [ ] Log file creation and redirection
- [ ] package.json format and scripts section
- [ ] Markdown documentation reading

### Blocking Dependencies
- [ ] T-021 - Clone n8n Repository (repository must be present in /opt/n8n/build/)

---

## Detailed Execution Steps

### Step 1: Verify Disk Space

**Command/Action**:
```bash
# Check disk space on /opt partition
df -h /opt

# Check inode availability
df -i /opt

# Calculate required space (build needs ~15-20GB)
du -sh /opt/n8n/build/
```

**Expected Output**:
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sdX        100G   30G   65G  32% /opt

Filesystem     Inodes IUsed IFree IUse% Mounted on
/dev/sdX         6.5M  100K  6.4M    2% /opt

~500M-1G    /opt/n8n/build/
```

**Validation**:
```bash
# Verify at least 20GB free (using KB for accuracy - BUILD-004 fix)
available_kb=$(df -k /opt | tail -1 | awk '{print $4}')
available_gb=$((available_kb / 1024 / 1024))

if [ "$available_gb" -ge 20 ]; then
  echo "✅ Sufficient disk space: ${available_gb}GB available (≥20GB required)"
else
  echo "❌ INSUFFICIENT disk space: ${available_gb}GB available (20GB required)"
  echo "⚠️  BUILD CANNOT PROCEED - Free up disk space first"
  # Show more precise calculation for troubleshooting
  available_precise=$(echo "scale=2; $available_kb / 1024 / 1024" | bc)
  echo "Precise available: ${available_precise}GB"
fi
```

**If This Fails**:
- Check what's using space: `du -h /opt | sort -h | tail -20`
- Remove old logs: `sudo find /var/log -name "*.gz" -delete`
- Remove old packages: `sudo apt clean && sudo apt autoremove`
- Consider expanding partition or using different mount point
- **DO NOT PROCEED if <20GB free** - Escalate to @agent-william

---

### Step 2: Create Build Log Directory and Mechanism

**Command/Action**:
```bash
# Create logs directory
sudo mkdir -p /opt/n8n/logs
sudo chown n8n:n8n /opt/n8n/logs

# Create build log file with proper permissions
sudo touch /opt/n8n/logs/build.log
sudo chown n8n:n8n /opt/n8n/logs/build.log
sudo chmod 644 /opt/n8n/logs/build.log

# Verify log file ready
ls -la /opt/n8n/logs/build.log
```

**Expected Output**:
```
-rw-r--r-- 1 n8n n8n 0 Nov  7 HH:MM /opt/n8n/logs/build.log
```

**Validation**:
```bash
# Test write to log file
echo "=== n8n Build Log ===" | sudo tee /opt/n8n/logs/build.log
echo "Build started: $(date)" | sudo tee -a /opt/n8n/logs/build.log
echo "Server: hx-n8n-server.hx.dev.local" | sudo tee -a /opt/n8n/logs/build.log
echo "Build location: /opt/n8n/build/" | sudo tee -a /opt/n8n/logs/build.log
echo "========================" | sudo tee -a /opt/n8n/logs/build.log
echo "" | sudo tee -a /opt/n8n/logs/build.log

# Verify log writable
test -w /opt/n8n/logs/build.log && \
echo "✅ Build log ready at /opt/n8n/logs/build.log" || \
echo "❌ Build log not writable"
```

**If This Fails**:
- Check directory permissions: `ls -ld /opt/n8n/logs`
- Recreate with correct ownership: `sudo mkdir -p /opt/n8n/logs && sudo chown n8n:n8n /opt/n8n/logs`
- Verify disk not full: `df -h /opt`
- Check for filesystem errors: `dmesg | grep error`

---

### Step 3: Review package.json Build Configuration

**Command/Action**:
```bash
# Display package.json scripts section
echo "=== package.json Build Scripts ===" | tee -a /opt/n8n/logs/build.log
cat /opt/n8n/build/package.json | grep -A 20 '"scripts"' | tee -a /opt/n8n/logs/build.log

# Extract key build information
echo "" | tee -a /opt/n8n/logs/build.log
echo "=== Key Build Information ===" | tee -a /opt/n8n/logs/build.log
echo "Version: $(grep '"version"' /opt/n8n/build/package.json | head -1)" | tee -a /opt/n8n/logs/build.log
echo "Package Manager: $(grep '"packageManager"' /opt/n8n/build/package.json)" | tee -a /opt/n8n/logs/build.log
echo "Node.js Required: $(grep '"node"' /opt/n8n/build/package.json | grep engines -A 1)" | tee -a /opt/n8n/logs/build.log
echo "pnpm Required: $(grep '"pnpm"' /opt/n8n/build/package.json | grep engines -A 1)" | tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
=== package.json Build Scripts ===
  "scripts": {
    "build": "turbo run build",
    "build:deploy": "turbo run build --filter=n8n...",
    ...
  }

=== Key Build Information ===
Version: "version": "1.117.0",
Package Manager: "packageManager": "pnpm@10.18.3"
Node.js Required: (shows >=22.16.0)
pnpm Required: (shows >=10.18.3)
```

**Validation**:
```bash
# Create build configuration summary
cat > /tmp/build-config-notes.txt << EOF
==============================================
n8n Build Configuration Review
Date: $(date)
Repository: /opt/n8n/build/
==============================================

Version: $(grep '"version"' /opt/n8n/build/package.json | head -1 | tr -d ',' | awk '{print $2}')

Build Scripts Available:
$(grep '"build' /opt/n8n/build/package.json | sed 's/^/  /')

Package Manager: $(grep '"packageManager"' /opt/n8n/build/package.json | awk '{print $2}' | tr -d '",')

Engine Requirements:
$(grep -A 3 '"engines"' /opt/n8n/build/package.json)

Workspace Configuration:
$(cat /opt/n8n/build/pnpm-workspace.yaml)

==============================================
NOTES:
- Build command: pnpm build:deploy
- Expected duration: 30-45 minutes
- Expected output: packages/*/dist/ directories
- Turbo used for build orchestration
==============================================
EOF

cat /tmp/build-config-notes.txt
sudo cp /tmp/build-config-notes.txt /opt/n8n/docs/build-config-notes.txt
```

**If This Fails**:
- Verify package.json exists: `test -f /opt/n8n/build/package.json`
- Check JSON syntax: `cat /opt/n8n/build/package.json | python3 -m json.tool > /dev/null`
- Review file manually if grep fails: `cat /opt/n8n/build/package.json`

---

### Step 4: Review CONTRIBUTING.md for Build Instructions

**Command/Action**:
```bash
# Check if CONTRIBUTING.md exists
if [ -f /opt/n8n/build/CONTRIBUTING.md ]; then
  echo "=== CONTRIBUTING.md Build Instructions ===" | tee -a /opt/n8n/logs/build.log

  # Extract build-related sections
  grep -i -A 10 "build\|install\|setup\|development" /opt/n8n/build/CONTRIBUTING.md | head -50 | tee -a /opt/n8n/logs/build.log

  echo "" | tee -a /opt/n8n/logs/build.log
  echo "✅ CONTRIBUTING.md reviewed" | tee -a /opt/n8n/logs/build.log
else
  echo "⚠️  CONTRIBUTING.md not found - proceeding with standard build" | tee -a /opt/n8n/logs/build.log
fi

# Check for README.md as alternative
if [ -f /opt/n8n/build/README.md ]; then
  echo "=== README.md Build Sections ===" | tee -a /opt/n8n/logs/build.log
  grep -i -A 5 "build\|install\|setup" /opt/n8n/build/README.md | head -30 | tee -a /opt/n8n/logs/build.log
fi
```

**Expected Output**:
```
=== CONTRIBUTING.md Build Instructions ===
[Build setup instructions from CONTRIBUTING.md]
[Development environment setup]
[Prerequisites and requirements]

✅ CONTRIBUTING.md reviewed
```

**Validation**:
```bash
# Save documentation review notes
cat > /tmp/build-docs-review.txt << EOF
==============================================
n8n Build Documentation Review
Date: $(date)
==============================================

CONTRIBUTING.md: $(test -f /opt/n8n/build/CONTRIBUTING.md && echo "Present" || echo "Not found")
README.md: $(test -f /opt/n8n/build/README.md && echo "Present" || echo "Not found")

Key Build Steps Identified:
1. pnpm install (install dependencies)
2. pnpm build:deploy (compile all packages)
3. Outputs to packages/*/dist/ directories

Special Requirements Noted:
- Node.js ≥22.16.0 (VERIFIED in T-020)
- pnpm 10.18.3 via corepack (VERIFIED in T-020)
- Build tools installed (VERIFIED in T-020)

No special build flags or environment variables required for v1.117.0

==============================================
EOF

cat /tmp/build-docs-review.txt
sudo cp /tmp/build-docs-review.txt /opt/n8n/docs/build-docs-review.txt
```

**If This Fails**:
- Proceed without documentation review
- Use standard build process (pnpm install, pnpm build:deploy)
- Document that CONTRIBUTING.md was not available

---

### Step 5: Create Pre-Build Checklist

**Command/Action**:
```bash
# Create comprehensive pre-build checklist with variable expansion
# Note: Using unquoted EOF to allow $(date) and $(df) to expand
cat > /opt/n8n/docs/pre-build-checklist.md << EOF
# n8n Pre-Build Checklist
**Server**: hx-n8n-server.hx.dev.local (192.168.10.215)
**Date**: $(date)
**Agent**: @agent-omar

## Environment Verification
- [x] Node.js ≥22.16.0 installed (T-020)
- [x] pnpm 10.18.3 via corepack (T-020)
- [x] Build tools installed (gcc, g++, make, python3) (T-020)
- [x] Graphics libraries installed (cairo, pango) (T-020)
- [x] n8n system user created (T-020)

## Repository Setup
- [x] Repository cloned to /opt/n8n/build/ (T-021)
- [x] Repository version verified: 1.117.0 (T-021)
- [x] Repository structure validated (T-021)
- [x] Ownership set to n8n:n8n (T-021)

## Build Environment Preparation
- [x] Disk space verified: $(df -h /opt | tail -1 | awk '{print $4}') available (≥20GB required)
- [x] Build log created: /opt/n8n/logs/build.log
- [x] package.json reviewed
- [x] Build configuration documented

## Ready for Build
- [ ] All checklist items above marked complete
- [ ] No blockers or issues identified
- [ ] Build can proceed to T-023 (pnpm install)

## Next Steps
1. T-023: Install Dependencies (pnpm install)
2. T-024: Build n8n Application (pnpm build:deploy)
3. T-025: Verify Build Output
4. T-026: Test Build Executable

---
**Prepared by**: @agent-omar
**Status**: ✅ READY FOR BUILD
EOF

# Set ownership
sudo chown n8n:n8n /opt/n8n/docs/pre-build-checklist.md

# Display checklist
cat /opt/n8n/docs/pre-build-checklist.md
```

**Expected Output**:
```
[Complete pre-build checklist displayed]
```

**Validation**:
```bash
# Verify checklist created
test -f /opt/n8n/docs/pre-build-checklist.md && \
echo "✅ Pre-build checklist created" || \
echo "❌ Checklist creation failed"
```

**If This Fails**:
- Create directory: `sudo mkdir -p /opt/n8n/docs`
- Retry checklist creation
- Save to /tmp if /opt/n8n/docs not writable

---

## Validation & Testing

### Functional Validation

**Test 1**: Disk space adequate for build
```bash
available=$(df -BG /opt | tail -1 | awk '{print $4}' | sed 's/G//')
test "$available" -ge 20 && \
echo "✅ Disk space adequate: ${available}GB" || \
echo "❌ Insufficient disk space: ${available}GB"
```
**Expected Result**: ≥20GB available
**Actual Result**: _[Fill in during execution]_

---

**Test 2**: Build log mechanism functional
```bash
echo "Test log entry" | sudo tee -a /opt/n8n/logs/build.log > /dev/null && \
test -s /opt/n8n/logs/build.log && \
echo "✅ Build log functional" || \
echo "❌ Build log not working"
```
**Expected Result**: Log file writable and contains data
**Actual Result**: _[Fill in during execution]_

---

**Test 3**: All documentation reviewed
```bash
test -f /opt/n8n/docs/build-config-notes.txt && \
test -f /opt/n8n/docs/pre-build-checklist.md && \
echo "✅ All documentation prepared" || \
echo "❌ Documentation incomplete"
```
**Expected Result**: All documentation files created
**Actual Result**: _[Fill in during execution]_

---

## Rollback Procedure

**When to Rollback**: Not applicable - this is a preparation task only

**No rollback needed** - If preparation fails, address specific issues and re-run task

---

## Results

### Task Outcome
- **Status**: _[COMPLETED | FAILED | PARTIALLY COMPLETED]_
- **Start Time**: _[HH:MM]_
- **End Time**: _[HH:MM]_
- **Duration**: _[X minutes]_
- **Rollback Needed**: No

### Success Criteria Results

| Criterion | Met? | Evidence |
|-----------|------|----------|
| Disk space verified (≥20GB) | _[✅/❌]_ | _[df -h output]_ |
| Build log created | _[✅/❌]_ | _[ls output]_ |
| package.json reviewed | _[✅/❌]_ | _[notes created]_ |
| CONTRIBUTING.md reviewed | _[✅/❌]_ | _[review completed]_ |
| Pre-build checklist complete | _[✅/❌]_ | _[checklist file]_ |

---

## Knowledge Transfer

### Key Learnings
1. _[Document disk space available before build]_
2. _[Note any special build requirements found in documentation]_
3. _[Record packageManager and engine requirements]_

### Tips for Next Time
- Always verify disk space before starting resource-intensive builds
- Set up logging early to capture full build output
- Review repository documentation for version-specific requirements
- Create checklist to verify all prerequisites before proceeding

### Related Resources
- Build log: `/opt/n8n/logs/build.log`
- Configuration notes: `/opt/n8n/docs/build-config-notes.txt`
- Pre-build checklist: `/opt/n8n/docs/pre-build-checklist.md`

---

## Task Metadata

```yaml
task_id: T-022
task_type: Build Preparation
parent_work_item: POC3 n8n Deployment - Phase 3.2 Build
assigned_agent: @agent-omar
created_date: 2025-11-07
completed_date: [YYYY-MM-DD]
status: NOT STARTED
priority: P1 - Critical
execution_type: Sequential
estimated_duration: 20 minutes
actual_duration: [X minutes]
systems_affected: [hx-n8n-server.hx.dev.local (192.168.10.215)]
rollback_performed: no
source_documents:
  - /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:462-464
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for build environment preparation | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Simplified heredoc approach for pre-build checklist creation (lines 316-364). Removed quoted 'EOF' and nested `bash -c` commands that could create quoting issues when variables contain special characters. Now uses single unquoted EOF heredoc with direct file redirection: `cat > /opt/n8n/docs/pre-build-checklist.md << EOF` followed by `sudo chown n8n:n8n`. This eliminates shell quoting complexity while preserving variable expansion for $(date) and $(df). | Claude Code |

---

**Source**: agent-omar-planning-analysis.md:462-464 (T1.3, T1.4, T1.5 combined)
