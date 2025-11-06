# Management Tools Test Cases

**POC-002: N8N MCP Server Deployment**
**Test Suite**: Management Tools (Phase 2)
**Author**: Julia Chen, Testing Framework Specialist
**Date**: 2025-11-06
**Version**: 1.0

---

## Overview

This document defines comprehensive test cases for the 21 N8N Management Tools provided by the N8N MCP Server. These tools require a live N8N instance at `192.168.10.215:5678` and are classified as Phase 2 End-to-End (E2E) tests.

### Test Execution Requirements

- **Phase**: Phase 2 (requires N8N instance)
- **Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`
- **Prerequisites**:
  - N8N instance running at `http://192.168.10.215:5678`
  - Valid N8N API key configured
  - MCP server at `192.168.10.214:3000`
  - Test credentials with workflow management permissions

### Test Client

All management tools tests use `MCPManagementClient` from `test_helpers.py`:

```python
from test_helpers import MCPManagementClient

async def test_example(management_client):
    """Example using management client fixture."""
    result = await management_client.list_workflows()
    assert result['success'] is True
```

---

## Test Categories

### 1. Workflow Management (8 tools)
### 2. Execution Management (5 tools)
### 3. Credential Management (4 tools)
### 4. User Management (2 tools)
### 5. Settings Management (2 tools)

---

## 1. Workflow Management Tests

### 1.1 List Workflows (`n8n_list_workflows`)

#### Test Case: MGT-WF-001 (P1)
**Title**: List all workflows successfully
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Preconditions**:
- N8N instance has at least 1 workflow
- Valid API credentials

**Test Steps**:
1. Call `n8n_list_workflows` with no filters
2. Verify response structure
3. Validate workflow metadata fields

**Expected Results**:
- Returns list of workflows
- Each workflow has: `id`, `name`, `active`, `createdAt`, `updatedAt`
- HTTP 200 status

**Implementation**:
```python
async def test_list_workflows_success(management_client):
    """Verify listing all workflows returns valid data."""
    result = await management_client.list_workflows()

    assert result['success'] is True
    assert isinstance(result['workflows'], list)
    assert len(result['workflows']) > 0

    workflow = result['workflows'][0]
    assert 'id' in workflow
    assert 'name' in workflow
    assert 'active' in workflow
```

---

#### Test Case: MGT-WF-002 (P2)
**Title**: Filter workflows by active status
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Call `n8n_list_workflows` with `active=true`
2. Verify all returned workflows are active
3. Call with `active=false`
4. Verify all returned workflows are inactive

**Expected Results**:
- Active filter returns only active workflows
- Inactive filter returns only inactive workflows

---

#### Test Case: MGT-WF-003 (P3)
**Title**: Handle empty workflow list
**Priority**: P3 (Low)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p3`

**Test Steps**:
1. Call `n8n_list_workflows` on fresh instance
2. Verify graceful handling of empty list

**Expected Results**:
- Returns empty array `[]`
- No errors raised

---

### 1.2 Get Workflow Details (`n8n_get_workflow`)

#### Test Case: MGT-WF-004 (P1)
**Title**: Retrieve workflow by valid ID
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. List workflows to get valid ID
2. Call `n8n_get_workflow(workflow_id)`
3. Verify detailed workflow structure

**Expected Results**:
- Returns complete workflow definition
- Includes: `nodes`, `connections`, `settings`, `staticData`

---

#### Test Case: MGT-WF-005 (P2)
**Title**: Handle invalid workflow ID
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Call `n8n_get_workflow("invalid-id-12345")`
2. Verify error handling

**Expected Results**:
- Returns error response
- HTTP 404 or appropriate error code

---

### 1.3 Create Workflow (`n8n_create_workflow`)

#### Test Case: MGT-WF-006 (P1)
**Title**: Create simple workflow successfully
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Define minimal workflow JSON
2. Call `n8n_create_workflow(workflow_data)`
3. Verify workflow creation
4. Cleanup: Delete created workflow

**Expected Results**:
- Workflow created with unique ID
- Returns workflow object with `id`
- Workflow visible in `n8n_list_workflows`

**Implementation**:
```python
async def test_create_workflow_success(management_client):
    """Verify creating a new workflow."""
    workflow_data = {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "start-node",
                "type": "n8n-nodes-base.start",
                "position": [250, 300],
                "parameters": {}
            }
        ],
        "connections": {},
        "active": False
    }

    result = await management_client.create_workflow(workflow_data)

    assert result['success'] is True
    assert 'id' in result['workflow']
    workflow_id = result['workflow']['id']

    # Cleanup
    await management_client.delete_workflow(workflow_id)
```

---

#### Test Case: MGT-WF-007 (P2)
**Title**: Validate workflow schema enforcement
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Attempt to create workflow with missing required fields
2. Verify schema validation

**Expected Results**:
- Returns validation error
- Indicates missing/invalid fields

---

### 1.4 Update Workflow (`n8n_update_workflow`)

#### Test Case: MGT-WF-008 (P1)
**Title**: Update workflow name and nodes
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Create test workflow
2. Update workflow name and add node
3. Verify changes persisted
4. Cleanup workflow

**Expected Results**:
- Workflow updated successfully
- Changes reflected in `n8n_get_workflow`

---

#### Test Case: MGT-WF-009 (P2)
**Title**: Handle concurrent workflow updates
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Create workflow
2. Perform two simultaneous updates
3. Verify conflict handling

**Expected Results**:
- Proper conflict resolution or error

---

### 1.5 Delete Workflow (`n8n_delete_workflow`)

#### Test Case: MGT-WF-010 (P1)
**Title**: Delete workflow successfully
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Create test workflow
2. Delete workflow by ID
3. Verify workflow no longer exists

**Expected Results**:
- Workflow deleted
- `n8n_get_workflow` returns 404

---

#### Test Case: MGT-WF-011 (P2)
**Title**: Prevent deletion of active workflows
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Create and activate workflow
2. Attempt deletion
3. Verify protection or warning

**Expected Results**:
- Deletion prevented or warning issued

---

### 1.6 Activate Workflow (`n8n_activate_workflow`)

#### Test Case: MGT-WF-012 (P1)
**Title**: Activate inactive workflow
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Create inactive workflow
2. Call `n8n_activate_workflow(workflow_id)`
3. Verify workflow is active
4. Cleanup

**Expected Results**:
- Workflow status changes to `active: true`
- Workflow executes on triggers

---

#### Test Case: MGT-WF-013 (P3)
**Title**: Handle activation of already active workflow
**Priority**: P3 (Low)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p3`

**Test Steps**:
1. Activate workflow twice
2. Verify idempotent behavior

**Expected Results**:
- No error, workflow remains active

---

### 1.7 Deactivate Workflow (`n8n_deactivate_workflow`)

#### Test Case: MGT-WF-014 (P1)
**Title**: Deactivate active workflow
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Create and activate workflow
2. Call `n8n_deactivate_workflow(workflow_id)`
3. Verify workflow is inactive

**Expected Results**:
- Workflow status changes to `active: false`
- Workflow stops executing

---

### 1.8 Export Workflow (`n8n_export_workflow`)

#### Test Case: MGT-WF-015 (P2)
**Title**: Export workflow to JSON
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Create test workflow
2. Call `n8n_export_workflow(workflow_id)`
3. Verify exported JSON structure
4. Cleanup

**Expected Results**:
- Returns valid workflow JSON
- JSON can be re-imported

---

## 2. Execution Management Tests

### 2.1 List Executions (`n8n_list_executions`)

#### Test Case: MGT-EX-001 (P1)
**Title**: List recent workflow executions
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Execute a workflow
2. Call `n8n_list_executions()`
3. Verify execution appears in list

**Expected Results**:
- Returns list of executions
- Each has: `id`, `workflowId`, `status`, `startedAt`

---

#### Test Case: MGT-EX-002 (P2)
**Title**: Filter executions by workflow ID
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Call `n8n_list_executions(workflow_id=specific_id)`
2. Verify all results match workflow ID

**Expected Results**:
- Only executions for specified workflow returned

---

### 2.2 Get Execution Details (`n8n_get_execution`)

#### Test Case: MGT-EX-003 (P1)
**Title**: Retrieve execution details by ID
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Execute workflow
2. Get execution ID
3. Call `n8n_get_execution(execution_id)`

**Expected Results**:
- Returns detailed execution data
- Includes node execution results, timing, errors

---

### 2.3 Execute Workflow (`n8n_execute_workflow`)

#### Test Case: MGT-EX-004 (P1)
**Title**: Manually trigger workflow execution
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Create simple workflow
2. Call `n8n_execute_workflow(workflow_id)`
3. Verify execution completes

**Expected Results**:
- Workflow executes successfully
- Returns execution ID
- Status is `success`

**Implementation**:
```python
async def test_execute_workflow(management_client):
    """Verify manual workflow execution."""
    # Create test workflow
    workflow_data = {
        "name": "Test Execution",
        "nodes": [
            {
                "id": "start",
                "type": "n8n-nodes-base.start",
                "position": [250, 300],
                "parameters": {}
            }
        ],
        "connections": {},
        "active": False
    }

    create_result = await management_client.create_workflow(workflow_data)
    workflow_id = create_result['workflow']['id']

    # Execute workflow
    exec_result = await management_client.execute_workflow(workflow_id)

    assert exec_result['success'] is True
    assert 'execution_id' in exec_result

    # Cleanup
    await management_client.delete_workflow(workflow_id)
```

---

#### Test Case: MGT-EX-005 (P2)
**Title**: Execute workflow with input data
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Execute workflow with JSON input
2. Verify input data passed to workflow

**Expected Results**:
- Workflow receives input data
- Execution processes input correctly

---

### 2.4 Stop Execution (`n8n_stop_execution`)

#### Test Case: MGT-EX-006 (P2)
**Title**: Stop running workflow execution
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Execute long-running workflow
2. Call `n8n_stop_execution(execution_id)`
3. Verify execution stopped

**Expected Results**:
- Execution status changes to `stopped`
- Workflow halts immediately

---

### 2.5 Delete Execution (`n8n_delete_execution`)

#### Test Case: MGT-EX-007 (P2)
**Title**: Delete execution record
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Execute workflow
2. Delete execution record
3. Verify execution no longer listed

**Expected Results**:
- Execution removed from history
- `n8n_get_execution` returns 404

---

## 3. Credential Management Tests

### 3.1 List Credentials (`n8n_list_credentials`)

#### Test Case: MGT-CR-001 (P1)
**Title**: List all credentials
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Call `n8n_list_credentials()`
2. Verify credential list structure

**Expected Results**:
- Returns list of credentials (without sensitive data)
- Each has: `id`, `name`, `type`

---

### 3.2 Get Credential Details (`n8n_get_credential`)

#### Test Case: MGT-CR-002 (P2)
**Title**: Retrieve credential by ID
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. List credentials
2. Get details for specific credential
3. Verify sensitive data handling

**Expected Results**:
- Returns credential metadata
- Sensitive fields masked or encrypted

---

### 3.3 Create Credential (`n8n_create_credential`)

#### Test Case: MGT-CR-003 (P1)
**Title**: Create new credential
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Define credential data
2. Call `n8n_create_credential(cred_data)`
3. Verify credential created
4. Cleanup

**Expected Results**:
- Credential created successfully
- Returns credential ID
- Data encrypted at rest

---

### 3.4 Delete Credential (`n8n_delete_credential`)

#### Test Case: MGT-CR-004 (P2)
**Title**: Delete unused credential
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Create test credential
2. Delete credential
3. Verify removal

**Expected Results**:
- Credential deleted
- No longer in credential list

---

#### Test Case: MGT-CR-005 (P1)
**Title**: Prevent deletion of in-use credentials
**Priority**: P1 (Critical)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p1`

**Test Steps**:
1. Create credential
2. Use in workflow
3. Attempt deletion

**Expected Results**:
- Deletion prevented
- Error indicates credential in use

---

## 4. User Management Tests

### 4.1 List Users (`n8n_list_users`)

#### Test Case: MGT-USR-001 (P2)
**Title**: List all N8N users
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Call `n8n_list_users()`
2. Verify user list structure

**Expected Results**:
- Returns list of users
- Each has: `id`, `email`, `firstName`, `lastName`

---

### 4.2 Get User Details (`n8n_get_user`)

#### Test Case: MGT-USR-002 (P2)
**Title**: Retrieve user by ID
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. List users
2. Get details for specific user

**Expected Results**:
- Returns user profile
- Includes role and permissions

---

## 5. Settings Management Tests

### 5.1 Get Settings (`n8n_get_settings`)

#### Test Case: MGT-SET-001 (P2)
**Title**: Retrieve N8N instance settings
**Priority**: P2 (High)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p2`

**Test Steps**:
1. Call `n8n_get_settings()`
2. Verify settings structure

**Expected Results**:
- Returns configuration settings
- Includes version, features, limits

---

### 5.2 Update Settings (`n8n_update_settings`)

#### Test Case: MGT-SET-002 (P3)
**Title**: Update instance settings
**Priority**: P3 (Low)
**Markers**: `@pytest.mark.phase2`, `@pytest.mark.e2e`, `@pytest.mark.p3`

**Test Steps**:
1. Get current settings
2. Update specific setting
3. Verify change persisted

**Expected Results**:
- Settings updated successfully
- Changes reflected immediately

---

## Test Execution Summary

### Total Test Cases: 35+

**By Priority**:
- P1 (Critical): 15 tests
- P2 (High): 17 tests
- P3 (Low): 3 tests

**By Category**:
- Workflow Management: 15 tests
- Execution Management: 7 tests
- Credential Management: 5 tests
- User Management: 2 tests
- Settings Management: 2 tests

**Markers**:
- All tests: `@pytest.mark.phase2`, `@pytest.mark.e2e`
- Priority markers: `@pytest.mark.p1`, `@pytest.mark.p2`, `@pytest.mark.p3`

**Prerequisites**:
- N8N instance at `http://192.168.10.215:5678`
- MCP server at `http://192.168.10.214:3000`
- Valid API credentials
- Test user with admin permissions

---

## Appendix: Tool Reference

### Complete Management Tools List

1. `n8n_list_workflows` - List all workflows
2. `n8n_get_workflow` - Get workflow details
3. `n8n_create_workflow` - Create new workflow
4. `n8n_update_workflow` - Update workflow
5. `n8n_delete_workflow` - Delete workflow
6. `n8n_activate_workflow` - Activate workflow
7. `n8n_deactivate_workflow` - Deactivate workflow
8. `n8n_export_workflow` - Export workflow JSON
9. `n8n_list_executions` - List workflow executions
10. `n8n_get_execution` - Get execution details
11. `n8n_execute_workflow` - Manually execute workflow
12. `n8n_stop_execution` - Stop running execution
13. `n8n_delete_execution` - Delete execution record
14. `n8n_list_credentials` - List credentials
15. `n8n_get_credential` - Get credential details
16. `n8n_create_credential` - Create credential
17. `n8n_delete_credential` - Delete credential
18. `n8n_list_users` - List users
19. `n8n_get_user` - Get user details
20. `n8n_get_settings` - Get instance settings
21. `n8n_update_settings` - Update settings

---

**Document Type**: Test Case Specification
**Version**: 1.0
**Date**: 2025-11-06
**Location**: `/srv/cc/Governance/0.5-projects/POC-002-n8n-mcp-server-deployment/tests/MGT-TOOLS-TEST-CASES.md`
