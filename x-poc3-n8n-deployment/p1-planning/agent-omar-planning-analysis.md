# Agent Omar Planning Analysis: N8N Application Deployment (POC3)

**Document Type**: Planning Analysis
**Created**: 2025-11-07
**Agent**: @agent-omar (Omar Rodriguez - N8N Workflow Worker Specialist)
**Project**: POC3 N8N Server Deployment - Phase 2: Collaborative Planning
**Classification**: Internal - Project Planning

---

## Document Metadata

```yaml
agent_name: Omar Rodriguez
agent_shortname: omar
invocation: "@agent-omar"
role: PRIMARY - N8N Application Deployment
server_assignment: hx-n8n-server.hx.dev.local (192.168.10.215)
phase: Phase 2 - Collaborative Planning
work_plan: /srv/cc/Governance/x-poc3-n8n-deployment/planning/work-plan.md
deep_dive_analysis: /srv/cc/Governance/x-poc3-n8n-deployment/x-docs/n8n-master-deep-dive-analysis.md
knowledge_source: /srv/knowledge/vault/n8n-master/
status: Active Planning
version: 1.0
```

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Knowledge Source Review](#2-knowledge-source-review)
3. [Responsibilities Analysis](#3-responsibilities-analysis)
4. [Deliverables](#4-deliverables)
5. [Dependencies](#5-dependencies)
6. [Task Breakdown](#6-task-breakdown)
7. [Timeline and Estimates](#7-timeline-and-estimates)
8. [Validation Criteria](#8-validation-criteria)
9. [SOLID Principles Application](#9-solid-principles-application)
10. [Risks and Mitigations](#10-risks-and-mitigations)
11. [Sign-off Criteria](#11-sign-off-criteria)

---

## 1. Executive Summary

### 1.1 Role Statement

I am the **PRIMARY agent** responsible for building and deploying the n8n workflow automation application on `hx-n8n-server.hx.dev.local` (192.168.10.215). My core responsibility spans from **source code compilation** through **first successful startup** of the n8n service.

### 1.2 Critical Understanding

Upon invocation, I have **reviewed my knowledge source** at `/srv/knowledge/vault/n8n-master/` and the comprehensive deep-dive analysis. Key findings:

- **Node.js Requirement**: ≥22.16.0, ≤24.x (Node.js 22 LTS recommended)
- **Package Manager**: pnpm 10.18.3 (strict requirement via corepack)
- **Build System**: Turbo-orchestrated monorepo with 30+ packages
- **Build Command**: `pnpm build:deploy` creates deployment artifacts
- **Executable**: `packages/cli/bin/n8n` (Node.js script wrapper)
- **Environment Variables**: 100+ configuration options
- **Build Duration**: 30-45 minutes (first build), 5-10 minutes (incremental)

### 1.3 Deployment Approach

**Selected Model**: Bare-metal installation via compiled build (Model 3 from analysis)

**Rationale**:
- Meets POC3 requirement for non-Docker deployment
- Provides full control over environment
- Native PostgreSQL integration
- Systemd service management
- Production-grade deployment pattern

### 1.4 Success Definition

**Application is successfully deployed when**:
1. ✅ n8n compiled artifacts deployed to `/opt/n8n/`
2. ✅ Systemd service `n8n.service` configured and enabled
3. ✅ Environment variables configured (100+ vars in `/opt/n8n/.env`)
4. ✅ Service starts successfully on first boot
5. ✅ Web UI accessible at `https://hx-n8n-server.hx.dev.local:5678`
6. ✅ PostgreSQL database connection verified
7. ✅ First user account created successfully

---

## 2. Knowledge Source Review

### 2.1 Repository Analysis Complete

**Source Location**: `/srv/knowledge/vault/n8n-master/`
**Version**: 1.117.0
**Review Status**: ✅ COMPLETE

**Key Files Analyzed**:
- `package.json` (root) - Build orchestration, Node.js requirements
- `packages/cli/package.json` - Application metadata, dependencies
- `packages/cli/bin/n8n` - CLI entry point and startup logic
- `packages/@n8n/config/src/configs/database.config.ts` - Database configuration
- `packages/@n8n/config/src/configs/auth.config.ts` - Authentication setup
- `packages/cli/src/ldap.ee/ldap.service.ee.ts` - LDAP integration (Enterprise)
- `docker/images/n8n/Dockerfile` - Reference for deployment patterns
- `CONTRIBUTING.md` - Development setup and build instructions

### 2.2 Critical Findings from Knowledge Source

#### Build System Requirements

```json
// From package.json (root)
{
  "engines": {
    "node": ">=22.16 <= 24.x",
    "pnpm": ">=10.18.3"
  },
  "packageManager": "pnpm@10.18.3"
}
```

**Implications**:
- Must use **exact** Node.js version range (coordinated with William)
- pnpm **must** be installed via corepack (not npm/standalone)
- Version enforcement is **strict** (startup will fail if violated)

#### Build Process Flow

```bash
# From scripts/build-n8n.mjs and package.json
pnpm install          # Downloads 2000+ packages
pnpm build:deploy     # Compiles all 30+ packages to dist/
```

**Output Locations**:
- Compiled code: `packages/cli/dist/`
- Executable: `packages/cli/bin/n8n`
- Dependencies: Bundled in `node_modules/` via pnpm workspaces

#### Environment Variable Architecture

**Critical Variables** (from `@n8n/config` package):

1. **Database Configuration** (18 variables)
   - `DB_TYPE=postgresdb`
   - `DB_POSTGRESDB_HOST`, `DB_POSTGRESDB_PORT`, `DB_POSTGRESDB_DATABASE`
   - `DB_POSTGRESDB_USER`, `DB_POSTGRESDB_PASSWORD`
   - Connection pooling, timeouts, SSL options

2. **Network Configuration** (12 variables)
   - `N8N_HOST=0.0.0.0`, `N8N_PORT=5678`, `N8N_PROTOCOL=https`
   - `WEBHOOK_URL`, `N8N_EDITOR_BASE_URL`

3. **Security Configuration** (8 variables)
   - `N8N_SECURE_COOKIE=true`, `N8N_SAMESITE_COOKIE=strict`
   - File access restrictions, encryption key management

4. **Performance & Execution** (10 variables)
   - Execution modes, data retention, timeout configuration

5. **Logging** (10 variables)
   - Log levels, output destinations, file locations

**Total**: 100+ configurable environment variables

#### Startup Process Analysis

From `packages/cli/bin/n8n`:

```javascript
#!/usr/bin/env node

// 1. Node.js version check (enforces >=22.16)
const satisfies = require('semver/functions/satisfies');
if (!satisfies(nodeVersion, supportedNodeVersions)) {
  process.exit(1);
}

// 2. Load .env file (dotenv)
require('dotenv').config();

// 3. Load configuration before TypeORM
require('../dist/config');

// 4. Execute command via DI container
const { CommandRegistry } = await import('../dist/command-registry.js');
await Container.get(CommandRegistry).execute();
```

**Implications for Configuration**:
- `.env` file loaded from **current working directory** (CWD)
- Must be present **before** service starts
- Configuration precedence: ENV vars > `.env` > defaults
- Config loading happens **before** TypeORM database connection

### 2.3 Deployment Pattern Selection

**Based on analysis of Section 3: Deployment Architecture** (Deep Dive Analysis):

| Model | Approach | Verdict | Reason |
|-------|----------|---------|--------|
| Model 1 | NPX Quick Start | ❌ NOT SUITABLE | Development only, ephemeral |
| Model 2 | Docker Container | ❌ NOT APPLICABLE | Violates bare-metal requirement |
| **Model 3** | **Bare-Metal Build** | **✅ SELECTED** | Production-grade, full control, native integration |

**Chosen Pattern**: Compile from source → Deploy artifacts → Systemd service

---

## 3. Responsibilities Analysis

### 3.1 Primary Responsibilities

As the N8N Workflow Worker Specialist, I am **PRIMARY** for:

#### R1: Repository Clone and Build Environment
- ✅ Clone n8n-master repository to build location
- ✅ Verify Node.js 22.x and pnpm 10.18.3 installed (coordinate with William)
- ✅ Install system build dependencies (build-essential, python3 - coordinate with William)

#### R2: Application Build Process
- ✅ Execute `pnpm install` (dependency installation)
- ✅ Execute `pnpm build:deploy` (compilation and packaging)
- ✅ Verify build output in `packages/cli/dist/`
- ✅ Monitor build duration and resource usage

#### R3: Application Deployment
- ✅ Deploy compiled artifacts to `/opt/n8n/app/`
- ✅ Create directory structure:
  ```
  /opt/n8n/
  ├── app/                    # Compiled application (from build)
  │   ├── bin/n8n             # Executable
  │   ├── dist/               # Compiled JavaScript
  │   └── node_modules/       # Dependencies
  ├── .n8n/                   # Data directory (runtime-created)
  │   ├── .encryption-key     # Auto-generated on first start
  │   └── .instance-id        # Auto-generated
  ├── .env                    # Environment configuration (I create)
  └── backups/                # Backup location
  ```
- ✅ Set correct ownership (`n8n:n8n` user - coordinate with William)
- ✅ Set correct permissions (700 for .n8n/, 755 for app/)

#### R4: Systemd Service Configuration
- ✅ Create `/etc/systemd/system/n8n.service` file
- ✅ Configure service to run as `n8n` user
- ✅ Set working directory to `/opt/n8n`
- ✅ Configure `EnvironmentFile=/opt/n8n/.env`
- ✅ Set restart policies and resource limits
- ✅ Enable security hardening (NoNewPrivileges, PrivateTmp, etc.)

#### R5: Environment Configuration (100+ Variables)
- ✅ Create comprehensive `/opt/n8n/.env` file with:
  - Database configuration (credentials from Quinn)
  - Network configuration (SSL details from Frank)
  - Security settings
  - Logging configuration
  - Performance tuning
- ✅ Document all non-default values
- ✅ Secure file permissions (600, owner n8n:n8n)

#### R6: First Startup and Validation
- ✅ Execute `systemctl daemon-reload`
- ✅ Execute `systemctl enable n8n`
- ✅ Execute `systemctl start n8n`
- ✅ Monitor startup logs (`journalctl -u n8n -f`)
- ✅ Verify TypeORM migrations execute successfully
- ✅ Verify web UI becomes accessible
- ✅ Create first admin user account

### 3.2 Responsibilities NOT Mine (Coordination Required)

#### William Taylor (@agent-william) - Ubuntu Server
- Node.js 22.x installation
- pnpm 10.18.3 installation via corepack
- System build dependencies (gcc, g++, make, python3)
- User account creation (`n8n:n8n`)
- Directory creation and ownership
- Nginx reverse proxy configuration
- Firewall rules (port 5678)

#### Quinn Davis (@agent-quinn) - PostgreSQL
- Database `n8n_poc3` creation
- User `n8n_user` with password
- Schema privileges (CREATE, INSERT, UPDATE, DELETE, SELECT)
- Connection pooling configuration
- Database ready **before** my first startup

#### Frank Lucas (@agent-frank) - Identity & Trust
- Service account `n8n@hx.dev.local` (if using LDAP - Enterprise only)
- DNS record `hx-n8n-server.hx.dev.local` → 192.168.10.215
- SSL certificate from Samba CA (for Nginx - William deploys)
- LDAP bind account (if Enterprise Edition licensed)

#### Samuel Wilson (@agent-samuel) - Redis
- Redis instance available (optional - for Bull queue mode)
- Connection details if used

#### Julia Santos (@agent-julia) - Testing & QA
- Functional validation post-deployment
- Workflow execution testing
- Integration testing with other services

---

## 4. Deliverables

### 4.1 Primary Deliverables

| Deliverable | Location | Format | Owner | Sign-off Criteria |
|------------|----------|--------|-------|------------------|
| **Built n8n Application** | `/opt/n8n/app/` | Compiled JS + node_modules | Omar | Build completes, all 30+ packages compiled |
| **Systemd Service File** | `/etc/systemd/system/n8n.service` | INI format | Omar | Service enabled, starts on boot |
| **Environment Configuration** | `/opt/n8n/.env` | Key-value pairs | Omar | 100+ variables configured, no errors on startup |
| **Running n8n Service** | systemd unit `n8n` | Active process | Omar | `systemctl status n8n` shows "active (running)" |
| **Accessible Web UI** | `https://hx-n8n-server.hx.dev.local:5678` | HTTP/HTTPS | Omar | Browser loads editor, no errors |
| **Admin User Account** | n8n database | Database record | Omar | Login successful with credentials |
| **Deployment Documentation** | `/srv/cc/Governance/x-poc3-n8n-deployment/x-docs/deployment-log.md` | Markdown | Omar | Complete record of build and deployment |

### 4.2 Supporting Deliverables

| Deliverable | Location | Purpose | Owner |
|------------|----------|---------|-------|
| **Build Log** | `/opt/n8n/build.log` | Troubleshooting reference | Omar |
| **Startup Log** | `/var/log/n8n/startup.log` | First startup validation | Omar |
| **Environment Template** | `/opt/n8n/.env.template` | Configuration reference | Omar |
| **Backup of Encryption Key** | `/opt/n8n/backups/.encryption-key.backup` | Disaster recovery | Omar |

---

## 5. Dependencies

### 5.1 Blocking Dependencies (MUST be complete before I start)

#### D1: Server Provisioned and Domain-Joined ✋ BLOCKER
- **Owner**: William Taylor (@agent-william)
- **Requirement**: `hx-n8n-server.hx.dev.local` online, domain-joined, SSH accessible
- **Verification**: `ssh n8n@hx-n8n-server.hx.dev.local` successful
- **Status**: TBD
- **Impact**: Cannot deploy without server

#### D2: Node.js 22.x Installed ✋ BLOCKER
- **Owner**: William Taylor (@agent-william)
- **Requirement**: `node --version` returns ≥22.16.0 and ≤24.x
- **Verification**: `node --version` output
- **Status**: TBD
- **Impact**: Build will fail without correct Node.js version

#### D3: pnpm 10.18.3 Installed ✋ BLOCKER
- **Owner**: William Taylor (@agent-william)
- **Requirement**: `pnpm --version` returns 10.18.3 (installed via corepack)
- **Verification**: `pnpm --version` output
- **Status**: TBD
- **Impact**: Build system requires exact pnpm version

#### D4: System Build Dependencies ✋ BLOCKER
- **Owner**: William Taylor (@agent-william)
- **Requirement**: `build-essential`, `python3`, `git` installed
- **Verification**: `gcc --version`, `make --version`, `python3 --version` all succeed
- **Status**: TBD
- **Impact**: Compilation will fail without build tools

#### D5: PostgreSQL Database Ready ✋ BLOCKER
- **Owner**: Quinn Davis (@agent-quinn)
- **Requirement**: Database `n8n_poc3` created, user `n8n_user` with full privileges
- **Verification**: `psql -h hx-postgres-server -U n8n_user -d n8n_poc3 -c "SELECT 1"`
- **Status**: TBD
- **Impact**: First startup will fail without database

#### D6: DNS Record Configured ✋ BLOCKER (for validation)
- **Owner**: Frank Lucas (@agent-frank)
- **Requirement**: `nslookup hx-n8n-server.hx.dev.local` resolves to 192.168.10.215
- **Verification**: `dig hx-n8n-server.hx.dev.local` returns A record
- **Status**: TBD
- **Impact**: Web UI access validation will fail

### 5.2 Non-Blocking Dependencies (Can proceed without, but affects final validation)

#### D7: SSL Certificate Deployed
- **Owner**: Frank Lucas (@agent-frank) + William Taylor (@agent-william)
- **Requirement**: Samba CA SSL certificate installed in Nginx
- **Verification**: `openssl s_client -connect hx-n8n-server.hx.dev.local:443`
- **Status**: TBD
- **Impact**: HTTPS access unavailable, but HTTP on port 5678 will work

#### D8: Nginx Reverse Proxy Configured
- **Owner**: William Taylor (@agent-william)
- **Requirement**: Nginx proxying `https://hx-n8n-server.hx.dev.local` → `http://127.0.0.1:5678`
- **Verification**: `curl https://hx-n8n-server.hx.dev.local/healthz`
- **Status**: TBD
- **Impact**: Direct access via `:5678` port will work, but production URL won't

#### D9: Redis Available (Optional)
- **Owner**: Samuel Wilson (@agent-samuel)
- **Requirement**: Redis accessible at `hx-redis-server:6379`
- **Verification**: `redis-cli -h hx-redis-server ping`
- **Status**: TBD
- **Impact**: Can deploy without Redis (use `EXECUTIONS_MODE=regular` instead of `queue`)

### 5.3 Dependency Timeline

```
PHASE 0: Infrastructure Foundation (William + Frank + Quinn)
├─ William: Server provisioned, domain-joined
├─ William: Node.js 22.x + pnpm 10.18.3 installed
├─ William: Build tools installed
├─ William: User n8n:n8n created
├─ Quinn: Database n8n_poc3 created
├─ Frank: DNS record configured
└─ CHECKPOINT: All D1-D6 complete

PHASE 1: Omar Build (30-45 minutes)
├─ Omar: Clone repository
├─ Omar: pnpm install
├─ Omar: pnpm build:deploy
└─ CHECKPOINT: Build artifacts ready

PHASE 2: Omar Deploy (1-2 hours)
├─ Omar: Deploy artifacts to /opt/n8n/
├─ Omar: Create .env file
├─ Omar: Create systemd service
├─ Omar: First startup
└─ CHECKPOINT: Service running, web UI accessible

PHASE 3: Network Integration (William + Frank)
├─ William: Nginx reverse proxy
├─ Frank: SSL certificate deployment
└─ CHECKPOINT: HTTPS access working

PHASE 4: Validation (Julia)
├─ Julia: Functional testing
├─ Julia: Workflow execution test
└─ CHECKPOINT: All acceptance criteria met
```

---

## 6. Task Breakdown

### 6.1 Task Categories

Based on **Single Responsibility Principle**, I've organized tasks into focused categories:

1. **Build Preparation** (5 tasks)
2. **Application Build** (4 tasks)
3. **Deployment** (6 tasks)
4. **Service Configuration** (5 tasks)
5. **First Startup** (4 tasks)
6. **Validation** (3 tasks)

**Total Tasks**: 27

---

### Task Numbering Cross-Reference

**Note**: This planning document uses logical categorization (T1.1, T2.1, T3.1, etc.) while actual task files use sequential numbering (T-027 through T-044). Use this mapping for cross-reference during execution:

| Planning Doc ID | Actual Task File | Category | Task Name |
|-----------------|------------------|----------|-----------|
| T1.1 | T-020 | Build Preparation | Verify build prerequisites |
| T1.2 | T-021 | Build Preparation | Clone n8n repository |
| T1.3 | T-022 | Build Preparation | Prepare build environment |
| T1.4 | T-023 | Build Preparation | Install dependencies |
| T1.5 | T-024 | Build Preparation | Compile TypeScript to JavaScript |
| T2.1 | T-025 | Application Build | Run unit tests |
| T2.2 | T-026 | Application Build | Test build executable |
| T2.3 | *Not created* | Application Build | Package application |
| T2.4 | *Not created* | Application Build | Create distribution archive |
| T3.1 | T-027 | Deployment | Create deployment directory structure |
| T3.2 | T-028 | Deployment | Deploy compiled artifacts |
| T3.3 | T-029 | Deployment | Deploy static assets |
| T3.4 | T-030 | Deployment | Set file ownership and permissions |
| T3.5 | T-031 | Deployment | Verify deployment structure |
| T3.6 | T-032 | Deployment | Create deployment manifest |
| T4.1 | T-033 | Service Configuration | Create environment configuration |
| T4.2 | T-034 | Service Configuration | Create systemd service |
| T4.3 | T-035 | Service Configuration | Create backup script |
| T4.4 | T-036 | Service Configuration | Configure logging |
| T4.5 | T-037 | Service Configuration | Configure monitoring |
| T5.1 | T-038 | First Startup | Start n8n service |
| T5.2 | T-039 | First Startup | Monitor first startup logs |
| T5.3 | *Not created* | First Startup | Verify process health |
| T5.4 | *Not created* | First Startup | Check resource consumption |
| T6.1 | T-041 | Validation | Verify web UI accessible |
| T6.2 | T-042 | Validation | Create first workflow |
| T6.3 | T-043 | Validation | Validate database connection |

**IP Address Consistency Note**: All references to hx-n8n-server use `192.168.10.215` (verified consistent across planning, specification, and task files).

---

### 6.2 Detailed Task List

#### Category 1: Build Preparation

**Owner**: Omar Rodriguez (with William's server ready)

| Task ID | Task Description | Estimated Duration | Dependencies | Deliverable |
|---------|------------------|-------------------|--------------|-------------|
| **T1.1** | Verify server prerequisites (Node.js 22.x, pnpm 10.18.3, build tools) | 15 min | D1-D4 | Verification checklist complete |
| **T1.2** | Clone n8n-master repository to build location (`/opt/n8n/build/`) | 10 min | T1.1 | Repository cloned |
| **T1.3** | Verify disk space (minimum 20 GB free for build) | 5 min | T1.2 | `df -h` output confirms space |
| **T1.4** | Create build log capture mechanism (`tee build.log`) | 5 min | T1.2 | Log file ready |
| **T1.5** | Review `package.json` and `CONTRIBUTING.md` for any special instructions | 10 min | T1.2 | Notes documented |

**Category Total**: 45 minutes

#### Category 2: Application Build

**Owner**: Omar Rodriguez

| Task ID | Task Description | Estimated Duration | Dependencies | Deliverable |
|---------|------------------|-------------------|--------------|-------------|
| **T2.1** | Execute `pnpm install` (downloads 2000+ packages) | 10-15 min | T1.5 | `node_modules/` populated |
| **T2.2** | Execute `pnpm build:deploy` (compiles 30+ packages) | 20-30 min | T2.1 | `packages/*/dist/` created |
| **T2.3** | Verify build output (check for errors, verify executables) | 10 min | T2.2 | Build success confirmed |
| **T2.4** | Test executable locally (`node packages/cli/bin/n8n --version`) | 5 min | T2.3 | Version output displayed |

**Category Total**: 45-60 minutes

**Notes**:
- Build time varies based on server performance
- First build is longest (30-45 min total)
- Monitor CPU and memory usage during build
- **CHECKPOINT**: Build must complete without errors before proceeding

#### Category 3: Deployment

**Owner**: Omar Rodriguez (with William's directory structure)

| Task ID | Task Description | Estimated Duration | Dependencies | Deliverable |
|---------|------------------|-------------------|--------------|-------------|
| **T3.1** | Create deployment directory structure in `/opt/n8n/` | 5 min | T2.4, William's n8n user | Directories created |
| **T3.2** | Copy compiled artifacts to `/opt/n8n/app/` | 10 min | T3.1 | Artifacts deployed |
| **T3.3** | Copy `node_modules/` to `/opt/n8n/app/node_modules/` | 5 min | T3.2 | Dependencies deployed |
| **T3.4** | Set ownership to `n8n:n8n` for all `/opt/n8n/` | 5 min | T3.3 | `chown -R n8n:n8n /opt/n8n` |
| **T3.5** | Set permissions (755 for app/, 700 for .n8n/) | 5 min | T3.4 | Permissions verified |
| **T3.6** | Create symbolic link `/usr/local/bin/n8n` → `/opt/n8n/app/bin/n8n` (optional) | 5 min | T3.5 | Symlink created |

**Category Total**: 35 minutes

#### Category 4: Service Configuration

**Owner**: Omar Rodriguez

| Task ID | Task Description | Estimated Duration | Dependencies | Deliverable |
|---------|------------------|-------------------|--------------|-------------|
| **T4.1** | Create comprehensive `.env` file (100+ variables) | 30 min | T3.6, D5 (Quinn's DB credentials) | `/opt/n8n/.env` complete |
| **T4.2** | Create systemd service file `/etc/systemd/system/n8n.service` | 20 min | T4.1 | Service file created |
| **T4.3** | Set `.env` permissions to 600 (secure secrets) | 5 min | T4.1 | `chmod 600 /opt/n8n/.env` |
| **T4.4** | Create log directory `/var/log/n8n/` with correct ownership | 5 min | T4.2 | Log directory ready |
| **T4.5** | Validate systemd service syntax (`systemd-analyze verify n8n.service`) | 5 min | T4.2 | Syntax validation passed |

**Category Total**: 65 minutes

**Critical File**: `.env` Configuration (excerpt):

```bash
# Database (from Quinn)
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=hx-postgres-server.hx.dev.local
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n_poc3
DB_POSTGRESDB_USER=n8n_user
DB_POSTGRESDB_PASSWORD=<FROM_QUINN>

# Network
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://hx-n8n-server.hx.dev.local
N8N_EDITOR_BASE_URL=https://hx-n8n-server.hx.dev.local

# Security
N8N_SECURE_COOKIE=true
N8N_SAMESITE_COOKIE=strict

# Logging
N8N_LOG_LEVEL=info
N8N_LOG_OUTPUT=file,console
N8N_LOG_FILE_LOCATION=/var/log/n8n/n8n.log

# Timezone
GENERIC_TIMEZONE=America/Chicago
TZ=America/Chicago
```

**Critical File**: Systemd Service (excerpt):

```ini
[Unit]
Description=n8n Workflow Automation Platform
After=network.target postgresql.service

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n
EnvironmentFile=/opt/n8n/.env
ExecStart=/usr/bin/node /opt/n8n/app/bin/n8n start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### Category 5: First Startup

**Owner**: Omar Rodriguez

| Task ID | Task Description | Estimated Duration | Dependencies | Deliverable |
|---------|------------------|-------------------|--------------|-------------|
| **T5.1** | Execute `systemctl daemon-reload` | 1 min | T4.5 | Systemd reloaded |
| **T5.2** | Execute `systemctl enable n8n` | 1 min | T5.1 | Service enabled on boot |
| **T5.3** | Execute `systemctl start n8n` and monitor startup logs | 5-10 min | T5.2, D5 (database ready) | Service started |
| **T5.4** | Verify TypeORM migrations execute successfully | 5 min | T5.3 | Database schema created |

**Category Total**: 12-17 minutes

**Startup Monitoring**:

```bash
# Terminal 1: Start service
sudo systemctl start n8n

# Terminal 2: Monitor logs in real-time
sudo journalctl -u n8n -f

# Expected output:
# Nov 07 10:00:00 n8n[12345]: n8n ready on port 5678
# Nov 07 10:00:01 n8n[12345]: Version: 1.117.0
# Nov 07 10:00:02 n8n[12345]: Editor UI: https://hx-n8n-server.hx.dev.local:5678
```

#### Category 6: Validation

**Owner**: Omar Rodriguez (sign-off) + Julia Santos (testing)

| Task ID | Task Description | Estimated Duration | Dependencies | Deliverable |
|---------|------------------|-------------------|--------------|-------------|
| **T6.1** | Verify web UI accessible at `http://hx-n8n-server:5678` | 5 min | T5.4 | Browser loads editor |
| **T6.2** | Create first admin user account via UI | 10 min | T6.1 | User created, login successful |
| **T6.3** | Verify database connection (check PostgreSQL logs for n8n connections) | 5 min | T6.2 | Connection verified |

**Category Total**: 20 minutes

**CHECKPOINT**: All validation tasks complete → **SIGN-OFF READY**

---

### 6.3 Parallel Execution Opportunities

Based on **Dependency Inversion Principle** (depend on abstractions, not timing):

#### Parallel Track 1: While Omar Builds (Can happen simultaneously)
- **William**: Nginx reverse proxy configuration
- **Frank**: SSL certificate generation and staging
- **Samuel**: Redis instance setup (if needed)
- **Julia**: Test plan preparation

#### Parallel Track 2: Post-Deployment
- **Omar**: Creates admin user + validates web UI
- **Julia**: Prepares workflow test cases
- **William**: Finalizes Nginx deployment (waiting for Omar's service to be running)

**Time Savings**: ~30-45 minutes by parallelizing network configuration with build process

---

## 7. Timeline and Estimates

### 7.1 Build Phase Timeline

| Phase | Tasks | Estimated Duration | Cumulative Time |
|-------|-------|-------------------|-----------------|
| **Build Preparation** | T1.1 - T1.5 | 45 min | 0:45 |
| **Application Build** | T2.1 - T2.4 | 45-60 min | 1:30 - 1:45 |
| **CHECKPOINT** | Verify build success | - | - |

**Build Phase Total**: **1 hour 30 minutes - 1 hour 45 minutes**

### 7.2 Deployment Phase Timeline

| Phase | Tasks | Estimated Duration | Cumulative Time |
|-------|-------|-------------------|-----------------|
| **Deployment** | T3.1 - T3.6 | 35 min | 0:35 |
| **Service Configuration** | T4.1 - T4.5 | 65 min | 1:40 |
| **First Startup** | T5.1 - T5.4 | 12-17 min | 1:52 - 1:57 |
| **Validation** | T6.1 - T6.3 | 20 min | 2:12 - 2:17 |

**Deployment Phase Total**: **2 hours 12 minutes - 2 hours 17 minutes**

### 7.3 Total Project Timeline

```
PRE-WORK (Blocking Dependencies): Variable (William + Frank + Quinn)
├─ Server provisioned: 2-4 hours
├─ Node.js + pnpm: 30 min
├─ Database setup: 1 hour
└─ DNS record: 15 min
TOTAL PRE-WORK: ~4-6 hours (not my responsibility)

OMAR'S WORK:
├─ Build Phase: 1.5 - 1.75 hours
├─ Deployment Phase: 2.2 - 2.3 hours
└─ TOTAL OMAR: ~3.7 - 4.0 hours

NETWORK INTEGRATION (William + Frank): 1-2 hours (parallel)

TOTAL PROJECT: ~8-12 hours (with parallelization ~6-8 hours)
```

### 7.4 When Can I Start?

**Ready to Start When**:
- ✅ D1: Server provisioned and accessible (William)
- ✅ D2: Node.js 22.x installed (William)
- ✅ D3: pnpm 10.18.3 installed (William)
- ✅ D4: Build tools installed (William)
- ✅ D5: Database `n8n_poc3` ready (Quinn)

**Estimated Start Date**: TBD (pending William's server provisioning completion)

**Estimated Completion Date**: Same day as start + 4 hours of focused work

---

## 8. Validation Criteria

### 8.1 Build Validation

**Checklist**:
- [ ] `pnpm install` completes without errors
- [ ] `pnpm build:deploy` completes without errors
- [ ] All 30+ packages have `dist/` directories
- [ ] `packages/cli/bin/n8n` file exists and is executable
- [ ] `node packages/cli/bin/n8n --version` returns version 1.117.0
- [ ] Build log shows no critical warnings
- [ ] Disk space sufficient after build (< 80% used)

**Sign-off**: Omar Rodriguez - Build Phase Complete

### 8.2 Deployment Validation

**Checklist**:
- [ ] All files present in `/opt/n8n/app/`
- [ ] Ownership is `n8n:n8n` for all files
- [ ] Permissions correct (755 for app/, 700 for .n8n/)
- [ ] `.env` file contains all required variables
- [ ] `.env` file permissions are 600
- [ ] Systemd service file syntax valid
- [ ] Log directory `/var/log/n8n/` exists and writable

**Sign-off**: Omar Rodriguez - Deployment Phase Complete

### 8.3 Service Startup Validation

**Checklist**:
- [ ] `systemctl status n8n` shows "active (running)"
- [ ] No errors in `journalctl -u n8n`
- [ ] TypeORM migrations executed successfully
- [ ] Encryption key generated at `/opt/n8n/.n8n/.encryption-key`
- [ ] Instance ID generated at `/opt/n8n/.n8n/.instance-id`
- [ ] Process listening on port 5678 (`netstat -tulpn | grep 5678`)
- [ ] PostgreSQL connection established (check PG logs)

**Sign-off**: Omar Rodriguez - Service Running

### 8.4 Functional Validation

**Checklist**:
- [ ] Web UI accessible at `http://hx-n8n-server.hx.dev.local:5678`
- [ ] UI loads without JavaScript errors
- [ ] First user account creation successful
- [ ] Login with created credentials successful
- [ ] Dashboard displays correctly
- [ ] Database tables populated (User, Settings tables exist)
- [ ] Webhook endpoint responding (`/webhook-test`)

**Sign-off**: Omar Rodriguez (functional) + Julia Santos (acceptance testing)

### 8.5 Integration Validation

**Checklist**:
- [ ] PostgreSQL connection verified (query executes)
- [ ] Redis connection working (if configured)
- [ ] HTTPS access via Nginx working (if configured)
- [ ] DNS resolution correct
- [ ] Logs being written to `/var/log/n8n/n8n.log`
- [ ] Service survives reboot (`systemctl reboot` test)

**Sign-off**: Omar Rodriguez + William Taylor (Nginx) + Quinn Davis (Database)

---

## 9. SOLID Principles Application

Based on `/srv/cc/Governance/0.0-governance/0.0.3-Development/development-and-coding-standards.md`:

### 9.1 Single Responsibility Principle (SRP)

**Application**:
- ✅ Each task has **one clear purpose** (build, deploy, configure, validate)
- ✅ No mixing of concerns (build ≠ deployment ≠ configuration)
- ✅ Separate validation from execution
- ✅ Distinct ownership: Omar (app), William (OS), Quinn (DB), Frank (DNS/SSL)

**Example**:
```
Task T4.1: Create .env file (ONLY configuration)
Task T5.3: Start service (ONLY startup)
Task T6.1: Validate UI (ONLY testing)
```

Each task serves ONE responsibility.

### 9.2 Open-Closed Principle (OCP)

**Application**:
- ✅ Deployment process **open for extension** (future: add Redis, add LDAP)
- ✅ Core build process **closed for modification** (follows n8n standard)
- ✅ Configuration via `.env` allows extension without changing systemd service

**Example**:
```bash
# Adding Redis (extension, no modification):
# 1. Add to .env:
QUEUE_BULL_REDIS_HOST=hx-redis-server
# 2. No changes to systemd service
# 3. No changes to build process
```

### 9.3 Liskov Substitution Principle (LSP)

**Application**:
- ✅ Any agent following Agent Constitution can execute my tasks (substitutability)
- ✅ Database backend substitutable (PostgreSQL ↔ MySQL via config change)
- ✅ Systemd service file follows standard format (any systemd can run it)

**Example**:
```ini
# This systemd service works on ANY systemd-based Linux
# No special dependencies, standard contract
[Service]
Type=simple
ExecStart=/usr/bin/node /opt/n8n/app/bin/n8n start
```

### 9.4 Interface Segregation Principle (ISP)

**Application**:
- ✅ Dependencies are **specific interfaces**, not monolithic
  - William provides: Server, Node.js, pnpm (not "everything")
  - Quinn provides: Database only (not full DB management)
  - Frank provides: DNS + SSL only (not infrastructure)
- ✅ Validation criteria **segregated by domain** (build, deploy, service, functional)

**Example**:
```
William's Interface:
- provideServer()
- installNodeJS()
- installPnpm()

NOT a monolithic "provideInfrastructure()" method
```

### 9.5 Dependency Inversion Principle (DIP)

**Application**:
- ✅ I depend on **abstractions** (database credentials, DNS records), not concretions (specific IP addresses)
- ✅ Configuration via `.env` (abstraction) vs. hardcoded values
- ✅ Service depends on **systemd interface**, not specific Ubuntu version

**Example**:
```bash
# ✅ Good: Depend on abstraction (hostname)
DB_POSTGRESDB_HOST=hx-postgres-server.hx.dev.local

# ❌ Bad: Depend on concrete (IP address)
DB_POSTGRESDB_HOST=192.168.10.209
```

**Result**: Database can move IPs, and my configuration still works (DNS abstraction).

---

## 10. Risks and Mitigations

### 10.1 Build Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Build timeout/failure** | Medium | High | Allocate 60+ min for build, monitor logs, retry with `--force` flag if needed |
| **Out of memory during build** | Low | High | Verify 4+ GB RAM available, close unnecessary processes before build |
| **Disk space exhaustion** | Low | High | Verify 20+ GB free before build, monitor with `df -h` during build |
| **Node.js version mismatch** | Medium | Critical | Use exact version check script before starting |
| **pnpm not via corepack** | Medium | High | Document corepack installation in prerequisites |

### 10.2 Deployment Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Incorrect file permissions** | Medium | Medium | Use scripted permission setting, verify with `ls -la` |
| **Missing environment variables** | Low | High | Use template, validate against checklist |
| **Database credentials wrong** | Low | Critical | Test database connection **before** first startup |
| **Systemd service syntax error** | Low | Medium | Use `systemd-analyze verify` before enabling |

### 10.3 Startup Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **TypeORM migration failure** | Medium | Critical | Test database connectivity first, have rollback SQL ready |
| **Port 5678 already in use** | Low | High | Check with `netstat -tulpn | grep 5678` before starting |
| **Encryption key not generated** | Low | Critical | Verify `.encryption-key` created on first start, backup immediately |
| **Database connection pool exhaustion** | Low | Medium | Start with conservative pool size (5), monitor connections |

### 10.4 Integration Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Nginx reverse proxy misconfigured** | Medium | Medium | Coordinate with William, test direct access first (:5678) |
| **SSL certificate issues** | Medium | Low | HTTPS optional for POC3, HTTP access sufficient for initial validation |
| **LDAP integration fails** | High | Low | **Not using LDAP for POC3** (Enterprise Edition only), use email/password auth |
| **Redis unavailable** | Low | Low | Redis optional, use `EXECUTIONS_MODE=regular` instead of `queue` |

### 10.5 Mitigation Strategy Summary

**Two-Attempt Rule** (from Constitution):
- If build fails: Review logs, fix issue, retry ONCE
- If second attempt fails: **ESCALATE to Agent Zero** with complete logs and context

**Rollback Plan**:
1. Stop service: `systemctl stop n8n`
2. Remove deployment: `rm -rf /opt/n8n/app/`
3. Document failure reason
4. Coordinate with team for issue resolution
5. Re-attempt after fixes

---

## 11. Sign-off Criteria

### 11.1 Omar's Sign-off (PRIMARY)

**I will sign off when ALL of the following are TRUE**:

#### Build Artifacts ✅
- [ ] Build completed without errors
- [ ] All 30+ packages compiled to `dist/`
- [ ] `n8n --version` returns 1.117.0
- [ ] Build log reviewed, no critical warnings

#### Deployment ✅
- [ ] All files deployed to `/opt/n8n/app/`
- [ ] Ownership and permissions correct
- [ ] `.env` file contains 100+ configured variables
- [ ] Systemd service file created and validated

#### Service Running ✅
- [ ] `systemctl status n8n` shows "active (running)"
- [ ] No errors in journalctl logs
- [ ] TypeORM migrations completed successfully
- [ ] Encryption key backed up

#### Functional ✅
- [ ] Web UI accessible (HTTP or HTTPS)
- [ ] First admin user created successfully
- [ ] Login successful
- [ ] Dashboard loads without errors

#### Documentation ✅
- [ ] Deployment log complete with timestamps
- [ ] Environment variables documented
- [ ] Known issues documented (if any)
- [ ] Handoff notes prepared for operations

**Sign-off Statement**:
> "I, Omar Rodriguez (N8N Workflow Worker Specialist), confirm that the n8n application has been successfully built, deployed, configured, and started on hx-n8n-server.hx.dev.local (192.168.10.215). The service is operational, the web UI is accessible, and an admin user account has been created. All build artifacts, configuration files, and startup logs have been documented. The application is ready for integration testing by Julia Santos and network configuration by William Taylor."

**Signature**: _________________
**Date**: _________________

### 11.2 Coordination Sign-offs (SUPPORTING)

#### William Taylor (Ubuntu Server) ✅
- [ ] Server infrastructure ready (Node.js, pnpm, build tools)
- [ ] User accounts and directories created
- [ ] Nginx reverse proxy configured and tested
- [ ] Firewall rules applied
- [ ] Service survives reboot

#### Quinn Davis (PostgreSQL) ✅
- [ ] Database `n8n_poc3` created
- [ ] User `n8n_user` configured with privileges
- [ ] Connection pooling configured
- [ ] Database connection verified from n8n
- [ ] Migrations applied successfully

#### Frank Lucas (Identity & Trust) ✅
- [ ] DNS record `hx-n8n-server.hx.dev.local` → 192.168.10.215
- [ ] SSL certificate generated (if using HTTPS)
- [ ] Certificate deployed to Nginx (coordinate with William)
- [ ] LDAP service account created (if using Enterprise Edition)

#### Julia Santos (Testing & QA) ✅
- [ ] Functional tests passed
- [ ] Workflow creation and execution successful
- [ ] Integration with PostgreSQL validated
- [ ] Performance baseline established
- [ ] Acceptance criteria met

### 11.3 Final Sign-off (Agent Zero)

**Agent Zero validates**:
- [ ] All PRIMARY and SUPPORTING sign-offs complete
- [ ] Work Plan acceptance criteria met
- [ ] Documentation artifacts updated
- [ ] No outstanding blockers
- [ ] Ready for production handoff

---

## Appendices

### Appendix A: Environment Variable Template

**File**: `/opt/n8n/.env.template`

```bash
# ============================================================================
# n8n POC3 Configuration Template
# Server: hx-n8n-server.hx.dev.local (192.168.10.215)
# Environment: Development/Testing
# Created: 2025-11-07 by Omar Rodriguez
# ============================================================================

# ----------------------------------------------------------------------------
# Database Configuration (from Quinn Davis @agent-quinn)
# ----------------------------------------------------------------------------
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=hx-postgres-server.hx.dev.local
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n_poc3
DB_POSTGRESDB_USER=n8n_user
DB_POSTGRESDB_PASSWORD=<CREDENTIAL_FROM_QUINN>
DB_POSTGRESDB_SCHEMA=public
DB_POSTGRESDB_POOL_SIZE=5
DB_POSTGRESDB_CONNECTION_TIMEOUT=20000
DB_POSTGRESDB_IDLE_CONNECTION_TIMEOUT=30000

# Optional: PostgreSQL SSL (if using encrypted connection)
# DB_POSTGRESDB_SSL_ENABLED=true
# DB_POSTGRESDB_SSL_CA=/etc/ssl/certs/ca.crt
# DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED=true

# ----------------------------------------------------------------------------
# Network & Server Configuration
# ----------------------------------------------------------------------------
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://hx-n8n-server.hx.dev.local
N8N_EDITOR_BASE_URL=https://hx-n8n-server.hx.dev.local

# ----------------------------------------------------------------------------
# Security Configuration
# ----------------------------------------------------------------------------
N8N_SECURE_COOKIE=true
N8N_SAMESITE_COOKIE=strict
N8N_RESTRICT_FILE_ACCESS_TO=/opt/n8n/.n8n
N8N_BLOCK_FILE_ACCESS_TO_N8N_FILES=true

# ----------------------------------------------------------------------------
# Authentication (Email/Password - Free Tier)
# NOTE: LDAP requires Enterprise Edition license
# ----------------------------------------------------------------------------
N8N_BASIC_AUTH_ACTIVE=false
N8N_USER_MANAGEMENT_DISABLED=false

# ----------------------------------------------------------------------------
# LDAP Configuration (Enterprise Edition Only - NOT USING FOR POC3)
# ----------------------------------------------------------------------------
# N8N_LICENSE_KEY=<your-license-key>
# LDAP_LOGIN_ENABLED=true
# LDAP_SERVER_URL=ldaps://hx-freeipa-server.hx.dev.local:636
# LDAP_BIND_DN=uid=n8n-service,cn=users,cn=accounts,dc=hx,dc=dev,dc=local
# LDAP_BIND_PASSWORD=<FROM_FRANK>
# LDAP_BASE_DN=cn=users,cn=accounts,dc=hx,dc=dev,dc=local
# LDAP_USER_FILTER=(uid={username})

# ----------------------------------------------------------------------------
# Performance & Execution
# ----------------------------------------------------------------------------
EXECUTIONS_MODE=regular
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_ON_SUCCESS=all
EXECUTIONS_DATA_MAX_AGE=168
EXECUTIONS_DATA_PRUNE=true

# ----------------------------------------------------------------------------
# Timezone & Localization
# ----------------------------------------------------------------------------
GENERIC_TIMEZONE=America/Chicago
TZ=America/Chicago

# ----------------------------------------------------------------------------
# Logging Configuration
# ----------------------------------------------------------------------------
N8N_LOG_LEVEL=info
N8N_LOG_OUTPUT=file,console
N8N_LOG_FILE_LOCATION=/var/log/n8n/n8n.log
DB_LOGGING_ENABLED=false

# ----------------------------------------------------------------------------
# Monitoring & Metrics (Optional)
# ----------------------------------------------------------------------------
N8N_METRICS=false

# ----------------------------------------------------------------------------
# Endpoints Configuration
# ----------------------------------------------------------------------------
N8N_ENDPOINT_REST=rest
N8N_ENDPOINT_WEBHOOK=webhook
N8N_ENDPOINT_WEBHOOK_TEST=webhook-test
N8N_DISABLE_UI=false

# ----------------------------------------------------------------------------
# Advanced Settings
# ----------------------------------------------------------------------------
N8N_GRACEFUL_SHUTDOWN_TIMEOUT=30
NODE_ENV=production
NODE_FUNCTION_ALLOW_BUILTIN=*
NODE_FUNCTION_ALLOW_EXTERNAL=*
```

### Appendix B: Systemd Service File

**File**: `/etc/systemd/system/n8n.service`

```ini
[Unit]
Description=n8n Workflow Automation Platform
Documentation=https://docs.n8n.io
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n
EnvironmentFile=/opt/n8n/.env
ExecStart=/usr/bin/node /opt/n8n/app/bin/n8n start
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=n8n

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/n8n/.n8n /var/log/n8n

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
```

### Appendix C: Deployment Checklist

**Pre-Deployment Verification**:
- [ ] Server hx-n8n-server accessible via SSH
- [ ] `node --version` returns ≥22.16.0
- [ ] `pnpm --version` returns 10.18.3
- [ ] `gcc --version` succeeds (build tools installed)
- [ ] Database credentials received from Quinn
- [ ] DNS record confirmed by Frank
- [ ] Disk space > 20 GB free

**Build Phase**:
- [ ] Repository cloned to `/opt/n8n/build/`
- [ ] `pnpm install` completed successfully
- [ ] `pnpm build:deploy` completed successfully
- [ ] Build log saved to `/opt/n8n/build.log`
- [ ] Version check: `node packages/cli/bin/n8n --version` = 1.117.0

**Deployment Phase**:
- [ ] Artifacts copied to `/opt/n8n/app/`
- [ ] Ownership set: `chown -R n8n:n8n /opt/n8n`
- [ ] Permissions: 755 for app/, 700 for .n8n/
- [ ] `.env` file created with 100+ variables
- [ ] `.env` permissions: 600
- [ ] Systemd service file created
- [ ] Log directory created: `/var/log/n8n/`

**Startup Phase**:
- [ ] `systemctl daemon-reload` executed
- [ ] `systemctl enable n8n` executed
- [ ] `systemctl start n8n` executed
- [ ] Service status: "active (running)"
- [ ] No errors in `journalctl -u n8n`
- [ ] TypeORM migrations completed
- [ ] Encryption key generated and backed up

**Validation Phase**:
- [ ] Web UI accessible at http://hx-n8n-server:5678
- [ ] First user account created
- [ ] Login successful
- [ ] Dashboard loads correctly
- [ ] PostgreSQL connection verified
- [ ] Service survives reboot test

### Appendix D: Troubleshooting Guide

**Issue**: Build fails with "Node.js version not supported"
**Solution**:
```bash
node --version  # Must be >=22.16.0 and <=24.x
# If wrong version, coordinate with William to install correct version
```

**Issue**: Build fails with "pnpm: command not found"
**Solution**:
```bash
# Install via corepack (coordinate with William)
corepack enable
corepack prepare pnpm@10.18.3 --activate
pnpm --version  # Should return 10.18.3
```

**Issue**: Service fails to start with "ECONNREFUSED" database error
**Solution**:
```bash
# Test database connectivity
PGPASSWORD=<password> psql -h hx-postgres-server -U n8n_user -d n8n_poc3 -c "SELECT 1"
# If fails, coordinate with Quinn to verify database is ready
```

**Issue**: Port 5678 already in use
**Solution**:
```bash
# Check what's using port 5678
sudo netstat -tulpn | grep 5678
sudo lsof -i :5678
# Kill conflicting process or change N8N_PORT in .env
```

**Issue**: Encryption key missing after startup
**Solution**:
```bash
# Check if key was generated
ls -la /opt/n8n/.n8n/.encryption-key
# If missing, check permissions and startup logs
# Service must have write access to /opt/n8n/.n8n/
```

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-07 | Omar Rodriguez (@agent-omar) | Initial planning analysis - comprehensive deployment plan |
| 1.1 | 2025-11-07 | Claude Code | **CodeRabbit Remediation**: Added Task Numbering Cross-Reference section (lines 454-488) mapping logical task IDs (T1.1, T2.1, etc.) to actual sequential task files (T-020 through T-044). Includes 27-task mapping table with categories and task names. Added IP address consistency verification note confirming all hx-n8n-server references use 192.168.10.215. Eliminates confusion during execution by providing clear cross-reference between planning document and actual task files. |

---

**Questions or Coordination Needed?**
Contact: Omar Rodriguez (@agent-omar) - N8N Workflow Worker Specialist
Orchestrating Agent: Agent Zero (@agent-zero)
Last Updated: 2025-11-07

---

**END OF DOCUMENT**
