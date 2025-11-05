# DNS Management Procedures
**Purpose**: Register service hostnames in domain DNS
**Applies To**: Every service requiring network access
**When**: DEPLOY-09 or Post-Deployment

---

## Overview

This procedure covers DNS record management in the hx.dev.local domain using samba-tool. All DNS operations are performed on the Domain Controller which acts as the authoritative DNS server for the domain.

**What This Procedure Provides:**
- DNS A record creation and management
- CNAME (alias) record creation
- DNS record verification and troubleshooting
- Standard naming conventions
- DNS resolution testing

---

## Development Environment Notice

⚠️ **DEVELOPMENT ENVIRONMENT ONLY**

This procedure uses simplified security for hx.dev.local:
- Domain admin: Administrator@HX.DEV.LOCAL / Major3059!
- SSH access: agent0@192.168.10.200 / Major8859!

**DO NOT** use these credentials in production environments.

**Credentials Reference**: `/srv/cc/Governance/0.2-credentials/hx-credentials.md`

---

## Prerequisites

**Required Access:**
- SSH to DC: `agent0@192.168.10.200` (Password: Major8859!)
- Domain Admin: `administrator` (Password: Major3059!)

**Required Information:**
- Service hostname (e.g., hx-postgres, hx-redis, hx-qdrant-ui)
- Service IP address (e.g., 192.168.10.209)

**DNS Infrastructure:**
- DNS Server: Samba AD DC (192.168.10.200)
- Domain: hx.dev.local
- Tool: samba-tool dns

---

## Procedure: Add DNS Record

### Step 1: SSH to Domain Controller

```bash
ssh agent0@192.168.10.200
# Password: Major8859!
```

### Step 2: Add DNS A Record

```bash
# Generic template
sudo samba-tool dns add localhost hx.dev.local <HOSTNAME> A <IP-ADDRESS> -U administrator
# sudo password: Major8859!
# administrator password: Major3059!

# Examples:
sudo samba-tool dns add localhost hx.dev.local hx-postgres A 192.168.10.209 -U administrator
sudo samba-tool dns add localhost hx.dev.local hx-redis A 192.168.10.210 -U administrator
sudo samba-tool dns add localhost hx.dev.local hx-qdrant-ui A 192.168.10.208 -U administrator
sudo samba-tool dns add localhost hx.dev.local hx-n8n A 192.168.10.211 -U administrator
```

**Expected Output:**
```
[sudo] password for agent0: Major8859!
WARNING: Using passwords on command line is insecure.
Password for [HX\administrator]: Major3059!
Record added successfully
```

### Step 3: Verify DNS Record

```bash
sudo samba-tool dns query localhost hx.dev.local <HOSTNAME> A -U administrator
# administrator password: Major3059!

# Expected output:
#   Name=, Records=1, Children=0
#     A: <IP-ADDRESS> (flags=f0, serial=X, ttl=900)
```

---

## DNS Operations

### Verify Record

```bash
sudo samba-tool dns query localhost hx.dev.local <HOSTNAME> A -U administrator
```

### Update Record (Delete + Add)

```bash
# Delete old
sudo samba-tool dns delete localhost hx.dev.local <HOSTNAME> A <OLD-IP> -U administrator

# Add new
sudo samba-tool dns add localhost hx.dev.local <HOSTNAME> A <NEW-IP> -U administrator

# Verify
sudo samba-tool dns query localhost hx.dev.local <HOSTNAME> A -U administrator
```

### Delete Record

```bash
sudo samba-tool dns delete localhost hx.dev.local <HOSTNAME> A <IP-ADDRESS> -U administrator
```

### List All DNS Records

```bash
# List zones
sudo samba-tool dns zonelist localhost -U administrator

# View zone records
sudo samba-tool dns query localhost hx.dev.local @ ALL -U administrator
```

---

## DNS Record Types

### A Record (Most Common)

```bash
# Map hostname to IPv4 address
sudo samba-tool dns add localhost hx.dev.local <HOSTNAME> A <IP> -U administrator
```

### CNAME Record (Alias)

```bash
# Create alias for existing hostname
sudo samba-tool dns add localhost hx.dev.local <ALIAS> CNAME <TARGET>.hx.dev.local. -U administrator

# Example: Short alias for service
sudo samba-tool dns add localhost hx.dev.local postgres CNAME hx-postgres.hx.dev.local. -U administrator
```

---

## Standard Naming Conventions

### Server Hostnames

```
Pattern: hx-<service>-server
Examples:
  - hx-postgres-server.hx.dev.local
  - hx-redis-server.hx.dev.local
  - hx-qdrant-server.hx.dev.local
  - hx-n8n-server.hx.dev.local
```

### Service Hostnames

```
Pattern: hx-<service>
Examples:
  - hx-postgres.hx.dev.local
  - hx-redis.hx.dev.local
  - hx-qdrant-ui.hx.dev.local
  - hx-n8n.hx.dev.local
```

### Short Aliases (Optional)

```
Pattern: <service>
Examples:
  - postgres.hx.dev.local → hx-postgres.hx.dev.local
  - redis.hx.dev.local → hx-redis.hx.dev.local
```

---

## Common DNS Patterns

### Pattern 1: Server + Service Hostname

```bash
# Server hostname (created during domain join)
# hx-postgres-server.hx.dev.local → 192.168.10.209

# Add service-specific alias
sudo samba-tool dns add localhost hx.dev.local hx-postgres A 192.168.10.209 -U administrator
# Now accessible as: hx-postgres.hx.dev.local
```

### Pattern 2: Multiple Services, Same Server

```bash
# PostgreSQL + pgAdmin on same server (192.168.10.209)
sudo samba-tool dns add localhost hx.dev.local hx-postgres A 192.168.10.209 -U administrator
sudo samba-tool dns add localhost hx.dev.local hx-pgadmin A 192.168.10.209 -U administrator
```

### Pattern 3: Service with Multiple Endpoints

```bash
# Qdrant API + Web UI (separate servers)
sudo samba-tool dns add localhost hx.dev.local hx-qdrant A 192.168.10.207 -U administrator
sudo samba-tool dns add localhost hx.dev.local hx-qdrant-ui A 192.168.10.208 -U administrator
```

---

## Testing DNS Resolution

### Test from Domain Controller

```bash
# Query DNS
nslookup <HOSTNAME>.hx.dev.local 192.168.10.200

# Expected:
# Server:     192.168.10.200
# Address:    192.168.10.200#53
# Name:   <HOSTNAME>.hx.dev.local
# Address: <IP-ADDRESS>
```

### Test from Any Domain Server

```bash
ssh agent0@<ANY-SERVER-IP>

# Test resolution
nslookup <HOSTNAME>.hx.dev.local

# Test connectivity
ping -c 3 <HOSTNAME>.hx.dev.local

# Test service access
curl http://<HOSTNAME>.hx.dev.local/
# Or appropriate service test
```

---

## DNS Propagation

### Within hx.dev.local

- Changes are **immediate** (no waiting)
- All domain servers query DC directly
- TTL is 900 seconds (15 minutes) but effective immediately

### Verify Propagation

```bash
# From multiple servers
ssh agent0@192.168.10.207
nslookup <HOSTNAME>.hx.dev.local

ssh agent0@192.168.10.208
nslookup <HOSTNAME>.hx.dev.local
```

---

## Troubleshooting DNS

### Issue: Record Not Resolving

```bash
# Symptoms: nslookup returns NXDOMAIN

# 1. Check record exists on DC
ssh agent0@192.168.10.200
sudo samba-tool dns query localhost hx.dev.local <HOSTNAME> A -U administrator

# 2. Check DNS server on client
cat /etc/resolv.conf
# Should contain: nameserver 192.168.10.200

# 3. Test direct query to DC
nslookup <HOSTNAME>.hx.dev.local 192.168.10.200

# 4. Check domain join
sudo realm list
```

### Issue: Wrong IP Resolving

```bash
# Fix: Delete old, add new
sudo samba-tool dns delete localhost hx.dev.local <HOSTNAME> A <WRONG-IP> -U administrator
sudo samba-tool dns add localhost hx.dev.local <HOSTNAME> A <CORRECT-IP> -U administrator
```

### Issue: Multiple IPs for Same Hostname

```bash
# Diagnose
sudo samba-tool dns query localhost hx.dev.local <HOSTNAME> A -U administrator
# Shows: Records=2 or more

# Delete unwanted
sudo samba-tool dns delete localhost hx.dev.local <HOSTNAME> A <UNWANTED-IP> -U administrator
```

### Issue: Changes Not Taking Effect

```bash
# Clear client DNS cache
sudo systemd-resolve --flush-caches
sudo systemctl restart systemd-resolved

# Test with dig (bypasses cache)
dig @192.168.10.200 <HOSTNAME>.hx.dev.local

# Restart SSSD
sudo systemctl restart sssd
```

---

## DNS Best Practices

### 1. Always Verify

```bash
# After adding/updating/deleting
sudo samba-tool dns query localhost hx.dev.local <HOSTNAME> A -U administrator
```

### 2. Use Consistent Naming

- Server: `hx-<service>-server`
- Service: `hx-<service>`
- Alias: `<service>` (short form)

### 3. Document Changes

Update service configuration documentation immediately after DNS changes.

### 4. Test Before and After

```bash
# Before: Should not exist
nslookup <HOSTNAME>.hx.dev.local  # NXDOMAIN

# After: Should resolve
nslookup <HOSTNAME>.hx.dev.local  # Returns IP
```

### 5. Use Hostnames in Configuration

Prefer `hx-postgres.hx.dev.local` over `192.168.10.209` in configs for flexibility and maintainability.

---

## Quick Reference Commands

### Add Record
```bash
ssh agent0@192.168.10.200
sudo samba-tool dns add localhost hx.dev.local <HOSTNAME> A <IP> -U administrator
# Password: Major3059!
```

### Verify Record
```bash
sudo samba-tool dns query localhost hx.dev.local <HOSTNAME> A -U administrator
```

### Test Resolution
```bash
nslookup <HOSTNAME>.hx.dev.local
ping <HOSTNAME>.hx.dev.local
```

---

## Related Procedures

- **LDAP Integration**: `/srv/cc/Governance/0.3-infrastructure/ldap-domain-integration.md`
- **SSL/TLS Deployment**: `/srv/cc/Governance/0.3-infrastructure/ssl-tls-deployment.md`
- **Credentials Reference**: `/srv/cc/Governance/0.2-credentials/hx-credentials.md`

---

## Document Metadata

**Created**: 2025-11-05
**Status**: Active - Production Ready
**Applies To**: ALL service deployments in hx.dev.local
**Referenced By**: All 30 service owner agents
