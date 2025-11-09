# Task: Verify Build Prerequisites

**Task ID**: T-020
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
| **Dependencies** | T-004, T-005, T-006, T-007, T-009, T-010, T-011 |
| **Estimated Duration** | 15 minutes |
| **Actual Duration** | _[Fill in during execution]_ |
| **Systems Affected** | hx-n8n-server.hx.dev.local (192.168.10.215) |
| **Rollback Required** | No |

---

## Task Overview

### Objective
Verify all prerequisite software and system configurations are correctly installed and ready for n8n monorepo build process on hx-n8n-server.

### Context
The n8n monorepo build requires exact versions of Node.js (≥22.16.0) and pnpm (10.18.3), along with system build dependencies. This verification task ensures all prerequisites from Phase 3.1 are correctly installed before proceeding with the build, preventing build failures due to missing or incompatible dependencies.

### Success Criteria
- [ ] Node.js version ≥22.16.0 and ≤24.x verified
- [ ] pnpm version 10.18.3 (installed via corepack) verified
- [ ] System build tools (gcc, g++, make, python3) verified
- [ ] Graphics libraries (cairo, pango, pixman) verified
- [ ] PostgreSQL client libraries verified
- [ ] n8n system user exists and is accessible

---

## Prerequisites

### Required Access
- [ ] SSH access to hx-n8n-server.hx.dev.local (192.168.10.215)
- [ ] Sudo privileges on hx-n8n-server
- [ ] Access to terminal as user with sudo rights

### Required Resources
- [ ] All Phase 3.1 prerequisite tasks (T-001 through T-019) completed
- [ ] Server accessible on network
- [ ] Internet connectivity (for future build downloads)

### Required Knowledge
- [ ] Linux command-line operations
- [ ] Node.js version verification
- [ ] Package manager verification
- [ ] System package verification (dpkg, apt)

### Blocking Dependencies
- [ ] T-004 - Provision Ubuntu Server (server must be accessible)
- [ ] T-005 - Install Build Tools (gcc, g++, make must be installed)
- [ ] T-006 - Install Graphics Libraries (cairo, pango must be installed)
- [ ] T-007 - Install PostgreSQL Client (libpq-dev must be installed)
- [ ] T-009 - Install Node.js (Node.js 22.x must be installed)
- [ ] T-010 - Install pnpm (pnpm 10.18.3 via corepack must be installed)
- [ ] T-011 - Create Service User (n8n user must exist)

---

## Detailed Execution Steps

### Step 1: Verify Node.js Installation and Version

**Command/Action**:
```bash
# SSH to hx-n8n-server
ssh agent0@hx-n8n-server.hx.dev.local

# Check Node.js version
node --version
```

**Expected Output**:
```
v22.16.0 (or higher, but less than v25.0.0)
```

**Validation**:
```bash
# Verify Node.js version is in acceptable range (22.x - 24.x)
node -e "const v = parseInt(process.version.slice(1).split('.')[0], 10); if (v >= 22 && v < 25) console.log('✅ Node.js version OK:', process.version); else console.log('❌ Node.js version out of range:', process.version, '- Expected: v22.x-v24.x');"
```

**If This Fails**:
- Check if Node.js is in PATH: `which node`
- Verify installation: `dpkg -l | grep nodejs`
- Re-run T-009 if Node.js not installed or wrong version
- Escalate to @agent-william if Node.js installation issues persist

---

### Step 2: Verify pnpm Installation via Corepack

**Command/Action**:
```bash
# Verify pnpm is installed via corepack
pnpm --version

# Verify corepack is enabled
corepack --version
```

**Expected Output**:
```
10.18.3
0.29.4 (or similar corepack version)
```

**Validation**:
```bash
# Check pnpm was installed via corepack (not npm global install)
which pnpm
# Expected: /usr/bin/pnpm or /usr/local/bin/pnpm (from corepack)

# Verify exact version
pnpm --version | grep -q "10.18.3" && echo "✅ pnpm version correct" || echo "❌ pnpm version mismatch"
```

**If This Fails**:
- Verify corepack is enabled: `corepack enable`
- Check if pnpm was installed globally via npm (WRONG): `npm list -g pnpm`
- If pnpm installed via npm, uninstall it: `npm uninstall -g pnpm`
- Re-run T-010 to install pnpm via corepack
- Escalate to @agent-william if issues persist

---

### Step 3: Verify System Build Tools

**Command/Action**:
```bash
# Verify gcc (C compiler)
gcc --version

# Verify g++ (C++ compiler)
g++ --version

# Verify make
make --version

# Verify python3
python3 --version
```

**Expected Output**:
```
gcc (Ubuntu X.X.X) X.X.X
g++ (Ubuntu X.X.X) X.X.X
GNU Make X.X
Python 3.10.X or 3.12.X
```

**Validation**:
```bash
# Check all build tools exist
for tool in gcc g++ make python3 git curl; do
  which $tool > /dev/null && echo "✅ $tool installed" || echo "❌ $tool MISSING"
done
```

**If This Fails**:
- Verify build-essential package: `dpkg -l | grep build-essential`
- Re-run T-005 if build tools missing
- Install missing packages: `sudo apt install -y build-essential python3 git curl`
- Escalate to @agent-william if persistent issues

---

### Step 4: Verify Graphics Libraries

**Command/Action**:
```bash
# Verify cairo library
pkg-config --modversion cairo

# Verify pango library
pkg-config --modversion pango

# Verify PostgreSQL client library
pg_config --version
```

**Expected Output**:
```
1.18.0 (or similar cairo version)
1.52.0 (or similar pango version)
PostgreSQL X.X.X
```

**Validation**:
```bash
# Verify all required libraries are installed (checks each package individually)
REQUIRED_PACKAGES=(libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev libpixman-1-dev pkg-config libpq-dev)
INSTALLED_COUNT=0
MISSING_PACKAGES=()

for pkg in "${REQUIRED_PACKAGES[@]}"; do
  if dpkg -l | grep "^ii  $pkg " >/dev/null 2>&1; then
    echo "✅ $pkg installed"
    ((INSTALLED_COUNT++))
  else
    echo "❌ $pkg NOT installed"
    MISSING_PACKAGES+=("$pkg")
  fi
done

echo ""
if [ ${#MISSING_PACKAGES[@]} -eq 0 ]; then
  echo "✅ All 8 graphics libraries installed successfully"
else
  echo "❌ Missing ${#MISSING_PACKAGES[@]} package(s): ${MISSING_PACKAGES[*]}"
  exit 1
fi
```

**If This Fails**:
- List installed libraries: `dpkg -l | grep -E 'libcairo|libpango|libpq'`
- Re-run T-006 if libraries missing
- Install missing packages: `sudo apt install -y libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev librsvg2-dev libpixman-1-dev pkg-config libpq-dev`
- Escalate to @agent-william if persistent issues

---

### Step 5: Verify n8n System User

**Command/Action**:
```bash
# Verify n8n user exists
id n8n

# Verify n8n user has correct home directory
getent passwd n8n | grep '/opt/n8n'

# Verify n8n user has no login shell
getent passwd n8n | grep 'nologin'
```

**Expected Output**:
```
uid=XXXX(n8n) gid=XXXX(n8n) groups=XXXX(n8n)
n8n:x:XXXX:XXXX::/opt/n8n:/usr/sbin/nologin
n8n:x:XXXX:XXXX::/opt/n8n:/usr/sbin/nologin
```

**Validation**:
```bash
# Comprehensive n8n user check
if id n8n &>/dev/null && \
   getent passwd n8n | grep -q '/opt/n8n' && \
   getent passwd n8n | grep -q 'nologin'; then
  echo "✅ n8n system user configured correctly"
else
  echo "❌ n8n system user configuration issues"
fi
```

**If This Fails**:
- Check if user exists: `id n8n`
- Re-run T-011 if user missing or misconfigured
- Manually create user if needed: `sudo useradd -r -m -s /usr/sbin/nologin -d /opt/n8n -U n8n`
- Escalate to @agent-william if user creation issues

---

### Step 5a: Verify n8n User File Descriptor Limits (BUILD-003)

**Command/Action**:
```bash
# Verify n8n user file descriptor limits
echo "Checking n8n user ulimits..."
n8n_ulimit=$(sudo -u n8n bash -c 'ulimit -n')
echo "n8n user file descriptors (ulimit -n): $n8n_ulimit"

# Check if adequate (need >=65536 for build)
if [ "$n8n_ulimit" -ge 65536 ]; then
  echo "✅ n8n user ulimit adequate: $n8n_ulimit"
else
  echo "⚠️  n8n user ulimit insufficient: $n8n_ulimit (need >=65536)"
  echo "Setting ulimits in /etc/security/limits.d/n8n.conf..."

  # Create limits configuration
  echo "n8n soft nofile 65536" | sudo tee -a /etc/security/limits.d/n8n.conf
  echo "n8n hard nofile 65536" | sudo tee -a /etc/security/limits.d/n8n.conf

  echo "✅ ulimits configured - will take effect on next login"
fi
```

**Expected Output**:
```
n8n user file descriptors (ulimit -n): 65536
✅ n8n user ulimit adequate: 65536
```

**If This Fails**:
- Verify limits file created: `cat /etc/security/limits.d/n8n.conf`
- Check PAM configuration includes limits: `grep pam_limits /etc/pam.d/common-session`
- May require system reboot for limits to apply
- Escalate to @agent-william if persistent issues

---

### Step 5b: Verify n8n User PATH (BUILD-007)

**Command/Action**:
```bash
# Verify n8n user can access required tools
echo "Verifying n8n user PATH access to build tools..."

# Check PATH
echo "n8n user PATH: $(sudo -u n8n bash -c 'echo $PATH')"

# Verify each required tool accessible
for tool in node pnpm gcc g++ make python3; do
  if sudo -u n8n which $tool >/dev/null 2>&1; then
    tool_path=$(sudo -u n8n which $tool)
    echo "✅ $tool: $tool_path"
  else
    echo "❌ $tool: NOT FOUND in n8n user PATH"
  fi
done
```

**Expected Output**:
```
n8n user PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
✅ node: /usr/local/bin/node
✅ pnpm: /usr/local/bin/pnpm
✅ gcc: /usr/bin/gcc
✅ g++: /usr/bin/g++
✅ make: /usr/bin/make
✅ python3: /usr/bin/python3
```

**If This Fails**:
- Check if tools installed: `which node pnpm gcc`
- Verify /usr/local/bin in n8n PATH
- Add to PATH if needed: Edit /etc/environment or /etc/profile
- Escalate to @agent-william for PATH configuration

---

### Step 5c: Test npm Registry Connectivity (BUILD-008)

**Command/Action**:
```bash
# Test connectivity to npm registry
echo "Testing npm registry connectivity..."
if timeout 10 curl -I https://registry.npmjs.org/ 2>&1 | grep -q "HTTP/[0-9.]\+ 200"; then
  echo "✅ npm registry accessible: https://registry.npmjs.org/"
else
  echo "❌ npm registry UNREACHABLE"
  echo "Build will fail during pnpm install - check network connectivity"
fi

# Also test pnpm store connectivity
echo "Testing pnpm store server..."
if sudo -u n8n timeout 10 pnpm store status >/dev/null 2>&1; then
  echo "✅ pnpm store accessible"
else
  echo "⚠️  pnpm store check failed (may be normal if store empty)"
fi
```

**Expected Output**:
```
Testing npm registry connectivity...
✅ npm registry accessible: https://registry.npmjs.org/
Testing pnpm store server...
✅ pnpm store accessible
```

**If This Fails**:
- Check internet connectivity: `ping -c 3 8.8.8.8`
- Check DNS resolution: `nslookup registry.npmjs.org`
- Check proxy settings if behind corporate firewall
- Test alternative registries: `curl -I https://registry.yarnpkg.com/`
- **DO NOT PROCEED** if registry unreachable - build will fail

---

### Step 6: Create Prerequisites Verification Summary

**Command/Action**:
```bash
# Create verification report
cat > /tmp/build-prereqs-verification.txt << 'EOF'
==============================================
n8n Build Prerequisites Verification Report
Server: hx-n8n-server.hx.dev.local
Date: $(date)
Verified by: @agent-omar
==============================================

Node.js Version:
$(node --version)

pnpm Version:
$(pnpm --version)

Corepack Version:
$(corepack --version)

System Build Tools:
gcc: $(gcc --version | head -1)
g++: $(g++ --version | head -1)
make: $(make --version | head -1)
python3: $(python3 --version)

Graphics Libraries:
cairo: $(pkg-config --modversion cairo)
pango: $(pkg-config --modversion pango)
libpq: $(pg_config --version)

n8n System User:
$(getent passwd n8n)

Disk Space:
$(df -h /opt/n8n | tail -1)

==============================================
All prerequisites verified: ✅ READY FOR BUILD
==============================================
EOF

# Expand variables in the report
bash -c "cat > /tmp/build-prereqs-verification.txt" << EOF
==============================================
n8n Build Prerequisites Verification Report
Server: hx-n8n-server.hx.dev.local
Date: $(date)
Verified by: @agent-omar
==============================================

Node.js Version:
$(node --version)

pnpm Version:
$(pnpm --version)

Corepack Version:
$(corepack --version)

System Build Tools:
gcc: $(gcc --version | head -1)
g++: $(g++ --version | head -1)
make: $(make --version | head -1)
python3: $(python3 --version)

Graphics Libraries:
cairo: $(pkg-config --modversion cairo)
pango: $(pkg-config --modversion pango)
libpq: $(pg_config --version)

n8n System User:
$(getent passwd n8n)

Disk Space:
$(df -h /opt | tail -1)

==============================================
All prerequisites verified: ✅ READY FOR BUILD
==============================================
EOF

# Display report
cat /tmp/build-prereqs-verification.txt
```

**Expected Output**:
```
Complete verification report showing all versions and configurations
```

**Validation**:
```bash
# Save report to documentation
sudo mkdir -p /opt/n8n/docs
sudo cp /tmp/build-prereqs-verification.txt /opt/n8n/docs/build-prereqs-verification-$(date +%Y%m%d).txt
sudo chown n8n:n8n /opt/n8n/docs/build-prereqs-verification-*.txt
```

**If This Fails**:
- Review each failed check individually
- Document which prerequisites are missing
- Coordinate with @agent-william to resolve missing prerequisites
- Do NOT proceed to build phase until all checks pass

---

## Validation & Testing

### Functional Validation

**Test 1**: All prerequisite software versions correct
```bash
# Run comprehensive check
node --version | grep -q 'v2[234]' && \
pnpm --version | grep -q '10.18.3' && \
gcc --version | grep -q 'gcc' && \
pkg-config --modversion cairo > /dev/null && \
echo "✅ All prerequisite software verified" || \
echo "❌ Prerequisite verification failed"
```
**Expected Result**: All checks pass with ✅ message
**Actual Result**: _[Fill in during execution]_

---

### Integration Validation

**Test 1**: n8n user can access build tools
```bash
# Test as n8n user (su requires password, use sudo instead)
sudo -u n8n node --version
sudo -u n8n pnpm --version
sudo -u n8n which gcc
```
**Expected Result**: All commands execute successfully as n8n user
**Actual Result**: _[Fill in during execution]_

---

## Rollback Procedure

**When to Rollback**: Not applicable - this is a verification task only

**No rollback needed** - If verification fails, re-run prerequisite installation tasks (T-004 through T-011)

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
| Node.js ≥22.16.0 verified | _[✅/❌]_ | _[node --version output]_ |
| pnpm 10.18.3 verified | _[✅/❌]_ | _[pnpm --version output]_ |
| Build tools verified | _[✅/❌]_ | _[gcc/g++/make/python3 versions]_ |
| Graphics libraries verified | _[✅/❌]_ | _[pkg-config output]_ |
| PostgreSQL client verified | _[✅/❌]_ | _[pg_config output]_ |
| n8n user exists | _[✅/❌]_ | _[id n8n output]_ |

---

## Knowledge Transfer

### Key Learnings
1. _[Learning 1]_
2. _[Learning 2]_
3. _[Learning 3]_

### Tips for Next Time
- Always verify pnpm was installed via corepack, not npm global install
- Check both software version AND that n8n user can access the tools
- Save verification report for audit trail

### Related Resources
- Planning document: `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md`
- Specification: `/srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/poc3-n8n-deployment-specification.md`
- Prerequisite tasks: `/srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-prereqs/`

---

## Task Metadata

```yaml
task_id: T-020
task_type: Verification
parent_work_item: POC3 n8n Deployment - Phase 3.2 Build
assigned_agent: @agent-omar
created_date: 2025-11-07
completed_date: [YYYY-MM-DD]
status: NOT STARTED
priority: P1 - Critical
execution_type: Sequential
estimated_duration: 15 minutes
actual_duration: [X minutes]
systems_affected: [hx-n8n-server.hx.dev.local (192.168.10.215)]
rollback_performed: no
source_documents:
  - /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md
  - /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/poc3-n8n-deployment-specification.md
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for build prerequisites verification | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Refactored graphics library package validation (lines 202-226) from fragile one-liner (`dpkg -l \| grep \| grep -c '^ii'`) to robust loop-based validation that checks each of 8 packages individually. New approach provides clear per-package status output, identifies specific missing packages, and is more resilient to package state variations (flagged/broken packages). Improves readability and debuggability for operations team. | Claude Code |

---

**Source**: agent-omar-planning-analysis.md:460 (T1.1)
