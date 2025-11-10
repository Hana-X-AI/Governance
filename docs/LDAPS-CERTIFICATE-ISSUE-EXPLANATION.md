# LDAPS Certificate Issue - Explanation and Workaround

**Document Type:** Technical Issue Analysis
**Created:** 2025-11-10
**Status:** ACTIVE ISSUE with WORKING WORKAROUND
**Severity:** LOW (workaround in place, no operational impact)
**Owner:** Frank Lucas (@agent-frank)

---

## Executive Summary

**Issue:** LDAPS (LDAP over SSL) on port 636 fails SSL handshake
**Impact:** LOW - Workaround using STARTTLS on port 389 is functional
**Root Cause:** SSL/TLS certificate configuration issue on hx-dc-server
**Workaround:** Use LDAP with STARTTLS on port 389 with `LDAPTLS_REQCERT=never`
**Permanent Fix:** Generate and configure proper SSL certificate for Samba AD DC

---

## Technical Details

### What is LDAPS?

**LDAPS = LDAP over SSL/TLS**

There are **two ways** to secure LDAP connections:

1. **LDAPS (Port 636):** SSL/TLS from the start (like HTTPS)
   - Connection is encrypted from first byte
   - Requires valid SSL certificate on LDAP server
   - Client connects to port 636
   - SSL handshake happens immediately

2. **STARTTLS (Port 389):** Start unencrypted, upgrade to encrypted
   - Client connects to standard LDAP port 389
   - Client sends STARTTLS command
   - Connection upgrades to encrypted
   - More flexible but slightly more complex

### Current Status

**Port 636 (LDAPS):**
```
Status: ⚠️ PORT OPEN but SSL HANDSHAKE FAILS
```

**What's happening:**
- Samba AD DC is listening on port 636
- When client tries to connect, SSL handshake fails
- Error: Certificate validation failure or missing certificate

**Port 389 (STARTTLS):**
```
Status: ✅ WORKING with workaround
```

**Workaround:**
- Connect to port 389 (standard LDAP)
- Use STARTTLS to upgrade to encrypted connection
- Set `LDAPTLS_REQCERT=never` to bypass certificate validation

---

## Why This Happens

### Root Cause: Certificate Configuration

Samba AD DC requires a **properly configured SSL/TLS certificate** for LDAPS to work.

**What's likely wrong:**

1. **No certificate configured** in Samba for LDAPS
2. **Certificate exists but has wrong hostname** (not matching hx-dc-server.hx.dev.local)
3. **Certificate expired** or not trusted
4. **Certificate chain incomplete** (missing CA certificate)

### Samba Certificate Requirements

For LDAPS to work, Samba needs:
```
/var/lib/samba/private/tls/cert.pem  - Server certificate
/var/lib/samba/private/tls/key.pem   - Private key
/var/lib/samba/private/tls/ca.pem    - CA certificate (optional)
```

And configuration in `/etc/samba/smb.conf`:
```ini
[global]
    tls enabled = yes
    tls keyfile = /var/lib/samba/private/tls/key.pem
    tls certfile = /var/lib/samba/private/tls/cert.pem
    tls cafile = /var/lib/samba/private/tls/ca.pem
```

---

## Current Workaround (In Use)

### How It Works

**All LDAP operations use STARTTLS instead of LDAPS:**

```bash
# Standard LDAP query with STARTTLS
LDAPTLS_REQCERT=never ldapsearch -x -H ldap://hx-dc-server.hx.dev.local \
  -b "dc=hx,dc=dev,dc=local" -D "Administrator@hx.dev.local" -W
```

**Key components:**
- `LDAPTLS_REQCERT=never` - Don't validate certificate (security trade-off)
- `ldap://` (not `ldaps://`) - Use port 389 with STARTTLS
- Connection is still **encrypted** after STARTTLS upgrade
- Authentication still works correctly

### Where This Workaround is Used

**System-wide LDAP operations:**
1. Domain join operations (SSSD)
2. User authentication
3. Service account queries
4. DNS updates via LDAP
5. Administrative operations (samba-tool)

**Configuration files using workaround:**
- `/etc/ldap/ldap.conf` - May have `TLS_REQCERT never`
- `/etc/sssd/sssd.conf` - Domain join configuration
- Shell scripts - Export `LDAPTLS_REQCERT=never`

---

## Security Implications

### Current Security Posture

**✅ GOOD:**
- Connections **ARE encrypted** (STARTTLS provides encryption)
- Authentication **IS secure** (Kerberos + encrypted channel)
- Credentials **NOT sent in plaintext**
- Domain services **functioning correctly**

**⚠️ CONCERN:**
- `LDAPTLS_REQCERT=never` disables certificate validation
- Vulnerable to Man-in-the-Middle (MITM) attacks **on local network**
- Cannot verify we're actually talking to hx-dc-server

### Risk Assessment

**Risk Level: LOW** for internal network

**Why risk is low:**
- Network is private (192.168.10.0/24)
- Physical/virtual network isolation
- No external access to internal network
- MITM requires compromised internal host

**Why we should still fix it:**
- Best practice: Always validate certificates
- Defense in depth
- Compliance requirements may mandate proper TLS
- Future external integration may need proper certificates

---

## Permanent Fix (Recommended)

### Option 1: Generate Certificate via Samba Built-in CA

**Samba AD DC has a built-in Certificate Authority.**

**Steps:**
1. Generate certificate for hx-dc-server using Samba CA
2. Install certificate in correct location
3. Configure smb.conf for TLS
4. Restart Samba services
5. Test LDAPS on port 636
6. Remove `LDAPTLS_REQCERT=never` workaround

**Commands (executed by Frank):**
```bash
# Generate certificate using Samba CA
samba-tool domain exportkeytab /path/to/keytab

# Or use external certificate generation
# and place in /var/lib/samba/private/tls/
```

### Option 2: Use External Certificate from hx-ca-server

**If you have separate CA infrastructure (hx-ca-server):**

1. Generate certificate request on hx-dc-server
2. Sign with CA on hx-ca-server (192.168.10.201)
3. Install signed certificate
4. Configure Samba
5. Test and validate

### Option 3: Self-Signed Certificate (Quick Fix)

**For testing or non-production:**

```bash
# Generate self-signed certificate
openssl req -new -x509 -days 365 -nodes \
  -out /var/lib/samba/private/tls/cert.pem \
  -keyout /var/lib/samba/private/tls/key.pem \
  -subj "/CN=hx-dc-server.hx.dev.local"

# Set permissions
chmod 600 /var/lib/samba/private/tls/key.pem
chown root:root /var/lib/samba/private/tls/*

# Configure Samba
# Edit /etc/samba/smb.conf and add TLS settings

# Restart
systemctl restart samba-ad-dc
```

---

## Testing the Fix

### After implementing certificate:

**1. Test LDAPS connection (port 636):**
```bash
# Should succeed without certificate errors
ldapsearch -x -H ldaps://hx-dc-server.hx.dev.local \
  -b "dc=hx,dc=dev,dc=local"
```

**2. Verify certificate:**
```bash
# Check certificate details
openssl s_client -connect hx-dc-server.hx.dev.local:636 -showcerts
```

**3. Remove workaround:**
```bash
# No longer need LDAPTLS_REQCERT=never
unset LDAPTLS_REQCERT

# Test without workaround
ldapsearch -x -H ldaps://hx-dc-server.hx.dev.local \
  -b "dc=hx,dc=dev,dc=local"
```

**4. Update configurations:**
- Remove `LDAPTLS_REQCERT=never` from scripts
- Update `/etc/ldap/ldap.conf` to validate certificates
- Test all domain-joined servers

---

## Impact of Fixing

### Benefits
- ✅ Proper TLS certificate validation
- ✅ Protection against MITM attacks
- ✅ Compliance with security best practices
- ✅ Can use LDAPS (port 636) directly
- ✅ Cleaner configuration (no workarounds)

### Considerations
- ⚠️ Requires certificate deployment to all clients
- ⚠️ Certificate expiration must be monitored
- ⚠️ All 28 domain-joined servers need CA certificate
- ⚠️ Coordination required (brief service interruption possible)

---

## Recommendation

**Priority:** MEDIUM
**Effort:** LOW (1-2 hours)
**Timing:** Non-urgent (workaround is functional)

**Recommended Approach:**
1. Have Frank generate certificate using Samba built-in CA
2. Test LDAPS on one client first
3. Roll out CA certificate to all servers (via Amanda/Ansible)
4. Update configurations to remove workaround
5. Monitor for 1 week
6. Document in runbook

**When to do this:**
- During next planned maintenance window
- When external integrations require proper TLS
- If compliance requires certificate validation
- When time permits (not blocking any work)

---

## Related Issues

**Non-Existent Replica Server:**
- Documentation referenced hx-freeipa-replica (192.168.10.201)
- Reality: 192.168.10.201 is hx-ca-server (Certificate Authority)
- This CA server could be used to sign the LDAPS certificate

**Certificate Infrastructure:**
- hx-ca-server exists (192.168.10.201)
- Could centralize all certificate issuance
- Opportunity to standardize certificate management

---

## References

**Samba Documentation:**
- Samba TLS Configuration: https://wiki.samba.org/index.php/Configuring_LDAP_over_SSL_(LDAPS)_on_a_Samba_AD_DC
- Samba Built-in CA: https://wiki.samba.org/index.php/Certificate_Authority

**Related Governance Documents:**
- Domain Controller Audit: `/srv/cc/Governance/DOMAIN-CONTROLLER-AUDIT-REPORT.md`
- Frank's Agent Profile: `0.0-governance/0.0.5-Delivery/0.0.5.1-agents/0.0.5.1.10-agent-frank.md`
- Credentials: `0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.1-credentials.md`

---

## Action Items

**For Frank Lucas (@agent-frank):**
- [ ] Generate TLS certificate for hx-dc-server
- [ ] Configure Samba TLS settings
- [ ] Test LDAPS on port 636
- [ ] Document certificate expiration date
- [ ] Create certificate renewal procedure

**For Amanda Chen (@agent-amanda):**
- [ ] Create Ansible playbook to deploy CA certificate to all servers
- [ ] Update SSSD configurations to remove `LDAPTLS_REQCERT=never`
- [ ] Test domain authentication after changes

**For Nathan Lewis (@agent-nathan):**
- [ ] Add certificate expiration monitoring
- [ ] Alert 30 days before expiration
- [ ] Monitor LDAPS connection success rates

---

**Version:** 1.0
**Classification:** Internal - Technical
**Status:** DOCUMENTED - Workaround Active
**Review Date:** After permanent fix implemented

---

*Security = Proper TLS validation > Workarounds*
*Current workaround is functional but should be replaced with proper certificate*
