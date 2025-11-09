# Phase 4: Execution Plan - N8N Server Deployment (POC3)

**Document Type**: Execution Plan
**Created**: 2025-11-07
**Project**: POC3 N8N Workflow Automation Platform Deployment
**Purpose**: Define step-by-step execution sequence, checkpoints, and validation procedures
**Classification**: Internal - Project Planning

---

## Table of Contents

1. [Overview](#overview)
2. [Pre-Flight Checklist](#pre-flight-checklist)
3. [Execution Timeline](#execution-timeline)
4. [Execution Sequence](#execution-sequence)
5. [Rollback Plan](#rollback-plan)
6. [Progress Tracking](#progress-tracking)

---

## Overview

This execution plan defines the step-by-step sequence for deploying n8n workflow automation platform. It incorporates lessons from Phase 2 Collaborative Planning and optimizes for parallel execution where possible.

**Execution Strategy**: **Standard Track (No MCP)** - 1.5-2 days for core n8n functionality

**Input Documents**:
- [Phase 0: Discovery](./phase0-discovery.md) - Scope, agents, technical findings
- [Phase 1: Specification](./phase1-specification.md) - Requirements, acceptance criteria
- [Phase 2: Collaborative Planning](./phase2-collaborative-planning.md) - Task breakdown, dependencies
- [Phase 3: Alignment Checkpoint](./work-plan.md#phase-3-alignment-checkpoint) - Readiness confirmation

**Critical Path Duration**: 9-10 hours (optimized with parallelization)

**Quality Gate**: Constitution Check MUST pass before execution begins.

---

## Pre-Flight Checklist

### Constitution Check (GATE - Must Pass Before Execution)

**Quality Over Speed** (PASS = All 3 criteria met):
- [ ] **Timeline Adequacy**: Estimated duration (13.5 hours over 1.5 days) ≤ Available time (no hard deadline forcing shortcuts)
  - **Objective Criteria**: If project must complete in <1 day, FAIL (insufficient time). If ≥1.5 days available, PASS.
- [ ] **Full Build Process**: Using `pnpm build:deploy` (30-45 min compilation), not npm shortcuts or pre-built binaries
  - **Objective Criteria**: Task 3.3 uses `pnpm build:deploy` command = PASS. Any alternative build method = FAIL.
- [ ] **Validation Coverage**: All 10 acceptance criteria (AC-001 through AC-010) have test procedures defined
  - **Objective Criteria**: Count acceptance criteria with test procedures in Phase 1 Specification. 10/10 = PASS. <10 = FAIL.

**Multi-Agent Coordination** (PASS = All 3 criteria met):
- [ ] **Agent Identification Complete**: All 7 agents (Frank, William, Quinn, Samuel, Omar, Julia, Zero) confirmed ready in Phase 3 Alignment Checkpoint
  - **Objective Criteria**: All agents signed Phase 3 Alignment Checkpoint = PASS. Any missing signature = FAIL.
- [ ] **Dependency Mapping**: All task dependencies documented in Phase 2 Collaborative Planning (43 tasks with blocking relationships identified)
  - **Objective Criteria**: Phase 2 document contains dependency graph or blocking task list = PASS. No dependency mapping = FAIL.
- [ ] **Communication Protocols**: Agent call format (`@agent-name`) and validation handoff procedures documented
  - **Objective Criteria**: Phase 2 or Agent Constitution contains agent communication standards = PASS. No documented protocol = FAIL.

**Documentation** (PASS = Both criteria met):
- [ ] **Documentation Plan Exists**: Phase 5 tasks (5.1-5.3) specify 6+ documentation deliverables (Platform Nodes, Network Topology, Credentials, Service Ops, Integration Matrix, Runbooks)
  - **Objective Criteria**: Count Phase 5 Task 5.1 documentation items. ≥6 items = PASS. <6 items = FAIL.
- [ ] **Update Scope Defined**: Specific governance documents to update identified (lines 931-936)
  - **Objective Criteria**: Phase 5 Task 5.1 lists specific files/sections to update = PASS. Generic "update docs" = FAIL.

**Validation** (PASS = All 3 criteria met):
- [ ] **Test Plan Exists**: Phase 4 contains Julia validation procedures (AC-001 through AC-010)
  - **Objective Criteria**: Phase 4 section (lines 895-916) lists all 10 acceptance criteria = PASS. <10 criteria = FAIL.
- [ ] **Acceptance Criteria Defined**: Phase 1 Specification contains measurable acceptance criteria
  - **Objective Criteria**: Phase 1 Specification file exists with "Acceptance Criteria" section containing ≥10 items = PASS.
- [ ] **Rollback Plan Exists**: Rollback procedures documented with step-by-step commands (lines 958-1014)
  - **Objective Criteria**: Rollback Plan section contains ≥5 rollback steps with validation checklist = PASS. <5 steps = FAIL.

**Escalation Awareness** (PASS = Both criteria met):
- [ ] **Escalation Rules Known**: 2-attempt rule from Agent Constitution (try twice, then escalate)
  - **Objective Criteria**: Team acknowledges 2-attempt rule = PASS. No awareness of escalation threshold = FAIL.
- [ ] **Escalation Paths Defined**: Agent-specific escalation → @agent-zero (Universal PM)
  - **Objective Criteria**: Escalation hierarchy documented (individual agent → @agent-zero) = PASS. Undefined hierarchy = FAIL.

**Constitution Check Status**: ⏳ **PENDING** - Must be completed before Phase 4 execution begins

**GATE DECISION CRITERIA**:
- **PASS**: All 5 sections (Quality, Coordination, Documentation, Validation, Escalation) meet objective criteria
- **FAIL**: Any section fails objective criteria → DO NOT PROCEED, remediate failing items first
- **Sign-Off Required**: @agent-zero must explicitly approve "Constitution Check PASS" before Phase 1 execution begins

---

### Resource Verification

**Infrastructure**:
- [ ] hx-n8n-server (192.168.10.215) accessible via SSH
- [ ] hx-postgres-server (192.168.10.209) operational
- [ ] hx-freeipa-server (192.168.10.200) Samba AD DC running
- [ ] hx-redis-server (192.168.10.210) accessible (optional)
- [ ] Network connectivity verified (192.168.10.0/24)

**Disk Space**:
- [ ] hx-n8n-server: ≥20GB free space (for build artifacts)
- [ ] hx-postgres-server: ≥5GB free space (for database)

**Access Credentials**:
- [ ] SSH access to hx-n8n-server (administrator@192.168.10.215)
- [ ] PostgreSQL admin credentials available
- [ ] Samba AD DC admin credentials available (set SAMBA_ADMIN_PASSWORD environment variable)

**Knowledge Sources**:
- [ ] `/srv/knowledge/vault/n8n-master/` accessible (n8n repository)
- [ ] All agent planning analyses reviewed
- [ ] Deep dive analysis available

**Pre-Flight Status**: ⏳ **PENDING** - Verify all items before proceeding

---

## Execution Timeline

| Phase | Tasks | Start | End | Duration | Checkpoint |
|-------|-------|-------|-----|----------|------------|
| **PRE-FLIGHT** | Constitution check, resource verification | Day 1, 08:00 | Day 1, 08:30 | 30 min | All resources ready? |
| **PHASE 1** | Infrastructure setup (Frank, William, Quinn parallel) | Day 1, 08:30 | Day 1, 11:30 | 3 hours | Phase 1 complete? |
| **PHASE 2** | Infrastructure validation (Quinn, Samuel, Frank parallel) | Day 1, 11:30 | Day 1, 13:30 | 2 hours | Phase 2 complete? |
| **CHECKPOINT** | Lunch break, status review | Day 1, 13:30 | Day 1, 14:00 | 30 min | Ready for build? |
| **PHASE 3** | Application build & deploy (Omar, William partial parallel) | Day 1, 14:00 | Day 1, 18:00 | 4 hours | Application running? |
| **PHASE 4** | Final validation (Julia) | Day 2, 09:00 | Day 2, 12:00 | 3 hours | All tests pass? |
| **PHASE 5** | Documentation & sign-off | Day 2, 12:00 | Day 2, 13:00 | 1 hour | All agents signed off? |

**Total Duration**: 13.5 hours over 1.5 days (includes checkpoints and buffer)

---

## Execution Sequence

### PRE-FLIGHT: Constitution & Resource Verification (Sequential)

**Duration**: 30 minutes
**Owner**: @agent-zero

```
□ Task 0.1: @agent-zero - Execute Constitution Check
  Expected outcome: All constitutional compliance items checked ✅
  Validation: Review checklist above, confirm all items PASS

□ Task 0.2: @agent-zero - Verify infrastructure resources
  Expected outcome: All servers accessible, disk space sufficient
  Validation: SSH to all servers, check disk space with `df -h`

□ Task 0.3: @agent-zero - Confirm agent readiness
  Expected outcome: All 7 agents ready to proceed
  Validation: Review Phase 3 Alignment Checkpoint sign-offs
```

**CHECKPOINT**: Pre-Flight Complete?
- [ ] Constitution check PASS
- [ ] All resources verified
- [ ] All agents ready

**Decision**: GO / NO-GO for Phase 1

---

### PHASE 1: Infrastructure Setup (Parallel Execution Available)

**Duration**: 3 hours (parallel execution)
**Start**: Day 1, 08:30 | **End**: Day 1, 11:30

#### Task 1.1 (Parallel): @agent-frank - DNS Record Creation

```
[P] Task 1.1: @agent-frank - Create DNS record for n8n.hx.dev.local

Command sequence:
# Connect to hx-freeipa-server
ssh administrator@192.168.10.200

# Set Samba admin password (REQUIRED: Set this environment variable before proceeding)
# Example: export SAMBA_ADMIN_PASSWORD='your_password_here'
if [ -z "$SAMBA_ADMIN_PASSWORD" ]; then
  echo "❌ ERROR: SAMBA_ADMIN_PASSWORD environment variable not set"
  echo "Set it with: export SAMBA_ADMIN_PASSWORD='your_password'"
  exit 1
fi

# Create DNS A record
samba-tool dns add 192.168.10.200 hx.dev.local n8n A 192.168.10.215 \
  -U administrator --password="$SAMBA_ADMIN_PASSWORD"

# Verify DNS record
samba-tool dns query 192.168.10.200 hx.dev.local n8n A \
  -U administrator --password="$SAMBA_ADMIN_PASSWORD"

# Test resolution
nslookup n8n.hx.dev.local 192.168.10.200

Expected outcome:
- DNS query returns 192.168.10.215
- Resolution time < 100ms
- No NXDOMAIN errors

Validation:
nslookup n8n.hx.dev.local
dig @192.168.10.200 n8n.hx.dev.local

Duration: 15 minutes
```

#### Task 1.2 (Parallel): @agent-frank - SSL Certificate Generation

```
[P] Task 1.2: @agent-frank - Generate SSL certificate from Samba CA

Command sequence:
# Generate private key
openssl genrsa -out /etc/ssl/private/n8n.hx.dev.local.key 2048
chmod 600 /etc/ssl/private/n8n.hx.dev.local.key

# Create SAN configuration
cat > /tmp/n8n-san.cnf << 'EOF'
[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
req_extensions = v3_req

[ req_distinguished_name ]
CN = n8n.hx.dev.local

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = n8n.hx.dev.local
DNS.2 = hx-n8n-server.hx.dev.local
EOF

# Generate CSR
openssl req -new -key /etc/ssl/private/n8n.hx.dev.local.key \
  -out /tmp/n8n.hx.dev.local.csr \
  -subj "/CN=n8n.hx.dev.local/O=Hana-X/OU=AI Ecosystem" \
  -config /tmp/n8n-san.cnf

# Sign with Samba CA (adapt based on CA setup)
# [CA signing procedure - coordinate with Samba CA process]

# Verify certificate
openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -text -noout

Expected outcome:
- Private key generated (0600 permissions)
- SSL certificate signed by Samba CA
- SAN includes n8n.hx.dev.local
- Certificate valid for 365 days

Validation:
openssl verify -CAfile /etc/ssl/certs/hx-dev-ca.crt /etc/ssl/certs/n8n.hx.dev.local.crt

Duration: 30 minutes
```

#### Task 1.3 (Parallel): @agent-william - Server Provisioning & Node.js Installation

```
[P] Task 1.3: @agent-william - Provision server and install Node.js 22.x LTS

Command sequence:
# Connect to hx-n8n-server
ssh administrator@192.168.10.215

# System updates
sudo apt update && sudo apt upgrade -y

# Install Node.js 22.x LTS via NodeSource
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Verify Node.js version
node --version  # Should be ≥22.16.0

# Enable corepack and install pnpm
sudo corepack enable
corepack prepare pnpm@10.18.3 --activate

# Verify pnpm version
pnpm --version  # Should be 10.18.3

# Install system dependencies
sudo apt install -y build-essential python3 python3-pip \
  libcairo2-dev libpango1.0-dev libjpeg-dev libgif-dev \
  librsvg2-dev libpq-dev

Expected outcome:
- Node.js 22.x installed (≥22.16.0)
- pnpm 10.18.3 installed via corepack
- All system dependencies installed
- Build tools verified

Validation:
node --version
pnpm --version
gcc --version
python3 --version

Duration: 2-3 hours (includes download time)
```

#### Task 1.4 (Parallel): @agent-william - Service User & Directory Structure

```
[P] Task 1.4: @agent-william - Create service user and directory structure

Command sequence:
# Create n8n service user
sudo useradd -r -s /bin/false n8n

# Create directory structure
sudo mkdir -p /opt/n8n/app
sudo mkdir -p /var/log/n8n
sudo mkdir -p /srv/n8n

# Set ownership
sudo chown -R n8n:n8n /opt/n8n
sudo chown -R n8n:n8n /var/log/n8n
sudo chown -R n8n:n8n /srv/n8n

# Set permissions
sudo chmod 750 /opt/n8n
sudo chmod 755 /var/log/n8n

Expected outcome:
- User `n8n` created (system user, no shell)
- Directory structure created
- Correct ownership and permissions

Validation:
id n8n
ls -la /opt/
ls -la /var/log/

Duration: 10 minutes
```

#### Task 1.5 (Parallel): @agent-quinn - PostgreSQL Database Creation

```
[P] Task 1.5: @agent-quinn - Create PostgreSQL database and user

Command sequence:
# Connect to hx-postgres-server
ssh administrator@192.168.10.209

# Switch to postgres user
sudo -u postgres psql

# Create database
CREATE DATABASE n8n_poc3
  WITH ENCODING='UTF8'
  LC_COLLATE='en_US.UTF-8'
  LC_CTYPE='en_US.UTF-8'
  TEMPLATE=template0;

# Create user (REQUIRED: Replace ${N8N_DB_PASSWORD} with generated secure password)
CREATE USER n8n_user WITH ENCRYPTED PASSWORD '${N8N_DB_PASSWORD}';

# Grant privileges
GRANT CREATE, CONNECT ON DATABASE n8n_poc3 TO n8n_user;
\c n8n_poc3
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO n8n_user;
GRANT USAGE, CREATE ON SCHEMA public TO n8n_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO n8n_user;

# Verify
\l n8n_poc3
\du n8n_user

Expected outcome:
- Database `n8n_poc3` created
- User `n8n_user` created with secure password
- Privileges granted (CREATE, SELECT, INSERT, UPDATE, DELETE)

Validation:
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3 -c "\dt"

Duration: 30 minutes
```

**CHECKPOINT**: Phase 1 Complete?
- [ ] DNS record created and verified
- [ ] SSL certificate generated
- [ ] Node.js 22.x + pnpm 10.18.3 installed
- [ ] Service user and directories created
- [ ] PostgreSQL database created

**Status**: ⏳ PENDING EXECUTION

---

### PHASE 2: Infrastructure Validation (Parallel Execution Available)

**Duration**: 2 hours (parallel execution)
**Start**: Day 1, 11:30 | **End**: Day 1, 13:30

#### Task 2.1 (Parallel): @agent-quinn - Database Connection Validation

```
[P] Task 2.1: @agent-quinn - Validate database connectivity from hx-n8n-server

Command sequence:
# From hx-n8n-server
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3

# Test query
SELECT version();

# Test CREATE privilege
CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(100));
INSERT INTO test_table (name) VALUES ('test');
SELECT * FROM test_table;
DROP TABLE test_table;

Expected outcome:
- Connection successful
- All privileges verified (CREATE, SELECT, INSERT, DELETE)

Validation:
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3 -c "SELECT 1"

Duration: 30 minutes
```

#### Task 2.2 (Parallel): @agent-samuel - Redis Configuration (OPTIONAL)

```
[P] Task 2.2: @agent-samuel - Configure Redis for n8n (if queue mode selected)

Command sequence:
# Connect to hx-redis-server
ssh administrator@192.168.10.210

# Edit Redis configuration
sudo vi /etc/redis/redis.conf

# Add n8n-specific configuration
# (DB 1: queue, DB 2: session, DB 3: cache)
maxmemory 2gb
maxmemory-policy allkeys-lru

# Restart Redis
sudo systemctl restart redis-server

# Test connectivity from hx-n8n-server
redis-cli -h 192.168.10.210 PING

Expected outcome:
- Redis configured with memory limits
- Connectivity verified from n8n server

Validation:
redis-cli -h 192.168.10.210 INFO memory

Duration: 1-2 hours

NOTE: OPTIONAL - Defer if using regular execution mode
```

#### Task 2.3 (Parallel): @agent-frank - SSL Certificate Transfer

```
[P] Task 2.3: @agent-frank - Transfer SSL certificate to hx-n8n-server

Command sequence:
# From hx-freeipa-server
scp /etc/ssl/private/n8n.hx.dev.local.key administrator@192.168.10.215:/tmp/
scp /etc/ssl/certs/n8n.hx.dev.local.crt administrator@192.168.10.215:/tmp/
scp /etc/ssl/certs/hx-dev-ca.crt administrator@192.168.10.215:/tmp/

# On hx-n8n-server (coordination with @agent-william)
sudo mv /tmp/n8n.hx.dev.local.key /etc/ssl/private/
sudo mv /tmp/n8n.hx.dev.local.crt /etc/ssl/certs/
sudo mv /tmp/hx-dev-ca.crt /etc/ssl/certs/

sudo chown root:root /etc/ssl/private/n8n.hx.dev.local.key
sudo chmod 600 /etc/ssl/private/n8n.hx.dev.local.key

sudo chown root:root /etc/ssl/certs/n8n.hx.dev.local.crt
sudo chmod 644 /etc/ssl/certs/n8n.hx.dev.local.crt

Expected outcome:
- SSL certificate files transferred securely
- Correct ownership and permissions
- Certificate files in final locations

Validation:
ls -la /etc/ssl/private/n8n.hx.dev.local.key
ls -la /etc/ssl/certs/n8n.hx.dev.local.crt

Duration: 30 minutes
```

#### Task 2.4 (Parallel): @agent-william - Nginx Installation & Configuration

```
[P] Task 2.4: @agent-william - Install and configure Nginx reverse proxy

Command sequence:
# Install Nginx
sudo apt install -y nginx

# Create Nginx configuration
sudo tee /etc/nginx/sites-available/n8n.conf << 'EOF'
server {
    listen 80;
    server_name n8n.hx.dev.local;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name n8n.hx.dev.local;

    ssl_certificate /etc/ssl/certs/n8n.hx.dev.local.crt;
    ssl_certificate_key /etc/ssl/private/n8n.hx.dev.local.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/n8n.conf /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Don't start yet (n8n service not running)

Expected outcome:
- Nginx installed and configured
- SSL/TLS termination configured
- WebSocket upgrade headers configured
- Configuration syntax valid

Validation:
sudo nginx -t

Duration: 30 minutes
```

**CHECKPOINT**: Phase 2 Complete?
- [ ] Database connection validated from n8n server
- [ ] Redis configured (if applicable)
- [ ] SSL certificate transferred and installed
- [ ] Nginx configured (syntax valid)
- [ ] Ready for application build

**Status**: ⏳ PENDING EXECUTION

---

### CHECKPOINT: Mid-Day Status Review

**Time**: Day 1, 13:30 - 14:00 (30 minutes)
**Owner**: @agent-zero

**Review Items**:
- [ ] Phase 1 and Phase 2 completed successfully
- [ ] All infrastructure prerequisites in place
- [ ] No blocking issues identified
- [ ] Team ready to proceed with build phase

**Decision**: GO / NO-GO for Phase 3 (Application Build)

---

### PHASE 3: Application Build & Deploy (Sequential - CRITICAL PATH)

**Duration**: 4 hours (sequential execution)
**Start**: Day 1, 14:00 | **End**: Day 1, 18:00
**Owner**: @agent-omar (primary), @agent-william (Nginx startup)

#### Task 3.1 (Sequential): @agent-omar - Repository Clone & Build Preparation

```
[S] Task 3.1: @agent-omar - Clone n8n repository and prepare build environment

Command sequence:
# Connect to hx-n8n-server as administrator
ssh administrator@192.168.10.215

# Navigate to build directory
cd /srv/n8n

# Clone n8n repository
git clone https://github.com/n8n-io/n8n.git
cd n8n

# Verify Node.js and pnpm versions
node --version  # Should be ≥22.16.0
pnpm --version  # Should be 10.18.3

# Check disk space
df -h .  # Should have ≥20GB free

Expected outcome:
- Repository cloned successfully
- Version requirements validated
- Sufficient disk space confirmed

Validation:
ls -la /srv/n8n/n8n/
cat /srv/n8n/n8n/package.json | grep version

Duration: 15 minutes
```

#### Task 3.2 (Sequential): @agent-omar - pnpm Install

```
[S] Task 3.2: @agent-omar - Install dependencies with pnpm
[Blocked by: Task 3.1]

Command sequence:
cd /srv/n8n/n8n

# Install all dependencies (2000+ packages)
pnpm install

# Monitor progress
# Expected: 5-10 minutes download time, 10-15 minutes install time

Expected outcome:
- All dependencies installed successfully
- No ERESOLVE errors
- node_modules/ populated

Validation:
ls -la node_modules/
pnpm list --depth=0

Duration: 15-30 minutes (network-dependent)
```

#### Task 3.3 (Sequential): @agent-omar - Build Application

```
[S] Task 3.3: @agent-omar - Build n8n application with pnpm build:deploy
[Blocked by: Task 3.2]

Command sequence:
cd /srv/n8n/n8n

# Run build (30-45 minutes, CPU-intensive)
pnpm build:deploy

# Monitor build logs for errors
# Expected: Turbo orchestration of 30+ package builds

Expected outcome:
- All 30+ packages compiled successfully
- Compiled artifacts in packages/cli/dist/
- No TypeScript compilation errors

Validation:
ls -la packages/cli/dist/
ls -la packages/cli/bin/n8n

Duration: 30-45 minutes (CPU-intensive)
```

#### Task 3.4 (Sequential): @agent-omar - Deploy Artifacts

```
[S] Task 3.4: @agent-omar - Deploy compiled artifacts to /opt/n8n/
[Blocked by: Task 3.3]

Command sequence:
# Copy entire n8n directory to /opt/n8n/app/
sudo cp -r /srv/n8n/n8n /opt/n8n/app/

# Set ownership
sudo chown -R n8n:n8n /opt/n8n/app/

# Set permissions
sudo chmod -R 750 /opt/n8n/app/

Expected outcome:
- All files copied to /opt/n8n/app/
- Correct ownership (n8n:n8n)
- Correct permissions (750)

Validation:
ls -la /opt/n8n/app/
ls -la /opt/n8n/app/packages/cli/bin/n8n

Duration: 10-15 minutes
```

#### Task 3.5 (Sequential): @agent-omar - Environment Configuration

```
[S] Task 3.5: @agent-omar - Create .env file with 100+ configuration variables
[Blocked by: Task 3.4]

Command sequence:
# REQUIRED: Set database password environment variable before proceeding
# This should match the password used in Task 1.5 (PostgreSQL database creation)
# Example: export N8N_DB_PASSWORD='your_secure_password_here'
if [ -z "$N8N_DB_PASSWORD" ]; then
  echo "❌ ERROR: N8N_DB_PASSWORD environment variable not set"
  echo "Set it with: export N8N_DB_PASSWORD='your_secure_password'"
  exit 1
fi

sudo tee /opt/n8n/.env << EOF
# Database Configuration
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=192.168.10.209
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n_poc3
DB_POSTGRESDB_USER=n8n_user
DB_POSTGRESDB_PASSWORD=${N8N_DB_PASSWORD}

# Network Configuration
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.hx.dev.local/
N8N_EDITOR_BASE_URL=https://n8n.hx.dev.local/

# Security Configuration
N8N_ENCRYPTION_KEY=$(openssl rand -hex 32)

# Execution Configuration
EXECUTIONS_MODE=regular

# Optional: Redis configuration (if queue mode)
# QUEUE_BULL_REDIS_HOST=192.168.10.210
# QUEUE_BULL_REDIS_PORT=6379
# QUEUE_BULL_REDIS_DB=1

# Logging
N8N_LOG_LEVEL=info
N8N_LOG_OUTPUT=console,file
N8N_LOG_FILE_LOCATION=/var/log/n8n/n8n.log
EOF

# Set permissions
sudo chown n8n:n8n /opt/n8n/.env
sudo chmod 600 /opt/n8n/.env

# CRITICAL: Backup encryption key (AUTOMATED with verification)
ENCRYPTION_KEY=$(sudo grep N8N_ENCRYPTION_KEY /opt/n8n/.env | cut -d'=' -f2)
echo "Encryption Key: $ENCRYPTION_KEY"

# Create secure backup directory (readable only by root)
sudo mkdir -p /root/n8n-backups
sudo chmod 700 /root/n8n-backups

# Save encryption key to backup file with timestamp
BACKUP_FILE="/root/n8n-backups/n8n-encryption-key-$(date +%Y%m%d-%H%M%S).txt"
echo "N8N_ENCRYPTION_KEY=$ENCRYPTION_KEY" | sudo tee "$BACKUP_FILE" > /dev/null
sudo chmod 600 "$BACKUP_FILE"

# VERIFICATION REQUIRED: Confirm backup was created successfully
if [ -f "$BACKUP_FILE" ]; then
  echo "✅ Encryption key backed up to: $BACKUP_FILE"
  echo "Verification: Backup file size = $(wc -c < "$BACKUP_FILE") bytes"

  # Verify backup contains the key
  if sudo grep -q "N8N_ENCRYPTION_KEY=" "$BACKUP_FILE"; then
    echo "✅ VERIFICATION PASSED: Backup file contains encryption key"
  else
    echo "❌ VERIFICATION FAILED: Backup file does not contain encryption key"
    echo "⚠️  DO NOT PROCEED - Manual intervention required"
    exit 1
  fi
else
  echo "❌ BACKUP FAILED: Encryption key backup file not created"
  echo "⚠️  DO NOT PROCEED - Manual intervention required"
  exit 1
fi

# Display backup location for operator record
echo ""
echo "================================================"
echo "⚠️  CRITICAL: RECORD THIS BACKUP LOCATION"
echo "================================================"
echo "Encryption Key Backup: $BACKUP_FILE"
echo "This key is required for data recovery!"
echo "================================================"

Expected outcome:
- .env file created with all required variables
- Encryption key generated and BACKED UP
- Correct ownership and permissions

Validation:
sudo -u n8n cat /opt/n8n/.env | head -20
ls -la /opt/n8n/.env

Duration: 15-20 minutes
```

#### Task 3.6 (Sequential): @agent-omar - Systemd Service Configuration

```
[S] Task 3.6: @agent-omar - Create and configure systemd service
[Blocked by: Task 3.5]

Command sequence:
sudo tee /etc/systemd/system/n8n.service << 'EOF'
[Unit]
Description=n8n Workflow Automation
After=network.target postgresql.service

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n/app
EnvironmentFile=/opt/n8n/.env
ExecStart=/usr/bin/node /opt/n8n/app/packages/cli/bin/n8n start
Restart=on-failure
RestartSec=5s
StandardOutput=journal
StandardError=journal

# Resource limits
LimitNOFILE=65536
MemoryMax=4G

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd
sudo systemctl daemon-reload

# Enable service (auto-start on boot)
sudo systemctl enable n8n.service

Expected outcome:
- Systemd service file created
- Service enabled for auto-start
- Service ready to start

Validation:
sudo systemctl status n8n.service
systemctl is-enabled n8n.service

Duration: 10 minutes
```

#### Task 3.7 (Sequential): @agent-omar - First Service Startup

```
[S] Task 3.7: @agent-omar - Start n8n service and validate TypeORM migrations
[Blocked by: Task 3.6]

Command sequence:
# Start service
sudo systemctl start n8n.service

# Monitor logs for TypeORM migrations
sudo journalctl -u n8n.service -f

# Wait for startup message (12-17 minutes)
# Look for: "Editor is now accessible via: https://n8n.hx.dev.local"

# Verify service running
sudo systemctl status n8n.service

Expected outcome:
- Service starts successfully
- TypeORM migrations execute successfully
- Web UI listening on port 5678
- No errors in logs

Validation:
sudo systemctl status n8n.service
curl http://localhost:5678/healthz

Duration: 12-17 minutes
```

#### Task 3.8 (Parallel): @agent-william - Nginx Service Startup

```
[P] Task 3.8: @agent-william - Start Nginx reverse proxy
[Can run during Task 3.7]

Command sequence:
# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Verify configuration loaded
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx

Expected outcome:
- Nginx started successfully
- Reverse proxy active
- SSL/TLS termination functional

Validation:
sudo systemctl status nginx
curl -I https://n8n.hx.dev.local

Duration: 5 minutes
```

#### Task 3.9 (Sequential): @agent-omar - Web UI Validation & Admin User Creation

```
[S] Task 3.9: @agent-omar - Validate web UI access and create first admin user
[Blocked by: Task 3.7, Task 3.8]

Command sequence:
# Test HTTPS access
curl -I https://n8n.hx.dev.local

# Create first admin user (via web UI or API)
# Manual step: Navigate to https://n8n.hx.dev.local in browser
# Follow setup wizard to create admin account

Expected outcome:
- Web UI accessible via HTTPS
- SSL certificate valid
- Admin user created successfully
- Can login to n8n

Validation:
# Manual browser test
# Expected: n8n login page loads, admin can login

Duration: 10-15 minutes
```

**CHECKPOINT**: Phase 3 Complete?
- [ ] n8n application built successfully
- [ ] Artifacts deployed to /opt/n8n/
- [ ] Environment variables configured
- [ ] Systemd service running
- [ ] Nginx reverse proxy active
- [ ] Web UI accessible via HTTPS
- [ ] Admin user created
- [ ] Encryption key backed up (CRITICAL)

**Status**: ⏳ PENDING EXECUTION

---

### PHASE 4: Final Validation (Sequential)

**Duration**: 3 hours
**Start**: Day 2, 09:00 | **End**: Day 2, 12:00
**Owner**: @agent-julia

Validation procedures documented in [Phase 1 Specification - Acceptance Criteria](./phase1-specification.md#acceptance-criteria).

#### Task 4.1: Execute All Acceptance Criteria Tests

```
□ AC-001: Web UI Accessibility (SSL validation)
□ AC-002: Workflow Execution (create & execute simple workflow)
□ AC-003: Database Persistence (verify data in PostgreSQL)
□ AC-004: Session Management (if Redis configured)
□ AC-005: Service Auto-Start (reboot test)
□ AC-006: WebSocket Support (real-time updates)
□ AC-007: Agent Sign-Off (collect from all agents)
□ AC-008: Backup & Recovery (encryption key backup verified)
□ AC-009: Health Checks (monitoring configured)
□ AC-010: Runbook Documentation (operational procedures complete)
```

**Duration**: 2-3 hours

---

### PHASE 5: Documentation & Sign-Off

**Duration**: 1 hour
**Start**: Day 2, 12:00 | **End**: Day 2, 13:00
**Owner**: @agent-zero

#### Task 5.1: Update Documentation

```
□ Platform Nodes document (add n8n server entry)
□ Network Topology (add n8n in application layer)
□ Credentials file (document n8n admin credentials)
□ Service operations guide (n8n start/stop/restart procedures)
□ Integration matrix (n8n → PostgreSQL, Nginx, DNS)
□ Runbooks (troubleshooting guide for n8n)
```

#### Task 5.2: Collect Agent Sign-Offs

```
□ @agent-frank: DNS + SSL validated
□ @agent-william: Server + Nginx validated
□ @agent-quinn: Database validated
□ @agent-samuel: Redis validated (if configured)
□ @agent-omar: Application validated
□ @agent-julia: All tests PASS
```

#### Task 5.3: Lessons Learned

Document what went well, what could be improved, recommendations for next time.

**Duration**: 1 hour

---

## Rollback Plan

### When to Rollback

Rollback if any of the following occur:

- [ ] Tests fail (acceptance criteria not met)
- [ ] Service won't start after multiple attempts
- [ ] Critical errors in logs (database connection failure, TypeORM migration errors)
- [ ] Integration breaks (PostgreSQL unreachable, Nginx proxy errors)
- [ ] Performance unacceptable (workflow execution >30 seconds, memory leaks)

### Rollback Procedure

**Step 1: @agent-omar - Stop n8n Service**
```bash
sudo systemctl stop n8n.service
sudo systemctl disable n8n.service
```

**Step 2: @agent-william - Stop Nginx**
```bash
sudo systemctl stop nginx
```

**Step 3: @agent-quinn - Drop Database (OPTIONAL - only if requested)**
```sql
DROP DATABASE IF EXISTS n8n_poc3;
DROP USER IF EXISTS n8n_user;
```

**Step 4: @agent-frank - Remove DNS Record (OPTIONAL)**
```bash
# REQUIRED: Set SAMBA_ADMIN_PASSWORD environment variable before proceeding
# Example: export SAMBA_ADMIN_PASSWORD='your_password_here'
samba-tool dns delete 192.168.10.200 hx.dev.local n8n A 192.168.10.215 \
  -U administrator --password="$SAMBA_ADMIN_PASSWORD"
```

**Step 5: @agent-omar - Remove Application Files (OPTIONAL)**
```bash
sudo rm -rf /opt/n8n/app/
sudo rm /opt/n8n/.env
sudo rm /etc/systemd/system/n8n.service
```

### Rollback Validation

- [ ] n8n service stopped
- [ ] Nginx stopped (or reverted to pre-n8n config)
- [ ] No n8n processes running (`ps aux | grep n8n`)
- [ ] Can retry deployment later

### Rollback Notes

**Greenfield Deployment**: This is a new deployment with no existing n8n service. Rollback is low-risk and primarily involves cleanup of created resources.

**Data Preservation**: If rollback due to non-critical issues, consider preserving database for retry (don't DROP database).

---

## Progress Tracking

### Phase Status

- [ ] **PRE-FLIGHT**: Constitution check & resource verification
- [ ] **PHASE 1**: Infrastructure setup (DNS, SSL, Node.js, Database)
- [ ] **PHASE 2**: Infrastructure validation (connectivity tests)
- [ ] **PHASE 3**: Application build & deploy (n8n compilation, service startup)
- [ ] **PHASE 4**: Final validation (acceptance criteria tests)
- [ ] **PHASE 5**: Documentation & sign-off

### Gate Status

- [ ] **Constitution Check**: PASS (Quality Over Speed, Multi-Agent Coordination, Documentation, Validation, Escalation)
- [ ] **All agents identified**: PASS (7 agents ready)
- [ ] **Resources available**: PASS (servers accessible, disk space sufficient)
- [ ] **Acceptance criteria defined**: PASS (10 criteria in Phase 1)
- [ ] **Test plan exists**: PASS (Julia validation procedures)
- [ ] **Rollback plan exists**: PASS (documented above)

### Completion Checklist

- [ ] All tasks executed (PRE-FLIGHT through PHASE 5)
- [ ] All validations passed (10 acceptance criteria)
- [ ] All documentation updated (6 governance documents)
- [ ] All agents notified of completion
- [ ] Lessons learned captured

---

## Next Steps

**Execution Plan Status**: ✅ **COMPLETE** (plan ready for execution)

**Ready to Proceed to**: **Phase 4 Execution** (PENDING APPROVAL)

**Prerequisites**:
- [ ] Constitution Check completed ✅
- [ ] All agents confirmed ready
- [ ] Go decision from Phase 3 Alignment Checkpoint

**Post-Execution**:
- Phase 5: Validation & Documentation (Tasks 5.1-5.3, lines 922-956)
- Lessons learned documentation (template: see Phase 5 Operational Documentation note below)
- MCP integration planning (Phase 2 enhancement if desired)

**Phase 5 Operational Documentation Note**:
To prevent ad-hoc post-deployment documentation, consider creating companion Phase 5 templates BEFORE execution:
- **Documentation Update Checklist Template** (Task 5.1): Structure for Platform Nodes, Network Topology, Credentials, Service Operations Guide, Integration Matrix, Runbooks
- **Agent Sign-Off Template** (Task 5.2): Structured sign-off form with validation criteria for each agent (@agent-frank, @agent-william, @agent-quinn, @agent-samuel, @agent-omar, @agent-julia)
- **Lessons Learned Template** (Task 5.3): Structured format with sections: "What Went Well", "What Could Be Improved", "Recommendations for Next Time", "Metrics" (actual vs. estimated duration, error count, rollback incidents)

Creating these templates now ensures consistent, comprehensive post-execution documentation and reduces cognitive load during the 1-hour Phase 5 window.

---

## Document Metadata

```yaml
document_type: Execution Plan
project: POC3 N8N Server Deployment
phase: Phase 4 - Execution
status: Ready for Execution
created_date: 2025-11-07
orchestrating_agent: @agent-zero
total_phases: 5
critical_path_duration: 9-10 hours
estimated_total_duration: 13.5 hours (over 1.5 days)
execution_strategy: Standard Track (No MCP)
quality_gate: Constitution Check (MUST PASS before execution)
rollback_difficulty: Low (greenfield deployment)
input_documents:
  - phase0-discovery.md
  - phase1-specification.md
  - phase2-collaborative-planning.md
  - work-plan.md (Phase 3 Alignment Checkpoint)
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial Phase 3 execution plan creation | @agent-zero |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Enhanced Post-Execution section (lines 1058-1069) with Phase 5 Operational Documentation Note. Added reference to Phase 5 tasks (lines 922-956) and detailed template recommendations for: (1) Documentation Update Checklist Template (Task 5.1) for Platform Nodes, Network Topology, Credentials, Service Ops Guide, Integration Matrix, Runbooks; (2) Agent Sign-Off Template (Task 5.2) with structured validation criteria for each agent; (3) Lessons Learned Template (Task 5.3) with "What Went Well", "What Could Be Improved", "Recommendations", "Metrics" sections. Creating these templates before execution prevents ad-hoc documentation and reduces cognitive load during 1-hour Phase 5 window. | Claude Code |
| 1.2 | 2025-11-07 | **CodeRabbit Remediation (4 fixes)**: **(1) Encryption Key Backup Automation** (lines 727-766): Replaced manual "MANUALLY COPY..." instruction with automated backup script featuring: secure backup directory creation (/root/n8n-backups/), timestamped backup file, verification checks (file exists, contains key), exit-on-failure safeguards, and operator notification of backup location. **(2) Constitution Check Objective Criteria** (lines 44-85): Transformed aspirational language ("We have time...") into measurable PASS/FAIL criteria with 5 sections (Quality Over Speed, Multi-Agent Coordination, Documentation, Validation, Escalation Awareness), 14 objective criteria (e.g., "Timeline Adequacy: ≥1.5 days = PASS", "Agent Identification: All 7 signed = PASS"), and gate decision process requiring @agent-zero sign-off. **(3) Credential Standardization** (lines 105, 360-361, 723, 716-723): Replaced all hardcoded credential values with environment variable references: SAMBA_ADMIN_PASSWORD for Samba operations (lines 105, 176-182, 1054-1057), N8N_DB_PASSWORD for PostgreSQL (lines 360-361, 716-723). Added environment variable validation checks (exit if not set). **(4) Consistent Placeholder Convention**: Changed PostgreSQL password from "GENERATED_PASSWORD_HERE" literal to ${N8N_DB_PASSWORD} variable reference (line 723), matching pattern used elsewhere. All credentials now use environment variables/placeholders, preventing accidental credential exposure in version control or documentation sharing. | Claude Code |

---

**Version**: 1.2
**Maintained By**: Agent Zero (Universal PM Orchestrator)
**Related Documents**:
- [Phase 0: Discovery](./phase0-discovery.md)
- [Phase 1: Specification](./phase1-specification.md)
- [Phase 2: Collaborative Planning](./phase2-collaborative-planning.md)
- [Agent Planning Analyses](./agent-*-planning-analysis.md)
- [Work Methodology](/srv/cc/Governance/0.0-governance/0.4-hx-work-methodology.md)
**Classification**: Internal - Project Planning
**Status**: Ready for Execution - Pending Approval
