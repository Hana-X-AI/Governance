# Phase 0: Discovery - N8N Server Deployment (POC3)

**Document Type**: Discovery Document
**Created**: 2025-11-07
**Project**: POC3 N8N Workflow Automation Platform Deployment
**Purpose**: Document initial discovery findings, scope, and agent identification
**Classification**: Internal - Project Planning

---

## Table of Contents

1. [Project Goals and Objectives](#project-goals-and-objectives)
2. [Project Scope](#project-scope)
3. [Out-of-Scope](#out-of-scope)
4. [Operational Context](#operational-context)
5. [Discovery Findings](#discovery-findings)
6. [Agents Identified](#agents-identified)
7. [Open Questions](#open-questions)

---

## Project Goals and Objectives

This initiative aims to establish a self-contained, on-premise automation platform to drive process efficiency and maintain data sovereignty.

**Primary Goal**: Implement a flexible and powerful workflow automation tool that operates entirely within the organization's infrastructure, as defined in `/srv/cc/Governance/0.0-governance/0.0.2-Architecture/0.0.2.2-ecosystem-architecture.md`.

**Objectives**:

1. **Reduce manual effort and human error** by introducing workflow automation capabilities
2. **Deploy n8n successfully** using Node.js and npm on designated server (192.168.10.215)
3. **Configure dev-ready environment** using documentation at `/srv/knowledge/vault/n8n-master/` as primary source
4. **Increase automation scope** - Enable teams to build and run unlimited workflows without commercial limitations on executions or active workflows
5. **Integrate with internal systems** - Facilitate secure connections to existing on-premise databases, services, and APIs
6. **Build technical expertise** - Cultivate internal knowledge around operation, maintenance, and customization of n8n application

---

## Project Scope

This deployment is being undertaken to enable internal automation capabilities, leveraging the self-hosted benefits of n8n, while deliberately avoiding the use of Docker containers. This approach is driven by a desire for total control over the environment and to meet specific infrastructure and security constraints that may conflict with a containerized setup.

**In Scope**:
- Ubuntu server provisioning and configuration (hx-n8n-server)
- Node.js 22.x LTS installation and configuration
- Build n8n from source using pnpm monorepo toolchain
- PostgreSQL database backend configuration
- Nginx reverse proxy with SSL/TLS termination
- DNS record creation and SSL certificate generation
- Systemd service configuration for auto-restart
- Email/password authentication (built-in, no license required)
- Backup and recovery procedures
- Operational runbook documentation

**Deployment Model**: Bare-metal installation via compiled build (non-Docker)

---

## Out-of-Scope

1. **High availability and scaling**: Multi-node, distributed, or high-availability deployments are excluded from this phase. Scaling will be limited to vertical scaling on the single server.

2. **Load balancing**: Implementing a load balancer or setting up multiple n8n instances is not part of this initial scope.

3. **LDAP Authentication**: Samba AD DC LDAP integration requires n8n Enterprise Edition license (not available for POC3). Will use built-in email/password authentication instead.

4. **Redis Queue Mode**: Initial deployment will use regular execution mode (no Redis queue dependency). Queue mode can be added in future phase if high-volume workflow execution needed.

5. **MCP Integration**: N8N MCP Server and FastMCP gateway integration deferred to Phase 2 (post-POC3 enhancement).

---

## Operational Context

### Systems & Services Involved

| System/Service | Agent | Server | IP Address | Role in This Work |
|----------------|-------|--------|------------|-------------------|
| Samba AD DC/DNS/SSL | @agent-frank | hx-freeipa-server | 192.168.10.200 | Supporting - Domain accounts, DNS records, SSL certificates |
| PostgreSQL | @agent-quinn | hx-postgres-server | 192.168.10.209 | Primary - n8n database backend |
| Ubuntu Server | @agent-william | hx-n8n-server | 192.168.10.215 | Primary - OS and server configuration |
| Redis | @agent-samuel | hx-redis-server | 192.168.10.210 | Supporting - Session/cache management (optional) |
| FastMCP Gateway | @agent-george | hx-fastmcp-server | 192.168.10.213 | Supporting - MCP integration (deferred to Phase 2) |
| N8N MCP | @agent-olivia | hx-n8n-mcp-server | 192.168.10.214 | Primary - n8n MCP orchestration (deferred to Phase 2) |
| N8N Workflow | @agent-omar | hx-n8n-server | 192.168.10.215 | Primary - n8n application deployment |
| Testing & QA | @agent-julia | N/A | N/A | Supporting - Validation and testing |

### Knowledge Sources

**Required Reading** (Deep analysis for all agents):

1. **Hana-X Agent Constitution**
   - Location: `/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.0-agent-constitution.md`
   - Purpose: Governance principles, quality standards, coordination protocols

2. **N8N Master Repository**
   - Location: `/srv/knowledge/vault/n8n-master/`
   - Purpose: Source code, build instructions, configuration reference
   - Version: 1.117.0

3. **Deep Dive Analysis**
   - Location: `/srv/cc/Governance/x-poc3-n8n-deployment/x-docs/n8n-master-deep-dive-analysis.md`
   - Purpose: Comprehensive technical analysis of n8n repository

### Environment

- **Domain**: hx.dev.local
- **Environment Type**: Development
- **Network**: 192.168.10.0/24
- **Criticality**: High (automation platform)
- **Rollback Difficulty**: Medium (greenfield deployment, no existing services affected)

### Dependencies

**Infrastructure Prerequisites**:
- DNS record for n8n.hx.dev.local → 192.168.10.215
- SSL certificate from Samba CA for n8n.hx.dev.local
- Service account n8n@hx.dev.local (optional, LDAP only)

**External Services**:
- PostgreSQL database on hx-postgres-server (192.168.10.209)
- Redis cache on hx-redis-server (192.168.10.210) - optional
- Samba AD DC for DNS/SSL (192.168.10.200) - LDAP optional with Enterprise license

**Blocking Work**:
- None - this is a greenfield deployment

---

## Discovery Findings

### What We Know

**Work Required**: Deploy n8n workflow automation platform on bare-metal (non-Docker) using Node.js and npm.

**Reason**: Enable internal automation capabilities while maintaining total environmental control and meeting infrastructure/security constraints that conflict with containerized deployments.

**Task Complexity**: **Complex**
- Multi-agent coordination required (7 agents)
- Custom build process (30+ packages via pnpm monorepo)
- Enterprise integration (PostgreSQL, optional Redis, Nginx reverse proxy)
- Estimated duration: 10-14 hours optimized with parallelization

**Affected Systems**:
- Primary: hx-n8n-server (192.168.10.215)
- Supporting: hx-postgres-server, hx-freeipa-server
- Optional: hx-redis-server (if queue mode selected)
- Deferred: hx-fastmcp-server, hx-n8n-mcp-server (Phase 2)

### Technical Requirements Identified

**Node.js Version**:
- ≥22.16.0, ≤24.x
- Recommendation: Node.js 22 LTS (22.16.0+)

**Package Manager**:
- pnpm 10.18.3 (strict requirement, via corepack)

**Build Process**:
- Clone n8n repository (monorepo with 30+ packages)
- Run `pnpm install` (downloads 2000+ packages)
- Run `pnpm build:deploy` (30-45 min compilation)
- Deploy compiled artifacts to `/opt/n8n/`

**Database Backend**:
- PostgreSQL ≥13.x required
- Database name: `n8n_poc3`
- User: `n8n_user` with CREATE, SELECT, INSERT, UPDATE, DELETE privileges

**Authentication**:
- Built-in email/password authentication (no license required)
- LDAP integration available with Enterprise Edition license (defer to future)

**Execution Mode**:
- Regular mode (default, no Redis dependency)
- Queue mode available if Redis configured (optional enhancement)

---

## Agents Identified

### Primary Agents (Critical Path)

1. **@agent-omar** - N8N Workflow Application
   - **Responsibility**: Build n8n from source, deploy application, configure systemd service
   - **Criticality**: PRIMARY - Owns application deployment
   - **Timeline**: 3.7-4.0 hours (after infrastructure ready)

2. **@agent-william** - Ubuntu Server & Node.js
   - **Responsibility**: Server provisioning, Node.js/pnpm installation, Nginx configuration
   - **Criticality**: PRIMARY - Blocks Omar's build process
   - **Timeline**: 3-8 hours (parallel with Frank)

3. **@agent-quinn** - PostgreSQL Database
   - **Responsibility**: Create database `n8n_poc3`, user `n8n_user`, configure connection parameters
   - **Criticality**: PRIMARY - Required for n8n first startup
   - **Timeline**: 2-4 hours (parallel with William)

4. **@agent-frank** - Samba AD DC/DNS/SSL
   - **Responsibility**: DNS record creation, SSL certificate generation, certificate deployment
   - **Criticality**: PRIMARY - Required for HTTPS access
   - **Timeline**: 1.5-2.5 hours (parallel with William)

### Supporting Agents (Non-Blocking or Optional)

5. **@agent-samuel** - Redis Cache & Queue
   - **Responsibility**: Redis configuration for session storage and queue mode (optional)
   - **Criticality**: OPTIONAL - n8n can run without Redis in regular mode
   - **Timeline**: 2-4 hours (if queue mode selected)

6. **@agent-julia** - Testing & QA
   - **Responsibility**: Validation testing, workflow execution test, acceptance sign-off
   - **Criticality**: SUPPORTING - Validates deliverables at end
   - **Timeline**: 2-3 hours (embedded in validation phase)

### Deferred to Phase 2 (MCP Integration)

7. **@agent-olivia** - N8N MCP Server
   - **Responsibility**: Deploy N8N MCP server with 40+ MCP tools
   - **Criticality**: DEFERRED - Not required for core automation
   - **Timeline**: 3-5 days (blocked by Omar completion)

8. **@agent-george** - FastMCP Gateway
   - **Responsibility**: Configure FastMCP gateway routing for N8N MCP
   - **Criticality**: DEFERRED - Depends on Olivia completion
   - **Timeline**: 6-15 hours (blocked by Olivia)

---

## Open Questions

### Resolved During Discovery

- [x] **Node.js version requirements?**
  - **Answer**: ≥22.16.0, ≤24.x (Node.js 22 LTS recommended)

- [x] **Build process for non-Docker deployment?**
  - **Answer**: Use pnpm 10.18.3, run `pnpm build:deploy`

- [x] **PostgreSQL configuration specifics?**
  - **Answer**: PostgreSQL ≥13.x, create database `n8n_poc3`

- [x] **LDAP integration requirements?**
  - **Answer**: Requires Enterprise Edition license (alternative: email/password auth)

- [x] **Execution mode decision?**
  - **Answer**: Use regular mode (no Redis) for POC3 simplicity

- [x] **MCP integration scope?**
  - **Answer**: Defer to Phase 2 (focus on core n8n first)

### Pending Infrastructure Completion

- [ ] **Service account n8n@hx.dev.local created?**
  - **Owner**: @agent-frank
  - **Status**: Pending (optional, LDAP only)

- [ ] **Database `n8n_poc3` created?**
  - **Owner**: @agent-quinn
  - **Status**: Pending Phase 3 prerequisites (must complete before T-033 .env configuration)
  - **Phase Boundary**: This is a PRE-FLIGHT prerequisite, not Phase 4 execution work

- [ ] **DNS record n8n.hx.dev.local configured?**
  - **Owner**: @agent-frank
  - **Status**: Pending Phase 3 prerequisites (must complete before deployment)
  - **Phase Boundary**: This is a PRE-FLIGHT or early execution task (Phase 1-2), not Phase 4

---

## Next Steps

**Discovery Phase Status**: ✅ **COMPLETE**

**Ready to Proceed to**: **Phase 1 - Specification**

**Phase 1 Deliverables**:
- High-level requirements (functional, non-functional, operational)
- Acceptance criteria (validation checkpoints)
- Success metrics (measurable outcomes)
- Risk assessment (what could go wrong, mitigations)

**Inputs for Phase 1**:
- This discovery document (agent identification, scope, technical findings)
- Agent Constitution (quality standards, governance principles)
- Deep-dive analysis (technical architecture, build process)

---

## Document Metadata

```yaml
document_type: Discovery Document
project: POC3 N8N Server Deployment
phase: Phase 0 - Discovery
status: Complete
created_date: 2025-11-07
orchestrating_agent: @agent-zero
task_size: Complex
agents_identified: 8
primary_agents: 4
supporting_agents: 2
deferred_agents: 2
next_phase: Phase 1 - Specification
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial Phase 0 discovery document | @agent-zero |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Corrected phase boundaries for pending infrastructure items (lines 259-267). Changed database creation and DNS record from "Pending Phase 4 execution" to "Pending Phase 3 prerequisites" with phase boundary clarifications. Database creation (Quinn) must complete before T-033 .env configuration (PRE-FLIGHT prerequisite), and DNS record (Frank) must complete before deployment (PRE-FLIGHT or Phase 1-2). These are prerequisites for Phase 4 execution, not Phase 4 work itself. This prevents confusion about when these tasks should be completed in the project timeline. | Claude Code |

---

**Version**: 1.1
**Maintained By**: Agent Zero (Universal PM Orchestrator)
**Related Documents**:
- [Work Methodology](/srv/cc/Governance/0.0-governance/0.4-hx-work-methodology.md)
- [Phase 1 Specification](./phase1-specification.md)
- [Deep Dive Analysis](/srv/cc/Governance/x-poc3-n8n-deployment/x-docs/n8n-master-deep-dive-analysis.md)
**Classification**: Internal - Project Planning
**Status**: Complete - Ready for Phase 1
