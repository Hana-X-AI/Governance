**Document Type**: Backlog - POC3 n8n Deployment
**Created**: 2025-11-07
**Topic**: Specification Gaps, Build Issues, Deployment Issues
**Purpose**: Track and prioritize 84 issues identified during reviews
**Classification**: Internal

---

# Backlog: POC3 n8n Deployment - All Issues & Gaps

**Last Updated**: 2025-11-07 | **Release/Sprint**: POC3 Phase 3 Execution
**Total Items**: 84 | **Critical**: 7 | **High**: 22 | **Medium**: 29 | **Low**: 26
- Specification Gaps: 35 items (original)
- Build Task Issues: 15 items (Phase 3.2 review)
- Deployment Task Issues: 35 items (Phase 3.3 review)

**Recent Updates**:
- 2025-11-07: CodeRabbit remediation - BI-013 story points +1, BI-020 severity Medium→High
- 2025-11-07: CodeRabbit remediation - DEPLOY-015 tool prerequisite clarification (bash-only option)

## Backlog Summary

| Status | Count | Priority Level |
|--------|-------|----------------|
| 🔴 Ready (Critical - BLOCKERS) | 4 | P0 |
| 📋 Ready (High - Before Execution) | 22 | P1 |
| ⚪ Not Ready (Medium - During/After) | 29 | P2 |
| ⚪ Not Ready (Low - Future) | 26 | P3 |
| ✅ Completed | 3 | P0 (2025-11-07) |

**Updates**:
- Phase 3.2 Build Review: +15 issues (2025-11-07)
- Phase 3.3 Deploy Review: +35 issues (2025-11-07)

## Current Sprint: Phase 4 Execution Preparation

### Sprint Goal
Address all critical and high-priority gaps before Phase 4 execution begins to prevent deployment failures and ensure operational readiness.

### Committed Items (Critical Priority - Must Fix Before Execution)

| ID | Title | Agent | Priority | Story Points | Status |
|----|-------|-------|----------|--------------|--------|
| BI-006 | Document n8n user creation procedure explicitly | @agent-william | P0 | 2 | ✅ Completed |
| BI-024 | Specify 3+ encryption key backup locations | @agent-omar | P0 | 3 | ✅ Completed |
| BI-005 | Expand system dependencies to complete list | @agent-william | P0 | 2 | ✅ Completed |

**Sprint Capacity**: 9 story points (critical fixes)
**Committed**: 7 story points
**Completed**: 7 story points (100% - Ready for Phase 4 Execution)

---

## Product Backlog

### Critical Priority (P0 - Before Execution) ✅ ALL COMPLETED

| ID | Title | Type | Agent | Story Points | Value | Effort | Status |
|----|-------|------|-------|--------------|-------|--------|--------|
| BI-006 | Document n8n user creation procedure | Documentation | @agent-william | 2 | High | Low | ✅ Completed 2025-11-07 |
| BI-024 | Specify encryption key backup locations (3+) | Critical Procedure | @agent-omar | 3 | Critical | Low | ✅ Completed 2025-11-07 |
| BI-005 | Expand system dependencies list | Configuration | @agent-william | 2 | High | Low | ✅ Completed 2025-11-07 |

**Total Critical**: 3 items, 7 story points, 100% completed

---

### High Priority (P1 - During Execution)

| ID | Title | Type | Agent | Story Points | Value | Effort | Dependencies |
|----|-------|------|-------|--------------|-------|--------|--------------|
| BI-013 | Document password expiry policy (1-year) ⚠️ | Documentation | @agent-quinn | 3 | High | Low | None |
| BI-016 | Add privilege validation test | Validation | @agent-quinn | 2 | High | Low | None |
| BI-020 | Provide complete .env template ⚠️ | Deliverable | @agent-omar | 3 | Critical | Medium | None |
| BI-022 | Create first-startup checklist | Validation | @agent-omar | 2 | High | Low | None |
| BI-028 | Provide automated test script | Tool | @agent-julia | 5 | High | Medium | None |
| BI-001 | Specify certificate validity (1 year) | Documentation | @agent-frank | 1 | High | Low | None |

**Total High**: 6 items, 16 story points (updated: BI-013 +1 SP, BI-020 value: Critical)

---

### Medium Priority (P2 - Runbook/Documentation)

| ID | Title | Type | Agent | Story Points | Value | Effort | Dependencies |
|----|-------|------|-------|--------------|-------|--------|--------------|
| BI-004 | Certificate renewal procedure | Documentation | @agent-frank | 3 | Medium | Low | BI-001 |
| BI-010 | Log rotation configuration | Configuration | @agent-william | 2 | Medium | Low | None |
| BI-015 | Database size monitoring | Monitoring | @agent-quinn | 2 | Medium | Low | None |
| BI-021 | Workflow backup/export procedure | Documentation | @agent-omar | 2 | Medium | Low | None |
| BI-023 | Common configuration errors guide | Documentation | @agent-omar | 3 | Medium | Medium | None |
| BI-025 | Build failure recovery procedure | Troubleshooting | @agent-omar | 2 | Medium | Low | None |
| BI-026 | Service restart impact documentation | Documentation | @agent-omar | 1 | Medium | Low | None |
| BI-027 | API key generation pre-documentation | Documentation | @agent-omar | 2 | Medium | Low | None |
| BI-017 | Redis authentication configuration | Security | @agent-samuel | 2 | Medium | Low | None |
| BI-031 | N8N MCP server infrastructure pre-verification | Infrastructure | @agent-olivia | 3 | Medium | Low | None |
| BI-007 | Nginx configuration validation | Validation | @agent-william | 2 | Medium | Low | None |

**Total Medium**: 11 items, 24 story points

---

### Low Priority (P3 - Future Enhancements)

| ID | Title | Type | Agent | Story Points | Value | Effort | Dependencies |
|----|-------|------|-------|--------------|-------|--------|--------------|
| BI-002 | DNS record TTL specification | Configuration | @agent-frank | 1 | Low | Low | None |
| BI-003 | Server hostname DNS record | Configuration | @agent-frank | 1 | Low | Low | None |
| BI-008 | Build progress monitoring | Operational | @agent-william | 2 | Low | Low | None |
| BI-009 | Systemd service security hardening | Security | @agent-william | 2 | Low | Low | None |
| BI-011 | Node.js version pinning strategy | Configuration | @agent-william | 2 | Low | Low | None |
| BI-012 | Database connection timeout config | Configuration | @agent-quinn | 1 | Low | Low | None |
| BI-014 | Connection pool size specification | Configuration | @agent-quinn | 1 | Low | Low | None |
| BI-018 | Redis cache storage documentation | Documentation | @agent-samuel | 2 | Low | Low | None |
| BI-019 | Queue mode decision criteria | Documentation | @agent-samuel | 1 | Low | Low | None |
| BI-029 | Test execution timeline | Documentation | @agent-julia | 1 | Low | Low | None |
| BI-030 | Regression test suite | Testing | @agent-julia | 5 | Low | High | None |
| BI-032 | Phase 2 MCP specification | Planning | @agent-olivia | 8 | Low | High | POC3 Complete |
| BI-033 | MCP decision point in POC3 | Process | @agent-olivia | 1 | Low | Low | None |
| BI-034 | FastMCP gateway coordination | Planning | @agent-olivia | 2 | Low | Low | BI-032 |
| BI-035 | Specification version control | Process | @agent-zero | 1 | Low | Low | None |

**Total Low**: 15 items, 31 story points

---

## Backlog Item Details

### BI-006: Document n8n User Creation Procedure ✅ COMPLETED

**Type**: Documentation Gap
**Priority**: P0 - Critical
**Status**: ✅ Completed (2025-11-07)
**Story Points**: 2
**Business Value**: High (blocks service deployment)
**Technical Complexity**: Low
**Created**: 2025-11-07
**Completed**: 2025-11-07
**Target Release**: Phase 4 Execution (Before Start)

**Description**:
FR-004 mentions "service user" but doesn't specify creation procedure. Without explicit documentation, the n8n systemd service cannot run because the dedicated user doesn't exist.

**Recommendation**:
Add to FR-001 or FR-004:
```markdown
### Service User Creation
Create dedicated system user for n8n service:
```bash
sudo useradd -r -m -s /usr/sbin/nologin -d /opt/n8n -U n8n
```
- User: `n8n` (system account, UID auto-assigned)
- Group: `n8n`
- Home: `/opt/n8n`
- Shell: `/usr/sbin/nologin` (no interactive login)
```

**Acceptance Criteria**:
- [x] User creation command documented in specification FR-004
- [x] Command included in T-011 task file
- [x] User properties (UID, group, home, shell) specified
- [x] Validation steps included

**Resolution**:
Updated specification FR-004 to include: "Service MUST run as dedicated n8n system user created with: `sudo useradd -r -m -s /usr/sbin/nologin -d /opt/n8n -U n8n`."
Task file T-011 already contained complete user creation procedure with validation steps.

**Technical Notes**:
- System user flag `-r` ensures low UID assignment
- No-login shell `/usr/sbin/nologin` prevents interactive access
- Home directory `/opt/n8n` matches application directory
- Group `-U n8n` creates matching group

**Impact**: High - Service cannot run without dedicated user (systemd requirement)

**Agent**: @agent-william

---

### BI-024: Specify 3+ Encryption Key Backup Locations ✅ COMPLETED

**Type**: Critical Procedure Gap
**Priority**: P0 - Critical
**Status**: ✅ Completed (2025-11-07)
**Story Points**: 3
**Business Value**: Critical (data loss prevention)
**Technical Complexity**: Low
**Created**: 2025-11-07
**Completed**: 2025-11-07
**Target Release**: Phase 4 Execution (Before Start)

**Description**:
Spec says "backup encryption key" but doesn't specify how many locations or which ones. n8n encrypts credentials using `N8N_ENCRYPTION_KEY`. Losing encryption key = permanent data loss (all encrypted credentials unrecoverable).

**Recommendation**:
Require 3+ backup locations:
1. Local encrypted storage (`/srv/backups/n8n-encryption-key-YYYYMMDD.txt.gpg`)
2. Password manager (1Password, Bitwarden, etc.)
3. Encrypted cloud storage or offline secure media

**Acceptance Criteria**:
- [x] Minimum 3 backup locations specified
- [x] Backup procedure documented with commands
- [x] Encryption for local backup specified (chmod 600)
- [x] Verification procedure included
- [x] Recovery test procedure documented

**Resolution**:
Updated specification FR-010 to require 3+ secure backup locations:
1. Local encrypted backup at `/opt/n8n/backups/.n8n-encryption-key.backup` (chmod 600, n8n user only)
2. Password manager entry (KeePassXC/1Password/Bitwarden)
3. Offline/cloud secure storage (encrypted USB drive or organization's secure backup system)

**Technical Notes**:
- GPG encryption for local backup: `gpg -c n8n-encryption-key.txt`
- Password manager: Store as secure note with metadata
- Cloud storage: Encrypted archive with strong password
- Offline media: USB drive in secure location

**Impact**: CRITICAL - Single backup failure = permanent data loss

**Agent**: @agent-omar

---

### BI-005: Expand System Dependencies List ✅ COMPLETED

**Type**: Configuration Gap
**Priority**: P0 - Critical
**Status**: ✅ Completed (2025-11-07)
**Story Points**: 2
**Business Value**: High (prevents build failures)
**Technical Complexity**: Low
**Created**: 2025-11-07
**Completed**: 2025-11-07
**Target Release**: Phase 4 Execution (Before Start)

**Description**:
Build dependencies listed as high-level packages (build-essential, python3, cairo, pango) without specific dev packages. Missing dev packages will cause n8n build compilation failures.

**Recommendation**:
Expand to complete list:
```bash
sudo apt install -y \
  build-essential \
  python3 python3-pip \
  git curl ca-certificates \
  libcairo2-dev libpango1.0-dev \
  libjpeg-dev libgif-dev librsvg2-dev \
  libpixman-1-dev \
  pkg-config \
  libpq-dev
```

**Acceptance Criteria**:
- [x] Complete dependency list in specification
- [x] All cairo/pango dev packages specified
- [x] pkg-config included
- [x] libpq-dev included
- [x] Updated in T-005 and T-006 task files

**Resolution**:
Updated specification FR-001 and External Dependencies section with complete list: build-essential, python3, python3-pip, git, curl, ca-certificates, libcairo2-dev, libpango1.0-dev, libjpeg-dev, libgif-dev, librsvg2-dev, libpixman-1-dev, pkg-config, libpq-dev.
Updated task file T-006 to include pkg-config and libpq-dev in installation commands and validation steps.

**Technical Notes**:
- `libcairo2-dev` and `libpango1.0-dev` provide C headers for canvas operations
- `pkg-config` required for build system to find libraries
- `libpq-dev` provides PostgreSQL client headers
- Missing any dev package causes "library not found" compile errors

**Impact**: High - Missing dev packages will cause build compilation failures

**Agent**: @agent-william

---

### BI-013: Document Password Expiry Policy (1-Year) ⚠️ UPDATED

**Type**: Configuration Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 3 (increased from 2 - added service account exception policy)
**Business Value**: High
**Technical Complexity**: Low
**Created**: 2025-11-07
**Updated**: 2025-11-07 (CodeRabbit: Added service account operational concern)
**Target Release**: Phase 4 Execution (During)

**Description**:
PostgreSQL user created but password expiry policy not specified. User correction: All Hana-X credentials have 1-year expiration policy.

**⚠️ CodeRabbit Operational Concern**:
Service accounts (`n8n@hx.dev.local`, `n8n_user` PostgreSQL role) are non-interactive and run unattended. Mandatory annual password rotation creates operational risks:
- Risk of forgotten rotation → service fails unexpectedly
- Operational complexity → requires coordinated rollout (update .env, restart service)
- Downtime risk → if password not updated in .env before rotation

**Recommendation**:
Document password rotation procedure (annual):
```sql
-- Annual password rotation (coordinate with @agent-omar for .env update)
ALTER ROLE n8n_user WITH PASSWORD 'NEW_GENERATED_PASSWORD';
```

**Recommended Service Account Exception Policy**:
```bash
# Samba domain service accounts
samba-tool user setexpiry n8n --noexpiry

# PostgreSQL service roles
ALTER ROLE n8n_user VALID UNTIL 'infinity';
```

**Alternative Security Controls** (if "never expire" not acceptable):
1. Annual Security Review instead of password rotation
2. Application-Managed Secrets (Phase 4: HashiCorp Vault)
3. Certificate-Based Authentication (PostgreSQL SSL client certificates)

**Acceptance Criteria**:
- [ ] 1-year password expiry policy documented
- [ ] Annual rotation procedure created
- [ ] Service account exception policy evaluated and documented
- [ ] Coordination with @agent-omar specified (.env update)
- [ ] Password generation guidelines included
- [ ] Rotation reminder mechanism documented
- [ ] Governance policy update recommended (explicit service account exemption)

**Impact**: Service account password expires after 1 year, n8n loses database access

**Resolution**: Specification updated (v1.1) with service account operational guidance and alternative security controls

**Agent**: @agent-quinn

**Reference**: specification-gaps-and-recommendations.md:191-241 (Gap 13)

---

### BI-016: Add Privilege Validation Test

**Type**: Missing Validation
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 2
**Business Value**: High
**Technical Complexity**: Low
**Created**: 2025-11-07
**Target Release**: Phase 4 Execution (During)

**Description**:
Privileges granted but not validated before n8n startup. Missing CREATE privilege causes TypeORM migration failures at runtime.

**Recommendation**:
Add to pre-deployment validation (AC-003):
```sql
-- Test CREATE privilege
CREATE TABLE privilege_test (id SERIAL);
DROP TABLE privilege_test;
-- Expected: Success (if fails, privileges incorrect)
```

**Acceptance Criteria**:
- [ ] Validation test added to T-019
- [ ] Test creates and drops table successfully
- [ ] Failure handling documented
- [ ] Run before n8n first startup

**Impact**: Missing CREATE privilege causes TypeORM migration failures at runtime

**Agent**: @agent-quinn

---

### BI-020: Provide Complete .env Template ⚠️ SEVERITY UPDATED

**Type**: Missing Deliverable
**Priority**: P1 - High (upgraded from Medium per CodeRabbit feedback)
**Status**: Ready
**Story Points**: 3
**Business Value**: Critical
**Technical Complexity**: Medium
**Created**: 2025-11-07
**Updated**: 2025-11-07 (CodeRabbit: Severity reclassified Medium→High)
**Target Release**: Phase 4 Execution (During)

**Description**:
Spec lists 100+ variables but no template provided. Manual .env creation is error-prone, missing variables cause n8n startup failures.

**⚠️ CodeRabbit Severity Reclassification**:
Gap 20 originally classified as "Medium" severity (line 291), but prioritization section (line 543) lists it as "Critical Priority" item #4, indicating higher impact. Missing .env template directly blocks:
- **Deployment (T-033)**: Cannot create valid .env configuration
- **n8n Startup**: Malformed .env prevents service start
- **Troubleshooting**: Difficult to diagnose missing variable errors

**Justification for High Severity**:
- Missing template directly blocks successful deployment
- Manual .env creation is error-prone (100+ variables)
- Malformed .env complicates troubleshooting when service fails

**Recommendation**:
Create complete .env template with all 100+ variables, comments, and examples.

**Acceptance Criteria**:
- [ ] Template includes all required variables
- [ ] Comments explain each variable purpose
- [ ] Examples provided for complex configurations
- [ ] Organized by category (database, network, security, etc.)
- [ ] Template location documented
- [ ] Critical variables highlighted (encryption key, database password)

**Technical Notes**:
- Template should be in `/srv/cc/Governance/x-poc3-n8n-deployment/x-docs/`
- Include placeholder values that must be replaced
- Validate against n8n source code configuration schema

**Impact**: High - Missing template directly blocks deployment (T-033) and n8n startup; malformed .env prevents service start and complicates troubleshooting

**Resolution**: Severity upgraded from Medium to High; prioritization now consistent with Critical Priority #4 classification

**Agent**: @agent-omar

**Reference**: specification-gaps-and-recommendations.md:290-296 (Gap 20)

---

### BI-022: Create First-Startup Checklist

**Type**: Missing Validation
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 2
**Business Value**: High
**Technical Complexity**: Low
**Created**: 2025-11-07
**Target Release**: Phase 4 Execution (During)

**Description**:
First startup critical but no systematic checklist provided. Missing prerequisites cause startup failures, time wasted troubleshooting.

**Recommendation**:
Create pre-startup checklist:
```markdown
## Pre-Startup Checklist
- [ ] All dependencies installed (Node.js, pnpm, PostgreSQL client)
- [ ] Database connection validated
- [ ] .env file complete (all 100+ variables)
- [ ] Encryption key backed up to 3+ locations
- [ ] Service file syntax validated
- [ ] Nginx configuration tested
- [ ] Firewall rules confirmed
```

**Acceptance Criteria**:
- [ ] Checklist created and documented
- [ ] All prerequisites included
- [ ] Validation commands provided
- [ ] Checklist integrated into execution plan

**Impact**: Missing prerequisites cause startup failures, time wasted troubleshooting

**Agent**: @agent-omar

---

### BI-028: Provide Automated Test Script

**Type**: Missing Tool
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 5
**Business Value**: High
**Technical Complexity**: Medium
**Created**: 2025-11-07
**Target Release**: Phase 4 Execution (During)

**Description**:
All tests documented but no automation script provided. Manual testing is error-prone and time-consuming (2+ hours).

**Recommendation**:
Create test automation script that executes all 10 acceptance criteria tests.

**Acceptance Criteria**:
- [ ] Script executes all 10 acceptance criteria
- [ ] Results clearly displayed (✅/❌)
- [ ] Execution time reduced from 2+ hours to 10-15 minutes
- [ ] Script location documented
- [ ] Usage instructions provided

**Benefit**: Reduces manual testing time from 2+ hours to 10-15 minutes

**Agent**: @agent-julia

---

### BI-001: Specify Certificate Validity (1 Year)

**Type**: Documentation Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 1
**Business Value**: High
**Technical Complexity**: Low
**Created**: 2025-11-07
**Target Release**: Phase 4 Execution (During)

**Description**:
Specification does not define certificate validity period for SSL certificate generation. User correction: All credentials have 1-year expiration per Hana-X policy.

**Recommendation**:
Add "Certificate Validity: 1 year (per Hana-X credential policy)" to FR-005.

**Acceptance Criteria**:
- [ ] Certificate validity documented in specification
- [ ] 1-year period specified
- [ ] Reference to Hana-X credential policy included
- [ ] Renewal reminder documented

**Impact**: Manual decision needed during certificate generation

**Agent**: @agent-frank

---

## Blocked Items

| ID | Title | Blocker | Blocked Since | Action Needed | Owner |
|----|-------|---------|---------------|---------------|-------|
| BI-032 | Phase 2 MCP Specification | POC3 not complete | 2025-11-07 | Complete POC3 deployment | @agent-olivia |
| BI-034 | FastMCP Gateway Coordination | BI-032 not started | 2025-11-07 | Complete BI-032 first | @agent-olivia |

---

## Summary Statistics

### Gaps by Severity

| Severity | Count | Story Points | Percentage |
|----------|-------|--------------|------------|
| **Critical (P0)** | 3 | 7 | 9% |
| **High (P1)** | 6 | 15 | 17% |
| **Medium (P2)** | 11 | 24 | 31% |
| **Low (P3)** | 15 | 31 | 43% |
| **TOTAL** | **35** | **77** | **100%** |

### Gaps by Agent

| Agent | Count | Critical | High | Medium | Low |
|-------|-------|----------|------|--------|-----|
| @agent-frank | 4 | 0 | 1 | 1 | 2 |
| @agent-william | 7 | 2 | 0 | 2 | 3 |
| @agent-quinn | 5 | 0 | 2 | 1 | 2 |
| @agent-samuel | 3 | 0 | 0 | 1 | 2 |
| @agent-omar | 8 | 1 | 3 | 4 | 0 |
| @agent-julia | 3 | 0 | 1 | 0 | 2 |
| @agent-olivia | 4 | 0 | 0 | 1 | 3 |
| @agent-zero | 1 | 0 | 0 | 0 | 1 |
| **TOTAL** | **35** | **3** | **7** | **10** | **15** |

### Gaps by Category

| Category | Count | Story Points |
|----------|-------|--------------|
| Documentation Gaps | 12 | 24 |
| Configuration Gaps | 10 | 18 |
| Missing Requirements | 8 | 20 |
| Missing Validation | 3 | 6 |
| Security Gaps | 2 | 4 |

---

## Prioritization Framework

### Priority Definitions
- **P0 (Critical)**: Must fix BEFORE Phase 4 execution begins - blocks deployment
- **P1 (High)**: Address DURING Phase 4 execution - prevents failures
- **P2 (Medium)**: Add to operational runbook/documentation - improves operations
- **P3 (Low)**: Future enhancements or Phase 2 planning - nice to have

### Value vs Effort Matrix

```
High Value, Low Effort  → P0/P1 (Do First) - 9 items
High Value, High Effort → P1/P2 (Plan Carefully) - 3 items
Low Value, Low Effort   → P2/P3 (Fill Capacity) - 18 items
Low Value, High Effort  → P3/Icebox (Defer) - 5 items
```

---

## Execution Recommendations

### Before Phase 4 Execution (Critical - Must Do)

**Sprint**: Pre-Execution Preparation
**Story Points**: 7
**Timeline**: 2-3 hours

1. ✅ **BI-006**: Document n8n user creation procedure (@agent-william, 2 pts)
2. ✅ **BI-024**: Specify 3+ encryption key backup locations (@agent-omar, 3 pts)
3. ✅ **BI-005**: Expand system dependencies list (@agent-william, 2 pts)

**Definition of Done**: All P0 items completed, specification updated, task files updated

---

### During Phase 4 Execution (High Priority)

**Sprint**: Phase 4 Execution
**Story Points**: 15
**Timeline**: Integrated into execution (no additional time)

4. ✅ **BI-013**: Document password expiry policy (@agent-quinn, 2 pts)
5. ✅ **BI-016**: Add privilege validation test (@agent-quinn, 2 pts)
6. ✅ **BI-020**: Provide complete .env template (@agent-omar, 3 pts)
7. ✅ **BI-022**: Create first-startup checklist (@agent-omar, 2 pts)
8. ✅ **BI-028**: Provide automated test script (@agent-julia, 5 pts)
9. ✅ **BI-001**: Specify certificate validity (@agent-frank, 1 pt)

**Definition of Done**: All P1 items completed during execution, no deployment blockers

---

### After Phase 4 Execution (Medium Priority)

**Sprint**: Operational Documentation
**Story Points**: 24
**Timeline**: 1-2 days (post-deployment)

10-20. All P2 items (operational runbooks, monitoring, troubleshooting guides)

**Definition of Done**: Operational runbook complete, monitoring configured, troubleshooting guide available

---

### Phase 2 / Future (Low Priority)

**Sprint**: Future Enhancements
**Story Points**: 31
**Timeline**: Deferred to Phase 2 or future releases

21-35. All P3 items (future enhancements, Phase 2 planning, automation)

**Definition of Done**: Deferred items documented in Phase 2 specification or future backlog

---

## Backlog Maintenance

### Last Refinement: 2025-11-07
**Refinement By**: @agent-zero (based on 7 specialist agent reviews)

**Items Refined**: All 35 gaps extracted from specification-gaps-and-recommendations.md
**Items Prioritized**: 3 critical, 6 high, 11 medium, 15 low
**Next Refinement**: After Phase 4 completion (review completed items, add new gaps if discovered)

---

## Definition of Ready

A backlog item is "Ready" when:
- [x] Gap extracted from specification review
- [x] Severity and impact assessed
- [x] Recommendation provided
- [x] Story points estimated
- [x] Agent assigned
- [x] Acceptance criteria defined
- [x] No blockers exist for P0/P1 items

**Status**: All 35 items meet Definition of Ready

---

## Definition of Done

A backlog item is "Done" when:
- [ ] Recommendation implemented
- [ ] Documentation updated
- [ ] Specification/task files updated (if applicable)
- [ ] Acceptance criteria validated
- [ ] Agent sign-off received

**Status**: 0/35 items complete (execution not started)

---

**Version**: 1.0
**Maintained By**: @agent-zero
**Related Documents**:
- [specification-gaps-and-recommendations.md](../p2-specification/specification-gaps-and-recommendations.md) - Source of all 35 gaps
- [poc3-n8n-deployment-specification.md](../p2-specification/poc3-n8n-deployment-specification.md) - Original specification
**Classification**: Internal
**Status**: Ready for Execution
**Last Review**: 2025-11-07


---

## Phase 3.2 Build Task Review Issues (NEW - 2025-11-07)

**Source**: Team reviews by @agent-omar, @agent-william, @agent-julia, @agent-alex
**Review Date**: 2025-11-07
**Tasks Reviewed**: T-020 through T-026 (7 build tasks)
**Total Issues Found**: 15

### BUILD-001: Missing Resource Limits on pnpm Processes ✅ IMPLEMENTED

**Type**: Infrastructure/Security Gap
**Priority**: P0 - Critical
**Status**: ✅ **IMPLEMENTED** - Fixed in task templates
**Story Points**: 3
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william, @agent-omar
**Resolution Date**: 2025-11-07

**Description**:
T-023 (Install Dependencies) and T-024 (Build Application) originally ran pnpm without resource limits. Could consume 2-4GB memory, risk OOM kill or service disruption.

**Implementation** (BUILD-FIXES-APPLIED.md):
- **T-023**: Added `systemd-run --scope -p MemoryMax=3G -p CPUQuota=80%` (dependency installation)
- **T-024**: Added `systemd-run --scope -p MemoryMax=4G -p CPUQuota=80%` (TypeScript compilation)

**Rationale for 4G vs 3G** (CodeRabbit clarification):
Build phase (T-024) requires 1GB additional memory beyond install phase (T-023) due to:
- Parallel TypeScript compilation across 30+ packages
- Multiple concurrent tsc processes
- Source map generation and optimization
- 1-1.5GB additional memory consumption during peak compilation

**Evidence**:
- T-023 lines 157-159: systemd-run with 3GB limit (install phase)
- T-024 lines 173-180: systemd-run with 4GB limit + rationale comment (build phase)
- BUILD-FIXES-APPLIED.md documents full implementation

**Tasks Affected**: T-023, T-024 (both updated)

---

### BUILD-002: Commands Run as Wrong User ✅ IMPLEMENTED

**Type**: Infrastructure/Permission Gap
**Priority**: P0 - Critical
**Status**: ✅ **IMPLEMENTED** - Fixed in task templates
**Story Points**: 2
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william, @agent-omar
**Resolution Date**: 2025-11-07

**Description**:
Build commands originally ran as root instead of n8n user. Would create root-owned artifacts blocking deployment phase (T-028 cannot copy to n8n-owned directories).

**Implementation** (BUILD-FIXES-APPLIED.md):
- **T-023**: Added `--uid=n8n --gid=n8n` to systemd-run command
- **T-024**: Added `--uid=n8n --gid=n8n` to systemd-run command

**Evidence**:
- T-023 lines 157-159: Commands run as n8n user via systemd-run
- T-024 lines 175-177: Commands run as n8n user via systemd-run
- BUILD-FIXES-APPLIED.md documents full implementation

**Impact**: Build artifacts now owned by n8n:n8n, deployment phase will succeed

**Tasks Affected**: T-023, T-024 (both updated)

---

### BUILD-003: Missing ulimit Verification ✅ IMPLEMENTED

**Type**: System Configuration Gap
**Priority**: P1 - High
**Status**: ✅ **IMPLEMENTED** - Fixed in task template
**Story Points**: 2
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william
**Resolution Date**: 2025-11-07

**Description**:
Originally no check that n8n user has adequate file descriptor limits (need ≥65536). Build opens thousands of files simultaneously.

**Implementation** (BUILD-FIXES-APPLIED.md):
- **T-020**: Added Step 5a for ulimit verification and automatic configuration

**Evidence**:
- T-020 Step 5a: ulimit verification with automatic limits.d configuration
- BUILD-FIXES-APPLIED.md documents implementation

**Tasks Affected**: T-020 (updated)

---

### BUILD-004: Disk Space Check Inaccurate ✅ IMPLEMENTED

**Type**: Validation Gap
**Priority**: P1 - High
**Status**: ✅ **IMPLEMENTED** - Fixed in task template
**Story Points**: 1
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william
**Resolution Date**: 2025-11-07

**Description**:
T-022 originally used `df -BG` which rounds down (19.9GB → 19GB), causing false negatives.

**Implementation** (BUILD-FIXES-APPLIED.md):
- **T-022**: Changed to KB-based calculation for precision

**Evidence**:
- T-022 Step 1: Disk space check now uses KB calculation
- BUILD-FIXES-APPLIED.md documents fix

**Tasks Affected**: T-022 (updated)

---

### BUILD-005: Exit Codes Captured Incorrectly ✅ IMPLEMENTED

**Type**: Error Handling Gap
**Priority**: P1 - High
**Status**: ✅ **IMPLEMENTED** - Fixed in task templates
**Story Points**: 2
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william
**Resolution Date**: 2025-11-07

**Description**:
Originally used `$?` after pipes which captures `tee` exit code, not pnpm. Build failures could go undetected.

**Implementation** (BUILD-FIXES-APPLIED.md):
- **T-023**: Changed to `${PIPESTATUS[0]}`
- **T-024**: Changed to `${PIPESTATUS[0]}`

**Evidence**:
- T-023: Exit code capture uses PIPESTATUS[0]
- T-024: Exit code capture uses PIPESTATUS[0]
- BUILD-FIXES-APPLIED.md documents fix

**Tasks Affected**: T-023, T-024 (both updated)

---

### BUILD-006: No Resource Monitoring During Build

**Type**: Operational Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 2
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william

**Description**:
20-30 minute build has no CPU/memory/I/O monitoring. Cannot diagnose performance issues.

**Recommendation**:
Background vmstat/iostat during build.

**Tasks Affected**: T-024

---

### BUILD-007: Missing PATH Verification for n8n User ✅ IMPLEMENTED

**Type**: Configuration Gap
**Priority**: P1 - High
**Status**: ✅ **IMPLEMENTED** - Fixed in task template
**Story Points**: 1
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william
**Resolution Date**: 2025-11-07

**Description**:
Originally no verification that n8n user's PATH includes node, pnpm, gcc. Commands could fail with "not found".

**Implementation** (BUILD-FIXES-APPLIED.md):
- **T-020**: Added Step 5b for PATH verification

**Evidence**:
- T-020 Step 5b: PATH verification for all required tools
- BUILD-FIXES-APPLIED.md documents implementation

**Tasks Affected**: T-020 (updated)

---

### BUILD-008: Missing npm Registry Connectivity Test ✅ IMPLEMENTED

**Type**: Validation Gap
**Priority**: P1 - High
**Status**: ✅ **IMPLEMENTED** - Fixed in task template
**Story Points**: 1
**Created**: 2025-11-07
**Source**: Julia Santos QA Review
**Agent**: @agent-julia
**Resolution Date**: 2025-11-07

**Description**:
Originally no test of npm registry connectivity. Build would fail 10+ min into install if registry unreachable.

**Implementation** (BUILD-FIXES-APPLIED.md):
- **T-020**: Added Step 5c for npm registry connectivity test

**Evidence**:
- T-020 Step 5c: npm registry connectivity test with timeout
- BUILD-FIXES-APPLIED.md documents implementation

**Tasks Affected**: T-020 (updated)

---

### BUILD-009: Missing File Count Verification

**Type**: Validation Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
No comparison of source vs destination file counts after repository clone. Incomplete copy undetected.

**Recommendation**:
Compare file counts between source and destination.

**Tasks Affected**: T-021

---

### BUILD-010: Missing Package Count Upper Bound

**Type**: Security/Validation Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
Only checks for 1500+ packages, no upper bound. 3000+ packages could indicate supply chain attack.

**Recommendation**:
Check package count in range 1500-2500.

**Tasks Affected**: T-023

---

### BUILD-011: Missing Error Extraction

**Type**: Operational Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 2
**Created**: 2025-11-07
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
Build log can be 10,000+ lines. No error/warning extraction for quick review.

**Recommendation**:
Extract errors and warnings to summary file.

**Tasks Affected**: T-024, T-025

---

### BUILD-012: Missing REST API Validation

**Type**: Integration Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 2
**Created**: 2025-11-07
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex

**Description**:
T-026 tests CLI but not REST API needed for MCP integration.

**Recommendation**:
Test `curl http://localhost:5678/healthz` after starting n8n.

**Tasks Affected**: T-026

---

### BUILD-013: Missing Disk I/O Monitoring During Copy

**Type**: Operational Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william

**Description**:
5GB repository copy has no I/O monitoring. Cannot diagnose slow operations.

**Tasks Affected**: T-021

---

### BUILD-014: Inefficient Ownership Setting

**Type**: Performance Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william

**Description**:
Separate `chown -R` after copy is inefficient. Use `rsync --chown` instead.

**Tasks Affected**: T-021

---

### BUILD-015: Missing Graphics Library Version Logging

**Type**: Documentation Gap
**Priority**: P3 - Low
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william

**Description**:
Cairo/pango versions not logged. Difficult to troubleshoot version-specific issues.

**Tasks Affected**: T-020

---

## Build Issues Summary

| Priority | Count | Story Points |
|----------|-------|--------------|
| **P0 (Critical)** | 2 | 5 |
| **P1 (High)** | 9 | 13 |
| **P2 (Medium)** | 3 | 4 |
| **P3 (Low)** | 1 | 1 |
| **TOTAL** | **15** | **23** |

**Critical Path Issues (MUST FIX)**:
1. BUILD-001: Add resource limits (systemd-run)
2. BUILD-002: Run commands as n8n user

**High Priority (STRONGLY RECOMMENDED)**:
- BUILD-003 through BUILD-011 (9 issues, 13 story points)



---

## Phase 3.3 Deployment Task Review Issues (NEW - 2025-11-07)

**Source**: Team reviews by @agent-omar, @agent-william, @agent-julia, @agent-alex, @agent-quinn
**Review Date**: 2025-11-07
**Tasks Reviewed**: T-027 through T-044 (18 deployment tasks)
**Total Issues Found**: 35

### Summary by Priority

| Priority | Count | Category | Status |
|----------|-------|----------|--------|
| **P0 (Critical/Blocker)** | ~~2~~ **0** | ~~Database configuration~~ | ✅ Both DEPLOY-001 and DEPLOY-002 resolved/downgraded |
| **P1 (High)** | 11 | Infrastructure, Database, Architecture, QA | Ready |
| **P2 (Medium)** | ~~14~~ **15** | Testing, Operations, Documentation | DEPLOY-002 downgraded to P2 |
| **P3 (Low)** | 8 | Enhancements, Best Practices | Ready |
| **TOTAL** | **34** | (originally 35) | 1 verified as not-an-issue |

**Critical Issues Update** (2025-11-07):
- ✅ **DEPLOY-001**: VERIFIED CORRECT - Variables confirmed via n8n source code (not a blocker)
- ⚠️ **DEPLOY-002**: DOWNGRADED to P2 - Manual workaround acceptable for POC3, .pgpass for Phase 4

---

## Critical Issues (P0 - BLOCKERS) - ✅ ALL RESOLVED

**Status**: ✅ **NO BLOCKERS** - Originally 2 P0 issues, both now resolved/downgraded

### DEPLOY-001: PostgreSQL Connection String Format Error ✅ VERIFIED CORRECT

**Type**: Configuration/Database Gap
**Priority**: P0 - Critical (originally BLOCKER, now **NOT A BLOCKER**)
**Status**: ✅ **VERIFIED** - Variables confirmed correct via n8n source code
**Story Points**: 2
**Created**: 2025-11-07
**Verified**: 2025-11-07 (by @agent-omar)
**Source**: Quinn Davis Database Review
**Agent**: @agent-quinn, @agent-omar

**Description**:
T-033 uses potentially incorrect PostgreSQL environment variable names. n8n may use different variable names than specified, causing database connection failure on first startup.

**✅ VERIFICATION COMPLETE** (REVIEW-FEEDBACK.md):
Variables verified against n8n source code (`n8n-master/packages/@n8n/config/src/configs/database.config.ts`):

```bash
# ✅ VERIFIED CORRECT from n8n source:
DB_TYPE=postgresdb                              # ✅ CORRECT
DB_POSTGRESDB_HOST=hx-postgres-server.hx.dev.local  # ✅ CORRECT
DB_POSTGRESDB_PORT=5432                         # ✅ CORRECT
DB_POSTGRESDB_DATABASE=n8n_poc3                 # ✅ CORRECT
DB_POSTGRESDB_USER=n8n_user                     # ✅ CORRECT
DB_POSTGRESDB_PASSWORD=<FROM_QUINN>             # ✅ CORRECT
DB_POSTGRESDB_POOL_SIZE=20                      # ✅ CORRECT (updated from 10)
```

**Evidence**:
- Source code verification: `n8n-master/packages/@n8n/config/src/configs/database.config.ts`
- Pattern confirmed: `DB_POSTGRESDB_*` is official n8n naming convention
- REVIEW-FEEDBACK.md lines 70-96: Complete verification documentation
- Status changed from BLOCKER to VERIFIED (not a blocker)

**Resolution**: No changes required to T-033. Variable names are correct as specified.

**Tasks Affected**: T-033 (no changes needed)

---

### DEPLOY-002: Password Exposure in psql Commands ⚠️ ADDRESSED (Manual Workaround)

**Type**: Security Gap
**Priority**: P2 - Medium (downgraded from P0 - sub-optimal but workable for POC3)
**Status**: ⚠️ **DEFERRED** - Manual workaround acceptable for POC3, fix in Phase 4
**Story Points**: 2
**Created**: 2025-11-07
**Reviewed**: 2025-11-07 (by @agent-omar, @agent-quinn)
**Source**: Quinn Davis Database Review
**Agent**: @agent-quinn, @agent-omar

**Description**:
T-040 and T-043 expose database password in command line via `-W` flag or password in connection string. Passwords visible in `ps aux` output and shell history.

**Security Assessment** (REVIEW-FEEDBACK.md DB-CRITICAL-2):
- **Severity**: SECURITY RISK - Sub-optimal password handling
- **POC3 Impact**: LOW (internal development environment, trusted users)
- **Production Impact**: MEDIUM-HIGH (should use .pgpass or alternative)

**Recommended Solutions** (in priority order):

**Option 1: .pgpass File** (PostgreSQL recommended - BEST for production):
```bash
# Create .pgpass file (PostgreSQL official method)
cat > ~/.pgpass <<EOF
hx-postgres-server.hx.dev.local:5432:n8n_poc3:n8n_user:<password>
EOF
chmod 600 ~/.pgpass

# Now psql connects without exposing password
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "SELECT 1"
# No password visible in ps aux or history
```

**Option 2: PGPASSWORD Environment Variable** (POC3 acceptable):
```bash
# Extract password from .env, use temporarily
export PGPASSWORD=$(grep DB_POSTGRESDB_PASSWORD /opt/n8n/.env | cut -d'=' -f2)
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "SELECT 1"
unset PGPASSWORD  # Clear immediately after use
```

**Option 3: Manual Password Entry** (POC3 acceptable - current approach):
```bash
# Operator manually types password when prompted
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "SELECT 1"
# Password: <typed by operator, not visible in history>
```

**POC3 Decision**: Use **Option 3** (manual entry) for deployment validation tasks
- Acceptable for internal development environment
- Tasks T-040, T-043 are one-time validation (not automated scripts)
- No password exposure risk if manually typed
- Phase 4 should implement Option 1 (.pgpass) for automated operations

**Phase 4 Requirement**: Implement .pgpass file for production deployments
- Document in operational runbook
- Create .pgpass during deployment setup
- Use for all automated database validation scripts

**Tasks Affected**: T-040, T-043 (manual password entry acceptable for POC3)

---

## High Priority Issues (P1)

### DEPLOY-003: Missing Log File Pre-creation

**Type**: Infrastructure Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william

**Description**:
systemd service may fail to start if n8n cannot create log file due to permissions. No pre-creation in T-027.

**Recommendation**:
Add to T-027:
```bash
sudo mkdir -p /var/log/n8n
sudo touch /var/log/n8n/n8n.log
sudo chown -R n8n:n8n /var/log/n8n
sudo chmod 755 /var/log/n8n
sudo chmod 644 /var/log/n8n/n8n.log
```

**Tasks Affected**: T-027

---

### DEPLOY-004: No .env Validation Before Service Start

**Type**: Infrastructure Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william

**Description**:
T-039 starts service without validating .env file exists and is readable. Cryptic systemd errors if missing.

**Recommendation**:
Add pre-start validation:
```bash
if [ ! -f /opt/n8n/.env ]; then
  echo "❌ .env file missing"
  exit 1
fi
if [ ! -r /opt/n8n/.env ]; then
  echo "❌ .env file not readable"
  exit 1
fi
```

**Tasks Affected**: T-039

---

### DEPLOY-005: Incomplete ReadWritePaths in systemd Service

**Type**: Infrastructure/Security Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william

**Description**:
T-034 systemd service hardening blocks access to `/opt/n8n/backups/`, breaking backup functionality.

**Recommendation**:
Fix ReadWritePaths in systemd service:
```ini
ReadWritePaths=/opt/n8n/.n8n
ReadWritePaths=/opt/n8n/backups
ReadWritePaths=/var/log/n8n
```

**Tasks Affected**: T-034

---

### DEPLOY-006: Inadequate Database Connection Pool

**Type**: Performance/Configuration Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 1
**Created**: 2025-11-07
**Source**: Quinn Davis Database Review
**Agent**: @agent-quinn, @agent-omar

**Description**:
T-033 sets connection pool size to 10. Too small for n8n workload - will cause "too many clients" errors.

**Recommendation**:
Increase pool size in .env:
```bash
DB_POSTGRESDB_POOL_SIZE=20  # Changed from 10
```

**Tasks Affected**: T-033

---

### DEPLOY-007: Insufficient Pre-Start Database Validation

**Type**: Validation Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 2
**Created**: 2025-11-07
**Source**: Quinn Davis Database Review
**Agent**: @agent-quinn

**Description**:
T-039 starts service without comprehensive database connectivity checks. Should verify database exists, credentials work, permissions granted BEFORE starting service.

**Recommendation**:
Add comprehensive pre-start checks.

**Tasks Affected**: T-039

---

### DEPLOY-008: Missing MCP Integration Architecture

**Type**: Architecture Gap
**Priority**: P1 - High (for Phase 4)
**Status**: Ready
**Story Points**: 5
**Created**: 2025-11-07
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex, @agent-olivia

**Description**:
No MCP (Model Context Protocol) integration pattern defined. Violates Hana-X agentic backbone requirement (Architecture 3.3).

**Recommendation**:
Create T-045-mcp-integration-architecture.md coordinating with @agent-olivia.

**Tasks Affected**: Phase 4 planning

---

### DEPLOY-009: Hardcoded Configuration Values

**Type**: Architecture Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 3
**Created**: 2025-11-07
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex, @agent-omar

**Description**:
T-033 hardcodes FQDNs, URLs, ports in .env. Violates Dependency Inversion Principle - not portable across environments.

**Recommendation**:
Parameterize configuration:
```bash
N8N_HOST=${N8N_HOST:-hx-n8n-server.hx.dev.local}
WEBHOOK_URL=${WEBHOOK_URL:-https://hx-n8n-server.hx.dev.local}
```

**Tasks Affected**: T-033

---

### DEPLOY-010: Missing Network Zone Validation

**Type**: Architecture/Security Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 2
**Created**: 2025-11-07
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex, @agent-william

**Description**:
T-027 doesn't validate server is in correct security zone (Application Layer, 192.168.10.x). Architecture 5.1 requirement.

**Recommendation**:
Add zone validation to T-027.

**Tasks Affected**: T-027

---

### DEPLOY-011: No Automated Testing

**Type**: Testing Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 8
**Created**: 2025-11-07
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
All deployment validation is manual. No automated test suite for regression testing or CI/CD integration.

**Recommendation**:
Create pytest test suite (included in Julia's review - 1000+ lines of code).

**Tasks Affected**: All validation tasks

---

### DEPLOY-012: Insufficient Edge Case Coverage

**Type**: Testing Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 5
**Created**: 2025-11-07
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
Tasks test happy path but not failure scenarios. Missing: disk full, network timeout, database unavailable, corrupted config.

**Recommendation**:
Add edge case testing to each task.

**Tasks Affected**: All tasks

---

### DEPLOY-013: Weak Integration Testing

**Type**: Testing Gap
**Priority**: P1 - High
**Status**: Ready
**Story Points**: 5
**Created**: 2025-11-07
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
Components tested in isolation. No end-to-end workflow execution tests, database-application integration tests.

**Recommendation**:
Create integration test suite.

**Tasks Affected**: T-042, T-043, T-044

---

## Medium Priority Issues (P2)

### DEPLOY-014: Missing logrotate Configuration

**Type**: Operations Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 2
**Source**: William Taylor Infrastructure Review
**Agent**: @agent-william

**Description**:
No log rotation configured. Logs will grow unbounded and fill disk over weeks/months.

**Tasks Affected**: T-027

---

### DEPLOY-015: No Pre-Start Health Checks ⚠️ UPDATED

**Type**: Infrastructure Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 2
**Source**: William Taylor Infrastructure Review (M-5)
**Updated**: 2025-11-07 (CodeRabbit: Added tool prerequisite clarification)
**Agent**: @agent-william

**Description**:
Service starts without verifying database is ready, leading to confusing connection failures.

**⚠️ CodeRabbit Prerequisite Clarification**:
Original recommendation uses `nc` (netcat) and `psql` for pre-start health checks, but tool availability not documented:
- `psql` - ✅ Already installed via T-007 (postgresql-client-16)
- `nc` (netcat) - ⚠️ NOT installed by default on hx-n8n-server
- `grep`, `ss` - ✅ Standard utilities (already present)

**Updated Recommendation**:
Two implementation options provided:

**Option 1: Install netcat conditionally**
```bash
if ! command -v nc >/dev/null 2>&1; then
  sudo apt install -y netcat-traditional
fi
nc -zv hx-postgres-server.hx.dev.local 5432
```

**Option 2: Bash-only (RECOMMENDED)**
```bash
# No external tools required - uses bash TCP redirection
timeout 2 bash -c "</dev/tcp/hx-postgres-server.hx.dev.local/5432" 2>/dev/null
```

**Recommendation**: Use bash-only Option 2 to avoid additional package dependencies.

**Tasks Affected**: T-039

**Resolution**: WILLIAM-REVIEW.md updated (v1.1) with tool prerequisites and bash-only alternative

**Reference**: WILLIAM-REVIEW.md:349-432 (M-5)

---

### DEPLOY-016: Wrong Protocol Configuration

**Type**: Configuration Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 1
**Source**: Omar Rodriguez N8N Review
**Agent**: @agent-omar

**Description**:
T-033 sets `N8N_PROTOCOL=https` but SSL isn't configured until Phase 4. Should be `http` initially.

**Tasks Affected**: T-033

---

### DEPLOY-017: Missing Operations Runbook

**Type**: Documentation Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 5
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex, @agent-omar

**Description**:
No operations runbook for common tasks: restart, backup, troubleshooting, log review.

**Tasks Affected**: T-044 (should create)

---

### DEPLOY-018: No Backup Procedures

**Type**: Operations Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 5
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex, @agent-omar

**Description**:
Deployment creates data but no automated backup procedures. Risk of data loss.

**Tasks Affected**: T-044

---

### DEPLOY-019: Technical Debt Not Documented

**Type**: Documentation Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 3
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex

**Description**:
16 technical debt items identified but not tracked in T-044 sign-off.

**Tasks Affected**: T-044

---

### DEPLOY-020: Secrets Management Strategy Missing

**Type**: Security/Architecture Gap
**Priority**: P2 - Medium (P0 for production)
**Status**: Ready
**Story Points**: 8
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex, @agent-frank

**Description**:
Plain-text passwords in .env OK for POC but no production migration path to HashiCorp Vault or similar.

**Tasks Affected**: T-033, future

---

### DEPLOY-021: No Test Data Management

**Type**: Testing Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 3
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
No test fixtures or test datasets for validation. Manual data entry required.

**Tasks Affected**: T-042

---

### DEPLOY-022: Limited Performance Validation

**Type**: Testing Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 3
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
No baseline performance metrics. Can't detect performance degradation.

**Tasks Affected**: T-044

---

### DEPLOY-023: Missing TypeORM Migration Monitoring

**Type**: Database Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 2
**Source**: Quinn Davis Database Review
**Agent**: @agent-quinn, @agent-omar

**Description**:
T-040 verifies migrations ran but doesn't monitor progress or detect stalls during long migrations.

**Tasks Affected**: T-040

---

### DEPLOY-024: No Database Performance Settings

**Type**: Database Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 2
**Source**: Quinn Davis Database Review
**Agent**: @agent-quinn

**Description**:
No PostgreSQL performance tuning for n8n workload. Should set work_mem, shared_buffers, etc.

**Tasks Affected**: T-033 (document), Quinn's DB config

---

### DEPLOY-025: Missing SSL/TLS Database Connection

**Type**: Security Gap
**Priority**: P2 - Medium (P1 for production)
**Status**: Ready
**Story Points**: 2
**Source**: Quinn Davis Database Review
**Agent**: @agent-quinn, @agent-frank

**Description**:
Database connection uses plain-text. Should use SSL/TLS (sslmode=require).

**Tasks Affected**: T-033

---

### DEPLOY-026: No Connection Timeout Configuration

**Type**: Configuration Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 1
**Source**: Quinn Davis Database Review
**Agent**: @agent-quinn, @agent-omar

**Description**:
No connection timeout set. App hangs indefinitely if database unreachable.

**Tasks Affected**: T-033

---

### DEPLOY-027: Incomplete .env Optional Variables

**Type**: Configuration Gap
**Priority**: P2 - Medium
**Status**: Ready
**Story Points**: 2
**Source**: Omar Rodriguez N8N Review
**Agent**: @agent-omar

**Description**:
T-033 missing optional but useful variables: DB_POSTGRESDB_SCHEMA, NODE_OPTIONS, timeouts.

**Tasks Affected**: T-033

---

## Low Priority Issues (P3)

### DEPLOY-028: No Encryption Key Verification

**Type**: Validation Gap
**Priority**: P3 - Low
**Status**: Ready
**Story Points**: 1
**Source**: Omar Rodriguez N8N Review
**Agent**: @agent-omar

**Description**:
T-039 doesn't verify .encryption-key was created on first startup. Nice-to-have assurance check.

**Tasks Affected**: T-039

---

### DEPLOY-029: Manual Admin User Creation

**Type**: Automation Gap
**Priority**: P3 - Low
**Status**: Ready
**Story Points**: 3
**Source**: Julia Santos QA Review
**Agent**: @agent-julia

**Description**:
T-042 requires manual browser interaction. Should automate via API.

**Tasks Affected**: T-042

---

### DEPLOY-030: No Disaster Recovery Testing

**Type**: Testing Gap
**Priority**: P3 - Low
**Status**: Ready
**Story Points**: 5
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex

**Description**:
No disaster recovery procedures tested. Unknown if backup/restore actually works.

**Tasks Affected**: Future

---

### DEPLOY-031: Missing ADR Documentation

**Type**: Documentation Gap
**Priority**: P3 - Low
**Status**: Ready
**Story Points**: 2
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex

**Description**:
Key architectural decisions not documented in ADR format (secrets management, auth pattern).

**Tasks Affected**: T-044

---

### DEPLOY-032: No Multi-Instance Support

**Type**: Scalability Gap
**Priority**: P3 - Low (CRITICAL for HA)
**Status**: Ready
**Story Points**: 13
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex

**Description**:
Deployment is single-instance only. No support for high availability or horizontal scaling.

**Tasks Affected**: Future (Phase 2)

---

### DEPLOY-033: Cross-Layer Auth Unclear

**Type**: Architecture Gap
**Priority**: P3 - Low
**Status**: Ready
**Story Points**: 5
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex, @agent-frank

**Description**:
Database uses password auth but Architecture mandates Kerberos. Pattern inconsistency.

**Tasks Affected**: Documentation

---

### DEPLOY-034: No SIEM Integration

**Type**: Security Gap
**Priority**: P3 - Low (P1 for production)
**Status**: Ready
**Story Points**: 5
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex

**Description**:
No security event logging to SIEM. Can't detect intrusion attempts.

**Tasks Affected**: Future (production)

---

### DEPLOY-035: No Credential Complexity Checks

**Type**: Security Gap
**Priority**: P3 - Low
**Status**: Ready
**Story Points**: 2
**Source**: Alex Rivera Architecture Review
**Agent**: @agent-alex

**Description**:
T-042 doesn't enforce password complexity for admin user.

**Tasks Affected**: T-042

---

## Deployment Issues Summary

| Priority | Count | Story Points |
|----------|-------|--------------|
| **P0 (Critical/Blocker)** | 2 | 4 |
| **P1 (High)** | 11 | 40 |
| **P2 (Medium)** | 14 | 44 |
| **P3 (Low)** | 8 | 43 |
| **TOTAL** | **35** | **131** |

**Critical Path Issues (MUST FIX BEFORE DEPLOYMENT)**:
1. DEPLOY-001: Fix PostgreSQL connection string format
2. DEPLOY-002: Remove password exposure in commands

**High Priority (STRONGLY RECOMMENDED - 4-5 hours)**:
- DEPLOY-003 through DEPLOY-013 (11 issues)

**Time to Address**:
- P0 issues: 1-2 hours
- P1 issues: 4-5 hours
- P2 issues: 10-14 days
- P3 issues: Deferred to Phase 4 or production

