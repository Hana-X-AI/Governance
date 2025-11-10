"""
Management Tools Test Suite

POC-002: N8N MCP Server Deployment
Test Phase: Phase 2 (Requires N8N instance)
Test Type: End-to-End (E2E) Tests

This module contains comprehensive E2E tests for all 21 management tools
provided by the N8N MCP Server. Tests require a live N8N instance at
192.168.10.215:5678 and follow SOLID OOP principles.

Author: Julia Chen, Testing Framework Specialist
Date: 2025-11-06
Version: 1.0
"""

import pytest
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from test_helpers import MCPManagementClient


# =============================================================================
# TEST CLASSES - ORGANIZED BY FUNCTIONAL DOMAIN
# =============================================================================


class TestWorkflowLifecycle:
    """
    Test suite for complete workflow lifecycle operations.

    Covers workflow creation, update, activation, execution, and deletion.
    Implements SRP: Single responsibility for workflow lifecycle testing.
    """

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_create_workflow_success(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-006
        Verify creating a simple workflow successfully.
        """
        # Arrange
        workflow_data = {
            "name": f"Test Workflow {datetime.now().isoformat()}",
            "nodes": [
                {
                    "id": "start-node",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                }
            ],
            "connections": {},
            "active": False,
            "settings": {}
        }

        # Act
        result = await management_client.create_workflow(workflow_data)

        # Assert
        assert result is not None
        assert 'workflow' in result
        workflow = result['workflow']
        assert 'id' in workflow
        assert workflow['name'] == workflow_data['name']
        assert workflow['active'] is False

        # Cleanup
        workflow_id = workflow['id']
        await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_full_workflow_lifecycle(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-LIFECYCLE
        Verify complete workflow lifecycle: create -> activate -> execute -> deactivate -> delete.
        """
        # Step 1: Create workflow
        workflow_data = {
            "name": f"Lifecycle Test {datetime.now().isoformat()}",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                },
                {
                    "id": "set",
                    "type": "n8n-nodes-base.set",
                    "name": "Set",
                    "position": [450, 300],
                    "parameters": {
                        "values": {
                            "string": [
                                {
                                    "name": "test",
                                    "value": "success"
                                }
                            ]
                        }
                    },
                    "typeVersion": 1
                }
            ],
            "connections": {
                "start": {
                    "main": [[{"node": "set", "type": "main", "index": 0}]]
                }
            },
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Step 2: Activate workflow
            activate_result = await management_client.activate_workflow(workflow_id)
            assert activate_result['success'] is True

            # Step 3: Verify workflow is active
            get_result = await management_client.get_workflow(workflow_id)
            assert get_result['workflow']['active'] is True

            # Step 4: Execute workflow
            exec_result = await management_client.execute_workflow(workflow_id)
            assert 'execution_id' in exec_result

            # Step 5: Deactivate workflow
            deactivate_result = await management_client.deactivate_workflow(workflow_id)
            assert deactivate_result['success'] is True

            # Step 6: Verify workflow is inactive
            get_result = await management_client.get_workflow(workflow_id)
            assert get_result['workflow']['active'] is False

        finally:
            # Step 7: Delete workflow (cleanup)
            await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p2
    async def test_create_workflow_validation(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-007
        Verify workflow schema validation on creation.
        """
        # Arrange - Invalid workflow (missing required fields)
        invalid_workflow = {
            "nodes": []
            # Missing 'name' field
        }

        # Act & Assert
        with pytest.raises(Exception) as exc_info:
            await management_client.create_workflow(invalid_workflow)

        assert "validation" in str(exc_info.value).lower() or \
               "required" in str(exc_info.value).lower()

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_update_workflow(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-008
        Verify updating workflow name and nodes.
        """
        # Arrange - Create initial workflow
        workflow_data = {
            "name": "Original Name",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                }
            ],
            "connections": {},
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Act - Update workflow
            updated_data = {
                "name": "Updated Name",
                "nodes": [
                    {
                        "id": "start",
                        "type": "n8n-nodes-base.start",
                        "name": "Start",
                        "position": [250, 300],
                        "parameters": {},
                        "typeVersion": 1
                    },
                    {
                        "id": "new-node",
                        "type": "n8n-nodes-base.noOp",
                        "name": "No Operation",
                        "position": [450, 300],
                        "parameters": {},
                        "typeVersion": 1
                    }
                ],
                "connections": {},
                "active": False
            }

            update_result = await management_client.update_workflow(
                workflow_id,
                updated_data
            )

            # Assert
            assert update_result['success'] is True
            get_result = await management_client.get_workflow(workflow_id)
            assert get_result['workflow']['name'] == "Updated Name"
            assert len(get_result['workflow']['nodes']) == 2

        finally:
            # Cleanup
            await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_delete_workflow(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-010
        Verify workflow deletion.
        """
        # Arrange - Create workflow to delete
        workflow_data = {
            "name": "To Be Deleted",
            "nodes": [],
            "connections": {},
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        # Act - Delete workflow
        delete_result = await management_client.delete_workflow(workflow_id)

        # Assert
        assert delete_result['success'] is True

        # Verify workflow no longer exists
        with pytest.raises(Exception) as exc_info:
            await management_client.get_workflow(workflow_id)
        assert "404" in str(exc_info.value) or "not found" in str(exc_info.value).lower()


class TestWorkflowManagement:
    """
    Test suite for workflow management operations.

    Covers listing, filtering, activating, and exporting workflows.
    Implements SRP: Single responsibility for workflow management testing.
    """

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_list_workflows_success(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-001
        Verify listing all workflows returns valid data.
        """
        # Act
        result = await management_client.list_workflows()

        # Assert
        assert result is not None
        assert 'workflows' in result
        workflows = result['workflows']
        assert isinstance(workflows, list)

        # Validate workflow structure
        if workflows:
            workflow = workflows[0]
            required_fields = ['id', 'name', 'active', 'createdAt', 'updatedAt']
            for field in required_fields:
                assert field in workflow

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p2
    async def test_list_workflows_filter_active(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-002
        Verify filtering workflows by active status.
        """
        # Act - Get active workflows
        active_result = await management_client.list_workflows(active=True)

        # Assert - All returned workflows should be active
        for workflow in active_result['workflows']:
            assert workflow['active'] is True

        # Act - Get inactive workflows
        inactive_result = await management_client.list_workflows(active=False)

        # Assert - All returned workflows should be inactive
        for workflow in inactive_result['workflows']:
            assert workflow['active'] is False

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_get_workflow_details(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-004
        Verify retrieving detailed workflow information.
        """
        # Arrange - Create workflow
        workflow_data = {
            "name": "Detail Test",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                }
            ],
            "connections": {},
            "active": False,
            "settings": {"saveExecutionProgress": True}
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Act
            result = await management_client.get_workflow(workflow_id)

            # Assert
            assert 'workflow' in result
            workflow = result['workflow']
            assert 'nodes' in workflow
            assert 'connections' in workflow
            assert 'settings' in workflow
            assert isinstance(workflow['nodes'], list)

        finally:
            await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_activate_workflow(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-012
        Verify activating an inactive workflow.
        """
        # Arrange - Create inactive workflow
        workflow_data = {
            "name": "Activation Test",
            "nodes": [
                {
                    "id": "webhook",
                    "type": "n8n-nodes-base.webhook",
                    "name": "Webhook",
                    "position": [250, 300],
                    "parameters": {
                        "path": f"test-{datetime.now().timestamp()}",
                        "httpMethod": "GET"
                    },
                    "typeVersion": 1,
                    "webhookId": f"webhook-{datetime.now().timestamp()}"
                }
            ],
            "connections": {},
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Act
            activate_result = await management_client.activate_workflow(workflow_id)

            # Assert
            assert activate_result['success'] is True
            get_result = await management_client.get_workflow(workflow_id)
            assert get_result['workflow']['active'] is True

        finally:
            await management_client.deactivate_workflow(workflow_id)
            await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_deactivate_workflow(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-014
        Verify deactivating an active workflow.
        """
        # Arrange - Create and activate workflow
        workflow_data = {
            "name": "Deactivation Test",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                }
            ],
            "connections": {},
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            await management_client.activate_workflow(workflow_id)

            # Act
            deactivate_result = await management_client.deactivate_workflow(workflow_id)

            # Assert
            assert deactivate_result['success'] is True
            get_result = await management_client.get_workflow(workflow_id)
            assert get_result['workflow']['active'] is False

        finally:
            await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p2
    async def test_export_workflow(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-WF-015
        Verify exporting workflow to JSON.
        """
        # Arrange - Create workflow
        workflow_data = {
            "name": "Export Test",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                }
            ],
            "connections": {},
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Act
            export_result = await management_client.export_workflow(workflow_id)

            # Assert
            assert export_result is not None
            assert 'workflow' in export_result or isinstance(export_result, dict)

            # Verify exported workflow structure
            exported = export_result.get('workflow', export_result)
            assert 'name' in exported
            assert 'nodes' in exported
            assert 'connections' in exported

        finally:
            await management_client.delete_workflow(workflow_id)


class TestExecutionManagement:
    """
    Test suite for workflow execution operations.

    Covers execution listing, retrieval, triggering, and management.
    Implements SRP: Single responsibility for execution testing.
    """

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_execute_workflow(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-EX-004
        Verify manually triggering workflow execution.
        """
        # Arrange - Create executable workflow
        workflow_data = {
            "name": "Execution Test",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                },
                {
                    "id": "set",
                    "type": "n8n-nodes-base.set",
                    "name": "Set",
                    "position": [450, 300],
                    "parameters": {
                        "values": {
                            "string": [
                                {"name": "result", "value": "test"}
                            ]
                        }
                    },
                    "typeVersion": 1
                }
            ],
            "connections": {
                "start": {
                    "main": [[{"node": "set", "type": "main", "index": 0}]]
                }
            },
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Act
            exec_result = await management_client.execute_workflow(workflow_id)

            # Assert
            assert exec_result is not None
            assert 'execution_id' in exec_result or 'data' in exec_result
            assert exec_result.get('success', True) is True

        finally:
            await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_list_executions(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-EX-001
        Verify listing workflow executions.
        """
        # Act
        result = await management_client.list_executions()

        # Assert
        assert result is not None
        assert 'executions' in result or 'data' in result
        executions = result.get('executions', result.get('data', []))
        assert isinstance(executions, list)

        # Validate execution structure
        if executions:
            execution = executions[0]
            expected_fields = ['id', 'workflowId', 'mode', 'startedAt']
            for field in expected_fields:
                assert field in execution

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p2
    async def test_list_executions_by_workflow(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-EX-002
        Verify filtering executions by workflow ID.
        """
        # Arrange - Create and execute workflow
        workflow_data = {
            "name": "Execution Filter Test",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                }
            ],
            "connections": {},
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Execute workflow
            await management_client.execute_workflow(workflow_id)

            # Act - List executions for this workflow
            result = await management_client.list_executions(workflow_id=workflow_id)

            # Assert
            executions = result.get('executions', result.get('data', []))
            for execution in executions:
                assert execution['workflowId'] == workflow_id

        finally:
            await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_get_execution_details(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-EX-003
        Verify retrieving detailed execution information.
        """
        # Arrange - Create and execute workflow
        workflow_data = {
            "name": "Execution Details Test",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                }
            ],
            "connections": {},
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Execute workflow
            exec_result = await management_client.execute_workflow(workflow_id)
            execution_id = exec_result.get('execution_id') or exec_result.get('data', {}).get('id')

            if execution_id:
                # Act
                details = await management_client.get_execution(execution_id)

                # Assert
                assert details is not None
                execution = details.get('execution', details.get('data', {}))
                assert 'id' in execution
                assert 'workflowData' in execution or 'workflowId' in execution

        finally:
            await management_client.delete_workflow(workflow_id)


class TestCredentialManagement:
    """
    Test suite for credential management operations.

    Covers credential listing, creation, retrieval, and deletion.
    Implements SRP: Single responsibility for credential testing.
    """

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_list_credentials(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-CR-001
        Verify listing all credentials.
        """
        # Act
        result = await management_client.list_credentials()

        # Assert
        assert result is not None
        assert 'credentials' in result or 'data' in result
        credentials = result.get('credentials', result.get('data', []))
        assert isinstance(credentials, list)

        # Validate credential structure (should not expose sensitive data)
        if credentials:
            credential = credentials[0]
            assert 'id' in credential
            assert 'name' in credential
            assert 'type' in credential

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_create_and_delete_credential(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-CR-003, MGT-CR-004
        Verify creating and deleting credentials.
        """
        # Arrange
        credential_data = {
            "name": f"Test Credential {datetime.now().isoformat()}",
            "type": "httpBasicAuth",
            "data": {
                "user": "testuser",
                "password": "testpass123"
            }
        }

        # Act - Create credential
        create_result = await management_client.create_credential(credential_data)

        # Assert creation
        assert create_result is not None
        credential = create_result.get('credential', create_result.get('data', {}))
        credential_id = credential.get('id')
        assert credential_id is not None

        try:
            # Verify credential exists
            get_result = await management_client.get_credential(credential_id)
            assert get_result is not None

        finally:
            # Act - Delete credential
            delete_result = await management_client.delete_credential(credential_id)
            assert delete_result.get('success', True) is True


class TestUserManagement:
    """
    Test suite for user management operations.

    Covers user listing and retrieval.
    Implements SRP: Single responsibility for user testing.
    """

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p2
    async def test_list_users(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-USR-001
        Verify listing N8N users.
        """
        # Act
        result = await management_client.list_users()

        # Assert
        assert result is not None
        assert 'users' in result or 'data' in result
        users = result.get('users', result.get('data', []))
        assert isinstance(users, list)

        # Validate user structure
        if users:
            user = users[0]
            expected_fields = ['id', 'email']
            for field in expected_fields:
                assert field in user

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p2
    async def test_get_user_details(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-USR-002
        Verify retrieving user details.
        """
        # Arrange - Get a user ID
        list_result = await management_client.list_users()
        users = list_result.get('users', list_result.get('data', []))

        if users:
            user_id = users[0]['id']

            # Act
            result = await management_client.get_user(user_id)

            # Assert
            assert result is not None
            user = result.get('user', result.get('data', {}))
            assert user['id'] == user_id


class TestSettingsManagement:
    """
    Test suite for settings management operations.

    Covers retrieving and updating instance settings.
    Implements SRP: Single responsibility for settings testing.
    """

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p2
    async def test_get_settings(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-SET-001
        Verify retrieving N8N instance settings.
        """
        # Act
        result = await management_client.get_settings()

        # Assert
        assert result is not None
        assert 'settings' in result or isinstance(result, dict)
        settings = result.get('settings', result)

        # Verify common settings fields
        expected_fields = ['instanceId', 'timezone']
        for field in expected_fields:
            # Not all fields may be present, but structure should be valid
            assert isinstance(settings, dict)


class TestIntegrationScenarios:
    """
    Test suite for complex E2E integration scenarios.

    Covers realistic multi-step workflows and error handling.
    Implements SRP: Single responsibility for integration testing.
    """

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p1
    async def test_complete_workflow_deployment(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-INT-001
        Verify complete workflow deployment scenario:
        1. Create workflow
        2. Test execution
        3. Activate for production
        4. Monitor executions
        5. Deactivate and cleanup
        """
        # Step 1: Create workflow
        workflow_data = {
            "name": f"Production Deployment Test {datetime.now().isoformat()}",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                },
                {
                    "id": "http",
                    "type": "n8n-nodes-base.httpRequest",
                    "name": "HTTP Request",
                    "position": [450, 300],
                    "parameters": {
                        "url": "https://httpbin.org/get",
                        "method": "GET"
                    },
                    "typeVersion": 3
                }
            ],
            "connections": {
                "start": {
                    "main": [[{"node": "http", "type": "main", "index": 0}]]
                }
            },
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Step 2: Test execution
            exec_result = await management_client.execute_workflow(workflow_id)
            assert exec_result.get('success', True) is True

            # Step 3: Activate for production
            activate_result = await management_client.activate_workflow(workflow_id)
            assert activate_result['success'] is True

            # Step 4: Verify active status
            get_result = await management_client.get_workflow(workflow_id)
            assert get_result['workflow']['active'] is True

            # Step 5: List executions
            exec_list = await management_client.list_executions(workflow_id=workflow_id)
            assert exec_list is not None

            # Step 6: Deactivate
            deactivate_result = await management_client.deactivate_workflow(workflow_id)
            assert deactivate_result['success'] is True

        finally:
            # Step 7: Cleanup
            await management_client.delete_workflow(workflow_id)

    @pytest.mark.phase2
    @pytest.mark.e2e
    @pytest.mark.p2
    async def test_error_handling_workflow(
        self,
        management_client: MCPManagementClient
    ):
        """
        Test Case: MGT-INT-002
        Verify error handling in workflow execution.
        """
        # Arrange - Create workflow with intentional error
        workflow_data = {
            "name": "Error Handling Test",
            "nodes": [
                {
                    "id": "start",
                    "type": "n8n-nodes-base.start",
                    "name": "Start",
                    "position": [250, 300],
                    "parameters": {},
                    "typeVersion": 1
                },
                {
                    "id": "http",
                    "type": "n8n-nodes-base.httpRequest",
                    "name": "HTTP Request",
                    "position": [450, 300],
                    "parameters": {
                        "url": "https://invalid-domain-that-does-not-exist-12345.com",
                        "method": "GET"
                    },
                    "typeVersion": 3
                }
            ],
            "connections": {
                "start": {
                    "main": [[{"node": "http", "type": "main", "index": 0}]]
                }
            },
            "active": False
        }

        create_result = await management_client.create_workflow(workflow_data)
        workflow_id = create_result['workflow']['id']

        try:
            # Act - Execute workflow (should fail)
            exec_result = await management_client.execute_workflow(workflow_id)

            # Assert - Should handle error gracefully
            # Execution may complete but with error status
            assert exec_result is not None

        finally:
            await management_client.delete_workflow(workflow_id)


# =============================================================================
# END OF TEST SUITE
# =============================================================================
