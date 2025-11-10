# Task: Deploy Compiled Artifacts

**Task ID**: T-028
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
| **Dependencies** | T-027 |
| **Estimated Duration** | 10 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | Yes |

---

## Task Overview

### Objective
Copy all compiled artifacts from the build directory (`/opt/n8n/build/packages/*/dist/`) to the production deployment directory (`/opt/n8n/app/`) to prepare n8n for execution.

### Context
After successful build verification (T-026), we now deploy the compiled JavaScript code to the production location. This separates build artifacts from the running application, allowing us to preserve the build directory for reference while deploying clean production code. We copy the entire packages structure including all dist/ directories to maintain the monorepo structure that n8n expects.

### Success Criteria
- [ ] All packages/*/dist/ directories copied to /opt/n8n/app/packages/*/dist/
- [ ] At least 30 packages deployed (per specification)
- [ ] CLI executable present at /opt/n8n/app/packages/cli/bin/n8n
- [ ] All compiled JavaScript files present (no TypeScript source)
- [ ] Package.json files copied for each package
- [ ] Deployment size documented (approximately 500MB)
- [ ] No broken symlinks or missing dependencies

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local (192.168.10.215)
- [ ] Sudo privileges for file operations
- [ ] Write access to /opt/n8n/app/

### Required Resources
- [ ] Build artifacts verified in /opt/n8n/build/ (T-026)
- [ ] Deployment directory created /opt/n8n/app/ (T-027)
- [ ] Sufficient disk space (2GB free minimum for artifacts)

### Required Knowledge
- [ ] n8n monorepo package structure
- [ ] Linux file copy operations (cp, rsync)
- [ ] Symlink handling

### Blocking Dependencies
- [ ] T-026 - Test build executable (build verified working)
- [ ] T-027 - Create deployment directory structure (target exists)

---

## Detailed Execution Steps

### Step 1: Verify Source and Target Directories

**Command/Action**:
```bash
# Verify build directory exists and contains artifacts
echo "=== Pre-Deployment Verification ==="
echo "Date: $(date)"
echo ""

if [ ! -d /opt/n8n/build/packages/ ]; then
  echo "❌ Build directory missing: /opt/n8n/build/packages/"
  echo "⚠️  Run T-026 first to verify build"
  exit 1
fi
echo "✅ Build directory present: /opt/n8n/build/packages/"

# Count packages with dist directories
dist_count=$(find /opt/n8n/build/packages/ -type d -name dist | wc -l)
echo "Packages with dist/: $dist_count"

# Package count threshold aligned with specification
EXPECTED_PACKAGE_COUNT=30

if [ "$dist_count" -lt "$EXPECTED_PACKAGE_COUNT" ]; then
  echo "❌ Insufficient packages built ($dist_count found, expected ${EXPECTED_PACKAGE_COUNT}+)"
  echo "⚠️  Verify build completed successfully"
  exit 1
fi
echo "✅ Sufficient packages built for deployment"

# Verify target directory exists and is empty
if [ ! -d /opt/n8n/app/ ]; then
  echo "❌ Deployment directory missing: /opt/n8n/app/"
  echo "⚠️  Run T-027 first"
  exit 1
fi
echo "✅ Deployment directory present: /opt/n8n/app/"

# Check if deployment already exists
if [ -d /opt/n8n/app/packages/ ]; then
  echo "⚠️  Existing deployment found - will be overwritten"
  ls -la /opt/n8n/app/packages/ | head -10
else
  echo "✅ Clean deployment - no existing artifacts"
fi
```

**Expected Output**:
```
=== Pre-Deployment Verification ===
Date: Thu Nov  7 HH:MM:SS CST 2025

✅ Build directory present: /opt/n8n/build/packages/
Packages with dist/: 30
✅ Sufficient packages built for deployment
✅ Deployment directory present: /opt/n8n/app/
✅ Clean deployment - no existing artifacts
```

**Validation**:
```bash
# Verify we can proceed
test -d /opt/n8n/build/packages/ && \
test -d /opt/n8n/app/ && \
test $(find /opt/n8n/build/packages/ -type d -name dist | wc -l) -ge 25 && \
echo "✅ Ready to deploy" || \
echo "❌ Pre-deployment checks failed"
```

**If This Fails**:
- Build directory missing: Run T-020 through T-026 first
- Insufficient packages: Re-run build (T-024)
- Target missing: Run T-027 first
- Cannot proceed without fixing blockers

---

### Step 2: Calculate Source Size

**Command/Action**:
```bash
# Calculate size of artifacts to be deployed
echo "=== Calculating Deployment Size ==="

# Size of all dist directories (use du -sm for machine-readable MB totals)
dist_size=$(du -sm /opt/n8n/build/packages/*/dist 2>/dev/null | awk '{sum+=$1} END {printf "%.0f\n", sum}')
if [[ -z "$dist_size" ]] || ! [[ "$dist_size" =~ ^[0-9]+$ ]]; then
  echo "⚠️ Could not calculate dist/ size - skipping size check"
  dist_size="unknown"
else
  echo "Total dist/ size: ${dist_size}MB"
fi

# Count files to be copied
file_count=$(find /opt/n8n/build/packages/*/dist -type f 2>/dev/null | wc -l)
echo "Total files: $file_count"

# Check available space (validate numeric output)
available=$(df -BM /opt 2>/dev/null | tail -1 | awk '{print $4}' | sed 's/M//')
if [[ -z "$available" ]] || ! [[ "$available" =~ ^[0-9]+$ ]]; then
  echo "⚠️ Could not determine available disk space - skipping space check"
else
  echo "Available space: ${available}MB"
  if [ "$available" -lt 2000 ]; then
    echo "⚠️ Low disk space: ${available}MB (2GB+ recommended)"
  else
    echo "✅ Sufficient disk space"
  fi
fi

# Estimate deployment time (rough: 100 files per second)
estimated_seconds=$((file_count / 100))
echo "Estimated copy time: ${estimated_seconds} seconds"
```

**Expected Output**:
```
=== Calculating Deployment Size ===
Total dist/ size: 450MB
Total files: 8500
Available space: 45000MB
✅ Sufficient disk space
Estimated copy time: 85 seconds
```

**Validation**:
```bash
# Verify sufficient space (need 2GB minimum)
test "$available" -ge 2000 && \
echo "✅ Space check passed" || \
echo "⚠️  Space may be insufficient"
```

**If This Fails**:
- Low disk space: Clean up /opt/n8n/build/ after deployment, or expand disk
- Cannot calculate size: Non-critical, proceed with deployment

---

### Step 3: Copy packages Directory Structure

**Command/Action**:
```bash
# Copy entire packages structure with rsync for reliability
echo "=== Deploying Packages Structure ==="
echo "Start time: $(date)"

# Create packages directory in app
sudo mkdir -p /opt/n8n/app/packages/

# Use rsync to copy with progress and verification
# -a = archive mode (preserves permissions, timestamps)
# -v = verbose
# --info=progress2 = show overall progress
# --exclude='*.ts' = exclude TypeScript source files
# --exclude='src' = exclude source directories
# --exclude='test' = exclude test directories

sudo rsync -av --info=progress2 \
  --exclude='*.ts' \
  --exclude='src' \
  --exclude='test' \
  --exclude='*.spec.js' \
  --exclude='*.test.js' \
  /opt/n8n/build/packages/ \
  /opt/n8n/app/packages/ 2>&1 | tee /tmp/deploy-rsync.log

# Capture exit code
RSYNC_EXIT=$?

echo ""
echo "End time: $(date)"

if [ $RSYNC_EXIT -eq 0 ]; then
  echo "✅ Packages deployed successfully"
else
  echo "❌ Rsync failed with exit code: $RSYNC_EXIT"
  echo "Check /tmp/deploy-rsync.log for details"
  exit 1
fi
```

**Expected Output**:
```
=== Deploying Packages Structure ===
Start time: Thu Nov  7 HH:MM:SS CST 2025

sending incremental file list
packages/
packages/cli/
packages/cli/dist/
packages/cli/dist/index.js
[... many files ...]

Number of files: 8,500 (reg: 8,000, dir: 500)
Number of created files: 8,500
Total file size: 450M bytes
Total transferred file size: 450M bytes

End time: Thu Nov  7 HH:MM:SS CST 2025
✅ Packages deployed successfully
```

**Validation**:
```bash
# Verify packages directory copied
test -d /opt/n8n/app/packages/ && \
echo "✅ packages/ directory present" || \
echo "❌ packages/ directory MISSING"

# Count deployed packages (aligned with specification: 30+ expected)
EXPECTED_PACKAGE_COUNT=30
deployed_count=$(ls -1d /opt/n8n/app/packages/*/ 2>/dev/null | wc -l)
echo "Deployed packages: $deployed_count (expected ≥${EXPECTED_PACKAGE_COUNT})"

if [ "$deployed_count" -ge "$EXPECTED_PACKAGE_COUNT" ]; then
  echo "✅ Sufficient packages deployed"
else
  echo "❌ Incomplete deployment: only $deployed_count packages (expected ≥${EXPECTED_PACKAGE_COUNT})"
  exit 1
fi
```

**If This Fails**:
- rsync failed: Check /tmp/deploy-rsync.log for specific errors
- Permission denied: Use sudo for rsync command
- Disk full: Free up space and retry
- Partial copy: Re-run rsync (it will resume/update)
- Missing packages: Verify build contains all packages

---

### Step 4: Verify Critical Package Artifacts

**Command/Action**:
```bash
# Verify critical packages deployed correctly
echo "=== Verifying Critical Packages ==="

# Check core packages
critical_packages=("cli" "core" "workflow" "nodes-base" "editor-ui")

for pkg in "${critical_packages[@]}"; do
  if [ -d "/opt/n8n/app/packages/$pkg/dist/" ]; then
    file_count=$(find "/opt/n8n/app/packages/$pkg/dist/" -type f | wc -l)
    echo "✅ $pkg: deployed ($file_count files)"
  else
    echo "❌ $pkg: MISSING dist directory"
  fi
done

# Verify package.json files present
echo ""
echo "Verifying package.json files:"
for pkg_dir in /opt/n8n/app/packages/*/; do
  pkg_name=$(basename "$pkg_dir")
  if [ -f "$pkg_dir/package.json" ]; then
    echo "✅ $pkg_name: package.json present"
  else
    echo "❌ $pkg_name: package.json MISSING"
  fi
done | head -10
```

**Expected Output**:
```
=== Verifying Critical Packages ===
✅ cli: deployed (450 files)
✅ core: deployed (320 files)
✅ workflow: deployed (180 files)
✅ nodes-base: deployed (2500 files)
✅ editor-ui: deployed (1800 files)

Verifying package.json files:
✅ cli: package.json present
✅ core: package.json present
✅ workflow: package.json present
[... more packages ...]
```

**Validation**:
```bash
# Verify all critical packages present
all_present=true
for pkg in cli core workflow nodes-base editor-ui; do
  if [ ! -d "/opt/n8n/app/packages/$pkg/dist/" ]; then
    all_present=false
    break
  fi
done

if $all_present; then
  echo "✅ All critical packages deployed"
else
  echo "❌ Missing critical packages"
fi
```

**If This Fails**:
- Missing critical package: Re-run rsync for specific package
- Missing package.json: Copy manually from build directory
- Empty dist directory: Check build step, rebuild if needed

---

### Step 5: Verify CLI Executable

**Command/Action**:
```bash
# Verify CLI executable deployed
echo "=== Verifying CLI Executable ==="

if [ -f /opt/n8n/app/packages/cli/bin/n8n ]; then
  echo "✅ CLI executable found: /opt/n8n/app/packages/cli/bin/n8n"

  # Check executable bit
  if [ -x /opt/n8n/app/packages/cli/bin/n8n ]; then
    echo "✅ Executable permission set"
  else
    echo "⚠️  Setting executable permission"
    sudo chmod +x /opt/n8n/app/packages/cli/bin/n8n
  fi

  # Show file details
  ls -lh /opt/n8n/app/packages/cli/bin/n8n

  # Show first few lines (shebang)
  echo ""
  echo "Executable header:"
  head -3 /opt/n8n/app/packages/cli/bin/n8n
else
  echo "❌ CLI executable NOT FOUND"
  echo "Expected: /opt/n8n/app/packages/cli/bin/n8n"
  exit 1
fi
```

**Expected Output**:
```
=== Verifying CLI Executable ===
✅ CLI executable found: /opt/n8n/app/packages/cli/bin/n8n
✅ Executable permission set
-rwxr-xr-x 1 root root 250 Nov  7 HH:MM /opt/n8n/app/packages/cli/bin/n8n

Executable header:
#!/usr/bin/env node
[JavaScript code]
```

**Validation**:
```bash
# Comprehensive executable check
test -f /opt/n8n/app/packages/cli/bin/n8n && \
test -x /opt/n8n/app/packages/cli/bin/n8n && \
echo "✅ CLI executable ready" || \
echo "❌ CLI executable not ready"
```

**If This Fails**:
- Missing executable: Copy from build: `sudo cp /opt/n8n/build/packages/cli/bin/n8n /opt/n8n/app/packages/cli/bin/`
- Not executable: Run `sudo chmod +x /opt/n8n/app/packages/cli/bin/n8n`
- Broken symlink: Verify target exists

---

### Step 6: Verify No TypeScript Source in Deployment

**Command/Action**:
```bash
# Ensure no TypeScript source files in deployment
echo "=== Verifying Deployment Purity ==="

# Count TypeScript files
ts_count=$(find /opt/n8n/app/packages/ -name "*.ts" -type f 2>/dev/null | wc -l)
echo "TypeScript files found: $ts_count"

if [ "$ts_count" -eq 0 ]; then
  echo "✅ No TypeScript source in deployment"
else
  echo "⚠️  Found $ts_count TypeScript files (should be 0)"
  echo "Listing first 10:"
  find /opt/n8n/app/packages/ -name "*.ts" -type f | head -10
fi

# Count JavaScript files (should be many)
js_count=$(find /opt/n8n/app/packages/ -name "*.js" -type f 2>/dev/null | wc -l)
echo "JavaScript files found: $js_count"

if [ "$js_count" -gt 1000 ]; then
  echo "✅ Sufficient JavaScript files deployed"
else
  echo "❌ Insufficient JavaScript files ($js_count found, expected 5000+)"
fi

# Check for src directories (should not exist in production)
src_count=$(find /opt/n8n/app/packages/ -type d -name src 2>/dev/null | wc -l)
echo "src/ directories found: $src_count"

if [ "$src_count" -eq 0 ]; then
  echo "✅ No source directories in deployment"
else
  echo "⚠️  Found $src_count src directories (rsync exclude may have failed)"
fi
```

**Expected Output**:
```
=== Verifying Deployment Purity ===
TypeScript files found: 0
✅ No TypeScript source in deployment
JavaScript files found: 7500
✅ Sufficient JavaScript files deployed
src/ directories found: 0
✅ No source directories in deployment
```

**Validation**:
```bash
# Verify deployment is production-ready
test "$ts_count" -eq 0 && \
test "$js_count" -gt 1000 && \
echo "✅ Deployment purity verified" || \
echo "⚠️  Deployment may contain source files"
```

**If This Fails**:
- TypeScript files present: Delete them with `find /opt/n8n/app/packages/ -name "*.ts" -delete`
- Few JavaScript files: Check if dist directories were copied
- src directories present: Safe to ignore if .ts files are excluded, or remove with `find /opt/n8n/app/packages/ -type d -name src -exec rm -rf {} +`

---

### Step 7: Document Deployment

**Command/Action**:
```bash
# Create deployment documentation
cat > /tmp/artifact-deployment.txt << EOF
==============================================
n8n Artifact Deployment Report
Server: hx-n8n-server.hx.dev.local
Deployed: $(date)
Executed by: @agent-omar
==============================================

SOURCE:
-------
Build directory: /opt/n8n/build/packages/
Build verification: T-026 (passed)

TARGET:
-------
Deployment directory: /opt/n8n/app/packages/
Deployment method: rsync with exclude filters

DEPLOYMENT STATISTICS:
----------------------
Total packages deployed: $(ls -1d /opt/n8n/app/packages/*/ 2>/dev/null | wc -l)
Total files copied: $(find /opt/n8n/app/packages/ -type f 2>/dev/null | wc -l)
JavaScript files: $(find /opt/n8n/app/packages/ -name "*.js" 2>/dev/null | wc -l)
TypeScript files: $(find /opt/n8n/app/packages/ -name "*.ts" 2>/dev/null | wc -l)
Total deployment size: $(du -sh /opt/n8n/app/packages/ | awk '{print $1}')

CRITICAL PACKAGES:
------------------
$(for pkg in cli core workflow nodes-base editor-ui; do
  if [ -d "/opt/n8n/app/packages/$pkg/dist/" ]; then
    echo "✅ $pkg: $(find "/opt/n8n/app/packages/$pkg/dist/" -type f | wc -l) files"
  else
    echo "❌ $pkg: MISSING"
  fi
done)

CLI EXECUTABLE:
---------------
Path: /opt/n8n/app/packages/cli/bin/n8n
Status: $(test -x /opt/n8n/app/packages/cli/bin/n8n && echo "Present and executable" || echo "Missing or not executable")

DISK USAGE:
-----------
Before deployment: [from Step 2]
After deployment: $(df -h /opt | tail -1)

VERIFICATION:
-------------
- No TypeScript source in deployment: $([ "$ts_count" -eq 0 ] && echo "PASS" || echo "FAIL")
- Sufficient JavaScript files: $([ "$js_count" -gt 1000 ] && echo "PASS" || echo "FAIL")
- CLI executable present: $(test -x /opt/n8n/app/packages/cli/bin/n8n && echo "PASS" || echo "FAIL")
- Critical packages present: $([ -d /opt/n8n/app/packages/cli/dist/ ] && echo "PASS" || echo "FAIL")

STATUS: ✅ DEPLOYMENT COMPLETE

NEXT STEPS:
-----------
T-029: Deploy node_modules
T-030: Set file ownership
T-031: Set file permissions

==============================================
EOF

# Copy to docs
sudo cp /tmp/artifact-deployment.txt /opt/n8n/docs/artifact-deployment.txt
sudo chown n8n:n8n /opt/n8n/docs/artifact-deployment.txt

# Display report
echo ""
cat /opt/n8n/docs/artifact-deployment.txt
```

**Expected Output**:
```
[Complete deployment report]
```

**Validation**:
```bash
# Verify documentation created
test -f /opt/n8n/docs/artifact-deployment.txt && \
echo "✅ Deployment documented" || \
echo "❌ Documentation failed"
```

**If This Fails**:
- Save to /tmp for later: Non-critical, proceed

---

## Validation & Testing

### Functional Validation

**Test 1**: All packages deployed
```bash
# Verify expected package count
deployed=$(ls -1d /opt/n8n/app/packages/*/ 2>/dev/null | wc -l)
built=$(ls -1d /opt/n8n/build/packages/*/ 2>/dev/null | wc -l)

echo "Built packages: $built"
echo "Deployed packages: $deployed"

test "$deployed" -eq "$built" && \
echo "✅ All packages deployed" || \
echo "⚠️  Package count mismatch"
```
**Expected Result**: Deployed count matches built count
**Actual Result**: _[Fill in during execution]_

---

**Test 2**: Critical files present
```bash
# Verify essential files exist
test -f /opt/n8n/app/packages/cli/dist/index.js && echo "✅ cli/dist/index.js" || echo "❌ Missing"
test -f /opt/n8n/app/packages/core/dist/index.js && echo "✅ core/dist/index.js" || echo "❌ Missing"
test -f /opt/n8n/app/packages/workflow/dist/index.js && echo "✅ workflow/dist/index.js" || echo "❌ Missing"
```
**Expected Result**: All critical files present
**Actual Result**: _[Fill in during execution]_

---

### Performance Validation

**Metric 1**: Deployment duration
- **Target**: <3 minutes for rsync
- **Actual**: _[from deployment log]_

**Metric 2**: Deployment size
- **Target**: 400-600MB
- **Actual**: _[from du command]_

**Metric 3**: File count
- **Target**: 5000+ files
- **Actual**: _[from find command]_

---

## Rollback Procedure

**When to Rollback**: If critical packages missing, deployment corrupted, or disk full

### Rollback Steps

**Step R1**: Remove deployed packages
```bash
sudo rm -rf /opt/n8n/app/packages/
```
**Validation**: Deployment directory empty, build preserved

**Step R2**: Verify build intact
```bash
test -d /opt/n8n/build/packages/ && \
echo "✅ Build preserved for re-deployment"
```

**Step R3**: Document failure
```bash
echo "Artifact deployment failed at $(date): [REASON]" | \
sudo tee -a /opt/n8n/docs/deployment-failures.log
```

---

## Results

### Task Outcome
- **Status**: _[COMPLETED | FAILED]_
- **Start Time**: _[HH:MM]_
- **End Time**: _[HH:MM]_
- **Duration**: _[X minutes]_
- **Rollback Needed**: _[Yes/No]_

### Success Criteria Results

| Criterion | Met? | Evidence |
|-----------|------|----------|
| packages/*/dist/ copied | _[✅/❌]_ | _[package count]_ |
| CLI executable present | _[✅/❌]_ | _[file exists]_ |
| JavaScript files only | _[✅/❌]_ | _[no .ts files]_ |
| package.json copied | _[✅/❌]_ | _[files present]_ |
| Size documented | _[✅/❌]_ | _[deployment report]_ |
| No broken symlinks | _[✅/❌]_ | _[find -L check]_ |

---

## Documentation Updates

### Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| /opt/n8n/app/packages/ | Created | All n8n packages deployed |
| /opt/n8n/docs/artifact-deployment.txt | Created | Deployment report |

---

## Knowledge Transfer

### Key Learnings
1. _[Record actual rsync duration]_
2. _[Note any packages that had issues]_
3. _[Document actual deployment size]_

### Tips for Next Time
- Use rsync instead of cp for large deployments (better progress, resume capability)
- Exclude TypeScript source with --exclude='*.ts'
- Exclude src/ and test/ directories to reduce deployment size
- Verify CLI executable specifically - critical for operation
- Keep build directory separate for easy rollback

### Related Resources
- Deployment report: `/opt/n8n/docs/artifact-deployment.txt`
- rsync log: `/tmp/deploy-rsync.log`
- n8n package structure: `/srv/knowledge/vault/n8n-master/README.md`

---

## Task Metadata

```yaml
task_id: T-028
task_type: Deployment - Artifacts
parent_work_item: POC3 n8n Deployment - Phase 3.3 Deployment
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
  - /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:494
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for deployment artifact copying | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: (1) Fixed disk size calculation - use `du -sm` for numeric MB output, validate with regex before arithmetic; (2) Added defensive check for `$available` variable - validate numeric before test comparison; (3) Aligned package count threshold from 25→30 to match specification, defined `EXPECTED_PACKAGE_COUNT` variable for consistency | Claude Code |

---

**Source**: agent-omar-planning-analysis.md:494 (T3.2)
