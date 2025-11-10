# Hana-X Knowledge Vault Catalog

**Location:** `/srv/knowledge/vault`
**Purpose:** Repository of documentation, source code, and reference materials for all Hana-X agents
**Maintained By:** Agent Zero
**Last Updated:** November 8, 2025

---

## Knowledge Organization

The knowledge vault contains documentation and source code for all technologies used in the Hana-X infrastructure. This catalog helps Agent Zero and specialist agents quickly find relevant information when orchestrating work.

---

## Layer 1: Identity & Trust Resources

### Authentication & Directory Services
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `ansible-devel` | Ansible Development | Amanda Chen | Configuration automation docs |
| `nginx` | Nginx | Frank Lucas | Reverse proxy documentation |
| `nginx-master` | Nginx Source | Frank Lucas | Web server and SSL/TLS proxy |

**Use when:** Setting up domain authentication, SSL certificates, web proxies

---

## Layer 2: Model & Inference Resources

### LLM Models & Frameworks
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `ollama-main` | Ollama | Patricia Miller | Local LLM deployment and management |
| `litellm-main` | LiteLLM | Maya Singh | LLM gateway, routing, proxy |
| `langgraph-main` | LangGraph | Laura Patel | Graph-based agent orchestration |
| `langchain` | LangChain | Laura Patel | Legacy chain-based patterns (reference) |
| `langchain-docs` | LangChain Docs | Laura Patel | Migration reference documentation |

**Use when:** Deploying LLM infrastructure, building agent workflows, model routing

---

## Layer 3: Data Plane Resources

### Databases & Caching
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `postgres-master` | PostgreSQL | Quinn Davis | Database deployment, optimization |
| `redis-unstable` | Redis | Samuel Wilson | Caching, session storage |
| `qdrant-master` | Qdrant | Robert Chen | Vector database source |
| `qdrant-client-master` | Qdrant Client | Robert Chen | Vector DB client library |
| `qdrant-web-ui` | Qdrant UI | Sarah Mitchell | Web interface for Qdrant |
| `prisma-main` | Prisma ORM | Multiple | Database ORM and migrations |

**Use when:** Setting up databases, implementing caching, vector storage

---

## Layer 4: Agentic & Toolchain Resources

### MCP Servers & Workers
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `fastmcp-main` | FastMCP | George Kim | MCP gateway implementation |
| `mcp-server-qdrant-master` | Qdrant MCP | Kevin O'Brien | Qdrant MCP server |
| `n8n-mcp-main` | N8N MCP | Olivia Chang | N8N MCP integration |
| `mcp-crawl4ai-rag` | Crawl4ai MCP | David Thompson | Web scraping MCP server |
| `docling-mcp` | Docling MCP | Eric Johnson | Document processing MCP |
| `magic-mcp` | Magic MCP | Multiple | MCP utilities and helpers |
| `shield_mcp_complete` | Shield MCP | Multiple | MCP security patterns |

### RAG & Document Processing
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `crawl4ai-main` | Crawl4ai | Diana Martinez | Web scraping and data extraction |
| `docling-main` | Docling | Elena Rodriguez | Document parsing and processing |
| `LightRAG-main` | LightRAG | Marcus Johnson | Knowledge graph RAG system |

### Agentic Patterns
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `agentic-design-patterns-docs-main` | Design Patterns | Agent Zero | Agent architecture patterns |
| `ottomator-agents-main` | Ottomator | Multiple | Multi-agent orchestration examples |
| `Skill_Seekers-development` | Skill Seekers | Multiple | Agent skill discovery patterns |

**Use when:** Building RAG pipelines, MCP integrations, multi-agent systems

---

## Layer 5: Application Resources

### Frontend Frameworks
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `next.js-canary` | Next.js | Victor Lee | React framework, SSR |
| `tailwindcss` | Tailwind CSS | Victor Lee | Utility-first CSS framework |
| `primitives` | Radix Primitives | Hannah Brooks | UI component primitives |
| `ui-main` | UI Components | Multiple | Shared UI component library |
| `solid-principles` | Solid.js | Brian Foster | Reactive UI framework |
| `zustand-main` | Zustand | Multiple | State management |

### UI & Interactions
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `CopilotKit-main` | CopilotKit | Hannah Brooks | AI copilot UI components |
| `ag-ui-main` | AG-UI | Brian Foster | Agentic UI framework |
| `21st-extension` | 21st Extension | Multiple | Browser extension patterns |
| `spec-kit-main` | Spec Kit | Multiple | Design specifications toolkit |
| `thesys` | Thesys | Multiple | Thesys integration documentation |

### Backend & API
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `fastapi` | FastAPI Docs | Fatima Hassan | API framework documentation |
| `fastapi-master` | FastAPI Source | Fatima Hassan | Python async API framework |
| `n8n-master` | N8N | Omar Rodriguez | Workflow automation platform |
| `open-webui-main` | Open WebUI | Paul Anderson | LLM web interface |

### Validation & Data
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `pydantic-main` | Pydantic | Multiple | Data validation library |
| `zod-main` | Zod | Multiple | TypeScript schema validation |

**Use when:** Building web applications, APIs, user interfaces

---

## Layer 6: Integration & Testing Resources

### CI/CD & Testing
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `cypress` | Cypress | Julia Santos | E2E testing framework |
| `pytest` | Pytest | Julia Santos | Python testing framework |

### Infrastructure & Deployment
| Directory | Technology | Agent | Purpose |
|-----------|-----------|-------|---------|
| `docker-install-master` | Docker Install | Yasmin Patel | Docker installation guides |
| `compose-main` | Docker Compose | Yasmin Patel | Multi-container orchestration |
| `cli-master` | CLI Tools | Multiple | Command-line interface patterns |

**Use when:** Setting up testing, CI/CD, containerization

---

## Quick Lookup: "Need Info About X?"

### By Technology Type

**Authentication/Security:**
- `ansible-devel`, `nginx`, `nginx-master`

**LLMs & AI:**
- `ollama-main`, `litellm-main`, `langgraph-main`, `langchain`, `langchain-docs`

**Databases:**
- `postgres-master`, `redis-unstable`, `qdrant-master`, `qdrant-client-master`, `qdrant-web-ui`

**MCP Ecosystem:**
- `fastmcp-main`, `mcp-server-qdrant-master`, `n8n-mcp-main`, `mcp-crawl4ai-rag`, `docling-mcp`, `magic-mcp`, `shield_mcp_complete`

**RAG & Documents:**
- `crawl4ai-main`, `docling-main`, `LightRAG-main`

**Frontend:**
- `next.js-canary`, `tailwindcss`, `CopilotKit-main`, `ag-ui-main`, `open-webui-main`

**Backend/API:**
- `fastapi`, `fastapi-master`, `n8n-master`

**Agent Patterns:**
- `agentic-design-patterns-docs-main`, `ottomator-agents-main`, `Skill_Seekers-development`

**Testing:**
- `cypress`, `pytest`

**Infrastructure:**
- `docker-install-master`, `compose-main`

---

## Usage Patterns for Agent Zero

### When Orchestrating a Task:

1. **Identify required technology** from user request
2. **Find relevant documentation** in this catalog
3. **Direct specialist agents** to appropriate knowledge resources
4. **Reference specific docs** when providing context to agents

### Example Orchestration:

```
User: "Deploy a new LangGraph application"

Agent Zero thinks:
1. LangGraph = Layer 2 (Model & Inference)
2. Agent: Laura Patel
3. Knowledge needed: /srv/knowledge/vault/langgraph-main
4. Related: fastmcp-main, open-webui-main

Agent Zero invokes:
@agent-laura "Build LangGraph application.
Reference: /srv/knowledge/vault/langgraph-main for architecture
Reference: /srv/knowledge/vault/fastmcp-main for MCP integration"
```

---

## Maintenance Guidelines

### Adding New Knowledge

When adding new documentation to `/srv/knowledge/vault`:

1. **Add directory** to vault: `git clone <repo> /srv/knowledge/vault/<name>`
2. **Update this catalog** with:
   - Directory name
   - Technology/project name
   - Responsible agent
   - Purpose/use case
   - Layer assignment
3. **Notify relevant agents** if it affects their domain
4. **Commit changes** to this catalog document

### Keeping Knowledge Current

**Monthly:**
- [ ] Review all `*-main`, `*-master` repositories for updates
- [ ] Run: `cd /srv/knowledge/vault/<dir> && git pull`
- [ ] Note any breaking changes in agent profiles

**Quarterly:**
- [ ] Archive deprecated documentation
- [ ] Add new technologies as they're adopted
- [ ] Reorganize if layer structure changes

**On Technology Migration:**
- [ ] Keep old docs as "legacy reference" (e.g., langchain)
- [ ] Add new docs (e.g., langgraph-main)
- [ ] Update agent profiles to prefer new over old

---

## File Structure Conventions

### Directory Naming
- `<project>-main` → Main branch of active project
- `<project>-master` → Master branch (legacy naming)
- `<project>-devel` → Development branch
- `<project>` → Stable release documentation

### Recommended Organization
```
/srv/knowledge/vault/
├── layer-1-identity/     (future: organize by layer)
├── layer-2-models/
├── layer-3-data/
├── layer-4-agentic/
├── layer-5-application/
└── layer-6-integration/
```

**Note:** Current flat structure works, but layer-based organization may improve as vault grows.

---

## Knowledge Vault Statistics

**Total Directories:** 50
**Coverage:**
- Layer 1: 3 directories
- Layer 2: 5 directories
- Layer 3: 6 directories
- Layer 4: 12 directories
- Layer 5: 18 directories
- Layer 6: 6 directories

**Languages Represented:**
- Python: 22 projects
- TypeScript/JavaScript: 18 projects
- Go: 3 projects
- Mixed: 7 projects

**Update Frequency:**
- Active (monthly updates): 35 directories
- Stable (quarterly updates): 10 directories
- Reference (rarely updated): 5 directories

---

## Agent-Specific Knowledge Profiles

### Frank Lucas (Samba DC)
**Primary:** `nginx`, `nginx-master`, `ansible-devel`
**Secondary:** None
**Reason:** SSL/TLS, reverse proxy, automation

### Laura Patel (LangGraph)
**Primary:** `langgraph-main`
**Secondary:** `langchain`, `langchain-docs`, `agentic-design-patterns-docs-main`
**Reason:** Graph-based orchestration, migration from chains

### Patricia Miller (Ollama)
**Primary:** `ollama-main`
**Secondary:** `litellm-main`
**Reason:** LLM deployment, model management

### Marcus Johnson (LightRAG)
**Primary:** `LightRAG-main`
**Secondary:** `qdrant-master`, `crawl4ai-main`, `docling-main`
**Reason:** RAG pipeline integration, knowledge graphs

### Diana Martinez (Crawl4ai)
**Primary:** `crawl4ai-main`
**Secondary:** `mcp-crawl4ai-rag`
**Reason:** Web scraping, MCP integration

### Elena Rodriguez (Docling)
**Primary:** `docling-main`
**Secondary:** `docling-mcp`
**Reason:** Document processing, MCP integration

### George Kim (FastMCP)
**Primary:** `fastmcp-main`
**Secondary:** `magic-mcp`, `shield_mcp_complete`
**Reason:** MCP gateway, security patterns

### Victor Lee (Next.js)
**Primary:** `next.js-canary`, `tailwindcss`
**Secondary:** `ui-main`, `primitives`
**Reason:** Frontend development, styling

### Hannah Brooks (CopilotKit)
**Primary:** `CopilotKit-main`
**Secondary:** `open-webui-main`, `primitives`
**Reason:** AI-powered UI components

---

## Quick Commands

### Search Knowledge Vault
```bash
# Find documentation about a technology
find /srv/knowledge/vault -name "*keyword*" -type d

# Search within documentation
grep -r "search term" /srv/knowledge/vault/

# List all README files
find /srv/knowledge/vault -name "README.md" -exec echo {} \;
```

### Update All Knowledge
```bash
# Update all git repositories
for dir in /srv/knowledge/vault/*/; do
  if [ -d "$dir/.git" ]; then
    echo "Updating $(basename $dir)..."
    (cd "$dir" && git pull)
  fi
done
```

### Check Knowledge Status
```bash
# Show last update time for each directory
for dir in /srv/knowledge/vault/*/; do
  echo "$(basename $dir): $(stat -c %y $dir | cut -d' ' -f1)"
done | sort -k2
```

---

## Related Documents

- **Agent Catalog:** `/srv/cc/Governance/0.1-agents/agent-catalog.md`
- **Orchestration Guide:** `/srv/cc/Governance/docs/HANA-X-ORCHESTRATION.md`
- **Agent Profiles:** `/srv/cc/Governance/0.1-agents/agent-*.md`

---

**Version:** 1.0
**Classification:** Internal - Governance
**Status:** ACTIVE - Primary knowledge reference
**Maintained By:** Agent Zero
**Last Review:** November 8, 2025

---

*This catalog helps Agent Zero and all specialist agents quickly locate relevant documentation when orchestrating infrastructure work. Keep it updated as new knowledge is added to the vault.*
