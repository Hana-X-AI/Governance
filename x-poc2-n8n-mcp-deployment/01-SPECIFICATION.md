# POC-002 Specification: N8N MCP Native Deployment

**Work ID**: POC-002
**Type**: Simple
**Date**: 2025-11-06
**Author**: Agent Zero
**Specialist**: @agent-olivia (Olivia Chang)

---

## 1. Objective

Deploy N8N MCP server on hx-n8n-mcp-server (192.168.10.214) using **native installation** (Node.js + systemd) and validate Phase 1 core capabilities.

**Scope**: Phase 1 only - MCP protocol server + documentation tools (536 nodes, 2,500+ templates)

**Out of Scope** (Phase 2): N8N API integration, workflow management tools (16 additional tools)

---

## 2. Functional Requirements

### FR-001: Node.js Runtime Installation
**Description**: Install Node.js 20+ and NPM on hx-n8n-mcp-server
**Rationale**: N8N MCP requires Node.js runtime for execution
**Priority**: Critical
**Dependencies**: None

**Details**:
- Install Node.js 20.x LTS (latest stable)
- Verify NPM installation (comes with Node.js)
- Confirm versions: `node --version` >= 20.0.0, `npm --version` >= 9.0.0

### FR-002: N8N MCP Repository Installation
**Description**: Clone N8N MCP repository and install dependencies
**Rationale**: Source code needed for native deployment
**Priority**: Critical
**Dependencies**: FR-001 (Node.js installed)

**Details**:
- Clone repository to `/opt/n8n-mcp/` or `/srv/n8n-mcp/`
- Run `npm install` to install dependencies (from package.json)
- Run `npm run build` to compile TypeScript to JavaScript
- Verify build output in `dist/` directory

### FR-003: Service Configuration
**Description**: Create systemd service for N8N MCP server
**Rationale**: Systemd manages service lifecycle (start, stop, restart, enable)
**Priority**: Critical
**Dependencies**: FR-002 (N8N MCP installed)

**Details**:
- Create `/etc/systemd/system/n8n-mcp.service` unit file
- Configure service user (agent0 or dedicated n8nmcp user)
- Set working directory to N8N MCP installation path
- Configure environment variables:
  - `MCP_MODE=http` (HTTP mode for n8n integration - future)
  - `PORT=3000` (default MCP port)
  - `LOG_LEVEL=info` (operational logging)
  - `NODE_ENV=production`
- Set ExecStart to `/usr/bin/node /opt/n8n-mcp/dist/mcp/index.js`
- Enable auto-restart on failure

### FR-004: Service Deployment
**Description**: Enable and start N8N MCP service
**Rationale**: Make service operational and persistent across reboots
**Priority**: Critical
**Dependencies**: FR-003 (Service configured)

**Details**:
- Run `systemctl daemon-reload` to load new service
- Run `systemctl enable n8n-mcp` for boot persistence
- Run `systemctl start n8n-mcp` to start service
- Verify service status: `systemctl status n8n-mcp`

### FR-005: MCP Protocol Validation
**Description**: Verify MCP server responds on port 3000
**Rationale**: Confirm MCP protocol server is operational
**Priority**: Critical
**Dependencies**: FR-004 (Service started)

**Details**:
- Check port listening: `ss -tlnp | grep 3000`
- Test health endpoint: `curl http://localhost:3000/health` (if available)
- Test MCP endpoint: `curl http://localhost:3000/mcp` (should return protocol version)
- Verify process running: `ps aux | grep n8n-mcp`

### FR-006: Node Documentation Database Validation
**Description**: Verify N8N MCP node database accessible
**Rationale**: Core functionality - 536 n8n nodes documented
**Priority**: High
**Dependencies**: FR-005 (MCP server operational)

**Details**:
- Database file: `data/nodes.db` (SQLite)
- Expected size: ~15MB
- Expected records: 536 nodes with 99% property coverage
- Validation: Query node count, verify sample nodes exist

### FR-007: Logging and Monitoring
**Description**: Configure logging for operational support
**Rationale**: Troubleshooting and audit trail
**Priority**: Medium
**Dependencies**: FR-004 (Service running)

**Details**:
- Systemd journal logs: `journalctl -u n8n-mcp -f`
- Application logs: Check for log file configuration
- Log rotation: Ensure systemd handles log management

---

## 3. Non-Functional Requirements

### NFR-001: Performance
- Service start time: < 10 seconds
- MCP endpoint response time: < 500ms
- Node database query time: < 100ms average
- Memory usage: < 512MB under normal operation

### NFR-002: Reliability
- Service uptime: 99.9% target
- Automatic restart on failure (systemd)
- Graceful shutdown on SIGTERM
- No memory leaks during extended operation

### NFR-003: Security
- Service runs as non-root user (agent0 or n8nmcp)
- File permissions: 755 for executables, 644 for configs
- No exposed credentials in environment variables (Phase 1 - no N8N API key)
- Firewall: Port 3000 accessible only from HX network (192.168.10.x)

### NFR-004: Maintainability
- Service managed via systemd (standard Ubuntu tooling)
- Logs accessible via journalctl
- Version tracking: Document N8N MCP version deployed
- Rollback: Keep installation backup before updates

---

## 4. Acceptance Criteria

### AC-001: Node.js Installation Success
**Test**:
```bash
node --version
npm --version
```
**Expected**:
- Node.js version >= v20.0.0
- NPM version >= 9.0.0
**Status**: ⬜ Pending

---

### AC-002: N8N MCP Build Success
**Test**:
```bash
cd /opt/n8n-mcp
ls -la dist/mcp/index.js
```
**Expected**:
- `dist/` directory exists
- `dist/mcp/index.js` file exists (compiled JavaScript)
- Build exit code: 0 (no errors)
**Status**: ⬜ Pending

---

### AC-003: Systemd Service Active
**Test**:
```bash
systemctl status n8n-mcp
systemctl is-enabled n8n-mcp
```
**Expected**:
- Service status: `active (running)`
- Service enabled: `enabled`
- Uptime: > 0 seconds
- No errors in status output
**Status**: ⬜ Pending

---

### AC-004: MCP Port Listening
**Test**:
```bash
ss -tlnp | grep 3000
```
**Expected**:
- Port 3000 listening on 0.0.0.0 or 127.0.0.1
- Process: node (n8n-mcp)
**Status**: ⬜ Pending

---

### AC-005: MCP Protocol Response
**Test**:
```bash
curl -s http://localhost:3000/mcp
```
**Expected**:
- HTTP 200 OK
- Response body: JSON with `protocolVersion` field
- Example: `{"protocolVersion":"2024-11-05"}`
**Status**: ⬜ Pending

---

### AC-006: Node Database Present
**Test**:
```bash
ls -lh /opt/n8n-mcp/data/nodes.db
sqlite3 /opt/n8n-mcp/data/nodes.db "SELECT COUNT(*) FROM nodes;"
```
**Expected**:
- Database file exists
- File size: ~10-20MB
- Node count: 536 (or close to this number)
**Status**: ⬜ Pending

---

### AC-007: Service Logs Clean
**Test**:
```bash
journalctl -u n8n-mcp --since "5 minutes ago" | grep -i error
```
**Expected**:
- 0 ERROR level entries
- 0 FATAL entries
- Startup sequence logs present (INFO level)
- No exceptions or stack traces
**Status**: ⬜ Pending

---

### AC-008: Service Auto-Restart
**Test**:
```bash
# Kill process
sudo pkill -f n8n-mcp
sleep 5
# Check if restarted
systemctl status n8n-mcp
```
**Expected**:
- Service restarts automatically within 5 seconds
- Service status: `active (running)` after restart
- Uptime: < 10 seconds (recent restart)
**Status**: ⬜ Pending

---

## 5. Architectural Decisions

**Architectural Review**: Completed by @agent-alex (Alex Rivera) - See `02-ARCHITECTURAL-REVIEW.md`

### AD-001: Access Pattern - Hybrid Approach
**Decision**: Hybrid access pattern (Phase 1: Direct, Phase 2: Gateway integration)
**Date**: 2025-11-06
**Authority**: @agent-alex (Platform Architect)

**Phase 1**:
- **Direct access** on port 3000 (HX network internal only)
- Clients: Claude Code (testing), other MCP clients for development
- No gateway routing required

**Phase 2** (Future):
- **Hybrid routing**: Direct for N8N worker (performance), gateway for AI assistants (standardization)
- FastMCP gateway integration (@agent-george)
- ADR required: "FastMCP Bypass Pattern for N8N Worker-MCP Communication"

**Rationale**: Follows MCP pattern (standardization) and routing pattern (specialization), architectural precedent in Document 0.3 Section 3.5 "LiteLLM Bypass Patterns"

### AD-002: Layer Placement - Compliant
**Decision**: N8N MCP in Layer 4 (Agentic & Toolchain)
**Status**: ✅ Compliant with Architecture Document 0.3

**Security Zone**: Agentic Zone (.213-.220, .228-.229)
**Network Topology**: No updates required for Phase 1

### AD-003: Multi-Client Access
**Decision**: Support multiple client types (N8N worker + AI assistants)
**Implementation**:
- Phase 1: AI assistants (Claude Code) for testing/validation
- Phase 2: N8N worker (direct, low-latency) + AI assistants (via FastMCP gateway)

**Architectural Compliance**: ✅ Cross-layer communication explicitly permitted (Document 0.3)

---

## 6. Out of Scope (Phase 2 Deferred)

The following are **explicitly out of scope** for Phase 1:

### OS-001: N8N API Integration
- N8N API URL configuration
- N8N API key setup
- 16 workflow management tools (n8n_create_workflow, n8n_list_workflows, etc.)
- **Reason**: N8N instance (hx-n8n-server:5678) not responding, requires coordination with @agent-omar

### OS-002: FastMCP Gateway Registration
- Registration with George Kim's FastMCP gateway
- MCP tool routing configuration
- Agent access via gateway
- **Reason**: Core MCP server must be operational first

### OS-003: SSL/TLS Configuration
- HTTPS support
- Certificate deployment
- TLS termination
- **Reason**: Not required for Phase 1 testing (localhost/internal access)

### OS-004: Domain Service Account
- Create n8nmcp@hx.dev.local service account
- Kerberos/LDAP integration
- **Reason**: Not required for Phase 1 (agent0 user sufficient)

### OS-005: Advanced Monitoring
- Prometheus metrics
- Grafana dashboards
- Alert configuration
- **Reason**: Basic systemd monitoring sufficient for Phase 1

---

## 6. Dependencies

### External Dependencies
| Dependency | Status | Owner | Impact |
|------------|--------|-------|--------|
| Node.js 20+ availability | ⬜ Not installed | @agent-william (OS) | CRITICAL - blocks deployment |
| N8N instance operational | ⚠️ Not responding | @agent-omar | LOW - Phase 2 only |
| Git (already installed) | ✅ Installed | N/A | NONE |

### Internal Dependencies
| Item | Depends On | Status |
|------|-----------|--------|
| Repository clone | Node.js installed | ⬜ Pending |
| NPM build | Repository cloned | ⬜ Pending |
| Service creation | Build complete | ⬜ Pending |
| Service start | Service created | ⬜ Pending |
| Validation | Service running | ⬜ Pending |

---

## 7. Risk Assessment

### Risk 1: Node.js Installation Conflicts
**Probability**: Low
**Impact**: Medium
**Mitigation**: Use NodeSource repository (official), verify no existing Node.js installations

### Risk 2: Build Failures
**Probability**: Low
**Impact**: High
**Mitigation**: Use stable N8N MCP release tag (not main branch), verify all dependencies install

### Risk 3: Port 3000 Conflict
**Probability**: Low
**Impact**: Medium
**Mitigation**: Verify port availability before deployment (`ss -tlnp | grep 3000`)

### Risk 4: Service User Permissions
**Probability**: Medium
**Impact**: Medium
**Mitigation**: Use agent0 user (already has sudo access), verify file ownership

### Risk 5: Memory Constraints
**Probability**: Very Low
**Impact**: Low
**Mitigation**: Server has 31GB RAM (97% free), N8N MCP uses < 512MB typical

---

## 8. Rollback Plan

If deployment fails or service does not start:

1. **Stop service**: `sudo systemctl stop n8n-mcp`
2. **Disable service**: `sudo systemctl disable n8n-mcp`
3. **Remove service file**: `sudo rm /etc/systemd/system/n8n-mcp.service`
4. **Reload systemd**: `sudo systemctl daemon-reload`
5. **Optionally remove installation**: `sudo rm -rf /opt/n8n-mcp/`
6. **Optionally remove Node.js**: (only if installed for this POC) `sudo apt remove nodejs npm`

**Rollback Time**: < 5 minutes

---

## 9. Success Criteria

**POC-002 Phase 1 is successful when**:

✅ All 8 Acceptance Criteria pass (AC-001 through AC-008)
✅ N8N MCP service running and stable for > 1 hour
✅ MCP protocol endpoint responding correctly
✅ Node database accessible with 536+ nodes
✅ Service logs show no errors
✅ Service survives restart testing
✅ Documentation created on server (deployment record)
✅ POC completion summary written

**Minimum Viable Success** (if issues arise):
- Node.js installed
- N8N MCP built successfully
- Service starts and responds on port 3000
- At least 6 of 8 acceptance criteria pass

---

## 10. Installation Path

**Recommended**: `/opt/n8n-mcp/`

**Rationale**:
- `/opt/` is standard for third-party packages on Ubuntu
- Clear ownership and permissions management
- Separate from system packages
- Easy to find and maintain

**Alternative**: `/srv/n8n-mcp/` (if /opt/ has space constraints - not an issue here with 82GB free)

---

## 11. Version Selection

**N8N MCP Version**: Latest stable release (v2.21.1 from knowledge source)

**How to obtain**:
```bash
git clone https://github.com/czlonkowski/n8n-mcp.git /opt/n8n-mcp
cd /opt/n8n-mcp
git checkout tags/v2.21.1  # Pin to known stable version
```

**Rationale**: Use tagged release instead of `main` branch for stability

---

## 12. Post-Deployment Validation

After deployment, verify the following:

1. **Service Health**: `systemctl status n8n-mcp` - active (running)
2. **Process Running**: `ps aux | grep n8n-mcp` - node process visible
3. **Port Listening**: `ss -tlnp | grep 3000` - port bound
4. **MCP Endpoint**: `curl http://localhost:3000/mcp` - JSON response
5. **Logs Clean**: `journalctl -u n8n-mcp -n 50` - no errors
6. **Memory Usage**: `ps -o pid,user,%mem,command -p $(pgrep -f n8n-mcp)` - < 5% of 31GB
7. **Auto-Start**: `systemctl is-enabled n8n-mcp` - enabled
8. **Restart Test**: Kill process, verify auto-restart within 5 seconds

---

## 13. Documentation Requirements

**On Server** (per Server Documentation Standard v1.0):
- `/etc/n8n-mcp/` or `/opt/n8n-mcp/docs/`:
  - `DEPLOYMENT-POSTMORTEM.md` - Deployment summary
  - `n8n-mcp-config.md` - Service configuration details
  - `n8n-mcp_storage_config.md` - Data locations, log paths

**In Governance**:
- `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/`:
  - `03-EXECUTION-LOG.md` - Real-time execution log
  - `04-VALIDATION-REPORT.md` - AC validation results
  - `05-COMPLETION-SUMMARY.md` - POC summary and lessons learned

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-06 | Initial specification for native N8N MCP deployment (Phase 1) | Agent Zero |

---

**Document Location**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/01-SPECIFICATION.md`
**Status**: DRAFT (Phase 1)
**Next**: Create 02-TASK-LIST.md with detailed task breakdown

---

*"Knowledge-grounded specifications, native deployment, aim small miss small."*

**END OF SPECIFICATION**
