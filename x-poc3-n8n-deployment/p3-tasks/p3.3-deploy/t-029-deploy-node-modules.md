# Task: Deploy node_modules

**Task ID**: T-029
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
| **Dependencies** | T-028 |
| **Estimated Duration** | 5 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | Yes |

---

## Task Overview

### Objective
Copy node_modules directory from build location to deployment location to provide runtime dependencies for n8n execution.

### Context
The node_modules directory contains all runtime dependencies needed for n8n to execute. This includes over 2000 packages totaling approximately 400-500MB. We copy the entire directory from the build location to ensure n8n has access to all required dependencies when running.

### Success Criteria
- [ ] node_modules copied to /opt/n8n/app/node_modules/
- [ ] All critical dependencies present (@n8n/*, express, typeorm, etc.)
- [ ] Symlinks preserved correctly
- [ ] Directory size approximately 400-500MB
- [ ] No missing or broken dependencies

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local
- [ ] Sudo privileges
- [ ] Write access to /opt/n8n/app/

### Required Resources
- [ ] node_modules from build (T-023 completed)
- [ ] Deployment directory ready (T-028 completed)
- [ ] Sufficient disk space (1GB free minimum)

### Required Knowledge
- [ ] Node.js dependency management
- [ ] Symlink handling in copies

### Blocking Dependencies
- [ ] T-028 - Deploy compiled artifacts (app directory ready)

---

## Detailed Execution Steps

### Step 1: Verify Source node_modules

**Command/Action**:
```bash
echo "=== Verifying Source node_modules ==="

if [ ! -d /opt/n8n/build/node_modules/ ]; then
  echo "❌ node_modules missing from build directory"
  exit 1
fi

size=$(du -sh /opt/n8n/build/node_modules/ | awk '{print $1}')
count=$(ls -1 /opt/n8n/build/node_modules/ | wc -l)

echo "✅ node_modules found"
echo "Size: $size"
echo "Top-level packages: $count"
```

**Expected Output**:
```
✅ node_modules found
Size: 450M
Top-level packages: 2000+
```

**Validation**:
```bash
test -d /opt/n8n/build/node_modules/ && \
echo "✅ Source ready" || echo "❌ Source missing"
```

**If This Fails**:
- Re-run T-023 (Install Dependencies)

---

### Step 2: Copy node_modules

**Command/Action**:
```bash
echo "=== Deploying node_modules ==="
echo "Start: $(date)"

sudo rsync -a --info=progress2 \
  /opt/n8n/build/node_modules/ \
  /opt/n8n/app/node_modules/ 2>&1 | tee /tmp/deploy-node-modules.log

RSYNC_EXIT=$?
echo "End: $(date)"

if [ $RSYNC_EXIT -eq 0 ]; then
  echo "✅ node_modules deployed"
else
  echo "❌ Deployment failed: exit code $RSYNC_EXIT"
  exit 1
fi
```

**Expected Output**:
```
=== Deploying node_modules ===
Start: Thu Nov  7 HH:MM:SS
[rsync progress...]
✅ node_modules deployed
End: Thu Nov  7 HH:MM:SS
```

**Validation**:
```bash
test -d /opt/n8n/app/node_modules/ && \
echo "✅ Deployed" || echo "❌ Failed"
```

**If This Fails**:
- Check disk space: `df -h /opt`
- Retry rsync (will resume)
- Use cp if rsync unavailable

---

### Step 3: Verify Critical Dependencies

**Command/Action**:
```bash
echo "=== Verifying Critical Dependencies ==="

critical=("express" "typeorm" "n8n-workflow" "n8n-core")

for dep in "${critical[@]}"; do
  if [ -d "/opt/n8n/app/node_modules/$dep" ]; then
    echo "✅ $dep present"
  else
    echo "❌ $dep MISSING"
  fi
done
```

**Expected Output**:
```
✅ express present
✅ typeorm present
✅ n8n-workflow present
✅ n8n-core present
```

**Validation**:
```bash
test -d /opt/n8n/app/node_modules/express && \
echo "✅ Dependencies verified"
```

**If This Fails**:
- Re-copy specific dependencies
- Escalate to re-run build phase

---

## Validation & Testing

**Test 1**: Dependency count matches
```bash
built=$(ls -1 /opt/n8n/build/node_modules/ | wc -l)
deployed=$(ls -1 /opt/n8n/app/node_modules/ | wc -l)
echo "Built: $built, Deployed: $deployed"
test "$built" -eq "$deployed" && echo "✅ Match" || echo "⚠️  Mismatch"
```
**Expected Result**: Counts match
**Actual Result**: _[Fill in]_

---

## Rollback Procedure

**Step R1**: Remove node_modules
```bash
sudo rm -rf /opt/n8n/app/node_modules/
```

---

## Results

### Task Outcome
- **Status**: _[COMPLETED/FAILED]_
- **Duration**: _[X min]_

### Success Criteria Results
| Criterion | Met? | Evidence |
|-----------|------|----------|
| node_modules copied | _[✅/❌]_ | _[ls output]_ |
| Critical deps present | _[✅/❌]_ | _[verification]_ |
| Symlinks preserved | _[✅/❌]_ | _[check]_ |

---

## Task Metadata

```yaml
task_id: T-029
task_type: Deployment - Dependencies
parent_work_item: POC3 n8n Deployment - Phase 3.3
assigned_agent: @agent-omar
created_date: 2025-11-07
priority: P1
estimated_duration: 5 minutes
source_documents:
  - agent-omar-planning-analysis.md:495
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

**Source**: agent-omar-planning-analysis.md:495 (T3.3)
