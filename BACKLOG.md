# Hana-X Project Backlog

**Project:** Hana-X Multi-Agent Infrastructure Platform
**Location:** `/srv/cc/Governance/`
**Maintained By:** Agent Zero
**Last Updated:** 2025-11-10

---

## Backlog Overview

This document tracks all identified work items, technical debt, and future improvements for the Hana-X infrastructure. Items are prioritized and categorized for systematic resolution.

**Status Legend:**
- 🔴 **Blocked** - Cannot proceed due to dependency
- 🟡 **Ready** - Can be worked on
- 🟢 **In Progress** - Actively being worked
- ✅ **Completed** - Done and validated

---

## High Priority Items

### None Currently

---

## Medium Priority Items

### LDAPS-001: Fix LDAPS Certificate Configuration

**Status:** 🟡 Ready
**Priority:** MEDIUM
**Severity:** LOW (workaround in place)
**Owner:** Frank Lucas (@agent-frank)
**Effort:** 1-2 hours
**Timing:** Next maintenance window (non-blocking)

#### The Issue

**Problem:** Port 636 (LDAPS) SSL handshake fails
**Current Status:** Working workaround in place
**Operational Impact:** None (services functioning normally)

#### What's Actually Happening

**Port 636 (LDAPS):** ⚠️ Open but SSL handshake fails
- Missing or misconfigured TLS certificate
- Samba AD DC not configured with proper certificate paths
- Certificate may not match hostname (hx-dc-server.hx.dev.local)

**Port 389 (STARTTLS):** ✅ WORKING with workaround
- Uses `LDAPTLS_REQCERT=never` to bypass certificate validation
- Connection IS still encrypted (STARTTLS upgrades to TLS)
- All authentication works correctly
- All 28 domain-joined servers using this method

#### Security Assessment

**Current State:**
- ✅ Connections are encrypted (STARTTLS provides TLS encryption)
- ✅ Authentication is secure (Kerberos + encrypted channel)
- ✅ Credentials NOT sent in plaintext
- ⚠️ Certificate validation disabled (accepts any certificate)
- ⚠️ Vulnerable to Man-in-the-Middle (MITM) attacks on local network

**Risk Level:** **LOW**
- Internal network only (192.168.10.0/24 - private subnet)
- No external access to domain controller
- MITM attack requires compromised internal host
- Physical/virtual network isolation in place

**Why we should still fix it:**
- Best practice: Always validate TLS certificates
- Defense in depth security posture
- Future compliance requirements may mandate proper TLS
- External integrations may require certificate validation
- Eliminates technical debt and workarounds

#### The Fix Options

**Option 1: Generate certificate via Samba built-in CA** ⭐ RECOMMENDED
- Samba AD DC includes built-in Certificate Authority
- Generate certificate for hx-dc-server.hx.dev.local
- Place in `/var/lib/samba/private/tls/`
- Configure in `/etc/samba/smb.conf`
- Restart Samba services
- **Pros:** Uses existing infrastructure, well-documented
- **Cons:** Certificate only trusted by domain members

**Option 2: Use external certificate from hx-ca-server**
- Generate CSR on hx-dc-server
- Sign with CA on hx-ca-server (192.168.10.201)
- Install signed certificate
- Configure Samba
- Deploy CA certificate to all clients
- **Pros:** Centralized CA management, trusted across infrastructure
- **Cons:** More complex, requires coordination with hx-ca-server

**Option 3: Self-signed certificate** ⚠️ NOT RECOMMENDED
- Quick fix for testing only
- Not suitable for production
- Still requires client trust configuration
- **Use case:** Testing LDAPS functionality only

#### Implementation Steps

**Phase 1: Generate Certificate (Frank)**
1. Choose Option 1 or Option 2 above
2. Generate TLS certificate for hx-dc-server.hx.dev.local
3. Install certificate files:
   - `/var/lib/samba/private/tls/cert.pem`
   - `/var/lib/samba/private/tls/key.pem`
   - `/var/lib/samba/private/tls/ca.pem` (if using Option 2)
4. Set permissions: `chmod 600 key.pem`, `chown root:root *`

**Phase 2: Configure Samba (Frank)**
1. Edit `/etc/samba/smb.conf`:
   ```ini
   [global]
       tls enabled = yes
       tls keyfile = /var/lib/samba/private/tls/key.pem
       tls certfile = /var/lib/samba/private/tls/cert.pem
       tls cafile = /var/lib/samba/private/tls/ca.pem
   ```
2. Restart Samba: `systemctl restart samba-ad-dc`
3. Verify service starts without errors

**Phase 3: Test LDAPS (Frank)**
1. Test from hx-dc-server:
   ```bash
   ldapsearch -x -H ldaps://hx-dc-server.hx.dev.local \
     -b "dc=hx,dc=dev,dc=local"
   ```
2. Test from remote server:
   ```bash
   # Should work without LDAPTLS_REQCERT=never
   ldapsearch -x -H ldaps://hx-dc-server.hx.dev.local \
     -b "dc=hx,dc=dev,dc=local" -D "Administrator@hx.dev.local" -W
   ```
3. Verify certificate details:
   ```bash
   openssl s_client -connect hx-dc-server.hx.dev.local:636 -showcerts
   ```

**Phase 4: Deploy to Clients (Amanda)**
1. Create Ansible playbook to deploy CA certificate to all 28 servers
2. Update `/etc/ldap/ldap.conf` to remove `TLS_REQCERT never`
3. Update `/etc/sssd/sssd.conf` if needed
4. Test domain authentication on each server
5. Monitor for authentication failures

**Phase 5: Remove Workaround (Frank + Amanda)**
1. Remove `LDAPTLS_REQCERT=never` from scripts
2. Update documentation to remove workaround references
3. Test all LDAP operations without workaround
4. Monitor for 1 week

**Phase 6: Monitoring (Nathan)**
1. Add certificate expiration monitoring
2. Alert 30 days before expiration
3. Monitor LDAPS connection success rates
4. Create renewal procedure

#### Success Criteria

- [ ] LDAPS (port 636) accepts connections without errors
- [ ] Certificate validates correctly (no warnings)
- [ ] All 28 servers can authenticate via LDAPS
- [ ] `LDAPTLS_REQCERT=never` removed from all configurations
- [ ] Certificate expiration monitoring in place
- [ ] Documentation updated to reflect proper LDAPS configuration

#### Dependencies

- None (can be started immediately)
- Optional: Coordinate with hx-ca-server if using Option 2

#### Related Documentation

- **Technical Details:** `docs/LDAPS-CERTIFICATE-ISSUE-EXPLANATION.md` (10KB)
- **DC Audit Report:** `DOMAIN-CONTROLLER-AUDIT-REPORT.md`
- **Corrections Summary:** `docs/INFRASTRUCTURE-DOCUMENTATION-CORRECTIONS-2025-11-10.md`

#### Coordination Required

**Frank Lucas (@agent-frank):**
- Generate and install certificate
- Configure Samba TLS settings
- Test LDAPS functionality
- Document certificate details (expiration, etc.)

**Amanda Chen (@agent-amanda):**
- Create Ansible playbook for CA certificate deployment
- Update client LDAP configurations
- Test authentication after changes

**Nathan Lewis (@agent-nathan):**
- Add certificate monitoring
- Configure expiration alerts
- Monitor LDAPS connection metrics

**William Taylor (@agent-william):**
- Support any OS-level changes needed
- Assist with troubleshooting if issues arise

---

## Low Priority Items

### None Currently

---

## Future Enhancements

### INF-001: Deploy Domain Controller Replica

**Status:** 🔴 Blocked (planning phase)
**Priority:** HIGH (but not urgent)
**Severity:** HIGH (single point of failure)
**Owner:** Frank Lucas + William Taylor
**Effort:** 4-8 hours
**Timing:** Next quarter

#### Issue

**Problem:** Single point of failure - no DC replica
- Current: Only hx-dc-server (192.168.10.200)
- If DC fails: All 28 servers lose authentication
- No redundancy for DNS, LDAP, Kerberos

#### Recommendation

Deploy **hx-dc-replica** at 192.168.10.202:
1. William provisions Ubuntu server
2. Frank configures as Samba AD DC replica
3. Test replication
4. Update DNS for failover
5. Configure clients for multiple DC servers
6. Test failover scenarios

**Dependencies:** Requires available IP and hardware resources

---

### GOV-001: Automated Documentation Consistency Checks

**Status:** 🟡 Ready
**Priority:** LOW
**Effort:** 2-3 hours
**Owner:** Agent Zero

#### Issue

Manual consistency checks needed when updating documentation.

#### Recommendation

Create script to validate:
- Server names match actual infrastructure
- IP addresses are consistent across files
- Technology names are consistent
- Cross-references are valid

**Implementation:** Shell script run monthly or pre-commit hook

---

## Completed Items

### ✅ DOCS-001: Fix FreeIPA References in Documentation

**Completed:** 2025-11-10
**Owner:** Agent Zero + Frank Lucas

**Issue:** Documentation referenced "FreeIPA" instead of actual "Samba AD DC"

**Resolution:**
- Updated 3 governance files
- Corrected server names (hx-dc-server, hx-ca-server)
- Validated consistency across all files

**Documentation:** `docs/INFRASTRUCTURE-DOCUMENTATION-CORRECTIONS-2025-11-10.md`

---

### ✅ DOCS-002: Create Comprehensive Governance Documentation

**Completed:** 2025-11-10
**Owner:** Agent Zero

**Issue:** Missing operational guides and documentation index

**Resolution:**
- Created docs/README.md (directory guide)
- Created AGENT-INVOCATION-EXAMPLES.md (8 scenarios)
- Created TROUBLESHOOTING-PLAYBOOK.md (18 common issues)
- Fixed all critical documentation issues

**Documentation:** `docs/GOVERNANCE-IMPROVEMENTS-2025-11-10.md`

---

## Backlog Statistics

**Total Items:** 3
- High Priority: 0
- Medium Priority: 1
- Low Priority: 0
- Future Enhancements: 2
- Completed: 2

**By Category:**
- Infrastructure: 2 (1 medium, 1 future)
- Documentation: 2 (completed)
- Governance: 1 (future)

---

## How to Use This Backlog

### Adding New Items

1. Identify issue or enhancement
2. Categorize by priority (High/Medium/Low/Future)
3. Assign owner (agent responsible)
4. Estimate effort
5. Document issue, solution, and success criteria
6. Add to appropriate priority section

### Working on Items

1. Change status to 🟢 In Progress
2. Update "Last Updated" date
3. Create task-specific documentation as needed
4. Coordinate with dependent agents
5. Move to Completed when done

### Review Schedule

- **Weekly:** Review High Priority items
- **Monthly:** Review Medium/Low Priority items
- **Quarterly:** Review Future Enhancements
- **Annually:** Archive completed items over 1 year old

---

**Version:** 1.0
**Classification:** Internal - Governance
**Status:** ACTIVE BACKLOG
**Next Review:** 2025-12-10

---

*Quality = Systematic completion of prioritized work*
*Backlog = Visibility into technical debt and future improvements*
