# POC4 CodeRabbit - Prerequisites Specification
**Pre-Implementation Checklist and Requirements (VERIFY-FIRST Methodology)**

**Document Type**: Delivery - Prerequisites Specification
**Created**: 2025-11-10
**Updated**: 2025-11-10 (v2.1 - Global Installation Requirements)
**Project**: POC4 CodeRabbit Integration - Path A (Linter Aggregator)
**Status**: Pre-Implementation

**Version History**:
- v1.0: Initial specification
- v2.0: Corrected to VERIFY-FIRST methodology
- v2.1: Added global installation requirements for all projects

---

## Executive Summary

**Purpose**: Ensure all prerequisites are met before Eric Johnson begins linter aggregator implementation.

**Methodology**: **VERIFY → CHECK → INSTALL → CREATE → VALIDATE**
1. **VERIFY** what already exists in the Hana-X ecosystem (reference architecture docs)
2. **CHECK** versions and configurations of existing services
3. **INSTALL** only what is confirmed missing
4. **CREATE** only new directories/configs needed
5. **VALIDATE** everything is operational

**Architecture Reference**: `/srv/cc/Governance/0.0-governance/0.0.2-Archtecture/0.0.2.2-ecosystem-architecture.md`
**Platform Nodes Reference**: `/srv/cc/Governance/0.0-governance/0.0.2-Archtecture/0.0.2.1-platform-nodes.md`

**Working Server**: `hx-cc-server.hx.dev.local` (192.168.10.224)
- **Role**: Claude Code systems integrator & knowledge hub
- **Status**: ✅ Active
- **Target Path**: `/srv/cc/hana-x-infrastructure/`
- **CodeRabbit CLI Installation**: Install HERE on 192.168.10.224 (NOT on .228)
- **Global Installation Requirement**: CodeRabbit MUST be globally accessible at `/usr/local/bin/coderabbit`
- **Access Requirement**: ALL projects (current and future) on hx-cc-server must access CodeRabbit WITHOUT PATH modifications

**IMPORTANT**:
- ✅ hx-cc-server (192.168.10.224) ← Install CodeRabbit CLI HERE (globally accessible)
- ❌ hx-coderabbit-server (192.168.10.228) ← MCP server already deployed (do NOT install CLI here)
- ✅ `/usr/local/bin/coderabbit` ← Global installation path (ALL projects can access)

**Estimated Time**: 2-4 hours (Phase 0 - reduced due to existing Hana-X infrastructure)

---

## Prerequisites Checklist

### Section 1: Infrastructure Verification (Existing Services)

#### 1.1 Verify Hana-X Ecosystem Services (Already Deployed)
**Owner**: William Taylor
**Status**: ⏳ TO BE VERIFIED

**Existing Infrastructure** (from ecosystem architecture):
```
Layer 1 - Identity & Trust (ALL ACTIVE ✅):
- hx-dc-server (192.168.10.200) - Domain Controller
- hx-ca-server (192.168.10.201) - Certificate Authority
- hx-ssl-server (192.168.10.202) - Reverse Proxy
- hx-control-node (192.168.10.203) - Ansible Control

Layer 3 - Data Plane (ALL ACTIVE ✅):
- hx-postgres-server (192.168.10.209) - PostgreSQL
- hx-redis-server (192.168.10.210) - Redis Cache
- hx-qdrant-server (192.168.10.207) - Vector Database
- hx-qdrant-ui-server (192.168.10.208) - Qdrant UI

Layer 4 - Agentic & Toolchain (CODERABBIT MCP ALREADY DEPLOYED ✅):
- hx-coderabbit-server (192.168.10.228) - CodeRabbit MCP (ALREADY EXISTS - NOT installing here)

Layer 6 - Integration (WORKING SERVER - INSTALLING CODERABBIT CLI HERE ✅):
- hx-cc-server (192.168.10.224) - Claude Code (THIS SERVER - CodeRabbit CLI installation target)
```

**Verification Tasks**:
- [ ] VERIFY: hx-cc-server (192.168.10.224) is accessible and operational - THIS is where we install CodeRabbit CLI
- [ ] VERIFY: Domain Controller (hx-dc-server) is reachable
- [ ] VERIFY: Redis (hx-redis-server) is operational
- [ ] VERIFY: PostgreSQL (hx-postgres-server) is operational
- [ ] NOTE: hx-coderabbit-server (192.168.10.228) already exists (MCP server) - no action needed

**Verification Commands**:
```bash
# Run on hx-cc-server (192.168.10.224) - THIS is where we install CodeRabbit CLI
hostname  # Should show: hx-cc-server.hx.dev.local
ip addr | grep "192.168.10.224"  # Confirm we're on the correct server

# Verify domain services
ping -c 2 hx-dc-server.hx.dev.local
ping -c 2 hx-redis-server.hx.dev.local
ping -c 2 hx-postgres-server.hx.dev.local

# Verify network connectivity
curl -I https://api.coderabbit.ai  # CodeRabbit API access (external)
```

**Expected Result**: All infrastructure services respond (already deployed per architecture)

**Deliverable**: Confirmation that Hana-X ecosystem services are operational

---

#### 1.2 Verify hx-cc-server System Environment
**Owner**: William Taylor
**Status**: ⏳ TO BE VERIFIED

**Requirements**:
- [ ] VERIFY: Ubuntu version (22.04 LTS or newer)
- [ ] VERIFY: Python version (3.11+ expected)
- [ ] VERIFY: pip installed
- [ ] VERIFY: Git installed
- [ ] VERIFY: Disk space available in `/srv/cc/` (10GB+)
- [ ] VERIFY: Memory available (4GB+)
- [ ] VERIFY: Internet access operational

**Verification Commands**:
```bash
# Run on hx-cc-server
lsb_release -a              # Check Ubuntu version
python3 --version           # Check Python version
pip3 --version              # Check pip
git --version               # Check Git
df -h /srv/cc/             # Check disk space
free -h                     # Check memory
ping -c 3 8.8.8.8          # Check internet
```

**Expected Output**:
```
Ubuntu: 22.04 LTS or newer
Python: 3.11.x or newer (likely already installed)
pip: 23.x or newer
Git: 2.x or newer
Disk: At least 10GB free in /srv/cc/
Memory: At least 4GB available
Network: Successful ping
```

**Deliverable**: System environment verification report

---

### Section 2: Python Linters Verification/Installation

#### 2.1 CHECK if Python Linters Already Installed
**Owner**: William Taylor
**Status**: ⏳ TO BE CHECKED

**Linters Required** (6 total):
1. `bandit` (security scanning)
2. `pylint` (code quality)
3. `mypy` (type checking)
4. `radon` (complexity metrics)
5. `black` (code formatting)
6. `pytest` + `pytest-cov` (test coverage)

**CHECK Commands** (run BEFORE installing):
```bash
# Run on hx-cc-server
# Check each linter individually
bandit --version 2>/dev/null && echo "✅ bandit installed" || echo "❌ bandit NOT installed"
pylint --version 2>/dev/null && echo "✅ pylint installed" || echo "❌ pylint NOT installed"
mypy --version 2>/dev/null && echo "✅ mypy installed" || echo "❌ mypy NOT installed"
radon --version 2>/dev/null && echo "✅ radon installed" || echo "❌ radon NOT installed"
black --version 2>/dev/null && echo "✅ black installed" || echo "❌ black NOT installed"
pytest --version 2>/dev/null && echo "✅ pytest installed" || echo "❌ pytest NOT installed"
```

**Decision Point**:
- **IF** linter exists: Check version meets minimum requirements
- **IF NOT** linter exists: Proceed to installation step

**Deliverable**: List of linters that need installation

---

#### 2.2 Install Missing Python Linters (ONLY IF NEEDED)
**Owner**: William Taylor
**Status**: ⏳ CONDITIONAL (only if 2.1 shows missing linters)

**Installation Command** (ONLY run if linters are missing):
```bash
# Run on hx-cc-server (only if CHECK showed missing linters)
pip3 install --break-system-packages \
    bandit \
    pylint \
    mypy \
    radon \
    black \
    pytest \
    pytest-cov
```

**Minimum Versions Required**:
- bandit: 1.7.5+
- pylint: 3.0.0+
- mypy: 1.7.0+
- radon: 6.0.0+
- black: 23.0.0+
- pytest: 7.4.0+
- pytest-cov: 4.1.0+

**Post-Installation Verification**:
```bash
# Verify all linters operational
bandit --version
pylint --version
mypy --version
radon --version
black --version
pytest --version
```

**Deliverable**: All 6 linters installed and verified operational

---

#### 2.3 System Dependencies Check
**Owner**: William Taylor
**Status**: ⏳ TO BE CHECKED

**CHECK for System Dependencies**:
```bash
# Run on hx-cc-server
# Check if build tools exist
gcc --version 2>/dev/null && echo "✅ gcc installed" || echo "❌ gcc NOT installed"
python3-dev --version 2>/dev/null || dpkg -l | grep python3-dev && echo "✅ python3-dev installed" || echo "❌ python3-dev NOT installed"
jq --version 2>/dev/null && echo "✅ jq installed" || echo "❌ jq NOT installed"
```

**Install ONLY if Missing**:
```bash
# ONLY run if CHECK shows missing packages
sudo apt-get update
sudo apt-get install -y build-essential python3-dev jq
```

**Deliverable**: System dependencies verified/installed

---

### Section 3: CodeRabbit CLI Verification/Installation (Layer 3)

#### 3.1 CHECK if CodeRabbit CLI Already Installed (GLOBAL ACCESS)
**Owner**: Carlos Martinez
**Status**: ⏳ TO BE CHECKED

**CRITICAL CLARIFICATION**:
- **Installing on**: hx-cc-server (192.168.10.224) ← CodeRabbit CLI goes HERE
- **NOT installing on**: hx-coderabbit-server (192.168.10.228) ← MCP server (already deployed)
- **Global Requirement**: MUST be accessible at `/usr/local/bin/coderabbit` for ALL projects

**CHECK Commands**:
```bash
# Run on hx-cc-server (192.168.10.224)
# Check if globally accessible (without PATH modifications)
coderabbit --version 2>/dev/null && echo "✅ CodeRabbit CLI globally installed" || echo "❌ CodeRabbit CLI NOT globally installed"

# Verify global location
which coderabbit
# Expected: /usr/local/bin/coderabbit

# Verify symlink target (if global install exists)
ls -la /usr/local/bin/coderabbit
# Expected: /usr/local/bin/coderabbit -> /home/agent0/.local/bin/coderabbit
```

**Decision Point**:
- **IF** globally installed at `/usr/local/bin/coderabbit`: Verify authentication status
- **IF NOT** globally installed: Proceed to installation step

**Deliverable**: CodeRabbit CLI global installation status report

---

#### 3.2 Install CodeRabbit CLI with Global Access (ONLY IF NEEDED)
**Owner**: Carlos Martinez
**Status**: ⏳ CONDITIONAL (only if 3.1 shows NOT globally installed)

**Installation Target**: hx-cc-server (192.168.10.224) ONLY
**Global Requirement**: MUST create symlink at `/usr/local/bin/coderabbit` for ALL projects to access

**Installation Commands** (ONLY if CLI not globally accessible):
```bash
# Step 1: Install CodeRabbit CLI (installs to /home/agent0/.local/bin/)
# Run on hx-cc-server (192.168.10.224) - NOT on .228
curl -fsSL https://cli.coderabbit.ai/install.sh | sh

# Step 2: Create global symlink (REQUIRED for all projects to access)
sudo ln -sf /home/agent0/.local/bin/coderabbit /usr/local/bin/coderabbit

# Step 3: Verify global installation
which coderabbit
# Expected output: /usr/local/bin/coderabbit

# Step 4: Verify version accessible globally (without PATH modifications)
coderabbit --version
# Expected output: 0.3.4 (or current version)

# Step 5: Test from any directory (confirms global access)
cd /tmp && coderabbit --version && cd - && echo "✅ Global access confirmed"
```

**Expected Outcome**:
- ✅ Binary installed at: `/home/agent0/.local/bin/coderabbit`
- ✅ Global symlink at: `/usr/local/bin/coderabbit`
- ✅ Accessible from ANY project directory without PATH modifications
- ✅ Version command works globally

**Deliverable**: CodeRabbit CLI installed with global access for all current and future projects

---

#### 3.3 Verify/Configure CodeRabbit Authentication (Global Access)
**Owner**: Carlos Martinez
**Status**: ⏳ TO BE VERIFIED

**Server**: hx-cc-server (192.168.10.224) - Configure authentication HERE
**Global Requirement**: Authentication must work from ANY project directory

**API Key** (from research docs):
```
cr-fe13e8590657e79c8ba231c3591afcd97b61e4395e79b0adf34aa1eb7c
```

**CHECK Current Authentication**:
```bash
# Run on hx-cc-server (192.168.10.224)
# Test from any directory to verify global access
coderabbit config show 2>/dev/null && echo "✅ Already authenticated" || echo "❌ Need authentication"
```

**Configure Authentication** (ONLY if needed):
```bash
# All commands run on hx-cc-server (192.168.10.224)

# Step 1: Set API key environment variable
export CODERABBIT_API_KEY="cr-fe13e8590657e79c8ba231c3591afcd97b61e4395e79b0adf34aa1eb7c"

# Step 2: Run interactive authentication (OAuth - requires browser)
coderabbit auth login

# Step 3: Verify authentication works globally
coderabbit config show

# Step 4: Test global access from different directories
cd /srv/cc/Governance/x-poc4-coderabbit/0.1-Planning && coderabbit --version && cd -
cd /tmp && coderabbit --version && cd -
echo "✅ Global access confirmed from multiple directories"

# Step 5: Test review functionality
coderabbit review --cwd /srv/cc/Governance/x-poc4-coderabbit/0.1-Planning --plain --type uncommitted
```

**Expected Outcome**:
- ✅ Authentication works from any directory
- ✅ No PATH modifications required
- ✅ All current and future projects can access CodeRabbit
- ✅ Review command functional

**Deliverable**: CodeRabbit CLI authenticated and globally accessible from all project directories

---

### Section 4: Directory Structure Verification/Creation

#### 4.1 CHECK if Directory Structure Already Exists
**Owner**: William Taylor
**Status**: ⏳ TO BE CHECKED

**CHECK Commands**:
```bash
# Run on hx-cc-server
ls -la /srv/cc/hana-x-infrastructure/ && echo "✅ Base directory exists" || echo "❌ Base directory NOT exists"
ls -la /srv/cc/hana-x-infrastructure/.claude/agents/roger/ && echo "✅ Roger directory exists" || echo "❌ Roger directory NOT exists"
```

**Expected Structure** (target):
```
/srv/cc/hana-x-infrastructure/
├── .claude/
│   └── agents/
│       └── roger/
│           ├── configs/       (linter config files)
│           ├── cache/         (CodeRabbit API cache)
│           ├── logs/          (execution logs)
│           └── linter_aggregator.py (Eric creates this)
└── bin/
    └── lint-all              (Eric creates this)
```

**Deliverable**: Directory status report (exists or needs creation)

---

#### 4.2 Create Missing Directory Structure (ONLY IF NEEDED)
**Owner**: William Taylor
**Status**: ⏳ CONDITIONAL (only if 4.1 shows missing dirs)

**Creation Commands** (ONLY run if directories don't exist):
```bash
# Run on hx-cc-server as sudo
sudo mkdir -p /srv/cc/hana-x-infrastructure/.claude/agents/roger/{configs,cache,logs}
sudo mkdir -p /srv/cc/hana-x-infrastructure/bin

# Set ownership (assuming 'agent0' user)
sudo chown -R agent0:agent0 /srv/cc/hana-x-infrastructure/.claude/agents/roger
sudo chown -R agent0:agent0 /srv/cc/hana-x-infrastructure/bin

# Set permissions
sudo chmod 755 /srv/cc/hana-x-infrastructure/.claude/agents/roger
sudo chmod 755 /srv/cc/hana-x-infrastructure/.claude/agents/roger/configs
sudo chmod 755 /srv/cc/hana-x-infrastructure/.claude/agents/roger/cache
sudo chmod 755 /srv/cc/hana-x-infrastructure/.claude/agents/roger/logs
sudo chmod 755 /srv/cc/hana-x-infrastructure/bin

# Verify structure created
tree /srv/cc/hana-x-infrastructure/.claude/agents/roger/
ls -la /srv/cc/hana-x-infrastructure/bin/
```

**Deliverable**: Complete directory structure created with proper permissions

---

### Section 5: Credentials & Secrets Verification

#### 5.1 Verify Password Standards Documentation
**Owner**: Agent Zero
**Status**: ⏳ TO BE VERIFIED

**CHECK Password Pattern Document**:
```bash
# Run on hx-cc-server
cat /srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.2-url-safe-password-pattern.md | head -20
```

**Password Pattern**: `[A-Z][a-z]+[0-9]{4}!`
- Example: `Major8859!`
- Format: Uppercase letter + lowercase letters + 4 digits + exclamation mark

**Deliverable**: Password pattern confirmed and documented

---

#### 5.2 Verify Credentials Documentation Access
**Owner**: Agent Zero
**Status**: ⏳ TO BE VERIFIED

**CHECK Credentials Document**:
```bash
# Run on hx-cc-server
ls -la /srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.1-credentials.md && echo "✅ Accessible" || echo "❌ NOT accessible"
```

**Document Location**: `/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.1-credentials.md`

**Usage**: All new credentials MUST be documented in this file immediately upon creation

**Deliverable**: Credentials document access confirmed

---

#### 5.3 Document CodeRabbit API Key
**Owner**: Carlos Martinez
**Status**: ⏳ TO BE DOCUMENTED

**API Key** (current):
```
cr-fe13e8590657e79c8ba231c3591afcd97b61e4395e79b0adf34aa1eb7c
```

**Action**: Add to credentials document if not already present

**Environment Configuration**:
```bash
# Add to /etc/environment or user's ~/.bashrc
export CODERABBIT_API_KEY="cr-fe13e8590657e79c8ba231c3591afcd97b61e4395e79b0adf34aa1eb7c"
```

**Deliverable**: API key documented in credentials file and configured in environment

---

### Section 6: Service Account Verification

#### 6.1 Verify System User Account
**Owner**: William Taylor
**Status**: ⏳ TO BE VERIFIED

**CHECK Current User**:
```bash
# Run on hx-cc-server
whoami                                 # Check current user
groups                                 # Check group membership
ls -la /srv/cc/hana-x-infrastructure/ # Check directory access
```

**Expected User**: `agent0` (or equivalent with proper permissions)

**Verify User Permissions**:
```bash
# Check user can execute linters
which bandit pylint mypy radon black pytest

# Check user can write to target directories
touch /srv/cc/hana-x-infrastructure/test.txt && rm /srv/cc/hana-x-infrastructure/test.txt && echo "✅ Write access" || echo "❌ NO write access"
```

**Deliverable**: User account confirmed with proper permissions

---

#### 6.2 Determine Service Account Need
**Owner**: Frank Lucas (minimal involvement)
**Status**: ⏳ TO BE DETERMINED

**Decision Point**: Is a domain service account needed for CodeRabbit Layer 3?

**CHECK if service account already exists**:
```bash
# Run on hx-dc-server or query from hx-cc-server
ldapsearch -x -H ldap://hx-dc-server.hx.dev.local -b "DC=hx,DC=dev,DC=local" "(sAMAccountName=roger_service)" 2>/dev/null && echo "✅ roger_service exists" || echo "❌ roger_service NOT exists"
```

**Likely Answer**: **NO** - API key is sufficient for Phase 1 (Layer 3 integration uses API key, not domain authentication)

**Deliverable**: Confirmation that API key is sufficient (no service account needed for Phase 1)

---

### Section 7: Testing Environment Verification

#### 7.1 Verify Test Suite Files Exist
**Owner**: Julia Santos
**Status**: ⏳ TO BE VERIFIED

**CHECK Test Directory**:
```bash
# Run on hx-cc-server
ls -la /srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/

# Check test files
ls -la /srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test_*.py

# Count tests
pytest /srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/ --collect-only 2>/dev/null | grep "test session starts"
```

**Expected Output**:
- Test directory exists with all test files
- 113 tests collected (from Julia's expanded test suite)
- All fixtures and mocks present

**Deliverable**: Test environment verified ready

---

#### 7.2 Verify pytest Installation
**Owner**: Julia Santos
**Status**: ⏳ TO BE VERIFIED

**CHECK pytest**:
```bash
# Run on hx-cc-server
pytest --version && pytest-cov --version
```

**If Missing** (install):
```bash
pip3 install --break-system-packages pytest pytest-cov pytest-mock
```

**Deliverable**: pytest operational

---

### Section 8: Network & Connectivity Verification

#### 8.1 Verify Network Access to Hana-X Services
**Owner**: William Taylor
**Status**: ⏳ TO BE VERIFIED

**VERIFY Connectivity**:
```bash
# Run on hx-cc-server
# Test Redis (already deployed)
redis-cli -h hx-redis-server.hx.dev.local ping && echo "✅ Redis reachable" || echo "❌ Redis NOT reachable"

# Test PostgreSQL (already deployed)
psql -h hx-postgres-server.hx.dev.local -U postgres -c "SELECT version();" && echo "✅ PostgreSQL reachable" || echo "❌ PostgreSQL NOT reachable"

# Test CodeRabbit API (external)
curl -I https://api.coderabbit.ai && echo "✅ CodeRabbit API reachable" || echo "❌ CodeRabbit API NOT reachable"

# Test PyPI (for future package installs)
curl -I https://pypi.org && echo "✅ PyPI reachable" || echo "❌ PyPI NOT reachable"
```

**Deliverable**: Network connectivity report

---

### Section 9: Git Repository Verification

#### 9.1 Verify Git Repository Configuration
**Owner**: Agent Zero
**Status**: ⏳ TO BE VERIFIED

**CHECK Git Repository**:
```bash
# Run on hx-cc-server
cd /srv/cc/Governance/
git status                   # Check if git repo initialized
git branch                   # Check current branch
cat .gitignore | head -20   # Check .gitignore exists
```

**Verify .gitignore Contents** (should exclude):
```
# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
.pytest_cache/
.coverage
coverage.json

# Linter Aggregator (add if missing)
/srv/cc/hana-x-infrastructure/.claude/agents/roger/cache/
/srv/cc/hana-x-infrastructure/.claude/agents/roger/logs/

# Secrets
*.env
*credentials*
*secrets*
```

**Deliverable**: Git repository configuration verified

---

## Prerequisites Task Assignment Matrix

| # | Task | Owner | Priority | Duration | Action |
|---|------|-------|----------|----------|--------|
| 1 | Verify Hana-X services operational | William Taylor | P0 | 15 min | VERIFY |
| 2 | Verify hx-cc-server environment | William Taylor | P0 | 15 min | VERIFY |
| 3 | CHECK if linters already installed | William Taylor | P0 | 10 min | CHECK |
| 4 | Install missing linters (if needed) | William Taylor | P0 | 30 min | CONDITIONAL |
| 5 | CHECK system dependencies | William Taylor | P0 | 10 min | CHECK |
| 6 | Install missing dependencies (if needed) | William Taylor | P0 | 15 min | CONDITIONAL |
| 7 | CHECK CodeRabbit CLI globally installed | Carlos Martinez | P1 | 5 min | CHECK |
| 8 | Install CodeRabbit CLI with global symlink (if needed) | Carlos Martinez | P1 | 15 min | CONDITIONAL |
| 9 | Verify CodeRabbit global authentication | Carlos Martinez | P1 | 15 min | VERIFY |
| 10 | Test CodeRabbit CLI from multiple directories | Carlos Martinez | P1 | 10 min | VALIDATE |
| 11 | CHECK directory structure exists | William Taylor | P0 | 5 min | CHECK |
| 12 | Create missing directories (if needed) | William Taylor | P0 | 10 min | CONDITIONAL |
| 13 | Verify test environment | Julia Santos | P1 | 15 min | VERIFY |
| 14 | Verify pytest installed | Julia Santos | P1 | 5 min | VERIFY |
| 15 | Verify password standards doc | Agent Zero | P2 | 10 min | VERIFY |
| 16 | Verify credentials doc accessible | Agent Zero | P2 | 5 min | VERIFY |
| 17 | Document CodeRabbit API key | Carlos Martinez | P2 | 10 min | DOCUMENT |
| 18 | Verify network connectivity | William Taylor | P2 | 10 min | VERIFY |
| 19 | Verify Git repository config | Agent Zero | P2 | 10 min | VERIFY |
| 20 | Verify user account permissions | William Taylor | P2 | 10 min | VERIFY |
| 21 | Determine service account need | Frank Lucas | P3 | 15 min | DETERMINE |

**Total Duration**: 2-4 hours (many tasks are verification only; installations are conditional)

**Key Principle**: **VERIFY BEFORE ACTION** - Most tasks should complete quickly if infrastructure already exists

---

## Prerequisites Verification Checklist

### Phase 0 Go/No-Go Gates

#### Gate 1: Infrastructure Verified (After 1 hour)
- [ ] hx-cc-server operational
- [ ] Hana-X ecosystem services reachable (Redis, PostgreSQL, CodeRabbit MCP)
- [ ] Python 3.11+ verified
- [ ] System environment verified

**Decision**: Can proceed to Gate 2

---

#### Gate 2: Tools Verified/Installed (After 2 hours)
- [ ] All 6 linters verified operational (or installed if missing)
- [ ] CodeRabbit CLI verified operational (or installed if missing)
- [ ] System dependencies verified/installed
- [ ] Directory structure verified/created

**Decision**: Can proceed to Gate 3

---

#### Gate 3: Testing & Documentation Verified (After 2.5 hours)
- [ ] Test environment verified (113 tests ready)
- [ ] pytest operational
- [ ] Password standards confirmed
- [ ] Credentials doc accessible
- [ ] Network connectivity verified
- [ ] Git repository configured
- [ ] CodeRabbit API key documented

**Decision**: Ready for Eric to begin implementation

---

## Prerequisites Completion Report Template

**Date**: _____________
**Completed By**: _____________

### Infrastructure (William Taylor)
- [ ] Hana-X services verified: ✅ / ❌
- [ ] hx-cc-server environment verified: ✅ / ❌
- [ ] 6 linters verified/installed: ✅ / ❌
- [ ] System dependencies verified/installed: ✅ / ❌
- [ ] Directory structure verified/created: ✅ / ❌
- [ ] Network connectivity verified: ✅ / ❌
- [ ] User account permissions verified: ✅ / ❌

### CodeRabbit Layer 3 (Carlos Martinez)
- [ ] CLI globally installed at `/usr/local/bin/coderabbit`: ✅ / ❌
- [ ] Global symlink verified: ✅ / ❌
- [ ] Accessible from all project directories: ✅ / ❌
- [ ] Authentication verified/configured: ✅ / ❌
- [ ] Test successful from multiple directories: ✅ / ❌
- [ ] API key documented: ✅ / ❌

### Testing (Julia Santos)
- [ ] Test environment verified: ✅ / ❌
- [ ] pytest verified operational: ✅ / ❌

### Documentation & Standards (Agent Zero)
- [ ] Password standards confirmed: ✅ / ❌
- [ ] Credentials doc accessible: ✅ / ❌
- [ ] Git configured: ✅ / ❌

### Optional (Frank Lucas)
- [ ] Service account needed: YES / NO
- [ ] Service account created (if needed): ✅ / ❌ / N/A

**Overall Status**: READY / NOT READY

**Blockers** (if any): _____________

**Items Installed** (list what was actually installed vs verified existing):
_____________

**Sign-off**: _____________

---

## Key Changes from Original Plan

**Original Approach** ❌:
- "Install Redis" → WRONG (already deployed as hx-redis-server)
- "Install PostgreSQL" → WRONG (already deployed as hx-postgres-server)
- Assumed nothing exists → WRONG (Hana-X has 30 active servers)
- Local installation with PATH modifications → WRONG (not accessible to all projects)

**Corrected Approach** ✅:
- **VERIFY** Hana-X ecosystem services first
- **CHECK** what's installed on hx-cc-server before installing
- **INSTALL** only confirmed missing components
- **LEVERAGE** existing infrastructure (Redis, PostgreSQL, Domain Controller, etc.)
- **REFERENCE** architecture documents for current state
- **GLOBAL INSTALLATION** CodeRabbit at `/usr/local/bin/coderabbit` for ALL projects
- **NO PATH MODIFICATIONS** required - accessible from any directory
- **ALL PROJECTS** (current and future) can access CodeRabbit without configuration

---

## Next Steps After Prerequisites Complete

1. **Agent Zero**: Confirm all gates passed
2. **Eric Johnson**: Begin linter aggregator implementation (16 hours)
3. **Carlos Martinez**: Begin Layer 3 integration work (15 hours, parallel)
4. **Julia Santos**: Stand by for test execution

---

**Document Version**: 2.1 (VERIFY-FIRST methodology + Global Installation)
**Classification**: Internal - Delivery
**Status**: Pre-Implementation Checklist (Corrected)
**Last Updated**: 2025-11-10 (Added global installation requirements)
**Next Action**: William Taylor begins Phase 0 verification work

**Updates in v2.1**:
- ✅ CodeRabbit CLI must be globally installed at `/usr/local/bin/coderabbit`
- ✅ All projects (current and future) can access without PATH modifications
- ✅ Global symlink required: `/usr/local/bin/coderabbit` → `/home/agent0/.local/bin/coderabbit`
- ✅ Verification steps updated to test global access from multiple directories

---

*VERIFY before you ACT = No wasted effort*
*CHECK what exists = Leverage existing infrastructure*
*INSTALL only missing = Efficient deployment*
*GLOBAL ACCESS = All projects benefit without configuration*
