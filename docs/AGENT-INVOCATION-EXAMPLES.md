# Agent Invocation Examples

**Document Type:** Operational Reference - Practical Examples
**Created:** 2025-11-10
**Purpose:** Real-world examples of agent invocation using Task tool
**Audience:** Agent Zero
**Classification:** Internal - Governance

---

## Overview

This document provides **practical, working examples** of agent invocation using the Claude Code Task tool. Each example demonstrates:
- Correct Task tool syntax
- Proper agent name format (lowercase, with exceptions)
- Complete prompt structure
- Expected output patterns
- Common mistakes to avoid

---

## Agent Name Reference

### Standard Naming (lowercase)
```
william, frank, quinn, samuel, patricia, maya, laura, george, kevin,
olivia, elena, eric, marcus, paul, hannah, brian, omar, victor,
fatima, isaac, julia, nathan, alex, carlos, amanda, sarah,
robert, yasmin
```

### Exceptions (capitalized)
```
Diana    - Crawl4ai worker (capital D)
David    - Crawl4ai MCP (capital D)
agent-zero - Agent Zero itself (with prefix)
```

---

## Example 1: Single Agent Invocation (Sequential)

### Scenario: Deploy PostgreSQL Database

**Step 1: William prepares Ubuntu server**

Correct invocation:
- subagent_type: "william" (lowercase)
- description: Brief task summary
- prompt: Full requirements using standard template

Expected result: William completes server prep, provides validation evidence

**Step 2: Frank configures Samba DC**

After William completes, invoke Frank with handoff information from William.

Expected result: Frank creates domain accounts, DNS, SSL certificate

**Step 3: Quinn deploys PostgreSQL**

After Frank completes, invoke Quinn with credentials and configuration.

Expected result: Quinn deploys and configures PostgreSQL service

---

## Example 2: Parallel Agent Invocation

### Scenario: RAG Pipeline Setup

**Step 1: Diana and Elena work simultaneously**

Invoke both agents in the SAME message for parallel execution.

Agent 1: Diana (Crawl4ai worker)
- subagent_type: "Diana" (capital D - exception)
- Task: Configure web scraping

Agent 2: Elena (Docling worker)
- subagent_type: "elena" (lowercase)
- Task: Configure document processing

Both agents execute simultaneously and return results independently.

**Step 2: Sequential after parallel completion**

After BOTH Diana and Elena complete, invoke Patricia for embeddings.

---

## Example 3: Layer 1 Foundation Pattern

### Scenario: New Service Deployment (Any Service)

**Universal Pattern: William → Frank → [Service Agent]**

This pattern ALWAYS applies for new service deployments:

1. William (Ubuntu prep) - ALWAYS FIRST
2. Frank (Samba DC setup) - ALWAYS SECOND
3. [Service Agent] - Deploy actual service
4. Amanda (Ansible) - Optional automation
5. Nathan (Monitoring) - Optional observability

**Critical Rule:** NEVER skip steps 1-2. Layer 1 must be complete before service deployment.

---

## Example 4: RAG Pipeline (End-to-End)

### Scenario: Build Complete RAG System

**Phase 1: Data Acquisition (Parallel)**

Invoke Diana and elena in the same message.

Diana output: Crawled web data in JSON format
Elena output: Processed documents with chunks

**Phase 2: Embedding Generation (Sequential)**

Invoke patricia after Phase 1 completes.

Patricia output: Vector embeddings ready for storage

**Phase 3: Vector Storage (Sequential)**

Invoke robert after Patricia completes.

Robert output: Qdrant collection created, vectors stored

**Phase 4: Knowledge Graph (Sequential)**

Invoke marcus after Robert completes.

Marcus output: LightRAG knowledge graph operational

---

## Example 5: LLM Application Build

### Scenario: Create AI-Powered Chat Application

**Phase 1: Model Routing**

Invoke maya to configure LiteLLM.

Maya output: LiteLLM gateway configured, API endpoints ready

**Phase 2: Agent Graphs**

Invoke laura after Maya completes.

Laura output: LangGraph agent graph deployed

**Phase 3: MCP Gateway**

Invoke george after Laura completes.

George output: FastMCP gateway exposing Laura's agent

**Phase 4: Frontend**

Invoke hannah OR paul OR brian (choose based on requirements).

Output: Complete frontend application integrated with backend

**Phase 5: Workflows (Optional)**

If complex automation needed, invoke omar.

Omar output: N8N workflows for automation

---

## Example 6: Troubleshooting Pattern

### Scenario: Service Authentication Failure

**Step 1: Identify Layer**

Authentication issue = Layer 1 (Identity & Trust)

**Step 2: Invoke Layer 1 Agent**

Choose frank (Samba DC specialist).

Frank diagnoses: DNS issue, SSL certificate expired, or account permissions

**Step 3: Frank Fixes Issue**

Frank resolves the problem and provides evidence.

**Step 4: Validate End-to-End**

After Frank completes, re-test the original failing operation.

If still failing: May need Layer 3 agent (quinn for PostgreSQL auth, samuel for Redis auth, etc.)

---

## Example 7: Architecture Review

### Scenario: Multi-Layer Service Integration

**When to Invoke Alex Rivera (Platform Architect)**

Invoke alex when:
- Architecture decisions affect multiple layers
- Need to create Architecture Decision Record (ADR)
- Validating design against governance standards
- Resolving architectural conflicts
- Planning major platform changes

Alex output: Architecture guidance, ADR documentation, governance alignment

---

## Example 8: Multi-Agent Coordination

### Scenario: Complex Deployment with Multiple Dependencies

**Pattern: Coordinate across layers with proper sequencing**

Layer 1 (Foundation):
1. william - Server prep
2. frank - Samba DC setup

Layer 2/3 (Infrastructure):
3. quinn - PostgreSQL database
4. samuel - Redis cache (can be parallel with #3)
5. robert - Qdrant vectors (can be parallel with #3-4)

Layer 4 (Agentic):
6. george - FastMCP gateway (after Layer 2/3 complete)
7. marcus - LightRAG (after robert completes)

Layer 5 (Application):
8. paul - Frontend application (after all layers complete)

Layer 6 (Observability):
9. nathan - Monitoring (after application deployed)

**Key Principle:** Respect layer dependencies, parallelize within layers when possible.

---

## Common Mistakes to Avoid

### ❌ Mistake 1: Wrong Agent Name Format
```
WRONG: subagent_type="@agent-william"
WRONG: subagent_type="agent-william"
WRONG: subagent_type="William"
RIGHT: subagent_type="william"
```

### ❌ Mistake 2: Capital D Exception
```
WRONG: subagent_type="diana" (lowercase for Diana is incorrect)
RIGHT: subagent_type="Diana" (capital D required)
```

### ❌ Mistake 3: Skipping Layer 1
```
WRONG:
1. Invoke quinn directly to deploy PostgreSQL

RIGHT:
1. Invoke william for server prep
2. Invoke frank for Samba DC
3. Invoke quinn for PostgreSQL
```

### ❌ Mistake 4: Sequential When Parallel Possible
```
WRONG (slow):
1. Invoke Diana
2. Wait
3. Invoke elena
4. Wait
5. Invoke patricia

RIGHT (faster):
1. Invoke Diana and elena in SAME message (parallel)
2. Wait for both
3. Invoke patricia
```

### ❌ Mistake 5: Vague Requirements
```
WRONG:
"Deploy PostgreSQL"

RIGHT:
"Deploy PostgreSQL on hx-postgres-server.hx.dev.local:
- Version: PostgreSQL 16
- Databases: production_db, staging_db
- Authentication: Samba DC via service account
- SSL: Required
- Backup: Daily 2am UTC
- Monitoring: Enabled via Nathan"
```

---

## Validation Checklist

### After EVERY Agent Invocation

Before considering agent work "complete":

**Task Completion**
- [ ] All requirements from prompt were addressed
- [ ] No partial work or "TODO" items left
- [ ] Agent provided evidence of completion

**Quality Gates**
- [ ] Output meets project standards
- [ ] Configuration documented
- [ ] Integration points validated
- [ ] No errors or warnings unresolved

**Handoff Readiness**
- [ ] Next agent has all information needed
- [ ] Credentials/endpoints clearly documented
- [ ] Dependencies explicitly stated

**If ANY checkbox fails:** Re-invoke agent with specific corrections

---

## Agent Response Patterns

### Successful Completion

Good agent responses include:
- ✅ "Task completed successfully"
- ✅ Specific validation evidence (test outputs, screenshots, logs)
- ✅ Configuration details in structured format
- ✅ Handoff information for next agent
- ✅ No errors or warnings

### Needs Correction

Agent responses requiring follow-up:
- ⚠️ Partial completion ("mostly done, but...")
- ⚠️ Assumptions made without confirmation
- ⚠️ Missing validation evidence
- ⚠️ Errors/warnings not resolved
- ⚠️ Vague or unclear outputs

Action: Provide specific corrections and re-invoke

### Failure

Agent responses indicating failure:
- ❌ "Unable to complete due to..."
- ❌ Dependency missing or broken
- ❌ Permission/access issues
- ❌ Configuration conflicts

Action: Diagnose root cause, resolve dependencies, re-invoke

---

## Decision Tree: Sequential vs Parallel

```
START: Need to invoke multiple agents
    ↓
Are agents in the same layer? → NO → SEQUENTIAL (layer dependencies)
    ↓ YES
Do they share data/outputs? → YES → SEQUENTIAL (data dependency)
    ↓ NO
Do they access shared resources? → YES → SEQUENTIAL (resource conflict)
    ↓ NO
Are prerequisites met for both? → NO → SEQUENTIAL (wait for prereqs)
    ↓ YES
PARALLEL - Invoke in same message
```

---

## Quick Reference: Agent Invocation Template

```
subagent_type: [agent-name]
description: [3-5 word summary]
prompt:
**Task:** [One sentence - what to do]

**Context:**
- Current work: [orchestration context]
- Layer status: [dependencies ready]
- Why this agent: [expertise needed]

**Requirements:**
1. [Requirement 1]
2. [Requirement 2]

**Infrastructure:**
- Server/IP: [if applicable]
- Dependencies: [what's needed]
- Configuration: [specifics]

**Expected Output:**
- [Deliverables]
- [Validation evidence]

**Quality Gates:**
- [How to verify success]

**Integration:**
- [What other agents need from this]
```

---

## Related Documentation

- **HANA-X-ORCHESTRATION.md** - Complete orchestration reference
- **HANA-X-QUICK-REF.md** - Quick lookup patterns
- **CLAUDE.md** - Agent Zero field manual
- **Agent Catalog** - `0.0-governance/0.0.5-Delivery/0.0.5.1-agents/0.0.5.1.0-agent-catalog.md`

---

**Version:** 1.0
**Last Updated:** 2025-11-10
**Status:** ACTIVE - Operational Reference
**Next Review:** 2025-12-10

---

*Quality = Accuracy > Speed > Efficiency*
*Clear invocation = Successful orchestration*
