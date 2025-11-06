"""
Template System Test Suite

POC-002: N8N MCP Server Deployment
Test Phase: Phase 1 (No N8N instance required)
Test Type: Integration Tests

This module validates the N8N workflow template system with 2,500+ templates.
Tests cover template listing, search, retrieval, metadata validation,
and workflow structure verification.

Author: Julia Chen, Testing Framework Specialist
Date: 2025-11-06
Version: 1.0
"""

import pytest
import json
from typing import Dict, List, Any, Optional, Set
from test_helpers import MCPDocumentationClient


# =============================================================================
# TEST CLASSES - ORGANIZED BY FUNCTIONAL DOMAIN
# =============================================================================


class TestTemplateListingOperations:
    """
    Test suite for template listing operations.

    Covers template retrieval, pagination, and filtering.
    Implements SRP: Single responsibility for template listing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_list_templates_basic(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-001
        Verify basic template listing functionality.
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
        template = templates[0]
        required_fields = ['id', 'name', 'description']
        for field in required_fields:
            assert field in template, \
                f"Template should have '{field}' field"

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
        page_size = 50
        offset = 0

        # Act - Get first page
        page1 = await documentation_client.list_templates(
            limit=page_size,
            offset=offset
        )

        # Assert first page
        assert len(page1['templates']) <= page_size
        first_page_ids = {t['id'] for t in page1['templates']}

        # Act - Get second page
        page2 = await documentation_client.list_templates(
            limit=page_size,
            offset=page_size
        )

        # Assert second page
        assert len(page2['templates']) <= page_size
        second_page_ids = {t['id'] for t in page2['templates']}

        # Verify no overlap between pages
        overlap = first_page_ids & second_page_ids
        assert len(overlap) == 0, \
            f"Pages should not overlap, found {len(overlap)} duplicates"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_list_templates_large_limit(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-003
        Verify handling of large page size requests.
        """
        # Arrange
        large_limit = 500

        # Act
        result = await documentation_client.list_templates(
            limit=large_limit,
            offset=0
        )

        # Assert
        assert result is not None
        templates = result['templates']
        # Should return up to limit, but may be capped by server
        assert len(templates) <= large_limit

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_list_templates_edge_cases(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-004
        Verify edge cases: offset beyond total, limit=0, etc.
        """
        # Act - Very high offset (should return empty or last page)
        result = await documentation_client.list_templates(
            limit=10,
            offset=999999
        )

        # Assert - Should handle gracefully
        assert 'templates' in result
        assert isinstance(result['templates'], list)


class TestTemplateSearchOperations:
    """
    Test suite for template search functionality.

    Covers keyword search, filtering, and search relevance.
    Implements SRP: Single responsibility for template search.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_search_templates_by_keyword(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-005
        Verify searching templates by keyword.
        """
        # Arrange
        search_keywords = ["email", "slack", "webhook", "ai", "data"]

        for keyword in search_keywords:
            # Act
            result = await documentation_client.search_templates(keyword)

            # Assert
            assert result is not None
            assert 'results' in result
            results = result['results']

            if results:
                # Verify search relevance
                for template in results:
                    text_content = f"{template.get('name', '')} {template.get('description', '')}"
                    assert keyword.lower() in text_content.lower(), \
                        f"Search result should contain keyword '{keyword}'"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_search_templates_email_workflows(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-006
        Verify searching for email-related templates.
        """
        # Act
        result = await documentation_client.search_templates("email")

        # Assert
        assert result is not None
        results = result['results']
        assert len(results) > 0, "Should find email-related templates"

        # Verify results contain email-related content
        email_related_count = sum(
            1 for t in results
            if 'email' in t.get('name', '').lower() or
               'email' in t.get('description', '').lower()
        )
        assert email_related_count > 0

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_search_templates_ai_workflows(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-007
        Verify searching for AI-related templates.
        """
        # Act
        result = await documentation_client.search_templates("AI")

        # Assert
        assert result is not None
        results = result['results']
        assert len(results) > 0, "Should find AI-related templates"

        # Verify AI-related templates include relevant nodes
        for template in results[:5]:  # Check first 5
            # Template should mention AI in name or description
            text = f"{template.get('name', '')} {template.get('description', '')}"
            assert any(
                keyword.lower() in text.lower()
                for keyword in ['ai', 'openai', 'gpt', 'llm', 'machine learning']
            )

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_search_templates_no_results(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-008
        Verify graceful handling when search returns no results.
        """
        # Arrange - Very specific/unlikely search term
        search_query = "xyzveryrarenonexistentworkflow999"

        # Act
        result = await documentation_client.search_templates(search_query)

        # Assert
        assert result is not None
        assert 'results' in result
        assert isinstance(result['results'], list)
        # May be empty or have zero results

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_search_templates_special_characters(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-009
        Verify search handles special characters safely.
        """
        # Arrange
        special_queries = [
            "test@email.com",
            "data-processing",
            "api/webhook",
            "n8n automation"
        ]

        for query in special_queries:
            # Act
            result = await documentation_client.search_templates(query)

            # Assert - Should not crash
            assert result is not None
            assert 'results' in result


class TestTemplateDetailsOperations:
    """
    Test suite for template detail retrieval.

    Covers template detail fetching and structure validation.
    Implements SRP: Single responsibility for template details.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_get_template_details(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-010
        Verify retrieving detailed template information.
        """
        # Arrange - Get a template ID
        list_result = await documentation_client.list_templates(limit=1)
        template_id = list_result['templates'][0]['id']

        # Act
        result = await documentation_client.get_template_details(template_id)

        # Assert
        assert result is not None
        assert 'template' in result
        template = result['template']

        # Verify comprehensive template structure
        required_fields = ['id', 'name', 'description', 'workflow']
        for field in required_fields:
            assert field in template, \
                f"Template details should include '{field}'"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_template_workflow_structure(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-011
        Verify template workflow structure is valid.
        """
        # Arrange
        list_result = await documentation_client.list_templates(limit=5)

        for template_summary in list_result['templates']:
            template_id = template_summary['id']

            # Act
            result = await documentation_client.get_template_details(template_id)
            template = result['template']

            # Assert workflow structure
            assert 'workflow' in template
            workflow = template['workflow']

            # Verify essential workflow components
            assert 'nodes' in workflow, "Workflow should have nodes"
            assert isinstance(workflow['nodes'], list)
            assert len(workflow['nodes']) > 0, "Workflow should have at least one node"

            # Verify connections exist
            assert 'connections' in workflow
            assert isinstance(workflow['connections'], dict)

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_template_node_definitions(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-012
        Verify template nodes have valid definitions.
        """
        # Arrange
        list_result = await documentation_client.list_templates(limit=3)
        template_id = list_result['templates'][0]['id']

        # Act
        result = await documentation_client.get_template_details(template_id)
        workflow = result['template']['workflow']

        # Assert node structure
        for node in workflow['nodes']:
            # Verify required node fields
            required_node_fields = ['id', 'type', 'name', 'position']
            for field in required_node_fields:
                assert field in node, \
                    f"Node should have '{field}' field"

            # Verify node type format
            assert isinstance(node['type'], str)
            # Most nodes should follow naming convention
            if 'base' in node['type']:
                assert node['type'].startswith('n8n-nodes-')

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_get_template_invalid_id(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-013
        Verify error handling for invalid template ID.
        """
        # Arrange
        invalid_id = "nonexistent-template-id-12345"

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await documentation_client.get_template_details(invalid_id)

        error_msg = str(exc_info.value).lower()
        assert "not found" in error_msg or "404" in error_msg or "invalid" in error_msg


class TestTemplateMetadata:
    """
    Test suite for template metadata validation.

    Covers template tags, categories, usage stats, and metadata quality.
    Implements SRP: Single responsibility for metadata validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_template_metadata_completeness(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-014
        Verify templates have complete metadata.
        """
        # Act
        result = await documentation_client.list_templates(limit=10)
        templates = result['templates']

        # Assert
        for template in templates:
            # Basic metadata should always be present
            assert 'id' in template
            assert 'name' in template
            assert template['name'].strip() != '', "Name should not be empty"

            # Description should exist (may be empty for some)
            assert 'description' in template

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_template_tags_and_categories(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-015
        Verify template tags and categories when present.
        """
        # Act
        result = await documentation_client.list_templates(limit=20)
        templates = result['templates']

        # Assert - Check if tags/categories are used
        templates_with_tags = [
            t for t in templates
            if 'tags' in t and t['tags']
        ]

        # If tags are used, verify structure
        if templates_with_tags:
            for template in templates_with_tags:
                assert isinstance(template['tags'], (list, str))

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_template_creation_dates(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-016
        Verify template creation/update dates when available.
        """
        # Act
        result = await documentation_client.list_templates(limit=10)
        templates = result['templates']

        # Assert - If date fields exist, verify format
        for template in templates:
            if 'createdAt' in template:
                # Should be in ISO format or timestamp
                assert template['createdAt'] is not None

            if 'updatedAt' in template:
                assert template['updatedAt'] is not None


class TestTemplateWorkflowValidation:
    """
    Test suite for validating template workflow integrity.

    Covers node connections, workflow logic, and execution readiness.
    Implements SRP: Single responsibility for workflow validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_template_workflow_connections(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-017
        Verify template workflow connections are valid.
        """
        # Arrange
        list_result = await documentation_client.list_templates(limit=5)

        for template_summary in list_result['templates']:
            template_id = template_summary['id']
            result = await documentation_client.get_template_details(template_id)
            workflow = result['template']['workflow']

            # Act - Validate connections
            nodes = workflow['nodes']
            connections = workflow['connections']

            # Assert - Connection references should point to existing nodes
            node_ids = {node['id'] for node in nodes}

            for source_id, connection_map in connections.items():
                # Source should be a valid node
                assert source_id in node_ids, \
                    f"Connection source '{source_id}' should reference existing node"

                # Verify connection targets
                for connection_type, target_lists in connection_map.items():
                    for target_list in target_lists:
                        for target in target_list:
                            target_node = target.get('node')
                            if target_node:
                                assert target_node in node_ids, \
                                    f"Connection target '{target_node}' should exist"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_template_has_start_node(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-018
        Verify templates have proper entry points.
        """
        # Arrange
        list_result = await documentation_client.list_templates(limit=10)

        for template_summary in list_result['templates']:
            template_id = template_summary['id']
            result = await documentation_client.get_template_details(template_id)
            workflow = result['template']['workflow']

            # Act - Look for start/trigger nodes
            nodes = workflow['nodes']

            # Assert - Should have at least one trigger or start node
            has_trigger = any(
                'trigger' in node.get('type', '').lower() or
                'start' in node.get('type', '').lower() or
                'webhook' in node.get('type', '').lower()
                for node in nodes
            )

            assert has_trigger, \
                f"Template {template_id} should have a trigger/start node"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_template_node_positions(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-019
        Verify template nodes have valid position data.
        """
        # Arrange
        list_result = await documentation_client.list_templates(limit=5)
        template_id = list_result['templates'][0]['id']

        # Act
        result = await documentation_client.get_template_details(template_id)
        workflow = result['template']['workflow']
        nodes = workflow['nodes']

        # Assert - Nodes should have position arrays
        for node in nodes:
            if 'position' in node:
                position = node['position']
                assert isinstance(position, list)
                assert len(position) == 2, "Position should be [x, y]"
                assert isinstance(position[0], (int, float))
                assert isinstance(position[1], (int, float))


class TestTemplateUseCases:
    """
    Test suite for template use case validation.

    Covers common template scenarios and practical usage patterns.
    Implements SRP: Single responsibility for use case testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_find_api_integration_templates(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-020
        Verify finding templates for API integrations.
        """
        # Act
        result = await documentation_client.search_templates("API")

        # Assert
        assert result is not None
        results = result['results']

        # Should find API-related templates
        api_templates = [
            t for t in results
            if 'api' in t.get('name', '').lower() or
               'api' in t.get('description', '').lower()
        ]
        assert len(api_templates) > 0

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_find_automation_templates(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-021
        Verify finding templates for automation workflows.
        """
        # Act
        result = await documentation_client.search_templates("automation")

        # Assert
        assert result is not None
        results = result['results']

        if results:
            # Verify results are relevant to automation
            automation_keywords = ['automation', 'auto', 'schedule', 'trigger']
            for template in results[:5]:
                text = f"{template.get('name', '')} {template.get('description', '')}"
                assert any(kw in text.lower() for kw in automation_keywords)

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_find_data_processing_templates(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-022
        Verify finding templates for data processing.
        """
        # Act
        result = await documentation_client.search_templates("data")

        # Assert
        assert result is not None
        results = result['results']
        assert len(results) > 0, "Should find data-related templates"


class TestTemplateCollectionStatistics:
    """
    Test suite for template collection statistics.

    Covers template counts, distribution, and collection metrics.
    Implements SRP: Single responsibility for statistics validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_template_collection_size(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-023
        Verify template collection has expected size (2,500+).
        """
        # Act - Try to get total count
        result = await documentation_client.list_templates(limit=1)

        # Assert - Should have metadata about total count
        # Note: Actual count may vary, expecting 2,500+ based on requirements
        if 'total' in result:
            assert result['total'] >= 2500, \
                f"Expected at least 2,500 templates, found {result['total']}"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_template_diversity(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-024
        Verify template collection has diverse use cases.
        """
        # Act - Sample templates
        result = await documentation_client.list_templates(limit=100)
        templates = result['templates']

        # Assert - Should have variety in names (not all similar)
        unique_prefixes = set()
        for template in templates:
            name = template['name']
            # Get first word of name
            prefix = name.split()[0] if name else ''
            unique_prefixes.add(prefix.lower())

        # Should have reasonable diversity
        assert len(unique_prefixes) > 10, \
            "Template collection should have diverse use cases"


class TestTemplateIntegrationScenarios:
    """
    Test suite for template integration scenarios.

    Covers realistic template discovery and usage workflows.
    Implements SRP: Single responsibility for integration testing.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_template_discovery_workflow(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-INT-001
        Verify complete template discovery workflow:
        1. Search for templates
        2. Get template details
        3. Examine workflow structure
        """
        # Step 1: Search for email templates
        search_result = await documentation_client.search_templates("email")
        assert len(search_result['results']) > 0

        # Step 2: Get details for first result
        template_id = search_result['results'][0]['id']
        details = await documentation_client.get_template_details(template_id)

        # Step 3: Examine workflow
        assert 'workflow' in details['template']
        workflow = details['template']['workflow']
        assert 'nodes' in workflow
        assert len(workflow['nodes']) > 0

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_template_comparison_workflow(
        self,
        documentation_client: MCPDocumentationClient
    ):
        """
        Test Case: DOC-TMPL-INT-002
        Verify comparing multiple templates for same use case.
        """
        # Act - Search for common use case
        result = await documentation_client.search_templates("webhook")
        templates = result['results']

        # Assert - Should find multiple webhook templates to compare
        assert len(templates) >= 2, "Should find multiple webhook templates"

        # Get details for first two templates
        template1 = await documentation_client.get_template_details(templates[0]['id'])
        template2 = await documentation_client.get_template_details(templates[1]['id'])

        # Both should have valid workflows
        assert 'workflow' in template1['template']
        assert 'workflow' in template2['template']


# =============================================================================
# END OF TEST SUITE
# =============================================================================
