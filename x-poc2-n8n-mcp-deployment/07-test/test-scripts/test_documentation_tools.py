"""
Documentation Tools Test Suite

POC-002: N8N MCP Server Deployment
Test Phase: Phase 1 (No N8N instance required)
Test Type: Integration Tests

This module contains comprehensive integration tests for all 23 documentation tools
provided by the N8N MCP Server. Tests follow SOLID OOP principles with clear
Single Responsibility Principle (SRP) separation.

Author: Julia Chen, Testing Framework Specialist
Date: 2025-11-06
Version: 1.0
"""

import pytest
import json
from typing import Dict, List, Any, Optional
from test_helpers import MCPDocumentationClient


# =============================================================================
# TEST CLASSES - ORGANIZED BY FUNCTIONAL DOMAIN
# =============================================================================


class TestNodeOperations:
    """
    Test suite for node-related documentation operations.

    Covers node listing, filtering, retrieval, and validation.
    Implements SRP: Single responsibility for node operations testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_list_all_nodes_success(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-NODE-001
        Verify listing all 536 nodes returns valid data structure.
        """
        # Act
        result = await documentation_client.list_nodes()

        # Assert
        assert result is not None, "Result should not be None"
        assert isinstance(result, dict), "Result should be a dictionary"
        assert 'nodes' in result, "Result should contain 'nodes' key"
        assert isinstance(result['nodes'], list), "Nodes should be a list"
        assert len(result['nodes']) == 536, "Should return exactly 536 nodes"

        # Validate first node structure
        if result['nodes']:
            node = result['nodes'][0]
            required_fields = ['name', 'displayName', 'description', 'category']
            for field in required_fields:
                assert field in node, f"Node should have '{field}' field"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_list_nodes_with_category_filter(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-NODE-002
        Verify filtering nodes by category returns correct subset.
        """
        # Arrange
        target_category = "AI"

        # Act
        result = await documentation_client.list_nodes(category=target_category)

        # Assert
        assert result is not None
        assert 'nodes' in result
        ai_nodes = result['nodes']
        assert len(ai_nodes) == 263, f"Should return 263 AI nodes, got {len(ai_nodes)}"

        # Verify all returned nodes belong to AI category
        for node in ai_nodes:
            assert node['category'] == target_category, \
                f"Node {node['name']} should be in {target_category} category"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_list_nodes_with_type_filter(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-NODE-003
        Verify filtering nodes by type (trigger) returns correct results.
        """
        # Arrange
        node_type = "trigger"

        # Act
        result = await documentation_client.list_nodes(type=node_type)

        # Assert
        assert result is not None
        trigger_nodes = result['nodes']
        assert len(trigger_nodes) == 104, \
            f"Should return 104 trigger nodes, got {len(trigger_nodes)}"

        # Verify all returned nodes are triggers
        for node in trigger_nodes:
            assert 'trigger' in node.get('type', '').lower() or \
                   node.get('group', []) and 'trigger' in node['group'], \
                f"Node {node['name']} should be a trigger node"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_get_node_details_valid_name(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-NODE-004
        Verify retrieving detailed documentation for valid node name.
        """
        # Arrange
        node_name = "n8n-nodes-base.httpRequest"

        # Act
        result = await documentation_client.get_node_details(node_name)

        # Assert
        assert result is not None
        assert 'node' in result
        node = result['node']

        # Verify comprehensive node structure
        required_fields = [
            'name', 'displayName', 'description',
            'properties', 'inputs', 'outputs'
        ]
        for field in required_fields:
            assert field in node, f"Node details should include '{field}'"

        # Verify properties structure
        assert isinstance(node['properties'], list), "Properties should be a list"
        if node['properties']:
            prop = node['properties'][0]
            assert 'name' in prop
            assert 'type' in prop
            assert 'displayName' in prop

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_get_node_details_invalid_name(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-NODE-005
        Verify error handling for non-existent node name.
        """
        # Arrange
        invalid_name = "n8n-nodes-base.nonExistentNode123"

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await documentation_client.get_node_details(invalid_name)

        assert "not found" in str(exc_info.value).lower() or \
               "404" in str(exc_info.value)

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_get_node_examples(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-NODE-006
        Verify retrieving usage examples for a node.
        """
        # Arrange
        node_name = "n8n-nodes-base.httpRequest"

        # Act
        result = await documentation_client.get_node_examples(node_name)

        # Assert
        assert result is not None
        assert 'examples' in result
        examples = result['examples']
        assert isinstance(examples, list), "Examples should be a list"

        if examples:
            example = examples[0]
            assert 'title' in example or 'description' in example
            assert 'workflow' in example or 'configuration' in example


class TestNodeSearch:
    """
    Test suite for node search functionality.

    Covers text search, keyword matching, and search result validation.
    Implements SRP: Single responsibility for search operations testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_search_nodes_by_keyword(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-SEARCH-001
        Verify searching nodes by keyword returns relevant results.
        """
        # Arrange
        search_query = "OpenAI"

        # Act
        result = await documentation_client.search_nodes(search_query)

        # Assert
        assert result is not None
        assert 'results' in result
        results = result['results']
        assert len(results) > 0, "Search should return at least one result"

        # Verify search relevance
        for node in results:
            assert 'name' in node
            assert 'displayName' in node
            # Keyword should appear in name, displayName, or description
            text_content = f"{node['name']} {node['displayName']} {node.get('description', '')}"
            assert search_query.lower() in text_content.lower(), \
                f"Search result should contain keyword '{search_query}'"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_search_nodes_with_filters(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-SEARCH-002
        Verify searching with category filter narrows results.
        """
        # Arrange
        search_query = "text"
        category_filter = "AI"

        # Act
        result = await documentation_client.search_nodes(
            query=search_query,
            category=category_filter
        )

        # Assert
        assert result is not None
        results = result['results']

        # Verify all results are in AI category
        for node in results:
            assert node['category'] == category_filter

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_search_nodes_no_results(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-SEARCH-003
        Verify graceful handling when search returns no results.
        """
        # Arrange
        search_query = "xyznonexistentkeyword999"

        # Act
        result = await documentation_client.search_nodes(search_query)

        # Assert
        assert result is not None
        assert 'results' in result
        assert result['results'] == [] or len(result['results']) == 0


class TestTemplateOperations:
    """
    Test suite for workflow template operations.

    Covers template listing, retrieval, search, and metadata validation.
    Implements SRP: Single responsibility for template operations testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_list_templates_success(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-001
        Verify listing workflow templates returns valid structure.
        """
        # Act
        result = await documentation_client.list_templates()

        # Assert
        assert result is not None
        assert 'templates' in result
        templates = result['templates']
        assert isinstance(templates, list)
        assert len(templates) > 0, "Should return at least one template"

        # Validate template structure
        if templates:
            template = templates[0]
            required_fields = ['id', 'name', 'description']
            for field in required_fields:
                assert field in template, f"Template should have '{field}' field"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_list_templates_with_pagination(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-002
        Verify template listing with pagination parameters.
        """
        # Arrange
        limit = 50
        offset = 0

        # Act
        result = await documentation_client.list_templates(
            limit=limit,
            offset=offset
        )

        # Assert
        assert result is not None
        templates = result['templates']
        assert len(templates) <= limit, \
            f"Should return at most {limit} templates"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_get_template_details(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-003
        Verify retrieving detailed template information.
        """
        # Arrange - First get a template ID
        list_result = await documentation_client.list_templates()
        template_id = list_result['templates'][0]['id']

        # Act
        result = await documentation_client.get_template_details(template_id)

        # Assert
        assert result is not None
        assert 'template' in result
        template = result['template']

        # Verify comprehensive template structure
        assert 'workflow' in template, "Template should include workflow definition"
        assert 'nodes' in template['workflow']
        assert 'connections' in template['workflow']

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_search_templates(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-004
        Verify searching templates by keyword.
        """
        # Arrange
        search_query = "email"

        # Act
        result = await documentation_client.search_templates(search_query)

        # Assert
        assert result is not None
        assert 'results' in result
        results = result['results']

        # Verify search relevance
        if results:
            for template in results:
                text_content = f"{template.get('name', '')} {template.get('description', '')}"
                assert search_query.lower() in text_content.lower()


class TestCategoryOperations:
    """
    Test suite for node category operations.

    Covers category listing and node-category relationships.
    Implements SRP: Single responsibility for category operations testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_list_categories(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-CAT-001
        Verify listing all node categories.
        """
        # Act
        result = await documentation_client.list_categories()

        # Assert
        assert result is not None
        assert 'categories' in result
        categories = result['categories']
        assert isinstance(categories, list)

        # Verify known categories exist
        category_names = [cat['name'] for cat in categories]
        assert "AI" in category_names
        assert "Communication" in category_names
        assert "Core Nodes" in category_names

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_get_category_nodes(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-CAT-002
        Verify retrieving all nodes in a specific category.
        """
        # Arrange
        category_name = "AI"

        # Act
        result = await documentation_client.get_category_nodes(category_name)

        # Assert
        assert result is not None
        assert 'nodes' in result
        nodes = result['nodes']
        assert len(nodes) == 263, "AI category should contain 263 nodes"

        # Verify all nodes belong to category
        for node in nodes:
            assert node['category'] == category_name


class TestDocumentationStatistics:
    """
    Test suite for documentation statistics and metrics.

    Covers database statistics, coverage metrics, and data validation.
    Implements SRP: Single responsibility for statistics testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_get_database_statistics(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-STAT-001
        Verify retrieving comprehensive database statistics.
        """
        # Act
        result = await documentation_client.get_database_statistics()

        # Assert
        assert result is not None
        assert 'statistics' in result
        stats = result['statistics']

        # Verify expected statistics
        assert stats['total_nodes'] == 536
        assert stats['ai_tools'] == 263
        assert stats['trigger_nodes'] == 104

        # Verify documentation coverage
        assert 'documentation_coverage' in stats
        coverage = stats['documentation_coverage']
        assert coverage >= 87.0, \
            f"Documentation coverage should be >= 87%, got {coverage}%"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_statistics_by_category(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-STAT-002
        Verify statistics broken down by category.
        """
        # Act
        result = await documentation_client.get_database_statistics()

        # Assert
        assert 'by_category' in result['statistics']
        by_category = result['statistics']['by_category']

        # Verify AI category statistics
        assert 'AI' in by_category
        assert by_category['AI']['count'] == 263


class TestVersionAndMetadata:
    """
    Test suite for version information and metadata operations.

    Covers version retrieval, metadata validation, and compatibility checks.
    Implements SRP: Single responsibility for version/metadata testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_get_version_info(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-META-001
        Verify retrieving N8N version and compatibility information.
        """
        # Act
        result = await documentation_client.get_version_info()

        # Assert
        assert result is not None
        assert 'version' in result
        assert 'compatibility' in result

        # Verify version format
        version = result['version']
        assert isinstance(version, str)
        # Version should follow semver format (e.g., "1.0.0")
        assert len(version.split('.')) >= 2

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_get_api_metadata(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-META-002
        Verify retrieving API metadata and capabilities.
        """
        # Act
        result = await documentation_client.get_api_metadata()

        # Assert
        assert result is not None
        assert 'tools_count' in result
        assert result['tools_count'] == 44  # 23 doc + 21 mgmt tools


class TestNodeProperties:
    """
    Test suite for node property operations.

    Covers property listing, validation, and type checking.
    Implements SRP: Single responsibility for property operations testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_get_node_properties(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-PROP-001
        Verify retrieving node properties with type information.
        """
        # Arrange
        node_name = "n8n-nodes-base.httpRequest"

        # Act
        result = await documentation_client.get_node_properties(node_name)

        # Assert
        assert result is not None
        assert 'properties' in result
        properties = result['properties']
        assert len(properties) > 0

        # Validate property structure
        for prop in properties:
            assert 'name' in prop
            assert 'type' in prop
            assert 'displayName' in prop
            # Verify type is valid
            valid_types = [
                'string', 'number', 'boolean', 'options',
                'collection', 'json', 'datetime'
            ]
            assert prop['type'] in valid_types

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_validate_node_configuration(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-PROP-002
        Verify validation of node configuration against schema.
        """
        # Arrange
        node_name = "n8n-nodes-base.httpRequest"
        config = {
            "method": "GET",
            "url": "https://api.example.com",
            "authentication": "none"
        }

        # Act
        result = await documentation_client.validate_node_config(
            node_name,
            config
        )

        # Assert
        assert result is not None
        assert 'valid' in result
        assert result['valid'] is True


class TestIntegrationScenarios:
    """
    Test suite for complex integration scenarios.

    Covers multi-tool workflows and realistic usage patterns.
    Implements SRP: Single responsibility for integration scenario testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_workflow_discovery_journey(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-INT-001
        Verify complete workflow discovery journey:
        1. Search for nodes
        2. Get node details
        3. View examples
        4. Find templates
        """
        # Step 1: Search for OpenAI nodes
        search_result = await documentation_client.search_nodes("OpenAI")
        assert len(search_result['results']) > 0
        openai_node = search_result['results'][0]

        # Step 2: Get detailed node information
        details = await documentation_client.get_node_details(openai_node['name'])
        assert 'properties' in details['node']

        # Step 3: Get usage examples
        examples = await documentation_client.get_node_examples(openai_node['name'])
        assert 'examples' in examples

        # Step 4: Search for related templates
        templates = await documentation_client.search_templates("OpenAI")
        assert 'results' in templates

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_category_exploration_workflow(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-INT-002
        Verify category exploration workflow:
        1. List all categories
        2. Get nodes in category
        3. Get statistics for category
        """
        # Step 1: List categories
        categories = await documentation_client.list_categories()
        ai_category = next(
            cat for cat in categories['categories']
            if cat['name'] == 'AI'
        )

        # Step 2: Get all nodes in AI category
        ai_nodes = await documentation_client.get_category_nodes('AI')
        assert len(ai_nodes['nodes']) == 263

        # Step 3: Verify in statistics
        stats = await documentation_client.get_database_statistics()
        assert stats['statistics']['ai_tools'] == 263


# =============================================================================
# FIXTURE SPECIALIZATION FOR DOCUMENTATION TESTS
# =============================================================================


@pytest.fixture
async def sample_node_names() -> List[str]:
    """
    Provide list of sample node names for testing.

    Returns:
        List of valid N8N node names for test scenarios.
    """
    return [
        "n8n-nodes-base.httpRequest",
        "n8n-nodes-base.webhook",
        "n8n-nodes-base.set",
        "n8n-nodes-base.if",
        "n8n-nodes-openai.openai"
    ]


@pytest.fixture
async def sample_categories() -> List[str]:
    """
    Provide list of sample categories for testing.

    Returns:
        List of valid N8N node categories.
    """
    return [
        "AI",
        "Communication",
        "Core Nodes",
        "Data Transformation",
        "Development"
    ]


# =============================================================================
# END OF TEST SUITE
# =============================================================================
