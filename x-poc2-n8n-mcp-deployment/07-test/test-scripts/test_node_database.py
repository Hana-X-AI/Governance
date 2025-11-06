"""
Node Database Validation Test Suite

POC-002: N8N MCP Server Deployment
Test Phase: Phase 1 (No N8N instance required)
Test Type: Integration Tests

This module validates the N8N node database integrity, completeness,
and statistical accuracy. Tests verify the 536 nodes, 263 AI tools,
104 triggers, and 87% documentation coverage metrics.

Author: Julia Chen, Testing Framework Specialist
Date: 2025-11-06
Version: 1.0
"""

import pytest
from typing import Dict, List, Any, Optional, Set
from test_helpers import MCPDocumentationClient, DatabaseValidator


# =============================================================================
# TEST CLASSES - ORGANIZED BY VALIDATION DOMAIN
# =============================================================================


class TestDatabaseStatistics:
    """
    Test suite for database-level statistics validation.

    Covers total counts, category breakdowns, and documentation coverage.
    Implements SRP: Single responsibility for statistics validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_total_node_count(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-STAT-001
        Verify database contains exactly 536 nodes.
        """
        # Act
        result = await documentation_client.get_database_statistics()

        # Assert
        assert result is not None
        stats = result['statistics']
        assert 'total_nodes' in stats
        assert stats['total_nodes'] == 536, \
            f"Expected 536 nodes, found {stats['total_nodes']}"

        # Cross-validate with direct node listing
        nodes_result = await documentation_client.list_nodes()
        actual_count = len(nodes_result['nodes'])
        assert actual_count == 536, \
            f"List nodes returned {actual_count}, expected 536"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_ai_tools_count(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-STAT-002
        Verify database contains exactly 263 AI tools.
        """
        # Act
        result = await documentation_client.get_database_statistics()

        # Assert
        stats = result['statistics']
        assert 'ai_tools' in stats
        assert stats['ai_tools'] == 263, \
            f"Expected 263 AI tools, found {stats['ai_tools']}"

        # Cross-validate by listing AI category nodes
        ai_nodes = await documentation_client.list_nodes(category='AI')
        ai_count = len(ai_nodes['nodes'])
        assert ai_count == 263, \
            f"AI category has {ai_count} nodes, expected 263"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_trigger_nodes_count(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-STAT-003
        Verify database contains exactly 104 trigger nodes.
        """
        # Act
        result = await documentation_client.get_database_statistics()

        # Assert
        stats = result['statistics']
        assert 'trigger_nodes' in stats
        assert stats['trigger_nodes'] == 104, \
            f"Expected 104 trigger nodes, found {stats['trigger_nodes']}"

        # Cross-validate by listing trigger type nodes
        trigger_nodes = await documentation_client.list_nodes(type='trigger')
        trigger_count = len(trigger_nodes['nodes'])
        assert trigger_count == 104, \
            f"Trigger type has {trigger_count} nodes, expected 104"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_documentation_coverage(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-STAT-004
        Verify documentation coverage is at least 87%.
        """
        # Act
        result = await documentation_client.get_database_statistics()

        # Assert
        stats = result['statistics']
        assert 'documentation_coverage' in stats
        coverage = stats['documentation_coverage']

        assert isinstance(coverage, (int, float)), \
            "Documentation coverage should be numeric"
        assert coverage >= 87.0, \
            f"Expected coverage >= 87%, found {coverage}%"
        assert coverage <= 100.0, \
            f"Coverage cannot exceed 100%, found {coverage}%"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_category_distribution(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-STAT-005
        Verify category distribution sums to total node count.
        """
        # Act
        result = await documentation_client.get_database_statistics()

        # Assert
        stats = result['statistics']
        assert 'by_category' in stats

        by_category = stats['by_category']
        category_sum = sum(cat_stats['count'] for cat_stats in by_category.values())

        assert category_sum == 536, \
            f"Category sum ({category_sum}) should equal total nodes (536)"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_statistics_consistency(
        self,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-STAT-006
        Verify all statistics are internally consistent.
        """
        # Act
        is_consistent = await database_validator.validate_statistics_consistency()

        # Assert
        assert is_consistent is True, \
            "Database statistics should be internally consistent"


class TestNodeDataIntegrity:
    """
    Test suite for node-level data integrity validation.

    Covers node structure, required fields, and data completeness.
    Implements SRP: Single responsibility for node data validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_all_nodes_have_required_fields(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-NODE-001
        Verify every node has all required fields.
        """
        # Arrange
        required_fields = [
            'name',
            'displayName',
            'description',
            'category',
            'version'
        ]

        # Act
        nodes_result = await documentation_client.list_nodes()
        nodes = nodes_result['nodes']

        # Assert
        missing_fields_report = []
        for node in nodes:
            for field in required_fields:
                if field not in node:
                    missing_fields_report.append({
                        'node': node.get('name', 'unknown'),
                        'missing_field': field
                    })

        assert len(missing_fields_report) == 0, \
            f"Found nodes with missing fields: {missing_fields_report[:10]}"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_node_names_are_unique(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-NODE-002
        Verify all node names are unique (no duplicates).
        """
        # Act
        nodes_result = await documentation_client.list_nodes()
        nodes = nodes_result['nodes']

        # Assert
        node_names = [node['name'] for node in nodes]
        unique_names = set(node_names)

        assert len(node_names) == len(unique_names), \
            f"Found duplicate node names. Total: {len(node_names)}, Unique: {len(unique_names)}"

        # Find duplicates if any
        if len(node_names) != len(unique_names):
            duplicates = [name for name in node_names if node_names.count(name) > 1]
            pytest.fail(f"Duplicate node names found: {set(duplicates)}")

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_node_descriptions_not_empty(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-NODE-003
        Verify all nodes have non-empty descriptions.
        """
        # Act
        nodes_result = await documentation_client.list_nodes()
        nodes = nodes_result['nodes']

        # Assert
        empty_descriptions = [
            node['name'] for node in nodes
            if not node.get('description') or node.get('description').strip() == ''
        ]

        # Allow up to 13% to have empty descriptions (87% coverage target)
        max_allowed_empty = int(536 * 0.13)
        assert len(empty_descriptions) <= max_allowed_empty, \
            f"Too many nodes with empty descriptions: {len(empty_descriptions)} " \
            f"(max allowed: {max_allowed_empty})"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_node_categories_are_valid(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-NODE-004
        Verify all nodes belong to valid categories.
        """
        # Arrange - Get valid categories
        categories_result = await documentation_client.list_categories()
        valid_categories = {cat['name'] for cat in categories_result['categories']}

        # Act
        nodes_result = await documentation_client.list_nodes()
        nodes = nodes_result['nodes']

        # Assert
        invalid_category_nodes = [
            {'name': node['name'], 'category': node.get('category')}
            for node in nodes
            if node.get('category') not in valid_categories
        ]

        assert len(invalid_category_nodes) == 0, \
            f"Found nodes with invalid categories: {invalid_category_nodes[:10]}"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_node_versions_are_valid(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-NODE-005
        Verify all nodes have valid version numbers.
        """
        # Act
        nodes_result = await documentation_client.list_nodes()
        nodes = nodes_result['nodes']

        # Assert
        invalid_version_nodes = []
        for node in nodes:
            version = node.get('version')
            if version is not None:
                # Version should be numeric
                if not isinstance(version, (int, float)):
                    try:
                        float(version)
                    except (ValueError, TypeError):
                        invalid_version_nodes.append({
                            'name': node['name'],
                            'version': version
                        })

        assert len(invalid_version_nodes) == 0, \
            f"Found nodes with invalid versions: {invalid_version_nodes[:10]}"


class TestNodeProperties:
    """
    Test suite for node properties validation.

    Covers property definitions, types, and completeness.
    Implements SRP: Single responsibility for property validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_sample_nodes_have_properties(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-PROP-001
        Verify sample of important nodes have property definitions.
        """
        # Arrange - Sample important nodes
        important_nodes = [
            "n8n-nodes-base.httpRequest",
            "n8n-nodes-base.webhook",
            "n8n-nodes-base.set",
            "n8n-nodes-base.if",
            "n8n-nodes-base.switch"
        ]

        # Act & Assert
        for node_name in important_nodes:
            try:
                result = await documentation_client.get_node_details(node_name)
                node = result['node']

                assert 'properties' in node, \
                    f"Node {node_name} should have properties field"
                assert isinstance(node['properties'], list), \
                    f"Node {node_name} properties should be a list"

            except Exception as e:
                pytest.fail(f"Failed to get properties for {node_name}: {e}")

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_property_types_are_valid(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-PROP-002
        Verify node properties have valid type definitions.
        """
        # Arrange
        valid_property_types = {
            'string', 'number', 'boolean', 'options', 'collection',
            'json', 'datetime', 'color', 'hidden', 'notice',
            'credentialsSelect', 'multiOptions', 'fixedCollection'
        }

        sample_nodes = [
            "n8n-nodes-base.httpRequest",
            "n8n-nodes-base.set"
        ]

        # Act & Assert
        for node_name in sample_nodes:
            result = await documentation_client.get_node_details(node_name)
            node = result['node']

            if 'properties' in node:
                for prop in node['properties']:
                    prop_type = prop.get('type')
                    assert prop_type in valid_property_types, \
                        f"Node {node_name} has invalid property type: {prop_type}"


class TestCategoryIntegrity:
    """
    Test suite for category-level integrity validation.

    Covers category definitions and node-category relationships.
    Implements SRP: Single responsibility for category validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_all_categories_have_nodes(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-CAT-001
        Verify every category contains at least one node.
        """
        # Act
        categories_result = await documentation_client.list_categories()
        categories = categories_result['categories']

        # Assert
        empty_categories = []
        for category in categories:
            category_name = category['name']
            nodes_result = await documentation_client.get_category_nodes(category_name)
            node_count = len(nodes_result['nodes'])

            if node_count == 0:
                empty_categories.append(category_name)

        assert len(empty_categories) == 0, \
            f"Found categories with no nodes: {empty_categories}"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_ai_category_statistics(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-CAT-002
        Verify AI category has exactly 263 nodes with correct distribution.
        """
        # Act
        ai_nodes_result = await documentation_client.get_category_nodes('AI')
        ai_nodes = ai_nodes_result['nodes']

        # Assert count
        assert len(ai_nodes) == 263, \
            f"AI category should have 263 nodes, found {len(ai_nodes)}"

        # Verify all nodes are properly categorized
        for node in ai_nodes:
            assert node['category'] == 'AI', \
                f"Node {node['name']} in AI category has wrong category: {node['category']}"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_category_names_are_unique(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-CAT-003
        Verify all category names are unique.
        """
        # Act
        categories_result = await documentation_client.list_categories()
        categories = categories_result['categories']

        # Assert
        category_names = [cat['name'] for cat in categories]
        unique_names = set(category_names)

        assert len(category_names) == len(unique_names), \
            f"Found duplicate categories. Total: {len(category_names)}, " \
            f"Unique: {len(unique_names)}"


class TestTriggerNodes:
    """
    Test suite for trigger node validation.

    Covers trigger node identification and properties.
    Implements SRP: Single responsibility for trigger validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_trigger_node_count(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-TRIG-001
        Verify exactly 104 trigger nodes exist.
        """
        # Act
        trigger_nodes = await documentation_client.list_nodes(type='trigger')

        # Assert
        assert len(trigger_nodes['nodes']) == 104, \
            f"Expected 104 trigger nodes, found {len(trigger_nodes['nodes'])}"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_trigger_nodes_have_webhook_properties(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-TRIG-002
        Verify trigger nodes have appropriate trigger-related properties.
        """
        # Act
        trigger_nodes = await documentation_client.list_nodes(type='trigger')
        nodes = trigger_nodes['nodes']

        # Sample some webhook/trigger nodes
        webhook_node = next(
            (n for n in nodes if 'webhook' in n['name'].lower()),
            None
        )

        if webhook_node:
            details = await documentation_client.get_node_details(webhook_node['name'])
            node = details['node']

            # Verify node has properties typical of triggers
            assert 'properties' in node or 'inputs' in node or 'outputs' in node


class TestDatabaseCompleteness:
    """
    Test suite for overall database completeness validation.

    Covers comprehensive validation across all dimensions.
    Implements SRP: Single responsibility for completeness validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p1
    async def test_database_validator_comprehensive_check(
        self,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-COMP-001
        Run comprehensive database validation check.
        """
        # Act
        validation_result = await database_validator.validate_complete_database()

        # Assert
        assert validation_result['valid'] is True, \
            f"Database validation failed: {validation_result.get('errors', [])}"

        # Verify all key metrics
        metrics = validation_result['metrics']
        assert metrics['total_nodes'] == 536
        assert metrics['ai_tools'] == 263
        assert metrics['trigger_nodes'] == 104
        assert metrics['documentation_coverage'] >= 87.0

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_no_orphaned_nodes(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-COMP-002
        Verify no nodes exist without valid category assignment.
        """
        # Act
        nodes_result = await documentation_client.list_nodes()
        categories_result = await documentation_client.list_categories()

        valid_categories = {cat['name'] for cat in categories_result['categories']}
        nodes = nodes_result['nodes']

        # Assert
        orphaned_nodes = [
            node['name'] for node in nodes
            if node.get('category') not in valid_categories
        ]

        assert len(orphaned_nodes) == 0, \
            f"Found orphaned nodes without valid category: {orphaned_nodes[:10]}"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_all_documented_nodes_are_retrievable(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-COMP-003
        Verify all nodes listed can be retrieved individually.
        """
        # Act
        nodes_result = await documentation_client.list_nodes()
        nodes = nodes_result['nodes']

        # Sample 20 random nodes to test retrieval
        import random
        sample_size = min(20, len(nodes))
        sample_nodes = random.sample(nodes, sample_size)

        # Assert
        failed_retrievals = []
        for node in sample_nodes:
            try:
                await documentation_client.get_node_details(node['name'])
            except Exception as e:
                failed_retrievals.append({
                    'name': node['name'],
                    'error': str(e)
                })

        assert len(failed_retrievals) == 0, \
            f"Failed to retrieve nodes: {failed_retrievals}"


class TestDataQuality:
    """
    Test suite for data quality validation.

    Covers data format, consistency, and quality metrics.
    Implements SRP: Single responsibility for quality validation.
    """

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_node_display_names_are_human_readable(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-QUAL-001
        Verify node display names are human-readable (not just technical names).
        """
        # Act
        nodes_result = await documentation_client.list_nodes()
        nodes = nodes_result['nodes']

        # Assert - Display names should not be identical to technical names
        identical_names = [
            node['name'] for node in nodes
            if node.get('displayName') == node.get('name')
        ]

        # Allow some overlap but most should be different
        assert len(identical_names) < len(nodes) * 0.5, \
            "Too many nodes have identical name and displayName"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p3
    async def test_description_quality_metrics(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-QUAL-002
        Verify description quality (length, content).
        """
        # Act
        nodes_result = await documentation_client.list_nodes()
        nodes = nodes_result['nodes']

        # Assert - Check description length distribution
        short_descriptions = [
            node['name'] for node in nodes
            if node.get('description') and len(node['description']) < 20
        ]

        # Most descriptions should be reasonably detailed
        assert len(short_descriptions) < len(nodes) * 0.3, \
            "Too many nodes have very short descriptions"

    @pytest.mark.phase1
    @pytest.mark.integration
    @pytest.mark.p2
    async def test_coverage_calculation_accuracy(
        self,
        documentation_client: MCPDocumentationClient,
        database_validator: DatabaseValidator
    ):
        """
        Test Case: DB-QUAL-003
        Verify documentation coverage calculation is accurate.
        """
        # Act
        nodes_result = await documentation_client.list_nodes()
        stats_result = await documentation_client.get_database_statistics()

        nodes = nodes_result['nodes']
        total_nodes = len(nodes)

        # Count nodes with documentation
        documented_nodes = sum(
            1 for node in nodes
            if node.get('description') and node.get('description').strip()
        )

        calculated_coverage = (documented_nodes / total_nodes) * 100

        # Assert - Coverage should match statistics (within 1% tolerance)
        reported_coverage = stats_result['statistics']['documentation_coverage']
        assert abs(calculated_coverage - reported_coverage) < 1.0, \
            f"Coverage mismatch: calculated {calculated_coverage}%, " \
            f"reported {reported_coverage}%"


# =============================================================================
# END OF TEST SUITE
# =============================================================================
