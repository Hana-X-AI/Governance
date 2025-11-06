# N8N MCP Testing Framework - Documentation Tools Test Cases

**Project:** POC-002 N8N MCP Deployment
**Phase:** Phase 1 - Documentation Tools (23 tools)
**Author:** Julia Chen, Testing Framework Specialist
**Date:** 2025-11-06
**Status:** READY FOR IMPLEMENTATION

---

## Executive Summary

This document defines comprehensive test cases for all **23 documentation tools** in Phase 1 of the N8N MCP deployment. These tools operate on the local node database and template library, requiring NO N8N instance. All test cases follow **SOLID OOP principles** and utilize the test framework defined in `conftest.py` and `test_helpers.py`.

### Phase 1 Overview

- **Total Tools:** 23 documentation tools
- **N8N Instance:** NOT REQUIRED
- **Test File:** `test_documentation_tools.py`
- **OOP Client:** `MCPDocumentationClient` (from `test_helpers.py`)
- **Fixtures:** From `conftest.py` (http_client, doc_tools_list, priority_tools)
- **Database:** 536 nodes, 263 AI tools, 104 triggers, 87% doc coverage
- **Templates:** 2,500+ templates, 2,646+ configurations

---

## 1. Tool Documentation & Statistics (2 tools)

### 1.1 TC-DOC-001: tools_documentation

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate retrieval of MCP tools documentation

**Test Class:** `TestToolDocumentation` (SOLID SRP)

**Preconditions:**
- MCP server running (192.168.10.214:3000)
- All 23 documentation tools registered

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestToolDocumentation:
    """Test MCP tools documentation - SOLID SRP"""

    def test_tools_documentation_retrieval(self, http_client):
        """Retrieve documentation for all MCP tools"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("tools_documentation", {})

        # Validate response structure
        validator = ToolResponseValidator()
        validator.assert_success(result)
        validator.assert_has_keys(result, ["tools"])

        # Validate tool count
        assert len(result["tools"]) == 23, "Expected 23 documentation tools"

    def test_tools_documentation_structure(self, http_client, doc_tools_list):
        """Validate tool documentation structure"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("tools_documentation", {})

        # Each tool should have required fields
        for tool in result["tools"]:
            assert "name" in tool
            assert "description" in tool
            assert "parameters" in tool

        # Verify all expected tools are present
        tool_names = [t["name"] for t in result["tools"]]
        for expected_tool in doc_tools_list:
            assert expected_tool in tool_names
```

**Expected Results:**
- Response contains 23 tool definitions
- Each tool has name, description, parameters
- All tools from `doc_tools_list` fixture present

---

### 1.2 TC-DOC-002: get_database_statistics

**Priority:** P1 (Critical Path)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p1`

**Objective:** Validate node database statistics and health check

**Test Class:** `TestToolDocumentation` (SOLID SRP)

**Preconditions:**
- Node database loaded with 536 nodes
- 263 AI-optimized nodes present
- 104 trigger nodes present
- 87% documentation coverage achieved

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p1
class TestToolDocumentation:
    """Test database statistics - SOLID SRP"""

    def test_database_statistics_validation(self, http_client, test_database_config):
        """Validate database statistics match expected values"""
        client = MCPDocumentationClient(http_client)
        validator = DatabaseValidator(client)

        # Validate all database metrics
        assert validator.validate_node_count(test_database_config.total_nodes)
        assert validator.validate_ai_tools_count(test_database_config.ai_optimized_nodes)
        assert validator.validate_trigger_count(test_database_config.trigger_nodes)
        assert validator.validate_doc_coverage(test_database_config.doc_coverage_percent)

    def test_database_statistics_response(self, http_client):
        """Validate database statistics response structure"""
        client = MCPDocumentationClient(http_client)
        result = client.get_database_statistics()

        # Validate response keys
        validator = ToolResponseValidator()
        validator.assert_success(result)
        validator.assert_has_keys(result, [
            "total_nodes",
            "ai_optimized_nodes",
            "trigger_nodes",
            "doc_coverage_percent",
            "packages"
        ])

        # Validate value types
        assert isinstance(result["total_nodes"], int)
        assert isinstance(result["ai_optimized_nodes"], int)
        assert isinstance(result["trigger_nodes"], int)
        assert isinstance(result["doc_coverage_percent"], (int, float))
```

**Expected Results:**
- Total nodes = 536
- AI-optimized nodes = 263
- Trigger nodes = 104
- Documentation coverage >= 87%
- Response includes package breakdown

---

## 2. Node Queries (5 tools)

### 2.1 TC-DOC-003: list_nodes

**Priority:** P1 (Critical Path)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p1`

**Objective:** Validate node listing with filters and pagination

**Test Class:** `TestNodeQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p1
class TestNodeQueries:
    """Test node query tools - SOLID SRP"""

    def test_list_nodes_basic(self, http_client):
        """List nodes with default parameters"""
        client = MCPDocumentationClient(http_client)
        result = client.list_nodes(limit=10)

        validator = ToolResponseValidator()
        validator.assert_success(result)
        assert "nodes" in result
        assert len(result["nodes"]) <= 10

    def test_list_nodes_by_category(self, http_client):
        """Filter nodes by category"""
        client = MCPDocumentationClient(http_client)
        result = client.list_nodes(category="trigger", limit=200)

        assert all(node["category"] == "trigger" for node in result["nodes"])

    def test_list_nodes_by_package(self, http_client):
        """Filter nodes by package"""
        client = MCPDocumentationClient(http_client)
        result = client.list_nodes(package="n8n-nodes-base", limit=50)

        assert all("n8n-nodes-base" in node["package"] for node in result["nodes"])

    @pytest.mark.parametrize("limit", [1, 10, 50, 100])
    def test_list_nodes_pagination(self, http_client, limit):
        """Test pagination with various limits"""
        client = MCPDocumentationClient(http_client)
        result = client.list_nodes(limit=limit)

        assert len(result["nodes"]) <= limit
```

**Expected Results:**
- Default limit respected
- Category filter works correctly
- Package filter works correctly
- Pagination limits enforced

---

### 2.2 TC-DOC-004: get_node_essentials

**Priority:** P1 (Critical Path)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p1`

**Objective:** Validate fast, optimized node information retrieval (<5KB, <2s)

**Test Class:** `TestNodeQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p1
class TestNodeQueries:
    """Test node essentials retrieval - SOLID SRP"""

    def test_get_node_essentials_basic(self, http_client, sample_node_types):
        """Retrieve essentials for common node types"""
        client = MCPDocumentationClient(http_client)

        for node_type in sample_node_types:
            result = client.get_node_essentials(node_type)

            validator = ToolResponseValidator()
            validator.assert_success(result)
            assert "node" in result
            assert result["node"]["type"] == node_type

    def test_get_node_essentials_with_examples(self, http_client):
        """Retrieve essentials with configuration examples"""
        client = MCPDocumentationClient(http_client)
        result = client.get_node_essentials(
            "nodes-base.httpRequest",
            include_examples=True
        )

        assert "examples" in result["node"]
        assert len(result["node"]["examples"]) > 0

    def test_get_node_essentials_performance(self, http_client):
        """Validate response time < 2s"""
        import time
        client = MCPDocumentationClient(http_client)

        start = time.time()
        client.get_node_essentials("nodes-base.webhook")
        elapsed = time.time() - start

        assert elapsed < 2.0, f"Essentials took {elapsed}s (expected < 2s)"
```

**Expected Results:**
- Response < 5KB
- Response time < 2s
- Node type matches request
- Examples included when requested

---

### 2.3 TC-DOC-005: search_nodes

**Priority:** P1 (Critical Path)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p1`

**Objective:** Validate node search with multiple modes (OR/AND/FUZZY)

**Test Class:** `TestNodeQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p1
class TestNodeQueries:
    """Test node search functionality - SOLID SRP"""

    def test_search_nodes_or_mode(self, http_client):
        """Search nodes with OR mode (any keyword)"""
        client = MCPDocumentationClient(http_client)
        result = client.search_nodes("http webhook", mode="OR", limit=20)

        assert len(result["nodes"]) > 0
        # Results should contain http OR webhook
        assert any("http" in n["name"].lower() or "webhook" in n["name"].lower()
                   for n in result["nodes"])

    def test_search_nodes_and_mode(self, http_client):
        """Search nodes with AND mode (all keywords)"""
        client = MCPDocumentationClient(http_client)
        result = client.search_nodes("google sheets", mode="AND", limit=20)

        # Results should contain google AND sheets
        for node in result["nodes"]:
            name_desc = (node["name"] + " " + node.get("description", "")).lower()
            assert "google" in name_desc and "sheets" in name_desc

    def test_search_nodes_fuzzy_mode(self, http_client):
        """Search nodes with FUZZY mode (approximate matching)"""
        client = MCPDocumentationClient(http_client)
        result = client.search_nodes("webhok", mode="FUZZY", limit=10)

        # Should find "webhook" despite typo
        assert len(result["nodes"]) > 0

    @pytest.mark.parametrize("query,expected_count", [
        ("http", 10),
        ("slack", 5),
        ("database", 15)
    ])
    def test_search_nodes_common_queries(self, http_client, query, expected_count):
        """Test common search queries"""
        client = MCPDocumentationClient(http_client)
        result = client.search_nodes(query, limit=20)

        assert len(result["nodes"]) >= expected_count
```

**Expected Results:**
- OR mode returns any keyword match
- AND mode requires all keywords
- FUZZY mode handles typos
- Common queries return expected results

---

### 2.4 TC-DOC-006: get_node_info

**Priority:** P2 (Common Usage)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p2`

**Objective:** Validate full node documentation retrieval (100KB+)

**Test Class:** `TestNodeDocumentation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p2
class TestNodeDocumentation:
    """Test full node documentation - SOLID SRP"""

    def test_get_node_info_complete(self, http_client, sample_node_types):
        """Retrieve complete node information"""
        client = MCPDocumentationClient(http_client)

        for node_type in sample_node_types:
            result = client.call_tool("get_node_info", {"nodeType": node_type})

            validator = ToolResponseValidator()
            validator.assert_node_response(result)

            node = result["node"]
            assert "type" in node
            assert "properties" in node
            assert "description" in node

    def test_get_node_info_properties(self, http_client):
        """Validate node properties structure"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_node_info", {
            "nodeType": "nodes-base.httpRequest"
        })

        properties = result["node"]["properties"]
        assert isinstance(properties, list)
        assert len(properties) > 0

        # Each property should have required fields
        for prop in properties:
            assert "name" in prop
            assert "type" in prop
```

**Expected Results:**
- Complete node information returned
- Properties list is comprehensive
- Documentation is detailed (100KB+ response)

---

### 2.5 TC-DOC-007: list_ai_tools

**Priority:** P2 (Common Usage)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p2`

**Objective:** Validate AI-optimized nodes listing (263 tools)

**Test Class:** `TestNodeQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p2
class TestNodeQueries:
    """Test AI tools listing - SOLID SRP"""

    def test_list_ai_tools_count(self, http_client, test_database_config):
        """Validate AI tools count"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("list_ai_tools", {"limit": 300})

        assert len(result["nodes"]) == test_database_config.ai_optimized_nodes

    def test_list_ai_tools_optimization(self, http_client):
        """Verify all returned nodes are AI-optimized"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("list_ai_tools", {"limit": 50})

        for node in result["nodes"]:
            assert node.get("ai_optimized", False) is True
```

**Expected Results:**
- Returns 263 AI-optimized nodes
- All nodes marked as AI-optimized
- Fast retrieval

---

## 3. Node Validation (4 tools)

### 3.1 TC-DOC-008: validate_node_operation

**Priority:** P1 (Critical Path)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p1`

**Objective:** Validate node configuration validation with multiple profiles

**Test Class:** `TestNodeValidation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p1
class TestNodeValidation:
    """Test node validation tools - SOLID SRP"""

    def test_validate_node_operation_valid_config(self, http_client):
        """Validate correct node configuration"""
        client = MCPDocumentationClient(http_client)
        config = {
            "parameters": {
                "url": "https://api.example.com",
                "method": "GET"
            }
        }

        result = client.validate_node_operation(
            "nodes-base.httpRequest",
            config,
            profile="ai-friendly"
        )

        assert result["valid"] is True
        assert len(result.get("errors", [])) == 0

    def test_validate_node_operation_invalid_config(self, http_client):
        """Validate detection of invalid configuration"""
        client = MCPDocumentationClient(http_client)
        config = {
            "parameters": {}  # Missing required fields
        }

        result = client.validate_node_operation(
            "nodes-base.httpRequest",
            config,
            profile="strict"
        )

        assert result["valid"] is False
        assert len(result["errors"]) > 0

    @pytest.mark.parametrize("profile", ["minimal", "runtime", "ai-friendly", "strict"])
    def test_validate_node_operation_profiles(self, http_client, profile):
        """Test validation with different profiles"""
        client = MCPDocumentationClient(http_client)
        config = {"parameters": {"url": "https://example.com", "method": "GET"}}

        result = client.validate_node_operation(
            "nodes-base.httpRequest",
            config,
            profile=profile
        )

        assert "valid" in result
        assert "profile" in result
        assert result["profile"] == profile
```

**Expected Results:**
- Valid configs pass validation
- Invalid configs are rejected
- All profiles work correctly
- Errors are descriptive

---

### 3.2 TC-DOC-009: validate_node_minimal

**Priority:** P2 (Common Usage)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p2`

**Objective:** Validate minimal node configuration checking

**Test Class:** `TestNodeValidation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p2
class TestNodeValidation:
    """Test minimal node validation - SOLID SRP"""

    def test_validate_node_minimal_required_fields(self, http_client):
        """Validate required fields check only"""
        client = MCPDocumentationClient(http_client)
        config = {"parameters": {"path": "/test"}}

        result = client.call_tool("validate_node_minimal", {
            "nodeType": "nodes-base.webhook",
            "config": config
        })

        assert "valid" in result
        assert result["valid"] is True

    def test_validate_node_minimal_missing_required(self, http_client):
        """Detect missing required fields"""
        client = MCPDocumentationClient(http_client)
        config = {"parameters": {}}

        result = client.call_tool("validate_node_minimal", {
            "nodeType": "nodes-base.webhook",
            "config": config
        })

        assert result["valid"] is False
        assert "errors" in result
```

**Expected Results:**
- Checks required fields only
- Faster than full validation
- Returns clear error messages

---

### 3.3 TC-DOC-010: get_property_dependencies

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate property dependency and visibility rules

**Test Class:** `TestNodeValidation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestNodeValidation:
    """Test property dependencies - SOLID SRP"""

    def test_get_property_dependencies_conditional(self, http_client):
        """Retrieve conditional property dependencies"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_property_dependencies", {
            "nodeType": "nodes-base.httpRequest",
            "propertyName": "authentication"
        })

        assert "dependencies" in result
        assert isinstance(result["dependencies"], list)

    def test_get_property_dependencies_visibility(self, http_client):
        """Validate visibility rules for properties"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_property_dependencies", {
            "nodeType": "nodes-base.webhook",
            "propertyName": "responseMode"
        })

        assert "visibility_rules" in result
```

**Expected Results:**
- Returns dependency tree
- Visibility rules documented
- Conditional logic explained

---

### 3.4 TC-DOC-011: get_node_as_tool_info

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate node-as-tool usage information for AI agents

**Test Class:** `TestNodeValidation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestNodeValidation:
    """Test node-as-tool information - SOLID SRP"""

    def test_get_node_as_tool_info_ai_friendly(self, http_client):
        """Retrieve AI-friendly tool usage information"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_node_as_tool_info", {
            "nodeType": "nodes-base.httpRequest"
        })

        assert "tool_description" in result
        assert "parameters" in result
        assert "examples" in result

    def test_get_node_as_tool_info_llm_context(self, http_client):
        """Validate LLM-optimized context"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_node_as_tool_info", {
            "nodeType": "nodes-langchain.agent"
        })

        assert "llm_context" in result
        assert len(result["llm_context"]) > 0
```

**Expected Results:**
- AI-friendly descriptions
- LLM-optimized context
- Usage examples provided

---

## 4. Template System (7 tools)

### 4.1 TC-DOC-012: list_templates

**Priority:** P2 (Common Usage)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p2`

**Objective:** Validate template listing with pagination (2,500+ templates)

**Test Class:** `TestTemplateQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p2
class TestTemplateQueries:
    """Test template discovery - SOLID SRP"""

    def test_list_templates_count(self, http_client, test_database_config):
        """Validate minimum template count"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("list_templates", {"limit": 3000})

        assert len(result["templates"]) >= test_database_config.min_templates

    def test_list_templates_pagination(self, http_client):
        """Test template pagination"""
        client = MCPDocumentationClient(http_client)

        page1 = client.call_tool("list_templates", {"limit": 100, "offset": 0})
        page2 = client.call_tool("list_templates", {"limit": 100, "offset": 100})

        # Pages should have different templates
        page1_ids = [t["id"] for t in page1["templates"]]
        page2_ids = [t["id"] for t in page2["templates"]]
        assert len(set(page1_ids) & set(page2_ids)) == 0

    def test_list_templates_metadata(self, http_client):
        """Validate template metadata structure"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("list_templates", {"limit": 10})

        for template in result["templates"]:
            assert "id" in template
            assert "name" in template
            assert "description" in template
```

**Expected Results:**
- Returns 2,500+ templates
- Pagination works correctly
- Metadata is complete

---

### 4.2 TC-DOC-013: get_template

**Priority:** P2 (Common Usage)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p2`

**Objective:** Validate template retrieval with multiple modes

**Test Class:** `TestTemplateQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p2
class TestTemplateQueries:
    """Test template retrieval - SOLID SRP"""

    @pytest.mark.parametrize("mode", ["nodes_only", "structure", "full"])
    def test_get_template_modes(self, http_client, mode):
        """Test template retrieval modes"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_template", {
            "templateId": "1",
            "mode": mode
        })

        assert "template" in result
        assert "nodes" in result["template"]

        if mode == "full":
            assert "metadata" in result["template"]
            assert "description" in result["template"]

    def test_get_template_invalid_id(self, http_client):
        """Handle invalid template ID"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_template", {
            "templateId": "999999",
            "mode": "nodes_only"
        })

        assert "error" in result or result.get("template") is None
```

**Expected Results:**
- All modes work correctly
- Invalid IDs handled gracefully
- Response size varies by mode

---

### 4.3 TC-DOC-014: search_templates

**Priority:** P2 (Common Usage)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p2`

**Objective:** Validate template keyword search

**Test Class:** `TestTemplateQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p2
class TestTemplateQueries:
    """Test template search - SOLID SRP"""

    def test_search_templates_keyword(self, http_client):
        """Search templates by keyword"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("search_templates", {
            "query": "slack notification"
        })

        assert len(result["templates"]) > 0
        # Results should be relevant to query
        for template in result["templates"]:
            name_desc = (template["name"] + " " + template["description"]).lower()
            assert "slack" in name_desc or "notification" in name_desc

    def test_search_templates_empty_query(self, http_client):
        """Handle empty search query"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("search_templates", {"query": ""})

        # Should return all templates (or reasonable subset)
        assert len(result["templates"]) > 0
```

**Expected Results:**
- Keyword search works correctly
- Results are relevance-ranked
- Empty query handled gracefully

---

### 4.4 TC-DOC-015: list_node_templates

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate templates filtered by node usage

**Test Class:** `TestTemplateQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestTemplateQueries:
    """Test node-based template filtering - SOLID SRP"""

    def test_list_node_templates_webhook(self, http_client):
        """Find templates using webhook node"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("list_node_templates", {
            "nodeType": "nodes-base.webhook"
        })

        assert len(result["templates"]) > 0
        # Verify all templates use the webhook node
        for template in result["templates"]:
            assert "nodes" in template
            node_types = [n["type"] for n in template["nodes"]]
            assert "n8n-nodes-base.webhook" in node_types

    def test_list_node_templates_langchain(self, http_client):
        """Find templates using LangChain nodes"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("list_node_templates", {
            "nodeType": "nodes-langchain.agent"
        })

        assert len(result["templates"]) > 0
```

**Expected Results:**
- Returns templates using specified node
- Node type verification passes
- Multiple node filters supported

---

### 4.5 TC-DOC-016: get_templates_for_task

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate curated template recommendations by task

**Test Class:** `TestTemplateQueries` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestTemplateQueries:
    """Test task-based template recommendations - SOLID SRP"""

    @pytest.mark.parametrize("task_type", [
        "data_transformation",
        "api_integration",
        "notification",
        "ai_workflow"
    ])
    def test_get_templates_for_task_types(self, http_client, task_type):
        """Test curated templates for common tasks"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_templates_for_task", {
            "task": task_type
        })

        assert len(result["templates"]) > 0
        assert "task" in result
        assert result["task"] == task_type
```

**Expected Results:**
- Curated templates returned by task
- Common tasks have templates
- Task metadata included

---

### 4.6 TC-DOC-017: search_templates_by_metadata

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate AI-generated metadata search

**Test Class:** `TestTemplateMetadata` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestTemplateMetadata:
    """Test template metadata search - SOLID SRP"""

    def test_search_templates_by_metadata_ai_tags(self, http_client):
        """Search templates by AI-generated tags"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("search_templates_by_metadata", {
            "query": "data transformation"
        })

        assert len(result["templates"]) > 0
        # Verify metadata is present
        for template in result["templates"]:
            assert "metadata" in template

    def test_search_templates_by_metadata_categories(self, http_client):
        """Search templates by categories"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("search_templates_by_metadata", {
            "query": "integration"
        })

        assert len(result["templates"]) > 0
```

**Expected Results:**
- AI-generated metadata searched
- Semantic search works
- Categories included

---

### 4.7 TC-DOC-018: list_tasks

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate task template categories

**Test Class:** `TestTemplateMetadata` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestTemplateMetadata:
    """Test task categories - SOLID SRP"""

    def test_list_tasks_categories(self, http_client):
        """List available task categories"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("list_tasks", {})

        assert "tasks" in result
        assert len(result["tasks"]) > 0

        # Each task should have metadata
        for task in result["tasks"]:
            assert "name" in task
            assert "description" in task
            assert "template_count" in task
```

**Expected Results:**
- Returns task categories
- Template counts included
- Descriptions provided

---

## 5. Workflow Validation (3 tools)

### 5.1 TC-DOC-019: validate_workflow

**Priority:** P2 (Common Usage)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p2`

**Objective:** Validate complete workflow validation (nodes + connections + expressions)

**Test Class:** `TestWorkflowValidation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p2
class TestWorkflowValidation:
    """Test workflow validation tools - SOLID SRP"""

    def test_validate_workflow_complete_valid(self, http_client, sample_workflow):
        """Validate correct workflow"""
        client = MCPDocumentationClient(http_client)
        result = client.validate_workflow(sample_workflow)

        assert result["valid"] is True
        assert len(result.get("errors", [])) == 0

    def test_validate_workflow_invalid_connections(self, http_client):
        """Detect invalid workflow connections"""
        client = MCPDocumentationClient(http_client)
        invalid_workflow = {
            "name": "Invalid Workflow",
            "nodes": [
                {"id": "1", "name": "Node1", "type": "n8n-nodes-base.webhook"},
                {"id": "2", "name": "Node2", "type": "n8n-nodes-base.httpRequest"}
            ],
            "connections": {
                "Node1": {
                    "main": [[{"node": "NonExistentNode", "type": "main", "index": 0}]]
                }
            }
        }

        result = client.validate_workflow(invalid_workflow)

        assert result["valid"] is False
        assert len(result["errors"]) > 0
        assert any("connection" in err.lower() for err in result["errors"])

    def test_validate_workflow_options(self, http_client, sample_workflow):
        """Test validation with specific options"""
        client = MCPDocumentationClient(http_client)
        result = client.validate_workflow(
            sample_workflow,
            validate_nodes=True,
            validate_connections=True,
            validate_expressions=False,
            profile="runtime"
        )

        assert "valid" in result
        assert "options" in result
        assert result["options"]["validate_expressions"] is False
```

**Expected Results:**
- Valid workflows pass
- Invalid workflows rejected
- Errors are detailed
- Validation options work

---

### 5.2 TC-DOC-020: validate_workflow_connections

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate workflow connection validation only

**Test Class:** `TestWorkflowValidation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestWorkflowValidation:
    """Test connection validation - SOLID SRP"""

    def test_validate_workflow_connections_valid(self, http_client, sample_workflow):
        """Validate correct connections"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("validate_workflow_connections", {
            "workflow": sample_workflow
        })

        assert result["valid"] is True

    def test_validate_workflow_connections_broken(self, http_client):
        """Detect broken connections"""
        client = MCPDocumentationClient(http_client)
        workflow = {
            "nodes": [{"id": "1", "name": "A"}],
            "connections": {"A": {"main": [[{"node": "B", "type": "main"}]]}}
        }

        result = client.call_tool("validate_workflow_connections", {
            "workflow": workflow
        })

        assert result["valid"] is False
        assert "errors" in result
```

**Expected Results:**
- Connection-only validation
- Broken connections detected
- Faster than full validation

---

### 5.3 TC-DOC-021: validate_workflow_expressions

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate N8N expression validation only

**Test Class:** `TestWorkflowValidation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestWorkflowValidation:
    """Test expression validation - SOLID SRP"""

    def test_validate_workflow_expressions_valid(self, http_client):
        """Validate correct N8N expressions"""
        client = MCPDocumentationClient(http_client)
        workflow = {
            "nodes": [{
                "id": "1",
                "name": "Set",
                "type": "n8n-nodes-base.set",
                "parameters": {
                    "value": "{{ $json.field }}"  # Valid expression
                }
            }],
            "connections": {}
        }

        result = client.call_tool("validate_workflow_expressions", {
            "workflow": workflow
        })

        assert result["valid"] is True

    def test_validate_workflow_expressions_invalid(self, http_client):
        """Detect invalid N8N expressions"""
        client = MCPDocumentationClient(http_client)
        workflow = {
            "nodes": [{
                "id": "1",
                "name": "Set",
                "type": "n8n-nodes-base.set",
                "parameters": {
                    "value": "{{ $json.field"  # Missing closing braces
                }
            }],
            "connections": {}
        }

        result = client.call_tool("validate_workflow_expressions", {
            "workflow": workflow
        })

        assert result["valid"] is False
        assert "errors" in result
```

**Expected Results:**
- Expression-only validation
- Syntax errors detected
- Valid expressions pass

---

## 6. Additional Documentation Tools (2 tools)

### 6.1 TC-DOC-022: get_node_documentation

**Priority:** P2 (Common Usage)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p2`

**Objective:** Validate human-readable node documentation (87% coverage)

**Test Class:** `TestNodeDocumentation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p2
class TestNodeDocumentation:
    """Test human-readable documentation - SOLID SRP"""

    def test_get_node_documentation_coverage(self, http_client, sample_node_types):
        """Verify documentation exists for sample nodes"""
        client = MCPDocumentationClient(http_client)

        documented_count = 0
        for node_type in sample_node_types:
            result = client.call_tool("get_node_documentation", {
                "nodeType": node_type
            })

            if result.get("documentation"):
                documented_count += 1

        coverage_percent = (documented_count / len(sample_node_types)) * 100
        assert coverage_percent >= 87.0

    def test_get_node_documentation_format(self, http_client):
        """Validate documentation format"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("get_node_documentation", {
            "nodeType": "nodes-base.httpRequest"
        })

        assert "documentation" in result
        doc = result["documentation"]
        assert "description" in doc
        assert "examples" in doc or "usage" in doc
```

**Expected Results:**
- 87% of nodes have documentation
- Documentation is human-readable
- Examples included

---

### 6.2 TC-DOC-023: search_node_properties

**Priority:** P3 (Specialized)
**Markers:** `@pytest.mark.phase1`, `@pytest.mark.integration`, `@pytest.mark.p3`

**Objective:** Validate property search within nodes

**Test Class:** `TestNodeDocumentation` (SOLID SRP)

**Test Implementation:**
```python
@pytest.mark.phase1
@pytest.mark.integration
@pytest.mark.p3
class TestNodeDocumentation:
    """Test property search - SOLID SRP"""

    def test_search_node_properties_by_name(self, http_client):
        """Search for properties by name"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("search_node_properties", {
            "nodeType": "nodes-base.httpRequest",
            "propertyName": "url"
        })

        assert "properties" in result
        assert len(result["properties"]) > 0

    def test_search_node_properties_by_type(self, http_client):
        """Search for properties by type"""
        client = MCPDocumentationClient(http_client)
        result = client.call_tool("search_node_properties", {
            "nodeType": "nodes-base.webhook",
            "propertyType": "string"
        })

        assert all(prop["type"] == "string" for prop in result["properties"])
```

**Expected Results:**
- Property search works
- Results filtered correctly
- Type filtering supported

---

## Summary

### Test Coverage

- **Total Test Cases:** 23 (one per tool)
- **Priority 1 (Critical):** 5 test cases (80% coverage target)
- **Priority 2 (Common):** 5 test cases (60% coverage target)
- **Priority 3 (Specialized):** 13 test cases (40% coverage target)

### Test Execution

```bash
# Run all Phase 1 tests
pytest -v -m phase1 07-test/test_documentation_tools.py

# Run P1 critical path tests only
pytest -v -m "phase1 and p1" 07-test/test_documentation_tools.py

# Run P2 common usage tests only
pytest -v -m "phase1 and p2" 07-test/test_documentation_tools.py

# Run P3 specialized tests only
pytest -v -m "phase1 and p3" 07-test/test_documentation_tools.py

# Run with coverage
pytest --cov=07-test --cov-report=html -m phase1 07-test/test_documentation_tools.py
```

### Success Criteria

- All 23 documentation tools tested
- Database validation passes (536 nodes, 263 AI tools, 104 triggers, 87% docs)
- Template library validated (2,500+ templates)
- SOLID OOP principles followed
- All test classes implement SRP
- Fixtures use DIP (dependency injection)

---

**Document Status:** READY FOR IMPLEMENTATION
**Author:** Julia Chen, Testing Framework Specialist
**Date:** 2025-11-06
**Version:** 2.0 (Complete Rewrite - Phase 2)
**Location:** `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/07-test/DOC-TOOLS-TEST-CASES.md`
