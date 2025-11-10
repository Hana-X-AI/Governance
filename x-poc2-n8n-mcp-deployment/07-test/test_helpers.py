"""
N8N MCP Testing Framework - OOP Helper Classes

This module provides object-oriented helper classes following SOLID principles:
- SRP: Each class has a single, well-defined responsibility
- OCP: Classes are designed for extension without modification
- LSP: Implementations are substitutable (e.g., real vs mock clients)
- ISP: Segregated interfaces for different client types
- DIP: High-level classes depend on abstractions, not concrete implementations

Knowledge Sources:
- /srv/knowledge/vault/n8n-mcp-main/tests/utils/test-helpers.ts
- /srv/knowledge/vault/pytest/ (best practices)

Author: Julia Chen, Testing Framework Specialist
Date: 2025-11-06
"""

import httpx
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# ABSTRACT BASE CLASSES (SOLID LSP - Liskov Substitution)
# ============================================================================

class MCPClientInterface(ABC):
    """
    Abstract interface for MCP clients.

    SOLID LSP: All MCP client implementations must be substitutable
    Purpose: Define contract for MCP tool communication
    """

    @abstractmethod
    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call an MCP tool.

        Args:
            tool_name: Name of the tool to call
            parameters: Tool parameters

        Returns:
            Tool response as dictionary
        """
        pass

    @abstractmethod
    def list_tools(self) -> List[str]:
        """
        List available tools.

        Returns:
            List of tool names
        """
        pass


class N8NClientInterface(ABC):
    """
    Abstract interface for N8N API clients.

    SOLID LSP: All N8N client implementations must be substitutable
    Purpose: Define contract for N8N API communication
    """

    @abstractmethod
    def health_check(self) -> bool:
        """
        Check N8N instance health.

        Returns:
            True if healthy, False otherwise
        """
        pass

    @abstractmethod
    def list_workflows(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List workflows.

        Args:
            limit: Maximum workflows to return

        Returns:
            List of workflow metadata
        """
        pass


# ============================================================================
# CONCRETE IMPLEMENTATIONS (SOLID SRP - Single Responsibility)
# ============================================================================

class MCPDocumentationClient(MCPClientInterface):
    """
    Client for N8N MCP documentation tools (Phase 1).

    SOLID SRP: Handles ONLY documentation tool calls
    SOLID LSP: Implements MCPClientInterface
    SOLID DIP: Depends on httpx.Client abstraction

    Phase: 1 - NO N8N instance required
    Tools: 23 documentation tools
    """

    def __init__(self, http_client: httpx.Client):
        """
        Initialize documentation tools client.

        Args:
            http_client: httpx.Client for MCP server communication
        """
        self.http_client = http_client
        self.endpoint = "/mcp/call-tool"

    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a documentation tool.

        Args:
            tool_name: Tool name (must be one of 23 doc tools)
            parameters: Tool parameters

        Returns:
            Tool response dictionary

        Raises:
            httpx.HTTPStatusError: If HTTP request fails
        """
        payload = {
            "tool": tool_name,
            "parameters": parameters
        }
        response = self.http_client.post(self.endpoint, json=payload)
        response.raise_for_status()
        return response.json()

    def list_tools(self) -> List[str]:
        """
        List available documentation tools.

        Returns:
            List of 23 documentation tool names
        """
        response = self.call_tool("tools_documentation", {})
        return response.get("tools", [])

    # Documentation tool convenience methods
    def list_nodes(self, limit: int = 50, category: Optional[str] = None,
                   package: Optional[str] = None) -> Dict[str, Any]:
        """
        Call list_nodes tool.

        Args:
            limit: Maximum nodes to return (default 50)
            category: Filter by category (trigger/transform/output/input/AI)
            package: Filter by package (n8n-nodes-base or @n8n/n8n-nodes-langchain)

        Returns:
            Dict with nodes list and metadata
        """
        params = {"limit": limit}
        if category:
            params["category"] = category
        if package:
            params["package"] = package
        return self.call_tool("list_nodes", params)

    def get_node_essentials(self, node_type: str, include_examples: bool = False) -> Dict[str, Any]:
        """
        Call get_node_essentials tool (fast, <5KB).

        Args:
            node_type: Full node type (e.g., "nodes-base.httpRequest")
            include_examples: Include real-world config examples

        Returns:
            Dict with essential node information
        """
        params = {
            "nodeType": node_type,
            "includeExamples": include_examples
        }
        return self.call_tool("get_node_essentials", params)

    def search_nodes(self, query: str, limit: int = 20, mode: str = "OR",
                     include_examples: bool = False) -> Dict[str, Any]:
        """
        Call search_nodes tool.

        Args:
            query: Search query
            limit: Maximum results (default 20)
            mode: Search mode (OR/AND/FUZZY)
            include_examples: Include config examples

        Returns:
            Dict with search results
        """
        params = {
            "query": query,
            "limit": limit,
            "mode": mode,
            "includeExamples": include_examples
        }
        return self.call_tool("search_nodes", params)

    def validate_node_operation(self, node_type: str, config: Dict[str, Any],
                                 profile: str = "ai-friendly") -> Dict[str, Any]:
        """
        Call validate_node_operation tool.

        Args:
            node_type: Full node type
            config: Node configuration to validate
            profile: Validation profile (minimal/runtime/ai-friendly/strict)

        Returns:
            Dict with validation results (valid, errors, warnings, suggestions)
        """
        params = {
            "nodeType": node_type,
            "config": config,
            "profile": profile
        }
        return self.call_tool("validate_node_operation", params)

    def get_database_statistics(self) -> Dict[str, Any]:
        """
        Call get_database_statistics tool.

        Returns:
            Dict with node database statistics (total, AI tools, triggers, coverage)
        """
        return self.call_tool("get_database_statistics", {})

    def validate_workflow(self, workflow: Dict[str, Any],
                          validate_nodes: bool = True,
                          validate_connections: bool = True,
                          validate_expressions: bool = True,
                          profile: str = "runtime") -> Dict[str, Any]:
        """
        Call validate_workflow tool.

        Args:
            workflow: Complete workflow JSON
            validate_nodes: Validate node configurations
            validate_connections: Validate workflow connections
            validate_expressions: Validate n8n expressions
            profile: Validation profile

        Returns:
            Dict with validation results
        """
        params = {
            "workflow": workflow,
            "options": {
                "validateNodes": validate_nodes,
                "validateConnections": validate_connections,
                "validateExpressions": validate_expressions,
                "profile": profile
            }
        }
        return self.call_tool("validate_workflow", params)


class MCPManagementClient(MCPClientInterface):
    """
    Client for N8N MCP management tools (Phase 2).

    SOLID SRP: Handles ONLY management tool calls
    SOLID LSP: Implements MCPClientInterface
    SOLID DIP: Depends on httpx.Client abstraction

    Phase: 2 - REQUIRES N8N instance with API key
    Tools: 21 management tools
    """

    def __init__(self, http_client: httpx.Client):
        """
        Initialize management tools client.

        Args:
            http_client: httpx.Client for MCP server communication
        """
        self.http_client = http_client
        self.endpoint = "/mcp/call-tool"

    def call_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call a management tool.

        Args:
            tool_name: Tool name (must be one of 21 mgmt tools)
            parameters: Tool parameters

        Returns:
            Tool response dictionary

        Raises:
            httpx.HTTPStatusError: If HTTP request fails
        """
        payload = {
            "tool": tool_name,
            "parameters": parameters
        }
        response = self.http_client.post(self.endpoint, json=payload)
        response.raise_for_status()
        return response.json()

    def list_tools(self) -> List[str]:
        """
        List available management tools.

        Returns:
            List of 21 management tool names
        """
        response = self.call_tool("n8n_list_available_tools", {})
        return response.get("tools", [])

    # Management tool convenience methods
    def create_workflow(self, name: str, nodes: List[Dict], connections: Dict,
                        settings: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Call n8n_create_workflow tool.

        Args:
            name: Workflow name
            nodes: List of workflow nodes
            connections: Workflow connections object
            settings: Optional workflow settings

        Returns:
            Dict with created workflow (includes ID)
        """
        params = {
            "name": name,
            "nodes": nodes,
            "connections": connections
        }
        if settings:
            params["settings"] = settings
        return self.call_tool("n8n_create_workflow", params)

    def get_workflow(self, workflow_id: str, mode: str = "full") -> Dict[str, Any]:
        """
        Call n8n_get_workflow tool (or variants).

        Args:
            workflow_id: Workflow ID
            mode: Retrieval mode (full/details/structure/minimal)

        Returns:
            Dict with workflow data
        """
        tool_map = {
            "full": "n8n_get_workflow",
            "details": "n8n_get_workflow_details",
            "structure": "n8n_get_workflow_structure",
            "minimal": "n8n_get_workflow_minimal"
        }
        tool_name = tool_map.get(mode, "n8n_get_workflow")
        return self.call_tool(tool_name, {"id": workflow_id})

    def list_workflows(self, limit: int = 100, cursor: Optional[str] = None,
                       active: Optional[bool] = None) -> Dict[str, Any]:
        """
        Call n8n_list_workflows tool.

        Args:
            limit: Maximum workflows to return (1-100)
            cursor: Pagination cursor
            active: Filter by active status

        Returns:
            Dict with workflows and pagination info
        """
        params = {"limit": limit}
        if cursor:
            params["cursor"] = cursor
        if active is not None:
            params["active"] = active
        return self.call_tool("n8n_list_workflows", params)

    def update_workflow(self, workflow_id: str, updates: Dict[str, Any],
                        mode: str = "full") -> Dict[str, Any]:
        """
        Call n8n_update_full_workflow or n8n_update_partial_workflow.

        Args:
            workflow_id: Workflow ID to update
            updates: Update payload
            mode: Update mode (full/partial)

        Returns:
            Dict with updated workflow
        """
        if mode == "partial":
            return self.call_tool("n8n_update_partial_workflow", {
                "id": workflow_id,
                "operations": updates.get("operations", [])
            })
        else:
            params = {"id": workflow_id, **updates}
            return self.call_tool("n8n_update_full_workflow", params)

    def delete_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Call n8n_delete_workflow tool.

        Args:
            workflow_id: Workflow ID to delete

        Returns:
            Dict with deletion confirmation
        """
        return self.call_tool("n8n_delete_workflow", {"id": workflow_id})

    def health_check(self) -> Dict[str, Any]:
        """
        Call n8n_health_check tool.

        Returns:
            Dict with health status and features
        """
        return self.call_tool("n8n_health_check", {})

    def diagnostic(self, verbose: bool = False) -> Dict[str, Any]:
        """
        Call n8n_diagnostic tool.

        Args:
            verbose: Include detailed debug information

        Returns:
            Dict with diagnostic information
        """
        return self.call_tool("n8n_diagnostic", {"verbose": verbose})


class N8NAPIClient(N8NClientInterface):
    """
    Direct N8N API client (for comparison/validation).

    SOLID SRP: Handles ONLY direct N8N API calls
    SOLID LSP: Implements N8NClientInterface
    SOLID DIP: Depends on httpx.Client abstraction

    Purpose: Verify MCP tool outputs match N8N API directly
    """

    def __init__(self, http_client: httpx.Client):
        """
        Initialize N8N API client.

        Args:
            http_client: httpx.Client configured with N8N API base URL and auth
        """
        self.http_client = http_client

    def health_check(self) -> bool:
        """
        Check N8N instance health via /healthz.

        Returns:
            True if healthy, False otherwise
        """
        try:
            response = self.http_client.get("/healthz", timeout=5.0)
            return response.status_code == 200
        except Exception:
            return False

    def list_workflows(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List workflows via N8N API.

        Args:
            limit: Maximum workflows to return

        Returns:
            List of workflow metadata
        """
        response = self.http_client.get("/api/v1/workflows", params={"limit": limit})
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])

    def get_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """
        Get workflow by ID via N8N API.

        Args:
            workflow_id: Workflow ID

        Returns:
            Workflow data
        """
        response = self.http_client.get(f"/api/v1/workflows/{workflow_id}")
        response.raise_for_status()
        return response.json()


# ============================================================================
# ASSERTION HELPERS (SOLID SRP - Single Responsibility)
# ============================================================================

class ToolResponseValidator:
    """
    Validator for MCP tool responses.

    SOLID SRP: Handles ONLY tool response validation
    Purpose: Consistent validation of tool outputs
    """

    @staticmethod
    def assert_success(response: Dict[str, Any]) -> None:
        """
        Assert tool call was successful.

        Args:
            response: Tool response dictionary

        Raises:
            AssertionError: If response indicates error
        """
        assert isinstance(response, dict), f"Expected dict, got {type(response)}"
        assert "error" not in response or response["error"] is None, \
            f"Tool returned error: {response.get('error')}"

    @staticmethod
    def assert_has_keys(response: Dict[str, Any], keys: List[str]) -> None:
        """
        Assert response contains expected keys.

        Args:
            response: Tool response dictionary
            keys: List of required keys

        Raises:
            AssertionError: If any key is missing
        """
        for key in keys:
            assert key in response, f"Response missing key: {key}"

    @staticmethod
    def assert_node_response(response: Dict[str, Any]) -> None:
        """
        Assert response is a valid node response.

        Args:
            response: Tool response dictionary

        Raises:
            AssertionError: If response is invalid
        """
        ToolResponseValidator.assert_success(response)
        assert "nodes" in response or "node" in response, \
            "Response must contain 'nodes' or 'node'"

    @staticmethod
    def assert_workflow_response(response: Dict[str, Any]) -> None:
        """
        Assert response is a valid workflow response.

        Args:
            response: Tool response dictionary

        Raises:
            AssertionError: If response is invalid
        """
        ToolResponseValidator.assert_success(response)
        required_keys = ["name", "nodes", "connections"]
        for key in required_keys:
            assert key in response, f"Workflow response missing key: {key}"


class DatabaseValidator:
    """
    Validator for N8N MCP database state.

    SOLID SRP: Handles ONLY database validation
    Purpose: Verify database meets expected standards
    """

    def __init__(self, client: MCPDocumentationClient):
        """
        Initialize database validator.

        Args:
            client: MCPDocumentationClient for database queries
        """
        self.client = client

    def validate_node_count(self, expected: int = 536) -> bool:
        """
        Validate total node count.

        Args:
            expected: Expected node count (default 536)

        Returns:
            True if count matches, False otherwise
        """
        stats = self.client.get_database_statistics()
        actual = stats.get("total_nodes", 0)
        return actual == expected

    def validate_ai_tools_count(self, expected: int = 263) -> bool:
        """
        Validate AI-optimized node count.

        Args:
            expected: Expected AI tools count (default 263)

        Returns:
            True if count matches, False otherwise
        """
        stats = self.client.get_database_statistics()
        actual = stats.get("ai_tools", 0)
        return actual == expected

    def validate_trigger_count(self, expected: int = 104) -> bool:
        """
        Validate trigger node count.

        Args:
            expected: Expected trigger count (default 104)

        Returns:
            True if count matches, False otherwise
        """
        stats = self.client.get_database_statistics()
        actual = stats.get("trigger_nodes", 0)
        return actual == expected

    def validate_doc_coverage(self, expected_percent: float = 87.0) -> bool:
        """
        Validate documentation coverage percentage.

        Args:
            expected_percent: Expected coverage (default 87.0)

        Returns:
            True if coverage meets or exceeds expected, False otherwise
        """
        stats = self.client.get_database_statistics()
        actual = stats.get("doc_coverage_percent", 0.0)
        return actual >= expected_percent


# ============================================================================
# TEST DATA BUILDERS (SOLID SRP - Single Responsibility)
# ============================================================================

class WorkflowBuilder:
    """
    Builder for test workflows.

    SOLID SRP: Handles ONLY workflow construction
    Purpose: Fluent API for creating test workflows
    """

    def __init__(self, name: str = "Test Workflow"):
        """
        Initialize workflow builder.

        Args:
            name: Workflow name
        """
        self.workflow = {
            "name": name,
            "nodes": [],
            "connections": {}
        }
        self.node_counter = 0

    def add_webhook_node(self, path: str = "test", method: str = "GET") -> "WorkflowBuilder":
        """
        Add webhook trigger node.

        Args:
            path: Webhook path
            method: HTTP method

        Returns:
            Self for chaining
        """
        node_id = f"webhook-{self.node_counter}"
        self.workflow["nodes"].append({
            "id": node_id,
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 1,
            "position": [250, 300 + (self.node_counter * 100)],
            "parameters": {
                "path": path,
                "httpMethod": method,
                "responseMode": "onReceived"
            }
        })
        self.node_counter += 1
        return self

    def add_http_request_node(self, url: str, method: str = "GET") -> "WorkflowBuilder":
        """
        Add HTTP request node.

        Args:
            url: Request URL
            method: HTTP method

        Returns:
            Self for chaining
        """
        node_id = f"http-{self.node_counter}"
        self.workflow["nodes"].append({
            "id": node_id,
            "name": "HTTP Request",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 3,
            "position": [450, 300 + (self.node_counter * 100)],
            "parameters": {
                "url": url,
                "method": method
            }
        })
        self.node_counter += 1
        return self

    def connect_nodes(self, from_name: str, to_name: str) -> "WorkflowBuilder":
        """
        Connect two nodes.

        Args:
            from_name: Source node name
            to_name: Target node name

        Returns:
            Self for chaining
        """
        if from_name not in self.workflow["connections"]:
            self.workflow["connections"][from_name] = {"main": [[]]}

        self.workflow["connections"][from_name]["main"][0].append({
            "node": to_name,
            "type": "main",
            "index": 0
        })
        return self

    def build(self) -> Dict[str, Any]:
        """
        Build final workflow.

        Returns:
            Complete workflow dictionary
        """
        return self.workflow


# ============================================================================
# ASYNC HELPERS (For async testing)
# ============================================================================

async def wait_for_condition(condition_func, timeout: float = 5.0, interval: float = 0.1) -> bool:
    """
    Wait for a condition to become true.

    Args:
        condition_func: Callable returning bool (can be sync or async)
        timeout: Maximum wait time in seconds
        interval: Check interval in seconds

    Returns:
        True if condition met, False if timeout

    Example:
        await wait_for_condition(lambda: client.health_check(), timeout=10.0)
    """
    elapsed = 0.0
    while elapsed < timeout:
        try:
            result = condition_func()
            if asyncio.iscoroutine(result):
                result = await result
            if result:
                return True
        except Exception:
            pass
        await asyncio.sleep(interval)
        elapsed += interval
    return False
