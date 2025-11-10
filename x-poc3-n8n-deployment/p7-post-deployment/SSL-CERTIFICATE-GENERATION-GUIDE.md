# SSL Certificate Generation Guide for Hana-X Infrastructure

**Project**: POC3 N8N Deployment
**Owner**: Frank Delgado (@agent-frank) - Infrastructure & Identity Specialist
**Created**: 2025-11-09
**Version**: 1.0
**Infrastructure**: Samba Active Directory (HX.DEV.LOCAL)
**Certificate Authority**: hx-ca-server.hx.dev.local (192.168.10.201)

---

## Executive Summary

This guide provides comprehensive procedures for SSL/TLS certificate generation, renewal, and management for the Hana-X infrastructure using the external Certificate Authority server (hx-ca-server).

**Infrastructure Context**:
- **Domain Controller**: hx-dc-server.hx.dev.local (192.168.10.200) - Samba AD DC
- **Certificate Authority**: hx-ca-server.hx.dev.local (192.168.10.201) - easy-rsa PKI
- **Domain**: HX.DEV.LOCAL (Samba Active Directory)
- **NOT FreeIPA**: This deployment uses Samba AD DC, NOT FreeIPA (no `ipa-getcert` command)

**Certificate Tools Available**:
1. **easy-rsa** (Recommended for internal CA) - Available on hx-ca-server
2. **OpenSSL** (Self-signed, development only)
3. **Let's Encrypt** (Future production, requires public DNS)

---

## Table of Contents

1. [Infrastructure Overview](#infrastructure-overview)
2. [Certificate Authority Setup](#certificate-authority-setup)
3. [Certificate Generation Workflows](#certificate-generation-workflows)
4. [Certificate Renewal Procedures](#certificate-renewal-procedures)
5. [Certificate Revocation Procedures](#certificate-revocation-procedures)
6. [Certificate Deployment](#certificate-deployment)
7. [Certificate Monitoring](#certificate-monitoring)
8. [Troubleshooting](#troubleshooting)
9. [Compliance and Security](#compliance-and-security)

---

## Infrastructure Overview

### Certificate Authority Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Hana-X Infrastructure                      │
│                                                               │
│  ┌──────────────────────┐      ┌──────────────────────┐    │
│  │  hx-dc-server        │      │  hx-ca-server        │    │
│  │  192.168.10.200      │      │  192.168.10.201      │    │
│  │                      │      │                      │    │
│  │  Samba AD DC         │      │  easy-rsa CA         │    │
│  │  - LDAP              │      │  - Certificate       │    │
│  │  - Kerberos          │      │    Generation        │    │
│  │  - DNS               │      │  - Certificate       │    │
│  │                      │      │    Signing           │    │
│  └──────────────────────┘      │  - CRL Management    │    │
│                                │                      │    │
│                                └──────────────────────┘    │
│                                           │                 │
│                                           │ Signs           │
│                                           │ Certificates    │
│                                           ↓                 │
│  ┌─────────────────────────────────────────────────────┐  │
│  │  Service Servers (N8N, OWUI, etc.)                   │  │
│  │  - Request certificates from CA                      │  │
│  │  - Install signed certificates                       │  │
│  │  - Use for TLS/HTTPS                                │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Certificate Types

| Certificate Type | Use Case | Validity Period | Renewal Frequency |
|-----------------|----------|-----------------|-------------------|
| **Server Certificate** | HTTPS/TLS for web services (N8N, OWUI) | 365 days | Annually |
| **Wildcard Certificate** | Multiple subdomains (*.hx.dev.local) | 365 days | Annually |
| **Client Certificate** | Mutual TLS authentication | 365 days | Annually |
| **CA Certificate** | Sign other certificates | 3650 days (10 years) | Every 10 years |

### Certificate Paths

**On hx-ca-server (192.168.10.201)**:
- **PKI Directory**: `/root/easy-rsa-pki/` or `/etc/easy-rsa/pki/`
- **CA Certificate**: `pki/ca.crt`
- **Issued Certificates**: `pki/issued/`
- **Private Keys**: `pki/private/`
- **Certificate Requests**: `pki/reqs/`
- **Revocation List**: `pki/crl.pem`

**On Service Servers** (after deployment):
- **Private Keys**: `/etc/ssl/private/` (permissions: 600, root:root)
- **Certificates**: `/etc/ssl/certs/` (permissions: 644, root:root)
- **CA Certificate**: `/etc/ssl/certs/hx-dev-ca.crt`

---

## Certificate Authority Setup

### Option 1: Verify Existing CA (Recommended)

**If hx-ca-server already has easy-rsa CA configured**:

```bash
# SSH to CA server
ssh administrator@192.168.10.201

# Verify easy-rsa installation
which easyrsa
# Expected: /usr/local/bin/easyrsa or /usr/share/easy-rsa/easyrsa

# Verify PKI directory
ls -la ~/easy-rsa-pki/pki/ca.crt
# Expected: CA certificate exists

# View CA certificate details
openssl x509 -in ~/easy-rsa-pki/pki/ca.crt -noout -subject -issuer -dates
# Expected: CA subject and validity dates
```

**If CA is already configured, skip to [Certificate Generation Workflows](#certificate-generation-workflows).**

---

### Option 2: Initialize New CA (If Not Configured)

**Step 1: Install easy-rsa**:

```bash
# SSH to hx-ca-server
ssh administrator@192.168.10.201

# Install easy-rsa (Ubuntu/Debian)
sudo apt update
sudo apt install -y easy-rsa

# Verify installation
easyrsa version
# Expected: EasyRSA Version Information
```

**Step 2: Initialize PKI**:

```bash
# Create PKI directory
mkdir -p ~/easy-rsa-pki
cd ~/easy-rsa-pki

# Copy easy-rsa scripts
cp -r /usr/share/easy-rsa/* .

# Initialize PKI
./easyrsa init-pki

# Expected output:
# init-pki complete; you may now create a CA or requests.
# Your newly created PKI dir is: /root/easy-rsa-pki/pki
```

**Step 3: Create CA Certificate**:

```bash
# Build CA (no password for automated operations)
./easyrsa build-ca nopass

# Interactive prompts:
# Common Name (eg: your user, host, or server name) [Easy-RSA CA]: Hana-X Development CA

# Expected output:
# CA creation complete and you may now import and sign cert requests.
# Your new CA certificate file for publishing is at:
# /root/easy-rsa-pki/pki/ca.crt
```

**Step 4: Verify CA Certificate**:

```bash
# View CA certificate
openssl x509 -in pki/ca.crt -noout -text

# Expected: CA certificate with 10-year validity, CA:TRUE
```

**Step 5: Deploy CA Certificate to Standard Location**:

```bash
# Copy CA certificate to standard location
sudo mkdir -p /etc/ssl/certs
sudo cp pki/ca.crt /etc/ssl/certs/hx-dev-ca.crt
sudo chmod 644 /etc/ssl/certs/hx-dev-ca.crt

# Verify
ls -la /etc/ssl/certs/hx-dev-ca.crt
# Expected: -rw-r--r-- 1 root root <size> <date> /etc/ssl/certs/hx-dev-ca.crt
```

---

## Certificate Generation Workflows

### Workflow 1: Generate Server Certificate (Single Hostname)

**Use Case**: Generate certificate for specific service (e.g., N8N, Open WebUI)

**Example**: Generate certificate for `n8n.hx.dev.local`

**Step 1: Generate Certificate Request and Key**:

```bash
# SSH to hx-ca-server
ssh administrator@192.168.10.201
cd ~/easy-rsa-pki

# Generate certificate request (no password for server certificates)
./easyrsa gen-req n8n.hx.dev.local nopass

# Interactive prompt:
# Common Name (eg: your user, host, or server name) [n8n.hx.dev.local]: n8n.hx.dev.local

# Expected output:
# Keypair and certificate request completed. Your files are:
# req: /root/easy-rsa-pki/pki/reqs/n8n.hx.dev.local.req
# key: /root/easy-rsa-pki/pki/private/n8n.hx.dev.local.key
```

**Step 2: Sign Certificate Request**:

```bash
# Sign the certificate (server type, 365-day validity)
./easyrsa sign-req server n8n.hx.dev.local

# Interactive prompts:
# Confirm request details and Common Name: yes
# Enter pass phrase for /root/easy-rsa-pki/pki/private/ca.key: <CA_PASSWORD>

# Expected output:
# Certificate created at: /root/easy-rsa-pki/pki/issued/n8n.hx.dev.local.crt
```

**Step 3: Verify Generated Certificate**:

```bash
# View certificate details
openssl x509 -in pki/issued/n8n.hx.dev.local.crt -noout -subject -issuer -dates

# Expected output:
# subject=CN = n8n.hx.dev.local
# issuer=CN = Hana-X Development CA
# notBefore=Nov  9 00:00:00 2025 GMT
# notAfter=Nov  9 00:00:00 2026 GMT
```

**Step 4: Copy Certificates to Standard Location**:

```bash
# Copy to standard SSL directories for easy access
sudo cp pki/issued/n8n.hx.dev.local.crt /etc/ssl/certs/
sudo cp pki/private/n8n.hx.dev.local.key /etc/ssl/private/
sudo chmod 644 /etc/ssl/certs/n8n.hx.dev.local.crt
sudo chmod 600 /etc/ssl/private/n8n.hx.dev.local.key

# Verify
ls -la /etc/ssl/private/n8n.hx.dev.local.key
# Expected: -rw------- 1 root root <size> <date> n8n.hx.dev.local.key

ls -la /etc/ssl/certs/n8n.hx.dev.local.crt
# Expected: -rw-r--r-- 1 root root <size> <date> n8n.hx.dev.local.crt
```

**Step 5: Transfer to Target Server**:

See Task T-003 (`t-003-transfer-ssl-certificate.md`) for automated transfer with error handling.

---

### Workflow 2: Generate Wildcard Certificate (Multiple Subdomains)

**Use Case**: Single certificate for multiple subdomains (e.g., `*.hx.dev.local`)

**Benefits**:
- One certificate for all services
- Simplified management
- Reduced transfer operations

**Step 1: Generate Wildcard Certificate Request**:

```bash
# SSH to hx-ca-server
ssh administrator@192.168.10.201
cd ~/easy-rsa-pki

# Generate wildcard certificate request
./easyrsa gen-req wildcard.hx.dev.local nopass

# Interactive prompt:
# Common Name: *.hx.dev.local
```

**Step 2: Sign Wildcard Certificate**:

```bash
# Sign wildcard certificate (server type)
./easyrsa sign-req server wildcard.hx.dev.local

# Confirm: yes
# Enter CA password

# Expected output:
# Certificate created at: /root/easy-rsa-pki/pki/issued/wildcard.hx.dev.local.crt
```

**Step 3: Verify Wildcard Certificate**:

```bash
# View certificate with subject alternative names
openssl x509 -in pki/issued/wildcard.hx.dev.local.crt -noout -text | grep -A1 "Subject Alternative Name"

# Expected: DNS:*.hx.dev.local
```

**Step 4: Deploy Wildcard Certificate**:

```bash
# Copy to standard location
sudo cp pki/issued/wildcard.hx.dev.local.crt /etc/ssl/certs/
sudo cp pki/private/wildcard.hx.dev.local.key /etc/ssl/private/
sudo chmod 644 /etc/ssl/certs/wildcard.hx.dev.local.crt
sudo chmod 600 /etc/ssl/private/wildcard.hx.dev.local.key
```

**Usage**: Deploy wildcard certificate to all service servers, configure each service to use the same certificate.

---

### Workflow 3: Self-Signed Certificate (Development Only)

**Use Case**: Quick certificate generation for development/testing (NOT for production)

**Advantages**:
- No CA required
- Fast generation
- No dependency on hx-ca-server

**Disadvantages**:
- Not trusted by browsers (requires manual trust)
- No centralized management
- No revocation capability

**Generate Self-Signed Certificate on Target Server**:

```bash
# SSH to target server (e.g., hx-n8n-server)
ssh administrator@192.168.10.215

# Generate self-signed certificate (365-day validity)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/n8n.hx.dev.local.key \
  -out /etc/ssl/certs/n8n.hx.dev.local.crt \
  -subj "/C=US/ST=Development/L=Dev/O=Hana-X/OU=Infrastructure/CN=n8n.hx.dev.local"

# Set permissions
sudo chmod 600 /etc/ssl/private/n8n.hx.dev.local.key
sudo chmod 644 /etc/ssl/certs/n8n.hx.dev.local.crt

# Verify
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -subject -dates
```

**Trust Self-Signed Certificate** (client workstations):

```bash
# Copy certificate to client
scp administrator@192.168.10.215:/etc/ssl/certs/n8n.hx.dev.local.crt ~/Downloads/

# Linux: Add to trusted certificates
sudo cp ~/Downloads/n8n.hx.dev.local.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# macOS: Add to Keychain
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ~/Downloads/n8n.hx.dev.local.crt

# Windows: Add to Trusted Root Certification Authorities
# (Use certmgr.msc to import certificate)
```

**Note**: Self-signed certificates should only be used in development. Use CA-signed certificates for production.

---

## Certificate Renewal Procedures

### When to Renew

**Proactive Renewal Schedule**:
- **30 days before expiry**: Plan renewal (low priority)
- **14 days before expiry**: Execute renewal (medium priority)
- **7 days before expiry**: Urgent renewal (high priority)
- **Expired**: Emergency renewal (critical)

**Check Certificate Expiry**:

```bash
# On service server
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -dates

# Check days until expiry
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -checkend 2592000
# Exit code 0: Valid for 30+ days
# Exit code 1: Expires within 30 days
```

---

### Renewal Workflow (CA-Signed Certificates)

**Step 1: Generate New Certificate on CA Server**:

```bash
# SSH to hx-ca-server
ssh administrator@192.168.10.201
cd ~/easy-rsa-pki

# Renew certificate (regenerate with new expiry)
# Note: easy-rsa doesn't have explicit renewal, so we regenerate

# Option A: Revoke old certificate (recommended)
./easyrsa revoke n8n.hx.dev.local
./easyrsa gen-crl

# Option B: Generate new certificate with incremented name
# (e.g., n8n.hx.dev.local-2026)

# Generate new request
./easyrsa gen-req n8n.hx.dev.local nopass

# Sign new certificate
./easyrsa sign-req server n8n.hx.dev.local

# Verify new expiry date
openssl x509 -in pki/issued/n8n.hx.dev.local.crt -noout -dates
```

**Step 2: Backup Old Certificates on Target Server**:

```bash
# SSH to target server
ssh administrator@192.168.10.215

# Backup old certificates
sudo cp /etc/ssl/private/n8n.hx.dev.local.key /etc/ssl/private/n8n.hx.dev.local.key.backup-$(date +%Y%m%d)
sudo cp /etc/ssl/certs/n8n.hx.dev.local.crt /etc/ssl/certs/n8n.hx.dev.local.crt.backup-$(date +%Y%m%d)
```

**Step 3: Transfer New Certificates**:

Use Task T-003 script (`ssl-transfer-t003.sh`) to transfer renewed certificates with error handling and validation.

**Step 4: Restart Services**:

```bash
# SSH to target server
ssh administrator@192.168.10.215

# Restart services using the certificate
sudo systemctl restart nginx
sudo systemctl restart n8n  # If N8N directly uses certificate

# Verify service restarted successfully
sudo systemctl status nginx
```

**Step 5: Verify New Certificate in Use**:

```bash
# Test HTTPS connection
curl -vI https://n8n.hx.dev.local 2>&1 | grep -E "expire date|subject"

# Expected: New expiry date (1 year from today)

# Check certificate via browser
# Navigate to: https://n8n.hx.dev.local
# View certificate details (should show new expiry)
```

---

### Renewal Workflow (Self-Signed Certificates)

**Simply regenerate the certificate on the target server**:

```bash
# SSH to target server
ssh administrator@192.168.10.215

# Backup old certificate
sudo cp /etc/ssl/private/n8n.hx.dev.local.key /etc/ssl/private/n8n.hx.dev.local.key.backup-$(date +%Y%m%d)
sudo cp /etc/ssl/certs/n8n.hx.dev.local.crt /etc/ssl/certs/n8n.hx.dev.local.crt.backup-$(date +%Y%m%d)

# Regenerate self-signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/private/n8n.hx.dev.local.key \
  -out /etc/ssl/certs/n8n.hx.dev.local.crt \
  -subj "/C=US/ST=Development/L=Dev/O=Hana-X/OU=Infrastructure/CN=n8n.hx.dev.local"

# Restart service
sudo systemctl restart nginx
```

---

## Certificate Revocation Procedures

### When to Revoke a Certificate

**Revocation Triggers**:
- Private key compromised or suspected compromise
- Certificate issued incorrectly (wrong hostname, wrong expiry)
- Service decommissioned
- Hostname changed
- Security incident requiring certificate rotation

**Important**: Revocation is only meaningful for CA-signed certificates. Self-signed certificates cannot be revoked (simply delete them).

---

### Revocation Workflow (CA-Signed Certificates)

**Step 1: Revoke Certificate on CA Server**:

```bash
# SSH to hx-ca-server
ssh administrator@192.168.10.201
cd ~/easy-rsa-pki

# Revoke certificate
./easyrsa revoke n8n.hx.dev.local

# Interactive prompts:
# Please confirm you wish to revoke this certificate: yes
# Enter pass phrase for /root/easy-rsa-pki/pki/private/ca.key: <CA_PASSWORD>

# Expected output:
# Revocation was successful. You must run gen-crl and upload a new CRL

# Generate updated Certificate Revocation List (CRL)
./easyrsa gen-crl

# Expected output:
# An updated CRL has been created.
# CRL file: /root/easy-rsa-pki/pki/crl.pem
```

**Step 2: Deploy Updated CRL to Service Servers** (if CRL checking enabled):

```bash
# Copy CRL to standard location
sudo cp pki/crl.pem /etc/ssl/certs/hx-dev-ca-crl.pem
sudo chmod 644 /etc/ssl/certs/hx-dev-ca-crl.pem

# Transfer to service servers
scp /etc/ssl/certs/hx-dev-ca-crl.pem administrator@192.168.10.215:/tmp/
ssh administrator@192.168.10.215 "sudo mv /tmp/hx-dev-ca-crl.pem /etc/ssl/certs/ && sudo chmod 644 /etc/ssl/certs/hx-dev-ca-crl.pem"
```

**Step 3: Remove Revoked Certificate from Target Server**:

```bash
# SSH to target server
ssh administrator@192.168.10.215

# Backup and remove old certificate
sudo mv /etc/ssl/private/n8n.hx.dev.local.key /root/revoked-certs/n8n.hx.dev.local.key-$(date +%Y%m%d)
sudo mv /etc/ssl/certs/n8n.hx.dev.local.crt /root/revoked-certs/n8n.hx.dev.local.crt-$(date +%Y%m%d)

# Verify removal
ls /etc/ssl/private/n8n.hx.dev.local.key
# Expected: No such file or directory
```

**Step 4: Generate and Deploy New Certificate**:

Follow [Certificate Generation Workflows](#certificate-generation-workflows) to generate replacement certificate.

**Step 5: Restart Services**:

```bash
# Restart services with new certificate
sudo systemctl restart nginx
```

---

## Certificate Deployment

### Deployment Checklist

**Before Deployment**:
- [ ] Certificate generated on CA server
- [ ] Certificate signed and valid
- [ ] Private key and certificate match (modulus check)
- [ ] Certificate not expired
- [ ] Backup of existing certificates (if present)

**During Deployment**:
- [ ] Use automated transfer script (T-003: `ssl-transfer-t003.sh`)
- [ ] Verify file integrity (checksums match)
- [ ] Set correct permissions (key: 600, cert: 644)
- [ ] Verify ownership (root:root)

**After Deployment**:
- [ ] Restart services using certificate
- [ ] Verify HTTPS connectivity
- [ ] Check certificate in browser (correct hostname, expiry)
- [ ] Review audit logs for errors
- [ ] Document deployment in change log

---

### Deployment Using Task T-003 Script

**Recommended Method**: Use automated script with error handling

```bash
# From workstation or jump host
cd /srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-prereqs

# Execute SSL transfer script
./ssl-transfer-t003.sh

# Script automatically:
# - Verifies connectivity
# - Validates certificates
# - Transfers securely
# - Sets permissions
# - Creates audit log
```

**Manual Deployment** (if script unavailable):

```bash
# Transfer from CA server to target
scp administrator@192.168.10.201:/etc/ssl/private/n8n.hx.dev.local.key administrator@192.168.10.215:/tmp/
scp administrator@192.168.10.201:/etc/ssl/certs/n8n.hx.dev.local.crt administrator@192.168.10.215:/tmp/
scp administrator@192.168.10.201:/etc/ssl/certs/hx-dev-ca.crt administrator@192.168.10.215:/tmp/

# SSH to target and install
ssh administrator@192.168.10.215
sudo mkdir -p /etc/ssl/private /etc/ssl/certs
sudo mv /tmp/n8n.hx.dev.local.key /etc/ssl/private/
sudo mv /tmp/n8n.hx.dev.local.crt /etc/ssl/certs/
sudo mv /tmp/hx-dev-ca.crt /etc/ssl/certs/
sudo chown root:root /etc/ssl/private/n8n.hx.dev.local.key /etc/ssl/certs/n8n.hx.dev.local.crt /etc/ssl/certs/hx-dev-ca.crt
sudo chmod 600 /etc/ssl/private/n8n.hx.dev.local.key
sudo chmod 644 /etc/ssl/certs/n8n.hx.dev.local.crt /etc/ssl/certs/hx-dev-ca.crt
```

---

## Certificate Monitoring

### Expiry Monitoring

**Manual Check**:

```bash
# Check certificate expiry on service server
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -dates

# Check days until expiry
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -checkend 2592000
# Exit 0: Valid for 30+ days
# Exit 1: Expires within 30 days
```

**Automated Monitoring Script** (optional):

```bash
#!/bin/bash
# /usr/local/bin/check-ssl-expiry.sh

CERT_PATH="/etc/ssl/certs/n8n.hx.dev.local.crt"
WARN_DAYS=30

if ! openssl x509 -in "$CERT_PATH" -noout -checkend $((WARN_DAYS * 86400)); then
    echo "WARNING: Certificate expires within $WARN_DAYS days"
    # Send alert (email, Slack, PagerDuty)
    exit 1
fi

echo "Certificate valid for more than $WARN_DAYS days"
exit 0
```

**Cron Job for Daily Checks**:

```bash
# Add to crontab (daily at 9 AM)
0 9 * * * /usr/local/bin/check-ssl-expiry.sh >> /var/log/ssl-expiry-check.log 2>&1
```

---

### Certificate Inventory

**Maintain Certificate Inventory** (recommended for multiple services):

```bash
# Create inventory file: /srv/ca/certificate-inventory.csv
# Format: hostname,certificate_path,expiry_date,status

echo "hostname,certificate_path,expiry_date,status" > /srv/ca/certificate-inventory.csv

# Add entries for each service
echo "n8n.hx.dev.local,/etc/ssl/certs/n8n.hx.dev.local.crt,2026-11-09,active" >> /srv/ca/certificate-inventory.csv
echo "owui.hx.dev.local,/etc/ssl/certs/owui.hx.dev.local.crt,2026-11-09,active" >> /srv/ca/certificate-inventory.csv
```

**Automated Inventory Update**:

```bash
#!/bin/bash
# /usr/local/bin/update-cert-inventory.sh

for cert in /etc/ssl/certs/*.crt; do
    hostname=$(openssl x509 -in "$cert" -noout -subject | sed -n 's/.*CN=\([^,]*\).*/\1/p')
    expiry=$(openssl x509 -in "$cert" -noout -enddate | cut -d= -f2)
    echo "$hostname,$cert,$expiry,active"
done
```

---

## Troubleshooting

### Common Issues and Solutions

#### Issue 1: Certificate Request Generation Fails

**Error**:
```
Can't load /root/.rnd into RNG
```

**Solution**:
```bash
# Initialize random number generator
dd if=/dev/urandom of=~/.rnd bs=256 count=1
```

---

#### Issue 2: Certificate Signing Fails (Wrong CA Password)

**Error**:
```
unable to load CA private key
```

**Solution**:
- Verify CA password is correct
- Check CA key file exists: `ls -la pki/private/ca.key`
- Ensure CA key is readable: `sudo chmod 600 pki/private/ca.key`

---

#### Issue 3: Certificate Not Trusted by Browser

**Error**: "NET::ERR_CERT_AUTHORITY_INVALID"

**Solution**:

**Option A**: Trust CA certificate on client workstation
```bash
# Linux
sudo cp hx-dev-ca.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates

# macOS
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain hx-dev-ca.crt
```

**Option B**: Add browser exception (development only)
- Chrome/Edge: Click "Advanced" → "Proceed to <hostname> (unsafe)"
- Firefox: Click "Advanced" → "Accept the Risk and Continue"

---

#### Issue 4: Certificate Subject Mismatch

**Error**: "NET::ERR_CERT_COMMON_NAME_INVALID"

**Cause**: Certificate Common Name (CN) doesn't match hostname

**Solution**:
- Regenerate certificate with correct hostname
- Verify CN matches hostname: `openssl x509 -in cert.crt -noout -subject`

---

#### Issue 5: Key-Certificate Pair Mismatch

**Error**: nginx fails to start: "key values mismatch"

**Solution**:
```bash
# Verify key and certificate match
sudo openssl rsa -in /etc/ssl/private/n8n.hx.dev.local.key -noout -modulus | openssl md5
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -noout -modulus | openssl md5
# Hashes must match

# If mismatch: regenerate certificate with correct key
```

---

#### Issue 6: Certificate Expired

**Error**: "NET::ERR_CERT_DATE_INVALID"

**Solution**:
- Follow [Certificate Renewal Procedures](#certificate-renewal-procedures)
- Generate new certificate with updated expiry
- Deploy and restart services

---

## Compliance and Security

### Security Best Practices

**Private Key Security**:
- ✅ Never store private keys in version control
- ✅ Set permissions to 600 (owner read/write only)
- ✅ Owner should be root or service account
- ✅ Generate keys without passphrase for automated services
- ✅ Use 2048-bit RSA minimum (4096-bit recommended for CA)
- ✅ Rotate keys annually or on compromise

**Certificate Authority Security**:
- ✅ Restrict access to CA server (hx-ca-server)
- ✅ Protect CA private key with strong passphrase
- ✅ Backup CA key to secure offline storage
- ✅ Monitor CA access logs
- ✅ Rotate CA key every 10 years (before expiry)

**Certificate Lifecycle**:
- ✅ Track certificate expiry dates
- ✅ Renew certificates 30 days before expiry
- ✅ Revoke compromised certificates immediately
- ✅ Maintain certificate inventory
- ✅ Audit certificate usage quarterly

---

### Compliance Requirements

**SOC 2 CC6.1**: Logical and Physical Access Controls
- ✅ CA server access restricted to administrators
- ✅ Private keys protected with file permissions
- ✅ Certificate operations logged

**PCI-DSS 4.1**: Strong Cryptography for Transmission
- ✅ 2048-bit RSA keys (minimum)
- ✅ TLS 1.2 or higher
- ✅ Valid certificates (not expired)

**NIST 800-53 SC-17**: PKI Certificates
- ✅ CA established and maintained
- ✅ Certificates issued with proper validation
- ✅ Certificate revocation capability

---

## Related Documentation

**Infrastructure**:
- Task T-003: `t-003-transfer-ssl-certificate.md` - Automated certificate transfer
- Remediation: `CODERABBIT-FIX-ssl-transfer-error-handling.md` - Error handling improvements
- Discovery: `ACTION-006A-INFRASTRUCTURE-DISCOVERY-REPORT.md` - Infrastructure type verification

**Samba AD Documentation**:
- `/srv/cc/Governance/0.3-infrastructure/ssl-tls-deployment.md` - SSL/TLS deployment procedures
- `/srv/cc/Governance/0.3-infrastructure/ldap-domain-integration.md` - Domain integration

**Credentials**:
- `/srv/cc/Governance/0.2-credentials/hx-credentials.md` - SSH credentials, CA passwords

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-09 | **ACTION-006B**: Initial SSL certificate generation guide created. Documented easy-rsa workflows for certificate generation, renewal, revocation. Included self-signed certificate procedures for development. Updated for Samba AD infrastructure (not FreeIPA). Added certificate monitoring, troubleshooting, compliance guidance. | @agent-frank |

---

**Document Type**: Operational Runbook
**Classification**: Internal - Infrastructure
**Owner**: Frank Delgado (@agent-frank) - Infrastructure & Identity Specialist
**Related Actions**: ACTION-006B (SSL Certificate Generation Documentation)
**Status**: ✅ COMPLETED
