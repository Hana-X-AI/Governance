# Task: Build n8n Application

**Task ID**: T-024
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
| **Dependencies** | T-023 |
| **Estimated Duration** | 20-30 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | Yes |

---

## Task Overview

### Objective
Execute `pnpm build:deploy` to compile all 30+ packages in the n8n monorepo from TypeScript source to JavaScript distribution files.

### Context
This is the core build step that transforms the n8n source code into executable JavaScript. The build process uses Turbo (monorepo build orchestrator) to compile packages in the correct dependency order. This is the most resource-intensive and time-consuming step in the build phase, typically taking 20-30 minutes depending on server performance.

### Success Criteria
- [ ] `pnpm build:deploy` completes without errors
- [ ] All 30+ packages have `dist/` directories created
- [ ] CLI executable created at `packages/cli/bin/n8n`
- [ ] Build artifacts are JavaScript files (not TypeScript)
- [ ] No compilation errors in build log
- [ ] Build duration logged for performance tracking

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local (192.168.10.215)
- [ ] Sudo privileges on hx-n8n-server
- [ ] Terminal session that won't disconnect (use tmux/screen recommended)

### Required Resources
- [ ] Dependencies installed (from T-023)
- [ ] node_modules/ populated
- [ ] Sufficient CPU and RAM (4GB+ recommended for build, vs 3GB in T-023 install phase)
- [ ] Build log ready at /opt/n8n/logs/build.log

**Note**: Build phase requires 4GB memory (increased from 3GB in T-023) due to TypeScript compilation overhead. Parallel tsc processes for 30+ packages consume 1-1.5GB additional memory beyond dependency installation.

### Required Knowledge
- [ ] TypeScript compilation process
- [ ] Turbo monorepo builds
- [ ] Long-running process monitoring
- [ ] Build error troubleshooting

### Blocking Dependencies
- [ ] T-023 - Install Dependencies (node_modules must be populated)

---

## Detailed Execution Steps

### Step 1: Verify Build Prerequisites

**Command/Action**:
```bash
# Ensure we're in build directory
cd /opt/n8n/build/

# Verify dependencies installed
test -d node_modules && \
echo "✅ node_modules present" || \
(echo "❌ node_modules missing - run T-023 first" && exit 1)

# Check available resources
echo "=== System Resources Before Build ===" | sudo tee -a /opt/n8n/logs/build.log
free -h | sudo tee -a /opt/n8n/logs/build.log
df -h /opt | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
✅ node_modules present
=== System Resources Before Build ===
              total        used        free      shared  buff/cache   available
Mem:           15Gi       2.0Gi        10Gi       100Mi       3.0Gi        12Gi
Filesystem     Size   Used  Avail Use% Mounted on
/dev/sdX       100G    35G    60G  37% /opt
```

**Validation**:
```bash
# Verify sufficient memory (at least 2GB free)
available_mem=$(free -g | awk '/Mem:/ {print $7}')
if [ "$available_mem" -ge 2 ]; then
  echo "✅ Sufficient memory: ${available_mem}GB available" | sudo tee -a /opt/n8n/logs/build.log
else
  echo "⚠️  Low memory: ${available_mem}GB available (2GB+ recommended)" | sudo tee -a /opt/n8n/logs/build.log
fi
```

**If This Fails**:
- Close unnecessary processes to free memory
- Check if other builds running: `ps aux | grep -E 'node|pnpm|turbo'`
- Consider rebooting server if memory very low
- Proceed with caution if <2GB free (build may be slower)

---

### Step 2: Clean Previous Build Artifacts

**Command/Action**:
```bash
# Remove any existing dist directories from previous builds
echo "=== Cleaning Previous Build Artifacts ===" | sudo tee -a /opt/n8n/logs/build.log

# Find and remove all dist directories
find packages/ -type d -name dist -exec rm -rf {} + 2>/dev/null || true

# Verify clean state
dist_count=$(find packages/ -type d -name dist 2>/dev/null | wc -l)
echo "Remaining dist directories: $dist_count" | sudo tee -a /opt/n8n/logs/build.log

if [ "$dist_count" -eq 0 ]; then
  echo "✅ Build artifacts cleaned" | sudo tee -a /opt/n8n/logs/build.log
else
  echo "⚠️  Some dist directories remain (may be locked)" | sudo tee -a /opt/n8n/logs/build.log
fi
```

**Expected Output**:
```
=== Cleaning Previous Build Artifacts ===
Remaining dist directories: 0
✅ Build artifacts cleaned
```

**Validation**:
```bash
# Verify no dist directories exist
test $(find packages/ -type d -name dist 2>/dev/null | wc -l) -eq 0 && \
echo "✅ Clean build state" || \
echo "⚠️  Some artifacts remain"
```

**If This Fails**:
- Use sudo to force remove: `sudo find packages/ -type d -name dist -exec rm -rf {} +`
- Check for processes locking files: `lsof +D /opt/n8n/build/packages/`
- Proceed anyway (build will overwrite)

---

### Step 3: Execute pnpm build:deploy

**Command/Action**:
```bash
# Record start time
BUILD_START=$(date +%s)
echo "=== N8N APPLICATION BUILD STARTED ===" | sudo tee -a /opt/n8n/logs/build.log
echo "Start time: $(date)" | sudo tee -a /opt/n8n/logs/build.log
echo "Command: pnpm build:deploy" | sudo tee -a /opt/n8n/logs/build.log
echo "Expected duration: 20-30 minutes" | sudo tee -a /opt/n8n/logs/build.log
echo "" | sudo tee -a /opt/n8n/logs/build.log

# Execute build with resource limits as n8n user
# systemd-run provides memory limit and CPU quota
# -p MemoryMax=4G: Build phase needs more memory than install phase (3GB in T-023)
#                  TypeScript compilation uses 1-1.5GB additional memory for tsc processes
# -p CPUQuota=80%: Limit to 80% CPU to prevent system starvation
# sudo -u n8n ensures files are owned by n8n:n8n
# NOTE: This will take 20-30 minutes - monitor progress
sudo systemd-run --scope -p MemoryMax=4G -p CPUQuota=80% \
  --uid=n8n --gid=n8n \
  bash -c "cd /opt/n8n/build && pnpm build:deploy" 2>&1 | sudo tee -a /opt/n8n/logs/build.log

# Capture exit code from pnpm (not tee) using PIPESTATUS
BUILD_EXIT_CODE=${PIPESTATUS[0]}

# Calculate duration
BUILD_END=$(date +%s)
BUILD_DURATION=$((BUILD_END - BUILD_START))
BUILD_MINUTES=$((BUILD_DURATION / 60))
BUILD_SECONDS=$((BUILD_DURATION % 60))

# Record completion
echo "" | sudo tee -a /opt/n8n/logs/build.log
echo "=== N8N APPLICATION BUILD COMPLETED ===" | sudo tee -a /opt/n8n/logs/build.log
echo "End time: $(date)" | sudo tee -a /opt/n8n/logs/build.log
echo "Duration: ${BUILD_MINUTES}m ${BUILD_SECONDS}s" | sudo tee -a /opt/n8n/logs/build.log
echo "Exit code: $BUILD_EXIT_CODE" | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
> n8n@1.117.0 build:deploy /opt/n8n/build
> turbo run build --filter=n8n...

• Packages in scope: @n8n/client-oauth2, @n8n/permissions, @n8n/config, ...
• Running build in 30 packages
• Remote caching disabled

@n8n/config:build: cache miss, executing...
@n8n/permissions:build: cache miss, executing...
[... many package builds ...]
n8n:build: cache miss, executing...

 Tasks:    30 successful, 30 total
Cached:    0 cached, 30 total
  Time:    25m30s
```

**Validation**:
```bash
# Check exit code
if [ $BUILD_EXIT_CODE -eq 0 ]; then
  echo "✅ Build completed successfully in ${BUILD_MINUTES}m ${BUILD_SECONDS}s" | sudo tee -a /opt/n8n/logs/build.log
else
  echo "❌ BUILD FAILED with exit code: $BUILD_EXIT_CODE" | sudo tee -a /opt/n8n/logs/build.log
  echo "Duration before failure: ${BUILD_MINUTES}m ${BUILD_SECONDS}s" | sudo tee -a /opt/n8n/logs/build.log
  echo "⚠️  Check /opt/n8n/logs/build.log for errors"
  exit 1
fi
```

**If This Fails**:
- Check for specific error in log: `grep -i "error\|failed" /opt/n8n/logs/build.log | tail -20`
- Common issues:
  - TypeScript compilation errors: Check for syntax errors in source
  - Out of memory: `dmesg | grep -i "out of memory"`
  - Missing dependency: Re-run `pnpm install`
  - Timeout: Increase if server is slow
- **RETRY ONCE** with clean build: `rm -rf packages/*/dist && pnpm build:deploy`
- If second attempt fails, escalate to @agent-zero with:
  - Full build log
  - Error messages
  - System resource status
  - Package that failed (if identifiable)

---

### Step 4: Verify dist Directories Created

**Command/Action**:
```bash
# Count packages with dist directories
echo "=== Build Output Verification ===" | sudo tee -a /opt/n8n/logs/build.log

dist_count=$(find packages/ -type d -name dist | wc -l)
echo "Packages with dist/: $dist_count" | sudo tee -a /opt/n8n/logs/build.log

# List all packages and their dist status
echo "Package Build Status:" | sudo tee -a /opt/n8n/logs/build.log
for pkg_dir in packages/*/; do
  pkg_name=$(basename "$pkg_dir")
  if [ -d "${pkg_dir}dist" ]; then
    file_count=$(find "${pkg_dir}dist" -type f | wc -l)
    echo "  ✅ $pkg_name: $file_count files in dist/" | sudo tee -a /opt/n8n/logs/build.log
  else
    echo "  ❌ $pkg_name: NO dist/ directory" | sudo tee -a /opt/n8n/logs/build.log
  fi
done
```

**Expected Output**:
```
=== Build Output Verification ===
Packages with dist/: 30+
Package Build Status:
  ✅ cli: 450 files in dist/
  ✅ core: 320 files in dist/
  ✅ workflow: 180 files in dist/
  [... more packages ...]
```

**Validation (Fail-Fast)**:
```bash
# Verify all expected packages built (Success Criterion: 30+ packages)
if [ "$dist_count" -ge 30 ]; then
  echo "✅ Build output verified: $dist_count packages compiled" | sudo tee -a /opt/n8n/logs/build.log
else
  echo "❌ INCOMPLETE BUILD: Only $dist_count packages compiled (expected ≥30)" | sudo tee -a /opt/n8n/logs/build.log
  echo "Build FAILED validation - not all packages compiled" | sudo tee -a /opt/n8n/logs/build.log
  echo "Review build log for package-specific errors: /opt/n8n/logs/build.log"
  exit 1
fi
```

**If This Fails**:
- **Check build log**: Review `/opt/n8n/logs/build.log` for compilation errors
- **Identify missing packages**: Compare list above against expected 30+ packages
- **Verify package source**: Ensure missing packages have `src/` directories
- **Check individual package**: Try building specific package: `cd packages/[name] && pnpm build`
- **Investigate errors**: Search build log for package-specific error messages
- **Note**: Some type-only packages may not need `dist/` - verify against n8n source if count is 28-29

---

### Step 5: Verify CLI Executable Created

**Command/Action**:
```bash
# Check for n8n executable
echo "=== CLI Executable Verification ===" | sudo tee -a /opt/n8n/logs/build.log

if [ -f packages/cli/bin/n8n ]; then
  echo "✅ CLI executable found: packages/cli/bin/n8n" | sudo tee -a /opt/n8n/logs/build.log

  # Check if it's executable
  if [ -x packages/cli/bin/n8n ]; then
    echo "✅ Executable permissions set" | sudo tee -a /opt/n8n/logs/build.log
  else
    echo "⚠️  Executable permissions missing - setting now" | sudo tee -a /opt/n8n/logs/build.log
    chmod +x packages/cli/bin/n8n
  fi

  # Show file details
  ls -lh packages/cli/bin/n8n | sudo tee -a /opt/n8n/logs/build.log
else
  echo "❌ CLI executable NOT FOUND" | sudo tee -a /opt/n8n/logs/build.log
  exit 1
fi

# Verify it's a JavaScript wrapper (not TypeScript)
head -5 packages/cli/bin/n8n | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
=== CLI Executable Verification ===
✅ CLI executable found: packages/cli/bin/n8n
✅ Executable permissions set
-rwxr-xr-x 1 n8n n8n 250 Nov  7 HH:MM packages/cli/bin/n8n

#!/usr/bin/env node
[JavaScript code or require() statements]
```

**Validation**:
```bash
# Comprehensive executable check
test -f packages/cli/bin/n8n && \
test -x packages/cli/bin/n8n && \
echo "✅ CLI executable ready" || \
echo "❌ CLI executable issues"
```

**If This Fails**:
- Check if cli package was built: `ls packages/cli/dist/`
- Verify bin directory exists: `ls -la packages/cli/bin/`
- Check build errors for cli package: `grep -A 10 "cli.*error" /opt/n8n/logs/build.log`
- Manually create symlink if needed: Review package.json bin configuration
- Escalate if executable cannot be found or created

---

### Step 6: Calculate Build Statistics

**Command/Action**:
```bash
# Create comprehensive build statistics
cat > /opt/n8n/docs/build-statistics.txt << EOF
==============================================
n8n Build Statistics
Server: hx-n8n-server.hx.dev.local
Build completed: $(date)
Executed by: @agent-omar
==============================================

Build Command: pnpm build:deploy
Exit Code: $BUILD_EXIT_CODE
Duration: ${BUILD_MINUTES}m ${BUILD_SECONDS}s

Package Statistics:
- Total packages in workspace: $(ls -1d packages/*/ | wc -l)
- Packages with dist/: $(find packages/ -type d -name dist | wc -l)
- Total compiled files: $(find packages/*/dist -type f 2>/dev/null | wc -l)

Key Artifacts:
- CLI executable: $(test -f packages/cli/bin/n8n && echo "Present" || echo "Missing")
- Core package: $(test -d packages/core/dist && echo "Built" || echo "Missing")
- Workflow package: $(test -d packages/workflow/dist && echo "Built" || echo "Missing")

Disk Usage:
- Repository size: $(du -sh /opt/n8n/build/ | awk '{print $1}')
- dist/ directories: $(du -sh packages/*/dist 2>/dev/null | awk '{sum+=$1} END {print sum "MB"}' || echo "N/A")

System Resources After Build:
$(free -h)
$(df -h /opt | tail -1)

Build Performance:
- Time per package: $((BUILD_DURATION / dist_count))s average
- Build rate: $(awk "BEGIN {print $dist_count / ($BUILD_DURATION / 60)}")  packages/min

Status: $([ $BUILD_EXIT_CODE -eq 0 ] && echo "✅ SUCCESS" || echo "❌ FAILED")

Next Step: T-025 - Verify Build Output
==============================================
EOF

sudo chown n8n:n8n /opt/n8n/docs/build-statistics.txt

# Display statistics
cat /opt/n8n/docs/build-statistics.txt | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
[Complete build statistics report]
```

**Validation**:
```bash
# Verify statistics created
test -f /opt/n8n/docs/build-statistics.txt && \
echo "✅ Build statistics documented" || \
echo "❌ Statistics documentation failed"
```

**If This Fails**:
- Save to /tmp: `cat > /tmp/build-statistics.txt`
- Copy manually later

---

## Validation & Testing

### Functional Validation

**Test 1**: All critical packages built
```bash
# Verify key packages have dist directories
for pkg in cli core workflow nodes-base editor-ui; do
  test -d "packages/$pkg/dist" && \
  echo "✅ $pkg built" || \
  echo "❌ $pkg MISSING"
done
```
**Expected Result**: All critical packages built
**Actual Result**: _[Fill in during execution]_

---

**Test 2**: Compiled JavaScript files present (not TypeScript)
```bash
# Check that dist contains .js files, not .ts
js_count=$(find packages/cli/dist -name "*.js" | wc -l)
ts_count=$(find packages/cli/dist -name "*.ts" | wc -l)

echo "JavaScript files: $js_count"
echo "TypeScript files: $ts_count"

test "$js_count" -gt 0 && test "$ts_count" -eq 0 && \
echo "✅ Proper compilation to JavaScript" || \
echo "❌ Compilation issues"
```
**Expected Result**: Many .js files, zero .ts files in dist
**Actual Result**: _[Fill in during execution]_

---

### Performance Validation

**Metric 1**: Build duration
- **Target**: 20-30 minutes
- **Actual**: _[${BUILD_MINUTES}m ${BUILD_SECONDS}s]_

**Metric 2**: Packages compiled
- **Target**: 30+ packages
- **Actual**: _[$dist_count packages]_

**Metric 3**: Total compiled files
- **Target**: 5000+ files across all packages
- **Actual**: _[Fill in from find count]_

---

## Rollback Procedure

**When to Rollback**: If build fails, produces incomplete artifacts, or corrupts source

### Rollback Steps

**Step R1**: Remove all dist directories
```bash
cd /opt/n8n/build/
find packages/ -type d -name dist -exec rm -rf {} + 2>/dev/null || true
```
**Validation**: `find packages/ -type d -name dist | wc -l` returns 0

**Step R2**: Clean Turbo cache
```bash
rm -rf .turbo
pnpm store prune
```
**Validation**: Cache cleared

**Step R3**: Verify source code intact
```bash
# Check that TypeScript source still exists
test -d packages/cli/src && \
test -d packages/core/src && \
echo "✅ Source code intact" || \
echo "❌ Source code missing - CRITICAL"
```

**Step R4**: Document build failure
```bash
echo "Build failed at $(date): Exit code $BUILD_EXIT_CODE" | \
sudo tee -a /opt/n8n/docs/build-failures.log

# Copy last 100 lines of build log to failure report
tail -100 /opt/n8n/logs/build.log | \
sudo tee -a /opt/n8n/docs/build-failures.log
```

**Step R5**: Analyze failure and retry
- Review error messages in build.log
- Check system resources (memory, disk)
- Verify all dependencies installed
- Re-run T-023 if dependency issues suspected
- Retry build: `pnpm build:deploy`

---

## Results

### Task Outcome
- **Status**: _[COMPLETED | FAILED | PARTIALLY COMPLETED]_
- **Start Time**: _[HH:MM from build log]_
- **End Time**: _[HH:MM from build log]_
- **Duration**: _[${BUILD_MINUTES}m ${BUILD_SECONDS}s]_
- **Rollback Needed**: _[Yes/No]_

### Success Criteria Results

| Criterion | Met? | Evidence |
|-----------|------|----------|
| pnpm build:deploy completed | _[✅/❌]_ | _[exit code $BUILD_EXIT_CODE]_ |
| All packages have dist/ | _[✅/❌]_ | _[$dist_count packages]_ |
| CLI executable created | _[✅/❌]_ | _[file exists and executable]_ |
| JavaScript artifacts (not TS) | _[✅/❌]_ | _[.js files present]_ |
| No compilation errors | _[✅/❌]_ | _[log review]_ |
| Duration logged | _[✅/❌]_ | _[timestamps in statistics]_ |

---

## Documentation Updates

### Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| packages/*/dist/ | Created | Compiled JavaScript for all packages |
| packages/cli/bin/n8n | Created | CLI executable wrapper |
| /opt/n8n/logs/build.log | Modified | Complete build output logged |
| /opt/n8n/docs/build-statistics.txt | Created | Build performance metrics |

---

## Knowledge Transfer

### Key Learnings
1. _[Record actual build duration and compare to estimate]_
2. _[Note any packages that took exceptionally long]_
3. _[Document any warnings that appeared during build]_

### Tips for Next Time
- Use tmux/screen for long-running builds to prevent SSH disconnection
- Monitor system resources during build (htop in another terminal)
- Turbo caching speeds up subsequent builds significantly
- First build is always longest; incremental builds much faster
- Watch for memory pressure - build can fail if OOM

### Related Resources
- Build log: `/opt/n8n/logs/build.log`
- Statistics: `/opt/n8n/docs/build-statistics.txt`
- Turbo documentation: https://turbo.build/repo/docs
- n8n build documentation: packages/cli/CONTRIBUTING.md

---

## Task Metadata

```yaml
task_id: T-024
task_type: Application Build
parent_work_item: POC3 n8n Deployment - Phase 3.2 Build
assigned_agent: @agent-omar
created_date: 2025-11-07
completed_date: [YYYY-MM-DD]
status: NOT STARTED
priority: P1 - Critical
execution_type: Sequential
estimated_duration: 20-30 minutes
actual_duration: [X minutes]
systems_affected: [hx-n8n-server.hx.dev.local (192.168.10.215)]
rollback_performed: [yes/no]
source_documents:
  - /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:475
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for n8n application build | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Added rationale for 4GB memory limit (vs 3GB in T-023). Documents that TypeScript compilation requires 1-1.5GB additional memory for parallel tsc processes across 30+ packages. Added explanation to prerequisites section (line 56) and inline comments (lines 173-174). | Claude Code |

---

**Source**: agent-omar-planning-analysis.md:475 (T2.2)
