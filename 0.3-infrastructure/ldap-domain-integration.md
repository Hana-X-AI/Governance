# LDAP/Domain Integration Procedures
**Purpose**: Create domain service accounts for all deployments
**Applies To**: Every service (PostgreSQL, Redis, Qdrant, N8N, etc.)
**When**: PRE-REQ-06 (CRITICAL - Never Defer)

---

## Overview

This procedure covers creating domain service accounts in Samba AD and integrating them with deployed services. **This is a mandatory prerequisite for all service deployments** and must never be deferred.

**What This Procedure Provides:**
- Domain user creation in Samba AD/DC
- SSSD integration for domain user visibility
- Service ownership migration to domain users
- LDAP/LDAPS connection configuration
- Testing and troubleshooting procedures

---

## Development Environment Notice

⚠️ **DEVELOPMENT ENVIRONMENT ONLY**

This procedure uses simplified security for hx.dev.local:
- Standard password: Major8859! (for all service accounts)
- Domain admin: Administrator@HX.DEV.LOCAL / Major3059!

**DO NOT** use these credentials in production environments.

**Credentials Reference**: `/srv/cc/Governance/0.2-credentials/hx-credentials.md`

---

## Prerequisites

**Required Access:**
- SSH to DC: `agent0@192.168.10.200` (Password: Major8859!)
- Domain Admin: `Administrator@HX.DEV.LOCAL` (Password: Major3059!)

**Required Information:**
- Service name (e.g., postgres, redis, qdrant, n8n, litellm)
- Service server IP (e.g., 192.168.10.209)
- Standard password: Major8859! (from credentials reference)

**Infrastructure:**
- Domain Controller: hx-dc-server.hx.dev.local (192.168.10.200)
- Realm: HX.DEV.LOCAL
- Base DN: dc=hx,dc=dev,dc=local

---

## Procedure: Create Service Account

### Step 1: SSH to Domain Controller

```bash
ssh agent0@192.168.10.200
# Password: Major8859!
```

### Step 2: Create Domain User

```bash
# Generic template - replace <SERVICE> with your service name
sudo samba-tool user create <SERVICE> 'Major8859!' \
  --description='<SERVICE-NAME> Service Account - Samba LDAP/DC' \
  --login-shell='/bin/bash' \
  --use-username-as-cn

# Examples:
sudo samba-tool user create postgres 'Major8859!' \
  --description='PostgreSQL Database Service Account - Samba LDAP/DC' \
  --login-shell='/bin/bash' \
  --use-username-as-cn

sudo samba-tool user create redis 'Major8859!' \
  --description='Redis Cache Service Account - Samba LDAP/DC' \
  --login-shell='/bin/bash' \
  --use-username-as-cn

sudo samba-tool user create qdrant 'Major8859!' \
  --description='Qdrant Vector DB Service Account - Samba LDAP/DC' \
  --login-shell='/bin/bash' \
  --use-username-as-cn

sudo samba-tool user create n8n 'Major8859!' \
  --description='N8N Workflow Automation Service Account - Samba LDAP/DC' \
  --login-shell='/bin/bash' \
  --use-username-as-cn
```

### Step 3: Verify User Creation

```bash
# On Domain Controller
sudo samba-tool user show <SERVICE>

# Expected output:
# dn: CN=<SERVICE>,CN=Users,DC=hx,DC=dev,DC=local
# userPrincipalName: <SERVICE>@hx.dev.local
# objectSid: S-1-5-21-xxxx-xxxx-xxxx-xxxx

# Verify from service server
ssh agent0@<SERVICE-IP>
id <SERVICE>@hx.dev.local

# Expected:
# uid=11142xxxxx(<SERVICE>@hx.dev.local) gid=1114200513(domain users@hx.dev.local)
```

### Exit Criteria

- ✅ User exists: `<SERVICE>@hx.dev.local`
- ✅ UID assigned (auto-generated, typically 1114201xxx)
- ✅ GID is 1114200513 (domain users)
- ✅ User visible on service server
- ✅ Password is Major8859!

---

## Domain User Management

### List All Domain Users

```bash
ssh agent0@192.168.10.200
sudo samba-tool user list

# Filter service accounts only
sudo samba-tool user list | grep -E "(postgres|redis|qdrant|n8n|litellm)"
```

### Show User Details

```bash
sudo samba-tool user show <SERVICE>

# Example output:
# dn: CN=postgres,CN=Users,DC=hx,DC=dev,DC=local
# cn: postgres
# sAMAccountName: postgres
# userPrincipalName: postgres@hx.dev.local
# objectSid: S-1-5-21-2514290708-4089471934-2416580579-1131
```

### Reset User Password

```bash
# If password needs to be reset to standard
sudo samba-tool user setpassword <SERVICE> --newpassword='Major8859!'
```

### Disable/Enable User

```bash
# Disable (decommissioned service)
sudo samba-tool user disable <SERVICE>

# Enable (reactivate)
sudo samba-tool user enable <SERVICE>
```

### Delete User

```bash
# Delete (use with caution - permanent)
sudo samba-tool user delete <SERVICE>
```

---

## LDAP/LDAPS Connection Information

### Connection Endpoints

| Protocol | Port | URL | Use Case |
|----------|------|-----|----------|
| LDAP | 389 | ldap://192.168.10.200:389 | Unencrypted (dev/testing) |
| LDAP | 389 | ldap://hx-dc-server.hx.dev.local:389 | Unencrypted (DNS) |
| LDAPS | 636 | ldaps://192.168.10.200:636 | Encrypted (production) |
| LDAPS | 636 | ldaps://hx-dc-server.hx.dev.local:636 | Encrypted (DNS) |

### Distinguished Names

```
Base DN:        dc=hx,dc=dev,dc=local
Users Container: CN=Users,DC=hx,DC=dev,DC=local

Bind DN Formats:
  UPN (recommended):  <SERVICE>@hx.dev.local
  DN:                CN=<SERVICE>,CN=Users,DC=hx,DC=dev,DC=local
```

---

## Service Integration on Target Server

**Complete integration checklist after domain user created:**

### 1. Verify Domain Membership

```bash
# On service server
ssh agent0@<SERVICE-IP>

# Check domain membership
sudo realm list
# Should show: hx.dev.local

# Test user visibility
id <SERVICE>@hx.dev.local
# Should show: uid=11142xxxxx(<SERVICE>@hx.dev.local) gid=1114200513(domain users@hx.dev.local)
```

### 2. Stop Service (if already running)

```bash
# SystemD service
sudo systemctl stop <service-name>

# Or manual stop
sudo -u <LOCAL-USER> <stop-command>
```

### 3. Change File Ownership

```bash
# Get domain GID
DOMAIN_GID=$(id -g <SERVICE>@hx.dev.local)

# Change ownership of all service files
sudo chown -R <SERVICE>@hx.dev.local:$DOMAIN_GID /path/to/service/data
sudo chown -R <SERVICE>@hx.dev.local:$DOMAIN_GID /path/to/service/config
sudo chown -R <SERVICE>@hx.dev.local:$DOMAIN_GID /path/to/service/logs
sudo chown -R <SERVICE>@hx.dev.local:$DOMAIN_GID /path/to/service/binaries

# Examples:
# PostgreSQL:
# sudo chown -R postgres@hx.dev.local:1114200513 /srv/postgres/data/pgdata17
# sudo chown -R postgres@hx.dev.local:1114200513 /usr/local/pgsql

# Qdrant:
# sudo chown -R qdrant@hx.dev.local:1114200513 /opt/qdrant/storage
# sudo chown -R qdrant@hx.dev.local:1114200513 /opt/qdrant/config

# Redis:
# sudo chown -R redis@hx.dev.local:1114200513 /var/lib/redis
# sudo chown -R redis@hx.dev.local:1114200513 /etc/redis
```

### 4. Create Home Directory

```bash
sudo mkdir -p /home/<SERVICE>@hx.dev.local
sudo chown <SERVICE>@hx.dev.local:$DOMAIN_GID /home/<SERVICE>@hx.dev.local
sudo chmod 700 /home/<SERVICE>@hx.dev.local
```

### 5. Update SystemD Service (if applicable)

```bash
sudo systemctl edit --full <service-name>

# Update User and Group:
[Service]
User=<SERVICE>@hx.dev.local
Group=domain users@hx.dev.local

# Save and reload
sudo systemctl daemon-reload
```

### 6. Start Service as Domain User

```bash
sudo systemctl start <service-name>

# Or manual start:
sudo -u <SERVICE>@hx.dev.local <start-command>
```

### 7. Verify Service Running

```bash
# Check process owner
ps aux | grep <service>
# Should show: <SERVICE>@hx.dev.local

# Check service status
sudo systemctl status <service-name>
```

---

## Testing LDAP/LDAPS Connections

### Install LDAP Utilities

```bash
sudo apt install -y ldap-utils
```

### Test LDAP (Unencrypted)

```bash
# Anonymous bind (will fail - auth required)
ldapsearch -x -H ldap://192.168.10.200 -b "dc=hx,dc=dev,dc=local" -LLL

# Authenticated bind
ldapsearch -x -H ldap://192.168.10.200 \
  -D "<SERVICE>@hx.dev.local" \
  -w 'Major8859!' \
  -b "dc=hx,dc=dev,dc=local" \
  -LLL "(objectClass=user)" sAMAccountName

# Search for specific user
ldapsearch -x -H ldap://192.168.10.200 \
  -D "Administrator@hx.dev.local" \
  -w 'Major3059!' \
  -b "CN=Users,DC=hx,DC=dev,DC=local" \
  -LLL "(userPrincipalName=<SERVICE>@hx.dev.local)"
```

### Test LDAPS (Encrypted)

```bash
# Test SSL certificate
echo | openssl s_client -connect 192.168.10.200:636 -CAfile /etc/samba/tls/ca.crt

# LDAPS query (skip cert verification - dev only)
LDAPTLS_REQCERT=never ldapsearch -x -H ldaps://192.168.10.200 \
  -D "<SERVICE>@hx.dev.local" \
  -w 'Major8859!' \
  -b "dc=hx,dc=dev,dc=local" \
  -LLL "(objectClass=domain)" dn

# LDAPS query (with cert verification - production)
ldapsearch -x -H ldaps://192.168.10.200 \
  -D "<SERVICE>@hx.dev.local" \
  -w 'Major8859!' \
  -b "dc=hx,dc=dev,dc=local" \
  -LLL "(objectClass=domain)" dn
```

### Test from Remote Server

```bash
# From any domain-joined server
ssh agent0@<ANY-SERVER-IP>

ldapsearch -x -H ldap://192.168.10.200 \
  -D "<SERVICE>@hx.dev.local" \
  -w 'Major8859!' \
  -b "dc=hx,dc=dev,dc=local" \
  -LLL "(userPrincipalName=<SERVICE>@hx.dev.local)" dn

# Expected: dn: CN=<SERVICE>,CN=Users,DC=hx,DC=dev,DC=local
```

---

## Application Configuration Examples

### Generic LDAP Configuration

```yaml
ldap:
  url: "ldap://192.168.10.200:389"
  base_dn: "dc=hx,dc=dev,dc=local"
  bind_dn: "<SERVICE>@hx.dev.local"
  bind_password: "Major8859!"
  user_search_base: "CN=Users,DC=hx,DC=dev,DC=local"
  user_search_filter: "(userPrincipalName={0})"
```

### Generic LDAPS Configuration

```yaml
ldaps:
  url: "ldaps://192.168.10.200:636"
  base_dn: "dc=hx,dc=dev,dc=local"
  bind_dn: "<SERVICE>@hx.dev.local"
  bind_password: "Major8859!"
  tls_verify: false  # Dev: false, Prod: true
  ca_cert_file: "/etc/ssl/certs/ca.crt"
```

### PostgreSQL pg_hba.conf

```conf
# LDAP authentication
host all all 192.168.10.0/24 ldap ldapserver=192.168.10.200 ldapbasedn="dc=hx,dc=dev,dc=local" ldapsearchattribute=userPrincipalName

# LDAPS authentication
hostssl all all 192.168.10.0/24 ldap ldapserver=192.168.10.200 ldapport=636 ldaptls=1 ldapbasedn="dc=hx,dc=dev,dc=local" ldapsearchattribute=userPrincipalName
```

### Python LDAP

```python
import ldap

ldap_url = "ldap://192.168.10.200:389"
bind_dn = "<service>@hx.dev.local"
bind_password = "Major8859!"
base_dn = "dc=hx,dc=dev,dc=local"

conn = ldap.initialize(ldap_url)
conn.simple_bind_s(bind_dn, bind_password)

# Search
search_filter = "(userPrincipalName=<service>@hx.dev.local)"
results = conn.search_s(base_dn, ldap.SCOPE_SUBTREE, search_filter)
conn.unbind()
```

### Node.js LDAP

```javascript
const ldap = require('ldapjs');

const client = ldap.createClient({
  url: 'ldap://192.168.10.200:389'
});

client.bind('<service>@hx.dev.local', 'Major8859!', (err) => {
  if (err) {
    console.error('Bind failed:', err);
  } else {
    console.log('Bind successful');
  }
});
```

---

## Common LDAP Search Filters

### Search by Username

```bash
"(sAMAccountName=<username>)"
"(userPrincipalName=<username>@hx.dev.local)"
```

### Search All Users

```bash
"(objectClass=user)"
"(&(objectClass=user)(!(objectClass=computer)))"
```

### Search Service Accounts

```bash
"(&(objectClass=user)(description=*Service Account*))"
```

### Search Enabled Accounts

```bash
"(&(objectClass=user)(!(userAccountControl:1.2.840.113556.1.4.803:=2)))"
```

---

## Installing CA Certificate for LDAPS

### Download from DC

```bash
# From service server
scp agent0@192.168.10.200:/etc/samba/tls/ca.crt /tmp/ca.crt

# Install to system trust store
sudo cp /tmp/ca.crt /usr/local/share/ca-certificates/hx-dev-local-ca.crt
sudo update-ca-certificates

# Verify
ls -la /etc/ssl/certs/ | grep hx-dev
```

### Alternative - From CA Server

```bash
scp agent0@192.168.10.201:~/easy-rsa-pki/pki/ca.crt /tmp/hx-ca.crt
sudo cp /tmp/hx-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

---

## Troubleshooting LDAP Integration

### Issue: User Not Visible on Service Server

```bash
# Problem: id username@hx.dev.local returns "no such user"

# Check domain membership
sudo realm list  # Should show hx.dev.local

# Check SSSD
sudo systemctl status sssd
sudo systemctl restart sssd

# Clear SSSD cache
sudo sss_cache -E
sudo systemctl restart sssd

# Test DNS
nslookup hx-dc-server.hx.dev.local  # Should: 192.168.10.200

# Test connectivity
ping -c 3 192.168.10.200
telnet 192.168.10.200 389
```

### Issue: LDAP Bind Fails

```bash
# Verify credentials
sudo samba-tool user show <username>  # On DC

# Test authentication
ldapwhoami -x -H ldap://192.168.10.200 \
  -D "<username>@hx.dev.local" \
  -w 'Major8859!'
# Should return: dn:CN=<username>,CN=Users,DC=hx,DC=dev,DC=local

# Check account status
sudo samba-tool user show <username> | grep userAccountControl
```

### Issue: Permission Denied After Migration

```bash
# Check ownership
ls -la /path/to/service/data
# Should show: username@hx.dev.local domain users@hx.dev.local

# Fix ownership
sudo chown -R username@hx.dev.local:domain\ users /path/to/service

# Check permissions
sudo chmod 755 /path/to/service
sudo chmod 700 /path/to/service/data

# Test access
sudo -u username@hx.dev.local ls -la /path/to/service/data
```

---

## Service Account Registry

### Current Domain Users

| Username | UPN | UID | GID | Purpose | Created |
|----------|-----|-----|-----|---------|---------|
| postgres | postgres@hx.dev.local | 1114201131 | 1114200513 | PostgreSQL Database | 2025-10-25 |
| qdrant | qdrant@hx.dev.local | 1114201130 | 1114200513 | Qdrant Vector DB | 2025-10-24 |
| redis | redis@hx.dev.local | 1114201132 | 1114200513 | Redis Cache | 2025-10-27 |
| fastmcp | fastmcp@hx.dev.local | 1114201135 | 1114200513 | FastMCP MCP Server | 2025-10-28 |
| n8n | n8n@hx.dev.local | TBD | 1114200513 | N8N Workflow | TBD |
| litellm | litellm@hx.dev.local | TBD | 1114200513 | LiteLLM Proxy | TBD |

### Standard for All Services

- GID: 1114200513 (domain users@hx.dev.local)
- Password: Major8859!
- Shell: /bin/bash
- UID: Auto-assigned by Samba (typically 1114201xxx)

---

## Related Procedures

- **DNS Management**: `/srv/cc/Governance/0.3-infrastructure/dns-management.md`
- **SSL/TLS Deployment**: `/srv/cc/Governance/0.3-infrastructure/ssl-tls-deployment.md`
- **Credentials Reference**: `/srv/cc/Governance/0.2-credentials/hx-credentials.md`

---

## Document Metadata

**Created**: 2025-11-05
**Status**: Active - Production Ready
**Applies To**: ALL service deployments in hx.dev.local
**Referenced By**: All 30 service owner agents
