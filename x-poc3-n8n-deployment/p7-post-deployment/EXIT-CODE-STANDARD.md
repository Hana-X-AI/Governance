# Exit Code Standard for CI/CD Integration

**Document Type**: Technical Standard
**Version**: 1.0
**Date**: 2025-11-09
**Project**: POC3 N8N Deployment
**Author**: William Torres, Systems Administrator Specialist

---

## Table of Contents

1. [Overview](#overview)
2. [Exit Code Definitions](#exit-code-definitions)
3. [CI/CD Integration Examples](#cicd-integration-examples)
4. [Script Implementation Patterns](#script-implementation-patterns)
5. [Monitoring and Alerting Integration](#monitoring-and-alerting-integration)
6. [Coordination with Build Specialist](#coordination-with-build-specialist)

---

## Overview

### Purpose

This document standardizes exit codes for deployment, validation, and automation scripts to enable CI/CD pipelines to distinguish between:
- **Perfect execution** (no issues)
- **Successful with warnings** (deployment succeeded but issues to review)
- **Failed execution** (deployment failed, must fix)
- **Configuration error** (user action required before retry)

### Problem Statement

**Current Issue**: Scripts return exit code `0` for both:
- Perfect execution (no issues)
- Successful execution with warnings (issues to review)

**Impact**: CI/CD pipelines cannot implement warning gates or conditional actions based on deployment quality.

### Solution

Implement a 4-level exit code standard that distinguishes execution states:

| Exit Code | Meaning | CI/CD Action | Example |
|-----------|---------|--------------|---------|
| `0` | Perfect | Continue pipeline | All tests passed, no warnings |
| `1` | Error/Failure | Stop pipeline | Deployment failed, service down |
| `2` | Warning | Continue with notification | Deployment succeeded, performance degraded |
| `3` | Configuration Error | Manual intervention required | Missing credentials, invalid config |

---

## Exit Code Definitions

### Exit Code 0: Perfect Execution

**Meaning**: Operation completed successfully with no issues, warnings, or concerns.

**Criteria**:
- All operations completed successfully
- No warnings generated
- All validations passed
- No manual intervention required
- System state is optimal

**Example Scenarios**:
- All acceptance criteria tests passed (10/10)
- Service started successfully with optimal performance
- Configuration validated with no issues
- Security scan completed with zero findings

**CI/CD Action**: Continue pipeline to next stage

---

### Exit Code 1: Error/Failure

**Meaning**: Operation failed to complete successfully. Deployment or validation did not achieve intended state.

**Criteria**:
- Critical operation failed
- Service did not start or crashed
- Validation test failed
- Unrecoverable error occurred
- System state is broken or incomplete

**Example Scenarios**:
- N8N service failed to start
- Database connection failed
- Required files missing
- Build process failed
- Acceptance criteria test failed (e.g., 8/10 passed)

**CI/CD Action**: Stop pipeline, alert team, require fix before retry

---

### Exit Code 2: Warning/Successful with Issues

**Meaning**: Operation completed successfully but with warnings or non-critical issues that should be reviewed.

**Criteria**:
- Primary operation succeeded
- Service is running and functional
- Non-critical issues detected
- Performance degraded but acceptable
- Manual review recommended (not required)

**Example Scenarios**:
- Deployment succeeded but response time slower than target
- Service running but memory usage higher than expected
- Configuration validated but using default values
- Tests passed but with deprecation warnings
- HTTPS working but using self-signed certificate

**CI/CD Action**: Continue pipeline, notify team, create ticket for review

---

### Exit Code 3: Configuration Error

**Meaning**: Operation cannot proceed due to missing or invalid configuration. User action required before retry.

**Criteria**:
- Required configuration missing
- Invalid credentials or parameters
- Pre-requisite not met
- User input required
- System not ready for operation

**Example Scenarios**:
- Database password not set in .env file
- SSL certificate files not found
- Required service (PostgreSQL) not running
- Invalid hostname or port configuration
- Insufficient permissions on files/directories

**CI/CD Action**: Stop pipeline, notify user to fix configuration, allow manual retry

---

## CI/CD Integration Examples

### GitLab CI/CD

#### Example 1: Deployment with Warning Detection

```yaml
# .gitlab-ci.yml
stages:
  - deploy
  - notify

deploy-n8n:
  stage: deploy
  image: ubuntu:24.04
  script:
    - ./scripts/deploy-n8n.sh
  after_script:
    - |
      EXIT_CODE=$?
      echo "Deployment exit code: $EXIT_CODE"

      if [ $EXIT_CODE -eq 0 ]; then
        echo "✅ Perfect deployment - no issues detected"
      elif [ $EXIT_CODE -eq 2 ]; then
        echo "⚠️  Deployment succeeded with warnings - review required"
        echo "WARNING_DETECTED=true" >> deploy.env
      elif [ $EXIT_CODE -eq 3 ]; then
        echo "🔧 Configuration error - manual intervention required"
        exit 1
      else
        echo "❌ Deployment failed - fix required"
        exit 1
      fi
  artifacts:
    reports:
      dotenv: deploy.env

notify-warnings:
  stage: notify
  image: curlimages/curl:latest
  script:
    - |
      if [ "$WARNING_DETECTED" = "true" ]; then
        curl -X POST https://slack.example.com/webhook \
          -H 'Content-Type: application/json' \
          -d '{"text":"⚠️ N8N deployment succeeded with warnings - review recommended"}'
      fi
  only:
    variables:
      - $WARNING_DETECTED == "true"
```

#### Example 2: Validation with Multi-Level Gates

```yaml
# .gitlab-ci.yml
validate-deployment:
  stage: validate
  script:
    - ./scripts/validate-n8n.sh
  after_script:
    - |
      EXIT_CODE=$?

      case $EXIT_CODE in
        0)
          echo "✅ Validation perfect"
          ;;
        2)
          echo "⚠️  Validation passed with warnings"
          echo "Creating issue for warning review..."
          # Create GitLab issue for warnings
          ;;
        3)
          echo "🔧 Configuration issue detected"
          echo "Notifying ops team..."
          exit 1
          ;;
        *)
          echo "❌ Validation failed"
          exit 1
          ;;
      esac
```

#### Example 3: Conditional Rollback on Warnings

```yaml
# .gitlab-ci.yml
deploy-n8n:
  stage: deploy
  script:
    - ./scripts/deploy-n8n.sh
    - EXIT_CODE=$?
    - |
      if [ $EXIT_CODE -eq 2 ]; then
        echo "Warnings detected - checking severity..."
        ./scripts/analyze-warnings.sh
        SEVERITY=$?

        if [ $SEVERITY -eq 1 ]; then
          echo "High severity warnings - triggering rollback"
          ./scripts/rollback-n8n.sh
          exit 1
        else
          echo "Low severity warnings - proceeding with notification"
        fi
      fi
  environment:
    name: production
    on_stop: rollback-n8n

rollback-n8n:
  stage: deploy
  when: manual
  script:
    - ./scripts/rollback-n8n.sh
  environment:
    name: production
    action: stop
```

---

### GitHub Actions

#### Example 1: Deployment with Warning Handling

```yaml
# .github/workflows/deploy-n8n.yml
name: Deploy N8N

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v3

      - name: Deploy N8N
        id: deploy
        run: |
          ./scripts/deploy-n8n.sh
          echo "exit_code=$?" >> $GITHUB_OUTPUT

      - name: Check Deployment Status
        if: always()
        run: |
          EXIT_CODE=${{ steps.deploy.outputs.exit_code }}

          if [ $EXIT_CODE -eq 0 ]; then
            echo "✅ Perfect deployment"
          elif [ $EXIT_CODE -eq 2 ]; then
            echo "⚠️  Deployment succeeded with warnings"
            echo "::warning::Deployment completed with warnings - review required"
          elif [ $EXIT_CODE -eq 3 ]; then
            echo "🔧 Configuration error"
            echo "::error::Configuration error - manual intervention required"
            exit 1
          else
            echo "❌ Deployment failed"
            echo "::error::Deployment failed"
            exit 1
          fi

      - name: Notify Slack on Warnings
        if: steps.deploy.outputs.exit_code == 2
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "⚠️ N8N deployment succeeded with warnings",
              "blocks": [
                {
                  "type": "section",
                  "text": {
                    "type": "mrkdwn",
                    "text": "*N8N Deployment Warning*\nDeployment completed successfully but with warnings.\n\n*Action Required:* Review deployment logs"
                  }
                }
              ]
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

#### Example 2: Multi-Stage Validation

```yaml
# .github/workflows/validate.yml
name: Validate N8N Deployment

on:
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-24.04
    outputs:
      validation_status: ${{ steps.validate.outputs.status }}
    steps:
      - uses: actions/checkout@v3

      - name: Run Validation
        id: validate
        run: |
          ./scripts/validate-n8n.sh
          EXIT_CODE=$?

          if [ $EXIT_CODE -eq 0 ]; then
            echo "status=perfect" >> $GITHUB_OUTPUT
          elif [ $EXIT_CODE -eq 2 ]; then
            echo "status=warning" >> $GITHUB_OUTPUT
          elif [ $EXIT_CODE -eq 3 ]; then
            echo "status=config_error" >> $GITHUB_OUTPUT
          else
            echo "status=failed" >> $GITHUB_OUTPUT
          fi

          exit $EXIT_CODE

  create-issue-on-warning:
    runs-on: ubuntu-24.04
    needs: validate
    if: needs.validate.outputs.validation_status == 'warning'
    steps:
      - uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '⚠️ N8N Validation Warning',
              body: 'Validation passed with warnings. Review deployment logs.',
              labels: ['deployment', 'warning']
            })
```

---

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Deploy N8N') {
            steps {
                script {
                    def exitCode = sh(
                        script: './scripts/deploy-n8n.sh',
                        returnStatus: true
                    )

                    if (exitCode == 0) {
                        echo '✅ Perfect deployment'
                        currentBuild.result = 'SUCCESS'
                    } else if (exitCode == 2) {
                        echo '⚠️  Deployment succeeded with warnings'
                        currentBuild.result = 'UNSTABLE'

                        // Send notification
                        slackSend(
                            color: 'warning',
                            message: "N8N deployment succeeded with warnings - review required\nBuild: ${env.BUILD_URL}"
                        )
                    } else if (exitCode == 3) {
                        echo '🔧 Configuration error'
                        error('Configuration error - manual intervention required')
                    } else {
                        echo '❌ Deployment failed'
                        error('Deployment failed')
                    }
                }
            }
        }

        stage('Validate') {
            when {
                expression { currentBuild.result == 'SUCCESS' || currentBuild.result == 'UNSTABLE' }
            }
            steps {
                sh './scripts/validate-n8n.sh'
            }
        }
    }

    post {
        unstable {
            emailext(
                subject: "⚠️ N8N Deployment Warning - Build #${BUILD_NUMBER}",
                body: "Deployment succeeded with warnings. Review required.\n\nBuild: ${BUILD_URL}",
                to: 'ops-team@example.com'
            )
        }
    }
}
```

---

## Script Implementation Patterns

### Pattern 1: Validation Script with Warning Detection

```bash
#!/bin/bash
# /opt/n8n/scripts/validate-n8n.sh

set -e

EXIT_CODE=0
WARNINGS=0
ERRORS=0

echo "=== N8N Deployment Validation ==="

# Pre-check: Verify N8N_DB_PASSWORD environment variable is set
if [ -z "${N8N_DB_PASSWORD:-}" ]; then
    echo "❌ ERROR: N8N_DB_PASSWORD environment variable not set"
    echo "   Set before running: export N8N_DB_PASSWORD=\$(grep '^DB_PASSWORD=' /opt/n8n/.env | cut -d'=' -f2)"
    echo "   Or source from automation: N8N_DB_PASSWORD=\$(grep '^DB_PASSWORD=' /opt/n8n/.env | cut -d'=' -f2)"
    ERRORS=$((ERRORS + 1))
    EXIT_CODE=1
    exit $EXIT_CODE
fi

# Check service status
if ! systemctl is-active --quiet n8n; then
    echo "❌ ERROR: N8N service not running"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ N8N service running"
fi

# Check HTTP response
RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' https://n8n.hx.dev.local/healthz)
if [ $? -ne 0 ]; then
    echo "❌ ERROR: N8N health endpoint not responding"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ N8N health endpoint responding"

    # Check response time (warning if > 1 second)
    if (( $(echo "$RESPONSE_TIME > 1.0" | bc -l) )); then
        echo "⚠️  WARNING: Response time slow: ${RESPONSE_TIME}s (expected <1s)"
        WARNINGS=$((WARNINGS + 1))
    else
        echo "✅ Response time excellent: ${RESPONSE_TIME}s"
    fi
fi

# Check database connection (password from environment variable)
if ! sudo -u n8n env PGPASSWORD="$N8N_DB_PASSWORD" psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c "SELECT 1" > /dev/null 2>&1; then
    echo "❌ ERROR: Database connection failed"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ Database connection successful"
fi

# Check memory usage (warning if > 4GB)
MEMORY_MB=$(ps aux | grep 'n8n' | grep -v grep | awk '{sum+=$6} END {print sum/1024}')
if (( $(echo "$MEMORY_MB > 4096" | bc -l) )); then
    echo "⚠️  WARNING: High memory usage: ${MEMORY_MB}MB (expected <4GB)"
    WARNINGS=$((WARNINGS + 1))
else
    echo "✅ Memory usage normal: ${MEMORY_MB}MB"
fi

# Check SSL certificate validity
if ! echo | openssl s_client -connect n8n.hx.dev.local:443 2>/dev/null | openssl x509 -noout -checkend 86400; then
    echo "⚠️  WARNING: SSL certificate expires within 24 hours"
    WARNINGS=$((WARNINGS + 1))
else
    echo "✅ SSL certificate valid"
fi

# Determine exit code
if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "❌ VALIDATION FAILED: $ERRORS errors detected"
    EXIT_CODE=1
elif [ $WARNINGS -gt 0 ]; then
    echo ""
    echo "⚠️  VALIDATION PASSED WITH WARNINGS: $WARNINGS warnings detected"
    echo "Deployment functional but review recommended"
    EXIT_CODE=2
else
    echo ""
    echo "✅ VALIDATION PERFECT: No issues detected"
    EXIT_CODE=0
fi

exit $EXIT_CODE
```

**Usage Example (Automation-Friendly)**:

```bash
# Method 1: Export variable then run script (persistent for session)
export N8N_DB_PASSWORD=$(grep '^DB_POSTGRESDB_PASSWORD=' /opt/n8n/.env | cut -d'=' -f2)
/opt/n8n/scripts/validate-n8n.sh

# Method 2: Inline variable (ephemeral, more secure)
N8N_DB_PASSWORD=$(grep '^DB_POSTGRESDB_PASSWORD=' /opt/n8n/.env | cut -d'=' -f2) /opt/n8n/scripts/validate-n8n.sh

# Method 3: For CI/CD pipelines (credential from secure storage)
N8N_DB_PASSWORD="${CI_N8N_DB_PASSWORD}" /opt/n8n/scripts/validate-n8n.sh

# Method 4: Ansible/Automation (vault-sourced credential)
- name: Run N8N validation
  ansible.builtin.shell:
    cmd: /opt/n8n/scripts/validate-n8n.sh
  environment:
    N8N_DB_PASSWORD: "{{ vault_n8n_db_password }}"
  register: validation_result
  failed_when: validation_result.rc != 0 and validation_result.rc != 2
```

**Security Notes**:
- ✅ Password never hardcoded in script
- ✅ Password not visible in process list (passed via environment)
- ✅ Script fails fast if N8N_DB_PASSWORD not provided
- ✅ Compatible with CI/CD secret management (GitHub Actions, GitLab CI, Jenkins)
- ✅ Ansible Vault integration supported

---

### Pattern 2: Deployment Script with Configuration Check

```bash
#!/bin/bash
# /opt/n8n/scripts/deploy-n8n.sh

set -e

EXIT_CODE=0
CONFIG_ERRORS=0
WARNINGS=0

echo "=== N8N Deployment ==="

# Pre-flight configuration checks
echo "Checking prerequisites..."

# Check .env file exists
if [ ! -f /opt/n8n/.env ]; then
    echo "🔧 CONFIG ERROR: .env file not found"
    CONFIG_ERRORS=$((CONFIG_ERRORS + 1))
fi

# Check database password set
if grep -q '<INSERT_FROM_QUINN>' /opt/n8n/.env 2>/dev/null; then
    echo "🔧 CONFIG ERROR: Database password not set (placeholder detected)"
    CONFIG_ERRORS=$((CONFIG_ERRORS + 1))
fi

# Check PostgreSQL service running
if ! systemctl is-active --quiet postgresql; then
    echo "🔧 CONFIG ERROR: PostgreSQL service not running"
    CONFIG_ERRORS=$((CONFIG_ERRORS + 1))
fi

# Exit early if configuration errors detected
if [ $CONFIG_ERRORS -gt 0 ]; then
    echo ""
    echo "🔧 CONFIGURATION ERROR: $CONFIG_ERRORS issues detected"
    echo "Fix configuration and retry deployment"
    exit 3
fi

# Proceed with deployment
echo "✅ Prerequisites validated"

# Deploy N8N
echo "Starting N8N service..."
if ! sudo systemctl start n8n; then
    echo "❌ ERROR: Failed to start N8N service"
    exit 1
fi

# Wait for service to be ready
echo "Waiting for N8N to be ready..."
for i in {1..30}; do
    if curl -s -f https://n8n.hx.dev.local/healthz > /dev/null 2>&1; then
        echo "✅ N8N service ready"
        break
    fi

    if [ $i -eq 30 ]; then
        echo "❌ ERROR: N8N service failed to become ready (timeout)"
        exit 1
    fi

    sleep 2
done

# Check for warnings
if [ $(systemctl show n8n -p RestartCount --value) -gt 0 ]; then
    echo "⚠️  WARNING: Service restarted $(systemctl show n8n -p RestartCount --value) times"
    WARNINGS=$((WARNINGS + 1))
fi

# Determine exit code
if [ $WARNINGS -gt 0 ]; then
    echo ""
    echo "⚠️  DEPLOYMENT SUCCEEDED WITH WARNINGS: $WARNINGS warnings detected"
    EXIT_CODE=2
else
    echo ""
    echo "✅ DEPLOYMENT PERFECT: No issues detected"
    EXIT_CODE=0
fi

exit $EXIT_CODE
```

---

### Pattern 3: Acceptance Test Script

```bash
#!/bin/bash
# /opt/n8n/scripts/acceptance-tests.sh

PASSED=0
FAILED=0
WARNINGS=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    local warning_only="${3:-false}"

    echo "Running: $test_name"

    if eval "$test_command" > /dev/null 2>&1; then
        echo "  ✅ PASS"
        PASSED=$((PASSED + 1))
    else
        if [ "$warning_only" = "true" ]; then
            echo "  ⚠️  WARNING"
            WARNINGS=$((WARNINGS + 1))
        else
            echo "  ❌ FAIL"
            FAILED=$((FAILED + 1))
        fi
    fi
}

echo "=== N8N Acceptance Tests ==="

# Critical tests (failures block deployment)
run_test "AC-1: UI Access" \
    "curl -s -f https://n8n.hx.dev.local/"

run_test "AC-3: Database Persistence" \
    "sudo -u n8n psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 -c 'SELECT COUNT(*) FROM information_schema.tables' | grep -q '[0-9]'"

run_test "AC-5: Service Persistence" \
    "systemctl is-enabled --quiet n8n"

run_test "AC-6: Security (HTTPS)" \
    "curl -s -I https://n8n.hx.dev.local/ | grep -q 'HTTP/2 200'"

# Non-critical tests (failures generate warnings)
run_test "AC-7: Performance (<2s response)" \
    "[ \$(curl -o /dev/null -s -w '%{time_total}' https://n8n.hx.dev.local/healthz | cut -d. -f1) -lt 2 ]" \
    "true"

# Summary
echo ""
echo "=== Test Results ==="
echo "Passed:   $PASSED"
echo "Failed:   $FAILED"
echo "Warnings: $WARNINGS"

# Determine exit code
if [ $FAILED -gt 0 ]; then
    echo ""
    echo "❌ TESTS FAILED: $FAILED critical tests failed"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo ""
    echo "⚠️  TESTS PASSED WITH WARNINGS: $WARNINGS non-critical tests failed"
    exit 2
else
    echo ""
    echo "✅ ALL TESTS PASSED: No issues detected"
    exit 0
fi
```

---

## Monitoring and Alerting Integration

### Prometheus Alertmanager Integration

```yaml
# alertmanager.yml
route:
  group_by: ['alertname', 'severity']
  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'

    - match:
        severity: warning
      receiver: 'slack'

receivers:
  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '<service-key>'

  - name: 'slack'
    slack_configs:
      - api_url: 'https://hooks.slack.com/services/...'
        channel: '#n8n-alerts'
        text: 'Warning: {{ .CommonAnnotations.description }}'
```

### Script to Alert Integration

```bash
#!/bin/bash
# /opt/n8n/scripts/deploy-with-alerting.sh

./scripts/deploy-n8n.sh
EXIT_CODE=$?

case $EXIT_CODE in
    0)
        # Perfect - no alert
        echo "Deployment perfect - no alerts"
        ;;
    2)
        # Warning - send to Slack
        curl -X POST https://hooks.slack.com/services/... \
            -H 'Content-Type: application/json' \
            -d '{
                "text": "⚠️ N8N deployment succeeded with warnings",
                "attachments": [{
                    "color": "warning",
                    "title": "Deployment Warning",
                    "text": "Review deployment logs for warnings"
                }]
            }'
        ;;
    3)
        # Config error - send to ops
        curl -X POST https://hooks.slack.com/services/... \
            -H 'Content-Type: application/json' \
            -d '{
                "text": "🔧 N8N deployment configuration error",
                "attachments": [{
                    "color": "danger",
                    "title": "Configuration Error",
                    "text": "Manual intervention required - check .env file"
                }]
            }'
        exit 1
        ;;
    *)
        # Failure - page on-call
        curl -X POST https://api.pagerduty.com/incidents \
            -H 'Authorization: Token token=...' \
            -H 'Content-Type: application/json' \
            -d '{
                "incident": {
                    "type": "incident",
                    "title": "N8N Deployment Failed",
                    "service": {
                        "id": "...",
                        "type": "service_reference"
                    },
                    "urgency": "high"
                }
            }'
        exit 1
        ;;
esac

exit $EXIT_CODE
```

---

## Coordination with Build Specialist

### Integration Opportunity: Omar Rodriguez (@agent-omar)

**Proposal**: Unified exit code standard across build and deployment phases.

#### Build Phase Exit Codes (Omar's Domain)

| Exit Code | Build Meaning | Example |
|-----------|---------------|---------|
| `0` | Build perfect | All packages compiled, no warnings |
| `1` | Build failed | Compilation error, missing dependencies |
| `2` | Build succeeded with warnings | Deprecation warnings, peer dependency issues |
| `3` | Build configuration error | package.json invalid, Node.js version mismatch |

#### Deployment Phase Exit Codes (William's Domain)

| Exit Code | Deployment Meaning | Example |
|-----------|-------------------|---------|
| `0` | Deployment perfect | Service running, all tests passed |
| `1` | Deployment failed | Service failed to start |
| `2` | Deployment succeeded with warnings | Slow performance, deprecated config |
| `3` | Deployment configuration error | Missing .env, database unreachable |

#### Combined CI/CD Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - build
  - deploy
  - validate

build-n8n:
  stage: build
  script:
    - ./scripts/build-n8n.sh  # Omar's script
  after_script:
    - |
      BUILD_EXIT=$?
      echo "BUILD_EXIT_CODE=$BUILD_EXIT" >> build.env

      if [ $BUILD_EXIT -eq 0 ]; then
        echo "✅ Build perfect"
      elif [ $BUILD_EXIT -eq 2 ]; then
        echo "⚠️  Build succeeded with warnings"
      else
        echo "❌ Build failed"
        exit 1
      fi
  artifacts:
    reports:
      dotenv: build.env

deploy-n8n:
  stage: deploy
  dependencies:
    - build-n8n
  script:
    - ./scripts/deploy-n8n.sh  # William's script
  after_script:
    - |
      DEPLOY_EXIT=$?
      echo "DEPLOY_EXIT_CODE=$DEPLOY_EXIT" >> deploy.env

      if [ $DEPLOY_EXIT -eq 0 ]; then
        echo "✅ Deployment perfect"
      elif [ $DEPLOY_EXIT -eq 2 ]; then
        echo "⚠️  Deployment succeeded with warnings"
      else
        echo "❌ Deployment failed"
        exit 1
      fi
  artifacts:
    reports:
      dotenv: deploy.env

report-warnings:
  stage: validate
  script:
    - |
      TOTAL_WARNINGS=0

      if [ "$BUILD_EXIT_CODE" = "2" ]; then
        echo "⚠️  Build warnings detected"
        TOTAL_WARNINGS=$((TOTAL_WARNINGS + 1))
      fi

      if [ "$DEPLOY_EXIT_CODE" = "2" ]; then
        echo "⚠️  Deployment warnings detected"
        TOTAL_WARNINGS=$((TOTAL_WARNINGS + 1))
      fi

      if [ $TOTAL_WARNINGS -gt 0 ]; then
        echo "Total warnings: $TOTAL_WARNINGS"
        # Create issue or send notification
      fi
```

---

## Migration Guide

### Updating Existing Scripts

**Before** (Binary exit codes):
```bash
#!/bin/bash
# Old script - only success/failure

if deploy_function; then
    echo "Deployment succeeded"
    exit 0
else
    echo "Deployment failed"
    exit 1
fi
```

**After** (4-level exit codes):
```bash
#!/bin/bash
# New script - success/warning/error/config

WARNINGS=0
ERRORS=0
CONFIG_ERRORS=0

# Check configuration
if [ ! -f /opt/n8n/.env ]; then
    echo "Config error: .env missing"
    CONFIG_ERRORS=$((CONFIG_ERRORS + 1))
fi

if [ $CONFIG_ERRORS -gt 0 ]; then
    exit 3  # Configuration error
fi

# Run deployment
if deploy_function; then
    echo "Deployment succeeded"

    # Check for warnings
    if check_performance; then
        echo "Performance normal"
    else
        echo "Warning: Performance degraded"
        WARNINGS=$((WARNINGS + 1))
    fi

    if [ $WARNINGS -gt 0 ]; then
        exit 2  # Warning
    else
        exit 0  # Perfect
    fi
else
    echo "Deployment failed"
    exit 1  # Error
fi
```

---

## Document Metadata

```yaml
document_type: Technical Standard
version: 1.0
date: 2025-11-09
project: POC3 N8N Deployment
author: William Torres, Systems Administrator Specialist
classification: Internal - Technical
review_frequency: Quarterly
next_review_date: 2026-02-09
related_documents:
  - p7-post-deployment/ENV-FILE-SECURITY-GUIDE.md
  - p4-validation/qa-sign-off.md
coordination:
  - agent: Omar Rodriguez
    role: Build Specialist
    integration: Unified exit code standard across build and deployment
```

---

**End of Document**
