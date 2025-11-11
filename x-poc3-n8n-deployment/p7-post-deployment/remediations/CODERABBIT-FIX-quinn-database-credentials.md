# CodeRabbit Fix: Quinn's Database Review - Hardcoded Credentials Remediation

**Document**: `p2-specification/review-quinn-database.md`
**Date**: 2025-11-09
**Reviewer**: CodeRabbit AI + Agent Zero
**Type**: Security Critical / Credential Management
**Severity**: CRITICAL

---

## Issue: Hardcoded Passwords in Database Review Documentation

**Location**: Multiple locations throughout review-quinn-database.md
**Primary Affected Lines**: 72-77, 545-557, 938-947 (plus additional instances)
**Severity**: CRITICAL - Plaintext credentials in version control
**Category**: Security / Credential Management / PCI-DSS 8.2.1 / SOC 2 CC6.1

### Problem

**Hardcoded password appears throughout database review**:

**Lines 72-77** (PostgreSQL Connection Test):
```bash
# Test connection with credentials
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d postgres \
    -c "SELECT current_database(), current_user;"
```

**Lines 545-557** (Database Schema Validation):
```bash
# Validate n8n database exists and is accessible
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "\dt"
```

**Lines 938-947** (Performance Baseline):
```bash
# Check connection pool settings
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "SHOW max_connections; SHOW shared_buffers;"
```

**Security Impact**:
1. **Plaintext Credential Exposure**: Password visible in version control history
2. **Audit Trail**: All git users have access to database credentials
3. **Credential Rotation**: Password must be rotated immediately upon discovery
4. **Compliance Violation**: PCI-DSS 8.2.1, SOC 2 CC6.1, NIST 800-53 IA-5

---

## Analysis

### Root Cause

**Documentation included working examples with live credentials**:
- Intent: Provide runnable examples for database validation
- Problem: Used actual production password instead of placeholder
- Pattern: Same issue as escalation document (CODERABBIT-FIX-escalation-plaintext-credentials.md)

### Scope Assessment

**Search for all instances**:
```bash
grep -n "Major8859" /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/review-quinn-database.md
```

**Expected findings**:
- Connection tests (lines 72-77)
- Schema validation (lines 545-557)
- Performance baselines (lines 938-947)
- Additional validation queries throughout document

### Compliance Implications

**PCI-DSS 8.2.1**: "Passwords must not be stored in plaintext"
**SOC 2 CC6.1**: "Logical access controls prevent unauthorized access to data and systems"
**NIST 800-53 IA-5**: "Authenticator management - passwords must be protected"

**Remediation Required**:
1. Remove plaintext credentials from version control
2. Rotate exposed credentials immediately
3. Implement credential vault references
4. Add pre-commit hooks to prevent future exposure

---

## Resolution

### Part 1: Replace Hardcoded Passwords with Placeholders

**Lines 72-77 - Change from**:
```bash
# Test connection with credentials
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d postgres \
    -c "SELECT current_database(), current_user;"
```

**To**:
```bash
# Test connection with credentials from vault
PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs) psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d postgres \
    -c "SELECT current_database(), current_user;"

# Alternative: Use environment variable placeholder for documentation
# PGPASSWORD='${DB_PASSWORD}' psql \
#     -h hx-postgres-server.hx.dev.local \
#     -U svc-n8n \
#     -d postgres \
#     -c "SELECT current_database(), current_user;"
```

**Lines 545-557 - Change from**:
```bash
# Validate n8n database exists and is accessible
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "\dt"
```

**To**:
```bash
# Validate n8n database exists and is accessible
PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs) psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "\dt"
```

**Lines 938-947 - Change from**:
```bash
# Check connection pool settings
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "SHOW max_connections; SHOW shared_buffers;"
```

**To**:
```bash
# Check connection pool settings
PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs) psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "SHOW max_connections; SHOW shared_buffers;"
```

---

### Part 2: Document Credential Management Procedure

**Add new section to review-quinn-database.md**:

```markdown
## Credential Management and Rotation Procedure

### Credential Vault Reference

**All database credentials stored in**:
```
/srv/cc/Governance/0.2-credentials/hx-credentials.md
```

**Access Pattern**:
```bash
# Extract svc-n8n password from credential vault
DB_PASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)

# Use in PostgreSQL commands
PGPASSWORD="$DB_PASSWORD" psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3
```

**Security Controls**:
- Credential vault: 600 permissions (owner read/write only)
- Owner: root:root
- Access: Restricted to authorized administrators with sudo
- Audit: All access logged via sudo audit trail

---

### Credential Rotation Procedure

**⚠️ CRITICAL: n8n requires restart after database credential changes**

**n8n caches database credentials at startup**:
- Updating `.env` file alone does NOT apply new credentials to running processes
- Running n8n instance continues using old credentials from memory
- Connection pool maintains connections with original credentials

**Rotation Steps**:

#### Option 1: Rolling Restart (High Availability)

**Prerequisites**:
- Multiple n8n instances behind load balancer
- Database connection pooling configured
- Health check endpoints enabled

**Procedure**:
```bash
# 1. Update credentials in vault
sudo nano /srv/cc/Governance/0.2-credentials/hx-credentials.md
# Change: svc-n8n:OldPassword123
# To:     svc-n8n:NewPassword456

# 2. Generate secure password and persist to protected file
# DO NOT echo or log the generated password
NEW_PASSWORD=$(openssl rand -base64 24)

# Store password securely (restrictive permissions, no stdout)
sudo mkdir -p /root/.credentials
echo "$NEW_PASSWORD" | sudo tee /root/.credentials/svc-n8n.password > /dev/null
sudo chmod 600 /root/.credentials/svc-n8n.password
echo "✅ Password generated and stored in /root/.credentials/svc-n8n.password"

# 3. Update PostgreSQL user password using peer authentication
# Run as postgres user (peer auth, no PGPASSWORD needed)
sudo -u postgres psql -c "ALTER USER \"svc-n8n\" WITH PASSWORD '$NEW_PASSWORD';"
echo "✅ PostgreSQL user password updated"

# 4. Create .pgpass for n8n service user (for application use)
sudo -u n8n bash -c "cat > ~/.pgpass << 'EOF'
hx-postgres-server.hx.dev.local:5432:n8n_poc3:svc-n8n:$NEW_PASSWORD
EOF"
sudo -u n8n chmod 0600 ~/.pgpass
echo "✅ .pgpass file created for n8n user"

# Clear password from shell memory
unset NEW_PASSWORD

# 5. Update .env file on n8n server (secure method using temporary file)
ssh hx-n8n-server.hx.dev.local << 'ENDSSH'
# Create secure temporary file
TEMP_ENV=$(mktemp /tmp/.env.XXXXXX)
chmod 600 "$TEMP_ENV"

# Read new password securely
read -sp "Enter new password for svc-n8n: " NEW_PASSWORD
echo

# Update password in temp file
sudo grep -v "^DB_POSTGRESDB_PASSWORD=" /opt/n8n/.env > "$TEMP_ENV"
echo "DB_POSTGRESDB_PASSWORD=$NEW_PASSWORD" >> "$TEMP_ENV"

# Atomic replace with correct permissions
sudo cp "$TEMP_ENV" /opt/n8n/.env
sudo chown n8n:n8n /opt/n8n/.env
sudo chmod 600 /opt/n8n/.env

# Clean up
rm -f "$TEMP_ENV"
unset NEW_PASSWORD
ENDSSH

# 6. Verify .env updated (without displaying password)
ssh hx-n8n-server.hx.dev.local "sudo grep -c DB_POSTGRESDB_PASSWORD /opt/n8n/.env"

# 7. Rolling restart (if clustered)
# Restart instance 1, wait for health check, then instance 2, etc.
ssh hx-n8n-server.hx.dev.local "sudo systemctl restart n8n"

# 8. Verify new credentials active (using .pgpass, no password in command)
sudo -u postgres psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT current_user;"

# 9. Monitor logs for connection errors
ssh hx-n8n-server.hx.dev.local "sudo journalctl -u n8n -f --since '5 minutes ago'"

# 10. Clean up sensitive variables
unset NEW_PASSWORD
```

**Downtime**: Zero (if multiple instances with load balancer)

---

#### Option 2: Service Restart (Single Instance)

**Prerequisites**:
- Single n8n instance (current POC3 deployment)
- Maintenance window scheduled
- Stakeholders notified of downtime

**Procedure**:
```bash
# 1. Update credentials in vault
sudo nano /srv/cc/Governance/0.2-credentials/hx-credentials.md

# 2. Generate secure password or use vault value
read -sp "Enter new password for svc-n8n: " NEW_PASSWORD
echo

# 3. Update PostgreSQL user password (single command, ephemeral credential)
PGPASSWORD="$NEW_PASSWORD" sudo -u postgres psql -c "ALTER USER \"svc-n8n\" WITH PASSWORD '$NEW_PASSWORD';"

# 4. Create/update .pgpass for postgres user (for verification)
sudo -u postgres bash -c "cat > ~/.pgpass << 'EOF'
hx-postgres-server.hx.dev.local:5432:n8n_poc3:svc-n8n:$NEW_PASSWORD
EOF"
sudo -u postgres chmod 0600 ~/.pgpass

# 5. Update .env file on n8n server (secure method)
ssh hx-n8n-server.hx.dev.local << 'ENDSSH'
# Create secure temporary file
TEMP_ENV=$(mktemp /tmp/.env.XXXXXX)
chmod 600 "$TEMP_ENV"

# Read password securely
read -sp "Enter new password for svc-n8n: " NEW_PASSWORD
echo

# Update password without exposing in process list
sudo grep -v "^DB_POSTGRESDB_PASSWORD=" /opt/n8n/.env > "$TEMP_ENV"
echo "DB_POSTGRESDB_PASSWORD=$NEW_PASSWORD" >> "$TEMP_ENV"

# Atomic replace
sudo cp "$TEMP_ENV" /opt/n8n/.env
sudo chown n8n:n8n /opt/n8n/.env
sudo chmod 600 /opt/n8n/.env

# Clean up
rm -f "$TEMP_ENV"
unset NEW_PASSWORD
ENDSSH

# 6. Restart n8n service
ssh hx-n8n-server.hx.dev.local "sudo systemctl restart n8n"

# 7. Verify service started successfully
ssh hx-n8n-server.hx.dev.local "sudo systemctl status n8n"

# 8. Test database connectivity (using .pgpass, no password in command)
sudo -u postgres psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"

# 9. Verify n8n can access database
curl -k https://n8n.hx.dev.local/healthz

# 10. Clean up sensitive variables
unset NEW_PASSWORD
```

**Downtime**: 5-30 seconds (service restart time)

---

#### Option 3: Service Account Exemption with Compensating Controls

**Policy Consideration**: Service accounts may be exempted from 1-year rotation policy if compensating controls exist.

**Compensating Controls for svc-n8n**:

1. **Multi-Factor Authentication** (Not Applicable - Service Account):
   - Service accounts don't support MFA
   - Compensate with certificate-based authentication or mTLS

2. **Minimal Privilege**:
   - svc-n8n granted ONLY necessary privileges (CONNECT, SELECT, INSERT, UPDATE, DELETE on n8n_poc3)
   - NO superuser, createdb, or replication privileges
   - Schema-level restrictions enforced

3. **Network Segmentation**:
   - Database access restricted to 192.168.10.0/24 subnet
   - pg_hba.conf enforces host-based authentication
   - Firewall rules limit PostgreSQL port 5432 access

4. **Audit Logging**:
   - PostgreSQL logs all svc-n8n connections (log_connections=on)
   - Failed authentication attempts logged (log_line_prefix includes username)
   - Audit logs retained for 90 days minimum

5. **Password Complexity**:
   - Minimum 12 characters (Major8859 = 9 chars - INCREASE to 12+)
   - Mix of uppercase, lowercase, numbers
   - Stored in encrypted credential vault (GPG-encrypted file or HashiCorp Vault)

6. **Monitoring and Alerting**:
   - Alert on failed authentication attempts (>3 failures in 5 minutes)
   - Alert on connections from unauthorized IPs
   - Weekly review of svc-n8n activity logs

**Recommendation**:
```markdown
## Service Account Exemption Request: svc-n8n

**Request**: Exempt svc-n8n from 1-year credential rotation policy

**Justification**:
- Credential rotation requires service restart (downtime risk)
- POC3 deployment lacks high-availability clustering
- Service account has compensating controls (minimal privilege, network segmentation, audit logging)

**Compensating Controls**:
- ✅ Minimal privilege (database-level permissions only)
- ✅ Network segmentation (host-based authentication)
- ✅ Audit logging (all connections logged)
- ⚠️  Password complexity: Increase from 9 to 12+ characters
- ⚠️  Encrypted storage: Migrate to GPG-encrypted vault or HashiCorp Vault

**Alternative**: Rotate on 2-year schedule during planned maintenance windows

**Approval Required**: Security team + Database administrator
```

---

### Post-Rotation Validation

**After credential rotation, verify**:

1. **n8n Service Health**:
   ```bash
   sudo systemctl status n8n
   # Expected: active (running)
   ```

2. **Database Connectivity**:
   ```bash
   PGPASSWORD='NewPassword' psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT current_user, version();"
   # Expected: current_user = svc-n8n, version = PostgreSQL 14.x
   ```

3. **n8n Application Access**:
   ```bash
   curl -k https://n8n.hx.dev.local/healthz
   # Expected: HTTP 200 OK
   ```

4. **Workflow Execution**:
   - Log into n8n UI (https://n8n.hx.dev.local)
   - Execute test workflow
   - Verify workflow completes successfully

5. **Log Review**:
   ```bash
   sudo journalctl -u n8n --since "10 minutes ago" | grep -i "database\|connection\|error"
   # Expected: No connection errors
   ```

---

### Emergency Rollback Procedure

**If new credentials fail**:

```bash
# 1. Revert PostgreSQL password to old value
sudo -u postgres psql -c "ALTER USER \"svc-n8n\" WITH PASSWORD 'OldPassword123';"

# 2. Revert .env file
ssh hx-n8n-server.hx.dev.local
sudo sed -i 's/DB_POSTGRESDB_PASSWORD=.*/DB_POSTGRESDB_PASSWORD=OldPassword123/' /opt/n8n/.env

# 3. Restart n8n
sudo systemctl restart n8n

# 4. Verify rollback successful
sudo systemctl status n8n
PGPASSWORD='OldPassword123' psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"
```

**RTO (Recovery Time Objective)**: 2 minutes
**RPO (Recovery Point Objective)**: Zero (no data loss - credentials only)

---

### Credential Rotation Schedule

**Service Accounts (with exemption)**:
- Frequency: 2 years OR during major version upgrades
- Trigger: Planned maintenance window
- Notification: 2 weeks advance notice to stakeholders

**Service Accounts (without exemption)**:
- Frequency: 1 year (standard policy)
- Trigger: Automated reminder 30 days before expiration
- Downtime: Schedule during maintenance window

**Emergency Rotation**:
- Trigger: Credential exposure (e.g., commit to version control)
- Timeframe: Within 24 hours of discovery
- Process: Immediate rotation + incident report + post-mortem
```

---

### Part 3: Update All Instances in Document

**Complete remediation script**:

```bash
#!/bin/bash
# Redact hardcoded passwords from Quinn's database review

FILE="/srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/review-quinn-database.md"
BACKUP="${FILE}.backup-$(date +%Y%m%d-%H%M%S)"

# Create backup
cp "$FILE" "$BACKUP"
echo "✅ Backup created: $BACKUP"

# Replace all instances of hardcoded password with credential vault reference
sed -i "s|PGPASSWORD='Major8859!'|PGPASSWORD=\$(grep \"svc-n8n:\" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)|g" "$FILE"

echo "✅ Replaced hardcoded passwords with credential vault references"

# Verify changes
echo ""
echo "=== Verification ==="
echo "Instances of 'Major8859' remaining:"
grep -c "Major8859" "$FILE" || echo "0 (all removed ✅)"

echo ""
echo "Instances of credential vault reference:"
grep -c "grep \"svc-n8n:\"" "$FILE"

echo ""
echo "=== Sample of changes ==="
grep -A2 "PGPASSWORD=" "$FILE" | head -20
```

---

## Complete Updated Examples

### Connection Test (Lines 72-77)

**BEFORE**:
```bash
# Test connection with credentials
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d postgres \
    -c "SELECT current_database(), current_user;"
```

**AFTER**:
```bash
# Test connection with credentials from vault
PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs) psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d postgres \
    -c "SELECT current_database(), current_user;"
```

---

### Schema Validation (Lines 545-557)

**BEFORE**:
```bash
# Validate n8n database exists and is accessible
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "\dt"
```

**AFTER**:
```bash
# Validate n8n database exists and is accessible
PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs) psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "\dt"
```

---

### Performance Baseline (Lines 938-947)

**BEFORE**:
```bash
# Check connection pool settings
PGPASSWORD='Major8859!' psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "SHOW max_connections; SHOW shared_buffers;"
```

**AFTER**:
```bash
# Check connection pool settings
PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs) psql \
    -h hx-postgres-server.hx.dev.local \
    -U svc-n8n \
    -d n8n_poc3 \
    -c "SHOW max_connections; SHOW shared_buffers;"
```

---

## Testing and Validation

### Pre-Remediation Checklist

- [ ] Backup review-quinn-database.md
- [ ] Verify credential vault accessible (/srv/cc/Governance/0.2-credentials/hx-credentials.md)
- [ ] Confirm svc-n8n entry exists in vault
- [ ] Document current password for rollback (store securely, NOT in git)

### Remediation Execution

```bash
# 1. Create backup
cp /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/review-quinn-database.md \
   /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/review-quinn-database.md.backup-20251109

# 2. Find all instances
grep -n "Major8859" /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/review-quinn-database.md

# 3. Replace with credential vault reference (manual or scripted)
# Use remediation script above OR manual edit

# 4. Verify all instances removed
grep "Major8859" /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/review-quinn-database.md
# Expected: No output (exit code 1)

# 5. Test credential vault reference works
PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)
echo "Password length: ${#PGPASSWORD} characters (should be 9 for 'Major8859')"

# 6. Verify database connection still works
PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs) \
    psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"
# Expected: 1 row returned
```

### Post-Remediation Validation

- [ ] Zero instances of "Major8859" in review-quinn-database.md
- [ ] Credential vault references functional (test 3+ examples)
- [ ] Credential management section added to document
- [ ] n8n restart procedure documented
- [ ] Service account exemption guidance included
- [ ] Git commit excludes plaintext passwords
- [ ] Pre-commit hook blocks future plaintext passwords

---

## Security Hardening Recommendations

### 1. Increase Password Complexity

**Current**: Major8859 (9 characters, alphanumeric only)
**Recommended**: Major8859Secure! (17 characters, mixed case + numbers + special)

**Rationale**:
- 9 characters: ~2.8e15 combinations (crackable in days with GPU cluster)
- 17 characters: ~4.8e30 combinations (crackable in centuries)
- NIST 800-63B: Minimum 12 characters for service accounts

**Update Command**:
```bash
# Generate strong password (12+ characters, mixed case, numbers, special)
NEW_PASSWORD=$(openssl rand -base64 18 | tr -d '/+' | cut -c1-16)
echo "Generated password: $NEW_PASSWORD"

# Update PostgreSQL
sudo -u postgres psql -c "ALTER USER \"svc-n8n\" WITH PASSWORD '$NEW_PASSWORD';"

# Update credential vault
sudo sed -i "s|svc-n8n:Major8859|svc-n8n:$NEW_PASSWORD|" /srv/cc/Governance/0.2-credentials/hx-credentials.md

# Update .env file
ssh hx-n8n-server.hx.dev.local
sudo sed -i "s|DB_POSTGRESDB_PASSWORD=Major8859|DB_POSTGRESDB_PASSWORD=$NEW_PASSWORD|" /opt/n8n/.env
sudo systemctl restart n8n
```

---

### 2. Encrypt Credential Vault

**Current**: Plaintext file with 600 permissions
**Recommended**: GPG-encrypted file or HashiCorp Vault

**Option A: GPG Encryption**:
```bash
# Encrypt credential vault
gpg --encrypt --recipient admin@hx.dev.local /srv/cc/Governance/0.2-credentials/hx-credentials.md

# Move encrypted file
sudo mv /srv/cc/Governance/0.2-credentials/hx-credentials.md.gpg /srv/cc/Governance/0.2-credentials/hx-credentials.md.gpg
sudo rm /srv/cc/Governance/0.2-credentials/hx-credentials.md  # Remove plaintext

# Access pattern (requires GPG key)
gpg --decrypt /srv/cc/Governance/0.2-credentials/hx-credentials.md.gpg | grep "svc-n8n:"
```

**Option B: HashiCorp Vault**:
```bash
# Store in Vault
vault kv put secret/postgres/svc-n8n password="Major8859Secure!"

# Access pattern
DB_PASSWORD=$(vault kv get -field=password secret/postgres/svc-n8n)
PGPASSWORD="$DB_PASSWORD" psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3
```

---

### 3. Implement Pre-Commit Hook

**Prevent plaintext credentials in git commits**:

```bash
#!/bin/bash
# .git/hooks/pre-commit - Block plaintext credentials

# Patterns to block
CREDENTIAL_PATTERNS=(
    "Major8859"
    "PGPASSWORD='[^$]"  # Block PGPASSWORD='literal' but allow PGPASSWORD='${VAR}'
    "password:\s*[^$]"  # Block password: literal but allow password: ${VAR}
)

echo "🔍 Scanning for plaintext credentials..."

for pattern in "${CREDENTIAL_PATTERNS[@]}"; do
    if git diff --cached | grep -qE "$pattern"; then
        echo "❌ BLOCKED: Plaintext credential detected (pattern: $pattern)"
        echo ""
        echo "Credentials must use:"
        echo "  - Environment variables: PGPASSWORD=\${DB_PASSWORD}"
        echo "  - Credential vault references: \$(grep 'svc-n8n:' /path/to/vault)"
        echo ""
        echo "To bypass (DANGEROUS): git commit --no-verify"
        exit 1
    fi
done

echo "✅ No plaintext credentials detected"
exit 0
```

**Install hook**:
```bash
cp /srv/cc/Governance/x-poc3-n8n-deployment/x-docs/coderabbit/pre-commit-hook.sh \
   /srv/cc/Governance/.git/hooks/pre-commit
chmod +x /srv/cc/Governance/.git/hooks/pre-commit
```

---

### 4. Certificate-Based Authentication (Future Enhancement)

**Replace password authentication with client certificates**:

**PostgreSQL Configuration** (pg_hba.conf):
```
# Before (password authentication)
hostssl n8n_poc3 svc-n8n 192.168.10.0/24 md5

# After (certificate authentication)
hostssl n8n_poc3 svc-n8n 192.168.10.0/24 cert clientcert=verify-full
```

**n8n Configuration** (.env):
```bash
# Certificate-based authentication
DB_POSTGRESDB_SSL_ENABLED=true
DB_POSTGRESDB_SSL_CA=/opt/n8n/certs/ca.crt
DB_POSTGRESDB_SSL_CERT=/opt/n8n/certs/svc-n8n.crt
DB_POSTGRESDB_SSL_KEY=/opt/n8n/certs/svc-n8n.key
DB_POSTGRESDB_SSL_REJECT_UNAUTHORIZED=true
```

**Benefits**:
- No password rotation required (certificates have longer validity)
- Mutual TLS authentication (server + client verification)
- Credential theft prevention (private key required)

---

## Incident Response Plan

### If Credentials Exposed in Git

**Immediate Actions** (within 1 hour):

1. **Rotate Credentials**:
   ```bash
   # Generate new password
   NEW_PASS=$(openssl rand -base64 18 | tr -d '/+' | cut -c1-16)

   # Update PostgreSQL
   sudo -u postgres psql -c "ALTER USER \"svc-n8n\" WITH PASSWORD '$NEW_PASS';"

   # Update .env
   ssh hx-n8n-server.hx.dev.local
   sudo sed -i "s|DB_POSTGRESDB_PASSWORD=.*|DB_POSTGRESDB_PASSWORD=$NEW_PASS|" /opt/n8n/.env
   sudo systemctl restart n8n
   ```

2. **Audit Access Logs**:
   ```bash
   # Check for unauthorized database access
   sudo -u postgres psql -c "
   SELECT usename, application_name, client_addr, backend_start, state
   FROM pg_stat_activity
   WHERE usename = 'svc-n8n'
   ORDER BY backend_start DESC
   LIMIT 50;"

   # Review PostgreSQL logs for failed auth attempts
   sudo grep "svc-n8n" /var/log/postgresql/postgresql-14-main.log | grep -i "authentication failed"
   ```

3. **Remove from Git History**:
   ```bash
   # Use git-filter-repo or BFG Repo-Cleaner
   git filter-repo --path p2-specification/review-quinn-database.md --invert-paths
   # WARNING: Rewrites history, requires force push
   ```

4. **Notify Stakeholders**:
   - Security team: Credential exposure incident
   - Database administrator: Credential rotated
   - Development team: Pull latest changes after force push

**Follow-up Actions** (within 24 hours):

- [ ] Incident report documenting exposure timeline
- [ ] Post-mortem analysis of how credentials entered version control
- [ ] Pre-commit hook implementation to prevent recurrence
- [ ] Security awareness training for team

---

## Lessons Learned

### Root Cause Analysis

**Why credentials appeared in documentation**:
1. Documentation included runnable examples
2. Examples used actual credentials instead of placeholders
3. No pre-commit hook to detect plaintext credentials
4. Code review didn't flag security issue

**Prevention Strategy**:
- Always use placeholders in documentation (${DB_PASSWORD})
- Pre-commit hooks block plaintext credentials
- Security review checklist for all documentation
- Automated scanning (git-secrets, truffleHog)

---

## Summary of Required Changes

### Critical Fixes

1. **Replace all hardcoded passwords** (lines 72-77, 545-557, 938-947, others):
   - Change: `PGPASSWORD='Major8859!'`
   - To: `PGPASSWORD=$(grep "svc-n8n:" /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)`

2. **Add credential management section** to review-quinn-database.md:
   - Credential vault reference pattern
   - Rotation procedure (3 options documented)
   - n8n restart requirements
   - Post-rotation validation steps
   - Emergency rollback procedure

3. **Document service restart requirement**:
   - n8n caches credentials at startup
   - Updating .env requires service restart
   - Provide rolling restart (HA) and single-instance restart procedures

### Security Enhancements

4. **Increase password complexity**:
   - Current: 9 characters (Major8859)
   - Target: 12+ characters with special characters
   - Command provided for secure password generation

5. **Implement pre-commit hook**:
   - Block commits containing plaintext credentials
   - Pattern matching for common credential formats
   - Installation instructions provided

6. **Encrypt credential vault** (future):
   - Option A: GPG encryption
   - Option B: HashiCorp Vault
   - Option C: Certificate-based authentication (eliminates passwords)

---

## Testing Checklist

After applying all fixes:

### Credential Remediation
- [ ] Zero instances of "Major8859" in review-quinn-database.md
- [ ] All PGPASSWORD commands use credential vault reference
- [ ] Credential vault reference tested and functional
- [ ] Backup of original file created

### Documentation Completeness
- [ ] Credential management section added
- [ ] n8n restart procedure documented (all 3 options)
- [ ] Post-rotation validation steps included
- [ ] Emergency rollback procedure documented
- [ ] Service account exemption guidance provided

### Security Controls
- [ ] Password complexity increased to 12+ characters
- [ ] Pre-commit hook installed and tested
- [ ] Credential vault permissions verified (600, root:root)
- [ ] Git history cleaned (no plaintext credentials)

### Operational Validation
- [ ] Test credential vault extraction works
- [ ] Test database connection with vault-referenced credentials
- [ ] Test n8n service restart procedure
- [ ] Verify n8n application functional after restart

---

## Cross-References

**Related Remediation Documents**:
- `CODERABBIT-FIX-escalation-plaintext-credentials.md` - Same credential exposure pattern
- `CODERABBIT-FIX-phase3-env-file-security.md` - .env file security hardening
- `CODERABBIT-FIX-db-username-inconsistency.md` - Database user standardization

**Affected Files**:
- `p2-specification/review-quinn-database.md` - Primary document requiring remediation
- `/srv/cc/Governance/0.2-credentials/hx-credentials.md` - Credential vault
- `/opt/n8n/.env` - n8n environment configuration (on hx-n8n-server)

**Policy References**:
- PCI-DSS 8.2.1: Password protection requirements
- SOC 2 CC6.1: Logical access controls
- NIST 800-53 IA-5: Authenticator management
- NIST 800-63B: Password complexity guidelines

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-09 | Initial CodeRabbit remediation: Redacted hardcoded passwords from Quinn's database review, replaced with credential vault references, documented n8n restart requirements, provided 3 rotation procedure options (rolling restart, single-instance restart, service account exemption), added security hardening recommendations | Agent Zero + CodeRabbit AI |

---

**Status**: ✅ REMEDIATION DOCUMENTED
**Next Step**: Execute remediation script, test credential vault references, add credential management section to document
**Priority**: CRITICAL - Plaintext credentials in version control (immediate rotation required)
**Coordination**: Security team (credential rotation), Database team (password update), n8n operator (service restart)
