# CodeRabbit Fix: Operational Runbook - Plaintext Database Credentials

**Document**: `p7-post-deployment/operational-runbook.md`
**Date**: 2025-11-09
**Reviewer**: CodeRabbit AI + Agent Zero
**Type**: Security Critical / Credential Exposure / Operational Documentation
**Severity**: CRITICAL

---

## Issue: Plaintext Database Password in Operational Runbook

**Locations**: Lines 221, 241, 407, 416
**Severity**: CRITICAL - Infrastructure credential in version control
**Category**: Security / Credential Management / PCI-DSS 8.2.1 / SOC 2 CC6.1

### Problem

**Database password appears in multiple locations throughout operational runbook**:

> **⚠️ ENVIRONMENT CONTEXT REQUIRED**
>
> **For Development Environment**: The credentials shown below are documentation/example only; rotation is optional.
>
> **For Production Environment**: Credentials MUST be rotated and remediated before deployment. See remediation section for secure alternatives.

**Line 221** (Configuration table):
```markdown
| `DB_POSTGRESDB_PASSWORD` | `Major8859` | Database password (URL-safe) |
```

**Line 241** (Database access instructions):
```bash
PGPASSWORD='Major8859' psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3
```

**Line 407** (Troubleshooting - Test connection):
```bash
PGPASSWORD='Major8859' psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"
```

**Line 416** (Troubleshooting - Verify password):
```markdown
**Verify Password** (should be `Major8859` without `!`):
- If password has `!`, see "URL-Safe Password Pattern" in credentials documentation
```

**Security Impact**:

1. **Infrastructure Credential in Git History**:
   - Database password `Major8859` in version control
   - Accessible to all users with repository access
   - Cannot be removed from git history without rewriting commits
   - **Same critical pattern as escalation document** (CODERABBIT-FIX-escalation-plaintext-credentials.md)

2. **Operational Runbook Exposure**:
   - Document intended for ongoing operational use
   - Likely referenced frequently by operations team
   - Higher risk of exposure through sharing, screenshots, etc.
   - Password hardcoded in troubleshooting examples

3. **Credential Scope**:
   - Account: `svc-n8n` (database service account)
   - Database: `n8n_poc3` (production n8n database)
   - Access Level: Full database access (SELECT, INSERT, UPDATE, DELETE)
   - Server: hx-postgres-server.hx.dev.local (192.168.10.209)

4. **Compliance Violation**:
   - PCI-DSS 8.2.1: "Passwords must not be stored in plaintext"
   - SOC 2 CC6.1: "Credentials must be protected from unauthorized access"
   - NIST 800-53 IA-5: "Authenticator management - passwords protected"

---

## Analysis

### Root Cause

**Operational documentation included working examples with actual credentials**:

**Intent**: Provide complete, copy-paste operational procedures
**Problem**: Used actual production database password instead of placeholder
**Pattern**: **CRITICAL** - Same issue as escalation document, now in operational runbook

### Credential Assessment

**Exposed Credential**:
- **Type**: Database service account password
- **Account**: `svc-n8n`
- **Password**: `Major8859` (exposed in 4 locations)
- **System**: PostgreSQL on hx-postgres-server.hx.dev.local
- **Database**: `n8n_poc3` (production n8n workflows)
- **Access Level**: Full CRUD operations on n8n database

**Data at Risk**:
- All n8n workflows (including credentials stored in workflows)
- Workflow execution history
- User accounts and permissions
- Encrypted credentials (if encryption key also compromised)
- Audit logs and execution metadata

### Comparison to Previous Credential Exposures

| Document | Password | Instances | Severity | Status |
|----------|----------|-----------|----------|--------|
| **Escalation Doc** | `Major8859!` | 9 locations | CRITICAL | Fixed (CODERABBIT-FIX-escalation-plaintext-credentials.md) |
| **Quinn DB Review** | `Major8859!` | 3 locations | CRITICAL | Fixed (CODERABBIT-FIX-quinn-database-credentials.md) |
| **Deployment Sign-off** | `Major8859!` | 7 psql commands | HIGH | Fixed (CODERABBIT-FIX-signoff-db-interactive-credentials.md) |
| **Operational Runbook** | `Major8859` | **4 locations** | **CRITICAL** | **THIS FIX** |

**Why CRITICAL**:
- Production database credential
- Operational runbook (frequently accessed)
- Infrastructure-level access
- Same password family as other exposed credentials (`Major8859` vs `Major8859!`)

---

## Resolution

### Part 1: Replace Configuration Table Entry (Line 221)

**Line 221 - Change from**:
```markdown
| `DB_POSTGRESDB_PASSWORD` | `Major8859` | Database password (URL-safe) |
```

**To**:
```markdown
| `DB_POSTGRESDB_PASSWORD` | `[See credential vault]` | Database password (URL-safe, no special chars) |
```

**Or** (with vault reference):
```markdown
| `DB_POSTGRESDB_PASSWORD` | `${DB_PASSWORD}` | From /srv/cc/Governance/0.2-credentials/hx-credentials.md (svc-n8n) |
```

---

### Part 2: Replace Database Access Command (Line 241)

**Lines 238-242 - Change from**:
```markdown
### Database Access

```bash
ssh hx-postgres-server.hx.dev.local
PGPASSWORD='Major8859' psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3
```
```

**To**:
```markdown
### Database Access

```bash
# Load password from credential vault
export PGPASSWORD="$(grep -m1 'svc-n8n:' /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)"

# Connect to database
ssh hx-postgres-server.hx.dev.local
psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3

# Unset password after use
unset PGPASSWORD
```

**Note**: Password loaded from secure credential vault, not hardcoded.
```

---

### Part 3: Replace Troubleshooting Connection Test (Line 407)

**Lines 404-408 - Change from**:
```markdown
**Test Connection**:
```bash
PGPASSWORD='Major8859' psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"
```
```

**To**:
```markdown
**Test Connection**:
```bash
# Load password from credential vault
export PGPASSWORD="$(grep -m1 'svc-n8n:' /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)"

# Test database connection
psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"

# Unset password
unset PGPASSWORD
```

**Expected Output**: `1` (single row)
**If Fails**: Check network connectivity, database service status, credentials in vault
```

---

### Part 4: Replace Password Verification Note (Line 416)

**Lines 410-417 - Change from**:
```markdown
**Check Credentials**:
```bash
# On n8n server
sudo cat /opt/n8n/.env | grep DB_POSTGRESDB
```

**Verify Password** (should be `Major8859` without `!`):
- If password has `!`, see "URL-Safe Password Pattern" in credentials documentation
```

**To**:
```markdown
**Check Credentials**:
```bash
# On n8n server - verify configuration (DO NOT display password)
sudo cat /opt/n8n/.env | grep DB_POSTGRESDB | grep -v PASSWORD

# Verify password is set (without displaying it)
if sudo grep -q '^DB_POSTGRESDB_PASSWORD=' /opt/n8n/.env; then
  echo "✅ Password configured in .env"
else
  echo "❌ Password missing from .env"
fi
```

**Verify Password Format** (URL-safe requirement):
- Password must be alphanumeric only (no special characters like `!`)
- Reason: URL-encoding issues in database connection strings
- Location: See credential vault for actual password
- **DO NOT display password in terminal output**
```

---

## Enhanced Solution: Add Credential Reference Section

**Add new section after line 230** (Configuration Reference):

```markdown
## Credential Management

### Credential Vault Location

**All production credentials stored in**:
```
/srv/cc/Governance/0.2-credentials/hx-credentials.md
```

**Permissions**: 600 (owner read/write only)
**Owner**: root:root
**Access**: Restricted to authorized administrators with sudo

### Database Credentials

**Service Account**: svc-n8n
**Password Location**: Credential vault entry `svc-n8n:`
**Database**: n8n_poc3 on hx-postgres-server.hx.dev.local

**Access Pattern** (for operational procedures):
```bash
# Load password from vault
export PGPASSWORD="$(grep -m1 'svc-n8n:' /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)"

# Use for database operations
psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT version();"

# ALWAYS unset after use
unset PGPASSWORD
```

**Security Requirements**:
- ⚠️ Never display password in terminal output
- ⚠️ Never commit passwords to version control
- ⚠️ Never send passwords in plaintext email/chat
- ✅ Always load from credential vault
- ✅ Always unset PGPASSWORD after use
- ✅ Audit credential access via sudo logs

### Credential Rotation

**Service Account Rotation Policy**:
- **Frequency**: Every 90 days or on suspected compromise
- **Procedure**: See `/srv/cc/Governance/x-poc3-n8n-deployment/x-docs/coderabbit/CODERABBIT-FIX-quinn-database-credentials.md`
- **Impact**: Requires n8n service restart (credentials cached at startup)

**Emergency Rotation** (if credential compromised):
1. Generate new password: `openssl rand -base64 18 | tr -d '/+=' | cut -c1-16`
2. Update PostgreSQL: `ALTER USER "svc-n8n" WITH PASSWORD 'new_password';`
3. Update .env file: `sudo sed -i 's/DB_POSTGRESDB_PASSWORD=.*/DB_POSTGRESDB_PASSWORD=new_password/' /opt/n8n/.env`
4. Update credential vault: Edit `/srv/cc/Governance/0.2-credentials/hx-credentials.md`
5. Restart n8n: `sudo systemctl restart n8n`
6. Verify: Test database connection with new credentials

---

### Password Format Requirements

**URL-Safe Password Pattern**:
- **Required**: Alphanumeric characters only (A-Z, a-z, 0-9)
- **Forbidden**: Special characters (`!@#$%^&*()`)
- **Reason**: Database connection string URL encoding issues
- **Example**: `Major8859` ✅ (URL-safe), `Major8859!` ❌ (not URL-safe)

**If Password Contains Special Characters**:
- Connection strings fail with URL encoding errors
- Must use password without special characters
- Update password to URL-safe format (rotate credential)
```

---

## Immediate Action Required: Credential Rotation

**Password `Major8859` is exposed in version control - MUST be rotated immediately**

### Rotation Steps

```bash
# 1. Generate new URL-safe password (alphanumeric only, 12+ chars)
NEW_PASSWORD=$(openssl rand -base64 18 | tr -d '/+=' | tr -d '[:punct:]' | cut -c1-16)
echo "Generated new password (save to credential vault): $NEW_PASSWORD"

# 2. Update PostgreSQL database user
export PGPASSWORD="Major8859"  # Current password
psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d postgres \
  -c "ALTER USER \"svc-n8n\" WITH PASSWORD '$NEW_PASSWORD';"
unset PGPASSWORD

# 3. Update credential vault
sudo sed -i "s|svc-n8n:Major8859|svc-n8n:$NEW_PASSWORD|" \
  /srv/cc/Governance/0.2-credentials/hx-credentials.md

# 4. Update .env file on n8n server
ssh hx-n8n-server.hx.dev.local
sudo sed -i "s|DB_POSTGRESDB_PASSWORD=Major8859|DB_POSTGRESDB_PASSWORD=$NEW_PASSWORD|" \
  /opt/n8n/.env

# 5. Restart n8n service (required - credentials cached at startup)
sudo systemctl restart n8n

# 6. Verify new credentials work
export PGPASSWORD="$NEW_PASSWORD"
psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"
unset PGPASSWORD

# 7. Verify n8n service started successfully
sudo systemctl status n8n
curl -k https://n8n.hx.dev.local/healthz

# 8. Audit database logs for suspicious activity
# Check for connections using old password after rotation
sudo -u postgres psql -c "
  SELECT usename, client_addr, backend_start, state
  FROM pg_stat_activity
  WHERE usename = 'svc-n8n'
  ORDER BY backend_start DESC
  LIMIT 20;
"
```

**Estimated Time**: 10-15 minutes
**Downtime**: 5-10 seconds (service restart)
**Rollback**: Revert password in .env and vault, restart service

---

## Testing and Validation

### Pre-Remediation Test (Demonstrates Exposure)

**Verify password in version control**:

```bash
# Search for password in current file
grep -n "Major8859" /srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/operational-runbook.md

# Expected: 4 matches (lines 221, 241, 407, 416)
# Result: Password visible in operational runbook

# Search git history for password
git log -p --all -S "Major8859" -- p7-post-deployment/operational-runbook.md

# Expected: Commits showing password in operational procedures
```

---

### Post-Remediation Test (Demonstrates Fix)

**Verify password removed and vault references work**:

```bash
# 1. Verify no plaintext passwords in runbook
grep -i "Major8859" /srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/operational-runbook.md

# Expected: No matches (or only in warning/documentation context)

# 2. Verify credential vault reference pattern used
grep "credential vault\|/srv/cc/Governance/0.2-credentials" \
  /srv/cc/Governance/x-poc3-n8n-deployment/p7-post-deployment/operational-runbook.md

# Expected: References to secure credential vault

# 3. Test credential vault access pattern
export PGPASSWORD="$(grep -m1 'svc-n8n:' /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)"
echo "Password loaded: ${#PGPASSWORD} characters"  # Show length only, not password
psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"
unset PGPASSWORD

# Expected: Connection successful, password not displayed
```

---

### Integration Test (Complete Operational Procedure)

**Test database troubleshooting procedure with vault credentials**:

```bash
#!/bin/bash
# Test operational runbook database procedures

set -euo pipefail

echo "=== Testing Operational Runbook Database Procedures ==="

# 1. Load password from vault (not hardcoded)
export PGPASSWORD="$(grep -m1 'svc-n8n:' /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)"

echo "✅ Password loaded from credential vault (${#PGPASSWORD} chars)"

# 2. Test database connection
echo -n "Test 1: Database connection... "
if psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;" >/dev/null 2>&1; then
  echo "✅ PASS"
else
  echo "❌ FAIL"
  unset PGPASSWORD
  exit 1
fi

# 3. Test database query
echo -n "Test 2: Query workflow count... "
workflow_count=$(psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 \
  -t -c "SELECT COUNT(*) FROM workflow_entity;" 2>/dev/null | xargs)
if [ -n "$workflow_count" ]; then
  echo "✅ PASS ($workflow_count workflows)"
else
  echo "❌ FAIL"
  unset PGPASSWORD
  exit 1
fi

# 4. Unset password
unset PGPASSWORD
echo "✅ Password unset from environment"

# 5. Verify password no longer accessible
if [ -z "${PGPASSWORD:-}" ]; then
  echo "✅ Password successfully removed from environment"
else
  echo "❌ Password still in environment (security risk)"
  exit 1
fi

echo ""
echo "✅ All operational runbook database procedures passed"
echo "✅ Credential vault pattern working correctly"
```

---

## Lessons Learned

### Root Cause Analysis

**Why credentials appeared in operational runbook**:
1. Runbook created from deployment procedures (which had credentials)
2. Credentials not removed when converting to operational documentation
3. Same pattern as escalation document (should have been caught)
4. Operational runbook treated as "internal only" (false sense of security)
5. No pre-commit hook to detect database credentials

**Prevention Strategy**:
- Scan ALL documentation for credentials before commit
- Operational runbooks require same security review as code
- Pre-commit hook detects ALL password patterns (Major8859, Major3059, etc.)
- "Internal only" documentation still must not contain credentials
- Credential vault references mandatory for all operational procedures

---

### Operational Runbook Security Policy

**Add to governance standards**:

```markdown
## Operational Runbook Credential Policy

**Operational runbooks are HIGH RISK for credential exposure**:
- Frequently accessed by operations team
- Often shared via screenshots, email, documentation sites
- May be printed or exported to other formats
- Subject to same security requirements as code

**NEVER Include in Operational Runbooks**:
- ❌ Plaintext passwords (any type)
- ❌ API keys or tokens
- ❌ Database connection strings with passwords
- ❌ SSH private keys
- ❌ Encryption keys
- ❌ Service account credentials

**ALWAYS Use Instead**:
- ✅ Credential vault references
- ✅ Environment variable placeholders
- ✅ "See credential vault" with vault path
- ✅ Secure loading patterns (grep from vault)
- ✅ Password rotation procedures (not passwords themselves)

**Operational Runbook Review Checklist**:
- [ ] No plaintext passwords
- [ ] All credentials reference vault
- [ ] Procedures include "load → use → unset" pattern
- [ ] Password rotation procedures documented
- [ ] Emergency response procedures included
- [ ] Credential vault location documented
- [ ] Security notes added for sensitive operations
```

---

## Summary of Required Changes

### All 4 Instances Require Remediation

**Locations**:
1. **Line 221**: Configuration table - Replace `Major8859` with `[See credential vault]`
2. **Line 241**: Database access command - Add vault loading pattern
3. **Line 407**: Troubleshooting connection test - Add vault loading pattern
4. **Line 416**: Password verification note - Remove plaintext password reference

**Pattern for All Fixes**:
```bash
# Load from vault
export PGPASSWORD="$(grep -m1 'svc-n8n:' /srv/cc/Governance/0.2-credentials/hx-credentials.md | cut -d':' -f2 | xargs)"

# Use for database operations
psql ...

# Unset after use
unset PGPASSWORD
```

---

### Critical Action: Immediate Password Rotation

**Exposed credential MUST be rotated**:
- Current password: `Major8859` (exposed)
- New password: Generate secure, URL-safe (alphanumeric only)
- Update: PostgreSQL, .env file, credential vault
- Restart: n8n service (credentials cached)
- Verify: Database connection, n8n service health
- Audit: Check for unauthorized access using old password

---

## Testing Checklist

After applying all fixes:

### Credential Removal
- [ ] Line 221: No plaintext password in config table
- [ ] Line 241: Database access uses vault reference
- [ ] Line 407: Troubleshooting uses vault reference
- [ ] Line 416: No plaintext password in verification note
- [ ] Credential vault references functional
- [ ] Load → Use → Unset pattern documented

### Password Rotation
- [ ] New password generated (URL-safe, 12+ chars)
- [ ] PostgreSQL user password updated
- [ ] .env file updated on n8n server
- [ ] Credential vault updated
- [ ] n8n service restarted
- [ ] New credentials verified working
- [ ] Database logs audited for suspicious activity

### Documentation Quality
- [ ] Credential management section added
- [ ] Password rotation procedure documented
- [ ] Emergency response procedure included
- [ ] Security notes added to sensitive sections
- [ ] No other plaintext passwords in p7-post-deployment

---

## Cross-References

**Affected Files**:
- `p7-post-deployment/operational-runbook.md` - Lines 221, 241, 407, 416 require remediation

**Related Remediation Documents**:
- `CODERABBIT-FIX-escalation-plaintext-credentials.md` - Same password exposure pattern (Major8859!)
- `CODERABBIT-FIX-quinn-database-credentials.md` - Database credential management, rotation procedures
- `CODERABBIT-FIX-signoff-db-interactive-credentials.md` - PGPASSWORD loading pattern

**Related Concepts**:
- Operational runbook security
- Credential vault architecture
- Database credential rotation
- URL-safe password requirements

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-09 | Initial CodeRabbit remediation: Removed plaintext database password (Major8859) from operational runbook (lines 221, 241, 407, 416), replaced with credential vault references, added credential management section, documented password rotation procedure, flagged for immediate credential rotation | Agent Zero + CodeRabbit AI |

---

**Status**: ✅ REMEDIATION DOCUMENTED
**Next Step**: Remove passwords from all 4 locations, rotate svc-n8n credentials IMMEDIATELY, update operational procedures
**Priority**: CRITICAL - Production database credential in operational documentation (same severity as escalation document)
**Coordination**: Security team (immediate rotation), Operations team (update procedures), Database team (password rotation)
