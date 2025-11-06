# Performance Test Cases

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | POC-002-TC-PERF-001 |
| **Version** | 1.0 |
| **Created** | 2025-11-06 |
| **Test Suite** | Performance Tests |
| **Total Test Cases** | 20 |
| **Automation** | 100% |
| **Priority** | High |
| **Phase** | Phase 2 |

---

## Test Suite Overview

**Objective**: Validate response times, throughput, concurrent operations, and resource utilization.

**Scope**:
- Response time benchmarks
- Concurrent operation handling
- Load testing
- Resource utilization

**Performance Goals**:
- Response time: < 500ms for most operations
- Concurrent users: 10+ simultaneous
- Throughput: 100+ requests/minute
- CPU utilization: < 70%
- Memory: < 2GB

**Related Acceptance Criteria**: AC9

---

## Response Time Benchmark Test Cases (8 test cases)

### TC-PERF-001: list_workflows Response Time

**Priority**: High | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Benchmark list_workflows response time.

**Test Steps**:
1. Execute list_workflows 100 times
2. Measure response time for each
3. Calculate: average, median, 95th percentile, 99th percentile

**Expected Results**:
- Average: < 300ms
- 95th percentile: < 500ms
- 99th percentile: < 1000ms

**Related AC**: AC2

---

### TC-PERF-002: get_workflow_details Response Time

**Priority**: High | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Benchmark get_workflow_details response time.

**Test Steps**:
1. Test with workflows of varying complexity:
   - Simple: 5 nodes
   - Medium: 20 nodes
   - Complex: 50+ nodes
2. Measure response time for each

**Expected Results**:
- Simple: < 200ms
- Medium: < 500ms
- Complex: < 1000ms

**Related AC**: AC4

---

### TC-PERF-003: manage_projects Response Time

**Priority**: Medium | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Benchmark project management operations.

**Test Steps**:
1. Measure create project time
2. Measure list projects time
3. Measure update project time
4. Measure delete project time

**Expected Results**:
- Create: < 300ms
- List: < 200ms
- Update: < 300ms
- Delete: < 200ms

**Related AC**: AC3

---

### TC-PERF-004: manage_credentials Response Time

**Priority**: High | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Benchmark credential operations.

**Test Steps**:
1. Measure create credential time
2. Measure list credentials time
3. Measure update credential time
4. Measure delete credential time

**Expected Results**:
- Create: < 400ms
- List: < 300ms
- Update: < 400ms
- Delete: < 200ms

**Related AC**: AC6

---

### TC-PERF-005: manage_webhooks Response Time

**Priority**: Medium | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Benchmark webhook operations.

**Test Steps**:
1. Measure create webhook time
2. Measure list webhooks time
3. Measure update webhook time
4. Measure delete webhook time

**Expected Results**:
- Create: < 300ms
- List: < 200ms
- Update: < 300ms
- Delete: < 200ms

**Related AC**: AC5

---

### TC-PERF-006: list_node_types Response Time

**Priority**: Medium | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Benchmark node type discovery.

**Test Steps**:
1. Measure list all node types time
2. Measure filtered node types time
3. Measure search node types time

**Expected Results**:
- List all: < 500ms
- Filtered: < 300ms
- Search: < 200ms

**Related AC**: AC7

---

### TC-PERF-007: check_execution_status Response Time

**Priority**: High | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Benchmark execution status checks.

**Test Steps**:
1. Execute workflow
2. Poll status 50 times during execution
3. Measure each poll time

**Expected Results**:
- Average poll time: < 100ms
- 95th percentile: < 200ms

**Related AC**: AC4

---

### TC-PERF-008: MCP Protocol Initialization Time

**Priority**: Medium | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Benchmark MCP initialization.

**Test Steps**:
1. Initialize MCP connection 50 times
2. Measure initialization time

**Expected Results**:
- Average: < 200ms
- 95th percentile: < 300ms

**Related AC**: AC1

---

## Concurrent Operation Test Cases (5 test cases)

### TC-PERF-009: Concurrent list_workflows

**Priority**: High | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Test concurrent workflow listing.

**Test Steps**:
1. Spawn 10 concurrent clients
2. Each executes list_workflows
3. Measure:
   - All requests complete successfully
   - Response times
   - Error rate

**Expected Results**:
- 100% success rate
- Average response time < 500ms
- No errors

**Related AC**: AC2

---

### TC-PERF-010: Concurrent Workflow Creation

**Priority**: High | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Test concurrent workflow creation.

**Test Steps**:
1. Create 20 workflows concurrently
2. Measure completion time and success rate

**Expected Results**:
- All 20 workflows created
- Total time < 10 seconds
- No race conditions

**Related AC**: AC9

---

### TC-PERF-011: Concurrent Webhook Triggers

**Priority**: Critical | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Test concurrent webhook execution.

**Test Steps**:
1. Create 10 workflows with webhooks
2. Trigger all 10 webhooks simultaneously
3. Monitor executions

**Expected Results**:
- All 10 executions start
- All complete successfully
- No dropped requests

**Related AC**: AC5

---

### TC-PERF-012: Mixed Concurrent Operations

**Priority**: High | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Test mixed concurrent operations.

**Test Steps**:
1. Concurrently execute:
   - 5x list_workflows
   - 5x create workflow
   - 5x get workflow details
   - 5x create credentials
   - 5x list executions
2. Measure overall performance

**Expected Results**:
- All operations complete
- Average response time < 600ms
- No deadlocks

**Related AC**: AC9

---

### TC-PERF-013: Concurrent Read/Write

**Priority**: High | **Type**: Performance | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Test concurrent reads and writes on same resource.

**Test Steps**:
1. Concurrently:
   - 10 clients reading workflow details
   - 1 client updating workflow
2. Verify consistency

**Expected Results**:
- No data corruption
- Reads complete successfully
- Write completes successfully

**Related AC**: AC9

---

## Load Testing Test Cases (4 test cases)

### TC-PERF-014: Sustained Load Test

**Priority**: High | **Type**: Load | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Test sustained load over time.

**Test Steps**:
1. Execute 100 requests/minute for 10 minutes
2. Mix of all tool operations
3. Monitor:
   - Response times
   - Error rate
   - Resource utilization

**Expected Results**:
- 99% success rate
- Response times stable
- No memory leaks

**Related AC**: AC9

---

### TC-PERF-015: Spike Load Test

**Priority**: High | **Type**: Load | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Test sudden traffic spike.

**Test Steps**:
1. Baseline: 10 requests/minute
2. Spike: 500 requests in 1 minute
3. Return to baseline
4. Measure recovery time

**Expected Results**:
- Spike handled (may have slower response)
- No crashes
- Recovery to baseline < 1 minute

**Related AC**: AC9

---

### TC-PERF-016: Large Dataset Performance

**Priority**: Medium | **Type**: Load | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Test with large number of workflows.

**Test Steps**:
1. Create 500+ workflows
2. Execute list_workflows
3. Filter and search operations
4. Measure response times

**Expected Results**:
- List with pagination: < 1 second
- Filtered list: < 1 second
- Search: < 500ms

**Related AC**: AC2

---

### TC-PERF-017: Stress Test to Failure

**Priority**: Medium | **Type**: Stress | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Identify breaking point.

**Test Steps**:
1. Gradually increase load
2. Start: 10 requests/second
3. Increase by 10 every minute
4. Continue until errors occur
5. Document breaking point

**Expected Results**:
- Breaking point identified
- System degrades gracefully
- Clear error messages at limit

**Related AC**: AC9

---

## Resource Utilization Test Cases (3 test cases)

### TC-PERF-018: CPU Utilization

**Priority**: High | **Type**: Resource | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Monitor CPU utilization under load.

**Test Steps**:
1. Execute sustained load test
2. Monitor MCP server CPU usage
3. Monitor N8N server CPU usage

**Expected Results**:
- MCP server CPU: < 70%
- N8N server CPU: < 80%
- No CPU throttling

**Related AC**: AC9

---

### TC-PERF-019: Memory Utilization

**Priority**: High | **Type**: Resource | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Monitor memory usage and detect leaks.

**Test Steps**:
1. Run extended test (1 hour)
2. Execute various operations continuously
3. Monitor memory usage over time

**Expected Results**:
- Memory usage stable
- MCP server memory: < 2GB
- No memory leaks (usage doesn't grow unbounded)

**Related AC**: AC9

---

### TC-PERF-020: Network Bandwidth

**Priority**: Medium | **Type**: Resource | **Phase**: Phase 2 | **Automation**: Yes

**Objective**: Measure network bandwidth utilization.

**Test Steps**:
1. Transfer large workflow details (50+ nodes)
2. List large result sets
3. Measure bandwidth usage

**Expected Results**:
- Efficient data transfer
- No unnecessary data transferred
- Bandwidth usage reasonable

**Related AC**: AC9

---

## Performance Baselines

### Response Time Baselines

| Operation | Target Avg | Target 95th | Target 99th |
|-----------|-----------|-------------|-------------|
| list_workflows | < 300ms | < 500ms | < 1000ms |
| get_workflow_details | < 500ms | < 1000ms | < 2000ms |
| manage_projects | < 300ms | < 500ms | < 1000ms |
| manage_credentials | < 400ms | < 700ms | < 1500ms |
| manage_webhooks | < 300ms | < 500ms | < 1000ms |
| list_node_types | < 500ms | < 800ms | < 1500ms |
| check_execution_status | < 100ms | < 200ms | < 500ms |
| list_executions | < 400ms | < 700ms | < 1500ms |
| get_execution_details | < 600ms | < 1200ms | < 2500ms |

### Throughput Baselines

| Metric | Target |
|--------|--------|
| Requests/minute | 100+ |
| Concurrent users | 10+ |
| Webhook triggers/minute | 60+ |
| Workflows created/minute | 20+ |

### Resource Baselines

| Resource | Target |
|----------|--------|
| MCP Server CPU | < 70% |
| MCP Server Memory | < 2GB |
| N8N Server CPU | < 80% |
| N8N Server Memory | < 4GB |
| Network bandwidth | < 10 Mbps |

---

## Test Suite Summary

**Total Test Cases**: 20

**By Category**:
- Response Time Benchmarks: 8 test cases
- Concurrent Operations: 5 test cases
- Load Testing: 4 test cases
- Resource Utilization: 3 test cases

**By Priority**:
- Critical: 1
- High: 13
- Medium: 6

**Automation**: 100%

---

**Document Type**: Test Case Documentation
**Version**: 1.0
**Created**: 2025-11-06
**Location**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test/test-cases/performance/PERFORMANCE-TEST-CASES.md`
