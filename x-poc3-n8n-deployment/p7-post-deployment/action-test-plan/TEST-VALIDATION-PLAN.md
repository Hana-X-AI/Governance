# POC3 N8N Deployment - Test & Validation Plan

**Project**: POC3 N8N Deployment Post-Deployment Remediation
**Created**: 2025-11-09
**Version**: 1.1
**Status**: ACTIVE
**Author**: Julia Santos (QA Lead)
**Source**: Consolidated Action Plan v3.1 (Team-Reviewed & Revised)

---

## Executive Summary

This test and validation plan ensures all 18 actions in the Consolidated Action Plan v3.1 are properly tested, validated, and verified before sign-off. The plan covers:

- **18 Actions**: ACTION-001 through ACTION-017 (006A/006B split)
- **144 Total Test Cases**: Detailed breakdown prevents v1.0 test inflation issue
- **58-62 hours** of remediation work requiring validation
- **51 CodeRabbit remediation documents** mapped via traceability matrix
- **7 original deployment defects** requiring regression testing
- **3.5-4 week execution timeline** with parallel and sequential testing

**Test Scope Clarity** (prevents v1.0-style inflation from 96→214):
- **v1.0 Problem**: Test count inflated from 96 to 214 by counting sub-criteria as separate tests
- **v1.1 Fix**: Clear categorization with explicit test IDs and no double-counting
- **Total = 144 tests**: 96 unit (TC-001 to TC-096) + 10 integration (INT-001 to INT-010) + 12 compliance (COMP-001 to COMP-012) + 18 performance (PERF-001 to PERF-018) + 8 documentation (DOC-001 to DOC-008)
- **Automation = 19 tests (13%)**: Subset within categories above, not additional tests

### Test Strategy Overview

| Test Type | Test Cases | Coverage | Automation |
|-----------|------------|----------|------------|
| **Unit Testing** | 96 detailed test cases (TC-001 to TC-096) | Individual action validation | Manual |
| **Integration Testing** | 10 scenarios (INT-001 to INT-010) | Cross-action dependencies | Manual |
| **Regression Testing** | 15 automated checks (subset of above) | Original defects + CodeRabbit findings | 15 automated |
| **Compliance Testing** | 12 checks (COMP-001 to COMP-012) | PCI-DSS, SOC 2, NIST standards | 3 automated |
| **Performance Testing** | 18 actions (PERF-001 to PERF-018) | Time estimate validation | Manual tracking |
| **Documentation Testing** | 8 quality checks (DOC-001 to DOC-008) | Consistency and accuracy | 1 automated |
| **Total** | **144 total test cases** | **100% action coverage** | **19 automated (13%)** |

**Test Count Clarification**:
- **144 total executable tests**: 96 unit + 10 integration + 12 compliance + 18 performance + 8 documentation
- **19 automated tests** (13% of total): Subset of categories above that support automation
  - 15 regression tests (automated checks of original defects + CodeRabbit findings)
  - 3 compliance tests (automated security/standards validation)
  - 1 documentation test (automated consistency check)
- **125 manual tests** (87% of total): Remaining tests requiring human validation
- **Note**: Automated tests are not additional to the above categories - they are automated implementations of specific tests within Unit, Compliance, and Documentation categories

### Success Criteria

✅ All 18 actions pass acceptance criteria
✅ No regression of 7 original deployment defects
✅ No regression of 51 CodeRabbit remediation items
✅ Compliance requirements met (PCI-DSS, SOC 2, NIST)
✅ Process improvements documented with owners (ACTION-017)
✅ Actual time within ±20% of estimated time (58-62h target)

---

## Table of Contents

1. [Test Environment Setup](#test-environment-setup)
2. [Test Execution Timeline](#test-execution-timeline)
3. [Action-by-Action Test Cases](#action-by-action-test-cases)
4. [Integration Test Scenarios](#integration-test-scenarios)
5. [Regression Test Suite](#regression-test-suite)
6. [Compliance Validation](#compliance-validation)
7. [Performance Validation](#performance-validation)
8. [Documentation Quality Tests](#documentation-quality-tests)
9. [Test Automation](#test-automation)
10. [Sign-Off Criteria](#sign-off-criteria)

---

## Test Environment Setup

### Required Access

| Resource | Hostname/URL | Purpose | Owner |
|----------|--------------|---------|-------|
| **N8N Instance** | https://n8n.hx.dev.local | Live system testing | Omar |
| **PostgreSQL DB** | hx-postgres-server.hx.dev.local:5432 | Database validation | Quinn |
| **Credential Vault** | `/srv/cc/Governance/0.2-credentials/` | Credential verification | William |
| **Task Documentation** | `/srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/` | Documentation updates | All |
| **Remediation Docs** | `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/remediations/` | Traceability validation | Julia |
| **Git Repository** | `/srv/cc/Governance/` | Version control | All |
| **Test Data** | `/srv/tests/data/` | Test fixtures and mock data | Julia |

### Test User Accounts

```bash
# Development environment test account
Username: caio@hx.dev.local
Password: <vault:hx-credentials:caio>
Purpose: LDAP authentication testing
```

### Test Data Infrastructure

**Location**: `/srv/tests/data/`

**Test Fixtures** (created Week 1, Day 1):
- **Sample .env files**:
  - `env-secure.sample` (600 permissions, vault references)
  - `env-insecure.sample` (644 permissions, plaintext passwords) - for testing
- **Mock SSL certificates**:
  - `test-cert.pem` (for ACTION-005 transfer testing)
  - `test-key.pem` (for ACTION-005 transfer testing)
- **Sample bash scripts**:
  - `test-variable-capture.sh` (for ACTION-001 testing)
  - `test-stat-commands.sh` (for ACTION-003 testing)
- **Database test data**:
  - `test-table-list.txt` (expected 50 tables for ACTION-004)
  - `test-db-credentials.env` (for ACTION-002 testing)

**Setup Script**: `/srv/tests/setup-test-fixtures.sh` (executed on Week 1, Day 1)

### Pre-Test Checklist

- [ ] Access to all servers (hx-n8n-server, hx-postgres-server)
- [ ] SSH keys configured for agent0 user
- [ ] Credential vault readable
- [ ] Git repository access (push/pull permissions)
- [ ] N8N service operational at https://n8n.hx.dev.local
- [ ] Database connection verified (psql access)
- [ ] Database backup created (see rollback procedures)
- [ ] Test data fixtures created in `/srv/tests/data/`
- [ ] All background bash processes from previous work cleaned up
- [ ] Agent availability confirmed (Omar, Quinn, Frank, William, Alex)

### Database Backup Procedure

**CRITICAL**: Create database backup before any testing to enable rollback.

```bash
# Create database backup (Week 1, Day 1 - BEFORE any testing)
PGPASSWORD=$(vault read -field=password secret/n8n) \
  pg_dump -h hx-postgres-server -U svc-n8n -d n8n_poc3 \
  > /tmp/n8n-backup-$(date +%Y%m%d).sql

# Verify backup
ls -lh /tmp/n8n-backup-*.sql

# Restoration procedure (if needed)
PGPASSWORD=$(vault read -field=password secret/n8n) \
  psql -h hx-postgres-server -U svc-n8n -d n8n_poc3 \
  < /tmp/n8n-backup-YYYYMMDD.sql
```

---

## Test Execution Timeline

### Week 1: Setup + HIGH Priority Actions (28-32 hours)

**Focus**: Technical fixes blocking automation

| Day | Actions | Test Focus | Owner(s) | Dependencies |
|-----|---------|------------|----------|--------------|
| **Mon** | Kickoff + Setup | Test environment validation, access verification, test fixtures creation | Julia | None |
| **Tue** | ACTION-001, 002 | Variable capture fix, database prompts | Omar, Quinn | Test fixtures |
| **Wed** | ACTION-003, 004 | Linux compatibility, table name validation | Omar, Quinn | None |
| **Thu** | ACTION-006A | Infrastructure discovery (FreeIPA vs Samba AD) | Frank | **MUST complete before Fri** |
| **Fri** | ACTION-005, 006B | SSL certificate error handling, SSL procedures | Frank | **006A complete** |

**⚠️ CRITICAL DEPENDENCY**: ACTION-006A (Thu) MUST complete before ACTION-005 (Fri) begins. ACTION-005 requires knowing infrastructure type to implement correct SSL procedures.

### Week 2: MEDIUM Priority Actions (20-22 hours)

**Focus**: Documentation improvements and process ownership

| Day | Actions | Test Focus | Owner(s) | Dependencies |
|-----|---------|------------|----------|--------------|
| **Mon** | ACTION-017 | Process improvement ownership assignment | Zero + Alex | None |
| **Tue** | ACTION-007, 008 | .env security, blocking prerequisites | Frank, William | Parallel OK |
| **Wed** | ACTION-009, 010 | Database username standardization, .env guidance | Quinn, William | Parallel OK |
| **Thu** | ACTION-011 | Exit code standardization for CI/CD | William | None |
| **Fri** | Integration Testing | Cross-action dependency validation | Julia | All actions complete |

### Week 3: LOW Priority + QA Sign-Off (10-12 hours)

**Focus**: Documentation quality and final validation

| Day | Actions | Test Focus | Owner(s) | Dependencies |
|-----|---------|------------|----------|--------------|
| **Mon** | ACTION-012, 013 | HTTPS clarification, specification updates | William, Omar | Parallel OK |
| **Tue** | ACTION-014, 015, 016 | Backlog count, grep patterns, stale output | Julia, William, Omar | Parallel OK |
| **Wed** | Regression Testing | All 51 remediations + 7 defects | Julia | All actions complete |
| **Thu** | Compliance Testing | PCI-DSS, SOC 2, NIST validation | Julia + Frank | All actions complete |
| **Fri** | **QA Sign-Off** | Final validation and approval | Julia | All tests pass |

### Week 4: Contingency + Documentation (if needed)

**Focus**: Address any failed tests, defect remediation, final documentation

| Day | Actions | Test Focus | Owner(s) |
|-----|---------|------------|----------|
| **Mon-Wed** | Defect remediation | Fix any test failures, re-test | TBD based on failures |
| **Thu** | Final regression | Re-run all tests after fixes | Julia |
| **Fri** | Final sign-off | Stakeholder approvals | All |

---

## Action-by-Action Test Cases

### ACTION-001: Fix Build Test Variable Capture Bug

**Owner**: Omar Rodriguez
**Priority**: HIGH
**Estimated Time**: 2 hours
**Test Approach**: Unit Testing + Integration

#### Pre-Test Checklist
- [ ] Read current file: `p3-tasks/p3.2-build/t-026-test-build-executable.md`
- [ ] Identify lines 224-230 (broken code)
- [ ] Prepare test build environment
- [ ] Test fixtures: `/srv/tests/data/test-variable-capture.sh`

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-001** | Verify broken code identified | Read lines 224-230 | Confirm `syntax_output` undefined, exit code captures tee | |
| **TC-002** | Test variable capture fix | Execute corrected code with pipefail | `syntax_output` contains version string | |
| **TC-003** | Test exit code capture | Run corrected code, node fails | Exit code = node exit code (not tee) | |
| **TC-004** | Test success scenario | Run corrected code, node succeeds | `exit_code=0` and `syntax_output` non-empty | |
| **TC-005** | Test failure scenario | Run corrected code, node fails | `exit_code≠0` and error logged | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Variable `syntax_output` properly assigned before use
✅ **Criterion 2**: Exit code captures `node` command, not `tee`
✅ **Criterion 3**: Build test can distinguish success from failure
✅ **Criterion 4**: Documentation updated with corrected code

#### Success Metrics

- ✅ Test executes without "undefined variable" error
- ✅ Exit code correctly reflects node command status
- ✅ Build validation logic works as intended

#### Rollback Procedure

**If fix fails**:
1. Revert to original code in git: `git checkout HEAD~1 p3-tasks/p3.2-build/t-026-test-build-executable.md`
2. Document why fix failed in defect log: `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/action-test-plan/TEST-DEFECT-LOG.md`
3. Create new remediation document with alternative approach
4. Re-test with alternative fix

---

### ACTION-002: Fix Interactive Database Password Prompts

**Owner**: Quinn Baker
**Priority**: HIGH
**Estimated Time**: 1 hour
**Test Approach**: Integration Testing

#### Pre-Test Checklist
- [ ] Access to hx-postgres-server.hx.dev.local
- [ ] Database password available from credential vault: `<vault:hx-credentials:svc-n8n>`
- [ ] File: `p3-tasks/p3.6-validation/t-044-deployment-sign-off.md`
- [ ] Identify 7 psql commands (lines 83, 88, 227-229, 387, 395)
- [ ] Test fixtures: `/srv/tests/data/test-db-credentials.env`

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-006** | Identify all interactive psql commands | Grep for `psql` without PGPASSWORD | Find all 7 instances (lines documented) | |
| **TC-007** | Test PGPASSWORD loading | Source .env, run `echo $PGPASSWORD` | Password loaded from vault | |
| **TC-008** | Test non-interactive execution (line 83) | Run `PGPASSWORD=... psql -c "SELECT 1;"` | No prompt, query succeeds | |
| **TC-009** | Test all 7 commands non-interactively | Execute each with PGPASSWORD | All succeed without prompts | |
| **TC-010** | Test automation compatibility | Run in bash script (non-TTY) | All commands execute without hanging | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: All 7 psql commands load PGPASSWORD from .env
✅ **Criterion 2**: No interactive password prompts during execution
✅ **Criterion 3**: Automated validation completes without manual input
✅ **Criterion 4**: .env file sourced before database queries

#### Success Metrics

- ✅ 0/7 commands prompt for password (was 7/7)
- ✅ Sign-off task can run unattended
- ✅ Time to execute sign-off: <5 minutes (was: blocked indefinitely)

#### Rollback Procedure

**If fix fails**:
1. Revert to original psql commands (without PGPASSWORD)
2. Document specific psql command that failed
3. Investigate vault access issues or password format issues
4. Re-test with corrected vault reference

---

### ACTION-003: Fix Linux Compatibility (BSD stat → GNU stat)

**Owner**: Omar Rodriguez
**Priority**: HIGH
**Estimated Time**: 4 hours
**Test Approach**: Cross-File Audit + Unit Testing

#### Pre-Test Checklist
- [ ] Search all task files for `stat -f%z` (BSD syntax)
- [ ] Verify target platform: Ubuntu 22.04 (GNU stat)
- [ ] Test environment: Linux server with GNU coreutils
- [ ] Test fixtures: `/srv/tests/data/test-stat-commands.sh`

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-011** | Identify all BSD stat commands | `grep -r "stat -f" p3-tasks/` | Find all instances (document locations) | |
| **TC-012** | Test BSD syntax on Ubuntu 22.04 | Run `stat -f%z file.txt` on Linux | Command fails with "invalid option" | |
| **TC-013** | Test GNU syntax on Ubuntu 22.04 | Run `stat -c%s file.txt` on Linux | Command succeeds, returns file size | |
| **TC-014** | Update all instances to GNU syntax | Replace `-f%z` with `-c%s` | All stat commands updated | |
| **TC-015** | Execute all updated stat commands | Run each command on target platform | All succeed on Ubuntu 22.04 | |
| **TC-016** | Cross-platform compatibility note | Add comment: `# GNU stat (Linux)` | Future readers understand platform dependency | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: All BSD stat commands identified (cross-file audit)
✅ **Criterion 2**: All updated to GNU syntax (`-c%s`)
✅ **Criterion 3**: All commands tested on Ubuntu 22.04
✅ **Criterion 4**: Documentation notes platform requirement

#### Success Metrics

- ✅ 0 BSD stat commands remain (comprehensive audit)
- ✅ 100% of stat commands work on target platform
- ✅ No "invalid option" errors during execution

#### Rollback Procedure

**If fix fails**:
1. Identify specific stat command that failed
2. Check if GNU stat alternative syntax needed (`-c` vs `--format`)
3. Test alternative GNU stat syntax
4. Update to working syntax

---

### ACTION-004: Verify Database Table Names in Migration Validation

**Owner**: Quinn Baker
**Priority**: HIGH
**Estimated Time**: 3 hours
**Test Approach**: Database Validation + Script Enhancement

#### Pre-Test Checklist
- [ ] Database access: `PGPASSWORD=<vault:hx-credentials:svc-n8n> psql -h hx-postgres-server -U svc-n8n -d n8n_poc3`
- [ ] Current expected tables: 50
- [ ] File: `p3-tasks/p3.6-validation/t-043-verify-database-tables.md`
- [ ] Test fixtures: `/srv/tests/data/test-table-list.txt` (expected 50 tables)

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-017** | Query actual table count | `SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';` | Returns actual count (50) | |
| **TC-018** | List all table names | Query with table_name ordering | Full list of 50 tables | |
| **TC-019** | Verify critical tables exist | Check: workflow, execution, credentials, user, settings | All critical tables present | |
| **TC-020** | Test enhanced validation script | Run 150+ line script from remediation doc | Reports table count, names, missing tables | |
| **TC-021** | Test table name validation | Compare actual vs expected list | Script detects any missing/extra tables | |
| **TC-022** | Test error reporting | Remove expected table from list | Script reports "Missing table: X" | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Enhanced script lists all actual table names
✅ **Criterion 2**: Script compares actual vs expected (validates)
✅ **Criterion 3**: Script reports missing/extra tables with clear messaging
✅ **Criterion 4**: Documentation updated with table name list

#### Success Metrics

- ✅ Script validates 50/50 tables correctly
- ✅ Missing table detection works (if table dropped)
- ✅ Execution time: <10 seconds for validation

#### Rollback Procedure

**If fix fails**:
1. Revert to original simple table count script
2. Manually verify critical tables exist
3. Document which table validation logic failed
4. Create alternative validation approach

---

### ACTION-005: Add SSL Certificate Transfer Error Handling

**Owner**: Frank Delgado
**Priority**: HIGH
**Estimated Time**: 8 hours
**Test Approach**: Script Development + Integration Testing
**CRITICAL DEPENDENCY**: ACTION-006A must complete first

#### Pre-Test Checklist
- [ ] **VERIFY ACTION-006A COMPLETE**: Infrastructure type documented
- [ ] Read: `p3-tasks/p3.1-preparation/t-003-transfer-ssl-certificate.md`
- [ ] Current code: Lines 16-36 (no error handling)
- [ ] Test fixtures: `/srv/tests/data/test-cert.pem`, `/srv/tests/data/test-key.pem`

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-023** | Test current script failure scenario | Run original script, SCP fails | Silent failure, no error logged | |
| **TC-024** | Test enhanced script - SCP failure | Run new script, SCP fails | Error logged, script exits 1 | |
| **TC-025** | Test enhanced script - permission denied | Run new script, chmod fails | Error logged, cleanup executed | |
| **TC-026** | Test enhanced script - success path | Run new script, all commands succeed | Success logged, exit 0 | |
| **TC-027** | Test audit logging | Check log file after execution | All operations logged with timestamps | |
| **TC-028** | Test cleanup on failure | Cause failure mid-script | Partial files cleaned up via trap | |
| **TC-029** | Test certificate validation | Transfer invalid cert | Script detects and reports | |
| **TC-030** | Test set -euo pipefail | Cause command failure in pipeline | Script exits immediately | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: All SCP/SSH commands have error checking
✅ **Criterion 2**: Failed operations logged with timestamps
✅ **Criterion 3**: Cleanup trap handles failures (no orphaned files)
✅ **Criterion 4**: Exit codes: 0=success, 1=failure
✅ **Criterion 5**: Audit log meets SOC 2 CC6.7 requirements

#### Success Metrics

- ✅ 0 silent failures (all errors reported)
- ✅ 100% operations logged to audit file
- ✅ Cleanup executes on 100% of failures

#### Rollback Procedure

**If fix fails**:
1. Revert to original SSL transfer script (no error handling)
2. Remove any partial transferred certificates: `ssh target-server 'rm -f /tmp/cert-*.pem'`
3. Document specific error handling that failed
4. Create alternative error handling approach
5. Re-test with alternative implementation

---

### ACTION-006A: Infrastructure Discovery (FreeIPA vs Samba AD)

**Owner**: Frank Delgado
**Priority**: HIGH
**Estimated Time**: 4 hours
**Test Approach**: Discovery + Documentation
**⚠️ BLOCKING**: Must complete before ACTION-005

#### Pre-Test Checklist
- [ ] Access to infrastructure documentation
- [ ] LDAP server: hx-identity-server (192.168.10.202)
- [ ] DNS/LDAP service status checks available

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-031** | Check LDAP service type | Query LDAP server schema | Identify FreeIPA or Samba AD | |
| **TC-032** | Verify DNS integration | Query DNS for hx.dev.local zone | Determine DNS server (Samba or FreeIPA) | |
| **TC-033** | Document findings | Create infrastructure discovery report | Clear statement of architecture | |
| **TC-034** | Update task documentation | Update references to match reality | All docs reflect actual infrastructure | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Clear documentation of actual infrastructure (FreeIPA vs Samba AD)
✅ **Criterion 2**: All task references updated to match reality
✅ **Criterion 3**: No conflicting statements about LDAP/DNS architecture

#### Success Metrics

- ✅ 100% clarity on infrastructure type
- ✅ 0 conflicting documentation statements
- ✅ Discovery report published

#### Rollback Procedure

**If discovery incomplete**:
1. Document what was discovered
2. Mark ambiguous findings as "needs further investigation"
3. Do not proceed to ACTION-005 until infrastructure type confirmed
4. Escalate to Alex Rivera (Architect) if unable to determine

---

### ACTION-006B: SSL Certificate Generation Procedures

**Owner**: Frank Delgado
**Priority**: HIGH
**Estimated Time**: 6 hours
**Test Approach**: Procedure Documentation + Testing

#### Pre-Test Checklist
- [ ] SSL certificates currently in use at n8n.hx.dev.local
- [ ] Certificate authority information
- [ ] Renewal procedures documented
- [ ] Test fixtures: Test CA and test certificate generation

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-035** | Document certificate generation | Reverse-engineer current cert creation | Complete procedure documented | |
| **TC-036** | Test certificate generation procedure | Follow documented steps, generate test cert | Valid certificate created | |
| **TC-037** | Test certificate installation | Install test cert on dev server | HTTPS works with test cert | |
| **TC-038** | Test certificate renewal | Document renewal process | Clear renewal procedure | |
| **TC-039** | Document expiry monitoring | Add monitoring recommendations | Expiry alerts defined | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Complete SSL certificate generation procedure
✅ **Criterion 2**: Certificate renewal process documented
✅ **Criterion 3**: Expiry monitoring recommendations included

#### Success Metrics

- ✅ Certificate generation procedure tested and verified
- ✅ Renewal process clear and actionable
- ✅ Monitoring recommendations meet SOC 2 requirements

#### Rollback Procedure

**If certificate generation fails**:
1. Revert test certificate installation
2. Restore original certificate
3. Restart N8N service with original cert
4. Document what step failed
5. Create alternative procedure

---

### ACTION-007: Add .env File Security (Permissions and Ownership)

**Owner**: Frank Delgado
**Priority**: MEDIUM
**Estimated Time**: 2 hours
**Test Approach**: File System Validation

#### Pre-Test Checklist
- [ ] Find all .env files: `find /opt/n8n -name ".env"`
- [ ] Current permissions: likely 644 (world-readable)
- [ ] Required permissions: 600 (owner read/write only)
- [ ] Test fixtures: `/srv/tests/data/env-secure.sample`, `/srv/tests/data/env-insecure.sample`

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-040** | Check current .env permissions | `ls -la /opt/n8n/.env` | Verify current permissions (likely 644) | |
| **TC-041** | Check current .env ownership | `ls -la /opt/n8n/.env` | Verify current owner (should be n8n:n8n) | |
| **TC-042** | Update permissions to 600 | `chmod 600 /opt/n8n/.env` | Permissions: -rw------- | |
| **TC-043** | Update ownership | `chown n8n:n8n /opt/n8n/.env` | Owner: n8n, Group: n8n | |
| **TC-044** | Test N8N service restart | `systemctl restart n8n` | Service starts, reads .env successfully | |
| **TC-045** | Test world-readability blocked | `sudo -u nobody cat /opt/n8n/.env` | Permission denied | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: All .env files have 600 permissions
✅ **Criterion 2**: All .env files owned by n8n:n8n
✅ **Criterion 3**: N8N service can read .env after permission changes
✅ **Criterion 4**: Documentation updated with security requirements

#### Success Metrics

- ✅ 0 .env files with world-readable permissions
- ✅ 100% .env files owned by service user
- ✅ N8N service operational after changes

#### Rollback Procedure

**If service fails after permission change**:
1. Stop N8N service: `systemctl stop n8n`
2. Revert permissions: `chmod 644 /opt/n8n/.env`
3. Restart service: `systemctl start n8n`
4. Verify service operational
5. Investigate why 600 permissions failed
6. Check systemd service user/group configuration

---

### ACTION-008: Reconcile Blocking Prerequisites Contradiction

**Owner**: William Harrison
**Priority**: MEDIUM
**Estimated Time**: 4 hours
**Test Approach**: Documentation Analysis + Reconciliation

#### Pre-Test Checklist
- [ ] Read William's review identifying scope contradiction
- [ ] Locate contradictory sections in prerequisites document
- [ ] Determine actual scope needed

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-046** | Identify contradiction | Read prerequisites doc, find conflicting scope | Contradiction documented | |
| **TC-047** | Determine actual scope | Analyze what prerequisites actually cover | Clear scope definition | |
| **TC-048** | Update documentation | Reconcile conflicting sections | No contradictions remain | |
| **TC-049** | Verify consistency | Read updated doc end-to-end | Scope consistent throughout | |
| **TC-050** | Verify resolution accuracy | Review fix against actual prerequisites | Resolution matches reality, not just consistent | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Contradiction identified and documented
✅ **Criterion 2**: Actual scope clearly defined
✅ **Criterion 3**: Documentation updated to be internally consistent
✅ **Criterion 4**: No conflicting statements about scope
✅ **Criterion 5**: Resolution verified by second reviewer (Frank or Alex)

#### Success Metrics

- ✅ 0 scope contradictions in prerequisites document
- ✅ Clear definition of what prerequisites cover
- ✅ Documentation passes consistency review
- ✅ Resolution verified as accurate (not just consistent)

#### Rollback Procedure

**If reconciliation creates new issues**:
1. Revert to original document version
2. Document what went wrong with reconciliation
3. Create alternative reconciliation approach
4. Re-test with alternative

---

### ACTION-017: Assign Ownership to Process Improvements for POC4

**Owner**: Agent Zero + Alex Rivera
**Priority**: HIGH
**Estimated Time**: 2 hours
**Test Approach**: Ownership Assignment + Documentation

#### Pre-Test Checklist
- [ ] Read 8 process improvements from lessons-learned.md
- [ ] Identify appropriate owners for each improvement
- [ ] Define success criteria and timelines

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-051** | List all 8 process improvements | Extract from lessons-learned.md | Complete list of improvements | |
| **TC-052** | Assign owner to each improvement | Match improvement to agent expertise | All 8 have designated owners | |
| **TC-053** | Define success criteria | For each improvement, define "done" | Measurable success criteria | |
| **TC-054** | Set implementation timelines | Realistic deadlines for POC4 | All improvements have deadlines | |
| **TC-055** | Create implementation plan document | Write formal plan | Plan published and reviewed | |
| **TC-056** | Get owner buy-in | Each owner confirms assignment | All owners acknowledge ownership | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: All 8 process improvements have designated owners
✅ **Criterion 2**: Each improvement has success criteria defined
✅ **Criterion 3**: Implementation timeline defined for POC4
✅ **Criterion 4**: Owners have acknowledged assignments

#### Success Metrics

- ✅ 8/8 process improvements have owners
- ✅ 8/8 have measurable success criteria
- ✅ 8/8 have implementation deadlines
- ✅ Implementation plan document published

#### Rollback Procedure

**If ownership assignments rejected**:
1. Document which owners rejected assignments
2. Identify alternative owners
3. Reassign to willing owners
4. Update implementation plan

---

### ACTION-009: Standardize Database Username Across Planning Documents

**Owner**: Quinn Baker
**Priority**: MEDIUM
**Estimated Time**: 2 hours
**Test Approach**: Documentation Audit + Update

#### Pre-Test Checklist
- [ ] Search all docs for `n8n_user` (planning docs)
- [ ] Search all docs for `svc-n8n` (execution docs)
- [ ] Determine standard: `svc-n8n` (current reality)

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-057** | Find all n8n_user references | `grep -r "n8n_user" p1-planning/` | List of all planning doc references | |
| **TC-058** | Find all svc-n8n references | `grep -r "svc-n8n" p3-tasks/` | List of execution doc references | |
| **TC-059** | Verify database actual username | `SELECT current_user;` on database | Confirm actual username: svc-n8n | |
| **TC-060** | Update all planning docs | Replace n8n_user → svc-n8n | All planning docs use svc-n8n | |
| **TC-061** | Verify consistency | `grep -r "n8n_user" .` | 0 references to old username | |
| **TC-062** | Test database connection | Connect using standardized username | Connection succeeds | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: All documents use standardized username `svc-n8n`
✅ **Criterion 2**: 0 references to deprecated `n8n_user`
✅ **Criterion 3**: Username matches actual database account
✅ **Criterion 4**: Database grants verified for `svc-n8n`

#### Success Metrics

- ✅ 0 references to `n8n_user` in documentation
- ✅ 100% consistency across planning and execution docs
- ✅ Database connection tests pass with standardized username

#### Rollback Procedure

**If username change breaks connections**:
1. Revert all documentation to `n8n_user`
2. Verify which username database actually uses
3. Update documentation to match actual database username
4. Consider database username migration if needed

---

### ACTION-010: Add .env Security Guidance Documentation

**Owner**: William Harrison
**Priority**: MEDIUM
**Estimated Time**: 8 hours
**Test Approach**: Documentation Creation + Review

#### Pre-Test Checklist
- [ ] Review current .env template (lines 191-205 in prerequisites doc)
- [ ] Identify missing security guidance
- [ ] Research best practices (password generation, permissions, etc.)

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-063** | Review current .env template | Read existing template | Identify missing security guidance | |
| **TC-064** | Add password generation guidance | Document `openssl rand -base64 32` | Clear password generation instructions | |
| **TC-065** | Add file permission requirements | Document `chmod 600 .env` requirement | Permission guidance included | |
| **TC-066** | Add .gitignore protection | Document version control protection | .gitignore guidance included | |
| **TC-067** | Add production secrets guidance | Document Vault, AWS, Azure options | Production-grade options documented | |
| **TC-068** | Test password generation command | Run documented command | Generates secure password | |
| **TC-069** | Review comprehensive guidance | Full template review | All security aspects covered | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Password generation commands documented
✅ **Criterion 2**: File permission requirements (600) documented
✅ **Criterion 3**: Version control protection (.gitignore) documented
✅ **Criterion 4**: Production secrets management options documented
✅ **Criterion 5**: Security guidance comprehensive and actionable

#### Success Metrics

- ✅ .env template includes all security guidance
- ✅ Password generation tested and verified
- ✅ Guidance meets PCI-DSS and SOC 2 requirements

#### Rollback Procedure

**If guidance creates confusion**:
1. Revert to original .env template
2. Identify confusing sections
3. Simplify or clarify guidance
4. Re-test with updated guidance

---

### ACTION-011: Standardize Exit Codes for CI/CD Integration

**Owner**: William Harrison
**Priority**: MEDIUM
**Estimated Time**: 2 hours
**Test Approach**: Exit Code Pattern Implementation

#### Pre-Test Checklist
- [ ] Review current exit code usage (0 for both success and warnings)
- [ ] Define exit code standard: 0=success, 2=warnings, 1=errors
- [ ] Identify scripts needing exit code updates

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-070** | Test success scenario (exit 0) | Run script, all checks pass | Script exits 0 | |
| **TC-071** | Test warning scenario (exit 2) | Run script, warnings present | Script exits 2 | |
| **TC-072** | Test error scenario (exit 1) | Run script, errors present | Script exits 1 | |
| **TC-073** | Test CI/CD warning gate | Simulate CI pipeline with exit 2 | Pipeline allows exit 2 as non-blocking | |
| **TC-074** | Update documentation | Document exit code standard | Clear CI/CD integration examples | |
| **TC-075** | Update GitLab CI examples | Add warning handling to CI config | CI config handles all 3 exit codes | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Exit code 0 = perfect success
✅ **Criterion 2**: Exit code 2 = success with warnings
✅ **Criterion 3**: Exit code 1 = failure/errors
✅ **Criterion 4**: CI/CD integration examples updated
✅ **Criterion 5**: Documentation clear on exit code usage

#### Success Metrics

- ✅ Exit codes distinguish success/warnings/errors
- ✅ CI/CD pipelines can implement warning gates
- ✅ Documentation includes working CI/CD examples

#### Rollback Procedure

**If exit code 2 causes issues**:
1. Revert to 0/1 exit codes
2. Document why exit 2 failed
3. Create alternative warning detection
4. Re-test with alternative

---

### ACTION-012: Clarify HTTPS Enforcement Status

**Owner**: William Harrison
**Priority**: LOW
**Estimated Time**: 2 hours
**Test Approach**: Configuration Verification + Documentation

#### Pre-Test Checklist
- [ ] Check nginx configuration for HTTP→HTTPS redirect
- [ ] Test HTTP access: http://n8n.hx.dev.local
- [ ] Review QA sign-off claims about HTTPS enforcement

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-076** | Test HTTP access | `curl -I http://n8n.hx.dev.local` | 301 redirect to HTTPS | |
| **TC-077** | Test HTTPS access | `curl -I https://n8n.hx.dev.local` | 200 OK | |
| **TC-078** | Review nginx config | Check nginx conf for redirect | Confirm 301 redirect configured | |
| **TC-079** | Update documentation | Document nginx redirect configuration | Clear statement of HTTP→HTTPS redirect | |
| **TC-080** | Add HTTP access test to sign-off | Update QA checklist | HTTP access test included | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: nginx 301 redirect configuration documented
✅ **Criterion 2**: HTTP access test added to sign-off checklist
✅ **Criterion 3**: Documentation clarifies HTTPS enforcement mechanism
✅ **Criterion 4**: No conflicting statements about HTTP accessibility

#### Success Metrics

- ✅ HTTP→HTTPS redirect verified and documented
- ✅ QA sign-off includes HTTP access test
- ✅ Documentation accurately reflects actual configuration

#### Rollback Procedure

**Not applicable** - Documentation-only action, no system changes.

---

### ACTION-013: Update Specification to Match Deployed Reality

**Owner**: Omar Rodriguez
**Priority**: LOW
**Estimated Time**: 1 hour
**Test Approach**: Documentation Reconciliation

#### Pre-Test Checklist
- [ ] Identify specification documents
- [ ] Compare specification to actual deployment
- [ ] List discrepancies

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-081** | Compare DB username (spec vs reality) | Read spec, check actual | Update spec: svc-n8n | |
| **TC-082** | Compare deployment path (spec vs reality) | Read spec, check actual | Update spec: /opt/n8n | |
| **TC-083** | Compare systemd service (spec vs reality) | Read spec, check actual | Update spec: n8n.service | |
| **TC-084** | Verify all updates | Read updated spec | Spec matches deployed reality | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Specification updated to match actual deployment
✅ **Criterion 2**: No discrepancies between spec and reality
✅ **Criterion 3**: Future deployments can reference accurate spec

#### Success Metrics

- ✅ 0 discrepancies between specification and deployment
- ✅ Specification reflects actual configuration
- ✅ Specification useful for future POCs

#### Rollback Procedure

**Not applicable** - Documentation-only action, no system changes.

---

### ACTION-014: Fix Backlog Count Inconsistency

**Owner**: Julia Santos
**Priority**: LOW
**Estimated Time**: 0.5 hours
**Test Approach**: Documentation Review

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-085** | Find inconsistent counts | Read backlog doc lines 1082, 1843 | 34 vs 35 identified | |
| **TC-086** | Count actual backlog items | Manual count of backlog | Determine correct count | |
| **TC-087** | Update all references | Update both lines to correct count | Consistent count throughout | |
| **TC-088** | Verify consistency | Read entire doc | No count mismatches | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Consistent backlog count throughout document
✅ **Criterion 2**: Count matches actual backlog items
✅ **Criterion 3**: No conflicting statements

#### Success Metrics

- ✅ 0 count inconsistencies
- ✅ Backlog count accurate

#### Rollback Procedure

**Not applicable** - Documentation-only action, no system changes.

---

### ACTION-015: Improve grep Pattern Robustness

**Owner**: William Harrison
**Priority**: LOW
**Estimated Time**: 0.5 hours
**Test Approach**: Pattern Testing

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-089** | Test current grep pattern | `grep "CodeRabbit"` (case-sensitive) | Misses "coderabbit", "CODERABBIT" | FAIL (as expected) |
| **TC-090** | Test improved pattern | `grep -iE "code\s*rabbit\|coderabbit"` | Matches all variations | PASS ✅ |
| **TC-091** | Update documentation | Replace grep pattern in CONSOLIDATED-ACTION-PLAN | Robust pattern documented | PASS ✅ |
| **TC-092** | Test on sample documents | Run on docs with varied capitalization | All CodeRabbit references found | PASS ✅ |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Case-insensitive grep pattern
✅ **Criterion 2**: Regex handles spacing variations
✅ **Criterion 3**: Documentation updated with robust pattern

#### Success Metrics

- ✅ Grep pattern catches all CodeRabbit variations
- ✅ No false negatives due to capitalization

#### Rollback Procedure

**Not applicable** - Documentation-only action, no system changes.

---

### ACTION-016: Update Stale Expected Output

**Owner**: Omar Rodriguez
**Priority**: LOW
**Estimated Time**: 0.5 hours
**Test Approach**: Documentation Update

#### Test Cases

| TC# | Test Case | Steps | Expected Result | Pass/Fail |
|-----|-----------|-------|-----------------|-----------|
| **TC-093** | Identify stale output | Read t-030, lines 121, 454 | "Files to update: 10000+" identified | |
| **TC-094** | Review actual command | Check v1.1 of task | File count operation removed | |
| **TC-095** | Remove stale output | Delete "Files to update" from expected | Expected output matches actual | |
| **TC-096** | Verify accuracy | Compare expected to actual execution | Output matches | |

#### Acceptance Criteria Validation

✅ **Criterion 1**: Expected output matches actual command output
✅ **Criterion 2**: No references to removed operations
✅ **Criterion 3**: Documentation reflects current task version

#### Success Metrics

- ✅ Expected output accurate
- ✅ No stale references

#### Rollback Procedure

**Not applicable** - Documentation-only action, no system changes.

---

## Integration Test Scenarios

### INT-001: Dependency Chain Testing

**Purpose**: Verify ACTION-006A must complete before ACTION-005 can start

**Test Steps**:
1. Complete ACTION-006A (infrastructure discovery)
2. Verify infrastructure type documented (FreeIPA or Samba AD)
3. Start ACTION-005 (SSL certificate transfer)
4. Verify SSL script references correct infrastructure
5. Confirm dependency satisfied

**Expected Result**: ACTION-005 cannot complete successfully without ACTION-006A findings

**Pass Criteria**: SSL transfer script uses correct infrastructure-specific commands

---

### INT-002: Credential Workflow Testing

**Purpose**: Verify database credential standardization flows through system

**Test Steps**:
1. Complete ACTION-009 (standardize username to svc-n8n)
2. Update ACTION-002 (database password prompts use svc-n8n)
3. Execute ACTION-004 (table validation uses svc-n8n)
4. Verify all database connections use consistent credentials

**Expected Result**: Single standardized username across all operations

**Pass Criteria**: `grep -r "n8n_user" .` returns 0 results, all connections use `svc-n8n`

---

### INT-003: Documentation Consistency Testing

**Purpose**: Verify documentation updates don't conflict

**Test Steps**:
1. Complete all documentation actions (007, 008, 009, 010, 012, 013)
2. Search for contradictory statements
3. Verify cross-references are accurate
4. Test that examples match documented procedures

**Expected Result**: 0 contradictions, all cross-references valid

**Pass Criteria**: Automated consistency scan passes, manual review confirms no conflicts

---

### INT-004: Exit Code CI/CD Integration

**Purpose**: Verify exit code standardization enables CI/CD gates

**Test Steps**:
1. Complete ACTION-011 (standardize exit codes)
2. Create mock GitLab CI pipeline
3. Test exit 0 (pipeline passes)
4. Test exit 2 (pipeline passes with warning)
5. Test exit 1 (pipeline fails)

**Expected Result**: CI pipeline distinguishes success/warnings/errors

**Pass Criteria**: Pipeline allows exit 2, blocks exit 1, passes exit 0

---

### INT-005: SSL Certificate Lifecycle Testing

**Purpose**: Verify certificate generation, transfer, and installation workflow

**Test Steps**:
1. Complete ACTION-006B (document generation procedure)
2. Generate test certificate using documented procedure
3. Complete ACTION-005 (transfer with error handling)
4. Transfer test certificate using enhanced script
5. Verify certificate installed and functional

**Expected Result**: Complete certificate lifecycle works end-to-end

**Pass Criteria**: Test certificate generates, transfers, and installs without errors

---

### INT-006: Build Test Validation Chain

**Purpose**: Verify build test fixes enable successful deployment validation

**Test Steps**:
1. Complete ACTION-001 (fix variable capture)
2. Execute build test with corrected code
3. Complete ACTION-003 (fix Linux compatibility)
4. Execute build test on Ubuntu 22.04
5. Verify all build tests pass

**Expected Result**: Build validation completes without errors

**Pass Criteria**: Build test script exits 0, all syntax checks pass

---

### INT-007: Database Validation Workflow

**Purpose**: Verify database validation enhancements work with credentials

**Test Steps**:
1. Complete ACTION-002 (fix password prompts)
2. Complete ACTION-004 (enhanced table validation)
3. Execute database validation without prompts
4. Verify all 50 tables validated correctly

**Expected Result**: Automated database validation completes successfully

**Pass Criteria**: Database validation script runs unattended, validates all 50 tables

---

### INT-008: Security Guidance Application

**Purpose**: Verify security guidance is consistent and actionable

**Test Steps**:
1. Complete ACTION-007 (.env permissions)
2. Complete ACTION-010 (.env security guidance)
3. Create new .env file following guidance
4. Verify permissions match documented requirements (600)
5. Test service can read secured .env file

**Expected Result**: Security guidance produces correct secure configuration

**Pass Criteria**: New .env file has 600 permissions, service reads it successfully

---

### INT-009: End-to-End Deployment Workflow

**Purpose**: Verify all fixes work together in complete deployment workflow

**Test Steps**:
1. Complete all HIGH priority actions (001-006B)
2. Execute complete deployment workflow
3. Verify build test works (ACTION-001, 003)
4. Verify database validation works (ACTION-002, 004)
5. Verify SSL transfer works (ACTION-005, 006A, 006B)
6. Confirm no errors in complete workflow

**Expected Result**: Complete deployment workflow executes without errors

**Pass Criteria**: All 18 actions integrate successfully, no workflow failures

---

### INT-010: Documentation Quality Improvements

**Purpose**: Verify all low-priority documentation fixes improve quality

**Test Steps**:
1. Complete ACTION-014 (backlog count)
2. Complete ACTION-015 (grep pattern)
3. Complete ACTION-016 (stale output)
4. Run documentation quality scan
5. Verify 0 quality issues remain

**Expected Result**: Documentation quality improved across all areas

**Pass Criteria**: Quality scan passes, no inconsistencies found

---

## Regression Test Suite

### Regression Testing Strategy

**Purpose**: Ensure fixes don't re-introduce original defects or CodeRabbit findings

**Coverage**:
- **7 Original Deployment Defects**: DEFECT-001 through DEFECT-007
- **51 CodeRabbit Remediation Documents**: All remediations must stay fixed
- **19 High-Priority Issues**: From REMEDIATION-LOG.md

### Original Defect Regression Tests

| Defect | Original Issue | Regression Test | Pass/Fail |
|--------|----------------|-----------------|-----------|
| **DEFECT-001** | TypeORM password URL encoding | Connect to DB with `Major8859` (no special chars) | |
| **DEFECT-002** | Systemd EnvironmentFile format | Service starts, reads .env correctly | |
| **DEFECT-003** | HTTP redirect missing | `curl http://n8n.hx.dev.local` → 301 redirect | |
| **DEFECT-004** | Winston warning | Warning acknowledged as cosmetic | |
| **DEFECT-005** | Domain name (kx→hx) | All docs reference hx.dev.local | |
| **DEFECT-006** | Login testing clarity | Clear login test procedure documented | |
| **DEFECT-007** | Manual workflow test | Deferred to user acceptance (documented) | |

### CodeRabbit Critical Findings Regression Tests

| Finding | Original Issue | Regression Test | Pass/Fail |
|---------|----------------|-----------------|-----------|
| **Variable Capture** | `syntax_output` undefined | Build test executes without error | |
| **Interactive Prompts** | 7 psql commands hang | All psql commands non-interactive | |
| **BSD stat** | Commands fail on Linux | All stat commands use GNU syntax | |
| **SSL Error Handling** | Silent failures | All operations logged and checked | |
| **DB Username** | Inconsistent (n8n_user vs svc-n8n) | All docs use svc-n8n | |
| **.env Permissions** | World-readable (644) | All .env files are 600 | |
| **Exit Codes** | Can't distinguish warnings | Exit 2 for warnings implemented | |
| **HTTPS Enforcement** | Ambiguous documentation | Clear nginx redirect documented | |

### Remediation Traceability Matrix

**Reference**: See `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/action-test-plan/REMEDIATION-TEST-MATRIX.md` for complete mapping of all 51 remediation documents to regression tests.

**Summary**:
- 51 CodeRabbit remediation documents
- 96 test cases covering all remediations
- 100% traceability: every remediation → test case

### Regression Test Execution

**Schedule**: Week 3, Day 3 (Wednesday)
**Owner**: Julia Santos
**Duration**: 4 hours
**Method**: Automated test suite + manual verification

**Automated Tests**: See Test Automation section for complete automated test suite.

---

## Compliance Validation

### Compliance Testing Strategy

**Frameworks**: PCI-DSS, SOC 2, NIST 800-53
**Purpose**: Verify remediation actions meet compliance requirements

### PCI-DSS 8.2.1: No Plaintext Passwords

| Requirement | Test | Expected Result | Pass/Fail |
|-------------|------|-----------------|-----------|
| **8.2.1.1** | Scan all docs for passwords | 0 plaintext passwords found | |
| **8.2.1.2** | Check .env file permissions | All .env files 600 (owner-only) | |
| **8.2.1.3** | Verify vault references | All docs reference credential vault | |
| **8.2.1.4** | Test password rotation | Procedure documented and tested | |

**Test Command**:
```bash
# Scan for password patterns
grep -rE 'Major[0-9]{4}!?' /srv/cc/Governance/x-poc3-n8n-deployment/
# Expected: 0 results (all replaced with vault references)
```

### SOC 2 CC6.7: Audit Logging

| Requirement | Test | Expected Result | Pass/Fail |
|-------------|------|-----------------|-----------|
| **CC6.7.1** | SSL transfer operations logged | All SCP/SSH logged with timestamps | |
| **CC6.7.2** | Credential access logged | Password vault access audited | |
| **CC6.7.3** | Configuration changes logged | .env permission changes logged | |
| **CC6.7.4** | Log retention policy | Logs retained per policy | |

**Test Command**:
```bash
# Verify SSL transfer script creates audit log
grep "log()" p3-tasks/p3.1-preparation/t-003-transfer-ssl-certificate.md
# Expected: Multiple logging statements present
```

### NIST 800-53 IA-5: Authenticator Management

| Requirement | Test | Expected Result | Pass/Fail |
|-------------|------|-----------------|-----------|
| **IA-5(1)** | Password complexity | Generation command uses secure random | |
| **IA-5(2)** | Credential storage | .env files encrypted or secured (600) | |
| **IA-5(3)** | Credential lifetime | Rotation policy documented | |
| **IA-5(7)** | Unencrypted credentials | .env files not world-readable | |

**Test Command**:
```bash
# Verify password generation uses cryptographic random
grep "openssl rand" p3-tasks/p3.1-preparation/t-001-prerequisites.md
# Expected: Password generation documented with openssl rand -base64
```

### Compliance Test Execution

**Schedule**: Week 3, Day 4 (Thursday)
**Owner**: Julia Santos + Frank Delgado
**Duration**: 4 hours
**Method**: Automated scans + manual policy review
**Prerequisite**: All actions 001-017 must be complete before compliance testing

---

## Performance Validation

### Performance Testing Strategy

**Purpose**: Verify actual time spent matches estimates (±20% tolerance)

**Total Estimated Time**: 58-62 hours
**Acceptable Range**: 46-74 hours (±20%)
**Method**: Track actual time per action, compare to estimates

### Performance Baselines

**Operation Performance Baselines** (added to validate operational efficiency):

| Operation | Baseline | Rationale |
|-----------|----------|-----------|
| Database table validation (50 tables) | <10 seconds | Should be simple SELECT queries |
| SSL certificate transfer | <30 seconds | Network transfer + chmod operations |
| File permission update (.env) | <5 seconds | Simple chmod/chown commands |
| Build test execution | <2 minutes | Node syntax check + validation |
| Documentation consistency scan | <30 seconds | Grep/find operations |
| Regression test suite | <5 minutes | Automated bash script execution |

**Variance Investigation Threshold**: >30% variance requires root cause analysis

### Time Tracking Template

| Action | Estimated | Actual | Variance | Status | Notes |
|--------|-----------|--------|----------|--------|-------|
| ACTION-001 | 2h | ___ | ___ | | |
| ACTION-002 | 1h | ___ | ___ | | |
| ACTION-003 | 4h | ___ | ___ | | |
| ACTION-004 | 3h | ___ | ___ | | |
| ACTION-005 | 8h | ___ | ___ | | |
| ACTION-006A | 4h | ___ | ___ | | |
| ACTION-006B | 6h | ___ | ___ | | |
| ACTION-007 | 2h | ___ | ___ | | |
| ACTION-008 | 4h | ___ | ___ | | |
| ACTION-009 | 2h | ___ | ___ | | |
| ACTION-010 | 8h | ___ | ___ | | |
| ACTION-011 | 2h | ___ | ___ | | |
| ACTION-012 | 2h | ___ | ___ | | |
| ACTION-013 | 1h | ___ | ___ | | |
| ACTION-014 | 0.5h | ___ | ___ | | |
| ACTION-015 | 0.5h | ___ | ___ | | |
| ACTION-016 | 0.5h | ___ | ___ | | |
| ACTION-017 | 2h | ___ | ___ | | |
| **TOTAL** | **58-62h** | **___** | **___** | | |

### Performance Metrics

**Key Metrics**:
- **Accuracy**: % of actions within ±20% of estimate
- **Total Variance**: Actual total vs estimated range
- **Longest Action**: Identify most time-consuming action
- **Shortest Action**: Identify quickest completions

**Target**: ≥80% of actions within ±20% of estimate

---

## Documentation Quality Tests

### Documentation Quality Strategy

**Purpose**: Ensure documentation meets Hana-X standards

**Standards Reference**:
- MVP Documentation Limits (IMPROVEMENT #2 from lessons-learned.md)
- 20/80 Planning/Building Rule (IMPROVEMENT #1)
- Clear, concise, actionable documentation

### Quality Test Cases

| Test | Criteria | Method | Pass/Fail |
|------|----------|--------|-----------|
| **DQ-001** | Length limits | Count lines: summaries ≤300, phase docs ≤600 | |
| **DQ-002** | No credentials | Scan for password patterns | |
| **DQ-003** | Consistency | Database username = svc-n8n everywhere | |
| **DQ-004** | Cross-references | All links valid and accurate | |
| **DQ-005** | Code examples | All examples tested and working | |
| **DQ-006** | Completeness | All required sections present | |
| **DQ-007** | Clarity | No ambiguous or contradictory statements | |
| **DQ-008** | Actionability | All procedures executable as written | |

### Enhanced Documentation Quality Tests

**Markdown Formatting**:
```bash
# Lint markdown files (if markdownlint installed)
markdownlint -c .markdownlint.json **/*.md
# Expected: 0 linting errors
```

**Metadata Completeness**:
```bash
# Check all docs have version, author, date
grep -L "Version:" p3-tasks/**/*.md
grep -L "Author:" p3-tasks/**/*.md
grep -L "Date:" p3-tasks/**/*.md
# Expected: 0 results (all docs have metadata)
```

### Length Limit Testing

```bash
# Test executive summaries (should be 50-300 lines)
wc -l */EXECUTIVE-SUMMARY.md | awk '$1 > 300 {print "❌ FAIL:", $2, "exceeds 300 lines"}'

# Test phase documents (should be 400-600 lines)
wc -l p*-*/quinn-*.md | awk '$1 > 600 {print "❌ FAIL:", $2, "exceeds 600 lines"}'
```

### Credential Scanning

```bash
# Scan for exposed passwords
grep -rE 'Major[0-9]{4}!?' p3-tasks/ p1-planning/ p7-post-deployment/
# Expected: 0 results (all credentials in vault references)
```

### Consistency Testing

```bash
# Verify database username standardization
grep -r "n8n_user" p1-planning/ p3-tasks/
# Expected: 0 results (all updated to svc-n8n)

# Verify deployment path consistency
grep -r "/srv/n8n" p3-tasks/ && grep -r "/opt/n8n" p3-tasks/
# Should use consistent path throughout
```

---

## Test Automation

### Automated Test Suite

**Purpose**: Automate repetitive validation tests

**Coverage**: 12% automation (15/120 total test operations)
- 10 regression tests (automated)
- 3 compliance tests (automated)
- 1 documentation quality test (automated)
- 1 pre-test validation script (automated)

**Realistic Automation Scope**: Focus on grep/find-based validations, file permission checks, and compliance scans. Manual testing required for integration scenarios, database validation, and SSL procedures.

### Pytest Test Suite

**Using pytest (our standard testing framework)** to provide structured, maintainable test automation with fixtures, parametrization, and detailed reporting.

**Location**: `/srv/tests/pytest/test_poc3_n8n.py`

```python
"""
POC3 N8N Deployment - Pytest Test Suite
Version: 1.0
Author: Julia Santos (QA Lead)

Test Categories:
- Regression tests (protect 7 defects + 51 CodeRabbit findings)
- Compliance tests (PCI-DSS, SOC 2, NIST)
- Documentation quality tests
"""

import pytest
import subprocess
import os
from pathlib import Path

# Pytest fixtures for test data and environment
@pytest.fixture
def project_root():
    """Return project root directory."""
    return Path("/srv/cc/Governance/x-poc3-n8n-deployment")

@pytest.fixture
def test_data_dir():
    """Return test data directory."""
    return Path("/srv/tests/data")

@pytest.fixture
def env_file_path():
    """Return .env file path for testing."""
    return Path("/opt/n8n/.env")


# Regression Tests
class TestRegression:
    """Regression tests to protect original defects and CodeRabbit findings."""

    def test_no_credentials_in_docs(self, project_root):
        """RT-001: Verify no plaintext credentials in documentation."""
        result = subprocess.run(
            ["grep", "-rE", r"Major[0-9]{4}!?", str(project_root / "p3-tasks")],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0, f"❌ FAIL: Credentials found in documentation:\n{result.stdout}"

    def test_env_file_permissions(self, env_file_path):
        """RT-002: Verify .env file has 600 permissions."""
        if env_file_path.exists():
            stat_info = env_file_path.stat()
            perms = oct(stat_info.st_mode)[-3:]
            assert perms == "600", f"❌ FAIL: .env permissions are {perms}, expected 600"

    def test_database_username_standardized(self, project_root):
        """RT-003: Verify database username standardized to svc-n8n."""
        result = subprocess.run(
            ["grep", "-r", "n8n_user", str(project_root / "p1-planning")],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0, f"❌ FAIL: Old username 'n8n_user' found:\n{result.stdout}"

    def test_no_bsd_stat_syntax(self, project_root):
        """RT-004: Verify no BSD stat syntax (should be GNU/Linux)."""
        result = subprocess.run(
            ["grep", "-r", "stat -f", str(project_root / "p3-tasks")],
            capture_output=True,
            text=True
        )
        assert result.returncode != 0, f"❌ FAIL: BSD stat syntax found:\n{result.stdout}"

    def test_no_interactive_psql(self, project_root):
        """RT-005: Verify all psql commands use PGPASSWORD (non-interactive)."""
        signoff_file = project_root / "p3-tasks/p3.6-validation/t-044-deployment-sign-off.md"
        if signoff_file.exists():
            result = subprocess.run(
                ["grep", "-E", r"psql.*-c", str(signoff_file)],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                # Check if all psql commands have PGPASSWORD
                for line in result.stdout.splitlines():
                    assert "PGPASSWORD" in line, f"❌ FAIL: Interactive psql found: {line}"


# Compliance Tests
class TestCompliance:
    """Compliance tests for PCI-DSS, SOC 2, NIST standards."""

    def test_pci_dss_no_plaintext_passwords(self, project_root):
        """CT-001: PCI-DSS 8.2.1 - No plaintext passwords."""
        result = subprocess.run(
            ["grep", "-rE", r"(password|passwd|pwd).*=.*[A-Za-z0-9!@#$%^&*]{8,}",
             str(project_root / "p3-tasks")],
            capture_output=True,
            text=True
        )
        # Filter out vault references
        if result.returncode == 0:
            matches = [line for line in result.stdout.splitlines() if "vault" not in line.lower()]
            assert len(matches) == 0, f"❌ FAIL: Plaintext passwords found (PCI-DSS violation):\n{chr(10).join(matches)}"

    def test_soc2_audit_logging(self, project_root):
        """CT-002: SOC 2 CC6.7 - Audit logging in SSL transfer script."""
        ssl_file = project_root / "p3-tasks/p3.1-preparation/t-003-transfer-ssl-certificate.md"
        if ssl_file.exists():
            content = ssl_file.read_text()
            assert "log(" in content, "❌ FAIL: No audit logging in SSL transfer script (SOC 2 violation)"

    def test_nist_password_generation(self, project_root):
        """CT-003: NIST 800-53 IA-5 - Password generation uses cryptographic random."""
        prereq_file = project_root / "p3-tasks/p3.1-preparation/t-001-prerequisites.md"
        if prereq_file.exists():
            content = prereq_file.read_text()
            assert "openssl rand" in content, "❌ FAIL: Password generation does not use cryptographic random (NIST violation)"


# Documentation Quality Tests
class TestDocumentationQuality:
    """Documentation quality tests."""

    def test_doc_length_limits(self, project_root):
        """DQ-001: Verify documentation adheres to length limits."""
        task_docs = (project_root / "p3-tasks").rglob("*.md")
        overlength = []
        for doc in task_docs:
            line_count = len(doc.read_text().splitlines())
            if line_count > 600:
                overlength.append(f"{doc.name}: {line_count} lines")

        assert len(overlength) == 0, f"❌ FAIL: {len(overlength)} documents exceed 600 line limit:\n{chr(10).join(overlength)}"

    def test_metadata_completeness(self, project_root):
        """DQ-002: Verify all task documents have metadata (version, author, date)."""
        task_docs = (project_root / "p3-tasks").rglob("t-*.md")
        missing_metadata = []

        for doc in task_docs:
            content = doc.read_text()
            if "Version:" not in content or "Author:" not in content:
                missing_metadata.append(doc.name)

        assert len(missing_metadata) == 0, f"❌ FAIL: {len(missing_metadata)} documents missing metadata:\n{chr(10).join(missing_metadata)}"


# Parametrized test example for testing multiple actions
@pytest.mark.parametrize("action_num,expected_owner", [
    ("001", "Omar"),
    ("002", "Quinn"),
    ("005", "Frank"),
    ("006A", "Frank"),
])
def test_action_ownership(action_num, expected_owner, project_root):
    """Verify action ownership documented correctly."""
    # This is an example of pytest parametrization
    # In practice, we'd read the action plan and verify owner
    pass


# Pytest configuration for reporting
if __name__ == "__main__":
    pytest.main([
        __file__,
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--html=/tmp/poc3-pytest-report.html",  # HTML report
        "--self-contained-html",  # Standalone HTML
    ])
```

**Pytest Configuration**: `/srv/tests/pytest/pytest.ini`

```ini
[pytest]
# Pytest configuration for POC3 N8N testing
testpaths = /srv/tests/pytest
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Reporting
addopts =
    -v
    --strict-markers
    --tb=short
    --html=/tmp/poc3-pytest-report.html
    --self-contained-html

# Markers
markers =
    regression: Regression tests protecting original defects
    compliance: Compliance tests (PCI-DSS, SOC 2, NIST)
    integration: Integration tests across actions
    smoke: Quick smoke tests for sanity checking
```

**Running Pytest Suite**:
```bash
# Run all tests
cd /srv/tests/pytest
pytest

# Run only regression tests
pytest -m regression

# Run only compliance tests
pytest -m compliance

# Generate detailed HTML report
pytest --html=/tmp/poc3-pytest-report.html --self-contained-html

# Run with coverage (if pytest-cov installed)
pytest --cov=/srv/cc/Governance/x-poc3-n8n-deployment
```

### Bash-Based Automated Test Script

**Purpose**: Lightweight automation for grep/find-based tests (complements pytest suite)

**Location**: `/srv/tests/automated-regression-suite.sh`

```bash
#!/bin/bash
# POC3 N8N Deployment - Automated Regression Test Suite
# Version: 1.1
# Author: Julia Santos (QA Lead)

set -euo pipefail

LOG_FILE="/tmp/poc3-test-results-$(date +%Y%m%d-%H%M%S).log"

log() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

fail_count=0
pass_count=0
warn_count=0

# Test Suite: Regression Tests
log "=== Starting Regression Test Suite ==="

# RT-001: No credentials in documentation
log "RT-001: Scanning for exposed credentials..."
if grep -rE 'Major[0-9]{4}!?' /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/ 2>/dev/null; then
  log "❌ FAIL RT-001: Credentials found in documentation"
  ((fail_count++))
else
  log "✅ PASS RT-001: No credentials found in documentation"
  ((pass_count++))
fi

# RT-002: .env file permissions
log "RT-002: Checking .env file permissions..."
if [ -f /opt/n8n/.env ]; then
  perms=$(stat -c%a /opt/n8n/.env)
  if [ "$perms" != "600" ]; then
    log "❌ FAIL RT-002: .env file has insecure permissions: $perms (expected 600)"
    ((fail_count++))
  else
    log "✅ PASS RT-002: .env file secured with 600 permissions"
    ((pass_count++))
  fi
else
  log "⚠️  WARN RT-002: .env file not found at /opt/n8n/.env"
  ((warn_count++))
fi

# RT-003: Database username consistency
log "RT-003: Checking database username standardization..."
if grep -r "n8n_user" /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/ 2>/dev/null; then
  log "❌ FAIL RT-003: Old username 'n8n_user' found in planning docs"
  ((fail_count++))
else
  log "✅ PASS RT-003: Database username standardized to svc-n8n"
  ((pass_count++))
fi

# RT-004: BSD stat compatibility
log "RT-004: Checking for BSD stat syntax..."
if grep -r "stat -f" /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/ 2>/dev/null; then
  log "❌ FAIL RT-004: BSD stat syntax found (not Linux-compatible)"
  ((fail_count++))
else
  log "✅ PASS RT-004: All stat commands use GNU/Linux syntax"
  ((pass_count++))
fi

# RT-005: Interactive psql prompts
log "RT-005: Checking for interactive psql commands..."
if grep -E "psql.*-c" /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.6-validation/t-044-deployment-sign-off.md 2>/dev/null | grep -v "PGPASSWORD"; then
  log "❌ FAIL RT-005: Interactive psql commands found (will hang automation)"
  ((fail_count++))
else
  log "✅ PASS RT-005: All psql commands use PGPASSWORD (non-interactive)"
  ((pass_count++))
fi

# RT-006: HTTP to HTTPS redirect
log "RT-006: Checking HTTP to HTTPS redirect..."
if command -v curl &> /dev/null; then
  http_response=$(curl -s -o /dev/null -w "%{http_code}" http://n8n.hx.dev.local 2>/dev/null || echo "000")
  if [ "$http_response" = "301" ] || [ "$http_response" = "302" ]; then
    log "✅ PASS RT-006: HTTP redirects to HTTPS (status $http_response)"
    ((pass_count++))
  else
    log "⚠️  WARN RT-006: HTTP response $http_response (expected 301/302 redirect)"
    ((warn_count++))
  fi
else
  log "⚠️  WARN RT-006: curl not available, skipping HTTP redirect test"
  ((warn_count++))
fi

# RT-007: Domain name consistency (hx.dev.local, not kx.dev.local)
log "RT-007: Checking domain name consistency..."
if grep -r "kx\.dev\.local" /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/ 2>/dev/null; then
  log "❌ FAIL RT-007: Old domain 'kx.dev.local' found (should be hx.dev.local)"
  ((fail_count++))
else
  log "✅ PASS RT-007: All references use correct domain (hx.dev.local)"
  ((pass_count++))
fi

# Test Suite: Compliance Tests
log "=== Starting Compliance Test Suite ==="

# CT-001: PCI-DSS 8.2.1 - No plaintext passwords
log "CT-001: PCI-DSS 8.2.1 - Scanning for plaintext passwords..."
if grep -rE '(password|passwd|pwd).*=.*[A-Za-z0-9!@#$%^&*]{8,}' /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/ 2>/dev/null | grep -v vault; then
  log "❌ FAIL CT-001: Plaintext passwords found (PCI-DSS violation)"
  ((fail_count++))
else
  log "✅ PASS CT-001: No plaintext passwords (PCI-DSS 8.2.1 compliant)"
  ((pass_count++))
fi

# CT-002: SOC 2 CC6.7 - Audit logging present
log "CT-002: SOC 2 CC6.7 - Checking SSL transfer audit logging..."
if [ -f /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-preparation/t-003-transfer-ssl-certificate.md ]; then
  if grep -q "log(" /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-preparation/t-003-transfer-ssl-certificate.md 2>/dev/null; then
    log "✅ PASS CT-002: Audit logging present in SSL transfer script (SOC 2 CC6.7)"
    ((pass_count++))
  else
    log "❌ FAIL CT-002: No audit logging in SSL transfer script (SOC 2 violation)"
    ((fail_count++))
  fi
else
  log "⚠️  WARN CT-002: SSL transfer script not found"
  ((warn_count++))
fi

# CT-003: NIST 800-53 IA-5 - Cryptographic password generation
log "CT-003: NIST 800-53 IA-5 - Checking password generation..."
if grep -q "openssl rand" /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-preparation/t-001-prerequisites.md 2>/dev/null; then
  log "✅ PASS CT-003: Password generation uses cryptographic random (NIST IA-5)"
  ((pass_count++))
else
  log "⚠️  WARN CT-003: openssl rand not found in prerequisites (may not be documented yet)"
  ((warn_count++))
fi

# Test Suite: Documentation Quality Tests
log "=== Starting Documentation Quality Test Suite ==="

# DQ-001: Documentation length limits
log "DQ-001: Checking documentation length limits..."
overlength_count=$(find /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/ -name "*.md" -exec wc -l {} \; | awk '$1 > 600 {print $2}' | wc -l)
if [ "$overlength_count" -gt 0 ]; then
  log "⚠️  WARN DQ-001: $overlength_count documents exceed 600 line limit"
  ((warn_count++))
else
  log "✅ PASS DQ-001: All documents within length limits"
  ((pass_count++))
fi

# Summary
log "=== Test Suite Complete ==="
log "PASSED: $pass_count tests"
log "FAILED: $fail_count tests"
log "WARNINGS: $warn_count tests"
log "TOTAL: $((pass_count + fail_count + warn_count)) tests"
log "Results logged to: $LOG_FILE"

# Exit code logic (implements ACTION-011 exit code standard)
if [ "$fail_count" -gt 0 ]; then
  log "EXIT CODE: 1 (failures present)"
  exit 1
elif [ "$warn_count" -gt 0 ]; then
  log "EXIT CODE: 2 (warnings present, no failures)"
  exit 2
else
  log "EXIT CODE: 0 (all tests passed)"
  exit 0
fi
```

### Pre-Test Environment Validation Script

**Location**: `/srv/tests/pre-test-validation.sh`

```bash
#!/bin/bash
# Pre-Test Environment Validation
# Verifies all prerequisites before test execution

set -euo pipefail

echo "=== Pre-Test Environment Validation ==="

# Check 1: SSH access to hx-n8n-server
echo "Check 1: SSH access to hx-n8n-server..."
if ssh agent0@hx-n8n-server "echo 'SSH OK'" 2>/dev/null; then
  echo "✅ SSH access: OK"
else
  echo "❌ SSH access: FAILED"
  exit 1
fi

# Check 2: Database connection
echo "Check 2: Database connection..."
if command -v psql &> /dev/null; then
  if PGPASSWORD="${DB_PASSWORD:-$(cat /srv/cc/Governance/0.2-credentials/hx-credentials.md | grep svc-n8n | awk '{print $2}')}" \
     psql -h hx-postgres-server -U svc-n8n -d n8n_poc3 -c "SELECT 1" &>/dev/null; then
    echo "✅ Database connection: OK"
  else
    echo "❌ Database connection: FAILED"
    exit 1
  fi
else
  echo "⚠️  psql not installed, skipping database check"
fi

# Check 3: N8N service operational
echo "Check 3: N8N service operational..."
if command -v curl &> /dev/null; then
  if curl -k -s -o /dev/null -w "%{http_code}" https://n8n.hx.dev.local | grep -q "200\|301\|302"; then
    echo "✅ N8N service: OK"
  else
    echo "❌ N8N service: FAILED"
    exit 1
  fi
else
  echo "⚠️  curl not installed, skipping N8N check"
fi

# Check 4: Test fixtures directory
echo "Check 4: Test fixtures directory..."
if [ -d /srv/tests/data ]; then
  echo "✅ Test fixtures: OK"
else
  echo "⚠️  Test fixtures directory missing, creating..."
  mkdir -p /srv/tests/data
  echo "✅ Test fixtures: Created"
fi

# Check 5: Git repository access
echo "Check 5: Git repository access..."
if cd /srv/cc/Governance && git status &>/dev/null; then
  echo "✅ Git repository: OK"
else
  echo "❌ Git repository: FAILED"
  exit 1
fi

echo "✅ Pre-test environment validation complete"
exit 0
```

### Test Automation Schedule

**Daily**: Run automated test suite during remediation work
**Weekly**: Full regression test suite + pytest suite
**Final**: Complete automated + manual test suite before sign-off

### Running the Automated Test Suite

**Bash Regression Suite**:
```bash
# Run regression test suite
cd /srv/tests
./automated-regression-suite.sh

# Output: Results logged to /tmp/poc3-test-results-YYYYMMDD-HHMMSS.log

# Exit Codes (per ACTION-011 standard):
# 0: All tests passed
# 1: One or more tests failed (blocking)
# 2: Warnings present, no failures (non-blocking)
```

**Pytest Suite**:
```bash
# Run pytest test suite
cd /srv/tests/pytest
pytest -v

# Generate HTML report
pytest --html=/tmp/poc3-pytest-report.html --self-contained-html

# Run specific test category
pytest -m regression  # Regression tests only
pytest -m compliance  # Compliance tests only
```

**Pre-Test Validation**:
```bash
# Run before any testing on Week 1, Day 1
cd /srv/tests
./pre-test-validation.sh
```

---

## Sign-Off Criteria

### Final QA Sign-Off Requirements

The POC3 N8N Deployment remediation is complete when:

#### 1. Action Completion (100%)
- [ ] All 18 actions completed (ACTION-001 through ACTION-017)
- [ ] All acceptance criteria met for each action
- [ ] All deliverables produced and verified

#### 2. Regression Testing (100%)
- [ ] No regression of 7 original deployment defects
- [ ] No regression of 51 CodeRabbit remediation items
- [ ] All regression tests pass automated suite

#### 3. Compliance Validation (100%)
- [ ] PCI-DSS 8.2.1: 0 plaintext passwords in documentation
- [ ] SOC 2 CC6.7: Audit logging present on critical operations
- [ ] NIST 800-53 IA-5: Credentials properly secured (600 permissions)

#### 4. Integration Testing (100%)
- [ ] All dependency chains validated (006A → 005, etc.)
- [ ] Cross-action integration scenarios pass
- [ ] End-to-end workflows functional

#### 5. Documentation Quality (100%)
- [ ] Length limits enforced (summaries ≤300, phase docs ≤600) OR exception documented
- [ ] 0 credentials in version control
- [ ] Database username standardized (svc-n8n everywhere)
- [ ] Cross-references valid and accurate
- [ ] No contradictory statements

#### 6. Performance Validation (≥80%)
- [ ] ≥80% of actions within ±20% of time estimate
- [ ] Total time within 46-74 hours (58-62h ±20%)
- [ ] Time variance documented and explained
- [ ] Performance baselines met (database <10s, SSL transfer <30s, etc.)

#### 7. Process Improvements (100%)
- [ ] All 8 process improvements have assigned owners
- [ ] Success criteria defined for each improvement
- [ ] Implementation timeline set for POC4
- [ ] Owners have acknowledged assignments

#### 8. Traceability (100%)
- [ ] All 51 remediation documents mapped to actions (see REMEDIATION-TEST-MATRIX.md)
- [ ] All actions traced to original issues
- [ ] Audit trail complete from issue → remediation → action → test → verification

#### 9. Stakeholder Approval
- [ ] Julia Santos (QA Lead) - Sign-off on quality
- [ ] Frank Delgado (Infrastructure) - Sign-off on SSL/infrastructure actions
- [ ] Quinn Baker (Database) - Sign-off on database actions
- [ ] Omar Rodriguez (Build) - Sign-off on build/deployment actions
- [ ] William Harrison (SysAdmin) - Sign-off on documentation/automation actions
- [ ] Alex Rivera (Architect) - Sign-off on architectural compliance

#### 10. Final Verification
- [ ] N8N service operational at https://n8n.hx.dev.local
- [ ] Database connectivity verified
- [ ] LDAP authentication functional
- [ ] No blocking issues remain
- [ ] All documentation published to git repository
- [ ] Database backup created and verified

### Pass Rate Calculation

**Formula**:
```
Pass Rate = (Passed Test Cases) / (Total Test Cases) × 100%
```

**Category-Specific Requirements**:
- **Unit Tests (96 test cases)**: ≥90% pass required (critical action validation)
- **Integration Tests (10 scenarios)**: 100% pass required (all dependencies must work)
- **Regression Tests (automated suite)**: 100% pass required (no defect regressions allowed)
- **Compliance Tests (12 checks)**: 100% pass required (non-negotiable)
- **Documentation Tests (8 checks)**: ≥95% pass required

**Overall Requirement**: ≥95% total pass rate across all categories

**Failure Tolerance**: Maximum 5 test case failures allowed (out of 96), provided:
- No failures in HIGH priority actions (001-006B, 017)
- No compliance failures
- No integration test failures
- Failures limited to LOW priority actions (014, 015, 016)

---

## Sign-Off Form

### POC3 N8N Deployment - Test & Validation Sign-Off

**Project**: POC3 N8N Deployment Post-Deployment Remediation
**Test Plan Version**: 1.1
**Date**: _________________

#### Test Execution Summary

| Category | Test Cases | Passed | Failed | % Passed |
|----------|------------|--------|--------|----------|
| Action Unit Tests | 96 | ___ | ___ | ___% |
| Integration Tests | 10 | ___ | ___ | ___% |
| Regression Tests (Automated) | 15 | ___ | ___ | ___% |
| Compliance Tests | 12 | ___ | ___ | ___% |
| Performance Tests | 18 | ___ | ___ | ___% |
| Documentation Tests | 8 | ___ | ___ | ___% |
| **TOTAL** | **159** | **___** | **___** | **___%** |

**Overall Pass Rate**: ______%
**Required for Sign-Off**: ≥95%

#### Defect Summary

**Defects Found**: ___
**Defects Resolved**: ___
**Defects Deferred**: ___
**Blocking Defects Remaining**: ___

**Defect Log**: `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/action-test-plan/TEST-DEFECT-LOG.md`

#### Time Validation

**Total Estimated**: 58-62 hours
**Total Actual**: ______ hours
**Variance**: ______%
**Within Acceptable Range (±20%)?**: ☐ YES ☐ NO

#### Sign-Off Approvals

| Role | Name | Approval | Date | Signature |
|------|------|----------|------|-----------|
| **QA Lead** | Julia Santos | ☐ APPROVED ☐ REJECTED | ____ | _________ |
| **Infrastructure** | Frank Delgado | ☐ APPROVED ☐ REJECTED | ____ | _________ |
| **Database** | Quinn Baker | ☐ APPROVED ☐ REJECTED | ____ | _________ |
| **Build** | Omar Rodriguez | ☐ APPROVED ☐ REJECTED | ____ | _________ |
| **SysAdmin** | William Harrison | ☐ APPROVED ☐ REJECTED | ____ | _________ |
| **Architect** | Alex Rivera | ☐ APPROVED ☐ REJECTED | ____ | _________ |

#### Final Status

☐ **APPROVED** - All sign-off criteria met, remediation complete
☐ **CONDITIONAL** - Minor issues, approved with action items
☐ **REJECTED** - Major issues, additional remediation required

**Notes**: _________________________________________________________________

---

## Cross-References

### Related Documentation

| Document | Location | Purpose |
|----------|----------|---------|
| **Consolidated Action Plan v3.1** | `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/CONSOLIDATED-ACTION-PLAN.md` | Source document for all test cases |
| **Remediation Log** | `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/REMEDIATION-LOG.md` | 19 high-priority issues |
| **51 Remediation Documents** | `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/remediations/` | Detailed remediation guidance |
| **Remediation Test Matrix** | `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/action-test-plan/REMEDIATION-TEST-MATRIX.md` | Complete mapping of 51 remediations to tests |
| **Lessons Learned** | `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/lessons-learned.md` | Process improvements for POC4 |
| **Defect Log** | `/srv/cc/Governance/x-poc3-n8n-deployment/p4-validation/issues-log.md` | 7 original deployment defects |
| **Test Defect Log** | `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/action-test-plan/TEST-DEFECT-LOG.md` | Defects found during testing phase |
| **Credential Vault** | `/srv/cc/Governance/0.2-credentials/hx-credentials.md` | Secure credential storage |
| **Julia's Review (v1.0)** | `/srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/action-test-plan/JULIA-REVIEW-TEST-PLAN.md` | Critical QA review identifying 32 issues |

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-09 | **Initial test/validation plan created**. Comprehensive test coverage for all 18 actions in Consolidated Action Plan v3.1. Includes 214 test cases (claimed) across 6 categories. Defined sign-off criteria requiring ≥95% pass rate. | Julia Santos (QA Lead) |
| 1.1 | 2025-11-09 | **MANDATORY FIXES APPLIED** based on critical QA review. **CRITICAL-001**: Updated test case count to realistic 96 detailed test cases + automated suite (was 214 inflated). **CRITICAL-002**: Reduced automation scope to 12% (15 automated tests) from unrealistic 40% claim. **CRITICAL-003**: Added test data infrastructure section with fixtures at `/srv/tests/data/`. **CRITICAL-004**: Fixed dependency schedule - swapped Week 1 Thu/Fri so ACTION-006A executes before ACTION-005. **CRITICAL-005**: Added pytest test suite leveraging Julia's expertise. **HIGH-001**: Added rollback procedures for all 18 actions. **HIGH-002**: Added database backup procedure and test environment isolation strategy. **HIGH-003**: Clarified pass rate calculation with formula and category-specific requirements. **HIGH-004**: Added defect tracking reference and defect summary to sign-off. **HIGH-005**: Added agent availability to pre-test checklist. **HIGH-006**: Updated compliance test timing to Week 3 Day 4 after all actions complete. **HIGH-007**: Added dependency column to timeline, marked sequential vs parallel execution. **HIGH-008**: Added remediation traceability matrix reference for 51 CodeRabbit docs. **MEDIUM-002**: Added performance baselines for operations. **MEDIUM-003**: Added enhanced documentation quality tests (metadata, markdown linting). **MEDIUM-005**: Clarified test execution roles in pre-test checklist. **MEDIUM-006**: Updated automated script to use exit 2 for warnings per ACTION-011. **MEDIUM-007**: Added pre-test validation script. **MEDIUM-008**: Added priority levels to ACTION-008 test validation. **MEDIUM-012**: Added documentation for running automated test suite. Timeline extended to 3.5-4 weeks (added Week 4 contingency). Test plan now execution-ready with realistic scope and comprehensive quality standards. | Julia Santos (QA Lead) |

---

## Summary

This test and validation plan provides comprehensive coverage for the POC3 N8N Deployment remediation effort. With **96 detailed test cases + automated test suite** across **6 test categories**, it ensures:

✅ **100% Action Coverage**: Every action from 001-017 has detailed test cases with rollback procedures
✅ **Complete Regression Testing**: All 7 defects + 51 CodeRabbit findings protected via automated suite
✅ **Compliance Validation**: PCI-DSS, SOC 2, NIST requirements verified with automated scans
✅ **Performance Tracking**: Time estimates validated against actuals with performance baselines
✅ **Documentation Quality**: Consistency, accuracy, and standards enforced via pytest and bash scripts
✅ **Integration Testing**: Dependencies and workflows validated end-to-end with 10 integration scenarios
✅ **Pytest Framework**: Structured, maintainable test automation leveraging Julia's core competency
✅ **Test Data Infrastructure**: Complete test fixtures and mock data at `/srv/tests/data/`
✅ **Realistic Automation**: 12% automation (15 automated tests) focused on grep/find validations

**Test Automation**: 12% automation (15 automated tests) using pytest + bash scripts
**Success Criteria**: ≥95% pass rate + ≥80% time accuracy + 100% stakeholder approval
**Timeline**: 3.5-4 weeks with Week 4 contingency for defect remediation

**Key Improvements in v1.1**:
- Accurate test case count (96 detailed + automated suite)
- Realistic automation scope (12% vs 40% claimed)
- Test data infrastructure defined
- Dependency schedule fixed (006A before 005)
- Pytest integration for structured testing
- Rollback procedures for all actions
- Database backup and test isolation
- Clear pass rate calculation
- Defect tracking integrated
- Performance baselines defined
- Enhanced documentation quality tests

**Ready for execution** ✅
