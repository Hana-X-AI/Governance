# Integration Test Cases

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | POC-002-TC-INT-001 |
| **Version** | 1.0 |
| **Created** | 2025-11-06 |
| **Test Suite** | Integration Tests |
| **Total Test Cases** | 40 |
| **Automation** | 90% |
| **Priority** | High |
| **Phase** | Phase 2 |

---

## Test Suite Overview

**Objective**: Validate integration scenarios, cross-tool workflows, end-to-end user journeys, and error recovery.

**Scope**:
- Tool integration scenarios
- Cross-tool workflows
- N8N to MCP communication
- End-to-end user journeys
- Error recovery and rollback

**Related Acceptance Criteria**: AC9

---

## Tool Integration Test Cases (15 test cases)

### TC-INT-001: Create Workflow with Project Assignment

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify creating workflow and assigning to project.

**Test Steps**:
1. Create project via `manage_projects`
2. Create workflow in N8N
3. Assign workflow to project
4. Verify via `list_workflows` with project filter

**Expected Results**:
- Workflow created and assigned
- Project association visible

**Related AC**: AC3, AC9

---

### TC-INT-002: Workflow Lifecycle with Tags

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Complete workflow lifecycle with tag management.

**Test Steps**:
1. Create workflow
2. Add tags via `manage_workflow_tags`
3. Update workflow
4. List workflows by tag
5. Remove tags
6. Delete workflow

**Expected Results**:
- All operations succeed
- Tags filter correctly
- Clean deletion

**Related AC**: AC2, AC3, AC9

---

### TC-INT-003: Credential Creation and Usage in Workflow

**Priority**: Critical | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Create credential and use in workflow.

**Test Steps**:
1. Create credential via `manage_credentials`
2. Create workflow using credential
3. Execute workflow
4. Verify credential used correctly

**Expected Results**:
- Credential created
- Workflow uses credential
- Execution succeeds

**Related AC**: AC6, AC9

---

### TC-INT-004: Webhook Trigger to Workflow Execution

**Priority**: Critical | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Create webhook and trigger workflow execution.

**Test Steps**:
1. Create workflow with webhook trigger
2. Create webhook via `manage_webhooks`
3. Trigger webhook via HTTP request
4. Check execution status via `check_execution_status`

**Expected Results**:
- Webhook created
- Workflow triggered
- Execution completes
- Status retrievable

**Related AC**: AC4, AC5, AC9

---

### TC-INT-005: Multi-Project Workflow Organization

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Organize workflows across multiple projects.

**Test Steps**:
1. Create 3 projects
2. Create workflows in each project
3. List workflows by project
4. Verify organization

**Expected Results**:
- Workflows correctly organized
- Filtering works correctly

**Related AC**: AC3, AC9

---

### TC-INT-006: Node Type Discovery to Workflow Creation

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Discover nodes and use in workflow creation.

**Test Steps**:
1. List node types via `list_node_types`
2. Identify required nodes
3. Create workflow using those nodes
4. Verify workflow structure

**Expected Results**:
- Nodes discovered
- Workflow created with correct nodes

**Related AC**: AC7, AC9

---

### TC-INT-007: Execution History and Details Retrieval

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Execute workflow and retrieve complete history.

**Test Steps**:
1. Execute workflow multiple times
2. List executions via `list_executions`
3. Get details for each via `get_execution_details`
4. Verify data consistency

**Expected Results**:
- All executions listed
- Details match execution data

**Related AC**: AC4, AC9

---

### TC-INT-008: Workflow Clone with Dependencies

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Clone workflow with credentials and webhooks.

**Test Steps**:
1. Create workflow with credential and webhook
2. Clone workflow
3. Verify dependencies handled correctly

**Expected Results**:
- Clone created
- Credentials referenced (not duplicated)
- Webhooks duplicated or warned

**Related AC**: AC9

---

### TC-INT-009: Project Deletion with Workflows

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Delete project containing workflows.

**Test Steps**:
1. Create project with workflows
2. Delete project
3. Verify workflow handling

**Expected Results**:
- Either: Workflows also deleted (cascade)
- Or: Workflows unassigned from project
- Or: Error: project contains workflows

**Related AC**: AC3, AC9

---

### TC-INT-010: Credential Update Propagation

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Update credential and verify workflows use new version.

**Test Steps**:
1. Create credential
2. Create workflow using credential
3. Update credential
4. Execute workflow
5. Verify new credential used

**Expected Results**:
- Workflow uses updated credential
- No stale credential issues

**Related AC**: AC6, AC9

---

### TC-INT-011: Tag-Based Workflow Discovery

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Use tags to organize and discover workflows.

**Test Steps**:
1. Create workflows with various tags
2. Search by single tag
3. Search by multiple tags
4. Verify filtering

**Expected Results**:
- Tag filtering accurate
- Multi-tag filtering works (AND/OR logic)

**Related AC**: AC2, AC3, AC9

---

### TC-INT-012: Webhook Deletion with Active Workflow

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Delete webhook used by active workflow.

**Test Steps**:
1. Create workflow with webhook
2. Activate workflow
3. Delete webhook
4. Verify workflow handling

**Expected Results**:
- Either: Error (webhook in use)
- Or: Warning and workflow deactivation

**Related AC**: AC5, AC9

---

### TC-INT-013: Execution Monitoring During Long Workflow

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Monitor execution progress of long-running workflow.

**Test Steps**:
1. Start long-running workflow (30+ seconds)
2. Poll execution status every 2 seconds
3. Track status transitions

**Expected Results**:
- Status updates correctly (waiting → running → success)
- Progress visible

**Related AC**: AC4, AC9

---

### TC-INT-014: Failed Workflow Execution Analysis

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Analyze failed workflow execution.

**Test Steps**:
1. Create workflow that will fail
2. Execute workflow
3. Check execution status (should be error)
4. Get execution details
5. Verify error information

**Expected Results**:
- Status shows error
- Error details include: message, node, stack trace

**Related AC**: AC4, AC8, AC9

---

### TC-INT-015: Workflow Import/Export with Dependencies

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Export workflow and verify dependency handling.

**Test Steps**:
1. Create workflow with credentials, webhooks, tags
2. Export workflow (via get_workflow_details)
3. Verify export includes dependency references
4. Import to new workflow
5. Verify dependencies restored

**Expected Results**:
- Export complete
- Dependencies preserved or flagged

**Related AC**: AC9

---

## Cross-Tool Workflow Test Cases (10 test cases)

### TC-INT-016: Complete Workflow Setup Journey

**Priority**: Critical | **Type**: End-to-End | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Complete end-to-end workflow setup.

**Test Steps**:
1. Create project
2. Create credentials
3. Discover available nodes
4. Create workflow in project
5. Add tags to workflow
6. Create webhook for workflow
7. Activate workflow
8. Test webhook trigger
9. Monitor execution
10. Retrieve execution details

**Expected Results**:
- All steps succeed
- Workflow fully functional

**Related AC**: AC2, AC3, AC4, AC5, AC6, AC7, AC9

---

### TC-INT-017: Multi-Workflow Orchestration

**Priority**: High | **Type**: End-to-End | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Create orchestration with multiple workflows.

**Test Steps**:
1. Create workflow A (webhook trigger)
2. Create workflow B (called by A)
3. Create workflow C (called by B)
4. Trigger A via webhook
5. Monitor all executions

**Expected Results**:
- All workflows execute in sequence
- Execution chain traceable

**Related AC**: AC9

---

### TC-INT-018: Batch Workflow Operations

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Perform batch operations on multiple workflows.

**Test Steps**:
1. Create 10 workflows
2. Bulk add tags
3. Bulk activate/deactivate
4. Bulk move to project
5. Verify all operations

**Expected Results**:
- Batch operations efficient
- All workflows updated correctly

**Related AC**: AC9

---

### TC-INT-019: Workflow Migration Between Projects

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Move workflows between projects.

**Test Steps**:
1. Create 2 projects
2. Create workflow in project A
3. Move workflow to project B
4. Verify workflow accessible in project B

**Expected Results**:
- Workflow moved successfully
- Dependencies maintained

**Related AC**: AC3, AC9

---

### TC-INT-020: Credential Sharing Across Workflows

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Share single credential across multiple workflows.

**Test Steps**:
1. Create credential
2. Create 3 workflows using same credential
3. Execute all workflows
4. Update credential
5. Re-execute all workflows

**Expected Results**:
- Credential shared correctly
- All workflows use updated credential

**Related AC**: AC6, AC9

---

### TC-INT-021: Webhook Load Distribution

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Trigger multiple workflows via webhooks simultaneously.

**Test Steps**:
1. Create 5 workflows with webhooks
2. Trigger all webhooks simultaneously
3. Monitor all executions

**Expected Results**:
- All webhooks trigger successfully
- All executions complete
- No request dropping

**Related AC**: AC5, AC9

---

### TC-INT-022: Complex Workflow with All Tools

**Priority**: High | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Create complex workflow using all MCP tools.

**Test Steps**:
1. Discover nodes (list_node_types)
2. Create credentials (manage_credentials)
3. Create project (manage_projects)
4. Create workflow with multiple nodes
5. Add tags (manage_workflow_tags)
6. Create webhook (manage_webhooks)
7. Get workflow details (get_workflow_details)
8. Trigger execution
9. Check status (check_execution_status)
10. List executions (list_executions)
11. Get execution details (get_execution_details)

**Expected Results**:
- All tools work together seamlessly
- Complex workflow functions correctly

**Related AC**: AC2, AC3, AC4, AC5, AC6, AC7, AC9

---

### TC-INT-023: Workflow Versioning Scenario

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Manage workflow versions.

**Test Steps**:
1. Create workflow v1
2. Execute and record execution
3. Update workflow to v2
4. Execute and record execution
5. Compare execution history

**Expected Results**:
- Version changes tracked
- Execution history shows versions

**Related AC**: AC9

---

### TC-INT-024: Cascading Workflow Updates

**Priority**: Medium | **Type**: Integration | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Update workflow and verify cascading effects.

**Test Steps**:
1. Create workflow with dependencies
2. Update dependency (credential, webhook)
3. Verify workflow still functional
4. Update workflow nodes
5. Re-execute

**Expected Results**:
- Updates propagate correctly
- Workflow remains functional

**Related AC**: AC9

---

### TC-INT-025: Workflow Debugging Journey

**Priority**: High | **Type**: End-to-End | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Debug failing workflow using MCP tools.

**Test Steps**:
1. Create workflow that fails
2. Execute workflow
3. Check status (should show error)
4. Get execution details
5. Identify failed node
6. Get workflow details
7. Fix workflow
8. Re-execute
9. Verify success

**Expected Results**:
- Error information sufficient for debugging
- Fix successful

**Related AC**: AC8, AC9

---

## Error Recovery Test Cases (10 test cases)

### TC-INT-026: Network Interruption Recovery

**Priority**: High | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: No (Manual)

**Objective**: Verify recovery from network interruption.

**Test Steps**:
1. Start workflow execution
2. Simulate network interruption
3. Restore network
4. Check execution status

**Expected Results**:
- Execution either completes or shows error
- No data corruption

**Related AC**: AC8, AC9

---

### TC-INT-027: Partial Workflow Execution Recovery

**Priority**: High | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify handling of partially completed workflows.

**Test Steps**:
1. Execute workflow that fails mid-execution
2. Check execution details
3. Identify completed vs failed nodes
4. Retry execution

**Expected Results**:
- Partial completion tracked
- Retry possible

**Related AC**: AC8, AC9

---

### TC-INT-028: Credential Rotation During Execution

**Priority**: Medium | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Handle credential updates during workflow execution.

**Test Steps**:
1. Start long-running workflow
2. Update credential used by workflow
3. Observe behavior

**Expected Results**:
- Either: Execution uses original credential
- Or: Execution fails gracefully with clear message

**Related AC**: AC6, AC8, AC9

---

### TC-INT-029: Concurrent Modification Conflict

**Priority**: Medium | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Handle concurrent workflow modifications.

**Test Steps**:
1. Get workflow details (session A)
2. Get workflow details (session B)
3. Update workflow (session A)
4. Update workflow (session B)
5. Verify conflict handling

**Expected Results**:
- Either: Last write wins
- Or: Optimistic locking error

**Related AC**: AC8, AC9

---

### TC-INT-030: Webhook Timeout Recovery

**Priority**: Medium | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Handle webhook trigger timeouts.

**Test Steps**:
1. Create workflow with slow execution
2. Trigger via webhook
3. Webhook request times out
4. Verify workflow continues executing

**Expected Results**:
- Webhook returns timeout response
- Workflow execution continues in background

**Related AC**: AC5, AC8, AC9

---

### TC-INT-031: MCP Server Restart During Operation

**Priority**: High | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: No (Manual)

**Objective**: Verify behavior when MCP server restarts.

**Test Steps**:
1. Start operation via MCP
2. Restart MCP server
3. Retry operation

**Expected Results**:
- Client receives error
- Retry succeeds
- N8N state unchanged

**Related AC**: AC8, AC9

---

### TC-INT-032: N8N Server Restart Recovery

**Priority**: High | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: No (Manual)

**Objective**: Verify MCP server handles N8N restart.

**Test Steps**:
1. Restart N8N server
2. Attempt MCP operations
3. Verify reconnection

**Expected Results**:
- MCP server reconnects
- Operations resume

**Related AC**: AC8, AC9

---

### TC-INT-033: Data Inconsistency Detection

**Priority**: High | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Detect data inconsistencies between MCP and N8N.

**Test Steps**:
1. Create workflow via N8N UI
2. Verify visible via MCP
3. Update via MCP
4. Verify in N8N UI
5. Compare all fields

**Expected Results**:
- Data consistent across interfaces
- No data loss

**Related AC**: AC9

---

### TC-INT-034: Rollback After Failed Update

**Priority**: Medium | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify rollback on failed updates.

**Test Steps**:
1. Get workflow state
2. Attempt invalid update
3. Verify workflow unchanged

**Expected Results**:
- Update fails with error
- Original state preserved

**Related AC**: AC8, AC9

---

### TC-INT-035: Idempotent Operation Verification

**Priority**: High | **Type**: Reliability | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Verify operations are idempotent.

**Test Steps**:
1. Perform operation (e.g., create, update)
2. Repeat exact same operation
3. Verify result identical

**Expected Results**:
- Duplicate operations handled gracefully
- No duplicate resources created

**Related AC**: AC9

---

## End-to-End User Journey Test Cases (5 test cases)

### TC-INT-036: Developer Onboarding Journey

**Priority**: Critical | **Type**: End-to-End | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Simulate new developer setting up N8N workflows.

**Test Steps**:
1. List available node types
2. Create project for workflows
3. Create credentials
4. Create first workflow
5. Add tags for organization
6. Create webhook for testing
7. Test workflow execution
8. Monitor results

**Expected Results**:
- Complete onboarding possible via MCP
- All tools intuitive

**Related AC**: AC1-AC9

---

### TC-INT-037: Production Deployment Journey

**Priority**: Critical | **Type**: End-to-End | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Deploy workflow from dev to production.

**Test Steps**:
1. Export workflow from dev (get_workflow_details)
2. Create production credentials
3. Import workflow to production
4. Update credential references
5. Create production webhooks
6. Activate workflow
7. Test in production
8. Monitor executions

**Expected Results**:
- Deployment smooth
- All dependencies transferred

**Related AC**: AC9

---

### TC-INT-038: Troubleshooting Journey

**Priority**: High | **Type**: End-to-End | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Troubleshoot failing production workflow.

**Test Steps**:
1. List executions, filter by error status
2. Get execution details for failed execution
3. Identify error node
4. Get workflow details
5. Analyze node configuration
6. Update workflow
7. Re-test
8. Verify fix

**Expected Results**:
- Troubleshooting tools sufficient
- Problem identified and resolved

**Related AC**: AC8, AC9

---

### TC-INT-039: Workflow Optimization Journey

**Priority**: Medium | **Type**: End-to-End | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Optimize workflow performance.

**Test Steps**:
1. List executions
2. Get execution details for slow executions
3. Identify bottleneck nodes
4. Get workflow details
5. Optimize node configuration
6. Re-execute
7. Compare execution times

**Expected Results**:
- Performance analysis possible
- Optimization effective

**Related AC**: AC9

---

### TC-INT-040: Workflow Decommissioning Journey

**Priority**: Medium | **Type**: End-to-End | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Safely decommission workflow.

**Test Steps**:
1. Deactivate workflow
2. Delete webhooks
3. Remove from project
4. Archive execution history
5. Delete workflow
6. Verify clean deletion

**Expected Results**:
- Safe decommissioning process
- No orphaned resources

**Related AC**: AC9

---

## Test Suite Summary

**Total Test Cases**: 40

**By Category**:
- Tool Integration: 15 test cases
- Cross-Tool Workflows: 10 test cases
- Error Recovery: 10 test cases
- End-to-End Journeys: 5 test cases

**By Priority**:
- Critical: 8
- High: 20
- Medium: 12

**By Phase**:
- Phase 2: 40 test cases (100%)

**Automation**: 90% (36 automated, 4 manual)

---

**Document Type**: Test Case Documentation
**Version**: 1.0
**Created**: 2025-11-06
**Location**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test/test-cases/integration/INTEGRATION-TEST-CASES.md`
