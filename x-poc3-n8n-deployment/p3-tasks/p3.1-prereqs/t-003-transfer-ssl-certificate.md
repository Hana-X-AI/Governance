# Task: Transfer SSL Certificate to hx-n8n-server

**Task ID**: T-003
**Assigned Agent**: @agent-frank
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-002, T-004
**Estimated Duration**: 30 minutes

---

## Objective
Transfer SSL certificate files from hx-ca-server (Certificate Authority) to hx-n8n-server (N8N application server) with comprehensive error handling, audit logging, and data integrity verification.

## Infrastructure Context

**Certificate Authority**: hx-ca-server.hx.dev.local (192.168.10.201)
- Tool: easy-rsa PKI
- Infrastructure: Samba Active Directory Domain (HX.DEV.LOCAL)
- NOT FreeIPA: This deployment uses Samba AD DC, not FreeIPA

**Target Server**: hx-n8n-server.hx.dev.local (192.168.10.215)
- Service: N8N workflow automation
- Requires: TLS/SSL certificates for HTTPS access

**Prerequisites**:
1. SSL certificates generated on hx-ca-server (see SSL-CERTIFICATE-GENERATION-GUIDE.md)
2. SSH access to both source and target servers
3. Sudo privileges on target server
4. Network connectivity between servers

---

## Commands

### Enhanced SSL Transfer Script (Recommended)

**IMPORTANT**: This task uses comprehensive error handling, audit logging, and data integrity verification patterns to ensure production-grade reliability and compliance.

**Script Location**: `ssl-transfer-t003.sh` (in same directory as this task)

**Features**:
- ✅ `set -euo pipefail` for fail-fast behavior
- ✅ Comprehensive error handling and logging
- ✅ Pre-flight checks (connectivity, file existence)
- ✅ File size validation (detect partial transfers)
- ✅ Certificate format validation (OpenSSL checks)
- ✅ Key-certificate pair matching verification
- ✅ Certificate expiry checking
- ✅ Permission verification after installation
- ✅ Automatic cleanup of temporary files
- ✅ Audit trail logging (SOC 2, PCI-DSS, NIST compliance)
- ✅ Backup of existing certificates before replacement
- ✅ Certificate chain verification
- ✅ Clear escalation path on failure

### Execution Instructions

**Step 1: Verify Prerequisites**:
```bash
# Ensure SSL certificates exist on CA server
ssh administrator@192.168.10.201 "ls -la /etc/ssl/private/n8n.hx.dev.local.key /etc/ssl/certs/n8n.hx.dev.local.crt /etc/ssl/certs/hx-dev-ca.crt"

# Expected output:
# -rw------- 1 root root 1704 Nov  9 10:00 /etc/ssl/private/n8n.hx.dev.local.key
# -rw-r--r-- 1 root root 2048 Nov  9 10:00 /etc/ssl/certs/n8n.hx.dev.local.crt
# -rw-r--r-- 1 root root 1234 Nov  9 10:00 /etc/ssl/certs/hx-dev-ca.crt
```

**Step 2: Execute Enhanced SSL Transfer Script**:
```bash
# Run from your workstation or jump host
cd /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-prereqs

# Execute script
./ssl-transfer-t003.sh

# Script will:
# 1. Verify connectivity to source and target servers
# 2. Verify source certificates exist and are valid
# 3. Transfer certificates to local temp directory
# 4. Validate certificate integrity (format, expiry, key-cert match)
# 5. Transfer to target server /tmp
# 6. Move to final destination with correct permissions
# 7. Verify installation and permissions
# 8. Create comprehensive audit log

# Monitor output (script logs to console and file)
# Log file: /opt/n8n/logs/t-003-ssl-transfer-YYYYMMDD-HHMMSS.log
```

**Step 3: Review Audit Log** (on target server):
```bash
# SSH to target server
ssh administrator@192.168.10.215

# View most recent transfer log
sudo cat /opt/n8n/logs/t-003-ssl-transfer-*.log | tail -100

# Expected: Complete execution log with timestamps, no ERROR entries
```

### Expected Output

```
========================================
Task T-003: SSL Certificate Transfer
========================================
Timestamp: 2025-11-09 10:30:00
Executing User: administrator
Source Server: hx-ca-server.hx.dev.local (192.168.10.201)
Target Server: hx-n8n-server.hx.dev.local (192.168.10.215)
Log File: /opt/n8n/logs/t-003-ssl-transfer-20251109-103000.log

[2025-11-09 10:30:05] Creating log directory on target server...
[2025-11-09 10:30:06] Created temporary directory: /tmp/ssl-transfer-12345
[2025-11-09 10:30:07] Verifying SSH connectivity to source server...
SSH connection successful
[2025-11-09 10:30:08] Verifying SSH connectivity to target server...
SSH connection successful
[2025-11-09 10:30:09] Verifying source certificate files on hx-ca-server.hx.dev.local...
[2025-11-09 10:30:10]   ✓ Private key found: /etc/ssl/private/n8n.hx.dev.local.key
[2025-11-09 10:30:10]   ✓ Certificate found: /etc/ssl/certs/n8n.hx.dev.local.crt
[2025-11-09 10:30:10]   ✓ CA certificate found: /etc/ssl/certs/hx-dev-ca.crt
[2025-11-09 10:30:11] SUCCESS: Pre-flight checks passed

========================================
Step 1: Transferring certificates from source server
========================================
[2025-11-09 10:30:12] Transferring private key: n8n.hx.dev.local.key
[2025-11-09 10:30:15] Private key size: 1704 bytes ✓
[2025-11-09 10:30:16] Transferring certificate: n8n.hx.dev.local.crt
[2025-11-09 10:30:18] Certificate size: 2048 bytes ✓
[2025-11-09 10:30:19] Transferring CA certificate: hx-dev-ca.crt
[2025-11-09 10:30:21] CA certificate size: 1234 bytes ✓
[2025-11-09 10:30:22] SUCCESS: All certificates transferred from source server

========================================
Step 2: Validating certificate integrity
========================================
[2025-11-09 10:30:23] Checking certificate format...
subject=CN = n8n.hx.dev.local, O = Hana-X Development, OU = Infrastructure
[2025-11-09 10:30:23] Certificate subject: subject=CN = n8n.hx.dev.local, O = Hana-X Development, OU = Infrastructure
[2025-11-09 10:30:23] Certificate issuer: issuer=CN = Hana-X Development CA, O = Hana-X
[2025-11-09 10:30:24] Certificate expiry: Dec 31 23:59:59 2025 GMT
Certificate will not expire
[2025-11-09 10:30:24] Certificate is currently valid ✓
[2025-11-09 10:30:25] Checking private key format...
RSA key ok
[2025-11-09 10:30:25] Private key format is valid ✓
[2025-11-09 10:30:26] Verifying private key matches certificate...
[2025-11-09 10:30:27] Private key matches certificate ✓
[2025-11-09 10:30:28] Checking CA certificate format...
subject=CN = Hana-X Development CA, O = Hana-X
[2025-11-09 10:30:28] CA certificate subject: subject=CN = Hana-X Development CA, O = Hana-X
[2025-11-09 10:30:29] SUCCESS: Certificate validation passed

========================================
Step 3: Transferring certificates to target server
========================================
[2025-11-09 10:30:30] Creating target directories on hx-n8n-server.hx.dev.local...
[2025-11-09 10:30:31] Target directories created/verified ✓
[2025-11-09 10:30:32] Transferring private key to target server...
[2025-11-09 10:30:35] Private key transferred successfully (1704 bytes) ✓
[2025-11-09 10:30:36] Transferring certificate to target server...
[2025-11-09 10:30:39] Certificate transferred successfully (2048 bytes) ✓
[2025-11-09 10:30:40] Transferring CA certificate to target server...
[2025-11-09 10:30:43] CA certificate transferred successfully (1234 bytes) ✓
[2025-11-09 10:30:44] SUCCESS: Files transferred to target server /tmp

========================================
Step 4: Installing certificates with permissions
========================================
[2025-11-09 10:30:45] Checking for existing certificates...
[2025-11-09 10:30:46] Installing private key to /etc/ssl/private...
[2025-11-09 10:30:47] Setting private key permissions (600, root:root)...
[2025-11-09 10:30:48] Installing certificate to /etc/ssl/certs...
[2025-11-09 10:30:49] Setting certificate permissions (644, root:root)...
[2025-11-09 10:30:50] Installing CA certificate to /etc/ssl/certs...
[2025-11-09 10:30:51] Setting CA certificate permissions (644, root:root)...
[2025-11-09 10:30:52] SUCCESS: Certificates installed with correct permissions

========================================
Step 5: Verifying certificate installation
========================================
[2025-11-09 10:30:53] Verifying private key...
[2025-11-09 10:30:54] Private key permissions: 600 root:root ✓
[2025-11-09 10:30:55] Verifying certificate...
[2025-11-09 10:30:56] Certificate permissions: 644 root:root ✓
[2025-11-09 10:30:57] Verifying CA certificate...
[2025-11-09 10:30:58] CA certificate permissions: 644 root:root ✓
[2025-11-09 10:30:59] Verifying certificate validity on target server...
subject=CN = n8n.hx.dev.local, O = Hana-X Development, OU = Infrastructure
[2025-11-09 10:31:00] Verifying certificate chain...
/etc/ssl/certs/n8n.hx.dev.local.crt: OK
[2025-11-09 10:31:01] Certificate chain verified ✓
[2025-11-09 10:31:02] SUCCESS: Certificate installation verified

========================================
✅ Task T-003 COMPLETED SUCCESSFULLY
========================================

SSL certificates transferred and installed:
  - Private Key: /etc/ssl/private/n8n.hx.dev.local.key (600, root:root)
  - Certificate: /etc/ssl/certs/n8n.hx.dev.local.crt (644, root:root)
  - CA Certificate: /etc/ssl/certs/hx-dev-ca.crt (644, root:root)

Certificate Details:
  subject=CN = n8n.hx.dev.local, O = Hana-X Development, OU = Infrastructure
  issuer=CN = Hana-X Development CA, O = Hana-X
  notBefore=Nov  9 10:00:00 2025 GMT
  notAfter=Dec 31 23:59:59 2025 GMT

Next Steps:
  1. Review log file: /opt/n8n/logs/t-003-ssl-transfer-20251109-103000.log
  2. Proceed to T-004 (Install Nginx)
  3. Configure Nginx to use these certificates:
       ssl_certificate /etc/ssl/certs/n8n.hx.dev.local.crt;
       ssl_certificate_key /etc/ssl/private/n8n.hx.dev.local.key;
  4. Test HTTPS connectivity after nginx configuration

[2025-11-09 10:31:03] SUCCESS: Task execution complete
[2025-11-09 10:31:03] Cleaning up temporary directory: /tmp/ssl-transfer-12345
[2025-11-09 10:31:03] Cleaning up temporary files on target server...
========================================
Task T-003 completed with exit code: 0
========================================
```

---

## Success Criteria

- [ ] All certificates transferred without errors
- [ ] Private key permissions: 600, owner root:root
- [ ] Certificate permissions: 644, owner root:root
- [ ] CA certificate permissions: 644, owner root:root
- [ ] Certificate format validated (openssl x509 -noout -subject succeeds)
- [ ] Private key matches certificate (modulus comparison passed)
- [ ] Certificate not expired
- [ ] Certificate chain verified (if possible)
- [ ] Audit log created: `/opt/n8n/logs/t-003-ssl-transfer-*.log`
- [ ] No sensitive data left in /tmp on source or target
- [ ] Existing certificates backed up (if present)

---

## Validation

**Automated validation is built into execution script. Manual verification (if needed)**:

```bash
# On hx-n8n-server (192.168.10.215)

# 1. Verify file existence and permissions
ls -la /etc/ssl/private/n8n.hx.dev.local.key
# Expected: -rw------- 1 root root  1704 Nov  9 10:30 n8n.hx.dev.local.key

ls -la /etc/ssl/certs/n8n.hx.dev.local.crt
# Expected: -rw-r--r-- 1 root root  2048 Nov  9 10:30 n8n.hx.dev.local.crt

ls -la /etc/ssl/certs/hx-dev-ca.crt
# Expected: -rw-r--r-- 1 root root  1234 Nov  9 10:30 hx-dev-ca.crt

# 2. Verify certificate validity
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -subject
# Expected: subject=CN = n8n.hx.dev.local, O = Hana-X Development, OU = Infrastructure

sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -dates
# Expected: notBefore and notAfter dates (cert not expired)

# 3. Verify private key format
sudo openssl rsa -in /etc/ssl/private/n8n.hx.dev.local.key -check -noout
# Expected: RSA key ok

# 4. Verify key-certificate pair match
sudo openssl rsa -in /etc/ssl/private/n8n.hx.dev.local.key -noout -modulus | openssl md5
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -modulus | openssl md5
# Expected: Both md5 hashes match (key and cert are a pair)

# 5. Verify certificate chain
sudo openssl verify -CAfile /etc/ssl/certs/hx-dev-ca.crt /etc/ssl/certs/n8n.hx.dev.local.crt
# Expected: /etc/ssl/certs/n8n.hx.dev.local.crt: OK

# 6. Review audit log
sudo cat /opt/n8n/logs/t-003-ssl-transfer-*.log
# Expected: Complete execution log with timestamps, no ERROR entries

# 7. Verify no sensitive files left in /tmp
ls -la /tmp/n8n.hx.dev.local* /tmp/ssl-transfer-*
# Expected: No such file or directory (cleaned up)
```

---

## Troubleshooting

### Common Issues and Solutions

**Issue 1: Source certificates not found**
```
ERROR: Private key not found: /etc/ssl/private/n8n.hx.dev.local.key
```
**Solution**: Generate SSL certificates first using SSL-CERTIFICATE-GENERATION-GUIDE.md

**Issue 2: SSH connection failed**
```
ERROR: Cannot connect to source server via SSH
```
**Solution**:
- Verify network connectivity: `ping 192.168.10.201`
- Verify SSH service running: `ssh administrator@192.168.10.201`
- Check SSH keys or credentials

**Issue 3: Certificate expired**
```
ERROR: Certificate has expired!
```
**Solution**: Generate a new certificate with updated expiry date

**Issue 4: Key-certificate mismatch**
```
ERROR: Private key does not match certificate (modulus mismatch)
```
**Solution**: Ensure you're using the correct key-certificate pair from the same generation process

**Issue 5: Permission denied**
```
ERROR: Failed to create target directories
```
**Solution**: Verify sudo access on target server: `ssh administrator@192.168.10.215 sudo -v`

**Issue 6: Certificate format validation failed**
```
ERROR: Certificate format validation failed (corrupted or invalid PEM format)
```
**Solution**:
- Verify certificate format: `openssl x509 -in cert.crt -text -noout`
- Regenerate if corrupted
- Check transfer didn't corrupt file (compare checksums)

### Escalation Path

**Primary Contact**: @agent-frank (Infrastructure & Identity Specialist)
- Email: frank@hx.dev.local
- Slack: #infrastructure-team
- PagerDuty: On-call rotation

**Secondary Contact**: Security team (certificate issues)
- For: Certificate validation, CA issues, PKI problems
- Slack: #security-team

**Tertiary Contact**: Network team (connectivity issues)
- For: Network connectivity, firewall, DNS resolution
- Slack: #network-ops

### Rollback Procedure

**If task fails or certificates are incorrect**:

```bash
# SSH to target server
ssh administrator@192.168.10.215

# Option 1: Restore from backup (if previous certificates existed)
sudo cp /etc/ssl/private/n8n.hx.dev.local.key.backup-* /etc/ssl/private/n8n.hx.dev.local.key
sudo cp /etc/ssl/certs/n8n.hx.dev.local.crt.backup-* /etc/ssl/certs/n8n.hx.dev.local.crt

# Option 2: Remove newly installed certificates
sudo rm -f /etc/ssl/private/n8n.hx.dev.local.key
sudo rm -f /etc/ssl/certs/n8n.hx.dev.local.crt
sudo rm -f /etc/ssl/certs/hx-dev-ca.crt

# Clean up temp files
sudo rm -f /tmp/n8n.hx.dev.local*
sudo rm -rf /tmp/ssl-transfer-*

# Fix the issue (regenerate certificates, fix connectivity, etc.)

# Re-run script after fixing issues
./ssl-transfer-t003.sh
```

---

## Compliance and Audit Requirements

### SOC 2 CC6.7: Audit Logging
- ✅ All certificate transfer operations logged with timestamps
- ✅ Executing user captured in audit log
- ✅ Source and target servers logged
- ✅ File sizes and integrity checks logged
- ✅ Success/failure status logged with exit codes

### PCI-DSS 10.2.7: System-Level Objects
- ✅ Creation of system-level certificate files logged
- ✅ Modification of file permissions logged
- ✅ Deletion/cleanup of temporary files logged
- ✅ User identity captured for all operations

### NIST 800-53 AU-2: Auditable Events
- ✅ Certificate installation events logged
- ✅ Certificate validation events logged
- ✅ Permission changes logged
- ✅ Error conditions logged with diagnostic information

**Audit Log Retention**: 90 days minimum (per SOC 2 requirements)

**Log Location**: `/opt/n8n/logs/t-003-ssl-transfer-*.log`

**Log Access**: Restricted to administrators and security team

---

## Related Documentation

**Certificate Generation**: See `SSL-CERTIFICATE-GENERATION-GUIDE.md` for complete procedures on:
- Generating SSL certificates using easy-rsa CA
- Certificate renewal procedures
- Certificate revocation procedures
- Certificate chain management

**Infrastructure Documentation**: `/srv/cc/Governance/0.3-infrastructure/`
- `ssl-tls-deployment.md` - SSL/TLS certificate deployment procedures
- `ldap-domain-integration.md` - Domain integration for certificate management

**Credentials**: `/srv/cc/Governance/0.2-credentials/hx-credentials.md`
- SSH credentials for administrator account
- Sudo access requirements

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-05 | Initial task created with basic SCP commands | Agent Zero |
| 2.0 | 2025-11-09 | **ACTION-005**: Enhanced with comprehensive error handling script (500+ lines), audit logging (SOC 2/PCI-DSS/NIST compliance), certificate validation, integrity checking, backup procedures, troubleshooting guide, escalation paths. Updated for Samba AD infrastructure (not FreeIPA). | @agent-frank |

---

**Source**: phase3-execution-plan.md:440-470, agent-frank-planning-analysis.md:124-135, CODERABBIT-FIX-ssl-transfer-error-handling.md
