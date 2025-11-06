# Management Tools Test Cases

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | POC-002-TC-MGT-001 |
| **Version** | 1.0 |
| **Created** | 2025-11-06 |
| **Test Suite** | Management Tools |
| **Total Test Cases** | 35 |
| **Automation** | 95% |
| **Priority** | Critical |
| **Phase** | Phase 1 & Phase 2 |

---

## Test Suite Overview

**Objective**: Validate all 5 management-related MCP tools for N8N infrastructure management.

**Tools Under Test**:
1. `list_node_types` - Discover available nodes
2. `manage_credentials` - Credential management
3. `manage_webhooks` - Webhook configuration
4. `list_executions` - Execution history
5. `get_execution_details` - Detailed execution information

**Related Acceptance Criteria**: AC5, AC6, AC7

---

## list_node_types Tool Test Cases (7 test cases)

### TC-MGT-001: List All Node Types

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify `list_node_types` returns all available node types.

**Test Steps**:
1. Call `list_node_types` with no filters

**Expected Results**:
- Returns array of node types
- Each node includes: name, displayName, description, version, inputs, outputs

**Related AC**: AC7

---

### TC-MGT-002: Filter Node Types by Category

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify filtering nodes by category.

**Test Steps**:
1. Call `list_node_types` with category filter

**Expected Results**:
- Only nodes from specified category returned

**Related AC**: AC7

---

### TC-MGT-003: Search Node Types by Name

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify searching nodes by name.

**Test Steps**:
1. Call `list_node_types` with search term

**Expected Results**:
- Returns nodes matching search term

**Related AC**: AC7

---

### TC-MGT-004: Get Node Type Details

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify detailed node information.

**Test Steps**:
1. Get specific node type details

**Expected Results**:
- Returns complete node schema
- Includes parameters, credentials, webhooks

**Related AC**: AC7

---

### TC-MGT-005: List Core vs Custom Nodes

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify distinction between core and custom nodes.

**Test Steps**:
1. List all nodes
2. Identify core vs custom

**Expected Results**:
- Core nodes identified
- Custom nodes identified

**Related AC**: AC7

---

### TC-MGT-006: Node Type Versioning

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify node version information.

**Test Steps**:
1. Get node types
2. Verify version field

**Expected Results**:
- Each node has version
- Version format valid

**Related AC**: AC7

---

### TC-MGT-007: Empty Search Results

**Priority**: Low | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify behavior when search matches no nodes.

**Test Steps**:
1. Search with term matching no nodes

**Expected Results**:
- Returns empty array
- No error

**Related AC**: AC7

---

## manage_credentials Tool Test Cases (10 test cases)

### TC-MGT-008: Create Credential Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify credential creation.

**Test Steps**:
1. Call `manage_credentials`:
   ```json
   {
     "action": "create",
     "type": "httpBasicAuth",
     "name": "Test Credential",
     "data": {
       "user": "testuser",
       "password": "testpass"
     }
   }
   ```

**Expected Results**:
- Credential created
- Returns credential ID
- Password encrypted

**Related AC**: AC6

---

### TC-MGT-009: List Credentials Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify listing credentials.

**Test Steps**:
1. Call `manage_credentials` with `action: "list"`

**Expected Results**:
- Returns array of credentials
- Each has: id, name, type
- Sensitive data not exposed

**Related AC**: AC6

---

### TC-MGT-010: Update Credential Success

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify credential update.

**Test Steps**:
1. Create credential
2. Update credential data

**Expected Results**:
- Credential updated
- Changes reflected

**Related AC**: AC6

---

### TC-MGT-011: Delete Credential Success

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify credential deletion.

**Test Steps**:
1. Create credential
2. Delete credential
3. Verify not in list

**Expected Results**:
- Credential deleted
- No longer accessible

**Related AC**: AC6

---

### TC-MGT-012: Get Credential Details (Without Sensitive Data)

**Priority**: High | **Type**: Security | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify sensitive data not exposed.

**Test Steps**:
1. Get credential details

**Expected Results**:
- Returns metadata
- Passwords/secrets masked or omitted

**Related AC**: AC6

---

### TC-MGT-013: Test Credential Connection

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify credential validation.

**Test Steps**:
1. Create credential
2. Test connection

**Expected Results**:
- Connection test succeeds for valid credentials
- Fails for invalid

**Related AC**: AC6

---

### TC-MGT-014: Create Duplicate Credential Name

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify handling of duplicate names.

**Test Steps**:
1. Create credential
2. Create another with same name

**Expected Results**:
- Either: Allowed (with warning)
- Or: Error (name conflict)

**Related AC**: AC6

---

### TC-MGT-015: Delete Credential In Use

**Priority**: High | **Type**: Negative | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify protection of credentials in use.

**Test Steps**:
1. Create workflow using credential
2. Try to delete credential

**Expected Results**:
- Error: credential in use
- Or: Cascade warning

**Related AC**: AC6, AC8

---

### TC-MGT-016: Invalid Credential Type

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify validation of credential type.

**Test Steps**:
1. Create credential with invalid type

**Expected Results**:
- Error: invalid credential type

**Related AC**: AC6, AC8

---

### TC-MGT-017: Missing Required Credential Fields

**Priority**: High | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify validation of required fields.

**Test Steps**:
1. Create credential missing required data

**Expected Results**:
- Error: missing required fields

**Related AC**: AC6, AC8

---

## manage_webhooks Tool Test Cases (8 test cases)

### TC-MGT-018: Create Webhook Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify webhook creation.

**Test Steps**:
1. Call `manage_webhooks`:
   ```json
   {
     "action": "create",
     "workflowId": "<id>",
     "path": "test-webhook",
     "method": "POST"
   }
   ```

**Expected Results**:
- Webhook created
- Returns webhook URL

**Related AC**: AC5

---

### TC-MGT-019: List Webhooks Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify listing webhooks.

**Test Steps**:
1. Call `manage_webhooks` with `action: "list"`

**Expected Results**:
- Returns array of webhooks
- Each has: id, path, method, workflowId, isActive

**Related AC**: AC5

---

### TC-MGT-020: Update Webhook Success

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify webhook update.

**Test Steps**:
1. Create webhook
2. Update webhook path/method

**Expected Results**:
- Webhook updated
- Changes reflected

**Related AC**: AC5

---

### TC-MGT-021: Delete Webhook Success

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify webhook deletion.

**Test Steps**:
1. Create webhook
2. Delete webhook

**Expected Results**:
- Webhook deleted
- No longer in list

**Related AC**: AC5

---

### TC-MGT-022: Activate/Deactivate Webhook

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify webhook activation control.

**Test Steps**:
1. Create webhook
2. Deactivate webhook
3. Activate webhook

**Expected Results**:
- Status changes correctly
- Active webhooks receive requests
- Inactive webhooks do not

**Related AC**: AC5

---

### TC-MGT-023: Webhook Duplicate Path

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify handling of duplicate paths.

**Test Steps**:
1. Create webhook with path
2. Create another with same path

**Expected Results**:
- Error: path conflict

**Related AC**: AC5, AC8

---

### TC-MGT-024: Invalid Webhook Method

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify validation of HTTP methods.

**Test Steps**:
1. Create webhook with invalid method

**Expected Results**:
- Error: invalid method

**Related AC**: AC5, AC8

---

### TC-MGT-025: Webhook for Non-Existent Workflow

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify validation of workflow ID.

**Test Steps**:
1. Create webhook with invalid workflow ID

**Expected Results**:
- Error: workflow not found

**Related AC**: AC5, AC8

---

## list_executions Tool Test Cases (5 test cases)

### TC-MGT-026: List All Executions

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify listing execution history.

**Test Steps**:
1. Call `list_executions` with no filters

**Expected Results**:
- Returns array of executions
- Each has: id, workflowId, status, startedAt, finishedAt

**Related AC**: AC4

---

### TC-MGT-027: Filter Executions by Workflow

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify filtering by workflow ID.

**Test Steps**:
1. Call `list_executions` with workflow ID filter

**Expected Results**:
- Only executions for specified workflow returned

**Related AC**: AC4

---

### TC-MGT-028: Filter Executions by Status

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify filtering by execution status.

**Test Steps**:
1. Call `list_executions` with status filter (success/error/waiting)

**Expected Results**:
- Only executions with specified status returned

**Related AC**: AC4

---

### TC-MGT-029: Pagination for Executions

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify pagination works.

**Test Steps**:
1. List executions with limit and offset

**Expected Results**:
- Correct page of results returned

**Related AC**: AC4

---

### TC-MGT-030: Empty Execution History

**Priority**: Low | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify behavior with no executions.

**Test Steps**:
1. List executions for workflow with no history

**Expected Results**:
- Returns empty array
- No error

**Related AC**: AC4

---

## get_execution_details Tool Test Cases (5 test cases)

### TC-MGT-031: Get Execution Details Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify getting detailed execution information.

**Test Steps**:
1. Call `get_execution_details` with execution ID

**Expected Results**:
- Returns complete execution data
- Includes: workflow data, node results, execution time

**Related AC**: AC4

---

### TC-MGT-032: Get Execution with Error Details

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify error information in failed executions.

**Test Steps**:
1. Get details for failed execution

**Expected Results**:
- Returns error details
- Includes: error message, failed node, stack trace

**Related AC**: AC4, AC8

---

### TC-MGT-033: Get Execution Node Results

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify individual node execution results.

**Test Steps**:
1. Get execution details
2. Verify node results

**Expected Results**:
- Each node has execution data
- Input/output data present

**Related AC**: AC4

---

### TC-MGT-034: Get Non-Existent Execution

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify error for invalid execution ID.

**Test Steps**:
1. Call with invalid execution ID

**Expected Results**:
- Error: execution not found

**Related AC**: AC4, AC8

---

### TC-MGT-035: Get Execution Performance Metrics

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify execution metrics are returned.

**Test Steps**:
1. Get execution details
2. Verify timing metrics

**Expected Results**:
- Total execution time
- Per-node execution time

**Related AC**: AC4

---

## Test Suite Summary

**Total Test Cases**: 35

**By Tool**:
- list_node_types: 7 test cases
- manage_credentials: 10 test cases
- manage_webhooks: 8 test cases
- list_executions: 5 test cases
- get_execution_details: 5 test cases

**By Priority**:
- Critical: 10
- High: 16
- Medium: 8
- Low: 1

**By Phase**:
- Phase 1: 24 test cases (69%)
- Phase 2: 11 test cases (31%)

**Automation**: 95% (33 automated, 2 manual)

---

**Document Type**: Test Case Documentation
**Version**: 1.0
**Created**: 2025-11-06
**Location**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test/test-cases/management-tools/MGT-TOOLS-TEST-CASES.md`
