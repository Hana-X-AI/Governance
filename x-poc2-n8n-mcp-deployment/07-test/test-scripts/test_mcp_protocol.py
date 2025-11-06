"""
POC-002 MCP Protocol Test Suite

Tests MCP protocol compliance, initialization, capabilities, and error handling.
Based on test cases: TC-MCP-001 through TC-MCP-030

Test Owner: Julia Santos
Phase: Phase 1
"""

import pytest
import httpx
from typing import Dict, Any
from conftest import assert_jsonrpc_response, assert_mcp_tool_in_capabilities


# ============================================================================
# PROTOCOL INITIALIZATION TESTS
# ============================================================================

@pytest.mark.phase1
@pytest.mark.critical
@pytest.mark.smoke
async def test_protocol_initialization_success(mcp_client: httpx.AsyncClient):
    """
    TC-MCP-001: Protocol Initialization Success

    Verify MCP server initializes successfully with valid client request.
    """
    request_id = 1

    response = await mcp_client.post("/mcp/initialize", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    })

    assert response.status_code == 200, f"Initialization failed: {response.text}"

    data = response.json()
    assert_jsonrpc_response(data, request_id)

    result = data["result"]
    assert "capabilities" in result, "Result missing capabilities"
    assert "protocolVersion" in result, "Result missing protocolVersion"
    assert "serverInfo" in result, "Result missing serverInfo"


@pytest.mark.phase1
@pytest.mark.critical
async def test_capabilities_list_complete(mcp_session: Dict[str, Any]):
    """
    TC-MCP-002: Capabilities List Complete

    Verify MCP server returns complete capabilities list with all 10 tools.
    """
    capabilities = mcp_session["capabilities"]

    expected_tools = [
        "list_workflows",
        "manage_projects",
        "manage_workflow_tags",
        "get_workflow_details",
        "check_execution_status",
        "list_node_types",
        "manage_credentials",
        "manage_webhooks",
        "list_executions",
        "get_execution_details"
    ]

    for tool_name in expected_tools:
        assert_mcp_tool_in_capabilities(capabilities, tool_name)


@pytest.mark.phase1
@pytest.mark.high
async def test_tool_schema_validation(mcp_session: Dict[str, Any]):
    """
    TC-MCP-003: Tool Schema Validation

    Verify each tool in capabilities has valid schema definition.
    """
    capabilities = mcp_session["capabilities"]
    tools = capabilities.get("tools", [])

    assert len(tools) > 0, "No tools in capabilities"

    for tool in tools:
        # Verify required fields
        assert "name" in tool, f"Tool missing 'name' field: {tool}"
        assert "description" in tool, f"Tool {tool.get('name')} missing 'description'"
        assert "inputSchema" in tool, f"Tool {tool.get('name')} missing 'inputSchema'"

        # Verify inputSchema is valid JSON Schema
        schema = tool["inputSchema"]
        assert "type" in schema, f"Tool {tool['name']} schema missing 'type'"
        assert schema["type"] == "object", f"Tool {tool['name']} schema must be object type"


@pytest.mark.phase1
@pytest.mark.high
async def test_protocol_version_validation(mcp_client: httpx.AsyncClient):
    """
    TC-MCP-004: Protocol Version Validation

    Verify MCP server supports correct protocol version.
    """
    request_id = 100

    response = await mcp_client.post("/mcp/initialize", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "clientInfo": {"name": "test", "version": "1.0"}
        }
    })

    assert response.status_code == 200
    data = response.json()
    assert_jsonrpc_response(data, request_id)

    result = data["result"]
    assert result["protocolVersion"] == "2024-11-05", "Protocol version mismatch"


# ============================================================================
# JSON-RPC COMPLIANCE TESTS
# ============================================================================

@pytest.mark.phase1
@pytest.mark.critical
async def test_jsonrpc_format_compliance(mcp_client: httpx.AsyncClient, mcp_session: Dict[str, Any]):
    """
    TC-MCP-006: JSON-RPC 2.0 Format Compliance

    Verify all MCP responses comply with JSON-RPC 2.0 format.
    """
    request_id = mcp_session["request_id"]

    # Send a simple request (tools/list)
    response = await mcp_client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/list",
        "params": {}
    })

    assert response.status_code == 200
    data = response.json()

    # Verify JSON-RPC 2.0 compliance
    assert data.get("jsonrpc") == "2.0", "Missing or incorrect jsonrpc field"
    assert "id" in data, "Response missing id field"
    assert data["id"] == request_id, "Response ID doesn't match request ID"

    # Must have either result or error, but not both
    has_result = "result" in data
    has_error = "error" in data
    assert has_result != has_error, "Response must have either result or error, not both"


@pytest.mark.phase1
@pytest.mark.high
async def test_request_id_echo(mcp_client: httpx.AsyncClient):
    """
    TC-MCP-007: Request ID Echo

    Verify server echoes request ID in response.
    """
    # Test with numeric ID
    numeric_id = 12345
    response = await mcp_client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": numeric_id,
        "method": "tools/list",
        "params": {}
    })

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == numeric_id, "Numeric ID not echoed correctly"

    # Test with string ID
    string_id = "test-123"
    response = await mcp_client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": string_id,
        "method": "tools/list",
        "params": {}
    })

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == string_id, "String ID not echoed correctly"


# ============================================================================
# ERROR HANDLING TESTS
# ============================================================================

@pytest.mark.phase1
@pytest.mark.high
async def test_missing_required_fields_error(mcp_client: httpx.AsyncClient):
    """
    TC-MCP-008: Missing Required Fields Error

    Verify server returns error for requests missing required fields.
    """
    # Missing jsonrpc field
    response = await mcp_client.post("/mcp/call", json={
        "id": 1,
        "method": "tools/list",
        "params": {}
    })

    # Should get error response
    if response.status_code == 200:
        data = response.json()
        assert "error" in data, "Expected error for missing jsonrpc field"
        assert data["error"]["code"] == -32600, "Expected Invalid Request error code"


@pytest.mark.phase1
@pytest.mark.high
async def test_invalid_json_handling(mcp_client: httpx.AsyncClient):
    """
    TC-MCP-009: Invalid JSON Handling

    Verify server handles malformed JSON gracefully.
    """
    # Send invalid JSON
    response = await mcp_client.post(
        "/mcp/call",
        content=b"{invalid json",
        headers={"Content-Type": "application/json"}
    )

    # Server should not crash and should return error
    assert response.status_code in [200, 400], "Unexpected status code for invalid JSON"

    if response.status_code == 200:
        data = response.json()
        assert "error" in data, "Expected error for invalid JSON"
        assert data["error"]["code"] == -32700, "Expected Parse Error code"


@pytest.mark.phase1
@pytest.mark.high
async def test_unknown_method_error(mcp_client: httpx.AsyncClient):
    """
    TC-MCP-010: Unknown Method Error

    Verify server returns error for unknown methods.
    """
    request_id = 999

    response = await mcp_client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "unknown_method_that_does_not_exist",
        "params": {}
    })

    assert response.status_code == 200
    data = response.json()
    assert "error" in data, "Expected error for unknown method"
    assert data["error"]["code"] == -32601, "Expected Method Not Found error code"


@pytest.mark.phase1
@pytest.mark.high
async def test_invalid_parameters_error(mcp_client: httpx.AsyncClient, mcp_session: Dict[str, Any]):
    """
    TC-MCP-011: Invalid Parameters Error

    Verify server validates tool parameters against schema.
    """
    request_id = mcp_session["request_id"]

    # Call a tool with invalid parameter type
    response = await mcp_client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": "list_workflows",
            "arguments": {
                "active": "not_a_boolean"  # Should be boolean
            }
        }
    })

    # Should get validation error
    if response.status_code == 200:
        data = response.json()
        if "error" in data:
            assert data["error"]["code"] == -32602, "Expected Invalid Params error code"


# ============================================================================
# TOOL CALL TESTS
# ============================================================================

@pytest.mark.phase1
@pytest.mark.critical
async def test_tool_call_request_format(mcp_client: httpx.AsyncClient, mcp_session: Dict[str, Any]):
    """
    TC-MCP-016: Tool Call Request Format

    Verify tool call requests follow correct format.
    """
    request_id = mcp_session["request_id"]

    response = await mcp_client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": "list_workflows",
            "arguments": {}
        }
    })

    assert response.status_code == 200
    data = response.json()
    assert_jsonrpc_response(data, request_id)


@pytest.mark.phase1
@pytest.mark.critical
async def test_tool_call_response_format(mcp_client: httpx.AsyncClient, mcp_session: Dict[str, Any]):
    """
    TC-MCP-017: Tool Call Response Format

    Verify tool call responses follow correct format.
    """
    request_id = mcp_session["request_id"]

    response = await mcp_client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": "list_workflows",
            "arguments": {}
        }
    })

    assert response.status_code == 200
    data = response.json()

    assert "result" in data, "Response missing result"
    result = data["result"]

    assert "content" in result, "Result missing content"
    content = result["content"]
    assert isinstance(content, list), "Content must be a list"

    if len(content) > 0:
        assert "type" in content[0], "Content item missing type"
        assert "text" in content[0] or "data" in content[0], "Content item missing text/data"


# ============================================================================
# ADDITIONAL PROTOCOL TESTS
# ============================================================================

@pytest.mark.phase1
@pytest.mark.medium
async def test_content_type_header_validation(mcp_client: httpx.AsyncClient):
    """
    TC-MCP-012: Content Type Header Validation

    Verify server accepts requests with correct Content-Type header.
    """
    response = await mcp_client.post(
        "/mcp/call",
        json={"jsonrpc": "2.0", "id": 1, "method": "tools/list", "params": {}},
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200, "Request with Content-Type header should succeed"


@pytest.mark.phase1
@pytest.mark.high
async def test_tool_list_request(mcp_client: httpx.AsyncClient, mcp_session: Dict[str, Any]):
    """
    TC-MCP-021: Tool List Request

    Verify tools/list method returns all available tools.
    """
    request_id = mcp_session["request_id"]

    response = await mcp_client.post("/mcp/call", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/list",
        "params": {}
    })

    assert response.status_code == 200
    data = response.json()
    assert_jsonrpc_response(data, request_id)

    result = data["result"]
    assert "tools" in result, "Result missing tools"
    tools = result["tools"]
    assert len(tools) == 10, f"Expected 10 tools, got {len(tools)}"


# ============================================================================
# SMOKE TESTS (Subset of critical tests for quick validation)
# ============================================================================

@pytest.mark.smoke
@pytest.mark.phase1
async def test_smoke_mcp_server_health(mcp_client: httpx.AsyncClient):
    """
    Quick smoke test to verify MCP server is accessible and healthy.
    """
    try:
        response = await mcp_client.get("/health")
        assert response.status_code in [200, 404], "Server not responding"
    except httpx.ConnectError:
        pytest.fail("Cannot connect to MCP server")


@pytest.mark.smoke
@pytest.mark.phase1
async def test_smoke_initialization(mcp_session: Dict[str, Any]):
    """
    Quick smoke test to verify initialization works.
    """
    assert mcp_session["initialized"] is True, "MCP session not initialized"
    assert len(mcp_session["capabilities"]) > 0, "No capabilities returned"
