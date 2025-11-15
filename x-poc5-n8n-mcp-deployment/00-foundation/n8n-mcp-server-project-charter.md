# Project Charter: n8n MCP Server Installation & Configuration

**Document Type**: Project Charter  
**Created**: November 10, 2025  
**Project Code**: HX-N8N-MCP-001  
**Classification**: Internal - Project Management  
**Status**: DRAFT - In Development  

---

## Summary

This project installs and configures the n8n MCP Server (hx-n8n-mcp-server at 192.168.10.214) to expose workflows from the operational n8n workflow automation instance (hx-n8n-server at 192.168.10.215) as standardized Model Context Protocol tools. The MCP server will translate incoming MCP requests from AI agents into n8n workflow executions, enabling the HANA-X 31-agent orchestration system to leverage n8n's 700+ application integrations as callable tools. This establishes n8n as the "hands" of the AI ecosystem—executing real-world actions across business systems—while preparing infrastructure for future integration with the LangGraph agent orchestrator (the "brain") when hx-lang-server (192.168.10.226) becomes operational.

The MCP server functions as a translation layer: AI agents make standardized MCP tool calls → MCP server receives and validates requests → corresponding n8n workflows execute → results return to calling agent through MCP protocol.

## Goals

1. **Operational MCP Integration**: Deploy a production-ready n8n MCP Server with complete package installation that reliably exposes designated n8n workflows as discoverable, callable MCP tools accessible to all HANA-X AI agents.

2. **Workflow-as-Tool Foundation**: Establish systematic patterns for defining n8n workflows as MCP tools, including proper metadata specification, parameter validation, error handling, and result formatting that meet MCP protocol standards.

3. **Quality-First Deployment**: Implement comprehensive testing and validation procedures ensuring 100% reliability in MCP request handling, workflow execution, and response delivery before declaring any workflow production-ready.

4. **Agent Integration Readiness**: Create clear integration patterns and documentation enabling current operational agents (Claude Code, other MCP-aware systems) to discover and invoke n8n workflows through both direct connections and FastMCP gateway routing, while establishing groundwork for future LangGraph orchestration.

## Objectives

1. **Complete MCP Server Installation & Configuration**: Install **full n8n MCP Server software stack** including all available MCP tools, packages, and dependencies on hx-n8n-mcp-server (192.168.10.214), configure authentication with hx-dc-server (192.168.10.200), establish TLS certificates from hx-ca-server (192.168.10.201), and verify **direct connectivity** to hx-n8n-server (192.168.10.215).

2. **Workflow Tool Registry**: Create an initial library of 3-5 foundational n8n workflows designed as MCP tools covering core capabilities (e.g., database query, external API call, file processing, notification dispatch), each with complete MCP metadata and parameter schemas. These workflows will validate the full MCP installation but represent only a subset of possible workflow tools.

3. **MCP Protocol Implementation**: Configure the MCP Server node within n8n to properly expose workflows with standardized tool definitions, implement request validation and error handling, and ensure response formatting meets MCP specification requirements.

4. **Testing & Validation Framework**: Develop systematic test procedures covering MCP discovery (tool listing), parameter validation, execution success paths, error handling, and timeout scenarios, achieving 100% pass rate across all test cases before production deployment.

5. **Dual Integration Pattern Implementation**: 
   - **Direct Connection**: Establish direct MCP protocol communication between n8n server (192.168.10.215) and n8n MCP server (192.168.10.214)
   - **FastMCP Gateway Integration**: Register n8n MCP server with hx-fastmcp-server (192.168.10.213) leveraging FastMCP's dual capability as both MCP server (for agent discovery) and MCP client (for routing to n8n MCP server), enabling unified tool discovery while supporting direct workflow execution paths

6. **Documentation & Standards**: Produce comprehensive technical documentation including: MCP server architecture, complete package inventory, workflow-to-tool design patterns, parameter schema standards, error handling conventions, direct connection vs. gateway routing patterns, troubleshooting procedures, and future LangGraph integration patterns (for when hx-lang-server becomes operational).

7. **Iterative Deployment Process**: Follow phased deployment methodology starting with single workflow validation, expanding to multi-workflow testing, conducting agent integration trials through both direct and gateway paths, and establishing systematic procedures for adding new workflow tools to the MCP registry.

## Scope

### In Scope

**Infrastructure & Installation**:
- **Complete installation** of n8n MCP Server software including:
  - All n8n MCP packages, tools, and dependencies
  - Full MCP protocol support libraries
  - All available n8n MCP integrations and extensions
  - Complete package inventory documentation
- Installation on hx-n8n-mcp-server (192.168.10.214)
- Domain join to hx.dev.local with Kerberos/LDAP authentication configuration
- TLS certificate acquisition from hx-ca-server (192.168.10.201) and SSL configuration
- **Direct network connectivity** validation between MCP server (.214) and n8n workflow server (.215)
- Service account creation and permission assignment via hx-dc-server (192.168.10.200)
- Port 8003 configuration and firewall rules (internal access only)

**MCP Protocol Implementation**:
- Configuration of MCP Server node within n8n for workflow exposure
- MCP tool definition schema development (metadata, parameters, response formats)
- Request validation and error handling implementation
- Response formatting to MCP specification standards
- Tool discovery endpoint configuration
- **Direct MCP protocol communication** between n8n server and n8n MCP server

**Initial Workflow Development**:
- Design and implementation of 3-5 foundational workflows as MCP tools (testing subset)
- Workflow categories: database operations, external API integration, file operations, notification systems
- Complete parameter schemas with type validation and required/optional field definitions
- Error handling patterns for workflow execution failures
- Success/failure response standardization
- **Note**: These workflows validate the complete MCP installation; many more workflows possible with installed packages

**Testing & Quality Assurance**:
- MCP discovery testing (tool listing and metadata verification)
- Parameter validation testing (required fields, type checking, boundary conditions)
- Execution path testing (success scenarios, error scenarios, timeout handling)
- **Direct connection testing** (n8n server → n8n MCP server → workflow execution)
- Integration testing via FastMCP gateway routing
- Integration testing with direct MCP client calls
- Load testing for concurrent workflow executions
- Achieving 100% pass rate on all test cases

**Integration with Existing Infrastructure**:
- **Primary Integration**: Direct MCP protocol connection between hx-n8n-server (.215) and hx-n8n-mcp-server (.214)
- **Secondary Integration**: Registration of n8n MCP server with hx-fastmcp-server (192.168.10.213) leveraging:
  - FastMCP as MCP server for agent-facing tool discovery
  - FastMCP as MCP client for routing to n8n MCP server
- Dual-path validation:
  - **Direct path**: AI agent → n8n MCP server (.214) → workflow execution
  - **Gateway path**: AI agent → FastMCP (.213) → n8n MCP server (.214) → workflow execution
- Verification of authentication flow through Layer 1 (Identity & Trust)
- Integration testing with operational AI agents (Claude Code on hx-cc-server)

**Documentation & Knowledge Transfer**:
- Technical architecture document (MCP server design, communication patterns)
- **Complete package inventory** (all installed MCP tools, packages, dependencies)
- Workflow-to-tool design guide (how to create MCP-compatible workflows)
- Parameter schema standards and best practices
- Error handling conventions and response codes
- **Direct connection vs. gateway routing** decision guide
- Troubleshooting guide (common issues, diagnostic procedures)
- Integration patterns for AI agents (discovery, invocation, result handling)
- Future LangGraph integration preparation guide
- Operational runbook (startup, shutdown, monitoring, maintenance)

**Standards & Governance**:
- Workflow naming and versioning conventions
- MCP tool metadata standards
- Parameter schema documentation requirements
- Testing checklist for new workflow tools
- Deployment approval process
- Change management procedures

### Out of Scope

**Excluded from This Project**:
- Development of n8n workflows beyond the initial 3-5 foundational tools (future epics)
- LangGraph server deployment and configuration (separate project - hx-lang-server at 192.168.10.226 not operational)
- Complex multi-step agent reasoning patterns (deferred until LangGraph integration)
- n8n workflow server infrastructure changes (hx-n8n-server at .215 already operational)
- Development of application-specific workflows (e.g., CRM integrations, business logic - future work)
- Performance optimization beyond basic load testing (advanced tuning is future phase)
- High availability or clustering configuration (single-node deployment for Phase 1)
- Comprehensive observability integration with hx-metric-server (basic logging only; full observability is future phase)
- User interface or dashboard development (CLI and API access only)
- Migration of existing n8n workflows to MCP format (start fresh with new workflows)
- External API key management system (use n8n's built-in credential storage)
- Advanced security features beyond basic Kerberos authentication (enhanced security is production requirement)

**Dependencies Not in Scope**:
- Changes to hx-fastmcp-server beyond registration configuration
- Modifications to hx-dc-server, hx-ca-server, or other Layer 1 infrastructure
- Database schema changes in hx-postgres-server, hx-redis-server, or hx-qdrant-server
- LiteLLM gateway modifications (MCP operates independently)
- Ollama cluster changes or model deployments

**Future Phase Considerations** (explicitly deferred):
- LangGraph "brain" integration when hx-lang-server becomes operational
- Advanced workflow orchestration patterns (multi-agent coordination)
- Workflow marketplace or discovery UI
- Automated workflow generation from natural language descriptions
- Workflow versioning and rollback mechanisms
- A/B testing framework for workflow variations
- Cost tracking and budget limits per workflow execution
- Integration with external workflow systems beyond n8n

### Key Deliverables

1. **Operational n8n MCP Server** (hx-n8n-mcp-server at 192.168.10.214) with:
   - **Complete MCP package installation** (all tools, packages, dependencies)
   - Domain-joined configuration (hx.dev.local)
   - TLS encryption enabled
   - Port 8003 exposed for MCP protocol communication
   - Service accounts and permissions properly configured
   - **Direct connectivity** to hx-n8n-server (192.168.10.215) verified
   - Comprehensive package inventory document

2. **Initial Workflow Tool Library** consisting of 3-5 production-ready workflows:
   - Complete MCP tool definitions with metadata
   - Validated parameter schemas
   - Error handling implementation
   - Success/failure response formatting
   - Documentation for each workflow tool
   - **Note**: Represents testing subset of full MCP capabilities

3. **Dual Integration Configuration** enabling:
   - **Direct MCP connections** from n8n server to MCP server
   - **FastMCP gateway integration** with:
     - MCP server functionality for agent discovery
     - MCP client functionality for routing to n8n MCP
   - Routing configuration for both direct and gateway paths
   - End-to-end execution path validation for both patterns

4. **Testing Framework** including:
   - Test suite covering all MCP operations
   - Test data sets for parameter validation
   - Direct connection test scenarios
   - Gateway routing test scenarios
   - Load testing scripts and results
   - 100% pass rate certification

5. **Comprehensive Documentation Package**:
   - Technical architecture document
   - **Complete MCP package inventory**
   - Workflow design guide
   - **Direct vs. gateway routing decision guide**
   - Integration patterns guide
   - Troubleshooting runbook
   - Future LangGraph preparation guide

6. **Operational Standards**:
   - Workflow naming conventions
   - MCP metadata standards
   - Testing checklist template
   - Deployment approval workflow

### Success Criteria

**Technical Success**:
- ✅ n8n MCP Server successfully deployed with **complete package installation** on hx-n8n-mcp-server (192.168.10.214)
- ✅ **Complete package inventory** documented (all MCP tools, packages, dependencies)
- ✅ All infrastructure dependencies resolved (authentication, certificates, network connectivity)
- ✅ **Direct MCP protocol connection** operational between n8n server (.215) and MCP server (.214)
- ✅ Minimum 3 workflows successfully exposed as MCP tools
- ✅ **Dual-path integration validated**: direct connections and FastMCP gateway routing both functional
- ✅ 100% pass rate on all test cases (discovery, parameter validation, execution, error handling) for both connection patterns
- ✅ End-to-end agent-to-workflow-to-response execution validated via both direct and gateway paths
- ✅ Response time under 5 seconds for simple workflows (excluding workflow execution time)
- ✅ Zero critical or high-severity defects in production deployment

**Quality Success**:
- ✅ Complete documentation package delivered and reviewed
- ✅ **Package inventory complete and accurate**
- ✅ All workflows meet established metadata and parameter schema standards
- ✅ Error handling consistently implemented across all workflows
- ✅ Code review completed and approved for all MCP configuration
- ✅ Security review completed (authentication, authorization, data handling)
- ✅ **Connection pattern decision guide** validated and approved

**Integration Success**:
- ✅ **Direct n8n-to-MCP connection** operational and tested
- ✅ Successful registration with hx-fastmcp-server (192.168.10.213) as both server and client target
- ✅ At least one operational AI agent successfully invokes n8n workflows via **both connection patterns**
- ✅ Workflows accessible through standardized MCP discovery mechanism
- ✅ No disruption to existing MCP services during integration
- ✅ FastMCP dual-role (server + client) configuration validated

**Operational Success**:
- ✅ Service starts automatically on server boot
- ✅ Logging and basic monitoring functional
- ✅ Troubleshooting runbook validated through actual issue resolution
- ✅ Team trained on workflow-to-tool development process
- ✅ **Team trained on direct vs. gateway routing decisions**
- ✅ Clear path established for adding new workflows to MCP registry

### Constraints

**Technical Constraints**:
- Must operate within HANA-X Layer 4 (Agentic & Toolchain) architecture
- Must authenticate through hx-dc-server (192.168.10.200) using Kerberos/LDAP
- Must use TLS certificates issued by hx-ca-server (192.168.10.201)
- Must communicate with n8n workflow server at 192.168.10.215 (no alternative server available)
- **Must support direct MCP protocol connections** from n8n server
- Must register with hx-fastmcp-server (192.168.10.213) for agent discovery
- **FastMCP acts as both MCP server (for agents) and MCP client (for n8n MCP routing)**
- Internal network only (no external access through hx-ssl-server in Phase 1)
- Single-node deployment (no clustering or high availability in Phase 1)
- Must comply with MCP protocol specification standards

**Resource Constraints**:
- Limited to single dedicated server (hx-n8n-mcp-server at 192.168.10.214)
- Development must use existing n8n server infrastructure (no additional n8n instances)
- No budget for external services or commercial MCP server implementations
- Must use open-source or built-in n8n MCP capabilities
- **Full package installation required** regardless of immediate usage

**Timeline Constraints**:
- Aggressive timeline with days between project phases (per user preference)
- Must achieve 100% pass rate before advancing each phase
- Cannot proceed to next milestone until quality gates passed
- Iterative learning approach requires validation at each step

**Security Constraints**:
- Development environment security model applies (standard passwords: Major8859! or Major8859)
- No external API access without explicit approval
- Secrets stored in plain text acceptable for development (production requires vault)
- Service account permissions must follow least-privilege principle within dev constraints

### Assumptions

**Infrastructure Assumptions**:
- hx-n8n-server (192.168.10.215) is fully operational and stable
- hx-n8n-server **supports direct MCP protocol communication**
- hx-dc-server (192.168.10.200) is available for authentication services
- hx-ca-server (192.168.10.201) can issue TLS certificates on demand
- hx-fastmcp-server (192.168.10.213) is operational and supports **dual-role operation** (MCP server for agents, MCP client for routing)
- hx-fastmcp-server can register and route to n8n MCP server as a backend target
- Network connectivity between .214 and .215 is reliable for direct connections
- DNS resolution through hx-dc-server is functional (hx.dev.local domain)

**n8n MCP Capability Assumptions**:
- n8n MCP Server software includes complete package distribution with all tools and integrations
- n8n includes native MCP Server node or compatible functionality
- n8n API **supports direct MCP protocol connections**
- n8n API supports workflow triggering via external MCP protocol
- n8n credential management can store required authentication tokens
- n8n supports parameter passing and response formatting required by MCP

**FastMCP Capability Assumptions**:
- FastMCP can function as **both MCP server and MCP client simultaneously**
- FastMCP supports routing to backend MCP servers (like n8n MCP)
- FastMCP can expose tools from multiple backend MCP servers to agents
- FastMCP supports service registration and discovery patterns

**Agent Assumptions**:
- At least one operational AI agent exists that can consume MCP tools (e.g., Claude Code on hx-cc-server)
- Agents understand standard MCP protocol discovery and invocation patterns
- Agents can connect via **either direct or gateway routing** patterns
- Future LangGraph integration (hx-lang-server) will follow same MCP patterns

**Operational Assumptions**:
- Team has access to hx-control-node (192.168.10.203) for Ansible deployment
- Administrative credentials available for server configuration
- Sufficient disk space and compute resources on hx-n8n-mcp-server for **complete package installation**
- No competing projects requiring hx-n8n-mcp-server resources during deployment

**Knowledge Assumptions**:
- Team has working knowledge of n8n workflow development
- MCP protocol documentation is accessible and complete
- Reference implementations or examples of MCP servers exist for guidance
- n8n documentation includes MCP Server node configuration guidance
- **FastMCP documentation includes dual-role configuration guidance**

### Risks & Mitigations

**Risk**: MCP Server node may not exist natively in n8n  
**Impact**: High - Project foundation at risk  
**Mitigation**: Research n8n MCP capabilities upfront; if unavailable, implement custom HTTP endpoint wrapper using MCP protocol libraries

**Risk**: Full package installation may exceed disk space or memory constraints  
**Impact**: Medium - May need to prune packages  
**Mitigation**: Verify disk/memory capacity before installation; document actual usage vs. capacity; establish package pruning criteria if needed

**Risk**: Direct MCP connections between n8n server and MCP server may not be supported  
**Impact**: High - Changes architecture significantly  
**Mitigation**: Validate n8n-to-MCP direct connection capability early; if unavailable, pivot to gateway-only pattern with FastMCP

**Risk**: FastMCP may not support dual-role operation (server + client simultaneously)  
**Impact**: Medium - Requires different routing pattern  
**Mitigation**: Test FastMCP dual-role capability early; if unavailable, implement separate routing layer or use direct connections only

**Risk**: Performance degradation on single-node deployment under load  
**Impact**: Low - Can be addressed in future phases  
**Mitigation**: Implement load testing early; establish baseline performance metrics; document scaling path for future

**Risk**: Network connectivity issues between .214 and .215  
**Impact**: High - Direct connections fail  
**Mitigation**: Validate connectivity before deployment; establish monitoring; document troubleshooting procedures; maintain gateway routing as backup

**Risk**: Authentication failures with Kerberos/LDAP integration  
**Impact**: Medium - Deployment blocked  
**Mitigation**: Follow established HANA-X authentication patterns; leverage existing working examples (other MCP servers at .211, .217, .218)

**Risk**: Scope creep with additional workflow requests during development  
**Impact**: Medium - Timeline延長  
**Mitigation**: Strict adherence to 3-5 initial workflows; maintain backlog for future workflow additions; emphasize complete package installation enables future workflows

**Risk**: LangGraph integration patterns may differ from assumptions  
**Impact**: Low - Future integration complexity  
**Mitigation**: Design flexible MCP interface; document integration patterns; prepare for future refactoring if needed

**Risk**: Package dependencies conflict with existing HANA-X infrastructure  
**Impact**: Medium - May require infrastructure changes  
**Mitigation**: Test installation in isolated environment first; document all dependencies; coordinate with infrastructure team before production deployment

---

## Project Phases

### Phase 1: Research & Planning (Days 1-2)
- Research n8n MCP capabilities and package inventory
- Validate direct connection support
- Validate FastMCP dual-role capabilities
- Document complete package requirements
- Create detailed installation plan
- **Go/No-Go Decision Point**: Confirm technical feasibility

### Phase 2: Infrastructure Setup (Days 3-5)
- Complete package installation on hx-n8n-mcp-server (.214)
- Domain join and authentication configuration
- TLS certificate installation
- Network connectivity validation
- Service account creation
- **Quality Gate**: All infrastructure tests pass 100%

### Phase 3: MCP Protocol Implementation (Days 6-8)
- Configure MCP Server node in n8n
- Implement direct MCP connections
- Configure FastMCP dual-role integration
- Implement tool discovery endpoints
- Implement parameter validation
- **Quality Gate**: MCP protocol compliance verified

### Phase 4: Initial Workflow Development (Days 9-12)
- Design and implement 3-5 foundational workflows
- Create MCP tool metadata
- Implement error handling
- Document workflows
- **Quality Gate**: All workflows pass unit tests 100%

### Phase 5: Integration Testing (Days 13-15)
- Direct connection testing (n8n → n8n MCP)
- Gateway routing testing (agent → FastMCP → n8n MCP)
- End-to-end agent integration testing
- Load testing
- **Quality Gate**: All integration tests pass 100%

### Phase 6: Documentation & Handoff (Days 16-17)
- Complete all documentation deliverables
- Package inventory documentation
- Operational runbook creation
- Team training sessions
- **Quality Gate**: Documentation review approved

### Phase 7: Production Deployment (Day 18)
- Final validation checks
- Production cutover
- Monitoring validation
- Post-deployment review
- **Quality Gate**: Zero critical defects, service operational

---

**Document Version**: 1.0  
**Created**: November 10, 2025  
**Last Updated**: November 10, 2025  
**Project Phase**: Planning & Charter Definition  
**Classification**: Internal - Project Management  
**Status**: DRAFT - In Development  

---

## Approval Signatures

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Sponsor | Agent Zero | _______________ | _______ |
| Technical Lead | Claude Code | _______________ | _______ |
| Infrastructure Lead | Layer 1 Team | _______________ | _______ |
| Quality Assurance | Roger (Code Quality) | _______________ | _______ |

---

## Document Change Log

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-10 | Initial draft with full package scope and direct connection clarifications | Claude Code |

---

*This project charter establishes the foundation for n8n MCP Server deployment, aligning with HANA-X quality-first principles and iterative development methodology. The complete package installation ensures maximum flexibility for future workflow development while the 3-5 initial workflows validate core capabilities.*
