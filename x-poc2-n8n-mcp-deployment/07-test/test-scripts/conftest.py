"""
POC-002 pytest configuration and shared fixtures.

This module provides pytest configuration, fixtures, and test utilities
for testing the N8N-MCP integration.

Based on pytest best practices from /srv/knowledge/vault/pytest/
"""

import asyncio
import os
from typing import AsyncGenerator, Dict, Any
import pytest
import httpx
from pydantic import BaseModel


# ============================================================================
# CONFIGURATION
# ============================================================================

class TestConfig(BaseModel):
    """Test environment configuration."""

    # Server URLs
    mcp_server_url: str = os.getenv(
        "N8N_MCP_SERVER_URL",
        "http://192.168.10.194:3000"
    )
    n8n_server_url: str = os.getenv(
        "N8N_SERVER_URL",
        "http://192.168.10.20:5678"
    )

    # Authentication
    n8n_api_key: str | None = os.getenv("N8N_API_KEY")

    # Test settings
    timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0

    # Test data
    test_project_name: str = "POC-002 Test Project"
    test_workflow_prefix: str = "test_workflow_"
    test_credential_prefix: str = "test_credential_"


@pytest.fixture(scope="session")
def test_config() -> TestConfig:
    """Provide test configuration."""
    return TestConfig()


# ============================================================================
# ASYNC HTTP CLIENT FIXTURES
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def http_client(test_config: TestConfig) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide async HTTP client for tests."""
    async with httpx.AsyncClient(
        timeout=test_config.timeout,
        follow_redirects=True
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def mcp_client(test_config: TestConfig) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide MCP server HTTP client."""
    async with httpx.AsyncClient(
        base_url=test_config.mcp_server_url,
        timeout=test_config.timeout,
        headers={"Content-Type": "application/json"}
    ) as client:
        yield client


@pytest.fixture(scope="session")
async def n8n_client(test_config: TestConfig) -> AsyncGenerator[httpx.AsyncClient, None]:
    """Provide N8N server HTTP client."""
    headers = {"Content-Type": "application/json"}
    if test_config.n8n_api_key:
        headers["X-N8N-API-KEY"] = test_config.n8n_api_key

    async with httpx.AsyncClient(
        base_url=test_config.n8n_server_url,
        timeout=test_config.timeout,
        headers=headers
    ) as client:
        yield client


# ============================================================================
# MCP PROTOCOL FIXTURES
# ============================================================================

@pytest.fixture
async def mcp_session(mcp_client: httpx.AsyncClient) -> Dict[str, Any]:
    """Initialize MCP session and return session info."""
    request_id = 1

    # Send initialize request
    response = await mcp_client.post("/mcp/initialize", json={
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "clientInfo": {
                "name": "poc-002-test-client",
                "version": "1.0.0"
            }
        }
    })

    assert response.status_code == 200, f"MCP initialization failed: {response.text}"

    result = response.json()
    assert "result" in result, "MCP initialization response missing result"

    return {
        "initialized": True,
        "capabilities": result["result"].get("capabilities", {}),
        "serverInfo": result["result"].get("serverInfo", {}),
        "request_id": request_id + 1
    }


@pytest.fixture
def next_request_id(mcp_session: Dict[str, Any]):
    """Generate next request ID for MCP calls."""
    request_id = mcp_session["request_id"]
    mcp_session["request_id"] += 1
    return request_id


# ============================================================================
# TEST DATA FIXTURES
# ============================================================================

@pytest.fixture
def sample_workflow_data() -> Dict[str, Any]:
    """Provide sample workflow data for testing."""
    return {
        "name": "Test Workflow",
        "active": False,
        "nodes": [
            {
                "id": "node-1",
                "name": "Start",
                "type": "n8n-nodes-base.start",
                "position": [250, 300],
                "parameters": {}
            },
            {
                "id": "node-2",
                "name": "Set",
                "type": "n8n-nodes-base.set",
                "position": [450, 300],
                "parameters": {
                    "values": {
                        "string": [
                            {
                                "name": "test",
                                "value": "value"
                            }
                        ]
                    }
                }
            }
        ],
        "connections": {
            "Start": {
                "main": [
                    [
                        {
                            "node": "Set",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "settings": {
            "executionOrder": "v1"
        }
    }


@pytest.fixture
def sample_project_data(test_config: TestConfig) -> Dict[str, Any]:
    """Provide sample project data for testing."""
    return {
        "name": test_config.test_project_name,
        "type": "team"
    }


@pytest.fixture
def sample_credential_data() -> Dict[str, Any]:
    """Provide sample credential data for testing."""
    return {
        "type": "httpBasicAuth",
        "name": "Test HTTP Basic Auth",
        "data": {
            "user": "testuser",
            "password": "testpassword"
        }
    }


# ============================================================================
# CLEANUP FIXTURES
# ============================================================================

@pytest.fixture
async def cleanup_workflows(mcp_client: httpx.AsyncClient, test_config: TestConfig):
    """Cleanup test workflows after test."""
    created_workflow_ids = []

    yield created_workflow_ids

    # Cleanup created workflows
    for workflow_id in created_workflow_ids:
        try:
            # Delete workflow via N8N API
            await mcp_client.delete(f"/api/v1/workflows/{workflow_id}")
        except Exception as e:
            print(f"Warning: Failed to cleanup workflow {workflow_id}: {e}")


@pytest.fixture
async def cleanup_projects(mcp_client: httpx.AsyncClient):
    """Cleanup test projects after test."""
    created_project_ids = []

    yield created_project_ids

    # Cleanup created projects
    for project_id in created_project_ids:
        try:
            await mcp_client.delete(f"/api/v1/projects/{project_id}")
        except Exception as e:
            print(f"Warning: Failed to cleanup project {project_id}: {e}")


@pytest.fixture
async def cleanup_credentials(mcp_client: httpx.AsyncClient):
    """Cleanup test credentials after test."""
    created_credential_ids = []

    yield created_credential_ids

    # Cleanup created credentials
    for credential_id in created_credential_ids:
        try:
            await mcp_client.delete(f"/api/v1/credentials/{credential_id}")
        except Exception as e:
            print(f"Warning: Failed to cleanup credential {credential_id}: {e}")


# ============================================================================
# PYTEST CONFIGURATION
# ============================================================================

def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "phase1: Phase 1 tests (MCP server only, no N8N integration)"
    )
    config.addinivalue_line(
        "markers", "phase2: Phase 2 tests (with N8N integration)"
    )
    config.addinivalue_line(
        "markers", "critical: Critical priority tests"
    )
    config.addinivalue_line(
        "markers", "high: High priority tests"
    )
    config.addinivalue_line(
        "markers", "medium: Medium priority tests"
    )
    config.addinivalue_line(
        "markers", "low: Low priority tests"
    )
    config.addinivalue_line(
        "markers", "smoke: Smoke test suite (quick validation)"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests"
    )
    config.addinivalue_line(
        "markers", "performance: Performance tests"
    )
    config.addinivalue_line(
        "markers", "reliability: Reliability tests"
    )


# ============================================================================
# HELPER FUNCTIONS (available to all tests)
# ============================================================================

def assert_jsonrpc_response(response_data: Dict[str, Any], expected_id: int | str):
    """Assert valid JSON-RPC 2.0 response format."""
    assert "jsonrpc" in response_data, "Response missing 'jsonrpc' field"
    assert response_data["jsonrpc"] == "2.0", "Invalid JSON-RPC version"
    assert "id" in response_data, "Response missing 'id' field"
    assert response_data["id"] == expected_id, f"Response ID mismatch: {response_data['id']} != {expected_id}"

    # Should have either result or error, but not both
    has_result = "result" in response_data
    has_error = "error" in response_data
    assert has_result != has_error, "Response must have either 'result' or 'error', not both"


def assert_mcp_tool_in_capabilities(capabilities: Dict[str, Any], tool_name: str):
    """Assert that a tool exists in MCP capabilities."""
    assert "tools" in capabilities, "Capabilities missing 'tools' field"
    tools = capabilities["tools"]
    assert isinstance(tools, list), "Capabilities 'tools' must be a list"

    tool_names = [tool.get("name") for tool in tools]
    assert tool_name in tool_names, f"Tool '{tool_name}' not found in capabilities: {tool_names}"


def assert_workflow_structure(workflow: Dict[str, Any]):
    """Assert valid workflow structure."""
    required_fields = ["id", "name", "active", "createdAt", "updatedAt"]
    for field in required_fields:
        assert field in workflow, f"Workflow missing required field: {field}"
