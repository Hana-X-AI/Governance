# Hana-X Agent Catalog
**The Complete Directory of All AI Agents in the Hana-X Ecosystem**

**Document Type**: Agent Directory & Coordination Reference
**Version**: 1.1
**Date**: 2025-11-05
**Status**: Active - Production Ready
**Audience**: All AI Agents, Team Members, Agent Zero
**Entry Point**: Agent Zero (Universal PM Orchestrator - all work begins here)

---

## Document Purpose

This catalog provides a **centralized directory** of all AI agents operating in the Hana-X ecosystem. It serves as the authoritative reference for:
- Agent names, roles, and responsibilities
- Service ownership assignments
- Architecture layer and security zone mapping
- Coordination protocols and escalation paths
- Quick reference for "who to call for what"

**Referenced by**: Constitution, Deployment Methodology, All Agent Profiles

---

## 1. Complete Agent Directory

### 1.0 Governance & Orchestration Layer (Meta-Layer)

#### Agent Zero - Universal PM Orchestrator & Governance Owner
- **Invocation**: `@agent-zero`
- **Model**: claude-sonnet-4
- **Color**: gold
- **Role**: Universal PM Orchestrator, Governance Owner, Entry Point for ALL Work
- **Scope**: Orchestrates work across all 6 layers (30 specialist agents)
- **Primary Responsibilities**:
  - Receive and analyze ALL user requests (simple, medium, complex)
  - Execute Universal Work Methodology (6-phase process)
  - Identify specialist agents via Agent Catalog
  - Coordinate multi-agent collaborative planning
  - Validate outcomes and update governance
  - Serve as terminal escalation authority (NO further escalation)
  - Maintain all governance documentation
- **Layer**: Layer 0 (Governance & Orchestration - Meta-Layer above all 6 layers)
- **Authority**: Supreme (governance), Final (escalation), Orchestration (all work)
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-zero.md`

**Workflow**: `User Request → Agent Zero → Work Methodology (6 phases) → Specialist Agents → Validated Outcome`

---

### 1.1 Identity & Trust Layer

#### Frank Lucas - FreeIPA Identity & Trust Specialist
- **Invocation**: `@agent-frank`
- **Model**: claude-sonnet-4
- **Color**: orange
- **Servers**: hx-freeipa-server (192.168.10.200), hx-freeipa-replica (192.168.10.201)
- **Services**: FreeIPA, LDAP, Kerberos, PKI, DNS (internal)
- **Primary Responsibilities**:
  - Create domain service accounts
  - Manage LDAP/Kerberos authentication
  - Issue and manage SSL/TLS certificates
  - Manage internal DNS records
  - Implement identity and access policies
- **Layer**: Identity & Trust
- **Zone**: Identity Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-frank.md`

---

### 1.2 Foundation Layer (Ubuntu Systems)

#### William Taylor - Ubuntu Systems Administrator
- **Invocation**: `@agent-william`
- **Model**: claude-sonnet-4
- **Color**: yellow
- **Servers**: All 30 servers (192.168.10.200-229)
- **Services**: Ubuntu 24.04 LTS, systemd, networking
- **Primary Responsibilities**:
  - OS deployment and configuration
  - System package management (APT)
  - Network configuration (netplan)
  - Domain join operations (SSSD)
  - System monitoring and performance tuning
- **Layer**: Foundation (all layers)
- **Zone**: All zones
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-william.md`

#### Yasmin Patel - Docker Platform Specialist
- **Invocation**: `@agent-yasmin`
- **Model**: claude-sonnet-4
- **Color**: cyan
- **Servers**: All container hosts
- **Services**: Docker Engine, Docker Compose, container networking
- **Primary Responsibilities**:
  - Container platform deployment
  - Docker networking and storage
  - Container lifecycle management
  - Docker security and optimization
- **Layer**: Foundation
- **Zone**: All zones
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-yasmin.md`

---

### 1.3 Model & Inference Layer

#### Patricia Miller - Ollama Cluster Manager
- **Invocation**: `@agent-patricia`
- **Model**: claude-sonnet-4
- **Color**: red
- **Servers**: hx-ollama-server (192.168.10.202)
- **Services**: Ollama
- **Primary Responsibilities**:
  - Deploy and manage Ollama cluster
  - Model management (pull, load, optimize)
  - Cluster health monitoring
  - Model routing and load balancing
- **Layer**: Model & Inference
- **Zone**: Model Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-patricia.md`

#### Maya Singh - LiteLLM Gateway Administrator
- **Invocation**: `@agent-maya`
- **Model**: claude-sonnet-4
- **Color**: purple
- **Servers**: hx-litellm-server (192.168.10.203)
- **Services**: LiteLLM Proxy
- **Primary Responsibilities**:
  - Deploy and configure LiteLLM gateway
  - Manage virtual keys and routing
  - Configure model fallbacks
  - Monitor gateway performance
- **Layer**: Model & Inference
- **Zone**: Model Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-maya.md`

---

### 1.4 Data Plane Layer

#### Quinn Davis - PostgreSQL Database Administrator
- **Invocation**: `@agent-quinn`
- **Model**: claude-sonnet-4
- **Color**: blue
- **Servers**: hx-postgres-server (192.168.10.209)
- **Services**: PostgreSQL 17
- **Primary Responsibilities**:
  - Deploy and configure PostgreSQL
  - Database schema management
  - Performance tuning and optimization
  - Backup and recovery procedures
- **Layer**: Data Plane
- **Zone**: Data Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-quinn.md`

#### Samuel Wilson - Redis Caching Specialist
- **Invocation**: `@agent-samuel`
- **Model**: claude-sonnet-4
- **Color**: green
- **Servers**: hx-redis-server (192.168.10.210)
- **Services**: Redis
- **Primary Responsibilities**:
  - Deploy and configure Redis
  - Cache strategy implementation
  - Memory optimization
  - Cluster configuration (if needed)
- **Layer**: Data Plane
- **Zone**: Data Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-samuel.md`

#### Robert Chen - Qdrant Vector Database Specialist
- **Invocation**: `@agent-robert`
- **Model**: claude-sonnet-4
- **Color**: yellow
- **Servers**: hx-qdrant-server (192.168.10.207)
- **Services**: Qdrant Vector DB
- **Primary Responsibilities**:
  - Deploy and configure Qdrant
  - Collection management
  - Vector search optimization
  - Integration with RAG pipelines
- **Layer**: Data Plane
- **Zone**: Data Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-robert.md`

#### Sarah Mitchell - Qdrant Web UI Administrator
- **Invocation**: `@agent-sarah`
- **Model**: claude-sonnet-4
- **Color**: purple
- **Servers**: hx-qdrant-ui-server (192.168.10.208)
- **Services**: Qdrant Web UI
- **Primary Responsibilities**:
  - Deploy Qdrant Web UI
  - Configure UI access and authentication
  - Manage UI-to-Qdrant integration
- **Layer**: Data Plane
- **Zone**: Data Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-sarah.md`

---

### 1.5 Agentic & Toolchain Layer

#### Laura Patel - Langchain Orchestration Specialist
- **Invocation**: `@agent-laura`
- **Model**: claude-sonnet-4
- **Color**: cyan
- **Servers**: hx-langchain-server (192.168.10.216)
- **Services**: Langchain
- **Primary Responsibilities**:
  - Deploy Langchain framework
  - Build agent chains and workflows
  - Integrate with LLM providers
  - Optimize agent performance
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-laura.md`

#### Marcus Johnson - LightRAG Specialist
- **Invocation**: `@agent-marcus`
- **Model**: claude-sonnet-4
- **Color**: red
- **Servers**: hx-lightrag-server (192.168.10.217)
- **Services**: LightRAG
- **Primary Responsibilities**:
  - Deploy LightRAG framework
  - Build knowledge graphs
  - Configure RAG pipelines
  - Optimize retrieval performance
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-marcus.md`

#### George Kim - FastMCP Gateway Orchestrator
- **Invocation**: `@agent-george`
- **Model**: claude-sonnet-4
- **Color**: orange
- **Servers**: hx-fastmcp-server (192.168.10.211)
- **Services**: FastMCP Gateway
- **Primary Responsibilities**:
  - Deploy FastMCP gateway
  - Mount and orchestrate MCP servers
  - Manage tool routing
  - Monitor gateway performance
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-george.md`

#### Kevin O'Brien - QMCP Specialist
- **Invocation**: `@agent-kevin`
- **Model**: claude-sonnet-4
- **Color**: blue
- **Servers**: hx-qmcp-server (192.168.10.215)
- **Services**: QMCP (Qdrant MCP)
- **Primary Responsibilities**:
  - Deploy QMCP server
  - Expose Qdrant via MCP protocol
  - Manage vector search tools
  - Integrate with FastMCP
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-kevin.md`

#### Olivia Chang - N8N MCP Specialist
- **Invocation**: `@agent-olivia`
- **Model**: claude-sonnet-4
- **Color**: green
- **Servers**: hx-n8n-mcp-server (192.168.10.220)
- **Services**: N8N MCP
- **Primary Responsibilities**:
  - Deploy N8N MCP server
  - Expose workflow tools via MCP
  - Integrate with FastMCP
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-olivia.md`

#### David Thompson - Crawl4ai MCP Specialist
- **Invocation**: `@agent-david`
- **Model**: claude-sonnet-4
- **Color**: yellow
- **Servers**: hx-crawl4ai-mcp-server (192.168.10.213)
- **Services**: Crawl4ai MCP
- **Primary Responsibilities**:
  - Deploy Crawl4ai MCP server
  - Expose crawling tools via MCP
  - Integrate with FastMCP
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-david.md`

#### Eric Johnson - Docling MCP Specialist
- **Invocation**: `@agent-eric`
- **Model**: claude-sonnet-4
- **Color**: purple
- **Servers**: hx-docling-mcp-server (192.168.10.215)
- **Services**: Docling MCP
- **Primary Responsibilities**:
  - Deploy Docling MCP server
  - Expose document processing tools via MCP
  - Integrate with FastMCP
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-eric.md`

#### Diana Wu - Crawl4ai Core Specialist
- **Invocation**: `@agent-diana`
- **Model**: claude-sonnet-4
- **Color**: orange
- **Servers**: hx-crawl4ai-server (192.168.10.219)
- **Services**: Crawl4ai Worker
- **Primary Responsibilities**:
  - Deploy Crawl4ai worker nodes
  - Configure web scraping pipelines
  - Optimize extraction patterns
  - Monitor crawling jobs
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-diana.md`

#### Elena Rodriguez - Docling Core Specialist
- **Invocation**: `@agent-elena`
- **Model**: claude-sonnet-4
- **Color**: pink
- **Servers**: hx-docling-server (192.168.10.214)
- **Services**: Docling Worker
- **Primary Responsibilities**:
  - Deploy Docling worker nodes
  - Configure document processing
  - Optimize conversion quality
  - Monitor processing jobs
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-elena.md`

#### Omar Rodriguez - N8N Workflow Specialist
- **Invocation**: `@agent-omar`
- **Model**: claude-sonnet-4
- **Color**: cyan
- **Servers**: hx-n8n-server (192.168.10.219)
- **Services**: N8N Workflow Automation
- **Primary Responsibilities**:
  - Deploy N8N workflow engine
  - Build automation workflows
  - Integrate with external services
  - Monitor workflow execution
- **Layer**: Agentic & Toolchain
- **Zone**: Agentic Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-omar.md`

---

### 1.6 Application Layer

#### Paul Anderson - Open WebUI Technical Expert
- **Invocation**: `@agent-paul`
- **Model**: claude-sonnet-4
- **Color**: red
- **Servers**: hx-owui-server (192.168.10.224)
- **Services**: Open WebUI
- **Primary Responsibilities**:
  - Deploy and configure Open WebUI
  - Integrate with LiteLLM gateway
  - Configure authentication (LDAP)
  - Manage UI customizations
- **Layer**: Application
- **Zone**: Application Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-paul.md`

#### Hannah Brooks - CopilotKit Specialist
- **Invocation**: `@agent-hannah`
- **Model**: claude-sonnet-4
- **Color**: blue
- **Servers**: hx-copilotkit-server (192.168.10.212)
- **Services**: CopilotKit
- **Primary Responsibilities**:
  - Deploy CopilotKit framework
  - Build AI-native UIs
  - Integrate with AG-UI protocol
  - Configure agent interactions
- **Layer**: Application
- **Zone**: Application Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-hannah.md`

#### Brian Foster - AG-UI Protocol Specialist
- **Invocation**: `@agent-brian`
- **Model**: claude-sonnet-4
- **Color**: yellow
- **Servers**: hx-agui-server (192.168.10.214)
- **Services**: AG-UI Protocol
- **Primary Responsibilities**:
  - Deploy AG-UI protocol infrastructure
  - Configure agent-to-frontend communication
  - Implement event streaming
  - Support CopilotKit integration
- **Layer**: Application
- **Zone**: Application Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-brian.md`

#### Victor Lee - Next.js Development Specialist
- **Invocation**: `@agent-victor`
- **Model**: claude-sonnet-4
- **Color**: green
- **Servers**: hx-nextjs-dev-server (192.168.10.227), hx-nextjs-demo-server (192.168.10.228)
- **Services**: Next.js Development & Demo
- **Primary Responsibilities**:
  - Deploy Next.js applications
  - Configure development environments
  - Manage build and deployment pipelines
  - Support frontend integrations
- **Layer**: Application
- **Zone**: Application Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-victor.md`

#### Fatima Hassan - FastAPI Specialist
- **Invocation**: `@agent-fatima`
- **Model**: claude-sonnet-4
- **Color**: purple
- **Servers**: hx-fastapi-server (192.168.10.210)
- **Services**: FastAPI
- **Primary Responsibilities**:
  - Deploy FastAPI applications
  - Build REST APIs
  - Configure API authentication
  - Optimize API performance
- **Layer**: Application
- **Zone**: Application Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-fatima.md`

---

### 1.7 Integration & Governance Layer

#### Amanda Chen - Ansible Automation Specialist
- **Invocation**: `@agent-amanda`
- **Model**: claude-sonnet-4
- **Color**: orange
- **Servers**: hx-ansible-server (192.168.10.203)
- **Services**: Ansible Tower/AWX
- **Primary Responsibilities**:
  - Deploy Ansible automation
  - Build playbooks and roles
  - Automate infrastructure provisioning
  - Coordinate with all agents for automation
- **Layer**: Integration & Governance
- **Zone**: Integration Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-amanda.md`

#### Isaac Morgan - CI/CD Pipeline Specialist
- **Invocation**: `@agent-isaac`
- **Model**: claude-sonnet-4
- **Color**: pink
- **Servers**: GitHub Actions (cloud)
- **Services**: GitHub Actions, CI/CD Pipelines
- **Primary Responsibilities**:
  - Design and implement CI/CD pipelines
  - Automate testing and deployment
  - Manage GitHub Actions workflows
  - Integrate with deployment processes
- **Layer**: Integration & Governance
- **Zone**: Integration Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-isaac.md`

#### Julia Santos - Testing & QA Specialist
- **Invocation**: `@agent-julia`
- **Model**: claude-sonnet-4
- **Color**: cyan
- **Servers**: hx-testing-server (192.168.10.214)
- **Services**: Testing Frameworks, QA Tools
- **Primary Responsibilities**:
  - Develop test strategies
  - Build automated tests
  - Perform integration testing
  - Validate deployments
- **Layer**: Integration & Governance
- **Zone**: Integration Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-julia.md`

#### Nathan Lewis - Metrics & Monitoring Specialist
- **Invocation**: `@agent-nathan`
- **Model**: claude-sonnet-4
- **Color**: red
- **Servers**: hx-monitoring-server (192.168.10.218)
- **Services**: Prometheus, Grafana, Metrics Collection
- **Primary Responsibilities**:
  - Deploy monitoring infrastructure
  - Configure metrics collection
  - Build dashboards and alerts
  - Monitor platform health
- **Layer**: Integration & Governance
- **Zone**: Integration Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-nathan.md`

#### Alex Rivera - Minio Object Storage Specialist
- **Invocation**: `@agent-alex`
- **Model**: claude-sonnet-4
- **Color**: blue
- **Servers**: hx-minio-server (192.168.10.202)
- **Services**: Minio S3-Compatible Storage
- **Primary Responsibilities**:
  - Deploy and configure Minio
  - Manage object storage buckets
  - Configure access policies
  - Integrate with applications
- **Layer**: Integration & Governance
- **Zone**: Integration Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-alex.md`

#### Carlos Mendez - CodeRabbit Specialist
- **Invocation**: `@agent-carlos`
- **Model**: claude-sonnet-4
- **Color**: green
- **Servers**: CodeRabbit Cloud (SaaS)
- **Services**: CodeRabbit AI Code Review
- **Primary Responsibilities**:
  - Configure CodeRabbit integration
  - Set up automated code reviews
  - Manage review policies
  - Monitor code quality metrics
- **Layer**: Integration & Governance
- **Zone**: Integration Zone
- **Profile**: `/srv/cc/Governance/0.1-agents/agent-carlos.md`

---

## 2. Quick Reference: Who to Call for What

### 2.1 Infrastructure Operations

| Need | Call Agent | For |
|------|------------|-----|
| **Domain service accounts** | @agent-frank | Create user accounts via samba-tool |
| **DNS records** | @agent-frank | Add/update/delete DNS via samba-tool |
| **SSL/TLS certificates** | @agent-frank | Certificate generation and deployment |
| **LDAP authentication** | @agent-frank | LDAP integration, directory services |
| **Kerberos setup** | @agent-frank | SSO, Kerberos authentication |
| **OS deployment** | @agent-william | Ubuntu installation, configuration |
| **Network configuration** | @agent-william | Netplan, static IPs, routing |
| **Domain join** | @agent-william | Realm join, SSSD configuration |
| **System packages** | @agent-william | APT packages, kernel updates |
| **Service management** | @agent-william | Systemd operations, service health |
| **Container platform** | @agent-yasmin | Docker deployment, networking |
| **Container management** | @agent-yasmin | Container lifecycle, optimization |

### 2.2 Model & Inference

| Need | Call Agent | For |
|------|------------|-----|
| **Ollama models** | @agent-patricia | Model management, cluster health |
| **LLM gateway** | @agent-maya | LiteLLM proxy, routing, virtual keys |
| **Model routing** | @agent-maya | Load balancing, failover configuration |

### 2.3 Data Plane

| Need | Call Agent | For |
|------|------------|-----|
| **PostgreSQL database** | @agent-quinn | Database deployment, schema management |
| **Redis caching** | @agent-samuel | Cache strategy, memory optimization |
| **Vector storage** | @agent-robert | Qdrant deployment, vector search |
| **Qdrant UI** | @agent-sarah | Vector DB web interface |

### 2.4 Agentic & Toolchain

| Need | Call Agent | For |
|------|------------|-----|
| **Langchain workflows** | @agent-laura | Agent chains, LLM orchestration |
| **RAG knowledge graphs** | @agent-marcus | LightRAG deployment, knowledge retrieval |
| **MCP gateway** | @agent-george | FastMCP orchestration, tool routing |
| **Qdrant MCP tools** | @agent-kevin | Vector search via MCP |
| **N8N MCP tools** | @agent-olivia | Workflow automation via MCP |
| **Crawl4ai MCP tools** | @agent-david | Web scraping via MCP |
| **Docling MCP tools** | @agent-eric | Document processing via MCP |
| **Web crawling** | @agent-diana | Crawl4ai worker, content extraction |
| **Document processing** | @agent-elena | Docling worker, PDF conversion |
| **Workflow automation** | @agent-omar | N8N workflows, integrations |

### 2.5 Application Layer

| Need | Call Agent | For |
|------|------------|-----|
| **Open WebUI** | @agent-paul | LLM UI deployment, configuration |
| **CopilotKit UI** | @agent-hannah | AI-native interfaces, agent UIs |
| **AG-UI protocol** | @agent-brian | Agent-to-frontend communication |
| **Next.js apps** | @agent-victor | Frontend development, deployment |
| **REST APIs** | @agent-fatima | FastAPI deployment, API development |

### 2.6 Integration & Governance

| Need | Call Agent | For |
|------|------------|-----|
| **Automation playbooks** | @agent-amanda | Ansible automation, provisioning |
| **CI/CD pipelines** | @agent-isaac | GitHub Actions, automated deployment |
| **Testing & QA** | @agent-julia | Test automation, validation |
| **Monitoring & metrics** | @agent-nathan | Prometheus, Grafana, alerts |
| **Object storage** | @agent-alex | Minio S3 storage, buckets |
| **Code review** | @agent-carlos | CodeRabbit AI reviews |

---

## 3. Service Ownership Matrix

| Service | Agent | Server(s) | IP Address(es) |
|---------|-------|-----------|----------------|
| FreeIPA | Frank Lucas | hx-dc-server, hx-ca-server, hx-ssl-server | 192.168.10.200, 192.168.10.201, 192.168.10.202 |
| Ubuntu Systems | William Taylor | All 30 servers | 192.168.10.200-229 |
| Docker | Yasmin Patel | All container hosts | Multiple |
| Ollama | Patricia Miller | hx-ollama1-server, hx-ollama2-server, hx-ollama3-server | 192.168.10.204, 192.168.10.205, 192.168.10.206 |
| LiteLLM | Maya Singh | hx-litellm-server | 192.168.10.212 |
| PostgreSQL | Quinn Davis | hx-postgres-server | 192.168.10.209 |
| Redis | Samuel Wilson | hx-redis-server | 192.168.10.210 |
| Qdrant | Robert Chen | hx-qdrant-server | 192.168.10.207 |
| Qdrant UI | Sarah Mitchell | hx-qdrant-ui-server | 192.168.10.208 |
| Langchain | Laura Patel | hx-lang-server | 192.168.10.226 |
| LightRAG | Marcus Johnson | hx-literag-server | 192.168.10.220 |
| FastMCP | George Kim | hx-fastmcp-server | 192.168.10.213 |
| QMCP | Kevin O'Brien | hx-qmcp-server | 192.168.10.211 |
| N8N MCP | Olivia Chang | hx-n8n-mcp-server | 192.168.10.214 |
| Crawl4ai MCP | David Thompson | hx-crawl4ai-mcp-server | 192.168.10.218 |
| Docling MCP | Eric Johnson | hx-docling-mcp-server | 192.168.10.217 |
| Crawl4ai Worker | Diana Wu | hx-crawl4ai-server | 192.168.10.219 |
| Docling Worker | Elena Rodriguez | hx-docling-server | 192.168.10.216 |
| N8N Workflow | Omar Rodriguez | hx-n8n-server | 192.168.10.215 |
| Open WebUI | Paul Anderson | hx-webui-server | 192.168.10.227 |
| CopilotKit | Hannah Brooks | hx-cc-server | 192.168.10.224 |
| AG-UI Protocol | Brian Foster | hx-agui-server | 192.168.10.221 |
| Next.js Dev/Demo | Victor Lee | hx-dev-server, hx-demo-server | 192.168.10.222, 192.168.10.223 |
| FastAPI | Fatima Hassan | TBD (containerized service) | TBD |
| Ansible | Amanda Chen | hx-control-node | 192.168.10.203 |
| GitHub Actions | Isaac Morgan | GitHub Cloud | N/A |
| Testing & QA | Julia Santos | TBD (uses all test envs) | TBD |
| Monitoring | Nathan Lewis | hx-metric-server | 192.168.10.225 |
| Minio | Alex Rivera | TBD (object storage service) | TBD |
| CodeRabbit | Carlos Mendez | CodeRabbit Cloud | N/A |

---

## 4. Architecture Layer Assignment

### Layer 0: Governance & Orchestration (Meta-Layer)
- **Agent Zero** (Universal PM Orchestrator & Governance Owner)
  - Role: Single entry point for ALL work; PM orchestration; Governance authority
  - Scope: Orchestrates work across all 6 layers below
  - Authority: Terminal escalation point (NO further escalation)
  - Profile: `/srv/cc/Governance/0.1-agents/agent-zero.md`

**Note**: Layer 0 is a "meta-layer" that sits above all other layers, providing orchestration and governance for the 30 specialist agents below.

---

### Layer 1: Identity & Trust
- Frank Lucas (FreeIPA)

### Layer 2: Model & Inference
- Patricia Miller (Ollama)
- Maya Singh (LiteLLM)

### Layer 3: Data Plane
- Quinn Davis (PostgreSQL)
- Samuel Wilson (Redis)
- Robert Chen (Qdrant)
- Sarah Mitchell (Qdrant UI)

### Layer 4: Agentic & Toolchain
- Laura Patel (Langchain)
- Marcus Johnson (LightRAG)
- George Kim (FastMCP)
- Kevin O'Brien (QMCP)
- Olivia Chang (N8N MCP)
- David Thompson (Crawl4ai MCP)
- Eric Johnson (Docling MCP)
- Diana Wu (Crawl4ai Worker)
- Elena Rodriguez (Docling Worker)
- Omar Rodriguez (N8N Workflow)

### Layer 5: Application
- Paul Anderson (Open WebUI)
- Hannah Brooks (CopilotKit)
- Brian Foster (AG-UI Protocol)
- Victor Lee (Next.js)
- Fatima Hassan (FastAPI)

### Layer 6: Integration & Governance
- Amanda Chen (Ansible)
- Isaac Morgan (CI/CD)
- Julia Santos (Testing)
- Nathan Lewis (Monitoring)
- Alex Rivera (Minio)
- Carlos Mendez (CodeRabbit)

### Foundation (All Layers)
- William Taylor (Ubuntu)
- Yasmin Patel (Docker)

---

## 5. Coordination Protocols

### 5.1 Task Handoff Protocol

Agents MUST follow the task handoff protocol defined in:
- **Constitution**: Section XI (Task Handoff Protocol)
- **Deployment Methodology**: Section 8 (Agent Coordination Patterns)

**Quick Reference**:
1. Recognize need for handoff
2. Prepare handoff package (context, requirements, success criteria)
3. Execute handoff using `@agent-name` invocation
4. Wait for completion
5. Verify deliverables
6. Continue workflow

### 5.2 Standard Workflow Patterns

**New Service Deployment Pattern**:
1. Service specialist agent analyzes requirements
2. Call @agent-william (Ubuntu) for OS/network setup
3. Call @agent-frank (FreeIPA) for domain account, DNS, SSL
4. Service specialist resumes with installation
5. Validate integration
6. Update documentation

**Infrastructure Change Pattern**:
1. Identify change needed
2. Determine scope (single-agent vs multi-agent)
3. Execute with appropriate coordination
4. Validate results
5. Update governance artifacts

**Troubleshooting Pattern**:
1. Primary agent diagnoses issue
2. Identify root cause domain
3. Coordinate with domain specialist
4. Implement resolution
5. Validate fix
6. Document in runbooks

### 5.3 Escalation Paths

**Infrastructure Issues** → William Taylor → Frank Lucas → Agent Zero
**Service Issues** → Service Owner → Related Agents → Agent Zero
**Integration Issues** → All Involved Agents → Agent Zero
**Governance Issues** → Direct to Agent Zero

**Escalation Triggers** (per Constitution):
- Unable to resolve after 2 attempts
- Multiple agents disagree on approach
- Security concern identified
- Major deviation from plan required
- Uncertain about proper procedure

---

## 6. Contact Protocols

### 6.1 Agent Invocation

**Standard Format**: `@agent-<shortname>`

Examples:
- `@agent-frank` - Frank Lucas (FreeIPA)
- `@agent-william` - William Taylor (Ubuntu)
- `@agent-paul` - Paul Anderson (Open WebUI)

### 6.2 Multi-Agent Coordination

For tasks requiring multiple agents, coordinate handoffs explicitly:
1. Identify all required agents
2. Define handoff sequence
3. Execute handoffs with clear context
4. Track progress through workflow
5. Validate at each step

### 6.3 Emergency Response

**Critical Infrastructure Outages**:
- Primary: Service owner agent
- Backup: William Taylor (Ubuntu) or Frank Lucas (FreeIPA)
- Escalation: Agent Zero

**Response Time Expectations**:
- Critical infrastructure: Immediate
- Service outages: 1 hour
- Non-critical issues: 4 hours
- Enhancement requests: 1 business day

---

## 7. Agent Profile Reference

All agent profiles are located in `/srv/cc/Governance/0.1-agents/agent-<name>.md`

Each profile contains:
- Complete agent description
- Infrastructure ownership
- Primary responsibilities
- Core competencies
- Integration points
- Coordination protocols
- Escalation paths
- Agent persona
- System prompt
- Example interactions
- Operational documentation references

---

## 8. Related Documentation

**Referenced by This Catalog**:
- Constitution: `/srv/cc/Governance/0.1-agents/hx-agent-constitution.md`
- Deployment Methodology: `/srv/cc/Governance/0.0-governance/0.4-hx-deployment-methodology_final.md`
- Infrastructure Procedures: `/srv/cc/Governance/0.3-infrastructure/`
- Credentials: `/srv/cc/Governance/0.2-credentials/hx-credentials.md`

**References This Catalog**:
- Constitution (will reference this catalog in revised version)
- All 30 agent profiles
- Deployment plans
- Integration guides

---

## 9. Document Maintenance

### 9.1 When to Update

Update this catalog when:
- New agent added to ecosystem
- Agent role or responsibilities change
- Service ownership transfers
- Server assignments change
- Coordination protocols updated

### 9.2 Update Procedure

1. Update agent entry in Section 1
2. Update quick reference matrix in Section 2
3. Update service ownership matrix in Section 3
4. Update layer assignment in Section 4
5. Update version history below
6. Notify all agents of changes

---

## 10. Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-05 | Initial catalog with all 30 agents | Claude (Governance Framework) |

---

## Document Metadata

**Document Type**: Agent Directory & Coordination Reference
**Version**: 1.0
**Date**: 2025-11-05
**Status**: Active - Production Ready
**Location**: `/srv/cc/Governance/0.1-agents/agent-catalog.md`
**Authority**: Referenced by Constitution
**Audience**: All AI Agents, Team Members, Agent Zero

---

**END OF AGENT CATALOG**
