# MCP Protocol Test Cases

## Document Control

| Field | Value |
|-------|-------|
| **Document ID** | POC-002-TC-MCP-001 |
| **Version** | 1.0 |
| **Created** | 2025-11-06 |
| **Test Suite** | MCP Protocol |
| **Total Test Cases** | 30 |
| **Automation** | 100% |
| **Priority** | Critical |
| **Phase** | Phase 1 |

---

## Test Suite Overview

**Objective**: Validate MCP protocol compliance, initialization, capabilities, request/response lifecycle, and error handling.

**Scope**:
- Protocol initialization
- Capabilities negotiation
- Request/response format validation
- Error handling and edge cases
- Security and authentication

**Related Acceptance Criteria**: AC1 (MCP Protocol Compliance)

---

## Test Cases

### TC-MCP-001: Protocol Initialization Success

**Priority**: Critical
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify MCP server initializes successfully with valid client request.

**Preconditions**:
- MCP server running on hx-n8n-mcp-server (192.168.10.194:3000)
- Network connectivity established

**Test Steps**:
1. Send MCP initialize request to `/mcp/initialize`
2. Include valid client information:
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "initialize",
     "params": {
       "protocolVersion": "2024-11-05",
       "clientInfo": {
         "name": "test-client",
         "version": "1.0.0"
       }
     }
   }
   ```
3. Verify response

**Expected Results**:
- HTTP 200 status code
- Valid JSON-RPC 2.0 response
- Response includes server capabilities
- Response includes protocol version
- Response includes server info

**Postconditions**:
- Server ready for tool requests

**Related AC**: AC1

---

### TC-MCP-002: Capabilities List Complete

**Priority**: Critical
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify MCP server returns complete capabilities list with all 10 tools.

**Preconditions**:
- MCP server initialized successfully

**Test Steps**:
1. Parse initialization response capabilities
2. Verify tools array contains all expected tools

**Expected Results**:
Capabilities include all 10 tools:
1. `list_workflows`
2. `manage_projects`
3. `manage_workflow_tags`
4. `get_workflow_details`
5. `check_execution_status`
6. `list_node_types`
7. `manage_credentials`
8. `manage_webhooks`
9. `list_executions`
10. `get_execution_details`

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-003: Tool Schema Validation

**Priority**: High
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify each tool in capabilities has valid schema definition.

**Preconditions**:
- MCP server initialized
- Capabilities received

**Test Steps**:
1. For each tool in capabilities
2. Verify tool has `name` field
3. Verify tool has `description` field
4. Verify tool has `inputSchema` field
5. Verify inputSchema follows JSON Schema format

**Expected Results**:
- Each tool has required fields
- Schemas are valid JSON Schema
- Schemas match expected parameters

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-004: Protocol Version Validation

**Priority**: High
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify MCP server supports correct protocol version.

**Preconditions**:
- None

**Test Steps**:
1. Send initialize request with protocol version "2024-11-05"
2. Verify server accepts version
3. Verify server responds with same version

**Expected Results**:
- Server accepts protocol version "2024-11-05"
- Response includes matching protocol version
- No version mismatch errors

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-005: Invalid Protocol Version Rejection

**Priority**: Medium
**Type**: Negative
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify MCP server rejects unsupported protocol versions.

**Preconditions**:
- None

**Test Steps**:
1. Send initialize request with invalid protocol version "1999-01-01"
2. Verify server rejects request

**Expected Results**:
- Server returns error response
- Error indicates unsupported protocol version
- Initialization fails gracefully

**Postconditions**:
- Server remains available for valid requests

**Related AC**: AC1, AC8

---

### TC-MCP-006: JSON-RPC 2.0 Format Compliance

**Priority**: Critical
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify all MCP responses comply with JSON-RPC 2.0 format.

**Preconditions**:
- None

**Test Steps**:
1. Send various MCP requests
2. Verify each response includes:
   - `jsonrpc`: "2.0"
   - `id`: matches request id
   - `result` or `error` (not both)

**Expected Results**:
- All responses have `jsonrpc: "2.0"`
- Response `id` matches request `id`
- Either `result` or `error` present (exclusive)
- No additional top-level fields

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-007: Request ID Echo

**Priority**: High
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server echoes request ID in response.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send request with numeric ID: `"id": 12345`
2. Verify response has same ID
3. Send request with string ID: `"id": "test-123"`
4. Verify response has same ID

**Expected Results**:
- Response ID matches request ID exactly
- Both numeric and string IDs supported

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-008: Missing Required Fields Error

**Priority**: High
**Type**: Negative
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server returns error for requests missing required fields.

**Preconditions**:
- None

**Test Steps**:
1. Send request without `jsonrpc` field
2. Verify error response
3. Send request without `method` field
4. Verify error response
5. Send request without `id` field
6. Verify error response

**Expected Results**:
- Server returns JSON-RPC error response
- Error code indicates invalid request (-32600)
- Error message describes missing field

**Postconditions**:
- Server remains operational

**Related AC**: AC1, AC8

---

### TC-MCP-009: Invalid JSON Handling

**Priority**: High
**Type**: Negative
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server handles malformed JSON gracefully.

**Preconditions**:
- None

**Test Steps**:
1. Send request with invalid JSON syntax
2. Verify error response

**Expected Results**:
- Server returns JSON-RPC error
- Error code: -32700 (Parse error)
- Server does not crash

**Postconditions**:
- Server remains operational

**Related AC**: AC1, AC8

---

### TC-MCP-010: Unknown Method Error

**Priority**: High
**Type**: Negative
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server returns error for unknown methods.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send request with non-existent method: `"method": "unknown_method"`
2. Verify error response

**Expected Results**:
- Server returns JSON-RPC error
- Error code: -32601 (Method not found)
- Error message indicates method not found

**Postconditions**:
- Server remains operational

**Related AC**: AC1, AC8

---

### TC-MCP-011: Invalid Parameters Error

**Priority**: High
**Type**: Negative
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server validates tool parameters against schema.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send tool call with invalid parameters (wrong type)
2. Verify error response
3. Send tool call with missing required parameter
4. Verify error response

**Expected Results**:
- Server returns JSON-RPC error
- Error code: -32602 (Invalid params)
- Error message describes validation failure

**Postconditions**:
- Server remains operational

**Related AC**: AC1, AC8

---

### TC-MCP-012: Content Type Header Validation

**Priority**: Medium
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server accepts requests with correct Content-Type header.

**Preconditions**:
- None

**Test Steps**:
1. Send request with `Content-Type: application/json`
2. Verify successful processing

**Expected Results**:
- Request accepted
- Response successful

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-013: Missing Content Type Handling

**Priority**: Medium
**Type**: Negative
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server behavior when Content-Type header is missing.

**Preconditions**:
- None

**Test Steps**:
1. Send request without Content-Type header
2. Observe server response

**Expected Results**:
- Server either:
  - Accepts request and processes (lenient)
  - Returns 415 Unsupported Media Type (strict)
- Server does not crash

**Postconditions**:
- Server remains operational

**Related AC**: AC1, AC8

---

### TC-MCP-014: Large Request Handling

**Priority**: Medium
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server handles large valid requests.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send request with large parameters (e.g., long workflow description)
2. Verify processing

**Expected Results**:
- Server accepts request
- Server processes without timeout
- Response successful

**Postconditions**:
- Server remains operational

**Related AC**: AC1

---

### TC-MCP-015: Concurrent Request Handling

**Priority**: High
**Type**: Performance
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server handles multiple concurrent requests.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send 10 concurrent requests with different IDs
2. Verify all responses received
3. Verify each response has correct ID

**Expected Results**:
- All 10 requests processed
- All responses have matching IDs
- No requests dropped
- No response mixing

**Postconditions**:
- Server remains operational

**Related AC**: AC1

---

### TC-MCP-016: Tool Call Request Format

**Priority**: Critical
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify tool call requests follow correct format.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send tool call request:
   ```json
   {
     "jsonrpc": "2.0",
     "id": 1,
     "method": "tools/call",
     "params": {
       "name": "list_workflows",
       "arguments": {}
     }
   }
   ```
2. Verify acceptance

**Expected Results**:
- Request accepted
- Tool executes
- Response includes tool result

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-017: Tool Call Response Format

**Priority**: Critical
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify tool call responses follow correct format.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Execute any tool call
2. Verify response structure

**Expected Results**:
Response includes:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "..."
      }
    ]
  }
}
```

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-018: Error Response Format

**Priority**: High
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify error responses follow JSON-RPC 2.0 error format.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Trigger various errors (invalid method, invalid params, etc.)
2. Verify error response format

**Expected Results**:
Error response includes:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32XXX,
    "message": "Error description",
    "data": {}  // Optional
  }
}
```

**Postconditions**:
- None

**Related AC**: AC1, AC8

---

### TC-MCP-019: Health Check Endpoint

**Priority**: Medium
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server health check endpoint.

**Preconditions**:
- None

**Test Steps**:
1. Send HTTP GET to `/health`
2. Verify response

**Expected Results**:
- HTTP 200 status
- Response indicates server is healthy

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-020: Server Info Metadata

**Priority**: Low
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server returns appropriate metadata in initialization.

**Preconditions**:
- None

**Test Steps**:
1. Send initialize request
2. Verify server info in response

**Expected Results**:
Response includes serverInfo:
- `name`: server name
- `version`: server version

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-021: Tool List Request

**Priority**: High
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify tools/list method returns all available tools.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send `tools/list` request
2. Verify response contains all tools

**Expected Results**:
- Response includes array of 10 tools
- Each tool has name, description, inputSchema

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-022: Unsupported Method Handling

**Priority**: Medium
**Type**: Negative
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server rejects unsupported MCP methods.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send request with valid MCP method not implemented by server
2. Verify error response

**Expected Results**:
- JSON-RPC error response
- Error code: -32601 (Method not found)

**Postconditions**:
- Server operational

**Related AC**: AC1, AC8

---

### TC-MCP-023: Request Timeout Handling

**Priority**: Medium
**Type**: Reliability
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server responds within reasonable timeout.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send various requests
2. Measure response time

**Expected Results**:
- All responses within 5 seconds
- No timeouts for standard operations

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-024: Server Restart Recovery

**Priority**: High
**Type**: Reliability
**Phase**: Phase 1
**Automation**: No (Manual)

**Objective**: Verify server recovers properly after restart.

**Preconditions**:
- Server running

**Test Steps**:
1. Restart MCP server
2. Wait for server to start
3. Send initialize request
4. Execute tool calls

**Expected Results**:
- Server starts successfully
- Initialization succeeds
- Tools function normally
- No state corruption

**Postconditions**:
- Server operational

**Related AC**: AC1, AC8

---

### TC-MCP-025: Authentication (If Implemented)

**Priority**: High
**Type**: Security
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify authentication mechanism if implemented.

**Preconditions**:
- Server configured with authentication

**Test Steps**:
1. Send request without authentication
2. Verify rejection
3. Send request with valid authentication
4. Verify acceptance

**Expected Results**:
- Unauthenticated requests rejected (401)
- Authenticated requests accepted

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-026: CORS Headers (If Web Access)

**Priority**: Low
**Type**: Security
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify CORS headers if server supports web access.

**Preconditions**:
- None

**Test Steps**:
1. Send OPTIONS request
2. Verify CORS headers

**Expected Results**:
- Appropriate CORS headers present
- Access-Control-Allow-Origin configured

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-027: Batch Requests (If Supported)

**Priority**: Low
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify batch request handling if supported.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send batch request (array of requests)
2. Verify batch response

**Expected Results**:
- Server processes batch
- Returns array of responses
- Each response has matching ID

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-028: Notification Support (If Applicable)

**Priority**: Low
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify server handles JSON-RPC notifications.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send notification (request without ID)
2. Verify server accepts

**Expected Results**:
- Server accepts notification
- No response returned
- No errors

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-029: Resource Endpoint (If Supported)

**Priority**: Low
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify resources endpoint if MCP server exposes resources.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send `resources/list` request
2. Verify response

**Expected Results**:
- Response indicates available resources (or empty if none)
- No errors

**Postconditions**:
- None

**Related AC**: AC1

---

### TC-MCP-030: Prompt Endpoint (If Supported)

**Priority**: Low
**Type**: Functional
**Phase**: Phase 1
**Automation**: Yes

**Objective**: Verify prompts endpoint if MCP server exposes prompts.

**Preconditions**:
- Server initialized

**Test Steps**:
1. Send `prompts/list` request
2. Verify response

**Expected Results**:
- Response indicates available prompts (or empty if none)
- No errors

**Postconditions**:
- None

**Related AC**: AC1

---

## Test Suite Summary

**Total Test Cases**: 30
**Critical Priority**: 6
**High Priority**: 12
**Medium Priority**: 8
**Low Priority**: 4

**Automation Rate**: 100% (29 automated, 1 manual)

**Coverage**:
- Protocol initialization: 5 test cases
- Capabilities and schema: 4 test cases
- JSON-RPC compliance: 8 test cases
- Error handling: 8 test cases
- Security: 2 test cases
- Additional features: 3 test cases

---

**Document Type**: Test Case Documentation
**Version**: 1.0
**Created**: 2025-11-06
**Location**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test/test-cases/mcp-protocol/MCP-PROTOCOL-TEST-CASES.md`
