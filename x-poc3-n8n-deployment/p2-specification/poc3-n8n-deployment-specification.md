# Work Specification: POC3 N8N Workflow Automation Platform Deployment

**Created**: 2025-11-07
**Status**: Approved
**Orchestrating Agent**: @agent-zero
**Task Size**: Complex

---

## Summary

**What**: Deploy n8n workflow automation platform (v1.117.0 → v1.118.2 AS-BUILT) on bare-metal Ubuntu server using Node.js and pnpm monorepo build, with PostgreSQL backend, Nginx reverse proxy, and SSL/TLS security.

**Why**: Enable internal automation capabilities while maintaining total environmental control and data sovereignty. Provide teams with unlimited workflow automation without commercial limitations, operating entirely within Hana-X on-premise infrastructure.

**Expected Outcome**: Production-ready n8n service running at https://n8n.hx.dev.local, accessible via web UI, capable of executing unlimited workflows, with full database persistence, proper authentication, and operational documentation complete.

---

## Operational Context

### Systems Affected

| System/Service | Current State | Expected Change | Impact Level |
|----------------|---------------|-----------------|--------------|
| hx-n8n-server (192.168.10.215) | Fresh Ubuntu 22.04/24.04 | Node.js 22.x, n8n application, Nginx proxy | High - new service deployment |
| hx-postgres-server (192.168.10.209) | Running PostgreSQL | New database `n8n_poc3`, user `n8n_user` | Medium - new database/user |
| hx-freeipa-server (192.168.10.200) | Running Samba AD DC | DNS record, SSL certificate for n8n.hx.dev.local | Low - standard DNS/SSL |
| hx-redis-server (192.168.10.210) | Running Redis | Optional session storage configuration | Low - optional enhancement |

### Environment

- **Domain**: hx.dev.local
- **Criticality**: High (automation platform for enterprise workflows)
- **User Impact**: Significant (new capability enablement)
- **Downtime Required**: None (greenfield deployment)

### Dependencies

**Prerequisites**:
- Ubuntu 22.04 or 24.04 LTS server provisioned (hx-n8n-server)
- PostgreSQL ≥13.x operational on hx-postgres-server
- Samba AD DC operational for DNS/SSL services
- Network connectivity: 192.168.10.0/24 (all services reachable)

**External Dependencies**:
- n8n source repository at `/srv/knowledge/vault/n8n-master/` (v1.117.0 → v1.118.2 AS-BUILT)
- Node.js 22.x LTS packages from NodeSource repository
- pnpm 10.18.3 via corepack (Node.js bundled tool)
- System build dependencies: build-essential, python3, python3-pip, git, curl, ca-certificates, libcairo2-dev, libpango1.0-dev, libjpeg-dev, libgif-dev, librsvg2-dev, libpixman-1-dev, pkg-config, libpq-dev

**Infrastructure Needs**:
- DNS A record: n8n.hx.dev.local → 192.168.10.215
- SSL certificate from Samba CA for n8n.hx.dev.local
- Service account (optional, Enterprise Edition only for LDAP)
- Disk space: ≥20GB free on hx-n8n-server for build artifacts

**Blocking Work**: None (greenfield deployment, no dependencies on other work)

---

## Requirements

### Functional Requirements

- **FR-001: System Prerequisites**
  System/Service MUST have Ubuntu 22.04 or 24.04 LTS with Node.js ≥22.16.0, ≤24.x, pnpm 10.18.3 via corepack, and system build dependencies (build-essential, python3, python3-pip, git, curl, ca-certificates, libcairo2-dev, libpango1.0-dev, libjpeg-dev, libgif-dev, librsvg2-dev, libpixman-1-dev, pkg-config, libpq-dev) installed for n8n compilation.

- **FR-002: Database Backend**
  PostgreSQL database `n8n_poc3` MUST exist on hx-postgres-server with user `n8n_user` having CREATE, SELECT, INSERT, UPDATE, DELETE privileges for TypeORM schema migrations and workflow persistence.

- **FR-003: Build & Deploy**
  Complete monorepo build using `pnpm build:deploy` MUST compile all 30+ packages, deploy artifacts to `/opt/n8n/app/`, and create executable wrapper at `/opt/n8n/app/packages/cli/bin/n8n` with proper n8n user ownership.

- **FR-004: Service Configuration**
  Systemd service `n8n.service` MUST be configured with auto-restart policy (on-failure), environment variable file `/opt/n8n/.env` (100+ configuration variables), resource limits (MemoryMax=4G, LimitNOFILE=65536), and enabled for boot-time startup. Service MUST run as dedicated n8n system user created with: `sudo useradd -r -m -s /usr/sbin/nologin -d /opt/n8n -U n8n`.

- **FR-005: Network & Security**
  Nginx reverse proxy MUST provide SSL/TLS termination using Samba CA certificate for n8n.hx.dev.local, WebSocket upgrade headers for real-time workflow execution, HTTPS redirect (port 80→443), and proxy to localhost:5678 for n8n application.

- **FR-006: Authentication**
  Email/password authentication MUST be configured using n8n built-in authentication (no Enterprise license required), allowing first user account creation during initial setup with password complexity enforcement per n8n defaults.

  **Note**: Built-in email/password authentication is development-grade and appropriate for POC3 only. For production deployment, implement LDAP (requires n8n Enterprise Edition) or SSO integration (OAuth2/SAML). Built-in authentication lacks enterprise features: no centralized user management, no group-based access control, no password policy enforcement, no audit logging, and no multi-factor authentication (MFA).

- **FR-007: Database Integration**
  n8n MUST successfully connect to PostgreSQL on startup, execute TypeORM migrations for schema creation (50 tables AS-BUILT, spec estimated 20+), persist workflow definitions and execution history to database, and maintain connection pooling (≥10 connections).

- **FR-008: Web UI Accessibility**
  Web interface MUST be accessible at https://n8n.hx.dev.local with valid SSL certificate (no browser warnings), complete page load (no 404/500 errors), and support for WebSocket connections for real-time workflow execution feedback.

- **FR-009: Workflow Execution**
  System MUST successfully create and execute simple workflows (HTTP Request node, timer trigger), record execution history in PostgreSQL, display results in web UI, and handle workflow errors gracefully with proper logging.

- **FR-010: Configuration Management**
  Environment file `/opt/n8n/.env` MUST contain all critical configuration: database connection (DB_TYPE, DB_POSTGRESDB_HOST, etc.), network settings (N8N_HOST, N8N_PORT, WEBHOOK_URL), encryption key (N8N_ENCRYPTION_KEY - randomly generated 64-char hex), execution mode (EXECUTIONS_MODE=regular), and logging (N8N_LOG_LEVEL, N8N_LOG_OUTPUT). Encryption key MUST be backed up to 3+ secure locations before first startup: (1) local encrypted backup at `/opt/n8n/backups/.n8n-encryption-key.backup` (chmod 600, n8n user only), (2) password manager entry (KeePassXC/1Password/Bitwarden), and (3) offline/cloud secure storage (encrypted USB drive or organization's secure backup system).

### Non-Functional Requirements

- **NFR-001: Performance**
  Simple workflow execution time MUST be ≤5 seconds from trigger to completion, web UI page load ≤2 seconds, database query response time ≤100ms for workflow retrieval.

- **NFR-002: Reliability**
  Service uptime MUST target 100% during deployment validation (24 hours post-deployment monitoring), auto-restart on failure within 5 seconds (systemd RestartSec=5s), no critical errors in logs during validation period.

- **NFR-003: Security**
  All credentials MUST follow standard security (password: Major8859! for development environment), SSL/TLS MUST be enforced (HTTPS only, no HTTP access), encryption key MUST be randomly generated and backed up to secure location, service MUST run as non-root user (n8n system user).

- **NFR-004: Scalability**
  Initial deployment MUST support 10+ concurrent workflow executions, database connection pool ≥10 connections, system resources allocated: 4GB memory limit (MemoryMax=4G), 65536 file descriptors (LimitNOFILE=65536).

- **NFR-005: Build Performance**
  Initial compilation MUST complete within 45 minutes maximum (pnpm install: 15-30 min, pnpm build:deploy: 30-45 min), incremental builds ≤10 minutes if rebuild needed, disk I/O optimized for build performance.

### Operational Requirements

- **OR-001: Monitoring**
  Health check endpoint `/healthz` MUST respond to validate service status, systemd journal MUST capture all n8n logs (StandardOutput=journal, StandardError=journal), file logging to `/var/log/n8n/n8n.log` MUST be configured.

- **OR-002: Backup/Rollback**
  Encryption key MUST be backed up before first startup (CRITICAL - required for data recovery), database backup procedure MUST be documented, rollback procedure MUST restore service to pre-deployment state if validation fails.

- **OR-003: Documentation**
  Operational runbook MUST document start/stop/restart procedures, troubleshooting guide for common issues (service won't start, database connection failure, etc.), configuration reference for environment variables, and escalation path to @agent-zero.

- **OR-004: Validation**
  All 10 acceptance criteria MUST be validated before final sign-off, agent sign-off collected from all 7 agents (Frank, William, Quinn, Samuel, Omar, Olivia, George), lessons learned documented for future deployments.

- **OR-005: Service Management**
  Systemd service MUST be enabled for auto-start on boot (`systemctl enable n8n.service`), service status MUST be verifiable via `systemctl status n8n.service`, logs accessible via `journalctl -u n8n.service`.

---

## Acceptance Criteria

### Success Criteria

- [x] **AC-001: Web UI Accessibility**
  n8n web interface accessible at https://n8n.hx.dev.local with valid SSL certificate (no browser warnings), complete page load, no 404/500/network errors.

- [x] **AC-002: Workflow Execution**
  User can create first admin account during setup, login with email/password credentials, create new workflow in editor (HTTP Request node + timer trigger), execute workflow successfully, view execution in history.

- [x] **AC-003: Database Persistence**
  PostgreSQL connection verified on n8n startup, TypeORM migrations execute successfully (50 tables created AS-BUILT, spec estimated 20+), workflow executions persist to database, workflow data retrieval functional via SQL queries.

- [x] **AC-004: Session Management** (Optional if Redis configured)
  User login creates session in Redis DB 2, session persists across browser page refresh, session expires after configured timeout (configurable via N8N_SESSION_TIMEOUT).

- [x] **AC-005: Service Auto-Start**
  Systemd service enabled (`systemctl is-enabled n8n.service` returns "enabled"), service starts automatically after server reboot, service auto-restarts after kill signal (systemd Restart=on-failure policy).

- [x] **AC-006: WebSocket Support**
  Nginx reverse proxy has WebSocket upgrade headers configured (`proxy_http_version 1.1`, `Upgrade` and `Connection` headers set), real-time workflow execution updates appear in editor, no WebSocket errors in browser console.

- [x] **AC-007: Agent Sign-Off**
  @agent-frank signs off on DNS record validated and SSL certificate deployed, @agent-william on server provisioned and Nginx configured, @agent-quinn on database created and connection validated, @agent-samuel on Redis configured (if applicable), @agent-omar on application built and first startup successful, @agent-julia on all acceptance criteria validated.

- [x] **AC-008: Backup & Recovery**
  Encryption key backed up to secure location (verified location documented), database backup procedure documented in runbook, restoration test performed successfully (test database restored from backup).

- [x] **AC-009: Health Checks**
  Health check endpoint `/healthz` responds with 200 OK, service status reporting correctly via systemd (`systemctl status n8n.service` shows "active (running)"), basic metrics collected (service uptime, workflow execution count).

- [x] **AC-010: Runbook Documentation**
  Runbook document complete with start/stop/restart procedures, troubleshooting guide for common issues (5+ scenarios documented), configuration reference for environment variables (100+ vars documented), escalation path to @agent-zero documented.

### Validation Methods

| Criterion | Validation Method | Expected Result |
|-----------|-------------------|-----------------|
| AC-001 | Browser access test: `https://n8n.hx.dev.local` | Page loads, valid SSL cert, no errors |
| AC-001 | SSL validation: `openssl s_client -connect n8n.hx.dev.local:443` | Certificate validates to Samba CA |
| AC-001 | DNS resolution: `nslookup n8n.hx.dev.local` | Returns 192.168.10.215 |
| AC-002 | Manual workflow creation test via web UI | Workflow created, executed, result in history |
| AC-002 | First user creation during initial setup | Admin account created successfully |
| AC-003 | Database connection test: `psql -h 192.168.10.209 -U n8n_user -d n8n_poc3 -c "\dt"` | Lists 50 TypeORM tables (AS-BUILT) |
| AC-003 | Query execution history: `SELECT * FROM execution_entity LIMIT 10;` | Execution records retrieved |
| AC-004 | Redis session check: `redis-cli -h 192.168.10.210 SELECT 2 && KEYS *` | Session keys present after login |
| AC-005 | Reboot test: `sudo reboot && systemctl status n8n.service` | Service auto-started after reboot |
| AC-005 | Restart test: `sudo kill -9 $(pgrep -f 'node.*n8n') && sleep 5 && systemctl status n8n.service` | Service auto-restarted within 5 seconds |
| AC-006 | Nginx config check: `grep -A 5 'upgrade' /etc/nginx/sites-enabled/n8n.conf` | WebSocket headers present |
| AC-006 | Browser console WebSocket test during workflow execution | WebSocket connection established, no errors |
| AC-007 | Agent sign-off checklist completion | All 7 agents confirmed ✅ |
| AC-008 | Encryption key backup verification: `cat /opt/n8n/.env \| grep N8N_ENCRYPTION_KEY` | Key copied to secure backup location |
| AC-008 | Database backup test: `pg_dump -h 192.168.10.209 -U n8n_user n8n_poc3 > backup.sql` | Backup file created successfully |
| AC-009 | Health endpoint test: `curl -I https://n8n.hx.dev.local/healthz` | Returns 200 OK |
| AC-009 | Service status check: `systemctl status n8n.service` | Shows "active (running)" |
| AC-010 | Runbook completeness review against template | All sections complete, procedures tested |

---

## Scenarios & Testing

### Pre-Change Baseline

**Purpose**: Establish current state before n8n deployment (greenfield, no existing service)

1. **Baseline Test 1: Server Resources**
   - **Method**: Check disk space, memory, CPU availability on hx-n8n-server
   - **Command**: `df -h /` (disk), `free -h` (memory), `top` (CPU)
   - **Expected Result**: ≥20GB free disk, ≥4GB available memory, CPU idle >50%

2. **Baseline Test 2: Network Connectivity**
   - **Method**: Test connectivity to PostgreSQL, DNS, Redis from hx-n8n-server
   - **Command**: `ping 192.168.10.209`, `ping 192.168.10.200`, `ping 192.168.10.210`
   - **Expected Result**: All services reachable, ping time <10ms

3. **Baseline Test 3: Port Availability**
   - **Method**: Verify port 5678 (n8n), port 80/443 (Nginx) are available
   - **Command**: `sudo netstat -tuln | grep -E '5678|80|443'`
   - **Expected Result**: No processes listening on target ports

### Post-Change Validation

**Purpose**: Verify n8n deployment works as expected

1. **Validation Test 1: Service Startup**
   - **Given**: n8n systemd service configured and ready
   - **When**: Service started via `systemctl start n8n.service`
   - **Then**: Service status shows "active (running)", no errors in logs (`journalctl -u n8n.service`)

2. **Validation Test 2: Database Connection**
   - **Given**: PostgreSQL database `n8n_poc3` created with user `n8n_user`
   - **When**: n8n service starts and connects to database
   - **Then**: TypeORM migrations execute successfully, 50 tables created (AS-BUILT, spec estimated 20+), connection pool established

3. **Validation Test 3: Web UI Access**
   - **Given**: Nginx reverse proxy configured with SSL certificate
   - **When**: Browser accesses https://n8n.hx.dev.local
   - **Then**: n8n login page loads, SSL certificate valid (Samba CA), no browser warnings

4. **Validation Test 4: Workflow Creation**
   - **Given**: Admin user logged into n8n web UI
   - **When**: User creates workflow with HTTP Request node and timer trigger
   - **Then**: Workflow saved to database, workflow ID generated, workflow appears in workflow list

5. **Validation Test 5: Workflow Execution**
   - **Given**: Workflow created with HTTP Request node
   - **When**: User manually executes workflow via "Execute Workflow" button
   - **Then**: Workflow executes successfully, result appears in execution history, WebSocket updates show real-time progress

6. **Validation Test 6: Service Auto-Restart**
   - **Given**: n8n service running successfully
   - **When**: Service process killed via `kill -9 $(pgrep -f 'node.*n8n')`
   - **Then**: Systemd auto-restarts service within 5 seconds, service recovers without manual intervention

### Edge Cases & Error Scenarios

- **Edge Case 1: What happens when database is unreachable during startup?**
  - **Expected**: n8n fails to start with clear error message "Unable to connect to database", systemd restarts service after 5 seconds, logs show database connection error with host/port details

- **Edge Case 2: What happens when encryption key is missing from .env?**
  - **Expected**: n8n generates new encryption key on first startup, logs warning about new key generation, existing encrypted data becomes unreadable (critical for migrations, not applicable for greenfield)

- **Edge Case 3: What happens when Nginx WebSocket proxy is misconfigured?**
  - **Expected**: Workflow editor loads but real-time execution updates fail, browser console shows WebSocket connection errors (ws:// or wss:// failed), workflows execute but status updates delayed

- **Edge Case 4: What happens when disk space exhausted during build?**
  - **Expected**: `pnpm install` or `pnpm build:deploy` fails with "ENOSPC: no space left on device", build artifacts incomplete, clean disk space required before retry

- **Edge Case 5: What happens when Node.js version is below 22.16.0?**
  - **Expected**: `pnpm install` fails with error "Unsupported Node.js version", package.json engines field enforces version requirement, upgrade to Node.js 22.x required

- **Edge Case 6: What happens when first user creation fails?**
  - **Expected**: n8n shows setup wizard on next login attempt, database transaction rolled back (no partial user record), user can retry setup with different credentials

- **Edge Case 7: What happens when PostgreSQL user lacks CREATE privilege?**
  - **Expected**: TypeORM migrations fail with "permission denied" error on first startup, n8n service fails to start, logs show specific SQL permission error, database privileges must be corrected

---

## Success Metrics

### Performance Metrics

| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|
| **Build Duration (First)** | N/A | 30-45 min | Time `pnpm build:deploy` from start to completion |
| **Service Startup Time** | N/A | 12-17 seconds | Time from `systemctl start` to "Editor is now accessible" log message |
| **Workflow Execution Time** | N/A | <5 seconds | Execute simple workflow (HTTP Request node), measure time from trigger to completion |
| **Database Connection Pool** | N/A | ≥10 connections | Query PostgreSQL: `SELECT count(*) FROM pg_stat_activity WHERE datname='n8n_poc3';` |
| **Web UI Page Load** | N/A | <2 seconds | Browser developer tools: Time to interactive for https://n8n.hx.dev.local |
| **SSL Handshake Time** | N/A | <200ms | `openssl s_client -connect n8n.hx.dev.local:443` measure connection time |

### Business/Operational Metrics

| Metric | Current | Target | How to Measure |
|--------|---------|--------|----------------|
| **Agent Sign-off Completion** | 0/7 | 7/7 | Checklist tracking across all agent deliverables |
| **Acceptance Criteria Pass Rate** | 0/10 | 10/10 | Validation testing: all criteria PASS |
| **Documentation Completeness** | 0% | 100% | Runbook review: all sections complete, tested procedures |
| **Deployment Time (Total)** | N/A | 1.5-2 days | Wall-clock time from Phase 1 start to Phase 5 completion |
| **Critical Path Duration** | N/A | 8-12 hours | Optimized execution time with parallelization |
| **Zero Downtime Achievement** | N/A | 100% | No impact to existing services during deployment |

---

## Risks & Mitigations

### Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Build fails due to missing system dependencies** | Medium | High | Pre-install all dependencies (build-essential, python3, cairo, pango, libpq-dev) before build, verify with test compilation first |
| **PostgreSQL connection issues** | Low | High | Test database connectivity before deployment (`psql` connection test), verify credentials, ensure firewall allows TCP 5432, test connection string format |
| **Node.js version incompatibility** | Low | High | Install exact version 22.16.0+ via NodeSource repository, use `nvm` for version management if needed, validate with `node --version` before build |
| **pnpm build timeout/failure** | Medium | High | Allocate 45+ minutes for build process, monitor build logs in real-time, retry on network issues, verify disk space ≥20GB before starting |
| **SSL certificate configuration errors** | Low | Medium | Pre-generate certificate with correct SANs (n8n.hx.dev.local, hx-n8n-server.hx.dev.local), test with `openssl verify`, coordinate transfer with @agent-william for permissions |
| **Systemd service fails to start** | Medium | High | Test service file syntax with `systemd-analyze verify n8n.service`, verify file permissions (644 for .service, 600 for .env), check logs with `journalctl -u n8n.service` for errors |
| **Nginx WebSocket proxy misconfiguration** | Medium | Medium | Use tested config from deep-dive analysis, verify upgrade headers (`proxy_http_version 1.1`, `Upgrade`, `Connection`), test WebSocket in browser console |
| **Disk space exhaustion during build** | Low | High | Verify ≥20GB free space before build (`df -h`), monitor during process, clean unnecessary files if needed, alert if space <5GB remaining |
| **Encryption key backup missed** | Low | CRITICAL | Mandatory backup step in checklist (cannot proceed without), verify backup location documented, test backup restoration procedure |
| **TypeORM migration failures** | Low | High | Test database privileges before first startup (CREATE, SELECT, INSERT, UPDATE, DELETE), validate PostgreSQL version ≥13.x, review migration logs for errors |
| **Network firewall blocking n8n ports** | Low | Medium | Verify firewall rules allow TCP 5678 (localhost), TCP 80/443 (external), test with `telnet localhost 5678` before service start |

### Risk Severity Definitions

- **Probability**: Low (<20%), Medium (20-50%), High (>50%)
- **Impact**: Low (minor inconvenience), Medium (requires workaround), High (blocks deployment), Critical (data loss risk)

### Overall Risk Level: **MEDIUM**

**Assessment Rationale**:
- Most risks are Low probability with concrete mitigation strategies in place
- High-impact risks have proactive prevention steps (pre-installation checks, validation tests)
- Critical risk (encryption key backup) has mandatory safeguard in checklist (cannot proceed without)
- Greenfield deployment reduces risk (no existing service to break)
- Medium overall risk acceptable for POC3 with comprehensive planning and validation

### Rollback Criteria

When should we rollback to pre-deployment state?

- [x] Build fails after 2 attempts with different approaches
- [x] Service won't start after troubleshooting (database connection, configuration errors)
- [x] Critical errors in logs that cannot be resolved (TypeORM migration failures, authentication system errors)
- [x] Integration breaks (PostgreSQL unreachable, SSL certificate invalid, Nginx proxy errors)
- [x] Performance unacceptable (workflow execution >30 seconds, memory leaks, CPU >90%)
- [x] Acceptance criteria failures that cannot be remediated (3+ criteria fail validation)
- [x] Security vulnerabilities discovered during deployment (exposed credentials, SSL misconfiguration)

**Rollback Procedure**: See Phase 4 Execution Plan - Rollback section (stop service, disable systemd, optionally drop database, remove DNS record)

---

## Out of Scope

What is explicitly NOT included in this deployment:

- **LDAP Authentication Integration**: Requires n8n Enterprise Edition license (not available for POC3). Will use built-in email/password authentication instead (see FR-006 note: development-grade only, lacks centralized user management, group-based access control, password policy enforcement, audit logging, and MFA). LDAP integration with Samba AD DC can be added in future with Enterprise license.

- **Redis Queue Mode**: Initial deployment uses regular execution mode (no Redis dependency). Queue mode provides high-volume workflow execution scaling but adds complexity. Can be enabled in future if needed.

- **N8N MCP Server Integration**: MCP server deployment (40+ MCP tools, 536+ n8n nodes metadata) deferred to Phase 2 post-POC3 enhancement. Requires n8n API key from running instance (blocked by this deployment).

- **FastMCP Gateway Integration**: FastMCP gateway routing for N8N MCP tools deferred to Phase 2. Depends on N8N MCP server completion.

- **High Availability / Load Balancing**: Multi-node n8n deployment, distributed execution, load balancers excluded from POC3. Single-server deployment sufficient for initial use case.

- **Advanced Monitoring**: Prometheus metrics, Grafana dashboards, alerting infrastructure excluded. Basic health checks and systemd journal logging sufficient for POC3.

- **Custom Node Development**: Building custom n8n nodes for Hana-X integrations excluded. Will use built-in 400+ nodes initially.

- **Workflow Migration**: No existing n8n workflows to migrate (greenfield deployment).

- **Performance Optimization**: Advanced tuning (database query optimization, workflow execution parallelization) excluded from initial deployment. Baseline performance acceptable for POC3.

- **Multi-Environment Setup**: Separate dev/staging/production environments excluded. Single production-like environment for POC3.

---

## Questions & Clarifications

### Open Questions

All questions resolved during Phase 0 Discovery and Phase 1 Specification:

- [x] **Q1: Node.js version requirements?**
  - **Answer**: ≥22.16.0, ≤24.x (Node.js 22 LTS recommended from package.json engines field)
  - **Source**: Deep-dive analysis of n8n-master/package.json

- [x] **Q2: Build process for non-Docker deployment?**
  - **Answer**: Use pnpm 10.18.3 (strict requirement via corepack), run `pnpm install` then `pnpm build:deploy`
  - **Source**: n8n-master repository analysis, CONTRIBUTING.md

- [x] **Q3: PostgreSQL configuration specifics?**
  - **Answer**: PostgreSQL ≥13.x, create database `n8n_poc3`, user `n8n_user` with CREATE, SELECT, INSERT, UPDATE, DELETE privileges
  - **Source**: packages/@n8n/config/src/configs/database.config.ts analysis

- [x] **Q4: LDAP integration requirements?**
  - **Answer**: Requires n8n Enterprise Edition license (not available for POC3), use email/password auth instead
  - **Source**: packages/@n8n/config/src/configs/auth.config.ts, Enterprise Edition documentation

- [x] **Q5: Execution mode decision (regular vs queue)?**
  - **Answer**: Use regular mode (EXECUTIONS_MODE=regular) for POC3 simplicity, no Redis dependency
  - **Source**: Phase 0 Discovery, Phase 1 Specification, @agent-samuel analysis

- [x] **Q6: MCP integration scope?**
  - **Answer**: Defer to Phase 2 enhancement, focus on core n8n deployment first
  - **Source**: Phase 0 Discovery, Phase 2 Collaborative Planning

- [x] **Q7: Redis session storage required?**
  - **Answer**: Optional for POC3, n8n can use cookie-based sessions without Redis
  - **Source**: @agent-samuel planning analysis, n8n session management documentation

- [x] **Q8: Disk space requirements?**
  - **Answer**: ≥20GB free space for build artifacts (pnpm install: ~2GB node_modules, build: ~5GB dist/, total: ~10GB with buffer)
  - **Source**: Deep-dive analysis, build process testing estimates

### Assumptions

Document any assumptions being made:

1. **Samba AD DC provides valid SSL certificates**: Assuming Samba CA infrastructure operational and can issue certificates for n8n.hx.dev.local domain.

2. **PostgreSQL supports TypeORM version 0.3.20**: Assuming PostgreSQL ≥13.x compatibility with TypeORM (validated in n8n documentation).

3. **Network connectivity stable**: Assuming 192.168.10.0/24 network provides reliable connectivity between hx-n8n-server, hx-postgres-server, hx-freeipa-server during deployment.

4. **Build environment has internet access**: Assuming hx-n8n-server can reach npm registry (registry.npmjs.org) for `pnpm install` package downloads (~2000+ packages).

5. **No concurrent deployments**: Assuming no other services deploying simultaneously that could exhaust system resources (CPU, memory, disk I/O).

6. **Standard credentials acceptable**: Assuming development environment credentials (Major8859!) acceptable for POC3, production deployment would use stronger credentials.

7. **First build duration acceptable**: Assuming 30-45 minute build time acceptable for POC3 timeline (incremental builds faster at 5-10 minutes).

8. **Email/password auth sufficient**: Assuming built-in authentication adequate for POC3, LDAP/SSO can be added later with Enterprise Edition.

9. **Single-server deployment sufficient**: Assuming vertical scaling on single server adequate for POC3 workflow volume, horizontal scaling (multi-node) not needed initially.

---

## Related Work

### Prerequisites

**Infrastructure Prerequisites** (must complete before n8n deployment):
- Ubuntu 22.04 or 24.04 LTS server provisioned and accessible via SSH (hx-n8n-server)
- PostgreSQL ≥13.x operational on hx-postgres-server with admin access for database creation
- Samba AD DC operational for DNS/SSL services (hx-freeipa-server)
- Network connectivity verified: 192.168.10.0/24 network reachable from all systems

**No blocking work items** - This is a greenfield deployment with no dependencies on prior work.

### Follow-up Work

**Phase 2 Enhancements** (post-POC3 optional work):

1. **N8N MCP Server Integration** (3-5 days)
   - Deploy N8N MCP server on hx-n8n-mcp-server (192.168.10.214)
   - Configure 40+ MCP tools for n8n workflow integration
   - Initialize 536+ n8n nodes metadata SQLite database
   - Integrate with running n8n instance via API key
   - **Blocked by**: POC3 n8n deployment completion (requires running instance for API key)

2. **FastMCP Gateway Integration** (8-10 hours)
   - Register N8N MCP service in FastMCP gateway
   - Configure routing rules for n8n MCP tools
   - Integrate n8n tool catalog with FastMCP
   - Update FastMCP documentation
   - **Blocked by**: N8N MCP Server deployment completion

3. **Redis Queue Mode** (2-4 hours)
   - Configure Redis for queue mode (DB 1: queue, DB 2: session, DB 3: cache)
   - Update n8n environment variables (EXECUTIONS_MODE=queue, QUEUE_BULL_REDIS_HOST, etc.)
   - Test high-volume workflow execution
   - **Blocked by**: Decision to enable queue mode (optional enhancement)

4. **LDAP Authentication** (4-6 hours, requires Enterprise Edition license)
   - Acquire n8n Enterprise Edition license
   - Configure LDAP integration with Samba AD DC
   - Create service account n8n@hx.dev.local
   - Test LDAP authentication flow
   - **Blocked by**: Enterprise Edition license acquisition

5. **Advanced Monitoring** (6-8 hours)
   - Deploy Prometheus metrics exporter for n8n
   - Create Grafana dashboards for workflow execution, system resources
   - Configure alerting for service failures, performance degradation
   - **Blocked by**: Monitoring infrastructure decision

### Related Documentation

**Governance Documents**:
- [Phase 0: Discovery](/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/phase0-discovery.md) - Project scope, agents identified, technical findings
- [Phase 1: Specification](/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/phase1-specification.md) - High-level requirements, acceptance criteria, risks
- [Phase 2: Collaborative Planning](/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/phase2-collaborative-planning.md) - Task breakdown, dependencies, timeline
- [Phase 3: Execution Plan](/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/phase3-execution-plan.md) - Step-by-step execution sequence
- [Agent Constitution](/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.0-agent-constitution.md) - Quality standards, coordination protocols

**Technical Documentation**:
- [N8N Deep Dive Analysis](/srv/cc/Governance/x-poc3-n8n-deployment/x-docs/n8n-master-deep-dive-analysis.md) - Comprehensive technical analysis of n8n repository
- [Agent Planning Analyses](/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-*-planning-analysis.md) - Detailed planning from all 7 agents
- [Naming Standards](/srv/cc/Governance/0.0-governance/0.0.1-Planning/0.0.1.0-naming-standards.md) - Governance file naming conventions
- [Development Standards](/srv/cc/Governance/0.0-governance/0.0.3-Development/development-and-coding-standards.md) - SOLID principles, code quality

**Platform Documentation**:
- [Ecosystem Architecture](/srv/cc/Governance/0.0-governance/0.0.2-Architecture/0.0.2.2-ecosystem-architecture.md) - Hana-X 6-layer architecture
- [Platform Nodes](/srv/cc/Governance/0.0-governance/0.0.2-Architecture/platform-nodes.md) - Server inventory, IP addresses
- [Network Topology](/srv/cc/Governance/0.0-governance/0.0.2-Architecture/network-topology.md) - Network architecture

---

## Approval & Sign-off

### Stakeholder Approval

| Stakeholder | Role | Approval Status | Date |
|-------------|------|-----------------|------|
| @agent-frank | Samba AD DC/DNS/SSL Owner | Pending | - |
| @agent-william | Ubuntu Server/Infrastructure Owner | Pending | - |
| @agent-quinn | PostgreSQL Database Owner | Pending | - |
| @agent-samuel | Redis Cache/Queue Owner | Pending | - |
| @agent-omar | N8N Application Owner | Pending | - |
| @agent-julia | Testing & QA Lead | Pending | - |
| @agent-zero | Universal PM Orchestrator | Approved | 2025-11-07 |

**Approval Process**: All agents review specification during Phase 3 Alignment Checkpoint, provide formal sign-off before Phase 4 Execution begins.

---

## Review Checklist

Before proceeding to Phase 3 Alignment and Phase 4 Execution, verify:

**Completeness**:
- [x] All mandatory sections completed (Summary, Context, Requirements, Acceptance Criteria, Success Metrics, Risks)
- [x] Requirements are specific and testable (10 functional, 5 non-functional, 5 operational requirements defined)
- [x] Acceptance criteria are measurable (10 criteria with clear validation methods)
- [x] Success metrics defined for medium/complex tasks (6 performance metrics, 6 operational metrics)
- [x] Risks identified and mitigations planned (11 risks with probability, impact, mitigation)

**Clarity**:
- [x] No ambiguous language (all requirements use MUST, specifications concrete)
- [x] All assumptions documented (9 assumptions listed in Questions & Clarifications)
- [x] Ambiguous language removed (no "should", "might", "perhaps")
- [x] Every stakeholder understands the work (all 7 agents identified, roles clear)

**Quality**:
- [x] Acceptance criteria cover all requirements (10 AC map to 20 requirements)
- [x] Test plan validates all acceptance criteria (validation methods table complete)
- [x] Rollback plan exists (documented in Phase 4 Execution Plan, criteria defined)
- [x] Edge cases considered (7 edge cases documented with expected behavior)
- [x] Related work identified (prerequisites, follow-up work, related documentation)

**Alignment**:
- [x] Aligns with Hana-X Constitution principles (Quality Over Speed, SOLID OOP, Multi-Agent Coordination)
- [x] All affected agents identified (7 agents: Frank, William, Quinn, Samuel, Omar, Julia, Zero)
- [x] Infrastructure dependencies clear (DNS, SSL, PostgreSQL, Node.js, pnpm)
- [x] Documentation plan exists (runbook, operational procedures, troubleshooting guide)

---

## Document Metadata

```yaml
work_item: POC3 N8N Workflow Automation Platform Deployment
created_by: @agent-zero
created_date: 2025-11-07
last_updated: 2025-11-07
status: Approved
task_size: Complex
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.7-work-spec-template.md
methodology: /srv/cc/Governance/0.0-governance/0.4-hx-work-methodology.md
input_documents:
  - phase0-discovery.md
  - phase1-specification.md
  - phase2-collaborative-planning.md
  - phase3-execution-plan.md
  - agent-frank-planning-analysis.md
  - agent-william-planning-analysis.md
  - agent-quinn-planning-analysis.md
  - agent-samuel-planning-analysis.md
  - agent-omar-planning-analysis.md
  - agent-olivia-planning-analysis.md
  - agent-george-planning-analysis.md
  - phase2-planning-summary.md
  - n8n-master-deep-dive-analysis.md
agents_involved: 7
primary_agents: 4
supporting_agents: 2
deferred_agents: 2
estimated_duration: 1.5-2 days (10-14 hours with parallelization)
critical_path: 8-12 hours
deployment_model: Bare-metal installation via compiled build
out_of_scope_items: 5
acceptance_criteria_count: 10
success_metrics_count: 12
risks_identified: 11
```

---

*Based on Hana-X Universal Work Methodology - See `/srv/cc/Governance/0.0-governance/0.4-hx-work-methodology.md`*

*Template Location: `/srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.7-work-spec-template.md`*

---

**Version**: 1.1
**Maintained By**: Agent Zero (Universal PM Orchestrator)
**Related Documents**:
- `phase0-discovery.md` - Discovery findings
- `phase1-specification.md` - Initial requirements
- `phase2-collaborative-planning.md` - Task breakdown
- `phase3-execution-plan.md` - Execution sequence
**Classification**: Internal - Project Planning
**Status**: Approved - Ready for Phase 3 Alignment Checkpoint
**Last Review**: 2025-11-07

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial POC3 n8n deployment specification | @agent-zero |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Added authentication limitations to FR-006. Documents that built-in email/password authentication is development-grade only, appropriate for POC3 but not production. Lists missing enterprise features: centralized user management, group-based access control, password policy enforcement, audit logging, and MFA. Updated Out of Scope section (line 351) with cross-reference to FR-006 limitations. | Claude Code |
