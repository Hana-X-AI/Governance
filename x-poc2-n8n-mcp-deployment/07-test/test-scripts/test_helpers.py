"""
POC-002 test helper utilities.

Shared utility functions for test scripts.
"""

import asyncio
from typing import Dict, Any, List
import httpx


# ============================================================================
# MCP PROTOCOL HELPERS
# ============================================================================

async def call_mcp_tool(
    client: httpx.AsyncClient,
    request_id: int,
    tool_name: str,
    arguments: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """
    Call an MCP tool and return the response.

    Args:
        client: HTTP client
        request_id: JSON-RPC request ID
        tool_name: Name of the MCP tool to call
        arguments: Tool arguments (optional)

    Returns:
        JSON-RPC response data
    """
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": arguments or {}
        }
    }

    response = await client.post("/mcp/call", json=payload)
    return response.json()


async def list_mcp_tools(
    client: httpx.AsyncClient,
    request_id: int
) -> List[Dict[str, Any]]:
    """
    List all available MCP tools.

    Args:
        client: HTTP client
        request_id: JSON-RPC request ID

    Returns:
        List of tool definitions
    """
    payload = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": "tools/list",
        "params": {}
    }

    response = await client.post("/mcp/call", json=payload)
    data = response.json()

    if "result" in data:
        return data["result"].get("tools", [])
    return []


# ============================================================================
# WORKFLOW HELPERS
# ============================================================================

async def create_test_workflow(
    client: httpx.AsyncClient,
    name: str,
    active: bool = False
) -> Dict[str, Any]:
    """
    Create a simple test workflow.

    Args:
        client: HTTP client
        name: Workflow name
        active: Active status

    Returns:
        Created workflow data
    """
    workflow_data = {
        "name": name,
        "active": active,
        "nodes": [
            {
                "id": "start-node",
                "name": "Start",
                "type": "n8n-nodes-base.start",
                "position": [250, 300],
                "parameters": {}
            }
        ],
        "connections": {},
        "settings": {"executionOrder": "v1"}
    }

    response = await client.post("/api/v1/workflows", json=workflow_data)
    return response.json()


async def delete_test_workflow(
    client: httpx.AsyncClient,
    workflow_id: str
) -> bool:
    """
    Delete a test workflow.

    Args:
        client: HTTP client
        workflow_id: Workflow ID to delete

    Returns:
        True if deleted successfully
    """
    try:
        response = await client.delete(f"/api/v1/workflows/{workflow_id}")
        return response.status_code in [200, 204]
    except Exception:
        return False


# ============================================================================
# PROJECT HELPERS
# ============================================================================

async def create_test_project(
    client: httpx.AsyncClient,
    name: str,
    project_type: str = "team"
) -> Dict[str, Any]:
    """
    Create a test project.

    Args:
        client: HTTP client
        name: Project name
        project_type: Project type

    Returns:
        Created project data
    """
    project_data = {
        "name": name,
        "type": project_type
    }

    response = await client.post("/api/v1/projects", json=project_data)
    return response.json()


# ============================================================================
# CREDENTIAL HELPERS
# ============================================================================

async def create_test_credential(
    client: httpx.AsyncClient,
    name: str,
    credential_type: str = "httpBasicAuth",
    data: Dict[str, Any] | None = None
) -> Dict[str, Any]:
    """
    Create a test credential.

    Args:
        client: HTTP client
        name: Credential name
        credential_type: Credential type
        data: Credential data

    Returns:
        Created credential data
    """
    credential_data = {
        "name": name,
        "type": credential_type,
        "data": data or {"user": "test", "password": "test"}
    }

    response = await client.post("/api/v1/credentials", json=credential_data)
    return response.json()


# ============================================================================
# ASSERTION HELPERS
# ============================================================================

def assert_valid_uuid(value: str, field_name: str = "id"):
    """Assert that a value is a valid UUID."""
    import uuid
    try:
        uuid.UUID(str(value))
    except ValueError:
        raise AssertionError(f"{field_name} is not a valid UUID: {value}")


def assert_iso_timestamp(value: str, field_name: str = "timestamp"):
    """Assert that a value is a valid ISO timestamp."""
    from datetime import datetime
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        raise AssertionError(f"{field_name} is not a valid ISO timestamp: {value}")


def assert_http_success(response: httpx.Response):
    """Assert that HTTP response is successful."""
    assert 200 <= response.status_code < 300, \
        f"HTTP request failed with status {response.status_code}: {response.text}"


# ============================================================================
# RETRY HELPERS
# ============================================================================

async def retry_async(
    func,
    max_attempts: int = 3,
    delay: float = 1.0,
    exceptions: tuple = (Exception,)
):
    """
    Retry an async function with exponential backoff.

    Args:
        func: Async function to retry
        max_attempts: Maximum retry attempts
        delay: Initial delay between retries
        exceptions: Exceptions to catch

    Returns:
        Function result
    """
    for attempt in range(max_attempts):
        try:
            return await func()
        except exceptions as e:
            if attempt == max_attempts - 1:
                raise
            await asyncio.sleep(delay * (2 ** attempt))


# ============================================================================
# PERFORMANCE HELPERS
# ============================================================================

import time
from contextlib import asynccontextmanager


@asynccontextmanager
async def measure_time():
    """
    Context manager to measure execution time.

    Usage:
        async with measure_time() as timer:
            # code to measure
        print(f"Execution time: {timer.elapsed}ms")
    """
    class Timer:
        def __init__(self):
            self.start = None
            self.end = None
            self.elapsed = None

    timer = Timer()
    timer.start = time.time()

    try:
        yield timer
    finally:
        timer.end = time.time()
        timer.elapsed = (timer.end - timer.start) * 1000  # Convert to milliseconds


async def measure_concurrent_operations(
    operations: List,
    max_concurrent: int = 10
) -> Dict[str, Any]:
    """
    Execute operations concurrently and measure performance.

    Args:
        operations: List of async functions to execute
        max_concurrent: Maximum concurrent operations

    Returns:
        Performance metrics
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def run_with_semaphore(op):
        async with semaphore:
            start = time.time()
            try:
                result = await op()
                elapsed = (time.time() - start) * 1000
                return {"success": True, "elapsed": elapsed, "result": result}
            except Exception as e:
                elapsed = (time.time() - start) * 1000
                return {"success": False, "elapsed": elapsed, "error": str(e)}

    results = await asyncio.gather(*[run_with_semaphore(op) for op in operations])

    # Calculate metrics
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]
    elapsed_times = [r["elapsed"] for r in results]

    return {
        "total": len(results),
        "successes": len(successes),
        "failures": len(failures),
        "success_rate": len(successes) / len(results) if results else 0,
        "avg_time": sum(elapsed_times) / len(elapsed_times) if elapsed_times else 0,
        "min_time": min(elapsed_times) if elapsed_times else 0,
        "max_time": max(elapsed_times) if elapsed_times else 0,
        "results": results
    }


# ============================================================================
# DATA GENERATION HELPERS
# ============================================================================

def generate_test_id(prefix: str = "test") -> str:
    """Generate a unique test identifier."""
    import uuid
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def generate_test_workflow_name() -> str:
    """Generate a unique test workflow name."""
    return generate_test_id("workflow")


def generate_test_project_name() -> str:
    """Generate a unique test project name."""
    return generate_test_id("project")


def generate_test_credential_name() -> str:
    """Generate a unique test credential name."""
    return generate_test_id("credential")
