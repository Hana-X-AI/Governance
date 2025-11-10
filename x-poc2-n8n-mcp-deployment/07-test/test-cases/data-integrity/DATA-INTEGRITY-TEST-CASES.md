# Data Integrity Test Cases

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | POC-002-TC-DATA-001 |
| **Version** | 1.0 |
| **Created** | 2025-11-06 |
| **Test Suite** | Data Integrity Tests |
| **Total Test Cases** | 25 |
| **Automation** | 85% |
| **Priority** | High |
| **Phase** | Phase 2 |

---

## Test Suite Overview

**Objective**: Validate data consistency, validation, transaction integrity, and state management.

**Scope**:
- Data validation and schema compliance
- State consistency between MCP and N8N
- Transaction integrity
- Rollback scenarios
- Data corruption prevention

**Related Acceptance Criteria**: AC9

---

## Data Validation Test Cases (8 test cases)

### TC-DATA-001: Workflow Data Validation

**Priority**: Critical | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify workflow data validates against N8N schema.

**Test Steps**:
1. Create workflow via MCP
2. Get workflow details
3. Validate all fields match N8N schema:
   - Required fields present
   - Data types correct
   - Enum values valid

**Expected Results**:
- All data valid
- No schema violations

**Related AC**: AC9

---

### TC-DATA-002: Credential Data Validation

**Priority**: Critical | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify credential data validation.

**Test Steps**:
1. Create credential with all required fields
2. Attempt create with missing required field
3. Attempt create with invalid field type
4. Verify validation

**Expected Results**:
- Valid credentials accepted
- Invalid credentials rejected with clear error

**Related AC**: AC6

---

### TC-DATA-003: Project Data Validation

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify project data validation.

**Test Steps**:
1. Create project with valid data
2. Attempt create with invalid project type
3. Attempt create with missing name
4. Verify validation

**Expected Results**:
- Validation enforced
- Clear error messages

**Related AC**: AC3

---

### TC-DATA-004: Tag Data Validation

**Priority**: Medium | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify tag format validation.

**Test Steps**:
1. Add tags with valid format
2. Attempt invalid tag formats:
   - Empty string
   - Special characters
   - Very long strings (1000+ chars)

**Expected Results**:
- Valid tags accepted
- Invalid tags rejected

**Related AC**: AC3

---

### TC-DATA-005: Webhook Path Validation

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify webhook path validation.

**Test Steps**:
1. Create webhook with valid path
2. Attempt invalid paths:
   - Spaces in path
   - Invalid characters
   - Duplicate paths

**Expected Results**:
- Validation enforced
- Duplicates prevented

**Related AC**: AC5

---

### TC-DATA-006: Node Configuration Validation

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify workflow node configuration validation.

**Test Steps**:
1. Create workflow with valid node configuration
2. Attempt invalid node configuration:
   - Unknown node type
   - Missing required parameters
   - Invalid parameter values

**Expected Results**:
- Validation enforced
- Clear error messages

**Related AC**: AC7

---

### TC-DATA-007: Execution Data Completeness

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify execution data is complete.

**Test Steps**:
1. Execute workflow
2. Get execution details
3. Verify all expected fields present:
   - Workflow ID
   - Status
   - Start/end times
   - Node results
   - Error info (if failed)

**Expected Results**:
- All data fields present
- No missing information

**Related AC**: AC4

---

### TC-DATA-008: Special Character Handling

**Priority**: Medium | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify special characters handled correctly.

**Test Steps**:
1. Create entities with special characters in names:
   - Unicode characters
   - Emojis
   - HTML entities
   - SQL injection attempts
2. Retrieve and verify

**Expected Results**:
- Special characters preserved
- No injection vulnerabilities
- Data retrieved correctly

**Related AC**: AC9

---

## State Consistency Test Cases (7 test cases)

### TC-DATA-009: MCP to N8N Consistency

**Priority**: Critical | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify data consistency between MCP and N8N.

**Test Steps**:
1. Create workflow via MCP
2. Retrieve via N8N API
3. Compare all fields
4. Update via MCP
5. Verify update in N8N

**Expected Results**:
- Data identical in both systems
- Updates synchronized

**Related AC**: AC9

---

### TC-DATA-010: N8N to MCP Consistency

**Priority**: Critical | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: No (Manual)

**Objective**: Verify MCP reflects N8N UI changes.

**Test Steps**:
1. Create workflow in N8N UI
2. Retrieve via MCP
3. Compare data
4. Update in N8N UI
5. Verify via MCP

**Expected Results**:
- MCP shows N8N changes
- Data consistent

**Related AC**: AC9

---

### TC-DATA-011: Workflow Activation State Consistency

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify workflow active state consistent.

**Test Steps**:
1. Create workflow (inactive)
2. Verify inactive via MCP and N8N
3. Activate via MCP
4. Verify active in both systems

**Expected Results**:
- State synchronized
- Activation status consistent

**Related AC**: AC9

---

### TC-DATA-012: Credential Reference Consistency

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify credential references remain valid.

**Test Steps**:
1. Create credential
2. Create workflow using credential
3. Verify credential reference in workflow
4. Update credential
5. Verify workflow still references correctly

**Expected Results**:
- References valid
- Updates don't break references

**Related AC**: AC6

---

### TC-DATA-013: Tag Synchronization

**Priority**: Medium | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify tags synchronized between MCP and N8N.

**Test Steps**:
1. Add tags via MCP
2. Verify tags in N8N
3. Remove tags via MCP
4. Verify removal in N8N

**Expected Results**:
- Tags synchronized
- Operations reflected in both systems

**Related AC**: AC3

---

### TC-DATA-014: Execution History Consistency

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify execution history consistent.

**Test Steps**:
1. Execute workflow multiple times
2. List executions via MCP
3. Compare with N8N execution list
4. Verify counts and details match

**Expected Results**:
- Execution counts match
- Details identical

**Related AC**: AC4

---

### TC-DATA-015: Project Assignment Consistency

**Priority**: Medium | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify project assignments consistent.

**Test Steps**:
1. Create project
2. Assign workflows to project
3. Verify assignment in N8N
4. Remove workflows from project
5. Verify removal in N8N

**Expected Results**:
- Assignments synchronized
- Project membership accurate

**Related AC**: AC3

---

## Transaction Integrity Test Cases (5 test cases)

### TC-DATA-016: Atomic Workflow Creation

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify workflow creation is atomic.

**Test Steps**:
1. Create workflow with complex configuration
2. If creation fails, verify no partial workflow created
3. If creation succeeds, verify workflow complete

**Expected Results**:
- Either full success or full failure
- No partial/corrupted workflows

**Related AC**: AC9

---

### TC-DATA-017: Atomic Credential Update

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify credential updates are atomic.

**Test Steps**:
1. Update credential with multiple fields
2. If update fails, verify original state preserved
3. If succeeds, verify all fields updated

**Expected Results**:
- Atomic updates
- No partial updates

**Related AC**: AC6

---

### TC-DATA-018: Workflow Deletion Integrity

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify workflow deletion is clean.

**Test Steps**:
1. Create workflow with tags, in project
2. Delete workflow
3. Verify:
   - Workflow removed
   - Tags removed
   - Project association removed
   - Execution history handling

**Expected Results**:
- Clean deletion
- No orphaned data

**Related AC**: AC9

---

### TC-DATA-019: Cascading Delete Behavior

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify cascading deletes handled correctly.

**Test Steps**:
1. Create project with workflows
2. Delete project
3. Verify workflow handling (cascade or prevent)
4. Create credential used by workflows
5. Attempt delete credential
6. Verify prevention or cascade

**Expected Results**:
- Cascading deletes documented
- Or prevention with clear error

**Related AC**: AC9

---

### TC-DATA-020: Transaction Rollback

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify failed operations rollback correctly.

**Test Steps**:
1. Get current state
2. Attempt invalid operation that should fail
3. Verify state unchanged (rollback)

**Expected Results**:
- Failed operations don't corrupt data
- State rolled back

**Related AC**: AC8, AC9

---

## Data Corruption Prevention Test Cases (5 test cases)

### TC-DATA-021: Concurrent Update Protection

**Priority**: Critical | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Prevent data corruption from concurrent updates.

**Test Steps**:
1. Two clients get same workflow
2. Both update workflow simultaneously
3. Verify data integrity

**Expected Results**:
- Either: Optimistic locking (one succeeds, one fails)
- Or: Last write wins (documented)
- No data corruption

**Related AC**: AC9

---

### TC-DATA-022: Invalid JSON Rejection

**Priority**: High | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify invalid data rejected.

**Test Steps**:
1. Attempt to create workflow with malformed JSON
2. Verify rejection

**Expected Results**:
- Invalid data rejected
- Clear error message
- No data corruption

**Related AC**: AC8, AC9

---

### TC-DATA-023: Schema Migration Safety

**Priority**: Medium | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: No (Manual)

**Objective**: Verify data preserved during schema changes.

**Test Steps**:
1. Create data with current schema
2. Upgrade N8N version (simulated schema change)
3. Verify data still accessible via MCP

**Expected Results**:
- Data preserved
- Backward compatibility maintained

**Related AC**: AC9

---

### TC-DATA-024: Large Payload Handling

**Priority**: Medium | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify large payloads don't corrupt data.

**Test Steps**:
1. Create workflow with very large configuration (100+ nodes)
2. Create credential with large data
3. Verify data integrity

**Expected Results**:
- Large payloads handled correctly
- No truncation or corruption

**Related AC**: AC9

---

### TC-DATA-025: Encoding Preservation

**Priority**: Medium | **Type**: Data Integrity | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify character encoding preserved.

**Test Steps**:
1. Create entities with various character encodings:
   - UTF-8
   - UTF-16
   - Special characters
2. Retrieve and verify encoding preserved

**Expected Results**:
- Encoding preserved
- No character corruption

**Related AC**: AC9

---

## Test Suite Summary

**Total Test Cases**: 25

**By Category**:
- Data Validation: 8 test cases
- State Consistency: 7 test cases
- Transaction Integrity: 5 test cases
- Corruption Prevention: 5 test cases

**By Priority**:
- Critical: 6
- High: 14
- Medium: 5

**By Phase**:
- Phase 2: 25 test cases (100%)

**Automation**: 85% (21 automated, 4 manual)

---

**Document Type**: Test Case Documentation
**Version**: 1.0
**Created**: 2025-11-06
**Location**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test/test-cases/data-integrity/DATA-INTEGRITY-TEST-CASES.md`
