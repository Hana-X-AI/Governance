# Agent Olivia Planning Analysis: N8N MCP Orchestration

**Document Type**: Planning Analysis
**Created**: 2025-11-07
**Agent**: @agent-olivia (Olivia Chang - N8N MCP Specialist)
**Project**: POC3 N8N Server Deployment - Phase 2: Collaborative Planning
**Classification**: Internal - Project Documentation

---

## Document Metadata

```yaml
agent_name: Olivia Chang
agent_id: agent-olivia
role: N8N MCP Specialist
project: POC3 N8N Server Deployment
phase: Phase 2 - Collaborative Planning
server: hx-n8n-mcp-server.hx.dev.local (192.168.10.217)
dependencies:
  - Omar Rodriguez (N8N Workflow Worker) - n8n instance
  - George Kim (FastMCP Gateway) - MCP routing
  - Frank Lucas (Identity & Trust) - DNS/SSL
  - William Taylor (Ubuntu Server) - OS configuration
knowledge_source: /srv/knowledge/vault/n8n-mcp-main
created_date: 2025-11-07
status: Draft - Awaiting Review
```

---

## Executive Summary

As the **N8N MCP Specialist**, I am responsible for deploying and maintaining the N8N MCP server that exposes n8n workflow automation capabilities to AI agents through the Model Context Protocol. This analysis outlines my specific responsibilities, deliverables, dependencies, timeline, and validation criteria for POC3.

**Key Findings**:
- **N8N MCP Architecture**: TypeScript-based MCP server providing 40+ tools for n8n node documentation, workflow validation, and n8n API integration
- **Deployment Model**: Standalone Node.js service on hx-n8n-mcp-server (192.168.10.217) with SQLite database for node documentation
- **Integration Points**: FastMCP gateway (George Kim) for MCP routing, n8n instance (Omar Rodriguez) for workflow operations
- **Timeline Estimate**: 3-5 days (parallel with n8n deployment by Omar)
- **Critical Dependencies**: n8n instance operational, FastMCP gateway configured, DNS/SSL from Frank

---

## Table of Contents

1. [Responsibilities & Scope](#1-responsibilities--scope)
2. [Deliverables](#2-deliverables)
3. [Dependencies](#3-dependencies)
4. [Technical Architecture](#4-technical-architecture)
5. [Timeline & Milestones](#5-timeline--milestones)
6. [Validation & Testing](#6-validation--testing)
7. [Risk Analysis](#7-risk-analysis)
8. [SOLID Principles Application](#8-solid-principles-application)
9. [Coordination Protocol](#9-coordination-protocol)
10. [Sign-Off Criteria](#10-sign-off-criteria)

---

## 1. Responsibilities & Scope

### 1.1 Primary Responsibilities

As outlined in my agent profile (`/srv/cc/Governance/0.1-agents/agent-olivia.md`), I am responsible for:

1. **N8N MCP Server Deployment**
   - Deploy n8n-mcp Node.js application to hx-n8n-mcp-server (192.168.10.217)
   - Configure SQLite database with 536+ n8n node documentation
   - Set up systemd service for automatic startup and restart
   - Configure logging and monitoring

2. **N8N Node Documentation Access**
   - Provide AI agents with access to 536+ n8n node types via MCP protocol
   - Expose node properties (99% coverage), operations (63.6% coverage), and documentation (90% coverage)
   - Serve real-world workflow examples (2,646 pre-extracted configurations from templates)
   - Enable AI-assisted workflow design and troubleshooting

3. **Workflow Template Library**
   - Maintain 2,500+ workflow template database for template discovery
   - Implement smart filtering by complexity, setup time, services, and audience
   - Support template-based workflow creation for rapid automation development

4. **N8N API Integration**
   - Connect MCP server to n8n instance (Omar Rodriguez @ hx-n8n-server)
   - Enable workflow management via MCP tools (create, update, execute workflows)
   - Coordinate safe workflow operations with Omar (he owns the n8n instance)

5. **MCP Tool Exposure**
   - Expose 40+ standardized MCP tools for AI agents:
     - **Core Tools**: node documentation, search, property lookup
     - **Template Tools**: template discovery, filtering, retrieval
     - **Validation Tools**: workflow validation, node configuration validation
     - **N8N Management Tools** (optional, requires API key): workflow CRUD, execution management

6. **FastMCP Gateway Integration**
   - Coordinate with George Kim (FastMCP Gateway) for MCP request routing
   - Register N8N MCP server endpoints with fastMCP
   - Ensure MCP protocol compliance for seamless integration

### 1.2 Out of Scope

The following are **NOT** my responsibilities:

- ❌ **N8N Instance Deployment**: Omar Rodriguez owns the n8n application on hx-n8n-server
- ❌ **Workflow Execution**: Omar's n8n instance executes workflows; I provide documentation and validation
- ❌ **N8N Database Management**: Omar manages PostgreSQL database for n8n workflows
- ❌ **DNS/SSL Provisioning**: Frank Lucas handles DNS records and SSL certificates
- ❌ **OS Configuration**: William Taylor manages Ubuntu server setup
- ❌ **MCP Gateway Infrastructure**: George Kim owns fastMCP gateway routing

### 1.3 Coordination with Other Agents

| Agent | Role | Coordination Point |
|-------|------|-------------------|
| **Omar Rodriguez** | N8N Workflow Worker | **CRITICAL** - I need his n8n instance operational and API key to enable workflow management tools |
| **George Kim** | FastMCP Gateway | **CRITICAL** - I register my MCP server with his gateway for AI agent access |
| **Frank Lucas** | Identity & Trust | **IMPORTANT** - Need DNS record (n8n-mcp.hx.dev.local) and SSL certificate |
| **William Taylor** | Ubuntu Server | **IMPORTANT** - Need server ready with Node.js 18+ and systemd |
| **Julia Martinez** | Testing & QA | **SUPPORTING** - Collaborate on MCP tool testing and validation |

---

## 2. Deliverables

### 2.1 Infrastructure Deliverables

| Deliverable | Description | Owner | Target Date |
|------------|-------------|-------|-------------|
| **Server Provisioned** | hx-n8n-mcp-server (192.168.10.217) with Ubuntu 22.04/24.04, Node.js 18+, npm, systemd | William Taylor | Day 1 |
| **DNS Record** | n8n-mcp.hx.dev.local → 192.168.10.217 | Frank Lucas | Day 1 |
| **SSL Certificate** | SSL cert for n8n-mcp.hx.dev.local from Samba CA | Frank Lucas | Day 1 |
| **N8N MCP Application** | n8n-mcp Node.js app installed at /opt/n8n-mcp/ | **Olivia Chang** | Day 2 |
| **SQLite Database** | Node documentation database (15MB) with 536+ nodes | **Olivia Chang** | Day 2 |
| **Systemd Service** | n8n-mcp.service configured for auto-start | **Olivia Chang** | Day 2 |
| **Environment Configuration** | .env file with N8N_API_URL and N8N_API_KEY (from Omar) | **Olivia Chang** | Day 3 |
| **MCP Endpoint Registration** | Register with fastMCP gateway (George Kim) | **Olivia Chang** | Day 3 |
| **Monitoring & Logging** | Logs at /var/log/n8n-mcp/, systemd journal integration | **Olivia Chang** | Day 3 |

### 2.2 Documentation Deliverables

| Deliverable | Location | Description |
|------------|----------|-------------|
| **MCP Tool Catalog** | `/srv/cc/Governance/0.4-service-operations/n8n-mcp-tool-catalog.md` | Complete list of 40+ MCP tools with descriptions, parameters, and examples |
| **N8N MCP Configuration Guide** | `/srv/cc/Governance/0.4-service-operations/n8n-mcp-configuration.md` | Environment variables, systemd service, MCP protocol settings |
| **Integration Documentation** | `/srv/cc/Governance/0.5-integrations/n8n-mcp-integration.md` | How to connect AI agents to N8N MCP (Claude Desktop, Claude Code, Cursor, etc.) |
| **Runbook** | `/srv/cc/Governance/0.6-runbooks/n8n-mcp-operations.md` | Operational procedures: start/stop, troubleshooting, database updates |
| **Credentials Update** | `/srv/cc/Governance/0.2-credentials/hx-credentials.md` | Add N8N MCP service account and API key (if needed) |

### 2.3 Testing Deliverables

| Deliverable | Description | Validation Method |
|------------|-------------|-------------------|
| **MCP Protocol Compliance** | Verify N8N MCP server responds to MCP protocol requests | MCP Inspector tool |
| **Node Documentation Access** | Validate all 536 nodes accessible via MCP tools | Automated test suite (Jest/Vitest) |
| **Template Library Access** | Verify 2,500+ templates searchable and retrievable | Query test script |
| **N8N API Integration** | Test workflow CRUD operations via MCP tools | Integration test with Omar's n8n instance |
| **FastMCP Gateway Integration** | Confirm AI agents can reach N8N MCP via George's gateway | End-to-end test from Claude Desktop |
| **Performance Benchmarks** | Average MCP tool response time <50ms (target: ~12ms) | Performance test suite |

---

## 3. Dependencies

### 3.1 Blocking Dependencies (CRITICAL PATH)

These dependencies **MUST** be resolved before I can proceed:

#### Dependency 1: N8N Instance Operational
- **Owner**: Omar Rodriguez (@agent-omar)
- **Requirement**: n8n instance running at https://hx-n8n-server.hx.dev.local (192.168.10.215)
- **Status**: ⏳ **BLOCKING** - Omar must complete n8n deployment first
- **Impact**: Without n8n instance, I can only provide node documentation tools (not workflow management tools)
- **Workaround**: Deploy N8N MCP in "documentation-only" mode first, add API integration later
- **Resolution**: Omar provides:
  - ✅ N8N instance URL (https://hx-n8n-server.hx.dev.local)
  - ✅ N8N API key for workflow management
  - ✅ Confirmation n8n API is accessible

#### Dependency 2: FastMCP Gateway Configured
- **Owner**: George Kim (@agent-george)
- **Requirement**: fastMCP gateway operational at hx-fastmcp-server (192.168.10.213)
- **Status**: ⏳ **BLOCKING** - George must deploy fastMCP gateway
- **Impact**: AI agents cannot reach N8N MCP tools without gateway routing
- **Workaround**: Test N8N MCP server directly via stdio mode (Claude Desktop) first, add gateway later
- **Resolution**: George provides:
  - ✅ FastMCP gateway URL/endpoint
  - ✅ MCP server registration procedure
  - ✅ Authentication requirements (if any)

#### Dependency 3: Server Provisioned
- **Owner**: William Taylor (@agent-william)
- **Requirement**: hx-n8n-mcp-server (192.168.10.217) ready with:
  - Ubuntu 22.04 or 24.04 LTS
  - Node.js 18+ installed
  - npm installed
  - systemd available
  - Network configured (SSH access, domain joined)
- **Status**: ⏳ **BLOCKING** - William must provision server
- **Impact**: Cannot deploy N8N MCP application
- **Resolution**: William confirms server ready via checklist

#### Dependency 4: DNS & SSL
- **Owner**: Frank Lucas (@agent-frank)
- **Requirement**:
  - DNS record: n8n-mcp.hx.dev.local → 192.168.10.217
  - SSL certificate from Samba CA for n8n-mcp.hx.dev.local
- **Status**: ⏳ **BLOCKING** - Frank must create DNS/SSL
- **Impact**: Cannot configure HTTPS endpoint for MCP server
- **Resolution**: Frank provides:
  - ✅ DNS record confirmed in Samba AD DC
  - ✅ SSL certificate files: /etc/ssl/certs/n8n-mcp.crt, /etc/ssl/private/n8n-mcp.key

### 3.2 Non-Blocking Dependencies (PARALLEL EXECUTION)

These can be resolved in parallel with my work:

| Dependency | Owner | Requirement | Impact if Missing |
|-----------|-------|-------------|-------------------|
| **N8N API Key** | Omar Rodriguez | API key for workflow management | Only documentation tools available (60% functionality) |
| **Template Library Updates** | Olivia Chang | Fetch latest n8n templates (2,500+) | Using pre-packaged templates (acceptable for POC3) |
| **MCP Inspector Tool** | George Kim | Tool for testing MCP protocol compliance | Use manual curl tests instead |

---

## 4. Technical Architecture

### 4.1 N8N MCP Server Architecture

Based on analysis of `/srv/knowledge/vault/n8n-mcp-main/`:

```
┌─────────────────────────────────────────────────────────────────────┐
│                      N8N MCP Server                                  │
│                   (hx-n8n-mcp-server:PORT)                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  MCP Protocol Handler (stdio or HTTP)                               │
│  ├── Tool Router (40+ tools)                                        │
│  │   ├── Core Tools: list_nodes, get_node_info, search_nodes       │
│  │   ├── Template Tools: search_templates, get_template            │
│  │   ├── Validation Tools: validate_workflow, validate_node        │
│  │   └── N8N Management Tools: n8n_create_workflow, n8n_execute    │
│  │                                                                  │
│  └── Data Layer                                                     │
│      ├── SQLite Database (15MB)                                    │
│      │   ├── n8n_nodes (536 nodes)                                 │
│      │   ├── n8n_properties (99% coverage)                         │
│      │   ├── n8n_operations (63.6% coverage)                       │
│      │   ├── n8n_documentation (90% coverage)                      │
│      │   └── n8n_templates (2,500+ workflows)                      │
│      │                                                              │
│      └── N8N API Client (optional)                                 │
│          └── HTTP client → hx-n8n-server.hx.dev.local              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
         │                                │
         ▼                                ▼
   FastMCP Gateway                   N8N Instance
   (George Kim)                      (Omar Rodriguez)
   192.168.10.213                    192.168.10.215
```

### 4.2 Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Node.js | ≥18.0.0 | JavaScript runtime for MCP server |
| **Language** | TypeScript | ^5.3.0 | Type-safe development |
| **Database** | SQLite (better-sqlite3, sql.js fallback) | Latest | Node documentation storage (15MB pre-built read-only database) |
| **MCP Protocol** | @modelcontextprotocol/sdk | ^1.0.4 | MCP server implementation |
| **HTTP Client** | axios | Latest | N8N API communication |
| **Process Manager** | systemd | System | Service lifecycle management |
| **Logging** | winston | Latest | Structured logging to file + console |

**Database Architecture Decision**:
- **SQLite is PRIMARY** (`better-sqlite3`): High-performance synchronous SQLite binding with FTS5 full-text search support
- **sql.js is FALLBACK**: WebAssembly-based SQLite for Node.js version compatibility issues (Docker v2.20.2+ defaults to better-sqlite3)
- **Decision Rationale**:
  - ✅ **Separate Concerns**: MCP server stores **static reference data** (node docs, templates), NOT operational data
  - ✅ **Pre-built Database**: 15MB SQLite database is packaged with n8n-mcp, contains 536 nodes + 2,500 templates
  - ✅ **Read-Only Access**: Documentation queries only, no writes during normal operation
  - ✅ **Performance**: better-sqlite3 provides 10-50x faster queries than sql.js (see: tests/benchmarks/)
  - ✅ **Portability**: Self-contained file-based database, no external dependencies
  - ❌ **PostgreSQL NOT used**: n8n's PostgreSQL (Omar's deployment) stores workflow instances, executions, and credentials—different data domain

**Why Not Reuse n8n's PostgreSQL?**
1. **Architectural Separation**: MCP server is independent service, should not depend on n8n database schema changes
2. **Data Volatility**: Node documentation is static (changes only with n8n version updates), workflow data is highly dynamic
3. **Query Patterns**: MCP needs FTS5 full-text search on documentation, n8n needs transactional workflow execution
4. **Deployment Independence**: MCP server can run standalone (documentation-only mode) without n8n instance
5. **Performance**: Embedded SQLite eliminates network latency for read-heavy documentation queries

### 4.3 File Structure

```
/opt/n8n-mcp/
├── app/                          # N8N MCP application
│   ├── dist/                     # Compiled JavaScript
│   │   └── mcp/
│   │       └── index.js          # MCP server entry point
│   ├── node_modules/             # Node.js dependencies
│   ├── package.json              # NPM package manifest
│   └── package-lock.json         # Dependency lock file
│
├── data/                         # Application data
│   └── n8n-nodes.db              # SQLite database (15MB)
│
├── logs/                         # Application logs
│   └── n8n-mcp.log               # Main log file (rotated)
│
├── .env                          # Environment configuration
└── README.md                     # Local documentation
```

### 4.4 Environment Configuration

**File**: `/opt/n8n-mcp/.env`

```bash
# ============================================================================
# N8N MCP Server Configuration
# Server: hx-n8n-mcp-server.hx.dev.local (192.168.10.217)
# Environment: Development
# Created: 2025-11-07
# ============================================================================

# ----------------------------------------------------------------------------
# MCP Server Mode
# ----------------------------------------------------------------------------
MCP_MODE=stdio                    # stdio for Claude Desktop, http for remote access
LOG_LEVEL=info                    # error, warn, info, debug
DISABLE_CONSOLE_OUTPUT=false      # Set true for production (stdio mode only)

# ----------------------------------------------------------------------------
# N8N API Integration (Optional - Enables Workflow Management Tools)
# ----------------------------------------------------------------------------
N8N_API_URL=https://hx-n8n-server.hx.dev.local
N8N_API_KEY=<provided-by-omar-rodriguez>

# ----------------------------------------------------------------------------
# Database Configuration
# ----------------------------------------------------------------------------
DATABASE_PATH=/opt/n8n-mcp/data/n8n-nodes.db
SQLJS_SAVE_INTERVAL_MS=10000      # SQLite save interval (if using sql.js fallback)

# ----------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------
WEBHOOK_SECURITY_MODE=strict      # strict (production) or moderate (local dev)

# ----------------------------------------------------------------------------
# Telemetry (Privacy)
# ----------------------------------------------------------------------------
N8N_MCP_TELEMETRY_DISABLED=true   # Disable anonymous usage statistics

# ----------------------------------------------------------------------------
# Performance
# ----------------------------------------------------------------------------
MAX_TEMPLATE_FETCH=100            # Max templates to fetch per request
CACHE_TTL_SECONDS=3600            # Template cache TTL (1 hour)
```

### 4.5 Systemd Service Configuration

**File**: `/etc/systemd/system/n8n-mcp.service`

```ini
[Unit]
Description=N8N MCP Server - Model Context Protocol for n8n Workflow Automation
Documentation=https://github.com/czlonkowski/n8n-mcp
After=network.target
Wants=network.target

[Service]
Type=simple
User=n8n-mcp
Group=n8n-mcp
WorkingDirectory=/opt/n8n-mcp
EnvironmentFile=/opt/n8n-mcp/.env
ExecStart=/usr/bin/node /opt/n8n-mcp/app/dist/mcp/index.js
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=n8n-mcp

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/n8n-mcp/data /opt/n8n-mcp/logs

# Resource limits
LimitNOFILE=4096
LimitNPROC=2048

[Install]
WantedBy=multi-user.target
```

---

## 5. Timeline & Milestones

### 5.1 Estimated Timeline

**Total Duration**: 3-5 days (assumes dependencies resolved)

**Parallel Execution Opportunities**: Days 1-2 can run in parallel with Omar's n8n deployment

### 5.2 Detailed Timeline

#### Day 1: Infrastructure Preparation (Parallel with Omar)

**Dependencies Required**: William Taylor (server), Frank Lucas (DNS/SSL)

| Task | Duration | Owner | Deliverable |
|------|----------|-------|------------|
| **1.1** Server provisioned | 2 hours | William Taylor | Ubuntu server ready with Node.js 18+ |
| **1.2** DNS record created | 30 min | Frank Lucas | n8n-mcp.hx.dev.local → 192.168.10.217 |
| **1.3** SSL certificate generated | 30 min | Frank Lucas | SSL cert from Samba CA |
| **1.4** Verify server access | 30 min | Olivia Chang | SSH login, sudo access confirmed |
| **1.5** Create service user | 15 min | Olivia Chang | `n8n-mcp` user created |

**Milestone 1**: ✅ **Infrastructure Ready** - Server provisioned with DNS/SSL

---

#### Day 2: N8N MCP Deployment (Parallel with Omar)

**Dependencies Required**: Day 1 complete

| Task | Duration | Owner | Deliverable |
|------|----------|-------|------------|
| **2.1** Clone n8n-mcp repository | 15 min | Olivia Chang | `/opt/n8n-mcp/` created |
| **2.2** Install npm dependencies | 30 min | Olivia Chang | `npm install` complete |
| **2.3** Build TypeScript application | 15 min | Olivia Chang | `npm run build` complete |
| **2.4** Initialize SQLite database | 45 min | Olivia Chang | 536 nodes loaded, 15MB database |
| **2.5** Configure .env file | 30 min | Olivia Chang | Basic config (no N8N API yet) |
| **2.6** Create systemd service | 30 min | Olivia Chang | n8n-mcp.service configured |
| **2.7** Test MCP server (stdio mode) | 1 hour | Olivia Chang | MCP protocol compliance verified |

**Milestone 2**: ✅ **N8N MCP Operational** - Documentation tools accessible via stdio mode

---

#### Day 3: N8N API Integration & Gateway Registration

**Dependencies Required**: Omar's n8n instance operational, George's fastMCP gateway ready

| Task | Duration | Owner | Deliverable |
|------|----------|-------|------------|
| **3.1** Receive n8n API key from Omar | 30 min | Omar Rodriguez | API key provided |
| **3.2** Update .env with N8N_API_URL and N8N_API_KEY | 15 min | Olivia Chang | N8N API integration configured |
| **3.3** Restart n8n-mcp service | 5 min | Olivia Chang | Service restarted with new config |
| **3.4** Test workflow management tools | 1 hour | Olivia Chang | n8n_create_workflow, n8n_list_workflows validated |
| **3.5** Register with fastMCP gateway | 1 hour | Olivia Chang + George Kim | MCP server registered with gateway |
| **3.6** Test end-to-end via Claude Desktop | 1 hour | Olivia Chang | AI agent can access N8N MCP tools via gateway |

**Milestone 3**: ✅ **Full N8N MCP Integration** - All 40+ tools accessible via fastMCP gateway

---

#### Day 4: Documentation & Testing

**Dependencies Required**: Day 3 complete

| Task | Duration | Owner | Deliverable |
|------|----------|-------|------------|
| **4.1** Write MCP Tool Catalog | 2 hours | Olivia Chang | `/srv/cc/Governance/0.4-service-operations/n8n-mcp-tool-catalog.md` |
| **4.2** Write Configuration Guide | 1 hour | Olivia Chang | `/srv/cc/Governance/0.4-service-operations/n8n-mcp-configuration.md` |
| **4.3** Write Integration Documentation | 2 hours | Olivia Chang | `/srv/cc/Governance/0.5-integrations/n8n-mcp-integration.md` |
| **4.4** Write Runbook | 2 hours | Olivia Chang | `/srv/cc/Governance/0.6-runbooks/n8n-mcp-operations.md` |
| **4.5** Update Credentials | 15 min | Olivia Chang | `/srv/cc/Governance/0.2-credentials/hx-credentials.md` updated |

**Milestone 4**: ✅ **Documentation Complete** - All operational guides written

---

#### Day 5: Validation & Sign-Off

**Dependencies Required**: Day 4 complete, Julia Martinez (Testing & QA)

| Task | Duration | Owner | Deliverable |
|------|----------|-------|------------|
| **5.1** Performance benchmarks | 1 hour | Olivia Chang | Average response time <50ms confirmed |
| **5.2** Integration testing with Julia | 2 hours | Olivia Chang + Julia Martinez | All MCP tools tested end-to-end |
| **5.3** Load testing | 1 hour | Olivia Chang | Sustained 100 req/min without errors |
| **5.4** Final validation checklist | 1 hour | Olivia Chang | All sign-off criteria met |
| **5.5** Handoff to operations | 30 min | Olivia Chang | Runbook review with ops team |

**Milestone 5**: ✅ **N8N MCP Production Ready** - Validated and operational

---

## 6. Validation & Testing

### 6.1 MCP Protocol Compliance

**Objective**: Verify N8N MCP server adheres to MCP protocol specification

**Test Method**: MCP Inspector tool (if available) or manual curl tests

**Test Cases**:

1. **MCP Protocol Handshake**
   ```bash
   # Test MCP server initialization
   echo '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}' | \
     node /opt/n8n-mcp/app/dist/mcp/index.js

   # Expected: MCP capabilities response with tools list
   ```

2. **Tool Discovery**
   ```bash
   # List available MCP tools
   echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}' | \
     node /opt/n8n-mcp/app/dist/mcp/index.js

   # Expected: Array of 40+ MCP tool definitions
   ```

3. **Tool Execution**
   ```bash
   # Test node documentation tool
   echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "list_nodes", "arguments": {}}}' | \
     node /opt/n8n-mcp/app/dist/mcp/index.js

   # Expected: List of 536 n8n nodes
   ```

**Success Criteria**: All 3 tests pass with valid JSON-RPC responses

---

### 6.2 Node Documentation Access

**Objective**: Validate all 536 n8n nodes accessible via MCP tools

**Test Method**: Automated test suite (npm test)

**Test Cases**:

| Test | Tool | Input | Expected Output |
|------|------|-------|----------------|
| **List All Nodes** | `list_nodes` | `{}` | 536 nodes returned |
| **Search Nodes** | `search_nodes` | `{query: "slack"}` | 1+ nodes with "slack" in name/description |
| **Get Node Info** | `get_node_info` | `{nodeType: "n8n-nodes-base.slack"}` | Complete node metadata |
| **Get Node Essentials** | `get_node_essentials` | `{nodeType: "n8n-nodes-base.httpRequest", includeExamples: true}` | 10-20 key properties + 3 examples |
| **Search Properties** | `search_node_properties` | `{nodeType: "n8n-nodes-base.slack", query: "auth"}` | Properties related to authentication |

**Success Criteria**: All tests pass with expected data returned in <50ms average

---

### 6.3 Template Library Access

**Objective**: Verify 2,500+ workflow templates searchable and retrievable

**Test Method**: Query test script

**Test Cases**:

| Test | Tool | Input | Expected Output |
|------|------|-------|----------------|
| **List Templates** | `list_templates` | `{}` | 2,500+ templates with metadata |
| **Search Templates** | `search_templates` | `{query: "slack notification"}` | 10+ relevant templates |
| **Advanced Search** | `search_templates_by_metadata` | `{complexity: "simple", maxSetupMinutes: 30}` | Simple templates ≤30 min setup |
| **Get Template** | `get_template` | `{templateId: "1234", mode: "full"}` | Complete workflow JSON |
| **Node Templates** | `list_node_templates` | `{nodeTypes: ["n8n-nodes-base.slack"]}` | Templates using Slack node |

**Success Criteria**: All tests return expected data, no errors

---

### 6.4 N8N API Integration

**Objective**: Test workflow CRUD operations via MCP tools

**Test Method**: Integration test with Omar's n8n instance

**Prerequisites**: Omar's n8n instance operational, API key configured

**Test Cases**:

| Test | Tool | Operation | Expected Behavior |
|------|------|-----------|-------------------|
| **Create Workflow** | `n8n_create_workflow` | Create simple webhook → HTTP workflow | Workflow created, ID returned |
| **Get Workflow** | `n8n_get_workflow` | Retrieve created workflow by ID | Workflow JSON returned |
| **List Workflows** | `n8n_list_workflows` | List all workflows | Array of workflows (including test workflow) |
| **Update Workflow** | `n8n_update_partial_workflow` | Update node position | Workflow updated successfully |
| **Validate Workflow** | `n8n_validate_workflow` | Validate workflow by ID | Validation report (pass/fail + details) |
| **Trigger Workflow** | `n8n_trigger_webhook_workflow` | Trigger via webhook URL | Workflow executed, execution ID returned |
| **Get Execution** | `n8n_get_execution` | Retrieve execution by ID | Execution details with status |
| **Delete Workflow** | `n8n_delete_workflow` | Delete test workflow | Workflow deleted successfully |

**Success Criteria**: All 8 operations complete without errors, workflows visible in n8n UI

---

### 6.5 FastMCP Gateway Integration

**Objective**: Confirm AI agents can reach N8N MCP via George's gateway

**Test Method**: End-to-end test from Claude Desktop

**Prerequisites**: FastMCP gateway configured (George Kim)

**Test Procedure**:

1. **Configure Claude Desktop**
   - Add N8N MCP server to Claude Desktop config via fastMCP gateway
   - Restart Claude Desktop

2. **Test Tool Discovery**
   - Ask Claude: "What n8n-mcp tools are available?"
   - Expected: Claude lists 40+ N8N MCP tools

3. **Test Documentation Tool**
   - Ask Claude: "Show me the properties of the Slack node in n8n"
   - Expected: Claude uses `get_node_essentials` tool and returns Slack node properties

4. **Test Template Search**
   - Ask Claude: "Find simple workflow templates for Slack notifications"
   - Expected: Claude uses `search_templates_by_metadata` and returns relevant templates

5. **Test Workflow Creation** (if N8N API configured)
   - Ask Claude: "Create a workflow that sends a Slack message when a webhook is triggered"
   - Expected: Claude uses `n8n_create_workflow` and returns workflow ID

**Success Criteria**: All 5 tests pass, Claude can successfully invoke N8N MCP tools via fastMCP gateway

---

### 6.6 Performance Benchmarks

**Objective**: Validate average MCP tool response time <50ms (target: ~12ms)

**Test Method**: Performance test suite (Apache Bench or custom script)

**Test Scenarios**:

| Test | Tool | Concurrency | Requests | Target Avg Response Time |
|------|------|-------------|----------|--------------------------|
| **Node List** | `list_nodes` | 1 | 100 | <20ms |
| **Node Search** | `search_nodes` | 5 | 500 | <30ms |
| **Node Essentials** | `get_node_essentials` | 10 | 1000 | <50ms |
| **Template Search** | `search_templates` | 5 | 500 | <100ms |
| **Sustained Load** | Mixed tools | 10 | 10,000 | <50ms average |

**Success Criteria**: All tests meet target response times, no errors under load

---

## 7. Risk Analysis

### 7.1 Technical Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **SQLite Database Corruption** | Low | High | Regular backups, use better-sqlite3 (not sql.js), implement database integrity checks |
| **Node Documentation Out of Sync** | Medium | Medium | Automated database rebuild on n8n version updates, version tracking in database |
| **N8N API Breaking Changes** | Medium | High | Pin n8n version, test API integration before updates, maintain compatibility layer |
| **Memory Leak (sql.js)** | Low | High | Use better-sqlite3 by default (Docker default in v2.20.2+), monitor memory usage |
| **MCP Protocol Changes** | Low | High | Pin @modelcontextprotocol/sdk version, monitor MCP spec updates, regression testing |

### 7.2 Integration Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **N8N Instance Unavailable** | Medium | High | Deploy N8N MCP in "documentation-only" mode first, graceful degradation if API unreachable |
| **FastMCP Gateway Misconfiguration** | Medium | Medium | Test N8N MCP standalone (stdio mode) first, coordinate closely with George Kim |
| **Network Connectivity Issues** | Low | Medium | Implement retry logic for n8n API calls, health checks for dependencies |
| **SSL Certificate Expiry** | Low | Medium | Document renewal procedure in runbook, set up expiry monitoring (future) |

### 7.3 Operational Risks

| Risk | Probability | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Systemd Service Fails to Start** | Low | High | Comprehensive pre-flight checks, detailed error logging, rollback procedure in runbook |
| **Disk Space Exhaustion** | Low | Medium | Monitor /opt/n8n-mcp/ disk usage, implement log rotation, database size limits |
| **Template Library Outdated** | Medium | Low | Scheduled database rebuilds (monthly), document manual rebuild procedure |
| **Insufficient Documentation** | Medium | Medium | Comprehensive runbook, MCP tool catalog, integration guides, coordination with Julia (QA) |

---

## 8. SOLID Principles Application

Per `/srv/cc/Governance/0.0-governance/0.0.3-Development/development-and-coding-standards.md`, all work must adhere to SOLID principles:

### 8.1 Single Responsibility Principle (SRP)

**Application to N8N MCP Deployment**:

- ✅ **N8N MCP Server**: Single responsibility = Expose n8n node documentation and workflow management via MCP protocol
- ✅ **Olivia Chang (this agent)**: Single responsibility = Deploy and maintain N8N MCP server infrastructure
- ✅ **Omar Rodriguez**: Single responsibility = Deploy and maintain n8n workflow execution instance
- ❌ **Anti-pattern avoided**: Olivia does NOT deploy n8n instance (that's Omar's job)
- ❌ **Anti-pattern avoided**: Olivia does NOT manage fastMCP gateway (that's George's job)

**Code-Level SRP**:

```typescript
// ✅ GOOD: N8N MCP server has single responsibility
class N8NMCPServer {
  // ONLY handles MCP protocol and tool routing
  async handleMCPRequest(request: MCPRequest): Promise<MCPResponse> {
    return this.toolRouter.route(request);
  }
}

// ✅ GOOD: Separate classes for data access
class NodeDocumentationRepository {
  // ONLY handles node documentation database queries
  async getNodeInfo(nodeType: string): Promise<NodeInfo> {
    return this.db.query('SELECT * FROM n8n_nodes WHERE type = ?', [nodeType]);
  }
}

// ✅ GOOD: Separate class for n8n API integration
class N8NAPIClient {
  // ONLY handles n8n API communication
  async createWorkflow(workflow: Workflow): Promise<string> {
    return this.httpClient.post('/workflows', workflow);
  }
}

// ❌ BAD: Multiple responsibilities in one class (AVOID THIS)
class N8NMCPServerWithEverything {
  // BAD: MCP protocol handling
  async handleMCPRequest() { /* ... */ }

  // BAD: Database access (should be separate repository)
  async getNodeFromDB() { /* ... */ }

  // BAD: n8n API calls (should be separate client)
  async createWorkflowInN8N() { /* ... */ }

  // BAD: fastMCP registration (should be separate service)
  async registerWithFastMCP() { /* ... */ }
}
```

---

### 8.2 Open-Closed Principle (OCP)

**Application to N8N MCP Deployment**:

- ✅ **Extensible Tool System**: New MCP tools can be added without modifying existing tool code
- ✅ **Plugin Architecture**: Template sources can be extended (n8n gallery, custom templates) without core changes
- ✅ **Configuration-Driven**: Environment variables allow behavior changes without code modifications

**Code-Level OCP**:

```typescript
// ✅ GOOD: Open for extension via interfaces
interface MCPTool {
  name: string;
  execute(params: any): Promise<any>;
}

// Existing tool (closed for modification)
class ListNodesTool implements MCPTool {
  name = 'list_nodes';
  async execute(params: any) { /* ... */ }
}

// NEW tool (extension, no modification to existing code)
class GetNodeDocumentationTool implements MCPTool {
  name = 'get_node_documentation';
  async execute(params: any) { /* ... */ }
}

// Tool router (open for extension)
class MCPToolRouter {
  private tools: MCPTool[] = [];

  registerTool(tool: MCPTool) {
    this.tools.push(tool); // Add new tools without modifying router
  }

  route(request: MCPRequest): Promise<MCPResponse> {
    const tool = this.tools.find(t => t.name === request.tool);
    return tool.execute(request.params);
  }
}
```

---

### 8.3 Liskov Substitution Principle (LSP)

**Application to N8N MCP Deployment**:

- ✅ **Database Adapters**: better-sqlite3 and sql.js adapters are interchangeable (both implement SQLite interface)
- ✅ **MCP Transport**: stdio and HTTP transports are substitutable without breaking clients
- ✅ **N8N API Clients**: Real and mock n8n API clients can be swapped for testing

**Code-Level LSP**:

```typescript
// ✅ GOOD: Base interface honored by all implementations
interface DatabaseAdapter {
  query(sql: string, params: any[]): Promise<any[]>;
  close(): Promise<void>;
}

// Implementation 1: better-sqlite3 (default)
class BetterSQLite3Adapter implements DatabaseAdapter {
  async query(sql: string, params: any[]) {
    return this.db.prepare(sql).all(params);
  }

  async close() {
    this.db.close();
  }
}

// Implementation 2: sql.js (fallback)
class SQLJSAdapter implements DatabaseAdapter {
  async query(sql: string, params: any[]) {
    return this.db.exec(sql, params)[0].values;
  }

  async close() {
    await this.saveToFile();
  }
}

// ✅ GOOD: Client code works with EITHER adapter
class NodeDocumentationRepository {
  constructor(private db: DatabaseAdapter) {}

  async getNodeInfo(nodeType: string) {
    // Works with BetterSQLite3Adapter OR SQLJSAdapter
    return this.db.query('SELECT * FROM n8n_nodes WHERE type = ?', [nodeType]);
  }
}
```

---

### 8.4 Interface Segregation Principle (ISP)

**Application to N8N MCP Deployment**:

- ✅ **Focused MCP Tools**: Each tool has specific interface (not fat interface forcing unused methods)
- ✅ **Database Interfaces**: Read-only vs. read-write interfaces segregated
- ✅ **N8N API Interfaces**: Workflow management vs. execution management separated

**Code-Level ISP**:

```typescript
// ✅ GOOD: Segregated interfaces (clients only implement what they need)

// Interface 1: Read-only node documentation
interface NodeDocumentationReader {
  getNodeInfo(nodeType: string): Promise<NodeInfo>;
  searchNodes(query: string): Promise<NodeInfo[]>;
}

// Interface 2: Template access (separate concern)
interface TemplateReader {
  getTemplate(templateId: string): Promise<Template>;
  searchTemplates(query: string): Promise<Template[]>;
}

// Interface 3: N8N workflow management (separate concern)
interface WorkflowManager {
  createWorkflow(workflow: Workflow): Promise<string>;
  updateWorkflow(id: string, workflow: Workflow): Promise<void>;
  deleteWorkflow(id: string): Promise<void>;
}

// ❌ BAD: Fat interface (forces implementations to provide everything)
interface N8NMCPService {
  // Node documentation
  getNodeInfo(): Promise<NodeInfo>;
  searchNodes(): Promise<NodeInfo[]>;

  // Templates
  getTemplate(): Promise<Template>;
  searchTemplates(): Promise<Template[]>;

  // Workflows
  createWorkflow(): Promise<string>;
  updateWorkflow(): Promise<void>;
  deleteWorkflow(): Promise<void>;

  // Executions
  triggerWorkflow(): Promise<string>;
  getExecution(): Promise<Execution>;

  // This class forces ALL implementations to provide ALL methods!
}
```

---

### 8.5 Dependency Inversion Principle (DIP)

**Application to N8N MCP Deployment**:

- ✅ **MCP Server depends on abstractions**: Database interface, not concrete SQLite implementation
- ✅ **N8N API integration depends on abstractions**: HTTP client interface, not concrete axios
- ✅ **Configuration-driven dependencies**: Environment variables inject dependencies at runtime

**Code-Level DIP**:

```typescript
// ✅ GOOD: Depend on abstractions (interfaces), not concrete classes

// High-level module (MCP server)
class N8NMCPServer {
  constructor(
    private nodeRepo: NodeDocumentationReader,    // Abstraction
    private templateRepo: TemplateReader,         // Abstraction
    private n8nClient: WorkflowManager | null     // Abstraction (optional)
  ) {}

  async handleListNodes() {
    return this.nodeRepo.searchNodes(''); // Uses abstraction
  }

  async handleCreateWorkflow(workflow: Workflow) {
    if (!this.n8nClient) {
      throw new Error('N8N API not configured');
    }
    return this.n8nClient.createWorkflow(workflow); // Uses abstraction
  }
}

// Dependency injection at runtime (configuration-driven)
const dbAdapter = new BetterSQLite3Adapter('/opt/n8n-mcp/data/n8n-nodes.db');
const nodeRepo = new NodeDocumentationRepository(dbAdapter);
const templateRepo = new TemplateRepository(dbAdapter);
const n8nClient = process.env.N8N_API_KEY
  ? new N8NAPIClient(process.env.N8N_API_URL, process.env.N8N_API_KEY)
  : null;

const mcpServer = new N8NMCPServer(nodeRepo, templateRepo, n8nClient);

// ❌ BAD: Depend on concrete classes (hardcoded)
class N8NMCPServerBad {
  constructor() {
    // BAD: Hardcoded concrete dependencies
    this.db = new BetterSQLite3Adapter('/opt/n8n-mcp/data/n8n-nodes.db');
    this.nodeRepo = new NodeDocumentationRepository(this.db);
    this.n8nClient = new N8NAPIClient('https://hx-n8n-server.hx.dev.local', 'api-key');
  }

  // Cannot swap implementations, cannot test with mocks!
}
```

---

## 9. Coordination Protocol

### 9.1 Handoff TO Other Agents

**When I need help from other agents, I will provide**:

#### To Omar Rodriguez (N8N Workflow Worker)

```markdown
@agent-omar

I'm deploying the N8N MCP server and need your n8n instance operational to enable workflow management tools.

Current Status:
- Task: N8N MCP Server deployment on hx-n8n-mcp-server (192.168.10.217)
- Progress: MCP server deployed, documentation tools working (Day 2 complete)
- Blocker: Need n8n API access to enable workflow management tools

Request:
- Action: Provide N8N API URL and API key
- Scope: Read-write access for workflow management (create, update, delete, execute)
- Outcome: N8N_API_URL and N8N_API_KEY environment variables

Context:
- Service: N8N MCP Server (exposes n8n capabilities to AI agents)
- Environment: hx-n8n-mcp-server.hx.dev.local (192.168.10.217)
- Dependencies: Your n8n instance at hx-n8n-server.hx.dev.local (192.168.10.215)
- Timeline: Need by Day 3 to enable workflow management tools

Success Criteria:
- N8N instance accessible at https://hx-n8n-server.hx.dev.local
- API key with full workflow management permissions
- API tested with curl: `curl -H "X-N8N-API-KEY: <key>" https://hx-n8n-server.hx.dev.local/api/v1/workflows`

Handoff Back:
- I will: Configure N8N_API_URL and N8N_API_KEY in /opt/n8n-mcp/.env
- I need: Confirmation API key is valid and has correct permissions
- Verify via: Test workflow creation via n8n_create_workflow MCP tool

I'll proceed with: Testing workflow management tools (Day 3)
```

#### To George Kim (FastMCP Gateway)

```markdown
@agent-george

I've deployed N8N MCP server and need to register it with your fastMCP gateway for AI agent access.

Current Status:
- Task: N8N MCP Server deployment on hx-n8n-mcp-server (192.168.10.217)
- Progress: MCP server operational, 40+ tools available (Day 3 in progress)
- Blocker: Need MCP server registered with fastMCP gateway

Request:
- Action: Register N8N MCP server with fastMCP gateway
- Scope: Route MCP requests from AI agents to N8N MCP server
- Outcome: AI agents (Claude Desktop, etc.) can access N8N MCP tools via gateway

Context:
- Service: N8N MCP Server
- Endpoint: hx-n8n-mcp-server.hx.dev.local (stdio mode currently, can switch to HTTP if needed)
- Purpose: Provide AI agents with n8n node documentation and workflow management capabilities
- Timeline: Need by Day 3 to enable end-to-end testing

Success Criteria:
- N8N MCP server registered in fastMCP gateway configuration
- Claude Desktop can discover N8N MCP tools via gateway
- Test query successful: "What n8n-mcp tools are available?" returns 40+ tools

Handoff Back:
- I will: Test MCP tools via Claude Desktop connected to fastMCP gateway
- I need: Gateway configuration details (URL, auth if needed)
- Verify via: End-to-end test from Claude Desktop

I'll proceed with: End-to-end validation (Day 3)
```

---

### 9.2 Handoff FROM Other Agents

**When other agents hand off to me, I expect**:

#### From William Taylor (Ubuntu Server)

**Expected Handoff Package**:
```markdown
@agent-olivia

Server hx-n8n-mcp-server is provisioned and ready for N8N MCP deployment.

Completed:
- Ubuntu 24.04 LTS installed
- Node.js 18.20.5 installed
- npm 10.8.2 installed
- systemd available and operational
- Network configured (SSH access on port 22)
- Domain joined to hx.dev.local

Deliverables:
- Server: hx-n8n-mcp-server.hx.dev.local (192.168.10.217)
- SSH access: ssh admin@hx-n8n-mcp-server.hx.dev.local
- Sudo access: Confirmed for admin user
- Node.js version: 18.20.5 (verified with `node --version`)
- npm version: 10.8.2 (verified with `npm --version`)

Verification:
- Logged in via SSH: ✅
- Ran `node --version`: ✅ 18.20.5
- Ran `npm --version`: ✅ 10.8.2
- Ran `systemctl --version`: ✅ systemd 255

You can now: Deploy N8N MCP application to /opt/n8n-mcp/
```

#### From Frank Lucas (Identity & Trust)

**Expected Handoff Package**:
```markdown
@agent-olivia

DNS record and SSL certificate for N8N MCP server are ready.

Completed:
- DNS record created: n8n-mcp.hx.dev.local → 192.168.10.217
- SSL certificate generated from Samba CA
- Certificate deployed to hx-n8n-mcp-server

Deliverables:
- DNS record: n8n-mcp.hx.dev.local resolves to 192.168.10.217
- SSL certificate: /etc/ssl/certs/n8n-mcp.crt
- SSL private key: /etc/ssl/private/n8n-mcp.key (permissions 600, root:root)
- CA certificate: /etc/ssl/certs/ca.crt (Samba CA)

Verification:
- DNS query: `dig n8n-mcp.hx.dev.local` returns 192.168.10.217 ✅
- SSL files exist: `ls -la /etc/ssl/certs/n8n-mcp.crt` ✅
- Certificate valid: `openssl x509 -in /etc/ssl/certs/n8n-mcp.crt -noout -text` ✅

You can now: Configure HTTPS endpoint for N8N MCP server
```

---

## 10. Sign-Off Criteria

### 10.1 Technical Validation

**All criteria MUST be met before sign-off**:

- [ ] **N8N MCP Server Deployed**
  - [ ] Application installed at /opt/n8n-mcp/
  - [ ] SQLite database initialized with 536 nodes (15MB)
  - [ ] Systemd service configured and enabled
  - [ ] Service starts automatically on boot
  - [ ] Service restarts on failure

- [ ] **MCP Protocol Compliance**
  - [ ] MCP protocol handshake successful
  - [ ] 40+ MCP tools discoverable via `tools/list`
  - [ ] Tools execute without errors
  - [ ] JSON-RPC responses valid

- [ ] **Node Documentation Access**
  - [ ] All 536 nodes accessible via `list_nodes`
  - [ ] Node search returns relevant results
  - [ ] `get_node_essentials` returns 10-20 properties + examples
  - [ ] Node documentation parsed from n8n-docs (90% coverage)

- [ ] **Template Library Access**
  - [ ] 2,500+ templates accessible via `list_templates`
  - [ ] Template search returns relevant results
  - [ ] `get_template` returns complete workflow JSON
  - [ ] Metadata filtering works (complexity, setup time, services)

- [ ] **N8N API Integration** (if configured)
  - [ ] Workflow creation via `n8n_create_workflow` successful
  - [ ] Workflow retrieval via `n8n_get_workflow` successful
  - [ ] Workflow update via `n8n_update_partial_workflow` successful
  - [ ] Workflow execution via `n8n_trigger_webhook_workflow` successful
  - [ ] Execution retrieval via `n8n_get_execution` successful

- [ ] **FastMCP Gateway Integration**
  - [ ] N8N MCP server registered with fastMCP gateway
  - [ ] AI agents can discover N8N MCP tools via gateway
  - [ ] End-to-end test from Claude Desktop successful

- [ ] **Performance Benchmarks**
  - [ ] Average MCP tool response time <50ms
  - [ ] Sustained load test: 100 req/min for 10 minutes without errors
  - [ ] Memory usage stable (<200MB)

---

### 10.2 Documentation Validation

**All documentation MUST be complete and reviewed**:

- [ ] **MCP Tool Catalog** (`/srv/cc/Governance/0.4-service-operations/n8n-mcp-tool-catalog.md`)
  - [ ] All 40+ tools documented with descriptions
  - [ ] Parameters and return types specified
  - [ ] Usage examples provided
  - [ ] Reviewed by Julia Martinez (QA)

- [ ] **Configuration Guide** (`/srv/cc/Governance/0.4-service-operations/n8n-mcp-configuration.md`)
  - [ ] Environment variables documented
  - [ ] Systemd service configuration explained
  - [ ] MCP protocol settings detailed
  - [ ] Reviewed by William Taylor (Ubuntu Server)

- [ ] **Integration Documentation** (`/srv/cc/Governance/0.5-integrations/n8n-mcp-integration.md`)
  - [ ] Claude Desktop setup instructions
  - [ ] Claude Code setup instructions
  - [ ] Cursor IDE setup instructions
  - [ ] Windsurf IDE setup instructions
  - [ ] Reviewed by George Kim (FastMCP)

- [ ] **Runbook** (`/srv/cc/Governance/0.6-runbooks/n8n-mcp-operations.md`)
  - [ ] Start/stop procedures
  - [ ] Troubleshooting guide
  - [ ] Database rebuild procedure
  - [ ] Log rotation configuration
  - [ ] Reviewed by operations team

- [ ] **Credentials Updated** (`/srv/cc/Governance/0.2-credentials/hx-credentials.md`)
  - [ ] N8N MCP service account documented (if created)
  - [ ] N8N API key documented (from Omar)
  - [ ] Reviewed by Frank Lucas (Identity & Trust)

---

### 10.3 Agent Sign-Offs

**All dependent agents MUST sign off**:

- [ ] **Olivia Chang (N8N MCP Specialist)** - Primary owner
  - [ ] All technical validation complete
  - [ ] All documentation complete
  - [ ] Performance benchmarks met
  - [ ] **Sign-off date**: _________________

- [ ] **Omar Rodriguez (N8N Workflow Worker)** - N8N API integration validated
  - [ ] N8N API accessible from N8N MCP server
  - [ ] Workflow creation/management tested successfully
  - [ ] No impact to n8n instance performance
  - [ ] **Sign-off date**: _________________

- [ ] **George Kim (FastMCP Gateway)** - Gateway integration validated
  - [ ] N8N MCP server registered with fastMCP gateway
  - [ ] AI agents can access N8N MCP tools via gateway
  - [ ] MCP routing working correctly
  - [ ] **Sign-off date**: _________________

- [ ] **William Taylor (Ubuntu Server)** - Server infrastructure validated
  - [ ] Server stable and performant
  - [ ] Systemd service configured correctly
  - [ ] No OS-level issues
  - [ ] **Sign-off date**: _________________

- [ ] **Frank Lucas (Identity & Trust)** - DNS/SSL validated
  - [ ] DNS record resolving correctly
  - [ ] SSL certificate valid and trusted
  - [ ] No security concerns
  - [ ] **Sign-off date**: _________________

- [ ] **Julia Martinez (Testing & QA)** - Testing validated
  - [ ] All test cases passed
  - [ ] No critical bugs or issues
  - [ ] Documentation accurate and complete
  - [ ] **Sign-off date**: _________________

---

## Appendix A: MCP Tool Quick Reference

**Core Tools** (always available):

| Tool | Purpose | Example Input |
|------|---------|---------------|
| `list_nodes` | List all 536 n8n nodes | `{}` |
| `get_node_info` | Get comprehensive node metadata | `{nodeType: "n8n-nodes-base.slack"}` |
| `get_node_essentials` | Get 10-20 key properties + examples | `{nodeType: "n8n-nodes-base.httpRequest", includeExamples: true}` |
| `search_nodes` | Full-text search across nodes | `{query: "send email", includeExamples: true}` |
| `search_node_properties` | Find specific properties | `{nodeType: "n8n-nodes-base.slack", query: "auth"}` |
| `list_ai_tools` | List AI-capable nodes (263) | `{}` |

**Template Tools** (always available):

| Tool | Purpose | Example Input |
|------|---------|---------------|
| `list_templates` | Browse 2,500+ templates | `{}` |
| `search_templates` | Text search templates | `{query: "slack notification"}` |
| `search_templates_by_metadata` | Advanced filtering | `{complexity: "simple", maxSetupMinutes: 30}` |
| `get_template` | Get complete workflow JSON | `{templateId: "1234", mode: "full"}` |
| `list_node_templates` | Find templates using specific nodes | `{nodeTypes: ["n8n-nodes-base.slack"]}` |

**Validation Tools** (always available):

| Tool | Purpose | Example Input |
|------|---------|---------------|
| `validate_workflow` | Complete workflow validation | `{workflow: {...}}` |
| `validate_workflow_connections` | Check workflow structure | `{workflow: {...}}` |
| `validate_node_operation` | Validate node configuration | `{nodeType: "...", config: {...}, profile: "runtime"}` |
| `validate_node_minimal` | Quick required field check | `{nodeType: "...", config: {...}}` |

**N8N Management Tools** (requires N8N API key):

| Tool | Purpose | Example Input |
|------|---------|---------------|
| `n8n_create_workflow` | Create new workflow | `{name: "...", nodes: [...], connections: {...}}` |
| `n8n_get_workflow` | Get workflow by ID | `{id: "123"}` |
| `n8n_update_partial_workflow` | Update workflow (diff operations) | `{id: "123", operations: [...]}` |
| `n8n_trigger_webhook_workflow` | Trigger workflow via webhook | `{workflowId: "123", webhookPath: "..."}` |
| `n8n_get_execution` | Get execution details | `{id: "456"}` |
| `n8n_list_workflows` | List workflows with filtering | `{active: true}` |

---

## Appendix B: Environment Variable Reference

**Complete .env file for N8N MCP Server**:

```bash
# ============================================================================
# N8N MCP Server Configuration
# Server: hx-n8n-mcp-server.hx.dev.local (192.168.10.217)
# Environment: Development
# Created: 2025-11-07
# ============================================================================

# ----------------------------------------------------------------------------
# MCP Server Mode
# ----------------------------------------------------------------------------
MCP_MODE=stdio                    # stdio (Claude Desktop) or http (remote access)
LOG_LEVEL=info                    # error, warn, info, debug
DISABLE_CONSOLE_OUTPUT=false      # Set true for production (stdio mode only)

# ----------------------------------------------------------------------------
# N8N API Integration (Optional - Enables Workflow Management Tools)
# ----------------------------------------------------------------------------
N8N_API_URL=https://hx-n8n-server.hx.dev.local
N8N_API_KEY=<provided-by-omar-rodriguez>

# ----------------------------------------------------------------------------
# Database Configuration
# ----------------------------------------------------------------------------
DATABASE_PATH=/opt/n8n-mcp/data/n8n-nodes.db
SQLJS_SAVE_INTERVAL_MS=10000      # SQLite save interval (if using sql.js fallback)

# ----------------------------------------------------------------------------
# Security
# ----------------------------------------------------------------------------
WEBHOOK_SECURITY_MODE=strict      # strict (production) or moderate (local dev)

# ----------------------------------------------------------------------------
# Telemetry (Privacy)
# ----------------------------------------------------------------------------
N8N_MCP_TELEMETRY_DISABLED=true   # Disable anonymous usage statistics

# ----------------------------------------------------------------------------
# Performance
# ----------------------------------------------------------------------------
MAX_TEMPLATE_FETCH=100            # Max templates to fetch per request
CACHE_TTL_SECONDS=3600            # Template cache TTL (1 hour)
```

---

## Appendix C: Systemd Service File

**File**: `/etc/systemd/system/n8n-mcp.service`

```ini
[Unit]
Description=N8N MCP Server - Model Context Protocol for n8n Workflow Automation
Documentation=https://github.com/czlonkowski/n8n-mcp
After=network.target
Wants=network.target

[Service]
Type=simple
User=n8n-mcp
Group=n8n-mcp
WorkingDirectory=/opt/n8n-mcp
EnvironmentFile=/opt/n8n-mcp/.env
ExecStart=/usr/bin/node /opt/n8n-mcp/app/dist/mcp/index.js
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=n8n-mcp

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/n8n-mcp/data /opt/n8n-mcp/logs

# Resource limits
LimitNOFILE=4096
LimitNPROC=2048

[Install]
WantedBy=multi-user.target
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-07 | Agent Olivia Chang | Initial planning analysis for POC3 N8N MCP deployment |
| 1.1 | 2025-11-07 | Claude Code | **CodeRabbit Remediation**: Clarified SQLite vs PostgreSQL database architecture decision (lines 269, 275-291). Added explicit documentation distinguishing better-sqlite3 (primary) from sql.js (fallback). Added comprehensive rationale explaining why MCP server uses embedded SQLite for static reference data (node documentation, templates) instead of reusing n8n's PostgreSQL deployment (operational workflow data). Documented architectural separation, performance benefits, and deployment independence. Cross-referenced n8n-mcp source code (`src/database/database-adapter.ts`) and benchmark data (`tests/benchmarks/`). |

---

**Status**: Draft - Awaiting Review
**Next Steps**:
1. Review with @agent-zero (Universal PM Orchestrator)
2. Coordinate with dependent agents (Omar, George, William, Frank)
3. Begin Phase 3: Alignment Checkpoint
4. Proceed to Phase 4: Execution (pending go/no-go decision)

---

**Agent Olivia Chang**
N8N MCP Specialist
Hana-X AI Ecosystem
2025-11-07
