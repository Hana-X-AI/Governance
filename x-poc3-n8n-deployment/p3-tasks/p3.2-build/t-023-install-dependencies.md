# Task: Install Dependencies

**Task ID**: T-023
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
| **Dependencies** | T-022 |
| **Estimated Duration** | 10-15 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | Yes |

---

## Task Overview

### Objective
Execute `pnpm install` to download and install all 2000+ npm package dependencies required for the n8n monorepo build process.

### Context
The n8n monorepo uses pnpm workspaces to manage 30+ internal packages and 2000+ external dependencies. This task downloads all required packages from npm registry and sets up the node_modules structure needed for the build phase. This is the longest download operation in the build process and must complete successfully before compilation can begin.

### Success Criteria
- [ ] `pnpm install` completes without errors
- [ ] node_modules/ directory created and populated
- [ ] Package count within expected range (1500-2500 packages - security bounds)
- [ ] All workspace packages have node_modules/ symlinks
- [ ] pnpm-lock.yaml verified
- [ ] Vulnerabilities documented (if any) for Phase 4 review
- [ ] Install duration logged for performance tracking

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local (192.168.10.215)
- [ ] Sudo privileges on hx-n8n-server
- [ ] Internet connectivity for npm package downloads

### Required Resources
- [ ] Build environment prepared (from T-022)
- [ ] Disk space verified (≥20GB free)
- [ ] Build log ready at /opt/n8n/logs/build.log
- [ ] npm registry accessible (registry.npmjs.org)

### Required Knowledge
- [ ] pnpm workspace concepts
- [ ] Node.js package management
- [ ] Understanding of dependency installation process
- [ ] Log monitoring and troubleshooting

### Blocking Dependencies
- [ ] T-022 - Prepare Build Environment (disk space verified, logging ready)

---

## Detailed Execution Steps

### Step 1: Navigate to Build Directory

**Command/Action**:
```bash
# Change to build directory
cd /opt/n8n/build/

# Verify we're in correct location
pwd
ls -la package.json pnpm-workspace.yaml
```

**Expected Output**:
```
/opt/n8n/build
-rw-r--r-- 1 n8n n8n XXXX Nov  7 HH:MM package.json
-rw-r--r-- 1 n8n n8n XXXX Nov  7 HH:MM pnpm-workspace.yaml
```

**Validation**:
```bash
# Verify required files present
test -f package.json && \
test -f pnpm-workspace.yaml && \
echo "✅ Build directory verified" || \
echo "❌ Missing required files"
```

**If This Fails**:
- Verify you're in correct directory: `pwd`
- Check if repository was cloned: `ls -la /opt/n8n/build/`
- Re-run T-021 if repository missing
- Escalate to @agent-omar if directory structure wrong

---

### Step 2: Clean Any Previous Installation Attempts

**Command/Action**:
```bash
# Remove any existing node_modules (if present from failed attempt)
if [ -d node_modules ]; then
  echo "⚠️  Removing existing node_modules from previous attempt" | sudo tee -a /opt/n8n/logs/build.log
  rm -rf node_modules
fi

# Remove pnpm cache to ensure clean install
pnpm store prune

# Verify clean state
ls -la | grep node_modules
# Expected: No output (node_modules should not exist)
```

**Expected Output**:
```
Removed X packages from store
(no node_modules directory listed)
```

**Validation**:
```bash
# Verify node_modules doesn't exist
test ! -d node_modules && \
echo "✅ Clean state verified" || \
echo "⚠️  node_modules still exists"
```

**If This Fails**:
- Use sudo to remove: `sudo rm -rf node_modules`
- Check for permission issues: `ls -ld node_modules`
- Proceed anyway if removal fails (pnpm install will overwrite)

---

### Step 3: Execute pnpm install with Logging

**Command/Action**:
```bash
# Record start time
echo "=== DEPENDENCY INSTALLATION STARTED ===" | sudo tee -a /opt/n8n/logs/build.log
echo "Start time: $(date)" | sudo tee -a /opt/n8n/logs/build.log
echo "Command: pnpm install" | sudo tee -a /opt/n8n/logs/build.log
echo "" | sudo tee -a /opt/n8n/logs/build.log

# Execute pnpm install with resource limits as n8n user
# systemd-run provides memory limit (3GB) and CPU quota (80%)
# sudo -u n8n ensures files are owned by n8n:n8n
sudo systemd-run --scope -p MemoryMax=3G -p CPUQuota=80% \
  --uid=n8n --gid=n8n \
  bash -c "cd /opt/n8n/build && pnpm install" 2>&1 | sudo tee -a /opt/n8n/logs/build.log

# Capture exit code from pnpm (not tee) using PIPESTATUS
INSTALL_EXIT_CODE=${PIPESTATUS[0]}

# Record completion
echo "" | sudo tee -a /opt/n8n/logs/build.log
echo "=== DEPENDENCY INSTALLATION COMPLETED ===" | sudo tee -a /opt/n8n/logs/build.log
echo "End time: $(date)" | sudo tee -a /opt/n8n/logs/build.log
echo "Exit code: $INSTALL_EXIT_CODE" | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
Lockfile is up to date, resolution step is skipped
Progress: resolved XXX, reused XXX, downloaded XXX, added XXX
Packages: +2000
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Progress: resolved XXXX, reused XXXX, downloaded XXX, added XXXX, done

dependencies:
[... long list of packages ...]

Done in XXs
```

**Validation**:
```bash
# Check exit code
if [ $INSTALL_EXIT_CODE -eq 0 ]; then
  echo "✅ pnpm install completed successfully" | sudo tee -a /opt/n8n/logs/build.log
else
  echo "❌ pnpm install FAILED with exit code: $INSTALL_EXIT_CODE" | sudo tee -a /opt/n8n/logs/build.log
  echo "⚠️  Check /opt/n8n/logs/build.log for errors"
  exit 1
fi
```

**If This Fails**:
- Check internet connectivity: `ping -c 3 registry.npmjs.org`
- Check for specific error in log: `tail -50 /opt/n8n/logs/build.log`
- Common issues:
  - Network timeout: Retry with `pnpm install --network-timeout 600000`
  - Disk full: Check `df -h /opt`
  - Permission errors: Check ownership `ls -ld /opt/n8n/build/`
  - Registry unavailable: Try alternative registry or wait and retry
- **RETRY ONCE** before escalating
- If second attempt fails, escalate to @agent-zero with full log

---

### Step 4: Verify node_modules Created

**Command/Action**:
```bash
# Check node_modules directory created
ls -ld node_modules/

# Count installed packages
package_count=$(ls -1 node_modules/ | wc -l)
echo "Packages installed: $package_count" | sudo tee -a /opt/n8n/logs/build.log

# Check size of node_modules
du -sh node_modules/ | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
drwxr-xr-x XXX n8n n8n XXXXX Nov  7 HH:MM node_modules/
Packages installed: 2000+ (exact count varies)
1.5G-2.5G    node_modules/
```

**Validation**:
```bash
# Verify package count is within expected range (with security bounds)
# Lower bound: 1500 (minimum expected for n8n)
# Upper bound: 2500 (anomaly detection for supply chain attacks or corrupted lock)
if [ "$package_count" -ge 1500 ] && [ "$package_count" -le 2500 ]; then
  echo "✅ node_modules populated: $package_count packages (within expected range)" | sudo tee -a /opt/n8n/logs/build.log
elif [ "$package_count" -lt 1500 ]; then
  echo "❌ Insufficient packages: $package_count (expected 1500-2500)" | sudo tee -a /opt/n8n/logs/build.log
  echo "⚠️  Incomplete installation - check for errors" | sudo tee -a /opt/n8n/logs/build.log
  exit 1
else
  echo "⚠️  SECURITY WARNING: Abnormal package count: $package_count (expected 1500-2500)" | sudo tee -a /opt/n8n/logs/build.log
  echo "⚠️  Possible supply chain attack or corrupted pnpm-lock.yaml" | sudo tee -a /opt/n8n/logs/build.log
  echo "⚠️  Verify pnpm-lock.yaml integrity before proceeding" | sudo tee -a /opt/n8n/logs/build.log
  # Exit on anomaly for security (can override with --force if verified)
  exit 1
fi
```

**If This Fails**:
- List what was installed: `ls node_modules/ | head -20`
- Check for errors in install output: `grep -i error /opt/n8n/logs/build.log`
- Verify pnpm-lock.yaml: `test -f pnpm-lock.yaml`
- Re-run `pnpm install --force` to force reinstall
- Escalate if repeated failures

---

### Step 5: Verify Workspace Packages Linked

**Command/Action**:
```bash
# Check that workspace packages have node_modules
echo "=== Workspace Package Verification ===" | sudo tee -a /opt/n8n/logs/build.log

# List packages and check for node_modules symlinks
for pkg in packages/*/; do
  pkg_name=$(basename "$pkg")
  if [ -e "${pkg}node_modules" ]; then
    echo "✅ $pkg_name: node_modules linked" | sudo tee -a /opt/n8n/logs/build.log
  else
    echo "⚠️  $pkg_name: NO node_modules" | sudo tee -a /opt/n8n/logs/build.log
  fi
done

# Count linked packages
linked_count=$(find packages/ -maxdepth 2 -name node_modules -type l | wc -l)
echo "Total linked packages: $linked_count" | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
=== Workspace Package Verification ===
✅ cli: node_modules linked
✅ core: node_modules linked
✅ workflow: node_modules linked
[... more packages ...]
Total linked packages: 30+
```

**Validation**:
```bash
# Verify key packages have node_modules
test -e packages/cli/node_modules && \
test -e packages/core/node_modules && \
test -e packages/workflow/node_modules && \
echo "✅ Key workspace packages linked" || \
echo "❌ Workspace linking incomplete"
```

**If This Fails**:
- Check pnpm workspace configuration: `cat pnpm-workspace.yaml`
- Verify symlinks created: `ls -la packages/cli/node_modules`
- Re-run install with workspace flag: `pnpm install --workspace-root`
- Check pnpm version: `pnpm --version` (must be 10.18.3)

---

### Step 6: Check for Vulnerabilities

**Command/Action**:
```bash
# Run pnpm audit to check for vulnerabilities
echo "=== Security Audit ===" | sudo tee -a /opt/n8n/logs/build.log
pnpm audit 2>&1 | sudo tee -a /opt/n8n/logs/build.log

# Capture audit summary
pnpm audit --json > /tmp/pnpm-audit.json 2>&1

# Extract severity counts
echo "" | sudo tee -a /opt/n8n/logs/build.log
echo "Audit Summary:" | sudo tee -a /opt/n8n/logs/build.log
grep -E "critical|high|moderate|low" /tmp/pnpm-audit.json | sudo tee -a /opt/n8n/logs/build.log || echo "No vulnerabilities found" | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
=== Security Audit ===
[Vulnerability report - may show some low/moderate issues]
Audit Summary:
[Severity counts]
```

**Validation**:
```bash
# Check for critical vulnerabilities (acceptable for dev/poc, track for production)
critical_count=$(grep -c '"severity":"critical"' /tmp/pnpm-audit.json 2>/dev/null || echo 0)
high_count=$(grep -c '"severity":"high"' /tmp/pnpm-audit.json 2>/dev/null || echo 0)

if [ "$critical_count" -eq 0 ] && [ "$high_count" -eq 0 ]; then
  echo "✅ No critical or high vulnerabilities" | sudo tee -a /opt/n8n/logs/build.log
else
  echo "⚠️  Vulnerabilities found: $critical_count critical, $high_count high" | sudo tee -a /opt/n8n/logs/build.log
  echo "ℹ️  Acceptable for POC3 - MUST be reviewed before Phase 4 production deployment" | sudo tee -a /opt/n8n/logs/build.log

  # Log vulnerabilities to tracking file for Phase 4 review
  cat >> /opt/n8n/docs/security-vulnerabilities-phase4.txt << EOF
==============================================
Vulnerability Scan Results - POC3 Build
Date: $(date)
Critical: $critical_count
High: $high_count
==============================================

PHASE 4 ACTION REQUIRED:
- Review all critical and high vulnerabilities
- Update dependencies to patched versions
- Re-run pnpm audit before production deployment
- Document accepted risks or mitigations

Full audit report: /tmp/pnpm-audit.json
==============================================
EOF

  echo "ℹ️  Vulnerabilities logged to /opt/n8n/docs/security-vulnerabilities-phase4.txt" | sudo tee -a /opt/n8n/logs/build.log
fi
```

**If This Fails**:
- Audit command not available: Skip this step (not critical for POC3)
- High critical count (>5): Document but proceed for POC3
- **Phase 4 Production**: Review `/opt/n8n/docs/security-vulnerabilities-phase4.txt`
  - Address all critical/high vulnerabilities before production
  - Update dependencies to patched versions
  - Re-run security audit and ensure clean results

---

### Step 7: Create Installation Summary Report

**Command/Action**:
```bash
# Create detailed installation summary
cat > /opt/n8n/docs/dependency-install-summary.txt << EOF
==============================================
n8n Dependency Installation Summary
Server: hx-n8n-server.hx.dev.local
Date: $(date)
Executed by: @agent-omar
==============================================

Installation Details:
- Command: pnpm install
- Duration: [See build.log for timing]
- Exit Code: $INSTALL_EXIT_CODE

Package Statistics:
- Total packages in node_modules: $(ls -1 node_modules/ 2>/dev/null | wc -l)
- Workspace packages linked: $(find packages/ -maxdepth 2 -name node_modules -type l 2>/dev/null | wc -l)
- node_modules size: $(du -sh node_modules/ 2>/dev/null | awk '{print $1}')

Disk Usage After Install:
$(df -h /opt | tail -1)

Lock File:
- pnpm-lock.yaml: $(test -f pnpm-lock.yaml && echo "Present" || echo "Missing")

Security Audit:
- Critical vulnerabilities: $critical_count
- Full audit: See /opt/n8n/logs/build.log

Status: ✅ DEPENDENCIES INSTALLED SUCCESSFULLY

Next Step: T-024 - Build n8n Application (pnpm build:deploy)
==============================================
EOF

sudo chown n8n:n8n /opt/n8n/docs/dependency-install-summary.txt

# Display summary
cat /opt/n8n/docs/dependency-install-summary.txt
```

**Expected Output**:
```
[Complete installation summary with all statistics]
```

**Validation**:
```bash
# Verify summary created
test -f /opt/n8n/docs/dependency-install-summary.txt && \
echo "✅ Installation summary created" || \
echo "❌ Summary creation failed"
```

**If This Fails**:
- Create in /tmp instead: `cat > /tmp/dependency-install-summary.txt`
- Copy manually to docs later

---

## Validation & Testing

### Functional Validation

**Test 1**: All required packages installed
```bash
# Test key dependency packages exist
for pkg in express typeorm n8n-workflow axios; do
  test -d "node_modules/$pkg" && \
  echo "✅ $pkg installed" || \
  echo "❌ $pkg MISSING"
done
```
**Expected Result**: All key packages present
**Actual Result**: _[Fill in during execution]_

---

**Test 2**: Workspace packages can resolve dependencies
```bash
# Test that CLI package can find its dependencies
cd packages/cli
node -e "require('express'); console.log('✅ Dependencies resolvable')" 2>&1
cd ../..
```
**Expected Result**: Dependencies resolvable without errors
**Actual Result**: _[Fill in during execution]_

---

### Performance Validation

**Metric 1**: Installation duration
- **Target**: 10-15 minutes
- **Actual**: _[Fill in from build.log timestamps]_

**Metric 2**: Download size
- **Target**: 1.5GB-2.5GB for node_modules
- **Actual**: _[Fill in from du -sh output]_

**Metric 3**: Package count
- **Target**: 1500+ packages
- **Actual**: _[Fill in from ls count]_

---

## Rollback Procedure

**When to Rollback**: If installation fails with errors, has incomplete packages, or corrupts repository

### Rollback Steps

**Step R1**: Remove node_modules
```bash
cd /opt/n8n/build/
rm -rf node_modules
```
**Validation**: `test ! -d node_modules`

**Step R2**: Clean pnpm cache
```bash
pnpm store prune
```
**Validation**: Cache cleaned message displayed

**Step R3**: Remove lock file (if corrupted)
```bash
rm -f pnpm-lock.yaml
```
**Validation**: `test ! -f pnpm-lock.yaml`

**Step R4**: Document failure
```bash
echo "Dependency installation failed at $(date): [reason]" | \
sudo tee -a /opt/n8n/docs/install-failures.log
```

**Step R5**: Retry task from Step 1
- Check internet connectivity first
- Verify disk space again
- Review error logs before retry

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
| pnpm install completed | _[✅/❌]_ | _[exit code 0]_ |
| node_modules created | _[✅/❌]_ | _[directory exists]_ |
| Workspace packages linked | _[✅/❌]_ | _[symlinks verified]_ |
| pnpm-lock.yaml present | _[✅/❌]_ | _[file exists]_ |
| No critical vulnerabilities | _[✅/❌]_ | _[audit results]_ |
| Duration logged | _[✅/❌]_ | _[timestamps in log]_ |

---

## Documentation Updates

### Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| /opt/n8n/build/node_modules/ | Created | 2000+ packages installed |
| /opt/n8n/build/pnpm-lock.yaml | Created/Updated | Dependency lock file |
| /opt/n8n/logs/build.log | Modified | Installation output logged |
| /opt/n8n/docs/dependency-install-summary.txt | Created | Installation summary |

---

## Knowledge Transfer

### Key Learnings
1. _[Record actual installation duration]_
2. _[Note any packages that had download issues]_
3. _[Document network performance during install]_

### Tips for Next Time
- Ensure stable internet connection before starting
- Monitor disk space during installation
- Use `--network-timeout` flag if registry is slow
- Save pnpm-lock.yaml for reproducible builds
- Review audit results but don't block on low/moderate issues for POC

### Related Resources
- Build log: `/opt/n8n/logs/build.log`
- Install summary: `/opt/n8n/docs/dependency-install-summary.txt`
- pnpm documentation: https://pnpm.io/workspaces
- npm registry: https://registry.npmjs.org

---

## Task Metadata

```yaml
task_id: T-023
task_type: Dependency Installation
parent_work_item: POC3 n8n Deployment - Phase 3.2 Build
assigned_agent: @agent-omar
created_date: 2025-11-07
completed_date: [YYYY-MM-DD]
status: NOT STARTED
priority: P1 - Critical
execution_type: Sequential
estimated_duration: 10-15 minutes
actual_duration: [X minutes]
systems_affected: [hx-n8n-server.hx.dev.local (192.168.10.215)]
rollback_performed: [yes/no]
source_documents:
  - /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:474
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for n8n dependency installation | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: (1) Added upper bound security check to package count validation - flags 2500+ packages as potential supply chain attack or corrupted lock file (lines 234-249); (2) Enhanced vulnerability handling to log critical/high vulns to `/opt/n8n/docs/security-vulnerabilities-phase4.txt` for Phase 4 production review (lines 338-377); (3) Updated success criteria to include security bounds and Phase 4 tracking (lines 36, 39) | Claude Code |

---

**Source**: agent-omar-planning-analysis.md:474 (T2.1)
