# Hana-X Orchestration Quick Reference

## Instant Lookup: Common Tasks

### New Service Deployment
```bash
Pattern: William → Frank → [Service] → Amanda → Nathan

1. @agent-william "Prepare server: [name].hx.dev.local, IP: 192.168.10.XXX"
2. @agent-frank "Samba DC: account + DNS + SSL for [name].hx.dev.local"
3. @agent-[service] "Deploy [service] on [name].hx.dev.local"
4. @agent-amanda "Ansible playbook" (optional)
5. @agent-nathan "Monitoring" (optional)
```

### RAG Pipeline Setup
```bash
Pattern: Diana+Elena → Patricia → Robert → Marcus

1. PARALLEL:
   @agent-diana "Crawl4ai: [sources]"
   @agent-elena "Docling: [documents]"
2. @agent-patricia "Generate embeddings"
3. @agent-robert "Store in Qdrant"
4. @agent-marcus "LightRAG knowledge graph"
```

### LLM Application
```bash
Pattern: Maya → Laura → George → [Frontend]

1. @agent-maya "LiteLLM routing"
2. @agent-laura "LangGraph graphs"
3. @agent-george "FastMCP gateway"
4. @agent-[paul|hannah|brian] "Frontend UI"
```

### Troubleshooting
```bash
Pattern: Identify → Diagnose → Fix → Validate

Layer 1 (Auth/DNS): @agent-frank or @agent-william
Layer 2 (Models): @agent-patricia or @agent-maya
Layer 3 (Data): @agent-quinn, @agent-samuel, @agent-robert
Layer 4+ (Apps): [specific agent]
```

---

## The 30 Agents (By Layer)

**Layer 0: Governance & Architecture** (Meta-Layer)
- Agent Zero: PM Orchestrator, terminal authority
- Alex: Platform Architect, ADRs, architecture governance

**Layer 1: Identity & Trust** (Foundation - Required First)
- Frank: Samba DC, DNS, SSL
- William: Ubuntu servers
- Yasmin: Docker
- Amanda: Ansible

**Layer 2: Model & Inference**
- Patricia: Ollama
- Maya: LiteLLM
- Laura: LangGraph

**Layer 3: Data Plane**
- Quinn: PostgreSQL
- Samuel: Redis
- Robert: Qdrant
- Sarah: Qdrant UI

**Layer 4: Agentic**
- George: FastMCP
- Kevin: Qdrant MCP
- Olivia: N8N MCP
- David: Crawl4ai MCP
- Eric: Docling MCP
- Diana: Crawl4ai Worker
- Elena: Docling Worker
- Marcus: LightRAG

**Layer 5: Application**
- Paul: Open WebUI
- Hannah: CopilotKit
- Brian: AG-UI
- Omar: N8N Workflows
- Victor: Next.js
- Fatima: FastAPI

**Layer 6: Integration & Governance**
- Isaac: GitHub Actions
- Julia: Testing
- Nathan: Monitoring
- Carlos: CodeRabbit

---

## Critical Rules

1. **Layer 1 FIRST** - William + Frank before everything else
2. **Validate ALWAYS** - Check outputs before proceeding
3. **Parallel when possible** - Same layer, independent work
4. **Sequential when required** - Cross-layer or dependencies

---

## Agent Invocation Template

```
@agent-[name]

Task: [One sentence]

Context:
- Working on: [what]
- Layer status: [ready?]

Requirements:
1. [What]
2. [How]

Expected:
- [Deliverable]
- [Proof of success]
```

**Programmatic Invocation:** Use Task tool with lowercase agent names
- Example: `subagent_type="william"` NOT `"@agent-william"`
- Exceptions: "Diana" and "David" (capital D), "agent-zero"

---

## Quality Checklist

**Foundation:**
- [ ] Server domain-joined
- [ ] DNS resolves
- [ ] SSL valid
- [ ] Service account created

**Service:**
- [ ] Installed & running
- [ ] Auth works
- [ ] Tests pass
- [ ] Logs clean

**Integration:**
- [ ] End-to-end tested
- [ ] Performance good
- [ ] Documentation done

---

## Error Response

**Layer 1 fails:** STOP - Fix before continuing
**Service fails:** Diagnose → Correct → Re-invoke
**2 failures:** Escalate to user

---

## IP Range: 192.168.10.200-229
**Domain:** hx.dev.local
**Claude Code Server:** hx-cc-server.hx.dev.local (192.168.10.224)
**Project Dir:** /srv/cc/Governance
**Knowledge Vault:** /srv/knowledge/vault
**Docs:** /srv/cc/Governance/

**Full Guide:** HANA-X-ORCHESTRATION.md

---

**Quality = Accuracy > Speed**
