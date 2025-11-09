# Task: Verify Build Output

**Task ID**: T-025
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
| **Dependencies** | T-024 |
| **Estimated Duration** | 10 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | No |

---

## Task Overview

### Objective
Comprehensively verify that the n8n build completed successfully by checking for errors, validating executables, confirming all critical packages compiled, and ensuring build artifacts are production-ready.

### Context
After the 20-30 minute build process, this verification task ensures that the build produced complete, valid, and deployable artifacts. This is a critical quality gate before proceeding to deployment - catching build issues now prevents deployment failures later.

### Success Criteria
- [ ] No build errors found in build log
- [ ] All critical packages (cli, core, workflow, nodes-base, editor-ui) have dist/
- [ ] CLI executable exists and is valid JavaScript
- [ ] Build artifacts contain no TypeScript source files
- [ ] Package manifests (package.json) present in dist/
- [ ] Build completion documented and signed off

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local (192.168.10.215)
- [ ] Read access to /opt/n8n/build/
- [ ] Read access to /opt/n8n/logs/build.log

### Required Resources
- [ ] Build completed (from T-024)
- [ ] Build log at /opt/n8n/logs/build.log
- [ ] Build statistics at /opt/n8n/docs/build-statistics.txt

### Required Knowledge
- [ ] n8n package structure
- [ ] TypeScript/JavaScript compilation outputs
- [ ] Log analysis and error pattern recognition
- [ ] Build artifact validation

### Blocking Dependencies
- [ ] T-024 - Build n8n Application (build must have completed)

---

## Detailed Execution Steps

### Step 1: Check Build Log for Errors

**Command/Action**:
```bash
# Navigate to build directory
cd /opt/n8n/build/

echo "=== BUILD LOG ERROR ANALYSIS ===" | sudo tee -a /opt/n8n/logs/build.log

# Search for error patterns
echo "Searching for errors in build log..." | sudo tee -a /opt/n8n/logs/build.log

# Count different error types
error_count=$(grep -i "error" /opt/n8n/logs/build.log | grep -v "0 errors" | wc -l)
fail_count=$(grep -i "failed" /opt/n8n/logs/build.log | grep -v "0 failed" | wc -l)
warning_count=$(grep -i "warning" /opt/n8n/logs/build.log | wc -l)

echo "Error occurrences: $error_count" | sudo tee -a /opt/n8n/logs/build.log
echo "Failed occurrences: $fail_count" | sudo tee -a /opt/n8n/logs/build.log
echo "Warnings: $warning_count" | sudo tee -a /opt/n8n/logs/build.log
```

**Expected Output**:
```
=== BUILD LOG ERROR ANALYSIS ===
Searching for errors in build log...
Error occurrences: 0
Failed occurrences: 0
Warnings: 10-50 (some warnings acceptable)
```

**Validation**:
```bash
# Analyze error severity
if [ "$error_count" -eq 0 ] && [ "$fail_count" -eq 0 ]; then
  echo "✅ No build errors detected" | sudo tee -a /opt/n8n/logs/build.log
elif [ "$error_count" -le 5 ]; then
  echo "⚠️  Minor errors detected ($error_count) - review manually" | sudo tee -a /opt/n8n/logs/build.log
  grep -i "error" /opt/n8n/logs/build.log | grep -v "0 errors" | tail -10 | sudo tee -a /opt/n8n/logs/build.log
else
  echo "❌ CRITICAL: $error_count errors detected" | sudo tee -a /opt/n8n/logs/build.log
  grep -i "error" /opt/n8n/logs/build.log | grep -v "0 errors" | tail -20 | sudo tee -a /opt/n8n/logs/build.log
  exit 1
fi
```

**If This Fails**:
- Extract actual errors: `grep -i -A 3 "error" /opt/n8n/logs/build.log | less`
- Check for TypeScript compilation errors
- Verify errors are not fatal (some warnings logged as "error" level)
- Review each error to determine if blocking
- Escalate if >5 genuine compilation errors

---

### Step 2: Verify Critical Package Builds

**Command/Action**:
```bash
echo "=== CRITICAL PACKAGE VERIFICATION ===" | sudo tee -a /opt/n8n/logs/build.log

# Define critical packages
critical_packages=("cli" "core" "workflow" "nodes-base" "editor-ui" "design-system")

# Check each critical package
all_critical_ok=true
for pkg in "${critical_packages[@]}"; do
  if [ -d "packages/$pkg/dist" ]; then
    file_count=$(find "packages/$pkg/dist" -type f | wc -l)
    js_count=$(find "packages/$pkg/dist" -name "*.js" | wc -l)
    echo "✅ $pkg: $file_count files ($js_count JavaScript)" | sudo tee -a /opt/n8n/logs/build.log
  else
    echo "❌ $pkg: MISSING dist/ directory" | sudo tee -a /opt/n8n/logs/build.log
    all_critical_ok=false
  fi
done

# Overall critical package status
if [ "$all_critical_ok" = true ]; then
  echo "✅ All critical packages built successfully" | sudo tee -a /opt/n8n/logs/build.log
else
  echo "❌ CRITICAL PACKAGES MISSING - Build incomplete" | sudo tee -a /opt/n8n/logs/build.log
  exit 1
fi
```

**Expected Output**:
```
=== CRITICAL PACKAGE VERIFICATION ===
✅ cli: 450+ files (420+ JavaScript)
✅ core: 320+ files (300+ JavaScript)
✅ workflow: 180+ files (170+ JavaScript)
✅ nodes-base: 2500+ files (2400+ JavaScript)
✅ editor-ui: 850+ files (50+ JavaScript, rest are assets)
✅ design-system: 120+ files (100+ JavaScript)
✅ All critical packages built successfully
```

**Validation**:
```bash
# Quick critical package check
test -d packages/cli/dist && \
test -d packages/core/dist && \
test -d packages/workflow/dist && \
test -d packages/nodes-base/dist && \
echo "✅ Critical packages present" || \
(echo "❌ Critical packages missing" && exit 1)
```

**If This Fails**:
- List which packages are missing
- Check build log for package-specific failures
- Try rebuilding individual package: `cd packages/[name] && pnpm build`
- Check if package.json has build script
- Escalate if core packages (cli, core, workflow) missing

---

### Step 3: Validate CLI Executable

**Command/Action**:
```bash
echo "=== CLI EXECUTABLE VALIDATION ===" | sudo tee -a /opt/n8n/logs/build.log

# Check executable exists
if [ -f packages/cli/bin/n8n ]; then
  echo "✅ CLI executable exists: packages/cli/bin/n8n" | sudo tee -a /opt/n8n/logs/build.log

  # Check permissions
  if [ -x packages/cli/bin/n8n ]; then
    echo "✅ Executable permissions correct" | sudo tee -a /opt/n8n/logs/build.log
  else
    echo "⚠️  Setting executable permissions" | sudo tee -a /opt/n8n/logs/build.log
    chmod +x packages/cli/bin/n8n
  fi

  # Check file type (should be script, not binary)
  file_type=$(file packages/cli/bin/n8n)
  echo "File type: $file_type" | sudo tee -a /opt/n8n/logs/build.log

  # Verify it's a Node.js script
  if head -1 packages/cli/bin/n8n | grep -q "node"; then
    echo "✅ Valid Node.js script" | sudo tee -a /opt/n8n/logs/build.log
  else
    echo "❌ Not a Node.js script" | sudo tee -a /opt/n8n/logs/build.log
  fi

  # Check if it references dist directory
  if grep -q "dist" packages/cli/bin/n8n; then
    echo "✅ References compiled dist/ code" | sudo tee -a /opt/n8n/logs/build.log
  else
    echo "⚠️  May not reference dist/ - review manually" | sudo tee -a /opt/n8n/logs/build.log
  fi

  # Display first 10 lines for manual inspection
  echo "CLI executable content (first 10 lines):" | sudo tee -a /opt/n8n/logs/build.log
  head -10 packages/cli/bin/n8n | sudo tee -a /opt/n8n/logs/build.log

else
  echo "❌ CLI EXECUTABLE MISSING" | sudo tee -a /opt/n8n/logs/build.log
  exit 1
fi
```

**Expected Output**:
```
=== CLI EXECUTABLE VALIDATION ===
✅ CLI executable exists: packages/cli/bin/n8n
✅ Executable permissions correct
File type: packages/cli/bin/n8n: a /usr/bin/env node script text executable
✅ Valid Node.js script
✅ References compiled dist/ code
CLI executable content (first 10 lines):
#!/usr/bin/env node
[require or import statements]
```

**Validation**:
```bash
# Comprehensive executable validation
test -f packages/cli/bin/n8n && \
test -x packages/cli/bin/n8n && \
head -1 packages/cli/bin/n8n | grep -q "node" && \
echo "✅ CLI executable validated" || \
echo "❌ CLI executable validation failed"
```

**If This Fails**:
- Check if cli package built: `ls packages/cli/dist/`
- Verify bin configuration in packages/cli/package.json
- Check build log for cli package errors
- Review Turbo build output for cli
- May need to manually create wrapper script

---

### Step 4: Check for TypeScript Leakage in dist/

**Command/Action**:
```bash
echo "=== TYPESCRIPT SOURCE LEAKAGE CHECK ===" | sudo tee -a /opt/n8n/logs/build.log

# Count TypeScript files in dist directories (should be zero)
ts_in_dist=$(find packages/*/dist -name "*.ts" -not -name "*.d.ts" 2>/dev/null | wc -l)
dts_in_dist=$(find packages/*/dist -name "*.d.ts" 2>/dev/null | wc -l)
js_in_dist=$(find packages/*/dist -name "*.js" 2>/dev/null | wc -l)

echo "JavaScript files (.js): $js_in_dist" | sudo tee -a /opt/n8n/logs/build.log
echo "TypeScript declaration files (.d.ts): $dts_in_dist" | sudo tee -a /opt/n8n/logs/build.log
echo "TypeScript source files (.ts): $ts_in_dist" | sudo tee -a /opt/n8n/logs/build.log

# Validate compilation
if [ "$js_in_dist" -gt 1000 ] && [ "$ts_in_dist" -eq 0 ]; then
  echo "✅ Proper TypeScript compilation (JS present, no TS source in dist)" | sudo tee -a /opt/n8n/logs/build.log
elif [ "$ts_in_dist" -gt 0 ]; then
  echo "⚠️  TypeScript source files found in dist/ - may be intentional" | sudo tee -a /opt/n8n/logs/build.log
  find packages/*/dist -name "*.ts" -not -name "*.d.ts" | head -5 | sudo tee -a /opt/n8n/logs/build.log
else
  echo "❌ Insufficient JavaScript files compiled" | sudo tee -a /opt/n8n/logs/build.log
fi
```

**Expected Output**:
```
=== TYPESCRIPT SOURCE LEAKAGE CHECK ===
JavaScript files (.js): 5000+
TypeScript declaration files (.d.ts): 3000+
TypeScript source files (.ts): 0
✅ Proper TypeScript compilation (JS present, no TS source in dist)
```

**Validation**:
```bash
# Quick TypeScript check
test "$js_in_dist" -gt 1000 && \
test "$ts_in_dist" -eq 0 && \
echo "✅ Compilation verified" || \
echo "⚠️  Compilation anomalies detected"
```

**If This Fails**:
- If .ts files in dist: Check if they're intentional (some packages include source)
- Verify .d.ts files present (type declarations are good)
- If very few .js files: Build may have failed silently
- Review build configuration in tsconfig.json files

---

### Step 5: Verify Package Manifests

**Command/Action**:
```bash
echo "=== PACKAGE MANIFEST VERIFICATION ===" | sudo tee -a /opt/n8n/logs/build.log

# Check that each dist has package.json (for proper module resolution)
manifest_count=0
missing_manifests=0

for pkg_dir in packages/*/; do
  pkg_name=$(basename "$pkg_dir")

  # Check if package has dist
  if [ -d "${pkg_dir}dist" ]; then
    # Some packages copy package.json to dist, others don't - both are valid
    if [ -f "${pkg_dir}dist/package.json" ]; then
      manifest_count=$((manifest_count + 1))
    fi

    # Verify source package.json exists (required)
    if [ ! -f "${pkg_dir}package.json" ]; then
      echo "❌ $pkg_name: Missing source package.json" | sudo tee -a /opt/n8n/logs/build.log
      missing_manifests=$((missing_manifests + 1))
    fi
  fi
done

echo "Packages with dist/package.json: $manifest_count" | sudo tee -a /opt/n8n/logs/build.log
echo "Packages missing source package.json: $missing_manifests" | sudo tee -a /opt/n8n/logs/build.log

if [ "$missing_manifests" -eq 0 ]; then
  echo "✅ All package manifests present" | sudo tee -a /opt/n8n/logs/build.log
else
  echo "❌ Missing package manifests detected" | sudo tee -a /opt/n8n/logs/build.log
fi
```

**Expected Output**:
```
=== PACKAGE MANIFEST VERIFICATION ===
Packages with dist/package.json: 10-15 (not all packages copy manifest)
Packages missing source package.json: 0
✅ All package manifests present
```

**Validation**:
```bash
# Verify critical package manifests
test -f packages/cli/package.json && \
test -f packages/core/package.json && \
test -f packages/workflow/package.json && \
echo "✅ Critical manifests present" || \
echo "❌ Critical manifests missing"
```

**If This Fails**:
- Check which packages missing manifests
- Verify not corrupted: `cat packages/[name]/package.json | python3 -m json.tool`
- Re-clone repository if manifests corrupted (T-021)

---

### Step 6: Create Build Verification Report

**Command/Action**:
```bash
# Generate comprehensive build verification report
cat > /opt/n8n/docs/build-verification-report.md << EOF
# n8n Build Verification Report

**Server**: hx-n8n-server.hx.dev.local (192.168.10.215)
**Verification Date**: $(date)
**Verified by**: @agent-omar
**Task**: T-025 - Verify Build Output

---

## Build Status: $([ "$all_critical_ok" = true ] && [ "$error_count" -eq 0 ] && echo "✅ PASS" || echo "❌ FAIL")

## Error Analysis
- Build errors: $error_count
- Build failures: $fail_count
- Warnings: $warning_count (acceptable)

## Package Compilation
- Total packages built: $(find packages/ -type d -name dist | wc -l)
- Critical packages: $([ "$all_critical_ok" = true ] && echo "✅ All present" || echo "❌ Missing")
  - cli: $(test -d packages/cli/dist && echo "✅" || echo "❌")
  - core: $(test -d packages/core/dist && echo "✅" || echo "❌")
  - workflow: $(test -d packages/workflow/dist && echo "✅" || echo "❌")
  - nodes-base: $(test -d packages/nodes-base/dist && echo "✅" || echo "❌")
  - editor-ui: $(test -d packages/editor-ui/dist && echo "✅" || echo "❌")

## Executable Validation
- CLI executable: $(test -f packages/cli/bin/n8n && echo "✅ Present" || echo "❌ Missing")
- Executable permissions: $(test -x packages/cli/bin/n8n && echo "✅ Set" || echo "❌ Not set")
- Script type: $(head -1 packages/cli/bin/n8n 2>/dev/null | grep -q node && echo "✅ Node.js" || echo "❌ Invalid")

## Compilation Quality
- JavaScript files (.js): $js_in_dist
- TypeScript source (.ts) in dist: $ts_in_dist (should be 0)
- TypeScript declarations (.d.ts): $dts_in_dist

## Package Manifests
- Missing source manifests: $missing_manifests (should be 0)

## Build Artifacts Size
$(du -sh packages/*/dist 2>/dev/null | head -10)

---

## Verification Checklist
- [$([ "$error_count" -eq 0 ] && echo "x" || echo " ")] No build errors
- [$([ "$all_critical_ok" = true ] && echo "x" || echo " ")] All critical packages built
- [$(test -f packages/cli/bin/n8n && echo "x" || echo " ")] CLI executable present
- [$([ "$ts_in_dist" -eq 0 ] && echo "x" || echo " ")] No TypeScript source in dist
- [$([ "$js_in_dist" -gt 1000 ] && echo "x" || echo " ")] Sufficient JavaScript compiled
- [$([ "$missing_manifests" -eq 0 ] && echo "x" || echo " ")] All manifests present

## Sign-Off

**Build Quality**: $([ "$all_critical_ok" = true ] && [ "$error_count" -eq 0 ] && echo "Production-ready" || echo "Requires review")

**Verified by**: @agent-omar
**Signature**: _________________
**Date**: $(date +%Y-%m-%d)

---

## Next Steps
$([ "$all_critical_ok" = true ] && [ "$error_count" -eq 0 ] && echo "✅ Proceed to T-026 - Test Build Executable" || echo "❌ Address build issues before proceeding")

---

**Report Location**: /opt/n8n/docs/build-verification-report.md
**Build Log**: /opt/n8n/logs/build.log
**Build Statistics**: /opt/n8n/docs/build-statistics.txt
EOF

sudo chown n8n:n8n /opt/n8n/docs/build-verification-report.md

# Display report
cat /opt/n8n/docs/build-verification-report.md
```

**Expected Output**:
```
[Complete build verification report with all checks marked ✅]
```

**Validation**:
```bash
# Verify report created
test -f /opt/n8n/docs/build-verification-report.md && \
echo "✅ Verification report created" || \
echo "❌ Report creation failed"
```

**If This Fails**:
- Save to /tmp: `cat > /tmp/build-verification-report.md`
- Copy manually later

---

## Validation & Testing

### Functional Validation

**Test 1**: Build log clean
```bash
grep -i "error" /opt/n8n/logs/build.log | grep -v "0 errors" | wc -l
# Expected: 0
```
**Expected Result**: No errors in build log
**Actual Result**: _[Fill in during execution]_

---

**Test 2**: All critical packages built
```bash
# Quick critical package verification
critical_ok=0
for pkg in cli core workflow nodes-base editor-ui; do
  test -d "packages/$pkg/dist" && critical_ok=$((critical_ok + 1))
done
test "$critical_ok" -eq 5 && echo "✅ 5/5 critical" || echo "❌ Only $critical_ok/5"
```
**Expected Result**: 5/5 critical packages present
**Actual Result**: _[Fill in during execution]_

---

## Rollback Procedure

**When to Rollback**: Not applicable - this is a verification task only

**If Verification Fails**:
- Do NOT proceed to T-026
- Review build log for specific errors
- Re-run T-024 (Build) if correctable issues found
- Escalate to @agent-zero if fundamental build problems

---

## Results

### Task Outcome
- **Status**: _[COMPLETED | FAILED]_
- **Start Time**: _[HH:MM]_
- **End Time**: _[HH:MM]_
- **Duration**: _[X minutes]_
- **Rollback Needed**: No

### Success Criteria Results

| Criterion | Met? | Evidence |
|-----------|------|----------|
| No build errors | _[✅/❌]_ | _[$error_count errors]_ |
| Critical packages built | _[✅/❌]_ | _[all_critical_ok status]_ |
| CLI executable valid | _[✅/❌]_ | _[file exists and executable]_ |
| No TS source in dist | _[✅/❌]_ | _[$ts_in_dist files]_ |
| Package manifests present | _[✅/❌]_ | _[$missing_manifests missing]_ |
| Verification documented | _[✅/❌]_ | _[report created]_ |

---

## Knowledge Transfer

### Key Learnings
1. _[Document any unexpected warnings or errors found]_
2. _[Note which packages took longest to verify]_
3. _[Record any anomalies in build output]_

### Tips for Next Time
- Verify incrementally during build to catch issues early
- Save build log immediately after build completes
- Check critical packages first before full verification
- Some TypeScript declaration files (.d.ts) in dist are normal
- Warnings are generally acceptable unless excessive (>100)

### Related Resources
- Verification report: `/opt/n8n/docs/build-verification-report.md`
- Build log: `/opt/n8n/logs/build.log`
- Build statistics: `/opt/n8n/docs/build-statistics.txt`

---

## Task Metadata

```yaml
task_id: T-025
task_type: Build Verification
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
rollback_performed: no
source_documents:
  - /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:476
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

---

**Source**: agent-omar-planning-analysis.md:476 (T2.3)
