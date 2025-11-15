# Credentials and Secrets Management Standards

**Document Type**: Standards - Security & Operations  
**Created**: November 10, 2025  
**Project Code**: HX-N8N-MCP-001  
**Classification**: Internal - Project Standards  
**Status**: ACTIVE - Required Reading for All Team Members  

---

## Table of Contents

1. [Overview](#overview)
2. [Password Standards](#password-standards)
3. [Ansible Vault Introduction](#ansible-vault-introduction)
4. [Variable Usage Patterns](#variable-usage-patterns)
5. [Environment File Patterns](#environment-file-patterns)
6. [n8n MCP Server Specific Patterns](#n8n-mcp-server-specific-patterns)
7. [Team Workflow](#team-workflow)
8. [Security Considerations](#security-considerations)

---

## 1. Overview

### 1.1 Purpose

This document establishes credentials and secrets management standards for the n8n MCP Server project. It introduces **Ansible Vault** as the primary secrets management tool while maintaining existing HANA-X password standards and .env file patterns.

**Key Principles**:
- **Ansible Vault** stores and encrypts all secrets
- **Variables** used in playbooks and configurations where possible
- **.env files** continue to be used for application configuration
- **Existing credentials** remain unchanged
- **Simple and consistent** patterns for all team members

---

### 1.2 Scope

**Applies to**:
- n8n MCP Server deployment (hx-n8n-mcp-server at 192.168.10.214)
- Service account credentials
- Database passwords
- API keys and tokens
- TLS certificates and keys
- Configuration secrets

**Does NOT apply to**:
- Existing deployed services (no changes to current credentials)
- User personal passwords (out of project scope)
- External third-party services (unless integrated into n8n MCP)

---

## 2. Password Standards

### 2.1 The Two Standard Passwords

**HANA-X uses exactly TWO standard passwords** for different account types:

#### **Service/System Accounts: `Major8859`**

**Pattern**: Alphanumeric only, **NO special characters**  
**Use for**:
- Service accounts (e.g., `svc-n8n`, `n8n@hx.dev.local`)
- System accounts running services
- Database service accounts (PostgreSQL, Redis, etc.)
- Any account used in connection URLs

**Why NO special characters**: Applications using connection URL format (TypeORM, Prisma, etc.) fail with special characters due to URL encoding issues.

**Examples**:
```bash
# Service account
n8n@hx.dev.local → Password: Major8859

# Database service account
svc-n8n → Password: Major8859

# Redis connection (if auth enabled)
redis://hx-redis-server.hx.dev.local:6379 → Password: Major8859
```

---

#### **User/Domain Accounts: `Major8859!`**

**Pattern**: Alphanumeric + exclamation mark  
**Use for**:
- Domain administrator (Administrator@hx.dev.local)
- Local administrator (agent0)
- Interactive user accounts
- Any account for human login

**Why exclamation mark**: Adds complexity while remaining memorable and not causing URL encoding issues in non-URL contexts.

**Examples**:
```bash
# Domain administrator
Administrator@hx.dev.local → Password: Major8859!

# Local administrator
agent0 → Password: Major8859!

# SSH login
ssh agent0@hx-n8n-mcp-server.hx.dev.local
Password: Major8859!
```

---

### 2.2 Ansible Vault Password

**Ansible Vault Master Password**: `Major8859!`

**Purpose**: Encrypts all secrets stored in Ansible Vault  
**Pattern**: Same as user/domain accounts (with exclamation mark)  
**Usage**: Required when encrypting/decrypting vault files

**Why this password**: 
- Consistent with existing HANA-X domain administrator pattern
- Easy to remember for all team members
- Acceptable security for development environment

---

### 2.3 Decision Matrix

```
┌──────────────────────────────────────────────────────────────┐
│ What type of account is this?                                │
└──────────────────────┬───────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
    SERVICE/SYSTEM                USER/DOMAIN
        │                             │
        ▼                             ▼
   Major8859                     Major8859!
   (no special chars)            (with !)
        │                             │
        │                             │
   Examples:                     Examples:
   - n8n@hx.dev.local           - agent0
   - svc-n8n                    - Administrator@hx.dev.local
   - Database accounts          - SSH logins
   - Service accounts           - Interactive users
```

---

### 2.4 Existing Credentials (DO NOT CHANGE)

**CRITICAL**: The following credentials are already deployed and **MUST NOT BE CHANGED** during this project:

| Account | Current Password | Type | Notes |
|---------|------------------|------|-------|
| `agent0` (all servers) | `Major8859!` | Local admin | Do not change |
| `Administrator@hx.dev.local` | `Major3059!` | Domain admin | Do not change |
| `qdrant@hx.dev.local` | `Major8859!` | Service | Do not change |
| `postgres@hx.dev.local` | `Major8859!` | Service | Do not change |
| `redis@hx.dev.local` | `Major8859!` | Service | Do not change |
| `svc-postgres` | `Major8859` | Database | Do not change |
| `svc-litellm` | `Major8859` | Database | Do not change |
| `svc-n8n` | `Major8859` | Database | Do not change |
| `litellm@hx.dev.local` | (existing) | Service | Do not change |
| `fastmcp@hx.dev.local` | `Major8859!` | Service | Do not change |
| `n8n@hx.dev.local` | `Major8859!` | Service | Do not change |

**API Keys/Tokens (DO NOT CHANGE)**:
- LiteLLM master key: (existing 64-char hex)
- CodeRabbit API key: (existing)
- CA passphrase: (existing)

---

## 3. Ansible Vault Introduction

### 3.1 What is Ansible Vault?

**Ansible Vault** is an encryption system for protecting sensitive data in Ansible projects.

**Benefits**:
- ✅ Encrypts passwords, API keys, certificates at rest
- ✅ Version control safe (encrypted files can be committed to Git)
- ✅ Integrates seamlessly with Ansible playbooks
- ✅ Simple to use (one master password)
- ✅ Transparent decryption during playbook execution

**For this project**: First time using Ansible Vault in HANA-X infrastructure.

---

### 3.2 Ansible Vault Password

**Master Password**: `Major8859!`

**Password File Location**: `/home/agent0/.ansible/vault_password`

**Setup** (One-time on hx-control-node):
```bash
# Create password file
mkdir -p ~/.ansible
echo 'Major8859!' > ~/.ansible/vault_password
chmod 600 ~/.ansible/vault_password

# Configure Ansible to use password file
cat >> ~/.ansible.cfg << 'EOF'
[defaults]
vault_password_file = ~/.ansible/vault_password
EOF
```

**Verification**:
```bash
# Test vault password
ansible-vault --version
cat ~/.ansible/vault_password
# Should output: Major8859!
```

---

### 3.3 Basic Ansible Vault Commands

#### **Encrypt a File**
```bash
# Create and encrypt new vault file
ansible-vault create secrets.yml
# Opens editor, saves encrypted

# Encrypt existing file
ansible-vault encrypt secrets.yml
```

#### **View Encrypted File**
```bash
# View contents (decrypts in memory, doesn't modify file)
ansible-vault view secrets.yml
```

#### **Edit Encrypted File**
```bash
# Edit encrypted file (decrypts to temp, re-encrypts on save)
ansible-vault edit secrets.yml
```

#### **Decrypt File** (Temporarily)
```bash
# Decrypt to plaintext (DANGER - only for debugging)
ansible-vault decrypt secrets.yml

# Re-encrypt immediately after debugging
ansible-vault encrypt secrets.yml
```

---

### 3.4 Ansible Vault File Structure

**Standard location**: `/srv/ansible/n8n-mcp/vault/secrets.yml`

**Example vault file**:
```yaml
---
# /srv/ansible/n8n-mcp/vault/secrets.yml
# Encrypted with: ansible-vault encrypt secrets.yml

# Service Accounts
n8n_service_password: "Major8859!"
n8n_db_password: "Major8859"

# Database Connections
postgres_host: "hx-postgres-server.hx.dev.local"
postgres_port: 5432
postgres_database: "n8n_mcp"
postgres_user: "svc-n8n"
postgres_password: "Major8859"

# Redis Connection
redis_host: "hx-redis-server.hx.dev.local"
redis_port: 6379
# Redis DEV mode - no password

# MCP Server Configuration
mcp_server_port: 8003
mcp_server_host: "hx-n8n-mcp-server.hx.dev.local"

# SSL/TLS
ssl_cert_path: "/etc/ssl/certs/hx-n8n-mcp-server.crt"
ssl_key_path: "/etc/ssl/private/hx-n8n-mcp-server.key"

# Domain Authentication
domain_name: "hx.dev.local"
domain_user: "Administrator"
domain_password: "Major3059!"

# API Keys (if needed)
# mcp_api_key: "{{ lookup('password', '/dev/null length=64 chars=hexdigits') }}"
```

**After creation**:
```bash
# View encrypted file
ansible-vault view /srv/ansible/n8n-mcp/vault/secrets.yml

# Edit secrets
ansible-vault edit /srv/ansible/n8n-mcp/vault/secrets.yml
```

---

## 4. Variable Usage Patterns

### 4.1 Using Vault Variables in Playbooks

**Load vault file in playbook**:
```yaml
---
# /srv/ansible/n8n-mcp/deploy.yml
- name: Deploy n8n MCP Server
  hosts: hx-n8n-mcp-server
  become: yes
  vars_files:
    - vault/secrets.yml  # Load encrypted secrets
  
  tasks:
    - name: Create n8n service account
      user:
        name: "n8n"
        password: "{{ n8n_service_password | password_hash('sha512') }}"
        shell: /bin/bash
    
    - name: Configure database connection
      template:
        src: templates/env.j2
        dest: /opt/n8n-mcp/.env
        mode: '0600'
        owner: n8n
        group: n8n
```

---

### 4.2 Using Variables in Templates

**Template file**: `/srv/ansible/n8n-mcp/templates/env.j2`
```bash
# n8n MCP Server Configuration
# Generated by Ansible from vault/secrets.yml

# Database Configuration
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST={{ postgres_host }}
DB_POSTGRESDB_PORT={{ postgres_port }}
DB_POSTGRESDB_DATABASE={{ postgres_database }}
DB_POSTGRESDB_USER={{ postgres_user }}
DB_POSTGRESDB_PASSWORD={{ postgres_password }}

# Redis Configuration
REDIS_HOST={{ redis_host }}
REDIS_PORT={{ redis_port }}

# MCP Server Configuration
MCP_PORT={{ mcp_server_port }}
MCP_HOST={{ mcp_server_host }}

# SSL/TLS Certificates
SSL_CERT_PATH={{ ssl_cert_path }}
SSL_KEY_PATH={{ ssl_key_path }}
```

**Result**: `/opt/n8n-mcp/.env` (generated on target server)
```bash
# Database Configuration
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=hx-postgres-server.hx.dev.local
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n_mcp
DB_POSTGRESDB_USER=svc-n8n
DB_POSTGRESDB_PASSWORD=Major8859

# Redis Configuration
REDIS_HOST=hx-redis-server.hx.dev.local
REDIS_PORT=6379

# MCP Server Configuration
MCP_PORT=8003
MCP_HOST=hx-n8n-mcp-server.hx.dev.local

# SSL/TLS Certificates
SSL_CERT_PATH=/etc/ssl/certs/hx-n8n-mcp-server.crt
SSL_KEY_PATH=/etc/ssl/private/hx-n8n-mcp-server.key
```

---

### 4.3 Variable Precedence

**Ansible variable precedence** (highest to lowest priority):
1. Command-line extra vars (`-e var=value`)
2. Task vars
3. Block vars
4. Role vars
5. Play vars
6. Vars files (our `vault/secrets.yml`)
7. Defaults

**Best practice**: Use vault files for secrets (priority 6) and override with command-line only when necessary.

---

## 5. Environment File Patterns

### 5.1 .env File Structure

**.env files remain the primary configuration method** for applications. Ansible simply generates them from vault variables.

**Standard .env file pattern**:
```bash
# /opt/n8n-mcp/.env
# Generated by Ansible - DO NOT EDIT MANUALLY
# Modify vault/secrets.yml and re-run playbook

# Section: Database Configuration
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=hx-postgres-server.hx.dev.local
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n_mcp
DB_POSTGRESDB_USER=svc-n8n
DB_POSTGRESDB_PASSWORD=Major8859

# Section: Redis Configuration
REDIS_HOST=hx-redis-server.hx.dev.local
REDIS_PORT=6379

# Section: MCP Server Configuration
MCP_PORT=8003
MCP_HOST=hx-n8n-mcp-server.hx.dev.local
MCP_PROTOCOL=http

# Section: SSL/TLS Configuration
SSL_ENABLED=true
SSL_CERT_PATH=/etc/ssl/certs/hx-n8n-mcp-server.crt
SSL_KEY_PATH=/etc/ssl/private/hx-n8n-mcp-server.key

# Section: Logging
LOG_LEVEL=info
LOG_FILE=/var/log/n8n-mcp/server.log
```

---

### 5.2 .env File Permissions

**CRITICAL**: .env files contain plaintext secrets and **MUST** be protected.

**Standard permissions**:
```bash
# Owner: service account (n8n)
# Group: service account (n8n)
# Mode: 600 (read/write owner only)

chown n8n:n8n /opt/n8n-mcp/.env
chmod 600 /opt/n8n-mcp/.env
```

**Verification**:
```bash
ls -la /opt/n8n-mcp/.env
# Should show: -rw------- 1 n8n n8n 512 Nov 10 10:00 .env
```

---

### 5.3 .env File Loading

**Systemd service loads .env automatically**:
```ini
# /etc/systemd/system/n8n-mcp.service
[Unit]
Description=n8n MCP Server
After=network.target postgresql.service

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n-mcp
EnvironmentFile=/opt/n8n-mcp/.env
ExecStart=/opt/n8n-mcp/bin/server
Restart=always

[Install]
WantedBy=multi-user.target
```

**Note**: `EnvironmentFile` directive loads all variables into service environment.

---

## 6. n8n MCP Server Specific Patterns

### 6.1 Required Secrets

**For n8n MCP Server deployment**, the following secrets are required:

| Secret | Variable Name | Value Pattern | Purpose |
|--------|---------------|---------------|---------|
| n8n service password | `n8n_service_password` | `Major8859!` | Domain service account |
| Database user | `postgres_user` | `svc-n8n` | PostgreSQL role |
| Database password | `postgres_password` | `Major8859` | PostgreSQL authentication |
| Database name | `postgres_database` | `n8n_mcp` | Database to use |
| MCP server port | `mcp_server_port` | `8003` | Port for MCP protocol |
| SSL certificate path | `ssl_cert_path` | `/etc/ssl/certs/...` | TLS certificate |
| SSL key path | `ssl_key_path` | `/etc/ssl/private/...` | TLS private key |

---

### 6.2 Vault File for n8n MCP Server

**Create vault file**: `/srv/ansible/n8n-mcp/vault/secrets.yml`

```yaml
---
# n8n MCP Server Secrets
# Created: 2025-11-10
# Encrypt with: ansible-vault encrypt secrets.yml
# Vault password: Major8859!

# Service Account (Domain)
n8n_service_user: "n8n@hx.dev.local"
n8n_service_password: "Major8859!"

# Database Configuration
postgres_host: "hx-postgres-server.hx.dev.local"
postgres_port: 5432
postgres_database: "n8n_mcp"
postgres_user: "svc-n8n"
postgres_password: "Major8859"

# Redis Configuration (DEV mode - no auth)
redis_host: "hx-redis-server.hx.dev.local"
redis_port: 6379
redis_password: ""  # Empty for DEV mode

# n8n Workflow Engine Connection
n8n_workflow_host: "hx-n8n-server.hx.dev.local"
n8n_workflow_port: 5678
n8n_workflow_protocol: "http"

# MCP Server Configuration
mcp_server_host: "hx-n8n-mcp-server.hx.dev.local"
mcp_server_port: 8003
mcp_server_protocol: "http"

# FastMCP Gateway
fastmcp_host: "hx-fastmcp-server.hx.dev.local"
fastmcp_port: 8000

# SSL/TLS Certificates
ssl_cert_path: "/etc/ssl/certs/hx-n8n-mcp-server.crt"
ssl_key_path: "/etc/ssl/private/hx-n8n-mcp-server.key"
ssl_ca_cert_path: "/etc/ssl/certs/ca-certificates.crt"

# Domain Authentication
domain_name: "hx.dev.local"
domain_controller: "hx-dc-server.hx.dev.local"
domain_admin_user: "Administrator"
domain_admin_password: "Major3059!"

# Server Configuration
server_hostname: "hx-n8n-mcp-server"
server_fqdn: "hx-n8n-mcp-server.hx.dev.local"
server_ip: "192.168.10.214"

# Installation Paths
install_base: "/opt/n8n-mcp"
config_path: "/opt/n8n-mcp/config"
data_path: "/opt/n8n-mcp/data"
log_path: "/var/log/n8n-mcp"
```

**After creating**:
```bash
# Encrypt the vault file
cd /srv/ansible/n8n-mcp
ansible-vault encrypt vault/secrets.yml
# Uses password from ~/.ansible/vault_password (Major8859!)

# Verify encryption
cat vault/secrets.yml
# Should show: $ANSIBLE_VAULT;1.1;AES256...

# View contents
ansible-vault view vault/secrets.yml
# Shows decrypted content
```

---

### 6.3 Playbook Structure

**Deployment playbook**: `/srv/ansible/n8n-mcp/deploy.yml`
```yaml
---
- name: Deploy n8n MCP Server
  hosts: hx-n8n-mcp-server
  become: yes
  vars_files:
    - vault/secrets.yml  # Load encrypted secrets
  
  tasks:
    - name: Include Layer 1 (William - Ubuntu prep)
      include_tasks: tasks/layer1-ubuntu.yml
    
    - name: Include Layer 1 (Frank - Domain join)
      include_tasks: tasks/layer1-domain.yml
    
    - name: Include MCP Server installation
      include_tasks: tasks/mcp-server-install.yml
    
    - name: Generate .env file from vault
      template:
        src: templates/env.j2
        dest: "{{ install_base }}/.env"
        mode: '0600'
        owner: n8n
        group: n8n
    
    - name: Configure systemd service
      template:
        src: templates/n8n-mcp.service.j2
        dest: /etc/systemd/system/n8n-mcp.service
        mode: '0644'
      notify: reload systemd
  
  handlers:
    - name: reload systemd
      systemd:
        daemon_reload: yes
```

---

## 7. Team Workflow

### 7.1 For William (Ubuntu Server Prep)

**What you need**:
- Local admin password: `Major8859!`
- Domain to join: `hx.dev.local`

**No vault access needed** - standard Ubuntu prep doesn't require secrets.

**Actions**:
1. Provision Ubuntu server
2. Configure network (IP: 192.168.10.214)
3. Prepare for domain join
4. Hand off to Frank

---

### 7.2 For Frank (Samba DC & Certificates)

**What you need**:
- Domain admin password: `Major3059!`
- Service account password: `Major8859!`
- CA passphrase: (existing, not changed)

**Vault variables you'll use**:
- `n8n_service_user`: "n8n@hx.dev.local"
- `n8n_service_password`: "Major8859!"
- `domain_name`: "hx.dev.local"
- `server_fqdn`: "hx-n8n-mcp-server.hx.dev.local"
- `server_ip`: "192.168.10.214"

**Ansible task example**:
```yaml
- name: Create n8n service account in Samba DC
  shell: |
    samba-tool user create {{ n8n_service_user | regex_replace('@.*', '') }} '{{ n8n_service_password }}' \
      --description='n8n MCP Server Service Account' \
      --home-directory=/home/{{ n8n_service_user }} \
      --login-shell=/bin/bash \
      --use-username-as-cn
  delegate_to: hx-dc-server.hx.dev.local
```

**Actions**:
1. Create computer account: `hx-n8n-mcp-server`
2. Create service account: `n8n@hx.dev.local` with password `Major8859!`
3. Configure DNS A record: `hx-n8n-mcp-server.hx.dev.local → 192.168.10.214`
4. Issue SSL certificate
5. Hand off to Olivia

---

### 7.3 For Olivia (n8n MCP Specialist)

**What you need**:
- **Full vault access** - you'll work with secrets most frequently
- Database credentials
- MCP server configuration
- SSL certificates

**Vault variables you'll use**:
- `postgres_*`: Database connection details
- `redis_*`: Redis connection details
- `mcp_server_*`: MCP server configuration
- `n8n_workflow_*`: n8n workflow engine connection
- `ssl_*`: Certificate paths

**Workflow**:

1. **View vault secrets**:
```bash
cd /srv/ansible/n8n-mcp
ansible-vault view vault/secrets.yml
```

2. **Edit vault (if needed)**:
```bash
ansible-vault edit vault/secrets.yml
# Make changes, save, automatically re-encrypted
```

3. **Deploy with vault**:
```bash
ansible-playbook deploy.yml
# Automatically decrypts vault using ~/.ansible/vault_password
```

4. **Verify .env generated correctly**:
```bash
ssh n8n@hx-n8n-mcp-server.hx.dev.local
cat /opt/n8n-mcp/.env
# Should show configuration with values from vault
```

---

### 7.4 For Omar (Workflow Developer)

**What you need**:
- Access to n8n workflow engine (existing at 192.168.10.215)
- MCP tool metadata requirements

**No direct vault access needed** - Omar works on n8n workflows, not infrastructure secrets.

**If credentials needed for workflows**:
- Use n8n's built-in credential store (not Ansible Vault)
- n8n encrypts workflow credentials separately

---

### 7.5 For George (FastMCP Integration)

**What you need**:
- FastMCP server endpoint: `hx-fastmcp-server.hx.dev.local:8000`
- n8n MCP server endpoint: `hx-n8n-mcp-server.hx.dev.local:8003`

**Vault variables you'll use**:
- `fastmcp_host`: "hx-fastmcp-server.hx.dev.local"
- `fastmcp_port`: 8000
- `mcp_server_host`: "hx-n8n-mcp-server.hx.dev.local"
- `mcp_server_port`: 8003

**Workflow**:
1. Register n8n MCP server with FastMCP
2. Configure routing
3. Test dual-path integration

---

### 7.6 For Amanda (Ansible Automation)

**What you need**:
- **Full vault access** - you'll automate deployment with secrets
- Understanding of all vault variables
- Ansible Vault password: `Major8859!`

**Workflow**:

1. **Create/edit vault files**:
```bash
# Create new vault
ansible-vault create vault/secrets.yml

# Edit existing vault
ansible-vault edit vault/secrets.yml

# Encrypt existing file
ansible-vault encrypt secrets.yml
```

2. **Use vault in playbooks**:
```yaml
---
- name: My Playbook
  hosts: all
  vars_files:
    - vault/secrets.yml
  tasks:
    - name: Use vault variable
      debug:
        msg: "Database is {{ postgres_host }}"
```

3. **Create reusable playbook**:
```bash
# Playbook automatically uses vault password file
ansible-playbook deploy.yml

# Or specify vault password file explicitly
ansible-playbook deploy.yml --vault-password-file ~/.ansible/vault_password
```

---

### 7.7 For Agent Zero (Orchestrator)

**What you need**:
- **Awareness of all secrets** (but delegating actual work to specialists)
- Vault password: `Major8859!`
- Understanding of when vault is/isn't needed

**Workflow**:

1. **Validate vault setup** (Phase 2):
```bash
# Ensure vault password file exists on hx-control-node
ssh agent0@hx-control-node.hx.dev.local
cat ~/.ansible/vault_password
# Should output: Major8859!

# Ensure vault file exists
ls -la /srv/ansible/n8n-mcp/vault/secrets.yml
# Should show: -rw------- (encrypted)

# Test vault access
ansible-vault view /srv/ansible/n8n-mcp/vault/secrets.yml
# Should decrypt and show contents
```

2. **Coordinate team**:
- William: No vault needed (Layer 1 Ubuntu)
- Frank: Vault variables for service account creation
- Olivia: Full vault access (MCP server deployment)
- George: Vault variables for FastMCP integration
- Amanda: Full vault access (automation)

3. **Validate deployments**:
```bash
# After deployment, verify .env generated correctly
ssh n8n@hx-n8n-mcp-server.hx.dev.local
ls -la /opt/n8n-mcp/.env
# Should show: -rw------- 1 n8n n8n (correct permissions)

cat /opt/n8n-mcp/.env
# Verify values match vault (without special chars in DB password)
```

---

## 8. Security Considerations

### 8.1 Development Environment Context

**This is a DEVELOPMENT environment (hx.dev.local)**:
- ✅ Acceptable to use standard passwords (`Major8859`, `Major8859!`)
- ✅ Acceptable to use single vault password (`Major8859!`)
- ✅ Acceptable to store vault password in plaintext file (`~/.ansible/vault_password`)
- ✅ Internal network only (192.168.10.0/24)
- ✅ Not exposed to internet

**Production would require**:
- ❌ Unique, complex passwords per service
- ❌ Separate vault passwords per project
- ❌ Vault password from secure secret store (not plaintext file)
- ❌ MFA for vault access
- ❌ Audit logging of vault access

---

### 8.2 Vault File Protection

**Vault files are encrypted BUT**:
- ⚠️ Vault password file (`~/.ansible/vault_password`) is plaintext
- ⚠️ Anyone with access to hx-control-node can decrypt vaults
- ⚠️ .env files generated on target servers are plaintext

**Mitigations**:
- ✅ Restrict access to hx-control-node (SSH key auth only)
- ✅ Limit sudo access (agent0 only)
- ✅ .env files have 600 permissions (owner read/write only)
- ✅ Regular credential rotation (quarterly in dev)

---

### 8.3 .env File Security

**.env files contain plaintext secrets**:
- **NEVER** commit .env files to Git
- **ALWAYS** set permissions to 600 (owner read/write only)
- **ALWAYS** set owner to service account (not root)
- **ALWAYS** generate .env from Ansible templates (don't create manually)

**Ansible ensures correct permissions**:
```yaml
- name: Generate .env file
  template:
    src: templates/env.j2
    dest: /opt/n8n-mcp/.env
    mode: '0600'        # Owner read/write only
    owner: n8n          # Service account owns file
    group: n8n          # Service account group
```

---

### 8.4 Git Repository Safety

**What CAN be committed to Git**:
- ✅ Ansible playbooks (contain no secrets)
- ✅ Ansible templates (.j2 files with variables, not values)
- ✅ Encrypted vault files (vault/secrets.yml after `ansible-vault encrypt`)
- ✅ Documentation (this file)

**What CANNOT be committed to Git**:
- ❌ Vault password file (`~/.ansible/vault_password`)
- ❌ Unencrypted vault files (secrets.yml before encryption)
- ❌ .env files (plaintext secrets)
- ❌ Private keys, certificates (SSL/TLS)

**.gitignore for n8n MCP project**:
```gitignore
# Ansible Vault password
.ansible/vault_password
vault_password
*.vault_pass

# Environment files
.env
.env.*
*.env

# Private keys
*.key
*.pem
private/

# Unencrypted secrets (backup files)
secrets.yml.bak
*unencrypted*
```

---

### 8.5 Credential Rotation Schedule

**Development Environment**:
- Service accounts: Quarterly (every 3 months)
- User accounts: On-demand (when needed)
- API keys: Annually
- SSL certificates: Before expiration (auto-renewed)
- Vault password: Annually

**Production Environment (if deployed)**:
- Service accounts: Monthly
- User accounts: 90 days (enforced)
- API keys: Quarterly
- SSL certificates: Auto-renewed (60 days before expiration)
- Vault password: Quarterly

---

## 9. Quick Reference

### 9.1 Password Cheat Sheet

| Account Type | Password | Use Case |
|--------------|----------|----------|
| **Service/System** | `Major8859` | Database accounts, service accounts, connection URLs |
| **User/Domain** | `Major8859!` | SSH logins, domain accounts, interactive users |
| **Ansible Vault** | `Major8859!` | Encrypting/decrypting vault files |

---

### 9.2 Common Commands

```bash
# View vault
ansible-vault view vault/secrets.yml

# Edit vault
ansible-vault edit vault/secrets.yml

# Encrypt file
ansible-vault encrypt secrets.yml

# Decrypt file (temporarily)
ansible-vault decrypt secrets.yml

# Run playbook (uses vault automatically)
ansible-playbook deploy.yml

# Generate .env from vault
ansible-playbook deploy.yml --tags generate-env
```

---

### 9.3 File Locations

| File | Location | Purpose |
|------|----------|---------|
| **Vault password** | `~/.ansible/vault_password` | Ansible Vault master password |
| **Vault file** | `/srv/ansible/n8n-mcp/vault/secrets.yml` | Encrypted secrets |
| **Deploy playbook** | `/srv/ansible/n8n-mcp/deploy.yml` | Main deployment |
| **.env template** | `/srv/ansible/n8n-mcp/templates/env.j2` | Template for .env |
| **Generated .env** | `/opt/n8n-mcp/.env` | Runtime configuration |

---

### 9.4 Troubleshooting

**Problem**: "Vault password file not found"
```bash
# Solution: Create password file
mkdir -p ~/.ansible
echo 'Major8859!' > ~/.ansible/vault_password
chmod 600 ~/.ansible/vault_password
```

**Problem**: "Decryption failed"
```bash
# Solution: Check vault password is correct
cat ~/.ansible/vault_password
# Should output: Major8859!

# Try manual decrypt
ansible-vault view vault/secrets.yml
# Enter password when prompted: Major8859!
```

**Problem**: ".env file has wrong permissions"
```bash
# Solution: Fix permissions
sudo chown n8n:n8n /opt/n8n-mcp/.env
sudo chmod 600 /opt/n8n-mcp/.env
```

**Problem**: "Variable not found in vault"
```bash
# Solution: Check vault contents
ansible-vault view vault/secrets.yml | grep <variable_name>

# If missing, add to vault
ansible-vault edit vault/secrets.yml
# Add: <variable_name>: "<value>"
# Save and exit
```

---

## 10. Summary

### Key Takeaways

1. **Two standard passwords**:
   - Service/system accounts: `Major8859` (no special chars)
   - User/domain accounts: `Major8859!` (with exclamation)

2. **Ansible Vault introduced**:
   - Master password: `Major8859!`
   - Encrypts all secrets at rest
   - Safe to commit encrypted files to Git

3. **Variables used in playbooks**:
   - Vault file: `/srv/ansible/n8n-mcp/vault/secrets.yml`
   - Templates: `.j2` files with `{{ variable_name }}`
   - Generated: `.env` files on target servers

4. **.env files continue**:
   - Generated by Ansible from vault
   - Permissions: 600 (owner read/write only)
   - Owner: service account (n8n)

5. **Existing credentials unchanged**:
   - All current accounts keep their passwords
   - All current API keys unchanged
   - No disruption to deployed services

---

## Document Metadata

**Version**: 1.0  
**Created**: November 10, 2025  
**Last Updated**: November 10, 2025  
**Project**: n8n MCP Server Installation & Configuration (HX-N8N-MCP-001)  

**Related Documents**:
- Project Charter: `/mnt/user-data/outputs/n8n-mcp-server-project-charter.md`
- Architecture Document: `/mnt/user-data/outputs/n8n-mcp-server-architecture.md`
- Roles and Responsibilities: `/mnt/user-data/outputs/n8n-mcp-server-roles-responsibilities.md`
- Knowledge Document: `/mnt/user-data/outputs/n8n-mcp-server-knowledge-document.md`

**Maintained By**: Agent Zero (Claude Code) + Amanda Chen (Ansible Specialist)  
**Classification**: Internal - Project Standards  
**Status**: ACTIVE - Required Reading  

---

## Approval

| Role | Name | Status | Date |
|------|------|--------|------|
| **CAIO** | Jarvis Richardson | Pending Review | _______ |
| **Agent Zero** | Claude Code | Active Use | 2025-11-10 |
| **Ansible Specialist** | Amanda Chen | Active Use | _______ |

---

*This credentials and secrets management standards document establishes clear, simple patterns for the n8n MCP Server project while introducing Ansible Vault for improved security. All existing credentials remain unchanged.*
