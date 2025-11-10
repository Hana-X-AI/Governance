# Hana-X Troubleshooting Playbook

**Document Type:** Operational Reference - Diagnostic Guide
**Created:** 2025-11-10
**Purpose:** Layer-based troubleshooting procedures for Hana-X infrastructure
**Audience:** Agent Zero, Specialist Agents
**Classification:** Internal - Governance

---

## Overview

This playbook provides **systematic troubleshooting procedures** for diagnosing and resolving issues across the Hana-X infrastructure. Organized by architecture layer for fast problem identification and resolution.

**Key Principle:** Start at the lowest affected layer and work upward.

---

## Quick Triage Decision Tree

```
ISSUE REPORTED
    ↓
Can you access ANY service? → NO → Layer 1 (Foundation)
    ↓ YES
Can you authenticate? → NO → Layer 1 (Identity & Trust)
    ↓ YES
Is it a model/LLM issue? → YES → Layer 2 (Model & Inference)
    ↓ NO
Is it a database/cache issue? → YES → Layer 3 (Data Plane)
    ↓ NO
Is it an agent/MCP issue? → YES → Layer 4 (Agentic & Toolchain)
    ↓ NO
Is it an application issue? → YES → Layer 5 (Application)
    ↓ NO
Is it monitoring/CI/CD? → YES → Layer 6 (Integration & Governance)
```

---

## Layer 1: Identity & Trust (Foundation)

**Common Symptoms:**
- Cannot reach any services
- Authentication failures across multiple services
- DNS resolution failures
- SSL certificate errors
- "Permission denied" errors

### Issue: DNS Resolution Failure

**Symptoms:**
- Hostnames don't resolve (e.g., `hx-postgres-server.hx.dev.local`)
- `ping` by hostname fails, but `ping` by IP succeeds
- Services can't find each other by name

**Diagnostic Commands:**
```bash
# Test DNS resolution
nslookup hx-postgres-server.hx.dev.local 192.168.10.200
dig @192.168.10.200 hx-postgres-server.hx.dev.local

# Check DNS server status (Samba AD DC integrated DNS)
ssh hx-samba-ad-dc "systemctl status samba-ad-dc"
```

**Resolution:**
1. Invoke frank: "Diagnose DNS resolution for [hostname]"
2. Frank checks:
   - DNS service running on hx-samba-ad-dc (Samba AD DC)
   - A record exists in AD-integrated zone
   - Reverse DNS configured in AD
3. Frank resolves and validates
4. Re-test DNS resolution

**Prevention:**
- Ensure all new services register DNS via Frank
- Monitor Samba AD DC service health (nathan)

---

### Issue: Samba DC Authentication Failure

**Symptoms:**
- LDAP bind failures
- Kerberos authentication errors
- Service accounts can't authenticate
- Domain join failures

**Diagnostic Commands:**
```bash
# Test LDAP connectivity
ldapsearch -x -H ldap://192.168.10.200 -b "dc=hx,dc=dev,dc=local"

# Check Kerberos tickets
klist

# Test service account
kinit postgres_service@HX.DEV.LOCAL
```

**Resolution:**
1. Invoke frank: "Diagnose Samba DC authentication for [service/user]"
2. Frank checks:
   - Samba AD DC operational
   - Account exists in AD and is not locked
   - Password not expired
   - Kerberos tickets valid
3. Frank resolves (reset password, unlock account, etc.)
4. Re-test authentication

**Prevention:**
- Regular password rotation with tracking
- Monitor account lockout events in Samba AD DC
- Automate service account management (amanda)

---

### Issue: SSL Certificate Errors

**Symptoms:**
- "Certificate not trusted" warnings
- "Certificate expired" errors
- HTTPS connections fail
- Certificate hostname mismatch

**Diagnostic Commands:**

**For PostgreSQL SSL Verification (Port 5432):**
```bash
# Verify PostgreSQL TLS/SSL connection using psql
# This shows actual SSL negotiation status from PostgreSQL's perspective
PGSSLMODE=require psql -h hx-postgres-server.hx.dev.local -U postgres -d postgres -c '\conninfo'

# Expected output should include:
#   SSL connection (protocol: TLSv1.3, cipher: TLS_AES_256_GCM_SHA384, bits: 256, compression: off)
# Or similar SSL details confirming encrypted connection

# Alternative: Test SSL requirement enforcement
PGSSLMODE=require psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT version();"
# If SSL is properly configured, connection succeeds
# If SSL fails, you'll see: "FATAL: no pg_hba.conf entry for host ... SSL off"

# Verify SSL is enforced (connection should fail without SSL)
PGSSLMODE=disable psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"
# Expected: Connection failure if SSL is required

# Check PostgreSQL server SSL configuration
ssh hx-postgres-server.hx.dev.local "sudo -u postgres psql -c 'SHOW ssl;'"
# Expected: ssl = on
```

**For HTTPS/Web Services Certificate Verification (Port 443):**
```bash
# Check HTTPS certificate validity
openssl s_client -connect n8n.hx.dev.local:443 -servername n8n.hx.dev.local -showcerts

# Check certificate expiration for web services
echo | openssl s_client -servername n8n.hx.dev.local \
  -connect n8n.hx.dev.local:443 2>/dev/null | \
  openssl x509 -noout -dates

# Check subject and issuer
echo | openssl s_client -servername n8n.hx.dev.local \
  -connect n8n.hx.dev.local:443 2>/dev/null | \
  openssl x509 -noout -subject -issuer
```

**For PostgreSQL Certificate Expiration (Separate Check):**
```bash
# Check PostgreSQL server certificate file directly
ssh hx-postgres-server.hx.dev.local \
  "sudo openssl x509 -in /var/lib/postgresql/server.crt -noout -dates"

# Check PostgreSQL certificate details
ssh hx-postgres-server.hx.dev.local \
  "sudo openssl x509 -in /var/lib/postgresql/server.crt -noout -subject -issuer -dates"
```

**Resolution:**
1. Invoke frank: "Check SSL certificate for [service].hx.dev.local"
2. Frank validates:
   - Certificate issued by correct CA
   - Not expired
   - Hostname matches
   - Certificate chain complete
3. Frank reissues if needed
4. Restart affected service to load new certificate

**Prevention:**
- Monitor certificate expiration (nathan)
- Automate certificate renewal (amanda)
- 30-day expiration warnings

---

### Issue: Ubuntu Server Not Accessible

**Symptoms:**
- Cannot SSH to server
- Ping fails
- Server not responding

**Diagnostic Commands:**
```bash
# Test connectivity
ping 192.168.10.XXX

# Test SSH
ssh -v user@192.168.10.XXX

# Check from hypervisor
# (if VM) check console access
```

**Resolution:**
1. Invoke william: "Diagnose connectivity to [server-name] (192.168.10.XXX)"
2. William checks:
   - Server powered on (if VM)
   - Network interface up
   - Firewall rules
   - SSH service running
   - Resource exhaustion (CPU, memory, disk)
3. William resolves (restart services, adjust firewall, etc.)
4. Re-test connectivity

**Prevention:**
- Monitor server health (nathan)
- Regular resource checks
- Automated recovery scripts (amanda)

---

## Layer 2: Model & Inference

**Common Symptoms:**
- LLM responses slow or failing
- Model loading errors
- Routing issues
- High latency

### Issue: Ollama Model Not Responding

**Symptoms:**
- Model requests timeout
- "Model not found" errors
- Ollama service not responding

**Diagnostic Commands:**
```bash
# Test Ollama endpoint
curl http://192.168.10.204:11434/api/tags

# Check Ollama service
ssh hx-ollama-01 "systemctl status ollama"

# Test model inference
ollama run llama2 "Hello world"
```

**Resolution:**
1. Invoke patricia: "Diagnose Ollama model [model-name] on [server]"
2. Patricia checks:
   - Ollama service running
   - Model downloaded and available
   - GPU/CPU resources
   - Memory sufficient for model
3. Patricia resolves (restart service, download model, etc.)
4. Re-test inference

**Prevention:**
- Pre-load frequently used models
- Monitor resource usage (nathan)
- Load balancing across cluster

---

### Issue: LiteLLM Routing Failure

**Symptoms:**
- Requests not reaching correct model
- Fallback not working
- Rate limiting incorrect

**Diagnostic Commands:**
```bash
# Test LiteLLM endpoint
curl -X POST http://192.168.10.212:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gpt-3.5-turbo", "messages": [{"role": "user", "content": "test"}]}'

# Check LiteLLM logs
ssh hx-litellm "journalctl -u litellm -n 50"
```

**Resolution:**
1. Invoke maya: "Diagnose LiteLLM routing for [model]"
2. Maya checks:
   - Routing configuration correct
   - Backend models accessible
   - Rate limiting configured properly
   - Fallback chain working
3. Maya resolves configuration
4. Re-test routing

**Prevention:**
- Regular routing configuration audits
- Monitor routing metrics (nathan)
- Test fallback chains

---

### Issue: LangGraph Agent Not Executing

**Symptoms:**
- Agent graphs not running
- State management issues
- Tool calling failures

**Diagnostic Commands:**
```bash
# Check LangGraph service
ssh hx-langgraph "systemctl status langgraph"

# Test graph endpoint
curl http://192.168.10.226:8000/health

# Check logs for errors
ssh hx-langgraph "tail -f /var/log/langgraph/app.log"
```

**Resolution:**
1. Invoke laura: "Diagnose LangGraph agent graph [graph-name]"
2. Laura checks:
   - Service running
   - Graph definition valid
   - Database connections (PostgreSQL for memory)
   - Tool availability
   - LLM connectivity
3. Laura resolves (fix graph, reconnect dependencies, etc.)
4. Re-test agent execution

**Prevention:**
- Validate graphs before deployment
- Monitor execution success rates (nathan)
- Regular dependency health checks

---

## Layer 3: Data Plane

**Common Symptoms:**
- Database connection failures
- Query timeouts
- Data not persisting
- Cache misses

### Issue: PostgreSQL Connection Failure

**Symptoms:**
- "Connection refused" errors
- Authentication failures
- Connection pool exhausted

**Diagnostic Commands:**
```bash
# Test connection
psql -h hx-postgres-server.hx.dev.local -U postgres_service -d production_db

# Check service status
ssh hx-postgres-server "systemctl status postgresql"

# Check connections
ssh hx-postgres-server "sudo -u postgres psql -c 'SELECT count(*) FROM pg_stat_activity;'"
```

**Resolution:**
1. Invoke quinn: "Diagnose PostgreSQL connection issues on [database]"
2. Quinn checks:
   - PostgreSQL service running
   - Max connections limit
   - Authentication configuration (pg_hba.conf)
   - Network connectivity
   - Disk space
3. Quinn resolves (adjust limits, fix auth, etc.)
4. Re-test connections

**Prevention:**
- Monitor connection pool usage (nathan)
- Set appropriate connection limits
- Regular vacuuming and maintenance
- Automated backup verification

---

### Issue: Redis Cache Not Responding

**Symptoms:**
- Cache operations timeout
- High cache miss rate
- Redis service down

**Diagnostic Commands:**
```bash
# Test Redis
redis-cli -h 192.168.10.210 ping

# Check memory usage
redis-cli -h 192.168.10.210 INFO memory

# Check service
ssh hx-redis "systemctl status redis"
```

**Resolution:**
1. Invoke samuel: "Diagnose Redis cache issues"
2. Samuel checks:
   - Redis service running
   - Memory limits
   - Eviction policy
   - Persistence settings
   - Network connectivity
3. Samuel resolves (restart, adjust config, etc.)
4. Re-test cache operations

**Prevention:**
- Monitor memory usage and evictions (nathan)
- Set appropriate TTLs
- Regular persistence snapshots
- Memory limit alerts

---

### Issue: Qdrant Vector Search Slow

**Symptoms:**
- Search queries timeout
- High latency
- Poor search results

**Diagnostic Commands:**
```bash
# Test Qdrant endpoint
curl http://192.168.10.207:6333/collections

# Check collection status
curl http://192.168.10.207:6333/collections/[collection-name]

# Check service
ssh hx-qdrant "systemctl status qdrant"
```

**Resolution:**
1. Invoke robert: "Diagnose Qdrant collection [collection-name] performance"
2. Robert checks:
   - Index optimization status
   - Vector dimensions correct
   - Distance metric appropriate
   - HNSW parameters tuned
   - Resource availability (CPU, RAM)
3. Robert resolves (reindex, optimize, tune params, etc.)
4. Re-test search performance

**Prevention:**
- Regular index optimization
- Monitor query latency (nathan)
- Appropriate collection sizing
- Batch insert optimization

---

## Layer 4: Agentic & Toolchain

**Common Symptoms:**
- MCP tools not available
- Worker services failing
- RAG pipeline broken

### Issue: FastMCP Gateway Not Responding

**Symptoms:**
- MCP tool calls fail
- Gateway timeout errors
- Tools not discovered

**Diagnostic Commands:**
```bash
# Test FastMCP endpoint
curl http://192.168.10.213:8000/health

# List available tools
curl http://192.168.10.213:8000/tools

# Check service
ssh hx-fastmcp "systemctl status fastmcp"
```

**Resolution:**
1. Invoke george: "Diagnose FastMCP gateway issues"
2. George checks:
   - Service running
   - Tool registration
   - Backend MCP servers accessible
   - Authentication working
   - Rate limiting not blocking
3. George resolves (restart, re-register tools, etc.)
4. Re-test tool availability

**Prevention:**
- Monitor gateway health (nathan)
- Regular tool registration audits
- Backend server health checks

---

### Issue: Crawl4ai Worker Failing

**Symptoms:**
- Web scraping jobs stuck
- Extraction errors
- Worker service down

**Diagnostic Commands:**
```bash
# Check worker service
ssh hx-crawl4ai "systemctl status crawl4ai-worker"

# Check job queue
curl http://192.168.10.219:8000/status

# Check logs
ssh hx-crawl4ai "tail -f /var/log/crawl4ai/worker.log"
```

**Resolution:**
1. Invoke Diana: "Diagnose Crawl4ai worker issues"
2. Diana checks:
   - Worker service running
   - Job queue status
   - Target site accessibility
   - Rate limiting compliance
   - Extraction rules valid
3. Diana resolves (restart, adjust rules, etc.)
4. Re-test scraping jobs

**Prevention:**
- Monitor job success rates (nathan)
- Respect robots.txt and rate limits
- Regular extraction rule validation

---

### Issue: LightRAG Knowledge Graph Incomplete

**Symptoms:**
- Missing entities or relationships
- Query results incomplete
- Graph construction errors

**Diagnostic Commands:**
```bash
# Check LightRAG service
ssh hx-lightrag "systemctl status lightrag"

# Query graph status
curl http://192.168.10.220:8000/graph/stats

# Check logs
ssh hx-lightrag "tail -f /var/log/lightrag/app.log"
```

**Resolution:**
1. Invoke marcus: "Diagnose LightRAG knowledge graph [graph-name]"
2. Marcus checks:
   - Service running
   - Vector database connectivity (Qdrant)
   - Entity extraction working
   - Relationship inference correct
   - Graph persistence
3. Marcus resolves (rebuild graph, fix extraction, etc.)
4. Re-test graph queries

**Prevention:**
- Regular graph integrity checks
- Monitor entity/relationship counts (nathan)
- Incremental updates vs full rebuilds

---

## Layer 5: Application

**Common Symptoms:**
- Frontend not loading
- API errors
- User authentication issues

### Issue: Frontend Application Not Loading

**Symptoms:**
- Blank page or 404 errors
- JavaScript errors in console
- API calls failing

**Diagnostic Commands:**
```bash
# Check web server
curl -I https://[app-name].hx.dev.local

# Check service (Next.js example)
ssh hx-nextjs "pm2 status"

# Check nginx
ssh hx-app-server "systemctl status nginx"
```

**Resolution:**
1. Identify frontend agent (victor for Next.js, hannah for CopilotKit, paul for Open WebUI, brian for AG-UI)
2. Invoke [agent]: "Diagnose frontend application [app-name]"
3. Agent checks:
   - Application server running
   - Build artifacts present
   - Environment variables correct
   - API endpoints accessible
   - SSL certificate valid
4. Agent resolves (rebuild, restart, fix config, etc.)
5. Re-test application

**Prevention:**
- Automated build and deployment (isaac)
- Health check endpoints
- Monitor uptime (nathan)

---

### Issue: N8N Workflow Not Executing

**Symptoms:**
- Workflows stuck or failing
- Trigger not firing
- Node execution errors

**Diagnostic Commands:**
```bash
# Check N8N service
ssh hx-n8n "systemctl status n8n"

# Access N8N UI
https://hx-n8n.hx.dev.local

# Check logs
ssh hx-n8n "tail -f /var/log/n8n/app.log"
```

**Resolution:**
1. Invoke omar: "Diagnose N8N workflow [workflow-name]"
2. Omar checks:
   - N8N service running
   - Workflow configuration
   - Node credentials valid
   - Trigger conditions met
   - Execution history for errors
3. Omar resolves (fix nodes, update creds, etc.)
4. Re-test workflow

**Prevention:**
- Regular workflow testing
- Monitor execution success rates (nathan)
- Credential expiration alerts

---

## Layer 6: Integration & Governance

**Common Symptoms:**
- CI/CD pipeline failures
- Test failures
- Monitoring gaps

### Issue: GitHub Actions Pipeline Failing

**Symptoms:**
- Builds failing
- Tests not running
- Deployment blocked

**Diagnostic Steps:**
1. Check GitHub Actions UI for error logs
2. Identify failing step
3. Review recent changes to workflow files

**Resolution:**
1. Invoke isaac: "Diagnose GitHub Actions pipeline [workflow-name]"
2. Isaac checks:
   - Workflow syntax
   - Secrets/environment variables
   - Runner availability
   - Dependency issues
   - Test failures
3. Isaac resolves (fix workflow, update secrets, etc.)
4. Re-run pipeline

**Prevention:**
- Test workflows in branches first
- Monitor pipeline success rates
- Regular dependency updates

---

### Issue: Tests Failing

**Symptoms:**
- Unit tests fail
- Integration tests fail
- E2E tests timeout

**Resolution:**
1. Invoke julia: "Diagnose test failures in [test-suite]"
2. Julia checks:
   - Test environment setup
   - Dependencies available
   - Test data present
   - Service connectivity
   - Test logic errors
3. Julia resolves (fix tests, update mocks, etc.)
4. Re-run test suite

**Prevention:**
- Regular test maintenance
- Monitor test coverage
- Fail early on broken tests

---

### Issue: Monitoring Gaps

**Symptoms:**
- Missing metrics
- Alerts not firing
- Dashboards broken

**Resolution:**
1. Invoke nathan: "Diagnose monitoring for [service/metric]"
2. Nathan checks:
   - Metrics collection agents running
   - Data pipeline functional
   - Alert rules configured
   - Dashboard queries correct
3. Nathan resolves (fix collectors, update dashboards, etc.)
4. Verify metrics flowing

**Prevention:**
- Regular monitoring health checks
- Test alert rules
- Dashboard review and updates

---

## Cross-Layer Issues

### Issue: Complete Service Outage

**Symptoms:**
- Nothing works
- Multiple layers affected
- Network-wide issues

**Triage Process:**
1. Check Layer 1 first (can you reach Samba DC?)
2. If Layer 1 down: Invoke frank and william immediately
3. If Layer 1 up: Check next layer systematically
4. Document timeline of failures
5. Coordinate recovery across layers

**Resolution:**
- Layer 1 recovery FIRST (frank + william)
- Then restore Layer 2/3 (infrastructure)
- Then Layer 4 (agentic services)
- Then Layer 5 (applications)
- Finally Layer 6 (observability)

**Prevention:**
- Regular disaster recovery drills
- Automated backup verification
- Layer dependency documentation

---

## Escalation Protocols

### When to Escalate

Escalate to user after:
1. **Two failed resolution attempts** with same agent
2. **Layer 1 complete outage** (critical - immediate escalation)
3. **Unknown issues** not matching any playbook pattern
4. **Multi-layer cascade failures** (coordinate escalation)
5. **Security incidents** (immediate escalation)

### How to Escalate

Provide user with:
1. Clear problem description
2. Symptoms observed
3. Diagnostic steps taken
4. Agent(s) invoked and their findings
5. Current system state
6. Recommended next steps

---

## Diagnostic Command Reference

### Layer 1 (Identity & Trust)
```bash
# DNS
nslookup [hostname] 192.168.10.200
dig @192.168.10.200 [hostname]

# LDAP
ldapsearch -x -H ldap://192.168.10.200 -b "dc=hx,dc=dev,dc=local"

# Kerberos
klist
kinit [user]@HX.DEV.LOCAL

# SSL
openssl s_client -connect [host]:443 -showcerts

# SSH
ssh -v user@[host]
```

### Layer 2 (Model & Inference)
```bash
# Ollama
curl http://192.168.10.204:11434/api/tags
ollama list
ollama run [model] "test"

# LiteLLM
curl http://192.168.10.212:8000/health
curl http://192.168.10.212:8000/models

# LangGraph
curl http://192.168.10.226:8000/health
```

### Layer 3 (Data Plane)
```bash
# PostgreSQL
psql -h [host] -U [user] -d [database]
pg_isready -h [host]

# Redis
redis-cli -h [host] ping
redis-cli -h [host] INFO

# Qdrant
curl http://192.168.10.207:6333/collections
```

### Layer 4 (Agentic)
```bash
# FastMCP
curl http://192.168.10.213:8000/health
curl http://192.168.10.213:8000/tools

# Workers
systemctl status [service]
journalctl -u [service] -n 50
```

### Layer 5 (Application)
```bash
# Web apps
curl -I https://[app].hx.dev.local
systemctl status nginx

# Node apps
pm2 status
pm2 logs [app]
```

### Layer 6 (Integration)
```bash
# Monitoring
curl http://192.168.10.225:9090/metrics
systemctl status prometheus
```

---

## Related Documentation

- **HANA-X-ORCHESTRATION.md** - Agent orchestration workflows
- **AGENT-INVOCATION-EXAMPLES.md** - How to invoke agents for troubleshooting
- **Network Topology** - `0.0-governance/0.0.2-Archtecture/0.0.2.3-network-topology.md`
- **Agent Profiles** - `0.0-governance/0.0.5-Delivery/0.0.5.1-agents/`

---

**Version:** 1.0
**Last Updated:** 2025-11-10
**Status:** ACTIVE - Operational Playbook
**Next Review:** 2025-12-10

---

*Quality = Accuracy > Speed > Efficiency*
*Layer-aware troubleshooting = Faster resolution*
