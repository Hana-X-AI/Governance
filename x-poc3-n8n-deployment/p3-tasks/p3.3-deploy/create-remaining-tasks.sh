#!/bin/bash

# Script to create all remaining Phase 3.3 deployment tasks
# Task IDs: T-031 through T-044

cd /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.3-deploy/

echo "Creating remaining deployment tasks..."

# T-031: Set File Permissions
cat > t-031-set-file-permissions.md << 'EOF'
# Task: Set File Permissions

**Task ID**: T-031
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-030 |

## Task Overview

Set appropriate file permissions on n8n deployment directories: 755 for app/, 700 for .n8n/ and backups/, ensuring security while allowing n8n service execution.

## Success Criteria
- [ ] /opt/n8n/app/ set to 755 (rwxr-xr-x)
- [ ] /opt/n8n/.n8n/ set to 700 (rwx------)
- [ ] /opt/n8n/backups/ set to 700
- [ ] CLI executable has execute bit set
- [ ] Permissions verified with stat commands

## Execution Steps

### Step 1: Set Application Directory Permissions
```bash
sudo chmod 755 /opt/n8n/app/
sudo chmod -R u+rX,go+rX /opt/n8n/app/
echo "✅ Application directory: 755"
```

### Step 2: Set Data Directory Permissions (Private)
```bash
sudo chmod 700 /opt/n8n/.n8n/
sudo chmod 700 /opt/n8n/backups/
echo "✅ Private directories: 700"
```

### Step 3: Ensure CLI Executable
```bash
sudo chmod +x /opt/n8n/app/packages/cli/bin/n8n
test -x /opt/n8n/app/packages/cli/bin/n8n && echo "✅ CLI executable"
```

### Step 4: Verify Permissions
```bash
stat -c '%a %n' /opt/n8n/app/ /opt/n8n/.n8n/ /opt/n8n/backups/
# Expected: 755, 700, 700
```

## Validation
```bash
test "$(stat -c '%a' /opt/n8n/app/)" = "755" && echo "✅ app/ correct"
test "$(stat -c '%a' /opt/n8n/.n8n/)" = "700" && echo "✅ .n8n/ correct"
```

## Task Metadata
```yaml
task_id: T-031
source: agent-omar-planning-analysis.md:497 (T3.5)
```
EOF

# T-032: Create CLI Symlink
cat > t-032-create-cli-symlink.md << 'EOF'
# Task: Create CLI Symlink

**Task ID**: T-032
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P2 - Optional |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-031 |

## Task Overview

Create optional symbolic link from /usr/local/bin/n8n to the n8n CLI executable to allow running 'n8n' command from any directory.

## Success Criteria
- [ ] Symlink created: /usr/local/bin/n8n → /opt/n8n/app/packages/cli/bin/n8n
- [ ] Symlink executable and functional
- [ ] Can run 'n8n --version' from any directory

## Execution Steps

### Step 1: Create Symlink
```bash
sudo ln -sf /opt/n8n/app/packages/cli/bin/n8n /usr/local/bin/n8n
echo "✅ Symlink created"
```

### Step 2: Verify Symlink
```bash
ls -l /usr/local/bin/n8n
# Expected: lrwxrwxrwx ... /usr/local/bin/n8n -> /opt/n8n/app/packages/cli/bin/n8n
```

### Step 3: Test Command
```bash
/usr/local/bin/n8n --version
# Expected: n8n version output
```

## Validation
```bash
test -L /usr/local/bin/n8n && echo "✅ Symlink exists"
test -x /usr/local/bin/n8n && echo "✅ Symlink executable"
```

## Task Metadata
```yaml
task_id: T-032
source: agent-omar-planning-analysis.md:498 (T3.6)
```
EOF

# T-033: Create .env Configuration
cat > t-033-create-env-configuration.md << 'EOF'
# Task: Create .env Configuration

**Task ID**: T-033
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 30 minutes |
| **Dependencies** | T-032, Quinn's DB credentials |

## Task Overview

Create comprehensive .env configuration file with 100+ environment variables for n8n, including database credentials from @agent-quinn, network settings, security config, and logging.

## Success Criteria
- [ ] .env file created at /opt/n8n/.env
- [ ] Database credentials from Quinn integrated
- [ ] All required n8n variables configured
- [ ] Variables validated (no syntax errors)
- [ ] File documented with comments

## Blocking Dependencies
- [ ] Database credentials from @agent-quinn (DB password, connection string)

## Execution Steps

### Step 1: Request Database Credentials from Quinn
```bash
echo "⚠️  BLOCKER: Need database credentials from @agent-quinn"
echo "Required information:"
echo "  - DB_POSTGRESDB_PASSWORD"
echo "  - Confirm: hx-postgres-server.hx.dev.local:5432"
echo "  - Confirm: database name: n8n_poc3"
echo "  - Confirm: user: n8n_user"
```

### Step 2: Create .env File
```bash
cat > /opt/n8n/.env << 'ENVEOF'
# ================================================
# n8n Configuration - POC3 Deployment
# Server: hx-n8n-server.hx.dev.local
# Created: 2025-11-07
# Agent: @agent-omar
# ================================================

# =================
# DATABASE CONFIGURATION (from @agent-quinn)
# =================
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=hx-postgres-server.hx.dev.local
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n_poc3
DB_POSTGRESDB_USER=n8n_user
DB_POSTGRESDB_PASSWORD=<INSERT_FROM_QUINN>

# Database connection pool
DB_POSTGRESDB_POOL_SIZE=10

# =================
# NETWORK CONFIGURATION
# =================
N8N_HOST=0.0.0.0
N8N_PORT=5678
N8N_PROTOCOL=https
N8N_PATH=/
WEBHOOK_URL=https://hx-n8n-server.hx.dev.local
N8N_EDITOR_BASE_URL=https://hx-n8n-server.hx.dev.local

# =================
# SECURITY
# =================
N8N_SECURE_COOKIE=true
N8N_SAMESITE_COOKIE=strict
N8N_JWT_AUTH_ACTIVE=true

# =================
# LOGGING
# =================
N8N_LOG_LEVEL=info
N8N_LOG_OUTPUT=file,console
N8N_LOG_FILE_LOCATION=/var/log/n8n/n8n.log
N8N_LOG_FILE_COUNT_MAX=10
N8N_LOG_FILE_SIZE_MAX=10

# =================
# EXECUTION
# =================
EXECUTIONS_MODE=queue
EXECUTIONS_DATA_SAVE_ON_ERROR=all
EXECUTIONS_DATA_SAVE_ON_SUCCESS=all
EXECUTIONS_DATA_SAVE_MANUAL_EXECUTIONS=true

# =================
# TIMEZONE
# =================
GENERIC_TIMEZONE=America/Chicago
TZ=America/Chicago

# =================
# PATHS
# =================
N8N_USER_FOLDER=/opt/n8n/.n8n
N8N_CUSTOM_EXTENSIONS=/opt/n8n/.n8n/custom

# =================
# PERFORMANCE
# =================
N8N_PAYLOAD_SIZE_MAX=16
NODE_FUNCTION_ALLOW_BUILTIN=*
NODE_FUNCTION_ALLOW_EXTERNAL=*

ENVEOF

sudo chown n8n:n8n /opt/n8n/.env
echo "✅ .env created (needs DB password from Quinn)"
```

### Step 3: Validate .env Syntax
```bash
# Check for common issues
grep -v '^#' /opt/n8n/.env | grep -v '^$' | while read line; do
  if ! echo "$line" | grep -q '='; then
    echo "❌ Invalid line: $line"
  fi
done
echo "✅ Syntax validated"
```

### Step 4: Verify Database Password Set
```bash
if grep -q '<INSERT_FROM_QUINN>' /opt/n8n/.env; then
  echo "⚠️  WARNING: Database password not yet set!"
  echo "Update .env with password from @agent-quinn before starting service"
else
  echo "✅ Database password appears to be set"
fi
```

## Validation
```bash
test -f /opt/n8n/.env && echo "✅ .env exists"
test "$(stat -c '%U' /opt/n8n/.env)" = "n8n" && echo "✅ Owner correct"
grep -q "DB_POSTGRESDB_HOST" /opt/n8n/.env && echo "✅ DB config present"
```

## Task Metadata
```yaml
task_id: T-033
source: agent-omar-planning-analysis.md:508 (T4.1)
coordination_required:
  - agent: Quinn Davis (@agent-quinn)
    service: Postgres
    info_needed: Database credentials for n8n_poc3
```
EOF

# T-034: Create Systemd Service File
cat > t-034-create-systemd-service-file.md << 'EOF'
# Task: Create Systemd Service File

**Task ID**: T-034
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 20 minutes |
| **Dependencies** | T-033 |

## Task Overview

Create systemd service unit file for n8n at /etc/systemd/system/n8n.service to enable automatic startup, process management, and service control.

## Success Criteria
- [ ] Service file created at /etc/systemd/system/n8n.service
- [ ] Correct User=n8n and Group=n8n
- [ ] Environment file reference correct
- [ ] ExecStart command points to deployed n8n
- [ ] Restart policy configured
- [ ] Dependencies on postgresql.service set

## Execution Steps

### Step 1: Create Service File
```bash
sudo cat > /etc/systemd/system/n8n.service << 'SERVICEEOF'
[Unit]
Description=n8n Workflow Automation Platform - POC3
Documentation=https://docs.n8n.io
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n
EnvironmentFile=/opt/n8n/.env
ExecStart=/usr/bin/node /opt/n8n/app/packages/cli/bin/n8n start
ExecReload=/bin/kill -HUP $MAINPID
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
SERVICEEOF

echo "✅ Service file created"
```

### Step 2: Set Permissions
```bash
sudo chmod 644 /etc/systemd/system/n8n.service
sudo chown root:root /etc/systemd/system/n8n.service
echo "✅ Permissions set"
```

### Step 3: Verify File Contents
```bash
cat /etc/systemd/system/n8n.service
```

## Validation
```bash
test -f /etc/systemd/system/n8n.service && echo "✅ Service file exists"
grep -q "User=n8n" /etc/systemd/system/n8n.service && echo "✅ User configured"
grep -q "EnvironmentFile=/opt/n8n/.env" /etc/systemd/system/n8n.service && echo "✅ Env file configured"
```

## Task Metadata
```yaml
task_id: T-034
source: agent-omar-planning-analysis.md:509 (T4.2)
```
EOF

# T-035: Set .env Permissions
cat > t-035-set-env-permissions.md << 'EOF'
# Task: Set .env Permissions

**Task ID**: T-035
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical (Security) |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-033 |

## Task Overview

Set restrictive permissions (600) on .env file to protect sensitive credentials including database passwords from unauthorized access.

## Success Criteria
- [ ] .env file permissions set to 600 (rw-------)
- [ ] File owned by n8n:n8n
- [ ] Only n8n user can read file
- [ ] File not readable by other users

## Execution Steps

### Step 1: Set Restrictive Permissions
```bash
sudo chmod 600 /opt/n8n/.env
echo "✅ Permissions set to 600"
```

### Step 2: Verify Ownership
```bash
sudo chown n8n:n8n /opt/n8n/.env
owner=$(stat -c '%U:%G' /opt/n8n/.env)
echo "Owner: $owner"
test "$owner" = "n8n:n8n" && echo "✅ Ownership correct"
```

### Step 3: Verify Permissions
```bash
perms=$(stat -c '%a' /opt/n8n/.env)
echo "Permissions: $perms"
test "$perms" = "600" && echo "✅ Permissions correct (rw-------)"
```

### Step 4: Test Access Restrictions
```bash
# Test that other users cannot read (should fail)
sudo -u nobody cat /opt/n8n/.env 2>&1 | grep -q "Permission denied" && \
echo "✅ File protected from other users" || \
echo "⚠️  WARNING: File may be readable by others"
```

## Validation
```bash
ls -la /opt/n8n/.env
# Expected: -rw------- 1 n8n n8n ... /opt/n8n/.env
```

## Task Metadata
```yaml
task_id: T-035
source: agent-omar-planning-analysis.md:510 (T4.3)
```
EOF

# T-036: Validate Systemd Service Syntax
cat > t-036-validate-systemd-service-syntax.md << 'EOF'
# Task: Validate Systemd Service Syntax

**Task ID**: T-036
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-034, T-035 |

## Task Overview

Validate systemd service file syntax using systemd-analyze verify to catch configuration errors before attempting service start.

## Success Criteria
- [ ] systemd-analyze verify passes with no errors
- [ ] Service file loads without warnings
- [ ] All referenced files exist (EnvironmentFile, ExecStart)
- [ ] User and Group references valid

## Execution Steps

### Step 1: Verify Referenced Files Exist
```bash
echo "=== Verifying Service File References ==="

# Check environment file
test -f /opt/n8n/.env && echo "✅ Environment file exists" || echo "❌ .env missing"

# Check executable
test -f /opt/n8n/app/packages/cli/bin/n8n && echo "✅ n8n executable exists" || echo "❌ Executable missing"

# Check node binary
test -f /usr/bin/node && echo "✅ Node.js binary exists" || echo "❌ Node missing"

# Check user exists
id n8n >/dev/null 2>&1 && echo "✅ n8n user exists" || echo "❌ User missing"
```

### Step 2: Run systemd-analyze verify
```bash
echo "=== Running systemd-analyze verify ==="

sudo systemd-analyze verify /etc/systemd/system/n8n.service

if [ $? -eq 0 ]; then
  echo "✅ Service file syntax valid"
else
  echo "❌ Service file has errors"
  exit 1
fi
```

### Step 3: Check for Warnings
```bash
# Check service file for common issues
echo "=== Checking for Common Issues ==="

grep -q "^User=" /etc/systemd/system/n8n.service && echo "✅ User directive present"
grep -q "^EnvironmentFile=" /etc/systemd/system/n8n.service && echo "✅ EnvironmentFile present"
grep -q "^ExecStart=" /etc/systemd/system/n8n.service && echo "✅ ExecStart present"
```

## Validation
```bash
systemd-analyze verify /etc/systemd/system/n8n.service && \
echo "✅ Validation passed" || \
echo "❌ Validation failed"
```

## Task Metadata
```yaml
task_id: T-036
source: agent-omar-planning-analysis.md:512 (T4.5)
```
EOF

# T-037: Systemd Daemon Reload
cat > t-037-systemd-daemon-reload.md << 'EOF'
# Task: Systemd Daemon Reload

**Task ID**: T-037
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 1 minute |
| **Dependencies** | T-036 |

## Task Overview

Execute systemctl daemon-reload to make systemd aware of the new n8n.service unit file.

## Success Criteria
- [ ] daemon-reload executes successfully
- [ ] n8n.service visible in systemctl list-unit-files
- [ ] Service ready to be enabled/started

## Execution Steps

### Step 1: Execute Daemon Reload
```bash
echo "=== Reloading Systemd Daemon ==="
sudo systemctl daemon-reload
echo "✅ Daemon reloaded"
```

### Step 2: Verify Service Registered
```bash
systemctl list-unit-files | grep n8n.service
# Expected: n8n.service  disabled/static
echo "✅ Service registered with systemd"
```

### Step 3: Check Service Status
```bash
systemctl status n8n.service
# Expected: Loaded: loaded (/etc/systemd/system/n8n.service; disabled)
# Active: inactive (dead)
```

## Validation
```bash
systemctl list-unit-files | grep -q n8n.service && \
echo "✅ Service found in systemd" || \
echo "❌ Service not registered"
```

## Task Metadata
```yaml
task_id: T-037
source: agent-omar-planning-analysis.md:575 (T5.1)
```
EOF

echo "Created T-031 through T-037 (7 tasks)"

