# POC-002 Task List: N8N MCP Native Deployment

**Work ID**: POC-002
**Version**: 1.0
**Date**: 2025-11-06
**Owner**: @agent-olivia (Olivia Chang - N8N MCP Specialist)
**Coordinator**: @agent-zero (Universal PM Orchestrator)

---

## Overview

**Deployment Method**: Native (Node.js 20+ + systemd, NO Docker)
**Scope**: Full 42-tool deployment (25 documentation + 17 management tools)
**Target Server**: hx-n8n-mcp-server (192.168.10.214)
**Reference**: `/srv/cc/Governance/WIP/HTTP_DEPLOYMENT.md` (Option 2: Local HTTP Server)

**Total Estimated Time**: 6-9 hours (depends on N8N instance availability)

---

## Task Status Legend

- ⬜ **Pending**: Not started
- 🔄 **In Progress**: Currently executing
- ✅ **Complete**: Finished and validated
- ⚠️ **Blocked**: Waiting on dependency
- ❌ **Failed**: Encountered error (requires remediation)

---

## Phase 0: Prerequisites & Coordination (2-4 hours)

### **T0.1: Verify N8N Instance Operational** ⚠️ **CRITICAL BLOCKER**

**Owner**: @agent-omar (Omar Rodriguez - N8N Workflows Specialist)
**Priority**: P0 Critical
**Status**: ⬜ Pending

**Description**: Verify hx-n8n-server (192.168.10.215) is operational and N8N service running on port 5678.

**Commands**:
```bash
# Option 1: HTTP health check
curl http://hx-n8n-server.hx.dev.local:5678/healthz

# Option 2: SSH verification
ssh hx-n8n-server "systemctl status n8n"

# Option 3: Port check
ssh hx-n8n-server "ss -tlnp | grep 5678"
```

**Expected Output**:
- Health endpoint returns 200 OK OR
- `systemctl status n8n` shows `active (running)` OR
- Port 5678 listening with n8n process

**Acceptance Criteria**:
- N8N service operational on port 5678
- N8N web UI accessible at http://hx-n8n-server.hx.dev.local:5678
- N8N version documented (for compatibility)

**Dependencies**: None (first task)

**Estimated Time**: 30 minutes

**If NOT Operational**:
- **Option A**: Deploy N8N instance (coordinate separate POC)
- **Option B**: Use test/demo N8N instance temporarily
- **Option C**: Proceed with documentation-only deployment (25 tools, Phase 1A)

**Coordination**: Report status to @agent-zero immediately

---

### **T0.2: Generate N8N API Key** ⚠️ **CRITICAL DEPENDENCY**

**Owner**: @agent-omar (N8N owner) OR @agent-frank (Credentials management)
**Priority**: P0 Critical
**Status**: ⬜ Pending
**Depends On**: T0.1 (N8N instance operational)

**Description**: Generate N8N API key for N8N MCP server integration.

**Procedure**:
1. Login to N8N instance: http://hx-n8n-server.hx.dev.local:5678
2. Navigate to **Settings** → **API**
3. Click **Create API Key**
4. Copy generated key (format: `n8n_api_...`)

**Security Storage** (choose one):
```bash
# Option A: Governance credentials file
echo "N8N_API_KEY=n8n_api_xxx..." >> /srv/cc/Governance/0.2-credentials/hx-credentials.md

# Option B: File-based secret on target server (recommended)
ssh hx-n8n-mcp-server "sudo mkdir -p /etc/n8n-mcp"
echo "n8n_api_xxx..." | ssh hx-n8n-mcp-server "sudo tee /etc/n8n-mcp/n8n_api_key"
ssh hx-n8n-mcp-server "sudo chmod 600 /etc/n8n-mcp/n8n_api_key"
```

**Validation Test**:
```bash
# Test API key with N8N API
curl -H "X-N8N-API-KEY: <generated-key>" \
     http://hx-n8n-server.hx.dev.local:5678/api/v1/workflows
```

**Expected Output**: JSON response with workflows list (may be empty array)

**Acceptance Criteria**:
- API key generated successfully
- API key stored securely (file permissions 600)
- API key validated with N8N API (200 OK response)
- API key documented in POC-002/06-docs/credentials-reference.txt (path only, not value)

**Dependencies**: T0.1 complete

**Estimated Time**: 15 minutes

**Deliverables**:
- N8N API key stored in `/etc/n8n-mcp/n8n_api_key` OR governance credentials
- Validation test results logged

---

### **T0.3: Install Node.js 20+ on Target Server**

**Owner**: @agent-william (William Taylor - Ubuntu Systems Administrator)
**Priority**: P0 Critical
**Status**: ⬜ Pending

**Description**: Install Node.js 20.x LTS and NPM on hx-n8n-mcp-server (192.168.10.214).

**Commands**:
```bash
# SSH to target server
ssh hx-n8n-mcp-server

# Install Node.js 20.x from NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt update
sudo apt install -y nodejs

# Verify installation
node --version  # Should be >= v20.0.0
npm --version   # Should be >= 9.0.0
```

**Expected Output**:
```
node --version
v20.11.0  # (or higher in 20.x series)

npm --version
10.2.4  # (or higher)
```

**Acceptance Criteria**:
- Node.js version >= 20.0.0
- NPM version >= 9.0.0
- Both commands executable by all users
- No installation errors in apt logs

**Dependencies**: None (can run parallel to T0.1, T0.2)

**Estimated Time**: 15 minutes

**Rollback Plan**:
```bash
# If issues arise
sudo apt remove nodejs npm
sudo apt autoremove
```

**Deliverables**:
- Node.js installed and verified
- Installation output logged in POC-002/06-docs/node-install-output.log

---

### **T0.4: Create N8N MCP Service User**

**Owner**: @agent-william
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T0.3 (Node.js installed)

**Description**: Create dedicated system user for N8N MCP service (security best practice).

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Create system user (no login shell)
sudo useradd -r -s /bin/false -d /opt/n8n-mcp -m n8n-mcp

# Create required directories
sudo mkdir -p /opt/n8n-mcp /etc/n8n-mcp
sudo chown n8n-mcp:n8n-mcp /opt/n8n-mcp
sudo chown n8n-mcp:n8n-mcp /etc/n8n-mcp

# Verify user creation
id n8n-mcp
```

**Expected Output**:
```
uid=999(n8n-mcp) gid=999(n8n-mcp) groups=999(n8n-mcp)
```

**Acceptance Criteria**:
- User `n8n-mcp` exists
- Home directory `/opt/n8n-mcp` created and owned by n8n-mcp
- Config directory `/etc/n8n-mcp` created and owned by n8n-mcp
- User has no login shell (security)

**Dependencies**: T0.3 complete

**Estimated Time**: 10 minutes

**Security Note**: System user (`-r` flag) with no login shell prevents unauthorized access.

---

### **T0.5: Generate AUTH_TOKEN for MCP Authentication**

**Owner**: @agent-olivia OR @agent-william
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T0.4 (service user created)

**Description**: Generate secure authentication token for N8N MCP HTTP server.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Generate 32-character random token
sudo sh -c 'openssl rand -base64 32 > /etc/n8n-mcp/auth_token'

# Set secure permissions
sudo chmod 600 /etc/n8n-mcp/auth_token
sudo chown n8n-mcp:n8n-mcp /etc/n8n-mcp/auth_token

# Display token for client configuration (SAVE THIS!)
sudo cat /etc/n8n-mcp/auth_token
```

**Expected Output**: Base64 string (e.g., `Xy7+9kLm3nQ...` - 44 characters)

**Acceptance Criteria**:
- Token file `/etc/n8n-mcp/auth_token` created
- File permissions 600 (readable only by owner)
- File owned by n8n-mcp:n8n-mcp
- Token value documented in POC-002/06-docs/auth-token-reference.txt

**Dependencies**: T0.4 complete

**Estimated Time**: 10 minutes

**IMPORTANT**: Copy token value to POC-002 documentation for client configuration (Phase 5).

**Security**: Token must remain secret. Never commit to version control.

---

### **T0.6: Verify Network Connectivity (N8N MCP ↔ N8N Instance)**

**Owner**: @agent-olivia
**Priority**: Medium
**Status**: ⬜ Pending
**Depends On**: T0.1 (N8N operational)

**Description**: Verify network connectivity from hx-n8n-mcp-server to hx-n8n-server on port 5678.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Test connectivity
curl -I http://hx-n8n-server.hx.dev.local:5678

# Test DNS resolution
nslookup hx-n8n-server.hx.dev.local

# Test port reachability
nc -zv hx-n8n-server.hx.dev.local 5678
```

**Expected Output**:
- `curl -I` returns HTTP 200 or 301 (redirect)
- DNS resolves to 192.168.10.215
- `nc` reports "Connection to hx-n8n-server.hx.dev.local 5678 port [tcp/*] succeeded!"

**Acceptance Criteria**:
- DNS resolves correctly
- Port 5678 reachable from hx-n8n-mcp-server
- No firewall blocks between .214 and .215

**Dependencies**: T0.1 complete

**Estimated Time**: 10 minutes

**If Blocked**: Coordinate with @agent-frank (firewall rules) or @agent-william (network config)

---

## Phase 1: N8N MCP Installation (1-2 hours)

### **T1.1: Clone N8N MCP Repository**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T0.3 (Node.js installed), T0.4 (service user created)

**Description**: Clone N8N MCP repository to /opt/n8n-mcp and checkout stable version.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Clone repository as n8n-mcp user
sudo -u n8n-mcp git clone https://github.com/czlonkowski/n8n-mcp.git /opt/n8n-mcp

# Enter directory
cd /opt/n8n-mcp

# Checkout stable version (pinned)
sudo -u n8n-mcp git checkout tags/v2.21.1

# Verify version
git describe --tags
```

**Expected Output**:
```
Cloning into '/opt/n8n-mcp'...
remote: Enumerating objects: ...
...
v2.21.1
```

**Acceptance Criteria**:
- Repository cloned to /opt/n8n-mcp
- Owned by n8n-mcp user
- Version v2.21.1 checked out
- `.git` directory present

**Dependencies**: T0.3, T0.4 complete

**Estimated Time**: 5-10 minutes (depends on network)

**Validation**:
```bash
ls -la /opt/n8n-mcp/
# Should show: package.json, src/, README.md, etc.
```

---

### **T1.2: Install NPM Dependencies**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T1.1 (repository cloned)

**Description**: Install Node.js dependencies from package.json (production dependencies only).

**Commands**:
```bash
ssh hx-n8n-mcp-server
cd /opt/n8n-mcp

# Install production dependencies
sudo -u n8n-mcp npm install --production --no-audit

# Verify node_modules created
ls -la node_modules/ | head -20
```

**Expected Output**:
```
added 150 packages, and audited 151 packages in 45s
...
found 0 vulnerabilities
```

**Acceptance Criteria**:
- `node_modules/` directory created
- All dependencies installed (no errors)
- No critical vulnerabilities reported
- Directory owned by n8n-mcp user

**Dependencies**: T1.1 complete

**Estimated Time**: 3-5 minutes (depends on network)

**Troubleshooting**:
- If permission errors: Verify n8n-mcp user owns /opt/n8n-mcp
- If network errors: Check proxy settings or retry

**Log Output**: Save npm install output to POC-002/06-docs/npm-install-output.log

---

### **T1.3: Build TypeScript to JavaScript**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T1.2 (dependencies installed)

**Description**: Compile TypeScript source code to JavaScript (dist/ directory).

**Commands**:
```bash
ssh hx-n8n-mcp-server
cd /opt/n8n-mcp

# Build TypeScript
sudo -u n8n-mcp npm run build

# Verify dist directory created
ls -la dist/
ls -la dist/mcp/index.js
```

**Expected Output**:
```
> n8n-mcp@2.21.1 build
> tsc -p tsconfig.build.json

# No errors
```

**Acceptance Criteria**:
- `dist/` directory created
- `dist/mcp/index.js` exists (main entry point)
- Build completes with 0 errors
- All TypeScript compiled successfully

**Dependencies**: T1.2 complete

**Estimated Time**: 2-3 minutes

**Validation**:
```bash
# Check main entry point exists
test -f /opt/n8n-mcp/dist/mcp/index.js && echo "Build successful"
```

**Log Output**: Save build output to POC-002/06-docs/npm-build-output.log

---

### **T1.4: Initialize Node Documentation Database**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T1.3 (build complete)

**Description**: Run rebuild script to create/update n8n node documentation database (SQLite).

**Commands**:
```bash
ssh hx-n8n-mcp-server
cd /opt/n8n-mcp

# Rebuild database
sudo -u n8n-mcp npm run rebuild

# Verify database created
ls -lh data/nodes.db
sqlite3 data/nodes.db "SELECT COUNT(*) FROM nodes;"
```

**Expected Output**:
```
> n8n-mcp@2.21.1 rebuild
> node dist/scripts/rebuild.js

[INFO] Rebuilding n8n node database...
[INFO] Extracted 536 nodes
[INFO] Database saved to data/nodes.db
```

**Acceptance Criteria**:
- `data/nodes.db` file created (~15MB)
- Database contains 536 nodes (or close to this)
- No errors during rebuild process
- File owned by n8n-mcp user

**Dependencies**: T1.3 complete

**Estimated Time**: 2-3 minutes

**Validation**:
```bash
# Verify node count
sqlite3 /opt/n8n-mcp/data/nodes.db "SELECT COUNT(*) FROM nodes;"
# Expected: 536 (or similar)
```

**Log Output**: Save rebuild output to POC-002/06-docs/database-rebuild-output.log

---

## Phase 2: N8N API Configuration (30 minutes)

### **T2.1: Create Environment Configuration File**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T0.2 (N8N API key generated), T0.5 (AUTH_TOKEN generated)

**Description**: Create environment configuration file for N8N MCP service (systemd EnvironmentFile).

**File**: `/etc/n8n-mcp/config.env`

**Content**:
```bash
# ============================================
# N8N MCP HTTP Server Configuration
# ============================================
# Reference: /srv/cc/Governance/WIP/HTTP_DEPLOYMENT.md
# Version: 1.0
# Date: 2025-11-06

# ===== Core HTTP Mode Settings =====
MCP_MODE=http
USE_FIXED_HTTP=true
NODE_ENV=production
PORT=3000
HOST=0.0.0.0
LOG_LEVEL=info

# ===== Authentication =====
# Uses file-based secret for security
AUTH_TOKEN_FILE=/etc/n8n-mcp/auth_token

# ===== N8N API Integration (ENABLES ALL 42 TOOLS) =====
# Without these, only 25 documentation tools available
N8N_API_URL=http://hx-n8n-server.hx.dev.local:5678
N8N_API_KEY_FILE=/etc/n8n-mcp/n8n_api_key
N8N_API_TIMEOUT=30000
N8N_API_MAX_RETRIES=3

# ===== Security Settings (v2.16.3+) =====
# SSRF Protection - Use 'moderate' for internal n8n on localhost
WEBHOOK_SECURITY_MODE=moderate

# Rate Limiting - Prevent brute force attacks
AUTH_RATE_LIMIT_WINDOW=900000  # 15 minutes in milliseconds
AUTH_RATE_LIMIT_MAX=20          # Max 20 failed auth attempts per IP

# ===== Network Settings =====
# Trust proxy headers (if behind nginx reverse proxy)
TRUST_PROXY=0  # Set to 1 if using reverse proxy

# ===== Optional: Telemetry =====
# Disable anonymous usage statistics (opt-out)
# N8N_MCP_TELEMETRY_DISABLED=true
```

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Create config file
sudo tee /etc/n8n-mcp/config.env > /dev/null << 'EOF'
[paste content above]
EOF

# Set secure permissions
sudo chmod 600 /etc/n8n-mcp/config.env
sudo chown n8n-mcp:n8n-mcp /etc/n8n-mcp/config.env

# Verify content
sudo cat /etc/n8n-mcp/config.env
```

**Acceptance Criteria**:
- File `/etc/n8n-mcp/config.env` created
- File permissions 600 (readable only by owner)
- File owned by n8n-mcp:n8n-mcp
- All required variables present
- N8N_API_URL points to correct server

**Dependencies**: T0.2, T0.5 complete

**Estimated Time**: 10 minutes

**Security Note**: File contains sensitive configuration but not secrets (those in separate files).

---

### **T2.2: Store N8N API Key Securely**

**Owner**: @agent-olivia OR @agent-frank
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T0.2 (API key generated)

**Description**: Store N8N API key in secure file on target server.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Store API key (replace with actual key from T0.2)
echo "n8n_api_xxx_ACTUAL_KEY_HERE" | sudo tee /etc/n8n-mcp/n8n_api_key > /dev/null

# Set secure permissions (readable only by n8n-mcp user)
sudo chmod 600 /etc/n8n-mcp/n8n_api_key
sudo chown n8n-mcp:n8n-mcp /etc/n8n-mcp/n8n_api_key

# Verify (shows file exists, not content)
ls -la /etc/n8n-mcp/n8n_api_key
```

**Expected Output**:
```
-rw------- 1 n8n-mcp n8n-mcp 45 Nov  6 10:30 /etc/n8n-mcp/n8n_api_key
```

**Acceptance Criteria**:
- File `/etc/n8n-mcp/n8n_api_key` created
- File permissions 600 (owner read/write only)
- File owned by n8n-mcp:n8n-mcp
- API key value correct (from T0.2)

**Dependencies**: T0.2 complete

**Estimated Time**: 5 minutes

**Security**:
- Never log or echo API key value
- Never commit to version control
- File-based secret (not environment variable)

**Validation Test**:
```bash
# Test API key works (run as n8n-mcp user)
sudo -u n8n-mcp curl -H "X-N8N-API-KEY: $(cat /etc/n8n-mcp/n8n_api_key)" \
     http://hx-n8n-server.hx.dev.local:5678/api/v1/workflows
```

**Expected**: JSON response with workflows (200 OK)

---

### **T2.3: Validate Configuration Files**

**Owner**: @agent-olivia
**Priority**: Medium
**Status**: ⬜ Pending
**Depends On**: T2.1, T2.2 complete

**Description**: Validate all configuration files exist with correct permissions before service deployment.

**Validation Checklist**:
```bash
ssh hx-n8n-mcp-server

# Check all required files exist
test -f /etc/n8n-mcp/config.env && echo "✅ config.env exists"
test -f /etc/n8n-mcp/auth_token && echo "✅ auth_token exists"
test -f /etc/n8n-mcp/n8n_api_key && echo "✅ n8n_api_key exists"

# Check permissions (should all be 600)
ls -l /etc/n8n-mcp/

# Check ownership (should all be n8n-mcp:n8n-mcp)
ls -l /etc/n8n-mcp/

# Validate environment file syntax
sudo -u n8n-mcp env $(cat /etc/n8n-mcp/config.env | xargs) printenv | grep -E '(MCP_MODE|N8N_API_URL|PORT)'
```

**Expected Output**:
```
✅ config.env exists
✅ auth_token exists
✅ n8n_api_key exists

-rw------- 1 n8n-mcp n8n-mcp  500 Nov  6 10:25 config.env
-rw------- 1 n8n-mcp n8n-mcp   44 Nov  6 10:20 auth_token
-rw------- 1 n8n-mcp n8n-mcp   45 Nov  6 10:30 n8n_api_key

MCP_MODE=http
N8N_API_URL=http://hx-n8n-server.hx.dev.local:5678
PORT=3000
```

**Acceptance Criteria**:
- All 3 files exist
- All files have 600 permissions
- All files owned by n8n-mcp:n8n-mcp
- Environment variables parse correctly

**Dependencies**: T2.1, T2.2 complete

**Estimated Time**: 10 minutes

**If Validation Fails**: Return to T2.1 or T2.2 to fix issues before proceeding.

---

## Phase 3: Systemd Service Creation (30 minutes)

### **T3.1: Create Systemd Service Unit File**

**Owner**: @agent-olivia OR @agent-william
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T1.4 (build complete), T2.3 (config validated)

**Description**: Create systemd service unit file for N8N MCP HTTP server.

**File**: `/etc/systemd/system/n8n-mcp.service`

**Content** (from HTTP_DEPLOYMENT.md lines 486-537):
```ini
[Unit]
Description=n8n-MCP HTTP Server
Documentation=https://github.com/czlonkowski/n8n-mcp
After=network.target
Requires=network.target

[Service]
Type=simple
User=n8n-mcp
Group=n8n-mcp
WorkingDirectory=/opt/n8n-mcp

# Load environment from file
EnvironmentFile=/etc/n8n-mcp/config.env

# Pre-start validation
ExecStartPre=/usr/bin/test -f /etc/n8n-mcp/auth_token
ExecStartPre=/usr/bin/test -f /etc/n8n-mcp/n8n_api_key
ExecStartPre=/usr/bin/test -f /opt/n8n-mcp/dist/mcp/index.js

# Start N8N MCP HTTP server
ExecStart=/usr/bin/node dist/mcp/index.js

# Restart configuration
Restart=always
RestartSec=10
StartLimitBurst=5
StartLimitInterval=60s

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/n8n-mcp/data
ProtectKernelTunables=true
ProtectControlGroups=true
RestrictSUIDSGID=true
LockPersonality=true

# Resource limits
LimitNOFILE=65536
MemoryLimit=512M
CPUQuota=50%

[Install]
WantedBy=multi-user.target
```

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Create service file
sudo tee /etc/systemd/system/n8n-mcp.service > /dev/null << 'EOF'
[paste content above]
EOF

# Set permissions
sudo chmod 644 /etc/systemd/system/n8n-mcp.service

# Reload systemd daemon
sudo systemctl daemon-reload

# Verify service file loaded
systemctl status n8n-mcp
```

**Expected Output**:
```
● n8n-mcp.service - n8n-MCP HTTP Server
     Loaded: loaded (/etc/systemd/system/n8n-mcp.service; disabled; vendor preset: enabled)
     Active: inactive (dead)
```

**Acceptance Criteria**:
- Service file created at `/etc/systemd/system/n8n-mcp.service`
- Service file permissions 644 (readable by all, writable by root)
- Systemd recognizes service (shows "Loaded: loaded")
- No syntax errors in service file

**Dependencies**: T1.4, T2.3 complete

**Estimated Time**: 15 minutes

**Validation**:
```bash
# Check for syntax errors
sudo systemd-analyze verify /etc/systemd/system/n8n-mcp.service
```

**Expected**: No output (silence = success)

---

### **T3.2: Enable Systemd Service**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T3.1 (service file created)

**Description**: Enable N8N MCP service to start automatically on boot.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Enable service (creates symlink)
sudo systemctl enable n8n-mcp

# Verify enabled
systemctl is-enabled n8n-mcp
```

**Expected Output**:
```
Created symlink /etc/systemd/system/multi-user.target.wants/n8n-mcp.service → /etc/systemd/system/n8n-mcp.service.

enabled
```

**Acceptance Criteria**:
- Service enabled (`systemctl is-enabled n8n-mcp` = "enabled")
- Symlink created in `/etc/systemd/system/multi-user.target.wants/`
- Service will start automatically on reboot

**Dependencies**: T3.1 complete

**Estimated Time**: 5 minutes

**Purpose**: Ensures service survives server reboots (high availability).

---

### **T3.3: Start N8N MCP Service**

**Owner**: @agent-olivia
**Priority**: P0 Critical
**Status**: ⬜ Pending
**Depends On**: T3.2 (service enabled)

**Description**: Start N8N MCP HTTP server service for the first time.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Start service
sudo systemctl start n8n-mcp

# Check status immediately
systemctl status n8n-mcp

# View startup logs
journalctl -u n8n-mcp -n 50 --no-pager
```

**Expected Output**:
```
● n8n-mcp.service - n8n-MCP HTTP Server
     Loaded: loaded (/etc/systemd/system/n8n-mcp.service; enabled; vendor preset: enabled)
     Active: active (running) since Wed 2025-11-06 12:00:00 UTC; 5s ago
   Main PID: 12345 (node)
      Tasks: 11 (limit: 4915)
     Memory: 150.0M
        CPU: 1.234s
     CGroup: /system.slice/n8n-mcp.service
             └─12345 /usr/bin/node dist/mcp/index.js

Nov 06 12:00:00 hx-n8n-mcp-server systemd[1]: Started n8n-MCP HTTP Server.
Nov 06 12:00:00 hx-n8n-mcp-server node[12345]: [INFO] Starting n8n-MCP HTTP Server v2.21.1...
Nov 06 12:00:01 hx-n8n-mcp-server node[12345]: [INFO] Server running at http://0.0.0.0:3000
```

**Acceptance Criteria**:
- Service status: `active (running)`
- No errors in journalctl logs
- Startup message shows version 2.21.1
- Server listening on port 3000

**Dependencies**: T3.2 complete

**Estimated Time**: 5 minutes

**If Service Fails to Start**:
1. Check logs: `journalctl -u n8n-mcp -n 100`
2. Verify pre-start checks passed (auth_token, n8n_api_key exist)
3. Check file permissions on /opt/n8n-mcp/
4. Validate environment variables in config.env

**Troubleshooting**:
```bash
# Test manual start to see errors
sudo -u n8n-mcp bash -c 'cd /opt/n8n-mcp && source /etc/n8n-mcp/config.env && node dist/mcp/index.js'
```

---

## Phase 4: Validation & Testing (1 hour)

### **T4.1: Health Endpoint Verification**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T3.3 (service started)

**Description**: Verify N8N MCP HTTP server health endpoint responding correctly.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Test health endpoint (localhost)
curl -v -H "Authorization: Bearer $(sudo cat /etc/n8n-mcp/auth_token)" \
     http://localhost:3000/health

# Save response for documentation
curl -H "Authorization: Bearer $(sudo cat /etc/n8n-mcp/auth_token)" \
     http://localhost:3000/health | jq '.' > /tmp/health-response.json
```

**Expected Response** (HTTP_DEPLOYMENT.md lines 580-599):
```json
{
  "status": "ok",
  "mode": "http-fixed",
  "version": "2.21.1",
  "uptime": 60,
  "memory": {
    "used": 150,
    "total": 512,
    "percentage": 29.3
  },
  "node": {
    "version": "v20.11.0",
    "platform": "linux"
  },
  "features": {
    "n8nApi": true,
    "authFile": true
  }
}
```

**Acceptance Criteria**:
- HTTP 200 OK status
- Response is valid JSON
- `status` = "ok"
- `features.n8nApi` = true (confirms N8N API integration)
- `features.authFile` = true (confirms file-based auth)
- Version matches deployment (2.21.1)

**Dependencies**: T3.3 complete

**Estimated Time**: 10 minutes

**If Health Check Fails**:
- Check service is running: `systemctl status n8n-mcp`
- Check port is listening: `ss -tlnp | grep 3000`
- Check auth token is correct
- Review service logs: `journalctl -u n8n-mcp -n 50`

---

### **T4.2: MCP Protocol Tool List Verification**

**Owner**: @agent-olivia
**Priority**: P0 Critical
**Status**: ⬜ Pending
**Depends On**: T4.1 (health check passed)

**Description**: Verify all 42 MCP tools are accessible via MCP protocol endpoint.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# List all MCP tools
curl -X POST http://localhost:3000/mcp \
  -H "Authorization: Bearer $(sudo cat /etc/n8n-mcp/auth_token)" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | jq '.result.tools | length'

# Save full tool list for documentation
curl -X POST http://localhost:3000/mcp \
  -H "Authorization: Bearer $(sudo cat /etc/n8n-mcp/auth_token)" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | jq '.' > /tmp/tools-list.json

# Check for specific management tools
curl -X POST http://localhost:3000/mcp \
  -H "Authorization: Bearer $(sudo cat /etc/n8n-mcp/auth_token)" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","method":"tools/list","id":1}' | jq '.result.tools[] | select(.name | contains("n8n_")) | .name'
```

**Expected Output**:
```
42  # Total tool count

# Management tools present:
"n8n_create_workflow"
"n8n_list_workflows"
"n8n_get_workflow"
"n8n_update_full_workflow"
"n8n_update_partial_workflow"
"n8n_delete_workflow"
"n8n_validate_workflow"
"n8n_autofix_workflow"
"n8n_trigger_webhook_workflow"
"n8n_get_execution"
"n8n_list_executions"
"n8n_health_check"
...
```

**Acceptance Criteria**:
- Tool count = 42 (25 documentation + 17 management)
- All `n8n_*` management tools present (validates N8N API integration)
- Documentation tools present (search_nodes, get_node_essentials, etc.)
- Template tools present (list_templates, search_templates, etc.)
- No errors in response

**Dependencies**: T4.1 complete

**Estimated Time**: 10 minutes

**Critical Validation**: If tool count != 42, N8N API integration may have failed.

**Deliverables**: Save tools-list.json to POC-002/06-docs/

---

### **T4.3: N8N API Connectivity Test**

**Owner**: @agent-olivia
**Priority**: P0 Critical
**Status**: ⬜ Pending
**Depends On**: T4.2 (tools verified)

**Description**: Verify N8N MCP server can successfully connect to N8N instance API.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Test N8N health check tool
curl -X POST http://localhost:3000/mcp \
  -H "Authorization: Bearer $(sudo cat /etc/n8n-mcp/auth_token)" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "n8n_health_check",
      "arguments": {}
    },
    "id": 2
  }' | jq '.'
```

**Expected Response**:
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "N8N API connection successful. Instance is reachable at http://hx-n8n-server.hx.dev.local:5678"
      }
    ]
  }
}
```

**Acceptance Criteria**:
- Health check tool executes without error
- Response indicates N8N API reachable
- No authentication errors
- Connection successful

**Dependencies**: T4.2 complete

**Estimated Time**: 10 minutes

**If Health Check Fails**:
- Verify N8N instance running (T0.1)
- Verify API key correct (T0.2)
- Check network connectivity (T0.6)
- Review N8N MCP service logs for API errors

---

### **T4.4: Port Listening Verification**

**Owner**: @agent-olivia OR @agent-william
**Priority**: Medium
**Status**: ⬜ Pending
**Depends On**: T3.3 (service started)

**Description**: Verify N8N MCP service is listening on port 3000.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Check port listening
ss -tlnp | grep 3000

# Check process
ps aux | grep -i n8n-mcp | grep -v grep

# Check network bindings
sudo netstat -tulpn | grep :3000
```

**Expected Output**:
```
LISTEN  0  511  0.0.0.0:3000  0.0.0.0:*  users:(("node",pid=12345,fd=19))

n8n-mcp   12345  0.5  3.8 1234567 150000 ?  Ssl  12:00  0:05 /usr/bin/node dist/mcp/index.js

tcp  0  0  0.0.0.0:3000  0.0.0.0:*  LISTEN  12345/node
```

**Acceptance Criteria**:
- Port 3000 listening on 0.0.0.0 (all interfaces)
- Process owner: n8n-mcp user
- Process command: node dist/mcp/index.js

**Dependencies**: T3.3 complete

**Estimated Time**: 5 minutes

**Network Accessibility Test**:
```bash
# From control plane or another HX server
curl -I -H "Authorization: Bearer <token>" \
     http://hx-n8n-mcp-server.hx.dev.local:3000/health
```

**Expected**: HTTP 200 OK (confirms network accessibility)

---

### **T4.5: Service Logs Review**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T3.3 (service started)

**Description**: Review systemd journal logs for N8N MCP service to identify any errors or warnings.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# View last 100 log lines
journalctl -u n8n-mcp -n 100 --no-pager

# Check for errors
journalctl -u n8n-mcp --since "10 minutes ago" | grep -iE '(error|fatal|exception)'

# Check startup sequence
journalctl -u n8n-mcp --since "10 minutes ago" | grep -i 'starting\|started\|running'

# Save logs for documentation
journalctl -u n8n-mcp --since "10 minutes ago" --no-pager > /tmp/n8n-mcp-startup-logs.txt
```

**Expected Output**:
```
Nov 06 12:00:00 hx-n8n-mcp-server systemd[1]: Starting n8n-MCP HTTP Server...
Nov 06 12:00:00 hx-n8n-mcp-server systemd[1]: Started n8n-MCP HTTP Server.
Nov 06 12:00:00 hx-n8n-mcp-server node[12345]: [INFO] Starting n8n-MCP HTTP Server v2.21.1...
Nov 06 12:00:00 hx-n8n-mcp-server node[12345]: [INFO] Loading node database from data/nodes.db
Nov 06 12:00:00 hx-n8n-mcp-server node[12345]: [INFO] Database loaded: 536 nodes
Nov 06 12:00:01 hx-n8n-mcp-server node[12345]: [INFO] N8N API configured: http://hx-n8n-server.hx.dev.local:5678
Nov 06 12:00:01 hx-n8n-mcp-server node[12345]: [INFO] Server running at http://0.0.0.0:3000
Nov 06 12:00:01 hx-n8n-mcp-server node[12345]: [INFO] Endpoints: /health, /mcp
```

**Acceptance Criteria**:
- 0 ERROR level entries
- 0 FATAL level entries
- 0 EXCEPTION entries
- Startup sequence shows database loaded (536 nodes)
- N8N API configuration logged
- Server running message present

**Dependencies**: T3.3 complete

**Estimated Time**: 10 minutes

**If Errors Found**: Investigate and remediate before proceeding to Phase 5.

**Deliverables**: Save startup logs to POC-002/06-docs/n8n-mcp-startup-logs.txt

---

### **T4.6: Service Stability Test (1 Hour)**

**Owner**: @agent-olivia
**Priority**: Medium
**Status**: ⬜ Pending
**Depends On**: T4.1, T4.2, T4.3, T4.4, T4.5 (all validations passed)

**Description**: Monitor N8N MCP service for 1 hour to verify stability (no crashes, memory leaks, or errors).

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Monitor service status every 5 minutes for 1 hour
watch -n 300 'systemctl status n8n-mcp'

# Monitor memory usage
watch -n 60 'ps -o pid,user,%mem,rss,command -p $(pgrep -f n8n-mcp)'

# Monitor logs in real-time
journalctl -u n8n-mcp -f
```

**Monitoring Checklist** (check every 15 minutes):
- [ ] Service status: active (running)
- [ ] Memory usage: < 512MB (50% of limit)
- [ ] CPU usage: reasonable (< 50% sustained)
- [ ] No new ERROR entries in logs
- [ ] Uptime increasing (no restarts)

**Acceptance Criteria**:
- Service runs continuously for 1+ hour
- No service restarts
- No ERROR log entries during monitoring period
- Memory usage stable (no leaks)
- Uptime increases linearly

**Dependencies**: All Phase 4 tests (T4.1-T4.5) passed

**Estimated Time**: 1 hour (monitoring duration)

**Deliverables**:
- Memory/CPU usage snapshot logged
- Uptime confirmation recorded
- Any anomalies documented

**Concurrent Activity**: Can proceed to Phase 5 (client configuration) while monitoring continues.

---

## Phase 5: Client Configuration & Testing (30 minutes)

### **T5.1: Document AUTH_TOKEN for Client Configuration**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T0.5 (AUTH_TOKEN generated)

**Description**: Extract AUTH_TOKEN value from server and document in POC-002 for client configuration.

**Commands**:
```bash
ssh hx-n8n-mcp-server

# Retrieve AUTH_TOKEN (this is the only time we'll expose it)
sudo cat /etc/n8n-mcp/auth_token
```

**Documentation**:
Create file: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/06-docs/client-configuration.md`

**Content**:
```markdown
# N8N MCP Client Configuration

## Server Details
- **URL**: http://hx-n8n-mcp-server.hx.dev.local:3000/mcp
- **AUTH_TOKEN**: <paste-token-value-here>

## Claude Code Configuration

Add to MCP servers configuration:

\`\`\`json
{
  "mcpServers": {
    "n8n-hx": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://hx-n8n-mcp-server.hx.dev.local:3000/mcp",
        "--header",
        "Authorization: Bearer <AUTH_TOKEN_VALUE>"
      ]
    }
  }
}
\`\`\`

**IMPORTANT**: Replace `<AUTH_TOKEN_VALUE>` with actual token from above.

## Security Note
- This token grants full access to N8N MCP tools
- Store securely, never commit to version control
- Rotate periodically (monthly recommended)
```

**Acceptance Criteria**:
- AUTH_TOKEN value documented
- Client configuration template provided
- Security notes included

**Dependencies**: T0.5 complete

**Estimated Time**: 10 minutes

**Security**: Ensure POC-002/06-docs/ directory has restricted permissions (not world-readable).

---

### **T5.2: Configure Claude Code MCP Client**

**Owner**: @agent-zero (for testing) OR CAIO
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T5.1 (AUTH_TOKEN documented), T4.3 (N8N API verified)

**Description**: Configure Claude Code to connect to N8N MCP server.

**Steps**:
1. Open Claude Code MCP servers configuration
2. Add N8N MCP server entry (from T5.1 template)
3. Replace `<AUTH_TOKEN_VALUE>` with actual token
4. Save configuration
5. Restart Claude Code

**Configuration File Location** (platform-specific):
- **Linux**: `~/.config/claude-code/mcp_servers.json`
- **macOS**: `~/Library/Application Support/claude-code/mcp_servers.json`
- **Windows**: `%APPDATA%\claude-code\mcp_servers.json`

**Configuration Entry**:
```json
{
  "mcpServers": {
    "n8n-hx": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "http://hx-n8n-mcp-server.hx.dev.local:3000/mcp",
        "--header",
        "Authorization: Bearer <ACTUAL_TOKEN_HERE>"
      ]
    }
  }
}
```

**Acceptance Criteria**:
- Configuration file updated
- No JSON syntax errors
- AUTH_TOKEN correctly inserted (no placeholder text)
- Claude Code restarts without errors

**Dependencies**: T5.1 complete

**Estimated Time**: 10 minutes

**Troubleshooting**:
- If connection fails: Verify AUTH_TOKEN matches server token exactly
- If "command not found: npx": Ensure Node.js 18+ installed on client machine
- If network error: Verify server accessible from client machine

---

### **T5.3: Test MCP Tool Discovery from Client**

**Owner**: @agent-zero OR CAIO
**Priority**: P0 Critical
**Status**: ⬜ Pending
**Depends On**: T5.2 (client configured)

**Description**: Verify Claude Code can discover and list N8N MCP tools.

**Test Steps**:
1. Restart Claude Code
2. Open new chat/conversation
3. Ask: **"List all available N8N MCP tools"**

**Expected Response**:
Claude should list 42 tools, including:
- **Documentation Tools**: search_nodes, get_node_essentials, list_nodes, get_node_documentation, etc.
- **Template Tools**: list_templates, search_templates, get_template, etc.
- **Validation Tools**: validate_workflow, validate_node_operation, etc.
- **Management Tools**: n8n_create_workflow, n8n_list_workflows, n8n_get_workflow, n8n_update_workflow, n8n_delete_workflow, n8n_validate_workflow, n8n_trigger_webhook_workflow, n8n_get_execution, n8n_list_executions, n8n_health_check, etc.

**Acceptance Criteria**:
- Claude successfully connects to N8N MCP server
- All 42 tools visible to Claude
- Tool descriptions present
- No authentication errors

**Dependencies**: T5.2 complete

**Estimated Time**: 5 minutes

**If Tool Discovery Fails**:
- Check Claude Code logs for connection errors
- Verify server is accessible: `curl -I http://hx-n8n-mcp-server.hx.dev.local:3000/health`
- Verify AUTH_TOKEN correct in client config
- Check mcp-remote installed: `npx mcp-remote --version`

---

### **T5.4: Test Workflow Creation via Claude Code**

**Owner**: @agent-zero OR CAIO
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T5.3 (tool discovery successful)

**Description**: End-to-end test - have Claude Code create a simple N8N workflow using N8N MCP tools.

**Test Prompt**:
```
Create a simple N8N workflow that:
1. Has a Manual Trigger node
2. Has an HTTP Request node that calls https://api.github.com/users/octocat
3. Deploy it to my N8N instance

Use the N8N MCP tools to build and deploy this workflow.
```

**Expected Behavior**:
1. Claude calls `search_nodes` or `get_node_essentials` to research nodes
2. Claude calls `validate_workflow` to validate structure
3. Claude calls `n8n_create_workflow` to deploy
4. Claude reports workflow ID and success

**Acceptance Criteria**:
- Claude successfully creates workflow
- Workflow appears in N8N instance (verify at http://hx-n8n-server.hx.dev.local:5678)
- Workflow has correct nodes (Manual Trigger + HTTP Request)
- No errors during creation process

**Dependencies**: T5.3 complete

**Estimated Time**: 10 minutes

**Validation**:
```bash
# Verify workflow created in N8N
curl -H "X-N8N-API-KEY: $(cat /etc/n8n-mcp/n8n_api_key)" \
     http://hx-n8n-server.hx.dev.local:5678/api/v1/workflows | jq '.data[] | {id, name}'
```

**If Workflow Creation Fails**:
- Check N8N API connectivity (T4.3)
- Review N8N MCP service logs for errors
- Verify N8N API key permissions (can create workflows)
- Test manually with curl + N8N API

**Deliverables**: Screenshot or log of successful workflow creation saved to POC-002/06-docs/

---

## Phase 6: Documentation & Governance (1 hour)

### **T6.1: Create Deployment Postmortem**

**Owner**: @agent-olivia
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: All phases complete

**Description**: Document deployment process, issues encountered, resolutions, and operational status.

**File**: `/opt/n8n-mcp/docs/DEPLOYMENT-POSTMORTEM.md` OR `/etc/n8n-mcp/DEPLOYMENT-POSTMORTEM.md`

**Content Template**:
```markdown
# N8N MCP Deployment Postmortem

**Service**: N8N MCP HTTP Server
**Server**: hx-n8n-mcp-server (192.168.10.214)
**Deployment Date**: 2025-11-06
**Deployed By**: @agent-olivia (Olivia Chang)
**Status**: OPERATIONAL

## Timeline
- [Date Time]: Phase 0 prerequisites started
- [Date Time]: Node.js installed
- [Date Time]: Service deployed
- [Date Time]: Validation complete
- [Date Time]: Client tested

## Configuration
- **Version**: n8n-mcp v2.21.1
- **Deployment Method**: Native (Node.js 20+ + systemd)
- **Mode**: HTTP (port 3000)
- **N8N API Integration**: Enabled (http://hx-n8n-server.hx.dev.local:5678)
- **Tool Count**: 42 (25 documentation + 17 management)

## Issues Encountered
[Document any issues from task execution]

## Resolutions Applied
[Document how issues were resolved]

## Current Status
- **Service**: Active (running)
- **Uptime**: [duration]
- **Memory Usage**: [current]
- **Response Time**: [average]

## Lessons Learned
[Document what went well and what could be improved]

## Next Steps
- Phase 2: FastMCP gateway integration
- Monitoring setup
- Backup strategy
```

**Acceptance Criteria**:
- Postmortem file created on server
- All sections completed
- Issues and resolutions documented
- Current operational status confirmed

**Dependencies**: All phases 0-5 complete

**Estimated Time**: 20 minutes

---

### **T6.2: Update Platform Nodes Document**

**Owner**: @agent-zero
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: T6.1 (postmortem complete)

**Description**: Update hx-n8n-mcp-server entry in Platform Nodes governance document.

**File**: `/srv/cc/Governance/0.0-governance/0.2-hana_x_platform_nodes_final.md`

**Location**: Lines 86-90

**Current Content**:
```markdown
### hx-n8n-mcp-server (192.168.10.214) — ⬜
**Role:** n8n Model Context Protocol (MCP) server.
**Primary responsibilities:** To be determined.
**Status:** PLANNED
```

**Updated Content**:
```markdown
### hx-n8n-mcp-server (192.168.10.214) — ✅
**Role:** n8n Model Context Protocol (MCP) server (HTTP mode, native deployment).
**Primary responsibilities:** Exposes 536 n8n nodes (263 AI-capable) via 42 MCP tools for AI-assisted workflow automation. Provides documentation access (25 tools) and workflow management capabilities (17 tools) integrated with N8N API.
**Status:** OPERATIONAL - Native deployment (Node.js 20.11.0 + systemd), Phase 1 complete (all 42 tools)
**Version:** n8n-mcp v2.21.1
**Deployment:** 2025-11-06 (POC-002)
**N8N API Integration:** http://hx-n8n-server.hx.dev.local:5678
**Access:** HTTP server on port 3000 (internal HX network)
```

**Acceptance Criteria**:
- Status changed from ⬜ to ✅
- Role description updated with accurate capabilities
- Version and deployment date added
- N8N API integration noted

**Dependencies**: T6.1 complete

**Estimated Time**: 10 minutes

---

### **T6.3: Update Network Topology Document**

**Owner**: @agent-alex (Platform Architect)
**Priority**: Medium
**Status**: ⬜ Pending
**Depends On**: T6.1 (postmortem complete)

**Description**: Add N8N MCP server entry to Network Topology port mapping reference.

**File**: `/srv/cc/Governance/0.0-governance/0.3.1-hx-network-topology-diagram.md`

**Location**: Section 5.2 (Port Mapping Reference), after line 351

**Entry to Add**:
```markdown
| **N8N MCP** | hx-n8n-mcp-server | 3000 | TCP | Workflow automation MCP (HTTP mode) | Internal HX network only |
```

**Acceptance Criteria**:
- Entry added to port mapping table
- Port 3000 documented
- Protocol marked as TCP
- Access scope noted (internal only)

**Dependencies**: T6.1 complete

**Estimated Time**: 10 minutes

---

### **T6.4: Create POC-002 Completion Summary**

**Owner**: @agent-zero
**Priority**: High
**Status**: ⬜ Pending
**Depends On**: All phases complete, T6.1-T6.3 (governance updates)

**Description**: Create comprehensive POC-002 completion summary with acceptance criteria results, lessons learned, and recommendations.

**File**: `/srv/cc/Governance/x-poc2-n8n-mcp-deployment/05-COMPLETION-SUMMARY.md`

**Content Sections**:
1. Executive Summary
2. Timeline (all 6 phases)
3. Acceptance Criteria Results (all 9 ACs with pass/fail status)
4. Deliverables (files created, configurations applied)
5. Issues Encountered & Resolutions
6. Multi-Agent Coordination Summary
7. Lessons Learned (what went well, what could improve)
8. Recommendations for Next Steps (Phase 2 gateway integration)
9. Sign-Off (orchestrator, executing agent, CAIO approval)
10. Metrics Summary

**Acceptance Criteria**:
- All sections complete
- All ACs documented with results
- Lessons learned captured
- Next steps identified
- Ready for CAIO review

**Dependencies**: All tasks complete

**Estimated Time**: 30 minutes

**Deliverables**: Completion summary document ready for governance review.

---

### **T6.5: Update Gap Analysis Status**

**Owner**: @agent-zero
**Priority**: Medium
**Status**: ⬜ Pending
**Depends On**: T6.4 (completion summary)

**Description**: Mark P0-GOV-001 (N8N MCP deployment) as COMPLETE in Gap Analysis document.

**File**: `/srv/cc/Governance/WIP/Current State/GAP-ANALYSIS-AND-REMEDIATION.md`

**Location**: Line ~1325 (P0-GOV-001 entry)

**Update**:
- Status: OPEN → **COMPLETE**
- Completion Date: 2025-11-06
- Reference: POC-002 completion summary
- Notes: Phase 1 complete (all 42 tools operational), Phase 2 (FastMCP gateway integration) deferred

**Acceptance Criteria**:
- Gap Analysis updated
- Status reflects completion
- Reference to POC-002 added

**Dependencies**: T6.4 complete

**Estimated Time**: 10 minutes

---

## Appendix A: Acceptance Criteria Summary

**AC-001**: Node.js 20+ Installed
**AC-002**: N8N MCP Built Successfully
**AC-003**: Systemd Service Active
**AC-004**: Port 3000 Listening
**AC-005**: MCP Protocol Responding
**AC-006**: All 42 Tools Accessible
**AC-007**: N8N API Integration Working
**AC-008**: Service Logs Clean
**AC-009**: Client Connection Successful

**All must pass for POC-002 Phase 1 completion.**

---

## Appendix B: Rollback Procedures

If deployment fails at any phase, follow these rollback steps:

### Phase 3 Rollback (Service Failed):
```bash
ssh hx-n8n-mcp-server
sudo systemctl stop n8n-mcp
sudo systemctl disable n8n-mcp
sudo rm /etc/systemd/system/n8n-mcp.service
sudo systemctl daemon-reload
```

### Phase 1-2 Rollback (Installation Failed):
```bash
ssh hx-n8n-mcp-server
sudo systemctl stop n8n-mcp 2>/dev/null
sudo rm -rf /opt/n8n-mcp
sudo rm -rf /etc/n8n-mcp
sudo userdel n8n-mcp
```

### Complete Rollback (All Phases):
```bash
# Remove service
sudo systemctl stop n8n-mcp
sudo systemctl disable n8n-mcp
sudo rm /etc/systemd/system/n8n-mcp.service
sudo systemctl daemon-reload

# Remove installation
sudo rm -rf /opt/n8n-mcp
sudo rm -rf /etc/n8n-mcp
sudo userdel n8n-mcp

# Optional: Remove Node.js (if installed for this POC only)
sudo apt remove nodejs npm
sudo apt autoremove
```

**Rollback Time**: < 10 minutes

---

## Appendix C: Coordination Matrix

| Agent | Phase | Tasks | Status | Critical Path |
|-------|-------|-------|--------|---------------|
| **@agent-omar** | 0 | T0.1, T0.2 | ⬜ Pending | ⚠️ **BLOCKER** |
| **@agent-frank** | 0 | T0.2 (alt) | ⬜ Pending | ⚠️ **BLOCKER** |
| **@agent-william** | 0 | T0.3, T0.4 | ⬜ Pending | **CRITICAL** |
| **@agent-olivia** | 0-5 | T0.5-T5.4 | ⬜ Pending | **PRIMARY** |
| **@agent-alex** | 6 | T6.3 | ⬜ Pending | Post-deployment |
| **@agent-zero** | All | T6.2, T6.4, T6.5 | ⬜ Pending | **COORDINATOR** |

---

**VERSION**: 1.0
**LAST UPDATED**: 2025-11-06
**STATUS**: Ready for Execution (pending CAIO approval)

**END OF TASK LIST**
