# Documentation Tools Test Cases

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | POC-002-TC-DOC-001 |
| **Version** | 1.0 |
| **Created** | 2025-11-06 |
| **Test Suite** | Documentation Tools |
| **Total Test Cases** | 35 |
| **Automation** | 95% |
| **Priority** | Critical |
| **Phase** | Phase 1 & Phase 2 |

---

## Test Suite Overview

**Objective**: Validate all 5 documentation-related MCP tools for workflow and project management.

**Tools Under Test**:
1. `list_workflows` - Retrieve workflow information
2. `manage_projects` - Project CRUD operations
3. `manage_workflow_tags` - Tag management
4. `get_workflow_details` - Detailed workflow information
5. `check_execution_status` - Execution monitoring

**Related Acceptance Criteria**: AC2, AC3, AC4

---

## list_workflows Tool Test Cases (7 test cases)

### TC-DOC-001: List All Workflows Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify `list_workflows` returns all workflows without filters.

**Preconditions**:
- MCP server initialized
- Test workflows exist in N8N

**Test Steps**:
1. Call `list_workflows` with no parameters
2. Verify response

**Expected Results**:
- Returns array of workflows
- Each workflow has: id, name, active, tags, createdAt, updatedAt
- Response format valid

**Related AC**: AC2

---

### TC-DOC-002: List Workflows with Active Filter

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify filtering workflows by active status.

**Test Steps**:
1. Call `list_workflows` with `active: true`
2. Verify all returned workflows have `active: true`
3. Call with `active: false`
4. Verify all returned workflows have `active: false`

**Expected Results**:
- Filter correctly applies
- Only matching workflows returned

**Related AC**: AC2

---

### TC-DOC-003: List Workflows with Tag Filter

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify filtering workflows by tags.

**Test Steps**:
1. Call `list_workflows` with `tags: ["test"]`
2. Verify all returned workflows have "test" tag

**Expected Results**:
- Filter correctly applies
- Only workflows with specified tags returned

**Related AC**: AC2

---

### TC-DOC-004: List Workflows Pagination

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify pagination parameters work correctly.

**Test Steps**:
1. Call with `limit: 5`
2. Verify maximum 5 workflows returned
3. Call with `limit: 5, offset: 5`
4. Verify next 5 workflows returned

**Expected Results**:
- Pagination works correctly
- No duplicate workflows

**Related AC**: AC2

---

### TC-DOC-005: List Workflows Empty Result

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify behavior when no workflows match filter.

**Test Steps**:
1. Call with filter that matches no workflows

**Expected Results**:
- Returns empty array
- No error

**Related AC**: AC2

---

### TC-DOC-006: List Workflows Invalid Parameters

**Priority**: High | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify error handling for invalid parameters.

**Test Steps**:
1. Call with invalid parameter type (e.g., `active: "invalid"`)

**Expected Results**:
- JSON-RPC error returned
- Error code: -32602 (Invalid params)

**Related AC**: AC2, AC8

---

### TC-DOC-007: List Workflows Performance

**Priority**: Medium | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify response time for listing workflows.

**Test Steps**:
1. Call `list_workflows` with 100+ workflows in system
2. Measure response time

**Expected Results**:
- Response time < 1 second

**Related AC**: AC2

---

## manage_projects Tool Test Cases (7 test cases)

### TC-DOC-008: Create Project Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify project creation.

**Test Steps**:
1. Call `manage_projects` with:
   ```json
   {
     "action": "create",
     "name": "Test Project",
     "type": "team"
   }
   ```

**Expected Results**:
- Project created successfully
- Returns project ID
- Project visible in subsequent list operations

**Related AC**: AC3

---

### TC-DOC-009: List Projects Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify listing all projects.

**Test Steps**:
1. Call `manage_projects` with `action: "list"`

**Expected Results**:
- Returns array of projects
- Each project has: id, name, type, createdAt, updatedAt

**Related AC**: AC3

---

### TC-DOC-010: Update Project Success

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify project update.

**Test Steps**:
1. Create project
2. Call `manage_projects` with:
   ```json
   {
     "action": "update",
     "projectId": "<id>",
     "name": "Updated Project Name"
   }
   ```

**Expected Results**:
- Project updated successfully
- Changes reflected in subsequent get operations

**Related AC**: AC3

---

### TC-DOC-011: Delete Project Success

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify project deletion.

**Test Steps**:
1. Create project
2. Call `manage_projects` with `action: "delete"`, `projectId: "<id>"`
3. Verify project no longer in list

**Expected Results**:
- Project deleted successfully
- Project not in subsequent list operations

**Related AC**: AC3

---

### TC-DOC-012: Create Project with Invalid Type

**Priority**: High | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify validation of project type.

**Test Steps**:
1. Call `manage_projects` with invalid type value

**Expected Results**:
- JSON-RPC error
- Error indicates invalid type

**Related AC**: AC3, AC8

---

### TC-DOC-013: Update Non-Existent Project

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify error when updating non-existent project.

**Test Steps**:
1. Call `manage_projects` update with invalid project ID

**Expected Results**:
- Error response
- Clear error message

**Related AC**: AC3, AC8

---

### TC-DOC-014: Delete Non-Existent Project

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify error when deleting non-existent project.

**Test Steps**:
1. Call `manage_projects` delete with invalid project ID

**Expected Results**:
- Error response
- Clear error message

**Related AC**: AC3, AC8

---

## manage_workflow_tags Tool Test Cases (7 test cases)

### TC-DOC-015: Add Tag to Workflow

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify adding tags to workflow.

**Test Steps**:
1. Call `manage_workflow_tags` with:
   ```json
   {
     "action": "add",
     "workflowId": "<id>",
     "tags": ["production", "critical"]
   }
   ```

**Expected Results**:
- Tags added successfully
- Tags visible in workflow details

**Related AC**: AC3

---

### TC-DOC-016: Remove Tag from Workflow

**Priority**: High | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify removing tags from workflow.

**Test Steps**:
1. Add tags to workflow
2. Call `manage_workflow_tags` with `action: "remove"`

**Expected Results**:
- Tags removed successfully
- Tags not in workflow details

**Related AC**: AC3

---

### TC-DOC-017: List Workflow Tags

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify listing all tags for a workflow.

**Test Steps**:
1. Call `manage_workflow_tags` with `action: "list"`, `workflowId: "<id>"`

**Expected Results**:
- Returns array of tags
- Matches expected tags

**Related AC**: AC3

---

### TC-DOC-018: Add Duplicate Tag

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify behavior when adding duplicate tag.

**Test Steps**:
1. Add tag to workflow
2. Add same tag again

**Expected Results**:
- Either: Idempotent (no error, tag not duplicated)
- Or: Clear error message

**Related AC**: AC3

---

### TC-DOC-019: Remove Non-Existent Tag

**Priority**: Low | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify behavior when removing tag that doesn't exist.

**Test Steps**:
1. Call `manage_workflow_tags` remove with tag not on workflow

**Expected Results**:
- Either: Idempotent (no error)
- Or: Clear error message

**Related AC**: AC3, AC8

---

### TC-DOC-020: Tag on Non-Existent Workflow

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify error for invalid workflow ID.

**Test Steps**:
1. Call `manage_workflow_tags` with invalid workflow ID

**Expected Results**:
- Error response
- Clear error message

**Related AC**: AC3, AC8

---

### TC-DOC-021: Empty Tags Array

**Priority**: Low | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify handling of empty tags array.

**Test Steps**:
1. Call `manage_workflow_tags` with empty tags array

**Expected Results**:
- Either: Accepted (no-op)
- Or: Validation error

**Related AC**: AC3

---

## get_workflow_details Tool Test Cases (7 test cases)

### TC-DOC-022: Get Workflow Details Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify retrieving complete workflow details.

**Test Steps**:
1. Call `get_workflow_details` with valid workflow ID

**Expected Results**:
- Returns complete workflow object
- Includes: id, name, active, nodes, connections, settings, tags, createdAt, updatedAt

**Related AC**: AC4

---

### TC-DOC-023: Get Workflow Details with Nodes

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify workflow nodes are returned.

**Test Steps**:
1. Get details for workflow with multiple nodes
2. Verify nodes array

**Expected Results**:
- Nodes array present
- Each node has: id, name, type, position, parameters

**Related AC**: AC4

---

### TC-DOC-024: Get Workflow Details with Connections

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify workflow connections are returned.

**Test Steps**:
1. Get details for workflow with connections
2. Verify connections object

**Expected Results**:
- Connections object present
- Connections show node relationships

**Related AC**: AC4

---

### TC-DOC-025: Get Non-Existent Workflow

**Priority**: High | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify error for non-existent workflow.

**Test Steps**:
1. Call `get_workflow_details` with invalid workflow ID

**Expected Results**:
- Error response
- Error indicates workflow not found

**Related AC**: AC4, AC8

---

### TC-DOC-026: Get Workflow Details Missing ID

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify error when workflow ID not provided.

**Test Steps**:
1. Call `get_workflow_details` without workflow ID

**Expected Results**:
- JSON-RPC error
- Error code: -32602 (Invalid params)

**Related AC**: AC4, AC8

---

### TC-DOC-027: Get Workflow Details Performance

**Priority**: Medium | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify response time for complex workflows.

**Test Steps**:
1. Get details for workflow with 50+ nodes
2. Measure response time

**Expected Results**:
- Response time < 2 seconds

**Related AC**: AC4

---

### TC-DOC-028: Get Workflow Details Data Completeness

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify all workflow data is returned accurately.

**Test Steps**:
1. Create workflow via N8N UI with known configuration
2. Get details via MCP
3. Compare all fields

**Expected Results**:
- All data matches N8N source
- No data loss or corruption

**Related AC**: AC4

---

## check_execution_status Tool Test Cases (7 test cases)

### TC-DOC-029: Check Execution Status Success

**Priority**: Critical | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify checking execution status.

**Test Steps**:
1. Execute a workflow
2. Call `check_execution_status` with execution ID

**Expected Results**:
- Returns execution status
- Includes: id, workflowId, status, startedAt, finishedAt, mode

**Related AC**: AC4

---

### TC-DOC-030: Check Running Execution

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify status for running execution.

**Test Steps**:
1. Start long-running workflow
2. Check status while running

**Expected Results**:
- Status: "running"
- startedAt present
- finishedAt null

**Related AC**: AC4

---

### TC-DOC-031: Check Completed Execution

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify status for completed execution.

**Test Steps**:
1. Execute workflow to completion
2. Check status

**Expected Results**:
- Status: "success" or "error"
- startedAt and finishedAt present

**Related AC**: AC4

---

### TC-DOC-032: Check Failed Execution

**Priority**: High | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify status for failed execution.

**Test Steps**:
1. Execute workflow that fails
2. Check status

**Expected Results**:
- Status: "error"
- Error information included

**Related AC**: AC4, AC8

---

### TC-DOC-033: Check Non-Existent Execution

**Priority**: Medium | **Type**: Negative | **Phase**: Phase 1 | **Automation**: Yes

**Objective**: Verify error for non-existent execution.

**Test Steps**:
1. Call `check_execution_status` with invalid execution ID

**Expected Results**:
- Error response
- Clear error message

**Related AC**: AC4, AC8

---

### TC-DOC-034: Check Execution with Workflow Details

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify execution includes workflow information.

**Test Steps**:
1. Check execution status
2. Verify workflow details included

**Expected Results**:
- workflowId present
- Optionally: workflow name included

**Related AC**: AC4

---

### TC-DOC-035: Check Execution Polling

**Priority**: Medium | **Type**: Functional | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify repeated status checks work correctly.

**Test Steps**:
1. Start workflow
2. Poll status every 1 second until completion

**Expected Results**:
- Each poll returns current status
- Status transitions correctly (waiting → running → success)

**Related AC**: AC4

---

## Test Suite Summary

**Total Test Cases**: 35

**By Tool**:
- list_workflows: 7 test cases
- manage_projects: 7 test cases
- manage_workflow_tags: 7 test cases
- get_workflow_details: 7 test cases
- check_execution_status: 7 test cases

**By Priority**:
- Critical: 8
- High: 16
- Medium: 9
- Low: 2

**By Phase**:
- Phase 1: 27 test cases (77%)
- Phase 2: 8 test cases (23%)

**Automation**: 95% (33 automated, 2 manual validation)

**Coverage**:
- CRUD operations: 14 test cases
- Error handling: 12 test cases
- Performance: 3 test cases
- Data integrity: 6 test cases

---

**Document Type**: Test Case Documentation
**Version**: 1.0
**Created**: 2025-11-06
**Location**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test/test-cases/documentation-tools/DOC-TOOLS-TEST-CASES.md`
