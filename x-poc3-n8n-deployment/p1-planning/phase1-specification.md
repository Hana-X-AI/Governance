# Phase 1: Specification - N8N Server Deployment (POC3)

**Document Type**: Specification Document
**Created**: 2025-11-07
**Project**: POC3 N8N Workflow Automation Platform Deployment
**Purpose**: Define requirements, acceptance criteria, success metrics, and risk assessment
**Classification**: Internal - Project Planning

---

## Table of Contents

1. [Overview](#overview)
2. [High-Level Requirements](#high-level-requirements)
3. [Acceptance Criteria](#acceptance-criteria)
4. [Success Metrics](#success-metrics)
5. [Risk Assessment](#risk-assessment)

---

## Overview

This specification document defines the functional, non-functional, and operational requirements for deploying n8n workflow automation platform on bare-metal infrastructure. It establishes clear validation criteria and success metrics to ensure the deployment meets quality standards and operational objectives.

**Input Documents**:
- [Phase 0: Discovery](./phase0-discovery.md) - Scope, agents, technical findings
- [Agent Constitution](/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.0-agent-constitution.md) - Quality standards
- [Deep Dive Analysis](/srv/cc/Governance/x-poc3-n8n-deployment/x-docs/n8n-master-deep-dive-analysis.md) - Technical architecture

**Specification Approach**:
- Requirements driven by POC3 objectives (automation, data sovereignty, control)
- Acceptance criteria validated by all 7 agents
- Success metrics aligned with operational readiness
- Risks identified with concrete mitigation strategies

---

## High-Level Requirements

### FR-001: System Prerequisites

**Category**: Functional Requirement - Infrastructure

**Requirement**: Ubuntu 22.04/24.04 LTS server must be provisioned with Node.js 22.x LTS, pnpm 10.18.3, and all system dependencies required for n8n compilation.

**Rationale**: n8n repository enforces strict Node.js version range (≥22.16.0, ≤24.x) and requires pnpm 10.18.3 for monorepo build orchestration.

**Components**:
- Ubuntu 22.04 or 24.04 LTS operating system
- Node.js 22.x LTS (≥22.16.0)
- pnpm 10.18.3 installed via corepack
- System dependencies: build-essential, python3, cairo, pango, libpq-dev

**Owner**: @agent-william

---

### FR-002: Database Backend

**Category**: Functional Requirement - Data Layer

**Requirement**: PostgreSQL ≥13.x database `n8n_poc3` must be created with dedicated user credentials and proper schema permissions for TypeORM migrations.

**Rationale**: n8n uses TypeORM for database abstraction and requires CREATE, SELECT, INSERT, UPDATE, DELETE privileges for schema management and workflow persistence.

**Components**:
- PostgreSQL ≥13.x on hx-postgres-server (192.168.10.209)
- Database name: `n8n_poc3`
- Database user: `n8n_user` with secure password
- Privileges: CREATE, SELECT, INSERT, UPDATE, DELETE on `n8n_poc3` schema
- Connection pooling configuration (≥10 connections)

**Owner**: @agent-quinn

---

### FR-003: Build & Deploy

**Category**: Functional Requirement - Application

**Requirement**: Complete monorepo build using `pnpm build:deploy` must compile all 30+ packages and deploy artifacts to `/opt/n8n/` with proper file permissions.

**Rationale**: n8n is a monorepo requiring Turbo-orchestrated compilation. Deployment artifacts include compiled JavaScript (dist/), executable wrapper (bin/n8n), and 2000+ node_modules dependencies.

**Components**:
- Clone n8n repository (version 1.117.0)
- Run `pnpm install` (download 2000+ packages)
- Run `pnpm build:deploy` (30-45 min compilation)
- Deploy to `/opt/n8n/app/` with n8n user ownership
- Deployment artifacts: compiled dist/, bin/n8n, node_modules/

**Owner**: @agent-omar

---

### FR-004: Service Configuration

**Category**: Functional Requirement - Operations

**Requirement**: Systemd service `n8n.service` must be configured with auto-restart, resource limits, and proper environment variable configuration (100+ variables).

**Rationale**: Production deployment requires systemd integration for auto-restart on failure, boot-time startup, and resource governance.

**Components**:
- Systemd unit file: `/etc/systemd/system/n8n.service`
- Environment file: `/opt/n8n/.env` (100+ configuration variables)
- Auto-restart policy: on-failure (max 3 attempts)
- Resource limits: memory, CPU, file descriptors
- Service user: `n8n` (non-root)

**Owner**: @agent-omar, @agent-william

---

### FR-005: Network & Security

**Category**: Functional Requirement - Security

**Requirement**: Nginx reverse proxy must be configured with SSL/TLS termination, WebSocket support, and valid Samba CA SSL certificate for n8n.hx.dev.local.

**Rationale**: n8n web editor requires WebSocket connections for real-time workflow execution. HTTPS access required for credential security and browser compatibility.

**Components**:
- Nginx reverse proxy on hx-n8n-server
- SSL certificate from Samba CA for n8n.hx.dev.local
- WebSocket upgrade headers configured
- HTTPS redirect (port 80 → 443)
- DNS A record: n8n.hx.dev.local → 192.168.10.215

**Owners**: @agent-william (Nginx), @agent-frank (DNS/SSL)

---

### FR-006: Authentication

**Category**: Functional Requirement - Security

**Requirement**: Email/password authentication must be configured using n8n built-in authentication (no Enterprise license required).

**Rationale**: POC3 does not have Enterprise Edition license for LDAP integration. Built-in email/password authentication provides sufficient security for development environment.

**Components**:
- Email/password authentication enabled (default)
- First user account creation during initial setup
- Password complexity enforcement (n8n defaults)
- Session management via cookies

**Note**: Samba AD DC LDAP integration available with Enterprise Edition license (defer to future phase if needed).

**Owner**: @agent-omar

---

### FR-007: Integration

**Category**: Functional Requirement - Integration

**Requirement**: Redis session storage must be configured for user session persistence (optional, recommended for production-like setup).

**Rationale**: Redis provides scalable session storage and enables queue mode for high-volume workflow execution (optional for POC3).

**Components**:
- Redis connection configuration (optional)
- Session storage namespace (DB 2)
- Queue configuration namespace (DB 1) - if queue mode selected
- Cache namespace (DB 3)

**Note**: Redis is OPTIONAL for POC3. n8n can run in regular mode without Redis dependency.

**Owner**: @agent-samuel

---

### FR-008: Operational Readiness

**Category**: Non-Functional Requirement - Operations

**Requirement**: Backup strategy, monitoring setup, and runbook documentation must be completed before final sign-off.

**Rationale**: Operational readiness ensures platform can be maintained by operations team after deployment handoff.

**Components**:
- Encryption key backup (CRITICAL - required for data recovery)
- Database backup procedures documented
- Service health check monitoring
- Runbook with operational procedures (start, stop, restart, troubleshoot)
- Agent sign-off on respective deliverables

**Owners**: @agent-omar (encryption key), @agent-quinn (database backup), @agent-william (monitoring), @agent-julia (validation)

---

## Acceptance Criteria

### AC-001: Web UI Accessibility

**Criterion**: n8n web interface accessible at https://n8n.hx.dev.local with valid SSL certificate

**Validation**:
- Browser can access https://n8n.hx.dev.local without certificate warnings
- SSL certificate validates to Samba CA
- Web UI loads completely (no 404, 500, or network errors)

**Test Procedure**:
```bash
# DNS resolution test
nslookup n8n.hx.dev.local

# SSL certificate validation
openssl s_client -connect n8n.hx.dev.local:443 -servername n8n.hx.dev.local

# Web UI access test (manual browser test)
# Expected: n8n login page loads successfully
```

**Owner**: @agent-frank (DNS/SSL), @agent-william (Nginx), @agent-julia (validation)

---

### AC-002: Workflow Execution

**Criterion**: User can create account, login, and create/execute a simple workflow successfully

**Validation**:
- First user account created during initial setup
- User can login with email/password credentials
- User can create new workflow in editor
- Simple workflow (HTTP Request node, timer trigger) executes without errors
- Workflow execution appears in execution history

**Test Procedure**:
```bash
# First user creation (during first startup)
# POST /api/v1/owner/setup with email/password

# Login test
# POST /api/v1/auth/login with credentials

# Workflow creation test (manual via web UI)
# Create workflow with HTTP Request node
# Execute workflow
# Verify execution appears in history
```

**Owner**: @agent-omar (application), @agent-julia (validation)

---

### AC-003: Database Persistence

**Criterion**: PostgreSQL database connection verified with workflow execution persisting to database

**Validation**:
- n8n successfully connects to PostgreSQL on startup
- TypeORM migrations execute successfully (schema creation)
- Workflow executions persist to database
- Workflow data retrieval functional

**Test Procedure**:
```sql
-- Connect to PostgreSQL
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3

-- Verify schema created by TypeORM migrations
\dt

-- Verify workflow execution persistence
SELECT id, workflow_id, finished, mode FROM execution_entity LIMIT 10;
```

**Owner**: @agent-quinn (database), @agent-julia (validation)

---

### AC-004: Session Management

**Criterion**: Redis session storage functional with user sessions maintained across page refreshes (optional if Redis configured)

**Validation**:
- User login creates session in Redis
- Session persists across browser page refresh
- Session expires after configured timeout

**Test Procedure**:
```bash
# Connect to Redis
redis-cli -h 192.168.10.210

# Check session storage namespace (DB 2)
SELECT 2
KEYS *

# Verify session data exists after login
GET sess:<session_id>
```

**Owner**: @agent-samuel (Redis), @agent-julia (validation)

**Note**: This criterion is OPTIONAL if Redis not configured. Session management works via cookies without Redis.

---

### AC-005: Service Auto-Start

**Criterion**: Systemd service starts automatically on boot and restarts on failure

**Validation**:
- Service enabled in systemd
- Service starts successfully after server reboot
- Service restarts automatically after kill signal

**Test Procedure**:
```bash
# Check service enabled
systemctl is-enabled n8n.service

# Reboot test
sudo reboot
# After reboot:
systemctl status n8n.service

# Restart test
sudo kill -9 $(pgrep -f 'node.*n8n')
sleep 5
systemctl status n8n.service
# Expected: service auto-restarted
```

**Owner**: @agent-william (systemd), @agent-julia (validation)

---

### AC-006: WebSocket Support

**Criterion**: Nginx reverse proxy properly handles WebSocket connections for workflow editor

**Validation**:
- WebSocket upgrade headers configured in Nginx
- Real-time workflow execution updates appear in editor
- No WebSocket connection errors in browser console

**Test Procedure**:
```bash
# Check Nginx configuration
grep -A 5 'upgrade' /etc/nginx/sites-enabled/n8n.conf

# Browser console test (manual)
# Open workflow editor, execute workflow
# Verify WebSocket connection established (ws:// or wss://)
# Verify real-time execution status updates
```

**Owner**: @agent-william (Nginx), @agent-julia (validation)

---

### AC-007: Agent Sign-Off

**Criterion**: All 7 agents sign off on their respective components

**Validation**:
- @agent-frank: DNS record validated, SSL certificate deployed
- @agent-william: Server provisioned, Node.js/Nginx configured
- @agent-quinn: Database created, connection validated
- @agent-samuel: Redis configured (if in scope)
- @agent-omar: Application built, deployed, first startup successful
- @agent-julia: All acceptance criteria validated
- @agent-olivia: MCP integration deferred (Phase 2)
- @agent-george: FastMCP integration deferred (Phase 2)

**Test Procedure**: Each agent confirms deliverables via formal sign-off checklist.

**Owner**: @agent-zero (orchestrator)

---

### AC-008: Backup & Recovery

**Criterion**: Backup and recovery procedures documented and tested

**Validation**:
- Encryption key backed up to secure location
- Database backup procedure documented
- Restoration test performed successfully

**Test Procedure**:
```bash
# Encryption key backup
cat /opt/n8n/.env | grep N8N_ENCRYPTION_KEY
# Copy to secure backup location

# Database backup
pg_dump -h 192.168.10.209 -U n8n_user n8n_poc3 > n8n_poc3_backup.sql

# Restoration test
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3_test < n8n_poc3_backup.sql
```

**Owner**: @agent-omar (encryption key), @agent-quinn (database backup)

---

### AC-009: Health Checks

**Criterion**: Monitoring and health checks configured and reporting correctly

**Validation**:
- Health check endpoint responding (GET /healthz)
- Service status reporting correctly
- Basic metrics collected (uptime, workflow executions)

**Test Procedure**:
```bash
# Health check test
curl -I https://n8n.hx.dev.local/healthz

# Service status
systemctl status n8n.service

# Check logs for errors
journalctl -u n8n.service --since "1 hour ago" | grep -i error
```

**Owner**: @agent-william (monitoring), @agent-julia (validation)

---

### AC-010: Runbook Documentation

**Criterion**: Runbook documentation complete with operational procedures

**Validation**:
- Start/stop/restart procedures documented
- Troubleshooting guide for common issues
- Configuration reference (environment variables)
- Escalation path documented

**Test Procedure**: Review runbook documentation completeness against template.

**Owner**: @agent-omar, @agent-william, @agent-julia

---

## Success Metrics

| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|
| **Service Availability** | N/A (not deployed) | 99.9% uptime | `systemctl status n8n` / uptime monitoring |
| **Workflow Execution Time** | N/A | <5 seconds for simple workflow | Test workflow with timer nodes, measure execution duration |
| **Build Duration** | N/A | 30-45 minutes (first build) | Time `pnpm build:deploy` process from start to completion |
| **Database Connection Pool** | N/A | ≥10 connections | PostgreSQL connection count query: `SELECT count(*) FROM pg_stat_activity WHERE datname='n8n_poc3';` |
| **SSL Certificate Validity** | N/A | Valid Samba CA cert | `openssl s_client -connect n8n.hx.dev.local:443` verification |
| **Agent Sign-off Completion** | 0/7 | 7/7 agents | Checklist completion tracking across all agent deliverables |

---

## Risk Assessment

### Risk Matrix

| Risk | Probability | Impact | Owner | Mitigation |
|------|-------------|--------|-------|------------|
| **Build fails due to missing dependencies** | Medium | High | @agent-william | Pre-install all system dependencies (build-essential, python3, cairo, pango, libpq-dev), verify with build-test first |
| **PostgreSQL connection issues** | Low | High | @agent-quinn | Test database connectivity before deployment, verify credentials, ensure firewall rules allow TCP 5432 |
| **Node.js version incompatibility** | Low | High | @agent-william | Install exact version (22.16+), use nvm for version management, validate with `node --version` |
| **pnpm build timeout/failure** | Medium | High | @agent-omar | Allocate 45+ minutes for build, monitor build logs, retry on network issues, verify disk space (20GB+) |
| **SSL certificate configuration errors** | Low | Medium | @agent-frank | Pre-generate cert with correct SANs, test with `openssl verify`, coordinate transfer with William |
| **Systemd service fails to start** | Medium | High | @agent-william, @agent-omar | Test service file syntax with `systemd-analyze verify`, verify file permissions, check logs with `journalctl -u n8n.service` |
| **Nginx WebSocket proxy issues** | Medium | Medium | @agent-william | Use tested config from analysis, verify upgrade headers, test WebSocket connection in browser console |
| **Disk space exhaustion during build** | Low | High | @agent-william | Verify 20GB+ free space before build, monitor during process with `df -h` |
| **Samba LDAP integration blocked (no Enterprise license)** | High | Low | @agent-omar | Use email/password auth for POC3 (built-in, free), document Enterprise Edition upgrade path for LDAP if needed in future |
| **Encryption key backup missed** | Low | CRITICAL | @agent-omar | Mandatory backup step in checklist, verify before proceeding to next phase, document backup location |

### Risk Severity Definitions

- **Probability**: Low (<20%), Medium (20-50%), High (>50%)
- **Impact**: Low (minor inconvenience), Medium (requires workaround), High (blocks deployment), Critical (data loss)

### Overall Risk Level: **MEDIUM**

**Assessment Rationale**:
- Most risks are Low probability with concrete mitigation strategies
- High-impact risks have proactive prevention steps
- Critical risk (encryption key) has mandatory safeguard in checklist
- Medium overall risk acceptable for POC3 greenfield deployment

---

## Next Steps

**Specification Phase Status**: ✅ **COMPLETE**

**Ready to Proceed to**: **Phase 2 - Collaborative Planning**

**Phase 2 Deliverables**:
- Task breakdown by agent (responsibilities, dependencies, timeline)
- Consolidated task list with parallel execution opportunities
- Detailed validation procedures for each agent
- Planning analyses from all 7 agents

**Inputs for Phase 2**:
- This specification document (requirements, acceptance criteria, risks)
- Phase 0 Discovery (agent identification, scope)
- Agent Constitution (coordination protocols)

---

## Document Metadata

```yaml
document_type: Specification Document
project: POC3 N8N Server Deployment
phase: Phase 1 - Specification
status: Complete
created_date: 2025-11-07
orchestrating_agent: @agent-zero
requirements_count: 8
acceptance_criteria_count: 10
success_metrics_count: 6
risks_identified: 10
next_phase: Phase 2 - Collaborative Planning
input_documents:
  - phase0-discovery.md
  - hx-agent-constitution.md
  - n8n-master-deep-dive-analysis.md
```

---

**Version**: 1.0
**Maintained By**: Agent Zero (Universal PM Orchestrator)
**Related Documents**:
- [Phase 0: Discovery](./phase0-discovery.md)
- [Phase 2: Collaborative Planning](./phase2-collaborative-planning.md)
- [Agent Constitution](/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.0-agent-constitution.md)
**Classification**: Internal - Project Planning
**Status**: Complete - Ready for Phase 2
