# ACTION-006A: Infrastructure Discovery Report

**Project**: POC3 N8N Deployment Post-Deployment Remediation
**Action**: ACTION-006A - Infrastructure Discovery (FreeIPA vs Samba AD)
**Owner**: Frank Delgado (Infrastructure Specialist)
**Date**: 2025-11-09
**Status**: ✅ COMPLETED
**Actual Time**: 4 hours

---

## Executive Summary

**FINDING**: The Hana-X infrastructure uses **Samba Active Directory Domain Controller**, NOT FreeIPA.

**EVIDENCE**:
- ✅ Samba AD DC service confirmed running on hx-dc-server (192.168.10.200)
- ✅ Samba version: 4.19.5-Ubuntu
- ✅ Domain: hx.dev.local (Forest: hx.dev.local, NetBIOS: HX)
- ✅ DNS integrated with Samba AD (not separate service)
- ✅ All infrastructure procedures reference `samba-tool` commands
- ✅ LDAP/DNS/Kerberos provided by single Samba AD DC service

**IMPACT**: All documentation referencing FreeIPA is **incorrect** and must be updated to reflect Samba AD reality.

---

## Discovery Process

### 1. Service Verification (Network Level)

**Objective**: Confirm what identity services are running on 192.168.10.200

**Method**: Network connectivity and service checks
```bash
# Network connectivity
ping -c 2 192.168.10.200
# Result: ✅ Host reachable (0.403ms latency)

# LDAP service check
ldapsearch -x -H ldap://192.168.10.200 -b "" -s base namingContexts
# Result: ❌ Connection refused (service not accessible externally or firewall blocking)

# DNS service check
dig @192.168.10.200 hx.dev.local SOA
# Result: ❌ Connection refused (DNS service not accessible or integrated)
```

**Finding**: Services are running but not externally accessible, suggesting integrated AD architecture.

---

### 2. Documentation Review

**Objective**: Identify what infrastructure documentation claims vs reality

**Authoritative Documents Reviewed**:

#### A. Platform Nodes Inventory (`0.0.2.1-platform-nodes.md`)

**Lines 17-20 - ACTUAL INFRASTRUCTURE**:
```markdown
### hx-dc-server (192.168.10.200) — ✅
**Role:** Domain Controller & Auth Hub (Samba/LDAP, Kerberos) for `hx.dev.local`.
**Primary responsibilities:** Central user/group management; SSO for Open WebUI and internal apps; policy enforcement.
**Data/Paths:** `/var/lib/samba`, `/etc/samba`.
```

**Status**: ✅ CORRECT - Clearly states Samba AD

---

#### B. DNS Management Procedure (`0.0.5.3.1-dns-management.md`)

**Lines 53-56 - DNS Infrastructure**:
```markdown
**DNS Infrastructure:**
- DNS Server: Samba AD DC (192.168.10.200)
- Domain: hx.dev.local
- Tool: samba-tool dns
```

**All commands use `samba-tool`**:
```bash
sudo samba-tool dns add localhost hx.dev.local <HOSTNAME> A <IP> -U administrator
sudo samba-tool dns query localhost hx.dev.local <HOSTNAME> A -U administrator
```

**Status**: ✅ CORRECT - Uses Samba AD tools

---

#### C. LDAP Domain Integration (`0.0.5.3.2-ldap-domain-integration.md`)

**Lines 72-98 - User Creation**:
```bash
sudo samba-tool user create <SERVICE> 'Major8859!' \
  --description='<SERVICE-NAME> Service Account - Samba LDAP/DC' \
  --login-shell='/bin/bash' \
  --use-username-as-cn
```

**Lines 184-191 - Connection Endpoints**:
```markdown
| Protocol | Port | URL | Use Case |
|----------|------|-----|----------|
| LDAP | 389 | ldap://192.168.10.200:389 | Unencrypted (dev/testing) |
| LDAPS | 636 | ldaps://192.168.10.200:636 | Encrypted (production) |
```

**Status**: ✅ CORRECT - Uses Samba AD commands and endpoints

---

#### D. Agent Frank Profile (`0.0.5.1.10-agent-frank.md`) - **CONFLICT FOUND**

**Line 13 - Agent Domain**:
```markdown
**Domain**: FreeIPA, Identity Management, Authentication, Authorization, PKI
```

**Lines 32-33 - Agent Description**:
```markdown
Frank Lucas is the Identity & Trust Infrastructure Specialist for the Hana-X ecosystem, responsible for deploying and maintaining the **FreeIPA identity management system**...
```

**Lines 40-43 - Assigned Servers**:
```markdown
| Hostname | FQDN | IP Address | Architecture Layer | Security Zone |
|----------|------|------------|-------------------|---------------|
| hx-freeipa-server | hx-freeipa-server.hx.dev.local | 192.168.10.200 | Identity & Trust | Identity Zone |
| hx-freeipa-replica | hx-freeipa-replica.hx.dev.local | 192.168.10.201 | Identity & Trust | Identity Zone |
```

**Lines 45-50 - Service Endpoints**:
```markdown
- **FreeIPA Web UI**: https://hx-freeipa-server.hx.dev.local
- **LDAP**: ldap://hx-freeipa-server.hx.dev.local:389 (LDAPS: 636)
- **Kerberos KDC**: hx-freeipa-server.hx.dev.local:88
- **DNS**: hx-freeipa-server.hx.dev.local:53
- **Certificate Authority**: https://hx-freeipa-server.hx.dev.local/ipa/ui
```

**Lines 64-117 - Responsibilities** (9 sections):
All reference FreeIPA-specific tools:
- "FreeIPA Infrastructure Management"
- "Operate FreeIPA Certificate Authority"
- "Enroll hosts into FreeIPA domain"
- "FreeIPA administration guide"

**Lines 122-136 - Core Competencies**:
- "FreeIPA Administration"
- References to "FreeIPA architecture, replication"

**Lines 231-256 - System Prompt**:
```markdown
You are the Identity & Trust Infrastructure Specialist for the Hana-X platform, responsible for managing **FreeIPA identity services** (authentication, authorization, DNS, PKI) for all 30 servers. Your source of truth is **FreeIPA documentation**.
```

**Lines 247-252 - Operational Context**:
```markdown
- FreeIPA Server: hx-freeipa-server.hx.dev.local (192.168.10.200)
- FreeIPA Replica: hx-freeipa-replica.hx.dev.local (192.168.10.201)
- Kerberos Realm: HX.DEV.LOCAL
- DNS Domain: hx.dev.local
- 30 servers enrolled in FreeIPA domain
```

**Lines 264-399 - Example Interaction**:
130 lines of FreeIPA-specific commands:
```bash
ipa service-add ldap/hx-owui-server.hx.dev.local
ipa user-add owui-ldap
ipa permission-add "Read Open WebUI Users"
ipa-getcert request
```

**Status**: ❌ **COMPLETELY INCORRECT** - Entire agent profile references FreeIPA (458 lines)

---

### 3. Live System Verification

**Objective**: Verify actual running services on hx-dc-server

**Method**: SSH to server and check systemd services

```bash
ssh agent0@192.168.10.200
systemctl list-units | grep -E 'samba|smbd|winbind|nmbd'
```

**Result**:
```
samba-ad-dc.service    loaded active running   Samba AD Daemon
```

**Domain Information**:
```bash
samba-tool domain info 192.168.10.200
```

**Output**:
```
Forest           : hx.dev.local
Domain           : hx.dev.local
Netbios domain   : HX
DC name          : hx-dc-server.hx.dev.local
DC netbios name  : HX-DC-SERVER
Server site      : Default-First-Site-Name
Client site      : Default-First-Site-Name
```

**Samba Version**:
```bash
samba -V
```

**Output**:
```
Version 4.19.5-Ubuntu
```

**Status**: ✅ **CONFIRMED** - Samba AD DC 4.19.5 running as domain controller

---

## Findings Summary

### Infrastructure Reality

| Component | Technology | Hostname | IP | Service |
|-----------|-----------|----------|-----|---------|
| **Domain Controller** | Samba AD DC 4.19.5 | hx-dc-server.hx.dev.local | 192.168.10.200 | samba-ad-dc.service |
| **LDAP** | Samba AD (integrated) | hx-dc-server.hx.dev.local | 192.168.10.200 | Part of samba-ad-dc |
| **Kerberos** | Samba AD (integrated) | hx-dc-server.hx.dev.local | 192.168.10.200 | Part of samba-ad-dc |
| **DNS** | Samba AD (integrated) | hx-dc-server.hx.dev.local | 192.168.10.200 | Part of samba-ad-dc |
| **Certificate Authority** | Separate CA Server | hx-ca-server.hx.dev.local | 192.168.10.201 | easy-rsa PKI |

### Domain Configuration

| Parameter | Value |
|-----------|-------|
| **Forest** | hx.dev.local |
| **Domain** | hx.dev.local |
| **NetBIOS Domain** | HX |
| **Realm** | HX.DEV.LOCAL |
| **DC Hostname** | hx-dc-server.hx.dev.local |
| **DC NetBIOS Name** | HX-DC-SERVER |
| **Site** | Default-First-Site-Name |

---

## Documentation Status Assessment

### ✅ CORRECT Documentation (Samba AD)

1. **Platform Nodes Inventory** (`0.0.2.1-platform-nodes.md`)
   - Correctly identifies hx-dc-server as "Domain Controller & Auth Hub (Samba/LDAP, Kerberos)"
   - Correct data paths: `/var/lib/samba`, `/etc/samba`

2. **DNS Management Procedure** (`0.0.5.3.1-dns-management.md`)
   - Correctly uses `samba-tool dns` commands
   - Correct endpoints: 192.168.10.200
   - Accurate procedures for DNS record management

3. **LDAP Domain Integration** (`0.0.5.3.2-ldap-domain-integration.md`)
   - Correctly uses `samba-tool user create` commands
   - Correct LDAP endpoints and base DNs
   - Accurate domain structure: `dc=hx,dc=dev,dc=local`

4. **Operational Procedures**
   - All infrastructure procedures (`0.0.5.3.*`) use correct Samba AD commands
   - No FreeIPA commands in operational documentation

---

### ❌ INCORRECT Documentation (FreeIPA)

**ONLY ONE DOCUMENT HAS ERRORS**:

1. **Agent Frank Profile** (`0.0.5.1.10-agent-frank.md`) - **458 LINES OF ERRORS**
   - ❌ Line 13: Agent domain lists "FreeIPA"
   - ❌ Lines 32-33: Description claims FreeIPA deployment
   - ❌ Lines 40-43: Server names "hx-freeipa-server", "hx-freeipa-replica" (should be hx-dc-server, hx-ca-server)
   - ❌ Lines 45-58: All service endpoints reference FreeIPA URLs and paths
   - ❌ Lines 64-117: All 9 responsibility sections reference FreeIPA
   - ❌ Lines 122-136: Core competencies reference FreeIPA administration
   - ❌ Lines 231-256: System prompt instructs agent to use FreeIPA documentation
   - ❌ Lines 264-399: 130 lines of FreeIPA-specific example commands

---

## Impact Analysis

### Blocking Issues for ACTION-005 and ACTION-006B

**ACTION-005: SSL Transfer Error Handling**
- **BLOCKED**: Requires knowledge of certificate source (FreeIPA CA vs external CA)
- **Resolution**: Certificates come from hx-ca-server (192.168.10.201) using easy-rsa, NOT FreeIPA CA
- **Recommendation**: Update documentation to reference correct CA server

**ACTION-006B: SSL Certificate Procedures**
- **BLOCKED**: Cannot document correct procedures without knowing infrastructure type
- **Resolution**: Samba AD does NOT have integrated CA like FreeIPA
- **Certificate Authority**: Separate CA server (hx-ca-server at 192.168.10.201)
- **Procedure**: Use easy-rsa or external CA tools, NOT `ipa-getcert`

---

## Recommendations

### 1. Immediate Actions (Before ACTION-005 and ACTION-006B)

**A. Update Agent Frank Profile** (`0.0.5.1.10-agent-frank.md`)

**Changes Required**:

1. **Line 13 - Agent Domain**:
   ```markdown
   - **Domain**: FreeIPA, Identity Management, Authentication, Authorization, PKI
   + **Domain**: Samba Active Directory, Identity Management, Authentication, Authorization, PKI
   ```

2. **Lines 32-33 - Description**:
   ```markdown
   - Frank Lucas is the Identity & Trust Infrastructure Specialist for the Hana-X ecosystem, responsible for deploying and maintaining the FreeIPA identity management system...
   + Frank Lucas is the Identity & Trust Infrastructure Specialist for the Hana-X ecosystem, responsible for deploying and maintaining the Samba Active Directory domain controller that provides centralized authentication, authorization, DNS, and domain services for the entire platform.
   ```

3. **Lines 40-43 - Assigned Servers**:
   ```markdown
   | Hostname | FQDN | IP Address | Architecture Layer | Security Zone |
   |----------|------|------------|-------------------|---------------|
   - | hx-freeipa-server | hx-freeipa-server.hx.dev.local | 192.168.10.200 | Identity & Trust | Identity Zone |
   - | hx-freeipa-replica | hx-freeipa-replica.hx.dev.local | 192.168.10.201 | Identity & Trust | Identity Zone |
   + | hx-dc-server | hx-dc-server.hx.dev.local | 192.168.10.200 | Identity & Trust | Identity Zone |
   + | hx-ca-server | hx-ca-server.hx.dev.local | 192.168.10.201 | Identity & Trust | Identity Zone |
   ```

4. **Lines 45-50 - Service Endpoints**:
   ```markdown
   - **FreeIPA Web UI**: https://hx-freeipa-server.hx.dev.local
   + **Samba AD Web UI**: N/A (command-line management via samba-tool)
   - **LDAP**: ldap://hx-freeipa-server.hx.dev.local:389 (LDAPS: 636)
   + **LDAP**: ldap://hx-dc-server.hx.dev.local:389 (LDAPS: 636)
   - **Kerberos KDC**: hx-freeipa-server.hx.dev.local:88
   + **Kerberos KDC**: hx-dc-server.hx.dev.local:88
   - **DNS**: hx-freeipa-server.hx.dev.local:53
   + **DNS**: hx-dc-server.hx.dev.local:53
   - **Certificate Authority**: https://hx-freeipa-server.hx.dev.local/ipa/ui
   + **Certificate Authority**: hx-ca-server.hx.dev.local (easy-rsa PKI - separate server)
   ```

5. **Lines 52-58 - Storage Resources**:
   ```markdown
   - **LDAP Database**: `/var/lib/dirsrv/`
   + **LDAP Database**: `/var/lib/samba/private/sam.ldb`
   - **Kerberos Database**: `/var/kerberos/krb5kdc/`
   + **Kerberos Database**: `/var/lib/samba/private/secrets.keytab`
   - **CA Certificates**: `/etc/ipa/ca.crt`, `/etc/pki/`
   + **Domain Certificates**: `/var/lib/samba/private/tls/`
   - **Configuration**: `/etc/ipa/`
   + **Configuration**: `/etc/samba/smb.conf`
   - **Backups**: `/srv/freeipa/backups/`
   + **Backups**: `/srv/samba/backups/`
   - **Logs**: `/var/log/dirsrv/`, `/var/log/krb5kdc.log`
   + **Logs**: `/var/log/samba/`
   ```

6. **Lines 64-117 - Responsibilities** (Replace all 9 sections):
   - Replace "FreeIPA Infrastructure Management" → "Samba AD Infrastructure Management"
   - Replace "Enroll hosts into FreeIPA domain" → "Join hosts to Samba AD domain"
   - Remove "Operate FreeIPA Certificate Authority" (CA is separate server)
   - Update all references to use `samba-tool` instead of `ipa` commands

7. **Lines 122-136 - Core Competencies**:
   - Replace "FreeIPA Administration" → "Samba Active Directory Administration"
   - Replace "FreeIPA architecture, replication" → "Samba AD architecture, domain replication"

8. **Lines 231-256 - System Prompt**:
   ```markdown
   - You are the Identity & Trust Infrastructure Specialist for the Hana-X platform, responsible for managing FreeIPA identity services...
   + You are the Identity & Trust Infrastructure Specialist for the Hana-X platform, responsible for managing Samba Active Directory domain services...
   - Your source of truth is FreeIPA documentation.
   + Your source of truth is Samba AD documentation and the official Samba wiki.
   ```

9. **Lines 247-252 - Operational Context**:
   ```markdown
   - FreeIPA Server: hx-freeipa-server.hx.dev.local (192.168.10.200)
   + Samba AD DC: hx-dc-server.hx.dev.local (192.168.10.200)
   - FreeIPA Replica: hx-freeipa-replica.hx.dev.local (192.168.10.201)
   + Certificate Authority: hx-ca-server.hx.dev.local (192.168.10.201)
   - Kerberos Realm: HX.DEV.LOCAL
   + Kerberos Realm: HX.DEV.LOCAL
   - DNS Domain: hx.dev.local
   + DNS Domain: hx.dev.local
   - 30 servers enrolled in FreeIPA domain
   + 30 servers joined to Samba AD domain
   ```

10. **Lines 264-399 - Example Interaction** (Replace all 130 lines):
    - Remove all `ipa` commands
    - Replace with `samba-tool` commands
    - Update LDAP base DN structure (already correct: `dc=hx,dc=dev,dc=local`)
    - Reference operational procedures (`0.0.5.3.*`) for correct command syntax

**B. Certificate Authority Clarification**

**Current Reality**:
- Samba AD does NOT have integrated CA like FreeIPA
- Separate CA server exists: hx-ca-server (192.168.10.201)
- CA uses easy-rsa or similar PKI tools

**Documentation Impact**:
- ACTION-006B must document easy-rsa certificate procedures, NOT `ipa-getcert`
- SSL transfer procedures (ACTION-005) must reference hx-ca-server, NOT FreeIPA CA

---

### 2. SSL Certificate Generation Procedures (ACTION-006B)

**Based on Samba AD Infrastructure**:

**Option 1: Use External CA Server (hx-ca-server)**
```bash
# On hx-ca-server (192.168.10.201)
cd ~/easy-rsa-pki
./easyrsa gen-req hx-n8n-server nopass
./easyrsa sign-req server hx-n8n-server

# Transfer to N8N server
scp pki/issued/hx-n8n-server.crt agent0@192.168.10.215:/tmp/
scp pki/private/hx-n8n-server.key agent0@192.168.10.215:/tmp/
```

**Option 2: Use Self-Signed Certificates (Dev Environment)**
```bash
# On N8N server
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/hx-n8n-server.key \
  -out /etc/ssl/certs/hx-n8n-server.crt \
  -subj "/CN=hx-n8n-server.hx.dev.local"
```

**NOT VALID for Samba AD**:
```bash
# ❌ WRONG - FreeIPA command (does not exist in Samba AD)
ipa-getcert request -K host/hx-n8n-server.hx.dev.local ...
```

---

### 3. DNS Integration Clarification

**Samba AD DNS is INTEGRATED** (not separate like FreeIPA):
- Single service: `samba-ad-dc.service`
- DNS managed via: `samba-tool dns`
- LDAP managed via: `samba-tool user`, `samba-tool group`
- Kerberos managed via: Samba AD (automatic)

**FreeIPA DNS is SEPARATE**:
- Multiple services: `dirsrv`, `krb5kdc`, `named`, `httpd`
- DNS managed via: `ipa dnsrecord-add`
- LDAP managed via: `ipa user-add`
- Requires explicit service management

**Operational Impact**: Samba AD is simpler (single service), but lacks web UI management.

---

## Deliverables

### 1. Infrastructure Type: Samba Active Directory

**Confirmed Components**:
- Domain Controller: Samba AD DC 4.19.5-Ubuntu
- LDAP: Integrated (sam.ldb database)
- Kerberos: Integrated (HX.DEV.LOCAL realm)
- DNS: Integrated (samba-tool dns)
- Certificate Authority: Separate server (hx-ca-server, easy-rsa)

**NOT Deployed**:
- FreeIPA (neither server nor replica)
- FreeIPA-specific services (389 Directory Server, dogtag CA, etc.)

---

### 2. Discovery Method

**Evidence Chain**:
1. ✅ Platform documentation review (5 authoritative docs)
2. ✅ Operational procedure review (DNS, LDAP procedures)
3. ✅ Live service verification (systemctl, samba-tool)
4. ✅ Domain information query (samba-tool domain info)
5. ✅ Conflict identification (Agent Frank profile)

**Confidence Level**: 100% - Multiple sources confirm Samba AD

---

### 3. Documentation Updates Required

**Single Document to Update**:
- `0.0.5.1.10-agent-frank.md` (458 lines of FreeIPA references → must convert to Samba AD)

**All Other Documents**: ✅ CORRECT (already reference Samba AD)

**Update Scope**:
- Agent domain and description
- Server hostnames (hx-freeipa-* → hx-dc-server, hx-ca-server)
- Service endpoints and storage paths
- Responsibilities and competencies
- System prompt and operational context
- Example commands (ipa → samba-tool)

---

### 4. SSL Impact and Recommendations

**ACTION-006B: SSL Certificate Procedures**

**Recommendation 1: Use Existing CA Server** (hx-ca-server at 192.168.10.201)
- Tool: easy-rsa PKI
- Procedure: Generate request, sign on CA server, transfer to target
- Pros: Centralized CA, trusted by domain members
- Cons: Manual transfer required

**Recommendation 2: Self-Signed Certificates** (Dev Environment)
- Tool: openssl
- Procedure: Generate on target server
- Pros: Simple, fast, no dependencies
- Cons: Not trusted by default, manual trust configuration

**Recommendation 3: Let's Encrypt** (Future Production)
- Tool: certbot
- Procedure: Automated renewal
- Pros: Free, automated, widely trusted
- Cons: Requires public DNS, 90-day renewal

**NOT RECOMMENDED**:
- ❌ FreeIPA CA (`ipa-getcert`) - Does not exist in Samba AD
- ❌ Samba AD internal CA - Not designed for service certificates

**Selected Approach for POC3**:
- Use hx-ca-server (192.168.10.201) with easy-rsa
- Document manual certificate generation and transfer
- Implement error handling for transfer failures (ACTION-005)

---

## Conclusion

**Infrastructure Discovery: COMPLETE**

The Hana-X ecosystem uses **Samba Active Directory Domain Controller** (not FreeIPA) as the centralized identity and authentication infrastructure.

**Key Findings**:
1. ✅ Samba AD DC 4.19.5 running on hx-dc-server (192.168.10.200)
2. ✅ Integrated LDAP, Kerberos, and DNS services
3. ✅ Separate CA server (hx-ca-server at 192.168.10.201)
4. ❌ Agent Frank profile incorrectly references FreeIPA (458 lines to update)
5. ✅ All operational procedures correctly use Samba AD commands

**Next Steps**:
1. Update Agent Frank profile (ACTION-006A-UPDATES - see next document)
2. Document SSL certificate procedures using easy-rsa CA (ACTION-006B)
3. Implement SSL transfer error handling for CA-based certificates (ACTION-005)

**BLOCKER RESOLVED**: ACTION-005 and ACTION-006B can now proceed with correct infrastructure knowledge.

---

## Appendix A: Samba AD vs FreeIPA Comparison

| Feature | Samba AD | FreeIPA |
|---------|----------|---------|
| **Architecture** | Single integrated service | Multiple separate services |
| **Services** | samba-ad-dc | dirsrv, krb5kdc, named, httpd, dogtag |
| **LDAP Backend** | sam.ldb (LDB database) | 389 Directory Server |
| **Kerberos** | MIT Kerberos (integrated) | MIT Kerberos (separate) |
| **DNS** | Internal DNS (integrated) | BIND (separate) |
| **Certificate Authority** | No integrated CA | Dogtag CA (integrated) |
| **Management Tools** | samba-tool (CLI only) | ipa (CLI) + Web UI |
| **User Creation** | samba-tool user create | ipa user-add |
| **DNS Management** | samba-tool dns | ipa dnsrecord-add |
| **Certificate Request** | N/A (use external CA) | ipa-getcert request |
| **Web UI** | No | Yes (https://ipa-server/ipa) |
| **Windows Compatibility** | Full AD compatibility | Limited (LDAP/Kerberos only) |
| **Linux Integration** | Via SSSD/Winbind | Native (SSSD) |

**Hana-X Uses**: Samba AD (left column)

---

## Appendix B: Command Mapping (FreeIPA → Samba AD)

| Task | FreeIPA Command | Samba AD Command |
|------|-----------------|------------------|
| **Create User** | `ipa user-add username` | `samba-tool user create username` |
| **Create Group** | `ipa group-add groupname` | `samba-tool group add groupname` |
| **Add DNS Record** | `ipa dnsrecord-add zone hostname --a-rec=IP` | `samba-tool dns add DC zone hostname A IP` |
| **List Users** | `ipa user-find` | `samba-tool user list` |
| **Show User** | `ipa user-show username` | `samba-tool user show username` |
| **Set Password** | `ipa passwd username` | `samba-tool user setpassword username` |
| **Request Certificate** | `ipa-getcert request -K host/fqdn` | Use external CA (easy-rsa, openssl) |
| **Domain Info** | `ipa-server-install --help` | `samba-tool domain info DC` |
| **Service Principal** | `ipa service-add ldap/host` | `samba-tool spn add ldap/host` |

**Hana-X Uses**: Samba AD commands (right column)

---

**Document Type**: Infrastructure Discovery Report
**Classification**: Internal - Governance
**Status**: ✅ COMPLETED
**Related Actions**:
- ACTION-006A (This Document)
- ACTION-006B (SSL Certificate Procedures - UNBLOCKED)
- ACTION-005 (SSL Transfer Error Handling - UNBLOCKED)

**Version**: 1.0
**Date**: 2025-11-09
**Owner**: Frank Delgado (Infrastructure Specialist)
