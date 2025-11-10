# Task: Create PostgreSQL User

**Task ID**: T-018
**Assigned Agent**: @agent-quinn
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-017
**Estimated Duration**: 15 minutes

---

## Objective
Create PostgreSQL user n8n_user with secure password and proper privileges.

## ⚠️ CRITICAL: Secure Password Requirements

**Before executing this task**:
1. Generate a **strong password** (minimum 32 characters, alphanumeric + special chars)
2. Store password securely (password manager or secure vault)
3. Replace `'GENERATE_SECURE_PASSWORD'` placeholder with actual password
4. Coordinate with @agent-omar to provide password for T-033 (.env configuration)

**Password Generation Methods** (choose one):

**Option 1: OpenSSL (Recommended)**
```bash
# Generate 32-character password (alphanumeric only, safe for shell/SQL)
SECURE_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
echo "Generated password: $SECURE_PASSWORD"
echo "⚠️  SAVE THIS PASSWORD - needed for T-033 .env file"
```

**Option 2: pwgen (if installed)**
```bash
pwgen -s 32 1
```

**Option 3: Password Manager** (most secure)
- Use 1Password, Bitwarden, or similar
- Generate 32+ character password with symbols
- Store in vault as "n8n_poc3 Database Password"

## Commands

```bash
# Step 1: Generate secure password BEFORE connecting to PostgreSQL
SECURE_PASSWORD=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
echo "⚠️  Save this password for T-033: $SECURE_PASSWORD"

# Step 2: Connect to PostgreSQL
sudo -u postgres psql

# Step 3: Create user with generated password
# IMPORTANT: Replace $SECURE_PASSWORD with actual generated value
CREATE USER n8n_user WITH ENCRYPTED PASSWORD 'PASTE_GENERATED_PASSWORD_HERE';

# Grant database privileges
GRANT CREATE, CONNECT ON DATABASE n8n_poc3 TO n8n_user;

# Connect to database
\c n8n_poc3

# Grant schema privileges
GRANT CREATE, SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO n8n_user;
GRANT USAGE, CREATE ON SCHEMA public TO n8n_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO n8n_user;

# Verify
\du n8n_user
```

## Success Criteria
- [ ] Secure password generated (32+ characters)
- [ ] Password saved to secure location (password manager or vault)
- [ ] User n8n_user created with encrypted password
- [ ] Privileges granted (CREATE, SELECT, INSERT, UPDATE, DELETE)
- [ ] Password provided to @agent-omar for T-033 .env file
- [ ] Coordination complete: Quinn → Omar password handoff documented

## Validation
```bash
sudo -u postgres psql -c "\du n8n_user"
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3 -c "SELECT 1"
```

---
**Source**: phase3-execution-plan.md:334-347, agent-quinn-planning-analysis.md:57-71
