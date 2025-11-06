"""
N8N MCP Testing Framework - Shared Fixtures (conftest.py)

This module provides shared pytest fixtures following SOLID principles:
- SRP: Each fixture has a single, well-defined purpose
- OCP: Base fixtures extensible without modification
- LSP: Fixtures are substitutable (real/mock clients)
- ISP: Segregated fixtures for different test needs
- DIP: Tests depend on fixture abstractions, not concrete implementations

Knowledge Sources:
- /srv/knowledge/vault/n8n-mcp-main/src/mcp/tools.ts (23 doc tools)
- /srv/knowledge/vault/n8n-mcp-main/src/mcp/tools-n8n-manager.ts (21 mgmt tools)
- /srv/knowledge/vault/pytest/ (fixture patterns)

Author: Julia Chen, Testing Framework Specialist
Date: 2025-11-06
"""

import pytest
import asyncio
import httpx
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# CONFIGURATION CLASSES (SOLID SRP - Single Responsibility)
# ============================================================================

class TestPhase(Enum):
    """Test phases for N8N MCP deployment"""
    DOCUMENTATION = "documentation"  # Phase 1: 23 doc tools, no N8N instance
    MANAGEMENT = "management"        # Phase 2: 21 mgmt tools, requires N8N instance
    INTEGRATION = "integration"      # Phase 3: Full E2E testing


@dataclass
class MCPServerConfig:
    """Configuration for N8N MCP server

    CORRECTED IPs (from Olivia feedback):
    - MCP Server: 192.168.10.214:3000 (NOT .194)
    - N8N Server: 192.168.10.215:5678 (NOT .20)
    """
    host: str = "192.168.10.214"
    port: int = 3000
    base_url: str = "http://192.168.10.214:3000"
    timeout: int = 30


@dataclass
class N8NServerConfig:
    """Configuration for N8N instance server"""
    host: str = "192.168.10.215"
    port: int = 5678
    base_url: str = "http://192.168.10.215:5678"
    api_key: Optional[str] = None  # Required for Phase 2 management tools
    timeout: int = 30


@dataclass
class TestDatabaseConfig:
    """Configuration for test database expectations"""
    total_nodes: int = 536
    ai_optimized_nodes: int = 263
    trigger_nodes: int = 104
    doc_coverage_percent: float = 87.0
    min_templates: int = 2500
    min_template_configs: int = 2646


# ============================================================================
# SESSION-SCOPED FIXTURES (SOLID OCP - Open for Extension)
# ============================================================================

@pytest.fixture(scope="session")
def mcp_server_config() -> MCPServerConfig:
    """
    Session-scoped MCP server configuration.

    Scope: session - Created once for all tests
    Purpose: Provide consistent MCP server configuration
    SOLID: SRP - Single source of truth for MCP config

    Returns:
        MCPServerConfig with correct IP (192.168.10.214)
    """
    return MCPServerConfig()


@pytest.fixture(scope="session")
def n8n_server_config() -> N8NServerConfig:
    """
    Session-scoped N8N server configuration.

    Scope: session - Created once for all tests
    Purpose: Provide consistent N8N server configuration
    SOLID: SRP - Single source of truth for N8N config

    Returns:
        N8NServerConfig with correct IP (192.168.10.215)
    """
    import os
    return N8NServerConfig(
        api_key=os.getenv("N8N_API_KEY")  # Optional: Required for Phase 2 only
    )


@pytest.fixture(scope="session")
def test_database_config() -> TestDatabaseConfig:
    """
    Session-scoped test database expectations.

    Scope: session - Created once for all tests
    Purpose: Define expected database state for validation
    SOLID: SRP - Single source of truth for DB expectations

    Returns:
        TestDatabaseConfig with node counts and coverage expectations
    """
    return TestDatabaseConfig()


@pytest.fixture(scope="session")
def event_loop():
    """
    Session-scoped event loop for async tests.

    Scope: session - Reuse event loop across tests for performance
    Purpose: Support async/await testing patterns

    Yields:
        asyncio event loop
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# FUNCTION-SCOPED FIXTURES (SOLID DIP - Dependency Inversion)
# ============================================================================

@pytest.fixture
def http_client(mcp_server_config: MCPServerConfig) -> httpx.Client:
    """
    Function-scoped HTTP client for MCP server.

    Scope: function - Fresh client for each test
    Purpose: Provide HTTP communication abstraction
    SOLID: DIP - Tests depend on this abstraction, not concrete httpx
    SOLID: LSP - Can be substituted with mock client

    Args:
        mcp_server_config: Injected MCP configuration

    Yields:
        httpx.Client configured for MCP server
    """
    client = httpx.Client(
        base_url=mcp_server_config.base_url,
        timeout=mcp_server_config.timeout,
        headers={"Content-Type": "application/json"}
    )
    yield client
    client.close()


@pytest.fixture
async def async_http_client(mcp_server_config: MCPServerConfig) -> httpx.AsyncClient:
    """
    Function-scoped async HTTP client for MCP server.

    Scope: function - Fresh async client for each test
    Purpose: Support async test operations
    SOLID: DIP - Async tests depend on this abstraction

    Args:
        mcp_server_config: Injected MCP configuration

    Yields:
        httpx.AsyncClient configured for MCP server
    """
    client = httpx.AsyncClient(
        base_url=mcp_server_config.base_url,
        timeout=mcp_server_config.timeout,
        headers={"Content-Type": "application/json"}
    )
    yield client
    await client.aclose()


@pytest.fixture
def n8n_http_client(n8n_server_config: N8NServerConfig) -> httpx.Client:
    """
    Function-scoped HTTP client for N8N server.

    Scope: function - Fresh client for each test
    Purpose: Provide HTTP communication with N8N API
    SOLID: DIP - Phase 2 tests depend on this abstraction

    Args:
        n8n_server_config: Injected N8N configuration

    Yields:
        httpx.Client configured for N8N API
    """
    headers = {"Content-Type": "application/json"}
    if n8n_server_config.api_key:
        headers["X-N8N-API-KEY"] = n8n_server_config.api_key

    client = httpx.Client(
        base_url=n8n_server_config.base_url,
        timeout=n8n_server_config.timeout,
        headers=headers
    )
    yield client
    client.close()


# ============================================================================
# SPECIALIZED FIXTURES (SOLID ISP - Interface Segregation)
# ============================================================================

@pytest.fixture
def doc_tools_list() -> List[str]:
    """
    List of 23 documentation tools (Phase 1).

    Source: /srv/knowledge/vault/n8n-mcp-main/src/mcp/tools.ts
    Phase: 1 - NO N8N instance required

    Returns:
        List of 23 documentation tool names
    """
    return [
        "tools_documentation",
        "list_nodes",
        "get_node_info",
        "search_nodes",
        "list_ai_tools",
        "get_node_documentation",
        "get_database_statistics",
        "get_node_essentials",
        "search_node_properties",
        "list_tasks",
        "validate_node_operation",
        "validate_node_minimal",
        "get_property_dependencies",
        "get_node_as_tool_info",
        "list_templates",
        "list_node_templates",
        "get_template",
        "search_templates",
        "get_templates_for_task",
        "search_templates_by_metadata",
        "validate_workflow",
        "validate_workflow_connections",
        "validate_workflow_expressions",
    ]


@pytest.fixture
def management_tools_list() -> List[str]:
    """
    List of 21 management tools (Phase 2).

    Source: /srv/knowledge/vault/n8n-mcp-main/src/mcp/tools-n8n-manager.ts
    Phase: 2 - REQUIRES N8N instance with API key

    Returns:
        List of 21 management tool names
    """
    return [
        # Workflow Management (11 tools)
        "n8n_create_workflow",
        "n8n_get_workflow",
        "n8n_get_workflow_details",
        "n8n_get_workflow_structure",
        "n8n_get_workflow_minimal",
        "n8n_update_full_workflow",
        "n8n_update_partial_workflow",
        "n8n_delete_workflow",
        "n8n_list_workflows",
        "n8n_validate_workflow",
        "n8n_autofix_workflow",
        # Execution Management (4 tools)
        "n8n_trigger_webhook_workflow",
        "n8n_get_execution",
        "n8n_list_executions",
        "n8n_delete_execution",
        # System Tools (3 tools)
        "n8n_health_check",
        "n8n_list_available_tools",
        "n8n_diagnostic",
    ]


@pytest.fixture
def all_tools_list(doc_tools_list: List[str], management_tools_list: List[str]) -> List[str]:
    """
    Combined list of all 44 tools.

    Composition: 23 doc tools + 21 management tools = 44 total

    Args:
        doc_tools_list: 23 documentation tools
        management_tools_list: 21 management tools

    Returns:
        List of all 44 tool names
    """
    return doc_tools_list + management_tools_list


@pytest.fixture
def priority_tools() -> Dict[str, List[str]]:
    """
    Tool prioritization for testing coverage.

    Priority 1: Critical path tools (80% coverage target)
    Priority 2: Common usage tools (60% coverage target)
    Priority 3: Specialized tools (40% coverage target)

    Returns:
        Dict mapping priority levels to tool lists
    """
    return {
        "p1_documentation": [
            "list_nodes",
            "get_node_essentials",
            "search_nodes",
            "validate_node_operation",
            "get_database_statistics",
        ],
        "p1_management": [
            "n8n_create_workflow",
            "n8n_get_workflow",
            "n8n_update_full_workflow",
            "n8n_list_workflows",
            "n8n_health_check",
        ],
        "p2_documentation": [
            "get_node_info",
            "get_node_documentation",
            "list_templates",
            "search_templates",
            "validate_workflow",
        ],
        "p2_management": [
            "n8n_update_partial_workflow",
            "n8n_validate_workflow",
            "n8n_trigger_webhook_workflow",
            "n8n_get_execution",
            "n8n_list_executions",
        ],
    }


# ============================================================================
# TEST DATA FIXTURES (SOLID SRP - Single Responsibility)
# ============================================================================

@pytest.fixture
def sample_node_types() -> List[str]:
    """
    Sample node types for testing.

    Format: "nodes-base.{nodeName}" or "nodes-langchain.{nodeName}"

    Returns:
        List of valid node type identifiers
    """
    return [
        "nodes-base.httpRequest",
        "nodes-base.webhook",
        "nodes-base.slack",
        "nodes-base.code",
        "nodes-base.set",
        "nodes-langchain.agent",
        "nodes-langchain.chainLlm",
    ]


@pytest.fixture
def sample_workflow() -> Dict[str, Any]:
    """
    Sample workflow structure for testing.

    Minimal valid workflow with webhook trigger and HTTP request.

    Returns:
        Dict representing a valid N8N workflow
    """
    return {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "webhook-1",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [250, 300],
                "parameters": {
                    "path": "test-webhook",
                    "httpMethod": "GET",
                    "responseMode": "onReceived",
                },
            },
            {
                "id": "http-1",
                "name": "HTTP Request",
                "type": "n8n-nodes-base.httpRequest",
                "typeVersion": 3,
                "position": [450, 300],
                "parameters": {
                    "url": "https://jsonplaceholder.typicode.com/posts/1",
                    "method": "GET",
                },
            },
        ],
        "connections": {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "HTTP Request",
                            "type": "main",
                            "index": 0,
                        }
                    ]
                ]
            }
        },
    }


# ============================================================================
# HELPER FUNCTION FIXTURES (SOLID SRP - Utility Functions)
# ============================================================================

@pytest.fixture
def assert_tool_response():
    """
    Helper function to assert tool response structure.

    Returns:
        Callable for validating MCP tool responses
    """
    def _assert(response: Dict[str, Any], expected_keys: Optional[List[str]] = None):
        """
        Assert that tool response has expected structure.

        Args:
            response: Tool response dictionary
            expected_keys: Optional list of required keys
        """
        assert isinstance(response, dict), "Response must be a dictionary"
        assert "error" not in response or response["error"] is None, \
            f"Tool returned error: {response.get('error')}"

        if expected_keys:
            for key in expected_keys:
                assert key in response, f"Response missing key: {key}"

    return _assert


@pytest.fixture
def assert_http_success():
    """
    Helper function to assert HTTP response success.

    Returns:
        Callable for validating HTTP responses
    """
    def _assert(response: httpx.Response, expected_status: int = 200):
        """
        Assert that HTTP response is successful.

        Args:
            response: httpx Response object
            expected_status: Expected HTTP status code (default 200)
        """
        assert response.status_code == expected_status, \
            f"Expected status {expected_status}, got {response.status_code}: {response.text}"

    return _assert


# ============================================================================
# MARKERS (SOLID ISP - Segregate Test Interfaces)
# ============================================================================

def pytest_configure(config):
    """
    Register custom pytest markers.

    Markers segregate tests by type (ISP):
    - unit: Unit tests (no external dependencies)
    - integration: Integration tests (requires MCP server)
    - e2e: End-to-end tests (requires MCP + N8N servers)
    - phase1: Documentation tools only (no N8N instance)
    - phase2: Management tools (requires N8N instance)
    - slow: Slow-running tests (can be skipped with -m "not slow")
    """
    config.addinivalue_line("markers", "unit: Unit tests with no external dependencies")
    config.addinivalue_line("markers", "integration: Integration tests requiring MCP server")
    config.addinivalue_line("markers", "e2e: End-to-end tests requiring MCP and N8N servers")
    config.addinivalue_line("markers", "phase1: Phase 1 documentation tools (no N8N instance)")
    config.addinivalue_line("markers", "phase2: Phase 2 management tools (requires N8N instance)")
    config.addinivalue_line("markers", "slow: Slow-running tests")
    config.addinivalue_line("markers", "p1: Priority 1 critical path (80% coverage target)")
    config.addinivalue_line("markers", "p2: Priority 2 common usage (60% coverage target)")
    config.addinivalue_line("markers", "p3: Priority 3 specialized (40% coverage target)")


# ============================================================================
# CLEANUP HOOKS
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_after_test():
    """
    Auto-use fixture for post-test cleanup.

    Scope: function - Runs after every test
    Purpose: Ensure clean state between tests

    Yields:
        None (cleanup happens after yield)
    """
    yield
    # Cleanup code here (if needed)
    # For now, clients are closed by their own fixtures
    pass
