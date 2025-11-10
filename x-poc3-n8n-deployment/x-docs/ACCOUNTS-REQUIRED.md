# N8N POC3 Deployment - Comprehensive Accounts Documentation

**Document Type**: Technical Reference - Account Inventory
**Created**: 2025-11-08
**Author**: Omar Rodriguez (N8N Workflow Worker Specialist)
**Project**: POC3 N8N Workflow Automation Platform Deployment
**Purpose**: Comprehensive documentation of all system, service, and database accounts used in n8n deployment
**Status**: Active Reference

---

## Executive Summary

This document provides a complete inventory of all accounts (system users, database roles, and service accounts) involved in the n8n POC3 deployment. It documents **what exists**, **what was attempted**, **what failed**, and **what is recommended** for proper configuration.

### Key Findings

1. ✅ **n8n system user** - Successfully created on hx-n8n-server
2. ✅ **PostgreSQL database roles** - All three roles exist (postgres, svc-postgres, n8n_user)
3. ⚠️ **Account confusion** - Multiple account attempts led to configuration issues
4. ❌ **Failed attempts** - Some accounts attempted but failed or were incorrect
5. ✅ **Current configuration** - Using n8n_user for database connections (as of deployment)

---

## Table of Contents

1. [System Accounts (OS Level)](#1-system-accounts-os-level)
2. [Database Roles (PostgreSQL)](#2-database-roles-postgresql)
3. [Domain Service Accounts (LDAP/Samba)](#3-domain-service-accounts-ldapsamba)
4. [Failed Account Attempts](#4-failed-account-attempts)
5. [Current Configuration](#5-current-configuration)
6. [Recommended Accounts](#6-recommended-accounts)
7. [Cleanup Recommendations](#7-cleanup-recommendations)
8. [Account Usage Matrix](#8-account-usage-matrix)

---

## 1. System Accounts (OS Level)

### 1.1 n8n System User (hx-n8n-server.hx.dev.local)

**Status**: ✅ **EXISTS AND WORKING**

| Property | Value |
|----------|-------|
| **Account Name** | `n8n` |
| **UID** | 999 |
| **GID** | 988 |
| **Home Directory** | `/home/n8n` |
| **Shell** | `/bin/false` (no login) |
| **Type** | Local system user (non-login) |
| **Created By** | William Taylor (agent-william) |
| **Creation Method** | `useradd -r -m -s /usr/sbin/nologin -d /opt/n8n -U n8n` |
| **Purpose** | Run n8n service process |
| **Server** | hx-n8n-server.hx.dev.local (192.168.10.215) |

**Ownership**:
- `/opt/n8n/` - n8n application directory
- `/opt/n8n/app/` - compiled application code
- `/opt/n8n/.env` - environment configuration (chmod 600)
- `/opt/n8n/logs/` - application logs
- `/opt/n8n/start-n8n.sh` - startup script

**Verification**:
```bash
# On hx-n8n-server
id n8n
# Output: uid=999(n8n) gid=988(n8n) groups=988(n8n)

getent passwd n8n
# Output: n8n:x:999:988::/home/n8n:/bin/false

ls -ld /opt/n8n
# Output: drwxr-xr-x 5 n8n n8n 4096 Nov 8 18:10 /opt/n8n
```

**Systemd Service**:
```ini
[Service]
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n
```

**Notes**:
- ✅ Correctly created as system user (UID < 1000)
- ✅ No login shell (security best practice)
- ✅ Proper file ownership on /opt/n8n
- ⚠️ Home directory is `/home/n8n` but should be `/opt/n8n` per task specification
  - **Deviation**: Task T-011 specified `-d /opt/n8n` but actual home is `/home/n8n`
  - **Impact**: Minimal - service still works, but inconsistent with plan

---

### 1.2 agent0 Administrative User (All Servers)

**Status**: ✅ **EXISTS (Standard Infrastructure Account)**

| Property | Value |
|----------|-------|
| **Account Name** | `agent0` |
| **UID** | 1000 |
| **GID** | 1000 |
| **Home Directory** | `/home/agent0` |
| **Shell** | `/bin/bash` |
| **Type** | Local administrator account |
| **Password** | `Major8859!` (per credentials document) |
| **Purpose** | Administrative access to all servers |
| **Servers** | All infrastructure servers |

**Permissions**:
- Member of `sudo` group
- Full sudo access (`/etc/sudoers.d/`)
- SSH access enabled

**Usage**:
- Used for server administration
- Used for service deployment
- Used for troubleshooting

**Notes**:
- Standard account across all Hana-X infrastructure
- Not specific to n8n deployment
- Referenced in Phase 2 execution status document

---

### 1.3 www-data Web Server User (hx-n8n-server)

**Status**: ✅ **EXISTS (Default System Account)**

| Property | Value |
|----------|-------|
| **Account Name** | `www-data` |
| **UID** | 33 |
| **GID** | 33 |
| **Home Directory** | `/var/www` |
| **Shell** | `/usr/sbin/nologin` |
| **Type** | System user (Nginx) |
| **Purpose** | Nginx web server process owner |
| **Server** | hx-n8n-server.hx.dev.local (192.168.10.215) |

**Ownership**:
- Nginx worker processes
- `/var/www/` (web root, not used for n8n)
- Nginx log files (via systemd)

**Notes**:
- Default Ubuntu/Debian account for web servers
- Not directly used by n8n (Nginx runs as www-data, proxies to n8n)
- No configuration changes needed

---

### 1.4 root Superuser (All Servers)

**Status**: ✅ **EXISTS (Default System Account)**

| Property | Value |
|----------|-------|
| **Account Name** | `root` |
| **UID** | 0 |
| **Type** | System superuser |
| **Purpose** | System administration |
| **Servers** | All infrastructure servers |

**Usage**:
- Used via `sudo` from agent0 account
- SSL certificate management (`/opt/n8n/ssl/`)
- Systemd service management
- Direct login disabled (security policy)

---

## 2. Database Roles (PostgreSQL)

All database roles exist on **hx-postgres-server.hx.dev.local** (192.168.10.209).

### 2.1 postgres Database Superuser

**Status**: ✅ **EXISTS (Default PostgreSQL Superuser)**

| Property | Value |
|----------|-------|
| **Role Name** | `postgres` |
| **Type** | PostgreSQL superuser (default) |
| **SUPERUSER** | Yes (t) |
| **LOGIN** | Yes (t) |
| **Password** | `Major8859!` (per credentials document) |
| **Purpose** | PostgreSQL administrative tasks |
| **Owner** | Default PostgreSQL installation |

**Privileges**:
- Full superuser privileges
- Can create databases, roles, extensions
- Can modify all database objects
- Can access all databases

**Usage**:
- Reserved for administrative tasks only
- Database maintenance and upgrades
- Schema migrations
- NOT recommended for application connections

**Verification**:
```bash
# On hx-postgres-server
sudo -u postgres /usr/local/pgsql/bin/psql -c "\du postgres"
# Output: postgres | Superuser, Create role, Create DB | {}
```

**Notes**:
- Standard PostgreSQL administrative account
- Exists by default in all PostgreSQL installations
- Should NOT be used by n8n application (use svc-postgres or n8n_user instead)

---

### 2.2 svc-postgres Application Service Account ⭐ RECOMMENDED

**Status**: ✅ **EXISTS AND VERIFIED**

| Property | Value |
|----------|-------|
| **Role Name** | `svc-postgres` |
| **Type** | PostgreSQL superuser (application service account) |
| **SUPERUSER** | Yes (t) |
| **LOGIN** | Yes (t) |
| **Password** | `Major8859!` (verified working 2025-11-08) |
| **Created** | October 27, 2025 |
| **Purpose** | **RECOMMENDED** application database connections |
| **Database** | n8n_poc3 (and all other databases) |

**Privileges**:
- Full superuser privileges (same as postgres)
- Can connect to n8n_poc3 database
- Can create tables, indexes, sequences
- Full CRUD operations on all schemas

**Connection Test** ✅:
```bash
# From hx-n8n-server (192.168.10.215)
PGPASSWORD='Major8859!' psql -h 192.168.10.209 -U svc-postgres -d n8n_poc3 -c "SELECT current_user;"
# Output: current_user = svc-postgres
# Result: ✅ SUCCESS (verified 2025-11-08 by Quinn Davis)
```

**Verification** (from QUINN-DATABASE-RESOLUTION.md):
```
✅ Role svc-postgres exists (SUPERUSER, LOGIN)
✅ Password 'Major8859!' verified working
✅ Remote connections from N8N server work via psql
✅ Authentication method: scram-sha-256
```

**Recommended Connection String**:
```bash
# Environment variables (recommended)
DB_TYPE=postgresdb
DB_POSTGRESDB_HOST=192.168.10.209
DB_POSTGRESDB_PORT=5432
DB_POSTGRESDB_DATABASE=n8n_poc3
DB_POSTGRESDB_USER=svc-postgres
DB_POSTGRESDB_PASSWORD=Major8859!

# Connection URL (alternative)
DATABASE_URL=postgresql://svc-postgres:Major8859!@192.168.10.209:5432/n8n_poc3
```

**Documentation References**:
- Credentials: `/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.1-credentials.md` (Section 6)
- Escalation: `/srv/cc/Governance/x-poc3-n8n-deployment/ESCALATION-QUINN-N8N-DATABASE-AUTH.md`
- Resolution: `/srv/cc/Governance/x-poc3-n8n-deployment/QUINN-DATABASE-RESOLUTION.md`

**Why Recommended** ⭐:
- Per credentials document: "**RECOMMENDED FOR ALL APPLICATIONS**"
- Dedicated application service account (not mixed with admin tasks)
- Same privileges as postgres superuser
- Already verified working from n8n server
- Used by other applications (LiteLLM, FastMCP)

**Notes**:
- Created via `samba-tool` on Domain Controller (hx-dc-server)
- Domain-integrated account (available on all domain-joined servers)
- Password verified reset and working as of 2025-11-08 (Quinn Davis)
- Superuser privileges allow n8n to run migrations automatically

---

### 2.3 n8n_user Database Role (Currently in Use)

**Status**: ✅ **EXISTS AND WORKING**

| Property | Value |
|----------|-------|
| **Role Name** | `n8n_user` |
| **Type** | PostgreSQL role (non-superuser) |
| **SUPERUSER** | No (f) |
| **LOGIN** | Yes (t) |
| **Password** | `Major8859!` (verified working 2025-11-08) |
| **Created** | During Phase 1 (Quinn Davis, Task T-018) |
| **Purpose** | N8N application database access |
| **Database** | n8n_poc3 |

**Privileges**:
- CONNECT privilege on n8n_poc3 database
- CREATE privilege on public schema
- SELECT, INSERT, UPDATE, DELETE on all tables in public schema
- USAGE on sequences
- Default privileges configured for future tables

**Connection Test** ✅:
```bash
# From hx-n8n-server (192.168.10.215)
PGPASSWORD='Major8859!' psql -h 192.168.10.209 -U n8n_user -d n8n_poc3 -c "SELECT current_user;"
# Output: current_user = n8n_user
# Result: ✅ SUCCESS (verified 2025-11-08 by Quinn Davis)
```

**Verification** (from QUINN-DATABASE-RESOLUTION.md):
```
✅ Role n8n_user exists (LOGIN)
✅ Password 'Major8859!' verified working
✅ Remote connections from N8N server work via psql
```

**Current Configuration** (as deployed):
```bash
# From /opt/n8n/.env on hx-n8n-server
DB_POSTGRESDB_URL=postgresql://n8n_user:Major8859!@192.168.10.209:5432/n8n_poc3
```

**Creation Command** (from Task T-018):
```sql
-- On hx-postgres-server
CREATE USER n8n_user WITH ENCRYPTED PASSWORD 'Major8859!';
GRANT CREATE, CONNECT ON DATABASE n8n_poc3 TO n8n_user;
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO n8n_user;
GRANT USAGE, CREATE ON SCHEMA public TO n8n_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO n8n_user;
```

**pg_hba.conf Entry**:
```
host    all    all    192.168.10.0/24    scram-sha-256
```

**Notes**:
- ✅ Currently configured in `/opt/n8n/.env`
- ✅ Password verified working (manual psql test successful)
- ⚠️ Non-superuser role (may require schema updates for migrations)
- ⚠️ Less privileged than svc-postgres (principle of least privilege)
- ⚠️ N8N service failing despite correct credentials (application config issue, NOT database issue per Quinn's investigation)

**Known Issue**:
- Database authentication works perfectly via psql
- N8N service fails to authenticate (environment variable loading issue)
- Root cause: N8N not reading .env file correctly or password escaping issue
- Documented in: `ESCALATION-QUINN-N8N-DATABASE-AUTH.md` and `QUINN-DATABASE-RESOLUTION.md`

---

## 3. Domain Service Accounts (LDAP/Samba)

### 3.1 n8n@hx.dev.local Domain Service Account

**Status**: ✅ **EXISTS (Domain-Integrated)**

| Property | Value |
|----------|-------|
| **Account Name** | `n8n@hx.dev.local` |
| **Type** | Domain service account (Samba LDAP/DC) |
| **UID** | 1114201137 (Samba DC auto-assigned) |
| **GID** | 1114200513 (Domain Users) |
| **Home Directory** | `/home/n8n@hx.dev.local` |
| **Shell** | `/bin/bash` |
| **Password** | `Major8859!` (per credentials document) |
| **Created** | Via `samba-tool` on hx-dc-server |
| **Purpose** | Domain-integrated n8n service account |
| **Server** | Available on ALL domain-joined servers |

**Creation Method**:
```bash
# On hx-dc-server.hx.dev.local
samba-tool user create n8n 'Major8859!' \
  --description='n8n Workflow Automation Service Account - Samba LDAP/DC' \
  --home-directory=/home/n8n@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn
```

**Usage**:
- Domain authentication via Kerberos + SSSD
- Available for SSH access to domain-joined servers
- NOT currently used by n8n service (local n8n user used instead)
- Created for future LDAP integration

**Documentation**:
- Credentials document Section 14: "n8n Service Account (Domain-Integrated)"
- `/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.1-credentials.md`

**Notes**:
- ⚠️ **NOT the same as local n8n system user**
  - Local user: `n8n` (UID 999, local system account)
  - Domain user: `n8n@hx.dev.local` (UID 1114201137, domain account)
- Domain account NOT currently used by systemd service
- Local system user (`n8n` UID 999) is used for service execution
- Domain account available for future LDAP authentication feature

---

### 3.2 svc-postgres@hx.dev.local Domain Service Account

**Status**: ✅ **EXISTS (Domain-Integrated)**

| Property | Value |
|----------|-------|
| **Account Name** | `svc-postgres@hx.dev.local` |
| **Type** | Domain service account (Samba LDAP/DC) |
| **UID** | 1114201133 (Samba DC auto-assigned) |
| **GID** | 1114200513 (Domain Users) |
| **Home Directory** | `/home/svc-postgres@hx.dev.local` |
| **Shell** | `/bin/bash` |
| **Password** | `Major8859!` |
| **Database Role Password** | `Major8859!` (SAME - standard password) |
| **Created** | October 27, 2025 |
| **Purpose** | Domain-integrated PostgreSQL service account |
| **Server** | Available on ALL domain-joined servers |

**Notes**:
- This is the **OS account** for svc-postgres
- Corresponding **database role** exists in PostgreSQL (Section 2.2)
- Database role password: `Major8859!` (same as OS account)
- **RECOMMENDED** for all application database connections

---

## 4. Failed Account Attempts

### 4.1 Attempted: agent0 as n8n Service User

**Status**: ❌ **INCORRECT ATTEMPT - ABANDONED**

| Property | Value |
|----------|-------|
| **Account Name** | `agent0` (existing admin account) |
| **Attempted Use** | Run n8n service as agent0 |
| **Why Attempted** | Confusion during deployment, agent0 used for testing |
| **Why Failed** | Security policy violation (admin account should not run services) |
| **Documented In** | Phase 2 execution logs, deployment attempts |

**Evidence**:
```bash
# Found in deployment logs and execution status
Server: agent0@192.168.10.215 (hx-n8n-server)
```

**Why This Was Wrong**:
- ❌ agent0 is an administrative account (UID 1000, full sudo access)
- ❌ Services should run as dedicated system users (principle of least privilege)
- ❌ Violates security best practices (separation of concerns)
- ❌ File ownership would be incorrect for production

**Resolution**:
- Created dedicated `n8n` system user (UID 999)
- Changed all file ownership from `agent0:agent0` to `n8n:n8n`
- Updated systemd service to run as `n8n` user

**Files Affected** (had to change ownership):
- `/opt/n8n/` - changed from agent0 to n8n
- `/opt/n8n/app/` - changed from agent0 to n8n
- `/opt/n8n/.env` - changed from agent0 to n8n

---

### 4.2 Attempted: Multiple Database User Changes

**Status**: ⚠️ **CONFUSION DURING DEPLOYMENT**

| Attempt | User | Status | Notes |
|---------|------|--------|-------|
| **Original Plan** | `n8n_user` | ✅ Created, works | Task T-018, created by Quinn |
| **Mid-Deployment** | `svc-postgres` | ✅ Attempted, works | Credentials doc recommends this |
| **Current Config** | `n8n_user` | ✅ In use | `/opt/n8n/.env` uses n8n_user |

**Timeline of Attempts**:

1. **Phase 1 (Task T-018)**: Created `n8n_user` per specification
   - Result: ✅ User created, privileges granted

2. **Mid-Deployment**: Attempted to switch to `svc-postgres`
   - Reason: Credentials document recommends svc-postgres for all apps
   - Updated `/opt/n8n/.env` to use svc-postgres
   - Result: ⚠️ Configuration changed but service still failed

3. **Current State**: Reverted to `n8n_user`
   - Current `.env`: `DB_POSTGRESDB_URL=postgresql://n8n_user:Major8859!@192.168.10.209:5432/n8n_poc3`
   - Result: ⚠️ Still failing (application config issue, not database)

**Evidence from ESCALATION-QUINN-N8N-DATABASE-AUTH.md**:
```
From Credentials Document:
  Username: svc-postgres@hx.dev.local
  Password: Major8859!
  Purpose: Application database connections (recommended for all apps)

From QUINN-DATABASE-RESOLUTION.md:
  Files Modified During Investigation:
  1. /opt/n8n/.env - Updated DB_POSTGRESDB_USER from n8n_user to svc-postgres
```

**Why This Caused Confusion**:
- Task T-018 specified creating `n8n_user` (per phase 1 plan)
- Credentials document recommends using `svc-postgres` (per infrastructure standard)
- Multiple attempts to switch between accounts during troubleshooting
- Both accounts work perfectly via psql (verified by Quinn)
- Service failure unrelated to account choice (env loading issue)

**Resolution**:
- Both `n8n_user` and `svc-postgres` are valid, working accounts
- Current deployment uses `n8n_user` (as planned)
- Can switch to `svc-postgres` if desired (just update .env)
- Service failure is NOT due to account choice (proven by Quinn's tests)

---

### 4.3 Attempted: Local postgres OS Account for N8N

**Status**: ❌ **INCORRECT ATTEMPT - NEVER IMPLEMENTED**

| Property | Value |
|----------|-------|
| **Account Name** | `postgres` (OS account on hx-n8n-server) |
| **Attempted Use** | Run n8n service as postgres user |
| **Why Attempted** | Confusion with database postgres user |
| **Why Failed** | Wrong server, wrong purpose |

**Why This Was Wrong**:
- ❌ `postgres` OS account exists on **hx-postgres-server** (database server)
- ❌ `postgres` user is for PostgreSQL database process, NOT applications
- ❌ N8N runs on **hx-n8n-server** (different server)
- ❌ Services should have their own dedicated users

**Resolution**:
- Never implemented (caught during planning)
- Created dedicated `n8n` system user instead

---

## 5. Current Configuration

### 5.1 Active Accounts (In Use)

| Account | Type | Server | Purpose | Status |
|---------|------|--------|---------|--------|
| **n8n** (UID 999) | Local system user | hx-n8n-server (215) | Run n8n service | ✅ Active |
| **n8n_user** | PostgreSQL role | hx-postgres-server (209) | Database access | ✅ Active |
| **agent0** | Local admin | All servers | Administration | ✅ Active |
| **www-data** | System user | hx-n8n-server (215) | Nginx web server | ✅ Active |

### 5.2 Available Accounts (Created But Not Used)

| Account | Type | Server | Purpose | Status |
|---------|------|--------|---------|--------|
| **svc-postgres** | PostgreSQL role | hx-postgres-server (209) | App DB access (recommended) | ✅ Available |
| **n8n@hx.dev.local** | Domain account | All domain servers | Domain integration | ✅ Available |
| **postgres** | PostgreSQL role | hx-postgres-server (209) | DB administration | ✅ Available |

### 5.3 Current Service Configuration

**Systemd Service** (`/etc/systemd/system/n8n.service`):
```ini
[Unit]
Description=n8n Workflow Automation
After=network.target

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n
ExecStart=/opt/n8n/start-n8n.sh
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Environment Configuration** (`/opt/n8n/.env`):
```bash
# Database connection (as of 2025-11-08)
DB_POSTGRESDB_URL=postgresql://n8n_user:Major8859!@192.168.10.209:5432/n8n_poc3
```

**File Ownership**:
```bash
# All n8n files owned by n8n:n8n
/opt/n8n/         - n8n:n8n (drwxr-xr-x)
/opt/n8n/app/     - n8n:n8n (drwxr-xr-x)
/opt/n8n/.env     - n8n:n8n (rw-------) chmod 600
/opt/n8n/logs/    - n8n:n8n (drwxr-xr-x)
/opt/n8n/ssl/     - root:root (drwx------) chmod 700 (SSL certs)
```

---

## 6. Recommended Accounts

### 6.1 Recommended Configuration (Based on Standards)

**For n8n Service (OS Level)**:
- ✅ **USE**: `n8n` (UID 999) - local system user
- ✅ **CORRECT**: Non-login shell, dedicated user, proper permissions
- ⚠️ **FIX**: Home directory should be `/opt/n8n` (currently `/home/n8n`)

**For Database Connection (PostgreSQL)**:
- ⭐ **RECOMMENDED**: `svc-postgres` (per credentials document)
  - Reason: Standardized across all applications
  - Superuser privileges (allows migrations)
  - Dedicated application service account
  - Matches LiteLLM, FastMCP, other services

- ✅ **ALTERNATIVE**: `n8n_user` (currently in use, works fine)
  - Reason: Principle of least privilege
  - Dedicated to n8n only
  - Non-superuser (more secure)
  - Sufficient privileges for n8n operations

**Recommended Change**:
```bash
# Update /opt/n8n/.env to use svc-postgres (recommended)
DB_POSTGRESDB_URL=postgresql://svc-postgres:Major8859!@192.168.10.209:5432/n8n_poc3

# OR keep n8n_user (also valid)
DB_POSTGRESDB_URL=postgresql://n8n_user:Major8859!@192.168.10.209:5432/n8n_poc3
```

**Either choice is valid** - both accounts work, verified by Quinn Davis.

---

### 6.2 Accounts to Keep

| Account | Reason |
|---------|--------|
| **n8n** (UID 999) | ✅ Required - runs n8n service |
| **n8n_user** (DB) | ✅ Keep - currently in use, works |
| **svc-postgres** (DB) | ✅ Keep - recommended alternative |
| **n8n@hx.dev.local** | ✅ Keep - future LDAP integration |
| **agent0** | ✅ Keep - infrastructure standard |
| **www-data** | ✅ Keep - Nginx default user |
| **postgres** (DB) | ✅ Keep - database administration |

---

### 6.3 Accounts to Avoid

| Account | Why to Avoid |
|---------|--------------|
| **agent0** for services | ❌ Admin account, security risk |
| **postgres** (DB) for apps | ❌ Reserved for DB admin tasks only |
| **root** for services | ❌ Security violation |
| **Local postgres** on n8n-server | ❌ Wrong server, wrong purpose |

---

## 7. Cleanup Recommendations

### 7.1 File Ownership Audit

**Verify all files owned by correct user**:
```bash
# On hx-n8n-server
sudo find /opt/n8n -not -user n8n -o -not -group n8n
# Should return ONLY /opt/n8n/ssl/ (owned by root)

# Fix any incorrect ownership
sudo chown -R n8n:n8n /opt/n8n
sudo chown -R root:root /opt/n8n/ssl
sudo chmod 600 /opt/n8n/.env
```

### 7.2 Home Directory Fix (Optional)

**Issue**: `n8n` user has home directory `/home/n8n` instead of `/opt/n8n`

**Fix** (if desired for consistency):
```bash
# On hx-n8n-server
sudo usermod -d /opt/n8n n8n
getent passwd n8n
# Verify: n8n:x:999:988::/opt/n8n:/bin/false
```

**Impact**: Low priority - service works regardless

---

### 7.3 Account Documentation Updates

**Update needed in**:
1. `/srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-prereqs/t-011-create-service-user.md`
   - Add note about actual home directory vs specified

2. `/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.1-credentials.md`
   - Add note distinguishing local `n8n` from domain `n8n@hx.dev.local`

---

## 8. Account Usage Matrix

### 8.1 System Users by Server

| Server | Account | UID | Purpose | Shell | Status |
|--------|---------|-----|---------|-------|--------|
| hx-n8n-server (215) | n8n | 999 | N8N service | /bin/false | ✅ Active |
| hx-n8n-server (215) | agent0 | 1000 | Admin | /bin/bash | ✅ Active |
| hx-n8n-server (215) | www-data | 33 | Nginx | /usr/sbin/nologin | ✅ Active |
| hx-postgres-server (209) | postgres | 999 | PostgreSQL | /bin/bash | ✅ Active |
| hx-postgres-server (209) | agent0 | 1000 | Admin | /bin/bash | ✅ Active |

### 8.2 Database Roles by Purpose

| Role | Superuser | Login | Purpose | Used By | Status |
|------|-----------|-------|---------|---------|--------|
| postgres | Yes | Yes | DB admin | PostgreSQL admin | ✅ Active |
| svc-postgres | Yes | Yes | App DB access | **Recommended** for n8n | ✅ Available |
| n8n_user | No | Yes | N8N DB access | **Currently used** by n8n | ✅ Active |

### 8.3 Domain Accounts by Purpose

| Account | UID | Purpose | Available On | Status |
|---------|-----|---------|--------------|--------|
| n8n@hx.dev.local | 1114201137 | N8N domain account | All domain servers | ✅ Available |
| svc-postgres@hx.dev.local | 1114201133 | PostgreSQL domain account | All domain servers | ✅ Available |
| agent0 | 1000 | Admin (local) | All servers | ✅ Active |

---

## 9. Account Creation Timeline

### Phase 0 - Infrastructure Setup
- **agent0** - Created during base server provisioning (all servers)
- **www-data** - Created during Ubuntu installation (default)
- **postgres** (DB role) - Created during PostgreSQL installation
- **postgres** (OS account) - Created on hx-postgres-server during PostgreSQL setup

### Phase 1 - POC3 Preparation
- **Task T-011** (William): Create `n8n` system user on hx-n8n-server
  - Result: ✅ Created (UID 999, home=/home/n8n, shell=/bin/false)

- **Task T-017** (Quinn): Create `n8n_poc3` database
  - Result: ✅ Created (UTF8, owned by postgres)

- **Task T-018** (Quinn): Create `n8n_user` database role
  - Result: ✅ Created (non-superuser, with privileges on n8n_poc3)

### Pre-POC3 - Domain Integration (October 2025)
- **October 27, 2025**: Created `svc-postgres@hx.dev.local` domain account
  - Created via `samba-tool` on hx-dc-server
  - Database role created: `svc-postgres` (superuser)

- **October 2025**: Created `n8n@hx.dev.local` domain account
  - Created via `samba-tool` on hx-dc-server
  - Purpose: Domain-integrated n8n authentication

### Phase 2 - Deployment (November 2025)
- **November 8, 2025**: Database role password resets
  - Quinn reset `svc-postgres` password to `Major8859!`
  - Quinn reset `n8n_user` password to `Major8859!`
  - Both verified working via psql from hx-n8n-server

---

## 10. Known Issues and Resolutions

### Issue 1: N8N Service Authentication Failure

**Status**: ⚠️ **ACTIVE ISSUE** (as of 2025-11-08)

**Symptoms**:
- N8N process running (PID exists)
- N8N NOT listening on port 5678
- PostgreSQL authentication failing in n8n logs
- Manual psql connections work perfectly

**Root Cause**:
- **NOT a database account issue** (verified by Quinn Davis)
- **NOT a database configuration issue** (verified by Quinn Davis)
- **Likely**: N8N environment variable loading problem
- **Likely**: Password special character escaping issue (exclamation mark)

**Evidence**:
- ✅ `PGPASSWORD='Major8859!' psql -h 192.168.10.209 -U n8n_user -d n8n_poc3` → SUCCESS
- ✅ `PGPASSWORD='Major8859!' psql -h 192.168.10.209 -U svc-postgres -d n8n_poc3` → SUCCESS
- ❌ N8N service start → FAILED (password authentication error)

**Attempted Fixes**:
1. ❌ Tried switching from n8n_user to svc-postgres
2. ❌ Tried quoting password in .env: `DB_POSTGRESDB_PASSWORD="Major8859!"`
3. ❌ Tried unquoted password: `DB_POSTGRESDB_PASSWORD=Major8859!`
4. ❌ Tried `EnvironmentFile=/opt/n8n/.env` in systemd
5. ❌ Tried manual export + start (worked, but not reproducible in systemd)

**Next Steps**:
- Investigate N8N's dotenv library (how it reads .env files)
- Try URL-encoded password: `Major8859%21`
- Try connection string format instead of individual variables
- Test with simplified password (no special characters) as diagnostic
- Enable N8N debug logging: `N8N_LOG_LEVEL=debug`

**Documentation**:
- `/srv/cc/Governance/x-poc3-n8n-deployment/ESCALATION-QUINN-N8N-DATABASE-AUTH.md`
- `/srv/cc/Governance/x-poc3-n8n-deployment/QUINN-DATABASE-RESOLUTION.md`

**Ownership**: Omar Rodriguez (N8N application layer, NOT database layer)

---

### Issue 2: Multiple Database User Attempts

**Status**: ✅ **RESOLVED** (clarity provided)

**Confusion**:
- Task T-018 specified creating `n8n_user`
- Credentials document recommends `svc-postgres` for all apps
- Multiple attempts to switch between accounts during deployment

**Resolution**:
- Both accounts are valid and work correctly
- Current configuration uses `n8n_user` (as planned)
- Can switch to `svc-postgres` if desired (just update .env)
- Service failure unrelated to account choice (both tested by Quinn)

**Recommendation**:
- **Option A**: Keep `n8n_user` (dedicated, principle of least privilege)
- **Option B**: Switch to `svc-postgres` (standardized, matches other apps)
- **Either is acceptable** - choose based on preference

---

### Issue 3: Home Directory Mismatch

**Status**: ⚠️ **MINOR DEVIATION** (low priority)

**Issue**:
- Task T-011 specified: `useradd -d /opt/n8n`
- Actual result: home directory is `/home/n8n`

**Impact**:
- Service works correctly (uses WorkingDirectory=/opt/n8n in systemd)
- File ownership correct (/opt/n8n owned by n8n:n8n)
- Only cosmetic inconsistency

**Fix** (optional):
```bash
sudo usermod -d /opt/n8n n8n
```

**Priority**: Low - does not affect service operation

---

## 11. References

### Internal Documentation
1. **Credentials Document**: `/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.1-credentials.md`
   - Section 6: svc-postgres Application Service Account
   - Section 14: n8n Service Account (Domain-Integrated)

2. **Task Specifications**:
   - `/srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-prereqs/t-011-create-service-user.md`
   - `/srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-prereqs/t-018-create-postgresql-user.md`

3. **Escalation Documents**:
   - `/srv/cc/Governance/x-poc3-n8n-deployment/ESCALATION-QUINN-N8N-DATABASE-AUTH.md`
   - `/srv/cc/Governance/x-poc3-n8n-deployment/QUINN-DATABASE-RESOLUTION.md`

4. **Execution Status**:
   - `/srv/cc/Governance/x-poc3-n8n-deployment/phase2-execution-status.md`

### Verification Commands

**System Users**:
```bash
# On hx-n8n-server (192.168.10.215)
id n8n
getent passwd n8n
ls -ld /opt/n8n
ps aux | grep n8n
```

**Database Roles**:
```bash
# On hx-postgres-server (192.168.10.209)
sudo -u postgres /usr/local/pgsql/bin/psql -c "\du"
sudo -u postgres /usr/local/pgsql/bin/psql -l | grep n8n_poc3
```

**Database Connection Tests**:
```bash
# From hx-n8n-server (192.168.10.215)
PGPASSWORD='Major8859!' psql -h 192.168.10.209 -U n8n_user -d n8n_poc3 -c "SELECT current_user;"
PGPASSWORD='Major8859!' psql -h 192.168.10.209 -U svc-postgres -d n8n_poc3 -c "SELECT current_user;"
```

**File Ownership**:
```bash
# On hx-n8n-server
sudo ls -la /opt/n8n/
sudo cat /opt/n8n/.env | grep DB_
sudo systemctl status n8n
```

---

## 12. Summary and Action Items

### ✅ Accounts That Exist and Work

1. ✅ **n8n** (UID 999) - Local system user for n8n service
2. ✅ **n8n_user** - PostgreSQL role for n8n database access (currently in use)
3. ✅ **svc-postgres** - PostgreSQL role for application connections (recommended alternative)
4. ✅ **n8n@hx.dev.local** - Domain service account (available for LDAP integration)
5. ✅ **agent0** - Infrastructure admin account (correct usage for administration)
6. ✅ **www-data** - Nginx web server account (correct usage for proxy)

### ⚠️ Issues to Address

1. ⚠️ **HIGH PRIORITY**: N8N service authentication failure
   - **Cause**: Environment variable loading issue, NOT database issue
   - **Owner**: Omar Rodriguez (application layer)
   - **Next Steps**: Debug .env loading, try URL encoding, test simplified password

2. ⚠️ **LOW PRIORITY**: Home directory mismatch
   - **Issue**: n8n user has /home/n8n instead of /opt/n8n
   - **Impact**: Cosmetic only, service works
   - **Fix**: `sudo usermod -d /opt/n8n n8n` (optional)

3. ⚠️ **DOCUMENTATION**: Clarify database user recommendation
   - **Issue**: Task T-018 says n8n_user, credentials doc says svc-postgres
   - **Resolution**: Both are valid, either can be used
   - **Recommendation**: Document choice and rationale

### ❌ Failed Attempts (Abandoned)

1. ❌ Using agent0 for service execution (security violation)
2. ❌ Multiple database user switches (caused confusion, both work)
3. ❌ Various .env password quoting attempts (still failing)

### 📋 Action Items

| Priority | Action | Owner | Status |
|----------|--------|-------|--------|
| **P0** | Debug N8N environment variable loading | Omar | 🔴 BLOCKED |
| **P0** | Try URL-encoded password (`Major8859%21`) | Omar | ⏳ TODO |
| **P0** | Test simplified password (no special chars) | Omar | ⏳ TODO |
| **P1** | Document final database user choice (n8n_user vs svc-postgres) | Omar | ⏳ TODO |
| **P2** | Fix n8n home directory mismatch | William | ⏳ TODO |
| **P2** | Verify all file ownership (n8n:n8n) | William | ⏳ TODO |
| **P3** | Update task T-011 with actual vs expected home dir | Documentation | ⏳ TODO |

---

## Document Metadata

```yaml
document_type: Technical Reference - Account Inventory
project: POC3 N8N Workflow Automation Platform Deployment
author: Omar Rodriguez (N8N Workflow Worker Specialist)
created: 2025-11-08
last_updated: 2025-11-08
status: Active Reference
version: 1.0
classification: Internal
location: /srv/cc/Governance/x-poc3-n8n-deployment/ACCOUNTS-REQUIRED.md

accounts_documented:
  system_users: 6
  database_roles: 3
  domain_accounts: 2
  failed_attempts: 3

servers_covered:
  - hx-n8n-server.hx.dev.local (192.168.10.215)
  - hx-postgres-server.hx.dev.local (192.168.10.209)
  - hx-dc-server.hx.dev.local (domain controller)

verification_date: 2025-11-08
verification_method: SSH commands, psql queries, file inspection
verified_by: Omar Rodriguez (N8N), Quinn Davis (Database roles)
```

---

**Document Status**: ✅ COMPLETE
**Review Required**: Yes (by William Taylor for infrastructure accuracy)
**Next Update**: After n8n service authentication issue resolved

---

*End of Accounts Documentation*
