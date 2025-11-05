# Service Integrations
**Purpose**: Document how services integrate with each other

## Contents

- `service-integration-matrix.md` - Complete matrix of all service integrations
- `<service>-integrations.md` - Integration details for each major service

## Integration Patterns

### Database Integrations
- PostgreSQL: Application database storage
- Redis: Caching and session management
- Qdrant: Vector storage for RAG pipelines

### LLM Integrations
- Ollama: Backend LLM providers
- LiteLLM: Unified LLM gateway (routes to Ollama)
- Langchain: LLM orchestration framework

### MCP Integrations
- FastMCP: MCP gateway (mounts other MCP servers)
- QMCP: Qdrant MCP interface
- Docling MCP: Document processing
- Crawl4ai MCP: Web crawling
- N8N MCP: Workflow automation

### Application Integrations
- Open WebUI: User interface for LLMs (uses LiteLLM)
- AG-UI: Agent-to-frontend communication protocol
- Next.js: Frontend applications (dev/demo servers)

## Usage

When integrating a new service:
1. Identify dependencies (upstream/downstream)
2. Document connection details (host, port, protocol, auth)
3. Provide integration examples (code, configuration)
4. Update integration matrix
5. Test integration end-to-end

**Referenced by**:
- Service owner agents (for integration coordination)
- Application developers (for connecting to services)
- Architecture documentation (for dependency mapping)
