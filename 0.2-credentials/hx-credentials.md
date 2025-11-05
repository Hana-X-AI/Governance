# 🔒 HX.DEV.LOCAL Credentials & Secrets

**⚠️ SECURITY WARNING ⚠️**
This file contains sensitive credentials for the hx.dev.local infrastructure.
- Do NOT share this file
- Do NOT commit to public repositories
- Keep this file secure and encrypted if possible
- Rotate passwords regularly in production environments

---

## � STANDARD PASSWORD POLICY

### **⚠️ CRITICAL - READ THIS FIRST ⚠️**

**ALL SERVICE ACCOUNTS USE THE SAME PASSWORD**: `Major8859!`

This applies to **ALL** domain service accounts including:
- ✅ qdrant@hx.dev.local → `Major8859!`
- ✅ postgres@hx.dev.local → `Major8859!`
- ✅ redis@hx.dev.local → `Major8859!`
- ✅ nginx@hx.dev.local → `Major8859!`
- ✅ n8n@hx.dev.local → `Major8859!`
- ✅ grafana@hx.dev.local → `Major8859!`
- ✅ **ANY** future service account → `Major8859!`

**NO EXCEPTIONS**: This password is used for **EVERYTHING** including database superusers.

**Template for ALL Service Account Creation**:
```bash
# Create ANY service account with standard password
samba-tool user create <service-name> 'Major8859!' \
  --description='<Service Description> - Samba LDAP/DC' \
  --home-directory=/home/<service-name>@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn
```

---

## �📋 Overview

This document centralizes all authentication credentials and secrets for the hx.dev.local domain infrastructure. All other documentation should reference this file rather than storing passwords in plain text.

**Last Updated:** October 27, 2025  
**Environment:** Development/Test  
**Domain:** hx.dev.local

---

## 🔑 User Credentials

### Local Administrator (agent0)
- **Username:** `agent0`
- **Password:** `Major8859!`
- **UID:** 1000
- **Purpose:** Local system administration, SSH access, sudo operations
- **Used On:** All Ubuntu servers in hx.dev.local infrastructure
- **Access Level:** Local sudo/root access
- **Authentication:** Local PAM

**Usage Examples:**
```bash
# SSH login
ssh agent0@<server-ip>
# Password: Major8859!

# Sudo operations
sudo <command>
# Password: Major8859!
```

---

### Domain Administrator
- **Username:** `Administrator`
- **Full UPN:** `Administrator@HX.DEV.LOCAL`
- **Password:** `Major3059!`
- **UID:** 1114200500 (on domain-joined systems)
- **Purpose:** Domain administration, realm joins, domain-wide management
- **Used On:** Active Directory domain controller, all domain operations
- **Access Level:** Full domain administrator (Enterprise Admins, Domain Admins, Schema Admins)
- **Authentication:** Kerberos + SSSD

**Usage Examples:**
```bash
# Domain join operations
sudo realm join --user=Administrator hx.dev.local
# Password: Major3059!

# Kerberos authentication
kinit Administrator@HX.DEV.LOCAL
# Password: Major3059!

# LDAP authentication
ldapsearch -H ldap://hx-dc-server.hx.dev.local \
  -D "Administrator@hx.dev.local" -w 'Major3059!' \
  -b "DC=hx,DC=dev,DC=local"
```

---

### 3. qdrant Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `qdrant@hx.dev.local`  
**Password**: `Major8859!`  
**Type**: Domain service account (Samba LDAP/DC - NOT local user)  
**UID**: `1114201130` (Samba DC auto-assigned)  
**GID**: `1114200513` (Domain Users)  
**Home**: `/home/qdrant@hx.dev.local`

**⚠️ IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- Runs Qdrant vector database service
- Domain-integrated authentication via Kerberos + SSSD
- Used for service operations on hx-qdrant-server
- Account available on ALL domain-joined servers

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create qdrant 'Major8859!' \
  --description='Qdrant v1.15.5 Service Account - Samba LDAP/DC' \
  --home-directory=/home/qdrant@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn
```

**Login Example**:
```bash
# Not typically used for interactive login
# Service account runs qdrant.service via systemd
sudo systemctl status qdrant.service

# Verify domain account:
id qdrant@hx.dev.local
getent passwd qdrant@hx.dev.local
```

---

### 4. postgres Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `postgres@hx.dev.local`  
**Password**: `Major8859!`  
**Type**: Domain service account (Samba LDAP/DC - NOT local user)  
**UID**: `1114201131` (Samba DC auto-assigned)  
**GID**: `1114200513` (Domain Users)  
**Home**: `/home/postgres@hx.dev.local`

**Database Superuser Password**: `Major8859!` (SAME as OS account - standard password for ALL accounts)

**⚠️ CRITICAL - Samba LDAP/DC ONLY**:
- **MUST** be created using `samba-tool` on Domain Controller (hx-dc-server.hx.dev.local)
- **NEVER** use `useradd` or other local account tools
- Created during PRE-REQ-06: Domain User Creation task
- Samba DC automatically assigns UID/GID from domain pool
- Account replicates across all domain-joined servers via SSSD
- Integrated with hx.dev.local Active Directory/Samba LDAP

**Usage**:
- Runs PostgreSQL 17.6 database service
- Domain-integrated authentication via Kerberos + SSSD
- Used for service operations on hx-postgres-server
- Database administration and management
- Account available on ALL domain-joined servers

**Account Creation (via Samba DC - Required Method)**:
```bash
# STEP 1: SSH to Domain Controller as Administrator
ssh agent0@hx-dc-server.hx.dev.local
sudo -i

# STEP 2: Create domain user via samba-tool (REQUIRED METHOD)
samba-tool user create postgres 'Major8859!' \
  --description='PostgreSQL 17.6 Service Account - Samba LDAP/DC' \
  --home-directory=/home/postgres@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn

# STEP 3: Verify account creation
samba-tool user show postgres
wbinfo -i postgres@hx.dev.local

# STEP 4: Account becomes available across domain (via SSSD replication)
# Test from any domain-joined server:
# id postgres@hx.dev.local
# getent passwd postgres@hx.dev.local
```

**Login Example**:
```bash
# SSH to postgres server (after account creation)
ssh postgres@hx-postgres-server.hx.dev.local
# Password: Major8859!

# Connect to PostgreSQL as superuser
psql -U postgres
# Database password: Postgres2025!

# Check service status
sudo systemctl status postgresql-17.service
```

**Connection Strings**:
```bash
# Standard connection
psql postgresql://postgres:Major8859!@192.168.10.209:5432/postgres

# From remote host
psql -h 192.168.10.209 -p 5432 -U postgres -d postgres
# Password: Major8859!
```

---

### 5. redis Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `redis@hx.dev.local`  
**Password**: `Major8859!`  
**Type**: Domain service account (Samba LDAP/DC - NOT local user)  
**UID**: `1114201132` (Samba DC auto-assigned)  
**GID**: `1114200513` (Domain Users)  
**Home**: `/home/redis@hx.dev.local`

**⚠️ DEVELOPMENT ENVIRONMENT - No Authentication Required**:
- **DEV Mode**: Redis configured WITHOUT password authentication for development convenience
- **Production Would Use**: `requirepass Major8859!` (same standard password)
- **Current Config**: `/etc/redis/redis.conf` (no auth, all commands enabled)

**⚠️ IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- Runs Redis 7.4.6 in-memory data store service
- Domain-integrated authentication via Kerberos + SSSD
- Used for service operations on hx-redis-server
- Account available on ALL domain-joined servers
- Service deployed: October 27, 2025

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create redis 'Major8859!' \
  --description='Redis 7.4.6 Service Account - Samba LDAP/DC' \
  --home-directory=/home/redis@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn
```

**Login Example**:
```bash
# SSH to redis server
ssh redis@hx-redis-server.hx.dev.local
# Password: Major8859!

# Connect to Redis (DEV mode - no auth required)
redis-cli -h 192.168.10.210 -p 6379
# No password prompt in DEV

# Verify domain account:
id redis@hx.dev.local
getent passwd redis@hx.dev.local
```

**Connection Strings (DEV Environment)**:
```bash
# No authentication in DEV
redis-cli -h 192.168.10.210 -p 6379

# Python redis-py (no auth)
redis.Redis(host='192.168.10.210', port=6379)

# Connection URI (no auth in DEV)
redis://192.168.10.210:6379

# Production would use:
# redis://:Major8859!@192.168.10.210:6379
```

**Service Management**:
```bash
# Check service status
sudo systemctl status redis-server

# View logs
sudo journalctl -u redis-server -f

# Configuration file (DEV mode)
cat /etc/redis/redis.conf
```

---

### 6. svc-postgres Application Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `svc-postgres@hx.dev.local`  
**Password**: `Major8859!`  
**Type**: Domain service account (Samba LDAP/DC - NOT local user)  
**UID**: `1114201133` (Samba DC auto-assigned)  
**GID**: `1114200513` (Domain Users)  
**Home**: `/home/svc-postgres@hx.dev.local`

**Database Superuser Password**: `Major8859!` (SAME as OS account - standard password)

**✅ PASSWORD VERIFIED**: Database role password confirmed reset to Major8859! on 2025-10-31
- Tested from hx-litellm-server (192.168.10.212) → hx-postgres-server (192.168.10.209)
- Connection successful to both litellm and postgres databases
- Authentication working correctly

**⚠️ RECOMMENDED FOR ALL APPLICATIONS ⭐**:
- **USE THIS ACCOUNT** for all application database connections
- **RESERVE postgres@hx.dev.local** for administrative tasks only (upgrades, configuration)
- Same privileges as postgres superuser but dedicated for application use
- Created: October 27, 2025
- Documented: `/etc/ansible/postgres/SVC-POSTGRES-SERVICE-ACCOUNT.md`

**⚠️ IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- **PRIMARY** service account for application database connections
- All API backends, web apps, services should use this account
- Domain-integrated authentication via Kerberos + SSSD
- Superuser privileges for database operations
- Account available on ALL domain-joined servers

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create svc-postgres 'Major8859!' \
  --description='PostgreSQL Application Service Account - Samba LDAP/DC' \
  --home-directory=/home/svc-postgres@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn

# Database role created with superuser privileges:
CREATE ROLE "svc-postgres" WITH LOGIN SUPERUSER PASSWORD 'Major8859!';
```

**Connection Strings (RECOMMENDED FOR ALL APPS ⭐)**:
```bash
# Standard connection (USE THIS)
psql postgresql://svc-postgres:Major8859!@192.168.10.209:5432/postgres

# From remote host
psql -h 192.168.10.209 -p 5432 -U svc-postgres -d postgres
# Password: Major8859!

# Python psycopg2
import psycopg2
conn = psycopg2.connect(
    host="192.168.10.209",
    database="postgres",
    user="svc-postgres",  # ⭐ Use this for apps
    password="Major8859!"
)

# SQLAlchemy
engine = create_engine('postgresql://svc-postgres:Major8859!@192.168.10.209:5432/postgres')
```

**Best Practice**:
- ✅ Applications → Use `svc-postgres@hx.dev.local`
- ✅ Administration → Use `postgres@hx.dev.local`
- ✅ Emergency/Maintenance → Use `postgres@hx.dev.local`

---

### 7. fastmcp Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `fastmcp@hx.dev.local`  
**Password**: `Major8859!`  
**Type**: Domain service account (Samba LDAP/DC - NOT local user)  
**UID**: `1114201135` (Samba DC auto-assigned)  
**GID**: `1114200513` (Domain Users)  
**Home**: `/home/fastmcp@hx.dev.local`

**⚠️ IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- Runs FastMCP v2.0 Model Context Protocol server
- Domain-integrated authentication via Kerberos + SSSD
- Used for service operations on hx-fastmcp-server (192.168.10.213)
- Provides MCP hub for mounting multiple MCP servers
- Account available on ALL domain-joined servers
- Service deployed: October 28, 2025

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create fastmcp 'Major8859!' \
  --description='FastMCP v2.0 MCP Server - Samba LDAP/DC' \
  --home-directory=/home/fastmcp@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn
```

**Service Configuration**:
- **Transport**: HTTP on port 8000
- **Installation**: /opt/fastmcp
- **Configuration**: /opt/fastmcp/.env
- **Data**: /opt/fastmcp/data
- **Logs**: systemd journal (journalctl -u fastmcp)

**Integration Points** (Phase 2):
```bash
# LiteLLM integration
LITELLM_URL=http://hx-litellm-server.hx.dev.local:4000
LITELLM_API_KEY=eee2c3d2aba9be064c3e6f7de1893aff44a992d0af3726bf73ccd2672f804cdb

# PostgreSQL integration
DATABASE_URL=postgresql://svc-postgres:Major8859!@hx-postgres-server.hx.dev.local:5432/postgres

# Redis integration
REDIS_URL=redis://hx-redis-server.hx.dev.local:6379
```

**MCP Server Mounting** (Phase 3):
- mcp-server-qdrant (Qdrant vector DB)
- n8n-mcp (N8N workflow automation)
- docling-mcp (Document processing)
- crawl4ai-mcp (Web crawling)

**Connection Strings**:
```bash
# HTTP transport
http://hx-fastmcp-server.hx.dev.local:8000

# Direct IP
http://192.168.10.213:8000

# Health check
curl http://192.168.10.213:8000/health
```

**Service Management**:
```bash
# SSH to server
ssh fastmcp@hx-fastmcp-server.hx.dev.local
# Password: Major8859!

# Check service status
sudo systemctl status fastmcp.service

# View logs
sudo journalctl -u fastmcp.service -f

# Verify domain account
id fastmcp@hx.dev.local
getent passwd fastmcp@hx.dev.local
```

**Security Notes**:
- ✅ Service runs as non-root domain user
- ✅ HTTP only (internal network)
- ⚠️ Consider adding authentication for production
- ⚠️ Consider HTTPS for production

---

### 8. litellm Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `litellm@hx.dev.local`  
**Password**: `PzvaDXmEwc/Rdq777rgVSZv9Mm6VNQLh`  
**Type**: Domain service account (Samba LDAP/DC - NOT local user)  
**UID**: `1114201134` (Samba DC auto-assigned)  
**GID**: `1114200513` (Domain Users)  
**Home**: `/home/litellm@hx.dev.local`

**LiteLLM Master Key (API Authentication)**: `eee2c3d2aba9be064c3e6f7de1893aff44a992d0af3726bf73ccd2672f804cdb`  
**Key Type**: 64-character hex string (generated via `openssl rand -hex 32`)  
**Key Storage**: `/opt/litellm/config/.env` (permissions: 600)  
**Key Usage**: Required for ALL API requests via `x-litellm-api-key` header

**⚠️ IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- Runs LiteLLM 1.77.7 proxy service (OpenAI v1 API gateway)
- Domain-integrated authentication via Kerberos + SSSD
- Used for service operations on hx-litellm-server (192.168.10.212)
- Proxies 12 Ollama models across 3 backend servers
- Account available on ALL domain-joined servers
- Service deployed: October 27, 2025

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create litellm 'PzvaDXmEwc/Rdq777rgVSZv9Mm6VNQLh' \
  --description='LiteLLM 1.77.7 Proxy Service Account - Samba LDAP/DC' \
  --home-directory=/home/litellm@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn
```

**API Authentication (REQUIRED FOR ALL REQUESTS)**:
```bash
# curl with master key
curl -H "x-litellm-api-key: eee2c3d2aba9be064c3e6f7de1893aff44a992d0af3726bf73ccd2672f804cdb" \
  http://hx-litellm-server.hx.dev.local:4000/models

# Python OpenAI SDK
from openai import OpenAI
client = OpenAI(
    api_key="eee2c3d2aba9be064c3e6f7de1893aff44a992d0af3726bf73ccd2672f804cdb",
    base_url="http://hx-litellm-server.hx.dev.local:4000"
)

# Web UI access
http://hx-litellm-server.hx.dev.local:4000/ui?key=eee2c3d2aba9be064c3e6f7de1893aff44a992d0af3726bf73ccd2672f804cdb
```

**Database Connection** (uses svc-postgres):
```bash
# LiteLLM connects to PostgreSQL as svc-postgres
DATABASE_URL=postgresql://svc-postgres:Major8859!@hx-postgres-server.hx.dev.local:5432/litellm?sslmode=require
```

**Service Management**:
```bash
# SSH to server (rarely needed - service runs automatically)
ssh litellm@hx-litellm-server.hx.dev.local
# Password: PzvaDXmEwc/Rdq777rgVSZv9Mm6VNQLh

# Check service status
sudo systemctl status litellm.service

# View logs
sudo journalctl -u litellm.service -f

# Verify domain account
id litellm@hx.dev.local
getent passwd litellm@hx.dev.local
```

**Available Models (12 total across 3 Ollama servers)**:
- Ollama1 (192.168.10.204): gemma3:27b, gpt-oss:20b, mistral:7b (chat models)
- Ollama2 (192.168.10.205): llama3.3:70b, qwen2.5:32b, qwen2.5-coder:7b, cogito:3b, qwen3-coder:30b, qwen2.5:7b (chat models)
- Ollama3 (192.168.10.206): aipromptassistant (prompt enhancement), bge-reranker-v2-m3 (reranking), bge-m3:567m (embeddings)

**Security Notes**:
- ⚠️ Master key provides full API access - store securely
- ⚠️ Consider moving master key to Ansible Vault for production
- ✅ Database connection uses SSL (sslmode=require)
- ✅ Service runs as non-root domain user
- ⚠️ API runs HTTP (not HTTPS) - internal network only

---

### 9. www-data Service Account (Qdrant Web UI)

**Username**: `www-data` (local system account)  
**Password**: N/A (system account, no password login)  
**Type**: Local system account (standard Nginx user)  
**UID**: 33 (Debian/Ubuntu standard)  
**GID**: 33 (www-data group)  
**Home**: `/var/www`

**⚠️ EXCEPTION**: This is a **local system account**, NOT a domain account via Samba LDAP/DC

**Usage**:
- Runs Qdrant Web UI v0.2.0 (React-based management interface)
- Nginx web server process owner
- Serves static files on hx-qdrant-ui-server (192.168.10.208)
- Browser-based access, no authentication required (development mode)
- Service deployed: October 25, 2025

**Service Configuration**:
- **Web Server**: Nginx 1.24.x
- **Installation**: /srv/ui/qdrant-web-ui/
- **Logs**: /var/log/nginx/
- **Port**: 80 (HTTP)

**Access URLs**:
```bash
# Via hostname (requires DNS)
http://hx-qdrant-ui.hx.dev.local

# Via IP address
http://192.168.10.208
```

**Service Management**:
```bash
# Check Nginx status
sudo systemctl status nginx

# View logs
sudo tail -f /var/log/nginx/qdrant-ui-access.log
sudo tail -f /var/log/nginx/qdrant-ui-error.log

# Verify www-data account
id www-data
getent passwd www-data
```

**Security Notes**:
- ✅ System account, cannot login via SSH
- ✅ Runs web server only (no shell access)
- ⚠️ HTTP only (no HTTPS in development)
- ⚠️ No UI authentication (development mode)
- ⚠️ Backend CORS must be configured for browser API access

---

### 10. svc-litellm Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `svc-litellm@hx.dev.local`
**Password**: `Major8859` (NO special characters - Prisma URL compatibility)
**Type**: Domain service account (Samba LDAP/DC - NOT local user)
**UID**: `1114201137` (Samba DC auto-assigned)
**GID**: `1114200513` (Domain Users)
**Home**: `/home/svc-litellm@hx.dev.local`

**Database Role Password**: `Major8859` (SAME as OS account - NO special characters)

**✅ PASSWORD VERIFIED**: Database role password confirmed on 2025-10-31
- Tested from hx-litellm-server (192.168.10.212) → hx-postgres-server (192.168.10.209)
- Connection successful to litellm database
- Authentication working correctly
- NO special characters to avoid Prisma URL encoding issues

**⚠️ DEDICATED FOR LITELLM APPLICATION**:
- **CREATED FOR**: LiteLLM application database connections only
- **PURPOSE**: Avoid special character issues in Prisma connection URLs
- **PASSWORD**: Major8859 (no exclamation mark or other special characters)
- Created: October 31, 2025
- Reason: Prisma cannot handle special characters in DATABASE_URL properly

**⚠️ IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- Dedicated service account for LiteLLM application database connections
- Domain-integrated authentication via Kerberos + SSSD
- PostgreSQL database access with full privileges on litellm database
- Account available on ALL domain-joined servers

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create svc-litellm 'Major8859' \
  --description='LiteLLM Proxy Service Account' \
  --home-directory=/home/svc-litellm@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn

# Database role created with full privileges on litellm database:
CREATE ROLE "svc-litellm" WITH LOGIN PASSWORD 'Major8859';
GRANT CONNECT ON DATABASE litellm TO "svc-litellm";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "svc-litellm";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "svc-litellm";
GRANT CREATE ON SCHEMA public TO "svc-litellm";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO "svc-litellm";
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO "svc-litellm";
```

**Connection Strings (RECOMMENDED FOR LITELLM)**:
```bash
# Standard connection (USE THIS IN LITELLM .env)
postgresql://svc-litellm:Major8859@hx-postgres-server.hx.dev.local:5432/litellm?sslmode=disable

# From remote host (psql test)
psql -h hx-postgres-server.hx.dev.local -U svc-litellm -d litellm
# Password: Major8859

# Python psycopg2
import psycopg2
conn = psycopg2.connect(
    host="hx-postgres-server.hx.dev.local",
    database="litellm",
    user="svc-litellm",
    password="Major8859"
)
```

**Database Permissions**:
- ✅ CONNECT on litellm database
- ✅ ALL PRIVILEGES on all tables in schema public
- ✅ ALL PRIVILEGES on all sequences in schema public
- ✅ CREATE on schema public (for migrations)
- ✅ Default privileges for future tables and sequences

**Best Practice**:
- ✅ LiteLLM application → Use `svc-litellm@hx.dev.local`
- ✅ Other applications → Use `svc-postgres@hx.dev.local` (standard password with special chars)
- ✅ Administration → Use `postgres@hx.dev.local`

**Security Notes**:
- ✅ Dedicated account for single application (isolation)
- ✅ Password has NO special characters (Prisma compatibility)
- ⚠️ Password is simpler (no special chars) - acceptable for dev environment
- ⚠️ SSL disabled in connection string - internal network only

---

### 11. crawl4ai Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `crawl4ai@hx.dev.local`
**Password**: `Major8859!`
**Type**: Domain service account (Samba LDAP/DC - NOT local user)
**UID**: `1114201138` (Samba DC auto-assigned)
**GID**: `1114200513` (Domain Users)
**Home**: `/home/crawl4ai@hx.dev.local`

**⚠️ IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- Runs Crawl4AI Worker Service
- Domain-integrated authentication via Kerberos + SSSD
- Used for service operations on hx-crawl4ai-server (192.168.10.219)
- Web crawling and content extraction service
- Account available on ALL domain-joined servers
- Service deployed: October 31, 2025

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create crawl4ai 'Major8859!' \
  --description='Crawl4AI Worker Service Account' \
  --given-name='Crawl4AI' \
  --surname='Worker'

# Password expiration disabled:
samba-tool user setexpiry crawl4ai --noexpiry
```

**Service Configuration**:
- **Server**: hx-crawl4ai-server.hx.dev.local (192.168.10.219)
- **Purpose**: Web crawling and content extraction
- **Integration**: Part of hx.dev.local AI ecosystem

**Login Example**:
```bash
# SSH to crawl4ai server
ssh crawl4ai@hx-crawl4ai-server.hx.dev.local
# Password: Major8859!

# Verify domain account:
id crawl4ai@hx.dev.local
getent passwd crawl4ai@hx.dev.local
```

**Service Management**:
```bash
# Check service status
sudo systemctl status crawl4ai.service

# View logs
sudo journalctl -u crawl4ai.service -f

# Verify domain account
id crawl4ai@hx.dev.local
getent passwd crawl4ai@hx.dev.local
```

---

### 12. crawl4aimcp Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `crawl4aimcp@hx.dev.local`
**Password**: `Major8859!`
**Type**: Domain service account (Samba LDAP/DC - NOT local user)
**UID**: `1114201139` (Samba DC auto-assigned)
**GID**: `1114200513` (Domain Users)
**Home**: `/home/crawl4aimcp@hx.dev.local`

**IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- Runs Crawl4AI MCP Server Service
- Domain-integrated authentication via Kerberos + SSSD
- Used for service operations on hx-crawl4ai-mcp-server (192.168.10.218)
- MCP protocol layer for Crawl4AI (client-facing HTTPS on port 8000)
- Account available on ALL domain-joined servers
- Service deployed: November 1, 2025

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create crawl4aimcp 'Major8859!' \
  --description='Crawl4AI MCP Server Service Account' \
  --given-name='Crawl4AI' \
  --surname='MCP'

# Password expiration disabled:
samba-tool user setexpiry crawl4aimcp --noexpiry
```

**Service Configuration**:
- **Server**: hx-crawl4ai-mcp-server.hx.dev.local (192.168.10.218)
- **Port**: 8000 HTTPS (SSL REQUIRED)
- **Purpose**: MCP protocol layer for Crawl4AI worker
- **SSL Certificates**: /srv/crawl4ai-mcp/ssl/
- **Integration**: Part of hx.dev.local AI ecosystem

**Login Example**:
```bash
# SSH to crawl4ai-mcp server
ssh crawl4aimcp@hx-crawl4ai-mcp-server.hx.dev.local
# Password: Major8859!

# Verify domain account:
id crawl4aimcp@hx.dev.local
getent passwd crawl4aimcp@hx.dev.local
```

**Service Management**:
```bash
# Check service status
sudo systemctl status crawl4ai-mcp.service

# View logs
sudo journalctl -u crawl4ai-mcp.service -f

# Verify domain account
id crawl4aimcp@hx.dev.local
getent passwd crawl4aimcp@hx.dev.local
```

**SSL/TLS Details**:
- **Certificate**: /srv/crawl4ai-mcp/ssl/server.crt
- **Private Key**: /srv/crawl4ai-mcp/ssl/server.key
- **CA Certificate**: /srv/crawl4ai-mcp/ssl/ca.crt
- **Expiration**: November 1, 2027 (730 days)
- **Issued By**: HX.DEV.LOCAL Internal CA

---

### 13. docling-mcp Service Account (Domain-Integrated - Samba LDAP/DC)

**Username**: `docling-mcp@hx.dev.local`
**Password**: `Major8859!`
**Type**: Domain service account (Samba LDAP/DC - NOT local user)
**UID**: `1114201140` (Samba DC auto-assigned)
**GID**: `1114200513` (Domain Users)
**Home**: `/home/docling-mcp@hx.dev.local`

**IMPORTANT**: Created via `samba-tool` on Domain Controller, NOT local useradd

**Usage**:
- Runs Docling MCP Server Service
- Domain-integrated authentication via Kerberos + SSSD
- Used for service operations on hx-docling-mcp-server (192.168.10.217)
- Document processing and OCR service via MCP protocol
- Account available on ALL domain-joined servers
- Service deployed: November 1, 2025

**Account Creation (Samba DC Method)**:
```bash
# Created on hx-dc-server.hx.dev.local via samba-tool:
samba-tool user create docling-mcp 'Major8859!' \
  --description='Docling MCP Service Account - Samba LDAP/DC' \
  --login-shell='/bin/bash' \
  --use-username-as-cn
```

**Service Configuration**:
- **Server**: hx-docling-mcp-server.hx.dev.local (192.168.10.217)
- **Purpose**: Document processing and OCR via MCP protocol
- **Integration**: Part of hx.dev.local AI ecosystem

**Login Example**:
```bash
# SSH to docling-mcp server
ssh docling-mcp@hx-docling-mcp-server.hx.dev.local
# Password: Major8859!

# Verify domain account:
id docling-mcp@hx.dev.local
getent passwd docling-mcp@hx.dev.local
```

**Service Management**:
```bash
# Check service status
sudo systemctl status docling-mcp.service

# View logs
sudo journalctl -u docling-mcp.service -f

# Verify domain account
id docling-mcp@hx.dev.local
getent passwd docling-mcp@hx.dev.local
```

---

### 14. Future Service Accounts (All Samba LDAP/DC)

**⚠️ MANDATORY RULE - ALL SERVICE ACCOUNTS**:
- **ALL** user accounts MUST be created via Samba LDAP/DC (`samba-tool`)
- **NEVER** use local account creation tools (useradd, adduser, etc.)
- Domain Controller: hx-dc-server.hx.dev.local (192.168.10.200)
- All accounts replicate automatically to domain-joined servers via SSSD

**Future Service Accounts** (to be created via `samba-tool`):
```bash
# Template for creating service accounts:
# SSH to hx-dc-server.hx.dev.local
ssh agent0@hx-dc-server.hx.dev.local
sudo -i

# Create service account via samba-tool
samba-tool user create <service-name> 'Major8859!' \
  --description='<Service Description> - Samba LDAP/DC' \
  --home-directory=/home/<service-name>@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn

# Examples for future services:
# - n8n@hx.dev.local (N8N automation service)
# - grafana@hx.dev.local (Grafana monitoring service)
# - nginx@hx.dev.local (Nginx web server service)
# - openwebui@hx.dev.local (OpenWebUI service)
```

**Service Account Standard Password**: `Major8859!` (consistent across all service accounts)

**Verification After Creation**:
```bash
# Test from any domain-joined server:
id <service-name>@hx.dev.local
getent passwd <service-name>@hx.dev.local
wbinfo -i <service-name>@hx.dev.local

# Should show domain UID (starting with 1114...)
# Should show domain GID (1114200513 - Domain Users)
```

---

## 🔐 Certificate Authority (CA) Secrets

### CA Private Key Passphrase
- **Passphrase:** `Longhorn88`
- **Purpose:** Protects CA private key for certificate generation
- **Used On:** hx-ca-server (192.168.10.201)
- **Location:** `~/easy-rsa-pki/private/ca.key` (encrypted)
- **Algorithm:** RSA 4096-bit
- **Valid Until:** 10 years from CA creation

**Usage Examples:**
```bash
# Generate server certificate (on hx-ca-server)
cd ~/easy-rsa-pki
./easyrsa build-server-full hx-<server>-server.hx.dev.local nopass
# Enter CA passphrase: Longhorn88

# Sign certificate requests
./easyrsa sign-req server <server-name>
# Enter CA passphrase: Longhorn88

# Renew certificate
./easyrsa renew <server-name>
# Enter CA passphrase: Longhorn88
```

---

## 🖥️ Server Access Matrix

| Server | IP Address | SSH User | SSH Password | Domain User | Domain Password | Notes |
|--------|------------|----------|--------------|-------------|-----------------|-------|
| hx-dc-server | 192.168.10.200 | agent0 | Major8859! | Administrator | Major3059! | Domain Controller |
| hx-ca-server | 192.168.10.201 | agent0 | Major8859! | Administrator | Major3059! | Certificate Authority |
| hx-ssl-server | 192.168.10.202 | agent0 | Major8859! | Administrator | Major3059! | SSL Infrastructure |
| hx-control-node | 192.168.10.203 | agent0 | Major8859! | Administrator | Major3059! | Ansible/Automation |
| hx-ollama1-server | 192.168.10.204 | agent0 | Major8859! | Administrator | Major3059! | Ollama AI (3 models) |
| hx-ollama2-server | 192.168.10.205 | agent0 | Major8859! | Administrator | Major3059! | Ollama AI (6 models) |
| hx-ollama3-server | 192.168.10.206 | agent0 | Major8859! | Administrator | Major3059! | Ollama AI (3 models) |
| hx-qdrant-server | 192.168.10.207 | agent0 | Major8859! | Administrator | Major3059! | Vector Database (qdrant service user) |
| hx-qdrant-ui-server | 192.168.10.208 | agent0 | Major8859! | Administrator | Major3059! | Qdrant Web UI (www-data system account) |
| hx-postgres-server | 192.168.10.209 | agent0 | Major8859! | Administrator | Major3059! | PostgreSQL 17.6 (postgres, svc-postgres) |
| hx-redis-server | 192.168.10.210 | agent0 | Major8859! | Administrator | Major3059! | Redis 7.4.6 (redis service user) |
| hx-litellm-server | 192.168.10.212 | agent0 | Major8859! | Administrator | Major3059! | LiteLLM 1.77.7 (litellm service user) |
| hx-fastmcp-server | 192.168.10.213 | agent0 | Major8859! | Administrator | Major3059! | FastMCP v2.0 (fastmcp service user) |
| hx-crawl4ai-server | 192.168.10.219 | agent0 | Major8859! | Administrator | Major3059! | Crawl4AI Worker (crawl4ai service user) |
| hx-crawl4ai-mcp-server | 192.168.10.218 | agent0 | Major8859! | Administrator | Major3059! | Crawl4AI MCP (crawl4aimcp service user) |
| hx-docling-mcp-server | 192.168.10.217 | agent0 | Major8859! | Administrator | Major3059! | Docling MCP (docling-mcp service user) |
| hx-cc-server | 192.168.10.224 | agent0 | Major8859! | Administrator | Major3059! | Infrastructure |
| hx-webui-server | 192.168.10.227 | agent0 | Major8859! | Administrator | Major3059! | OpenWebUI (offline) |

---

## 🔄 Password Policy

### Current Policy (Dev/Test Environment)
- **Complexity:** Medium (alphanumeric + special characters)
- **Length:** 8-10 characters
- **Expiration:** None (static for infrastructure stability)
- **Rotation:** On-demand (not automated)
- **Scope:** Development/Test environment only

### Recommendations for Production
If this infrastructure moves to production:
- ✅ Increase password length to 16+ characters
- ✅ Enable password expiration (90 days)
- ✅ Implement MFA for Administrator account
- ✅ Use password manager (1Password, Bitwarden, etc.)
- ✅ Rotate CA passphrase annually
- ✅ Enable audit logging for credential usage
- ✅ Separate dev/prod credentials completely

---

## 🛡️ Security Best Practices

### Current State (Development)
- ✅ All servers use same local credentials (simplified management)
- ✅ Domain admin separate from local admin (proper separation)
- ✅ CA passphrase protects certificate generation
- ⚠️ Passwords stored in documentation (convenience over security)
- ⚠️ No MFA enabled (acceptable for dev/test)
- ⚠️ Static passwords (acceptable for dev/test)

### Access Control
- **SSH Access:** Key-based authentication preferred (passwords allowed for convenience)
- **Sudo Access:** Password required (no NOPASSWD for security)
- **Domain Access:** Kerberos tickets expire after 10 hours (default)
- **Certificate Generation:** Passphrase required (protects CA)

### Credential Storage
- **This File:** Primary source of truth for credentials
- **Other Documentation:** Should reference this file, not duplicate passwords
- **Scripts:** Use variables or prompt for passwords, don't hardcode
- **Backups:** Encrypt any backups containing this file

---

## 📝 Usage Guidelines

### For SSH Access
```bash
# Always use agent0 for SSH (never Administrator directly)
ssh agent0@<server-fqdn>
# Password: Major8859!

# Then switch to domain user if needed
su - Administrator
# Password: Major3059!
```

### For Domain Operations
```bash
# Use Administrator for domain joins
sudo realm join --user=Administrator hx.dev.local
# Password: Major3059!

# Use Administrator for Kerberos
kinit Administrator@HX.DEV.LOCAL
# Password: Major3059!
```

### For Creating Service Accounts (REQUIRED: Samba LDAP/DC)
```bash
# ⚠️ CRITICAL: ALL accounts MUST use this method
# STEP 1: SSH to Domain Controller
ssh agent0@hx-dc-server.hx.dev.local
sudo -i

# STEP 2: Create domain user via samba-tool (ONLY VALID METHOD)
samba-tool user create <username> 'Major8859!' \
  --description='<Service Name> Service Account - Samba LDAP/DC' \
  --home-directory=/home/<username>@hx.dev.local \
  --login-shell=/bin/bash \
  --use-username-as-cn

# STEP 3: Verify account replication
wbinfo -i <username>@hx.dev.local
samba-tool user show <username>

# STEP 4: Test from target server (domain-joined)
ssh agent0@<target-server>
id <username>@hx.dev.local
getent passwd <username>@hx.dev.local

# ❌ NEVER DO THIS (local accounts not domain-integrated):
# useradd <username>  # WRONG - local only, not domain-integrated
# adduser <username>  # WRONG - local only, not domain-integrated
```

### For Certificate Generation
```bash
# SSH to CA server as agent0
ssh agent0@192.168.10.201
# Password: Major8859!

# Generate certificate (will prompt for CA passphrase)
cd ~/easy-rsa-pki
./easyrsa build-server-full <servername>.hx.dev.local nopass
# Enter CA passphrase: Longhorn88
```

---

## 🔍 Credential Verification

### Test Local Credentials
```bash
# SSH test
ssh agent0@<server-ip>
# Should succeed with Major8859!

# Sudo test
sudo whoami
# Should return: root
```

### Test Domain Credentials
```bash
# User resolution test
id Administrator
# Should return UID 1114200500

# Domain membership test
sudo realm list
# Should show: configured: kerberos-member

# Kerberos test
kinit Administrator@HX.DEV.LOCAL
klist
# Should show valid ticket
```

### Test CA Passphrase
```bash
# On hx-ca-server
cd ~/easy-rsa-pki
./easyrsa show-ca
# Enter passphrase: Longhorn88
# Should display CA certificate
```

---

## 📊 Credential History

| Date | Change | Reason | Updated By |
|------|--------|--------|------------|
| 2025-10-22 | Initial documentation | Centralize credentials | GitHub Copilot |
| 2025-10-24 | Added qdrant service account | Qdrant deployment prerequisites | GitHub Copilot |
| 2025-10-25 | Added postgres service account (UID 1114201131) | PostgreSQL 17.6 deployment | GitHub Copilot |
| 2025-10-27 | Added redis service account (UID 1114201132) | Redis 7.4.6 deployment (DEV mode) | GitHub Copilot |
| 2025-10-27 | Added svc-postgres account (UID 1114201133) | PostgreSQL application service account | GitHub Copilot |
| 2025-10-27 | Added litellm service account (UID 1114201134) | LiteLLM 1.77.7 proxy deployment | GitHub Copilot |
| 2025-10-27 | Added LiteLLM master key | API authentication for LiteLLM proxy | GitHub Copilot |
| 2025-10-28 | Added fastmcp service account (UID 1114201135) | FastMCP v2.0 deployment | GitHub Copilot |
| 2025-10-28 | Added www-data system account | Qdrant Web UI (Nginx) | GitHub Copilot |
| 2025-10-31 | Added svc-litellm service account (UID 1114201137) | LiteLLM dedicated PostgreSQL account (no special chars) | Claude Code |
| 2025-10-31 | Added crawl4ai service account (UID 1114201138) | Crawl4AI Worker Service deployment | Claude Code |
| 2025-11-01 | Added crawl4aimcp service account (UID 1114201139) | Crawl4AI MCP Server deployment | Claude Code Infrastructure Agent |
| 2025-11-01 | Added docling-mcp service account (UID 1114201140) | Docling MCP Server deployment | Claude Code Infrastructure Agent |

**Note:** Passwords have been static since infrastructure creation. No changes required for dev/test environment.

---

## 🚨 Emergency Procedures

### Lost/Forgotten Passwords

**If Local Password (Major8859!) is Lost:**
1. Physical console access required
2. Boot into recovery mode
3. Reset agent0 password using `passwd` command
4. Update this document

**If Domain Password (Major3059!) is Lost:**
1. Access Domain Controller (hx-dc-server) as agent0
2. Reset Administrator password using `samba-tool user setpassword Administrator`
3. Update all documentation
4. Re-test all domain-joined servers

**If CA Passphrase (Longhorn88) is Lost:**
1. CA private key is unusable
2. Must generate new CA (breaks all existing certificates)
3. Re-issue all server certificates
4. Re-deploy to all servers
5. **Last Resort Only** - Document carefully

### Compromised Credentials

**If Credentials are Compromised:**
1. Immediately rotate all passwords
2. Check audit logs for unauthorized access
3. Review all recent system changes
4. Generate new CA if passphrase compromised
5. Update this document with new credentials
6. Notify all users with access

---

## 📧 Contact Information

**Infrastructure Owner:** Agent 99  
**AI Assistant:** GitHub Copilot  
**Environment:** hx.dev.local (Development/Test)  
**Support:** Internal team only

---

## 📚 Related Documentation

**Primary References:**
- [instructions.md](instructions.md) - AI assistant instructions (references this file)
- [lessons-learned.md](lessons-learned.md) - Migration project lessons

**Domain Migration:**
- [Domain-Migration/README.md](../tasks/Domain-Migration/README.md) - Migration overview
- [Domain-Migration/STATUS.md](../tasks/Domain-Migration/STATUS.md) - Current progress

**SSL/TLS:**
- [SSL-Certificate-Deployment.md](../configurations/SSL-Certificate-Deployment.md) - Certificate procedures
- [hx-ca-server-configuration.md](../configurations/hx-ca-server-configuration.md) - CA server config

**Server Configurations:**
- All configuration documents in `../configurations/` directory reference these credentials

---

## ⚖️ Legal & Compliance

**Environment Classification:** Development/Test  
**Data Sensitivity:** Medium (Infrastructure credentials)  
**Compliance Requirements:** None (non-production environment)  
**Encryption:** Not required (isolated dev environment)  
**Access Control:** Limited to authorized team members

**Production Note:** If this infrastructure is promoted to production, implement proper secrets management (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, etc.) and comply with organizational security policies.

---

**Document Version:** 1.4  
**Created:** October 22, 2025  
**Last Modified:** October 28, 2025  
**Classification:** Internal/Confidential  
**Retention:** Keep secure, rotate passwords if environment persists beyond 1 year  
**Recent Changes:** Added fastmcp service account (UID 1114201135), www-data system account (Qdrant UI), updated Server Access Matrix

---

*End of Credentials Document*
