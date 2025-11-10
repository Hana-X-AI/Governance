# Environment File Security Guide

**Document Type**: Security Best Practices
**Version**: 1.0
**Date**: 2025-11-09
**Project**: POC3 N8N Deployment
**Author**: William Torres, Systems Administrator Specialist

---

## Table of Contents

1. [Password Generation Best Practices](#1-password-generation-best-practices)
2. [File Permission Requirements](#2-file-permission-requirements)
3. [Version Control Protection](#3-version-control-protection)
4. [Production Secrets Management](#4-production-secrets-management)
5. [Validation Checks and Automated Testing](#5-validation-checks-and-automated-testing)
6. [Password Manager Usage](#6-password-manager-usage)
7. [Credential Rotation Policy](#7-credential-rotation-policy)
8. [Compliance References](#8-compliance-references)
9. [.env Format Validation](#9-env-format-validation)
10. [Troubleshooting Common Issues](#10-troubleshooting-common-issues)

---

## 1. Password Generation Best Practices

### 1.1 Minimum Requirements

**Length**: 32+ characters for production systems
**Character Diversity**:
- Uppercase letters (A-Z)
- Lowercase letters (a-z)
- Numbers (0-9)
- Special characters (!@#$%^&*-_+=)

### 1.2 Recommended Generation Tools

#### Using OpenSSL (Linux/macOS)
```bash
# Generate 32-character base64 password
openssl rand -base64 32

# Generate 48-character base64 password (recommended for production)
openssl rand -base64 48

# Generate hex password (64 characters)
openssl rand -hex 32
```

#### Using /dev/urandom (Linux)
```bash
# Generate 32-character alphanumeric password
tr -dc 'A-Za-z0-9!@#$%^&*-_+=' < /dev/urandom | head -c 32; echo
```

#### Using Python
```python
import secrets
import string

def generate_password(length=32):
    """Generate cryptographically secure password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_+="
    return ''.join(secrets.choice(alphabet) for i in range(length))

# Generate password
print(generate_password(48))
```

#### Using Password Managers
- **1Password**: Generate → Custom → 48 characters → All character types
- **LastPass**: Generate Secure Password → 48 characters → Include symbols
- **Bitwarden**: Generator → Password → Length: 48 → All options enabled

### 1.3 What to Avoid

**NEVER use**:
- Dictionary words or common phrases
- Personal information (birthdays, names, addresses)
- Sequential patterns (abc123, qwerty)
- Repeated characters (aaaa1111)
- Previously leaked passwords (check haveibeenpwned.com)
- Short passwords (<20 characters for production)

### 1.4 Special Considerations for .env Files

**Shell-safe characters**: Avoid characters that require escaping in shell:
- Avoid: ` (backtick), $ (dollar), " (double quote), \ (backslash)
- Safe: Letters, numbers, and symbols like !@#%^&*-_+=

**Example safe password generation**:
```bash
# Generate password safe for .env files (no shell metacharacters)
openssl rand -base64 48 | tr -d '\n' | sed 's/[`$"\\]//g'
```

---

## 2. File Permission Requirements

### 2.1 Why Permissions Matter

**Risk**: World-readable .env files expose credentials to any user on the system
**Attack Vector**: Local privilege escalation, credential harvesting
**Best Practice**: Restrict access to service user only

### 2.2 Correct Permission Settings

#### Standard .env File Permissions
```bash
# Set owner read/write only (600)
sudo chmod 600 /opt/n8n/.env

# Set proper ownership
sudo chown n8n:n8n /opt/n8n/.env

# Verify permissions
ls -la /opt/n8n/.env
# Expected output: -rw------- 1 n8n n8n 1234 Nov 09 12:00 /opt/n8n/.env
```

#### Permission Breakdown
| Permission | Owner | Group | Others | Octal |
|------------|-------|-------|--------|-------|
| Read       | ✓     | ✗     | ✗      | 400   |
| Write      | ✓     | ✗     | ✗      | 200   |
| Execute    | ✗     | ✗     | ✗      | 000   |
| **Total**  | **rw-** | **---** | **---** | **600** |

### 2.3 Directory Permission Requirements

```bash
# Parent directory should be accessible but not writable by others
sudo chmod 755 /opt/n8n
sudo chown n8n:n8n /opt/n8n

# Verify directory permissions
ls -lad /opt/n8n
# Expected: drwxr-xr-x 3 n8n n8n 4096 Nov 09 12:00 /opt/n8n
```

### 2.4 Common Permission Mistakes

#### INSECURE - World Readable
```bash
-rw-r--r-- 1 n8n n8n 1234 Nov 09 12:00 /opt/n8n/.env
# RISK: Any user can read credentials
```

#### INSECURE - Group Readable
```bash
-rw-r----- 1 n8n n8n 1234 Nov 09 12:00 /opt/n8n/.env
# RISK: All members of n8n group can read credentials
```

#### INSECURE - Wrong Owner
```bash
-rw------- 1 root root 1234 Nov 09 12:00 /opt/n8n/.env
# RISK: N8N service cannot read file (permission denied)
```

### 2.5 Automated Permission Verification

```bash
#!/bin/bash
# verify-env-permissions.sh

ENV_FILE="/opt/n8n/.env"
EXPECTED_PERMS="600"
EXPECTED_OWNER="n8n"
EXPECTED_GROUP="n8n"

# Check file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: $ENV_FILE not found"
    exit 1
fi

# Check permissions
ACTUAL_PERMS=$(stat -c "%a" "$ENV_FILE")
if [ "$ACTUAL_PERMS" != "$EXPECTED_PERMS" ]; then
    echo "ERROR: Incorrect permissions. Expected: $EXPECTED_PERMS, Actual: $ACTUAL_PERMS"
    exit 1
fi

# Check ownership
ACTUAL_OWNER=$(stat -c "%U" "$ENV_FILE")
ACTUAL_GROUP=$(stat -c "%G" "$ENV_FILE")
if [ "$ACTUAL_OWNER" != "$EXPECTED_OWNER" ] || [ "$ACTUAL_GROUP" != "$EXPECTED_GROUP" ]; then
    echo "ERROR: Incorrect ownership. Expected: $EXPECTED_OWNER:$EXPECTED_GROUP, Actual: $ACTUAL_OWNER:$ACTUAL_GROUP"
    exit 1
fi

echo "SUCCESS: $ENV_FILE has correct permissions and ownership"
exit 0
```

---

## 3. Version Control Protection

### 3.1 .gitignore Patterns

**CRITICAL**: Never commit .env files to version control

#### .gitignore Configuration
```bash
# Add to .gitignore in project root
cat >> /path/to/project/.gitignore << 'EOF'

# Environment files (SECURITY: Never commit credentials)
.env
.env.*
!.env.example
*.env
.env.local
.env.production
.env.staging
.env.development

# Backup files
.env.backup
.env.bak
*.env.bak

EOF
```

### 3.2 .env.example Template Pattern

**Best Practice**: Commit example file with placeholder values

```bash
# .env.example - Safe to commit
DB_TYPE=postgresdb
DB_HOST=postgres.example.com
DB_PORT=5432
DB_DATABASE=n8n
DB_USERNAME=n8n_user
DB_PASSWORD=CHANGEME_GENERATE_SECURE_PASSWORD

ENCRYPTION_KEY=CHANGEME_RUN_openssl_rand_base64_32

N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=CHANGEME_GENERATE_SECURE_PASSWORD

# Generation instructions in comments
# DB_PASSWORD: openssl rand -base64 48
# ENCRYPTION_KEY: openssl rand -base64 32
# N8N_BASIC_AUTH_PASSWORD: openssl rand -base64 32
```

### 3.3 Pre-commit Hook to Block .env Commits

#### Git Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for .env files in commit
if git diff --cached --name-only | grep -E '\.env$|\.env\.[^.]+$' | grep -v '\.env\.example$'; then
    echo "ERROR: Attempting to commit .env file"
    echo "Blocked files:"
    git diff --cached --name-only | grep -E '\.env$|\.env\.[^.]+$' | grep -v '\.env\.example$'
    echo ""
    echo "SECURITY: .env files contain credentials and must not be committed"
    echo "Add to .gitignore or use .env.example for templates"
    exit 1
fi

# Check for common credential patterns in all files
if git diff --cached --diff-filter=d | grep -E 'password\s*=\s*[^(CHANGEME|REPLACE|TODO)]' | grep -v '.env.example'; then
    echo "WARNING: Possible hardcoded password detected"
    echo "Review changes carefully before committing"
fi

exit 0
```

#### Install Pre-commit Hook
```bash
# Make hook executable
chmod +x .git/hooks/pre-commit

# Test hook
git add .env  # Should be blocked
git add .env.example  # Should be allowed
```

### 3.4 Git History Cleanup (If .env Already Committed)

**WARNING**: This rewrites history. Coordinate with team before executing.

```bash
# Remove .env from entire git history
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch .env' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (coordinate with team)
git push origin --force --all
git push origin --force --tags

# Cleanup
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Rotate ALL credentials in leaked .env file
# Consider previous commits compromised
```

#### Alternative: BFG Repo-Cleaner (Faster)
```bash
# Install BFG
# Ubuntu/Debian
sudo apt-get install bfg

# Remove .env files from history
bfg --delete-files .env

# Cleanup
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

---

## 4. Production Secrets Management

### 4.1 HashiCorp Vault Integration

#### 4.1.1 Vault Server Setup

```bash
# Install Vault (Ubuntu 24.04)
wget -O- https://apt.releases.hashicorp.com/gpg | sudo gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt install vault

# Configure Vault
sudo mkdir -p /opt/vault/data
sudo tee /etc/vault.d/vault.hcl > /dev/null << 'EOF'
storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 0
  tls_cert_file = "/etc/vault.d/certs/vault.crt"
  tls_key_file = "/etc/vault.d/certs/vault.key"
}

api_addr = "https://vault.hx.dev.local:8200"
cluster_addr = "https://vault.hx.dev.local:8201"
ui = true
EOF

# Start Vault
sudo systemctl enable vault
sudo systemctl start vault

# Initialize Vault (save unseal keys and root token securely!)
vault operator init -key-shares=5 -key-threshold=3
```

#### 4.1.2 Store N8N Credentials in Vault

```bash
# Authenticate to Vault
export VAULT_ADDR='https://vault.hx.dev.local:8200'
vault login <root-token>

# Enable KV secrets engine
vault secrets enable -path=n8n kv-v2

# Store N8N credentials
vault kv put n8n/config \
  db_password="$(openssl rand -base64 48)" \
  encryption_key="$(openssl rand -base64 32)" \
  basic_auth_password="$(openssl rand -base64 32)"

# Verify storage
vault kv get n8n/config
```

#### 4.1.3 N8N Integration with Vault

**Option A: Vault Agent (Recommended)**

```bash
# Install Vault Agent configuration
sudo tee /etc/vault-agent.d/n8n.hcl > /dev/null << 'EOF'
pid_file = "/var/run/vault-agent.pid"

vault {
  address = "https://vault.hx.dev.local:8200"
}

auto_auth {
  method {
    type = "approle"
    config = {
      role_id_file_path = "/etc/vault-agent.d/role-id"
      secret_id_file_path = "/etc/vault-agent.d/secret-id"
      remove_secret_id_file_after_reading = false
    }
  }

  sink {
    type = "file"
    config = {
      path = "/var/run/vault-token"
    }
  }
}

template {
  source      = "/opt/n8n/.env.template"
  destination = "/opt/n8n/.env"
  perms       = "0600"
  command     = "systemctl restart n8n"
}
EOF

# Create .env template
sudo tee /opt/n8n/.env.template > /dev/null << 'EOF'
DB_TYPE=postgresdb
DB_HOST=hx-postgres-server.hx.dev.local
DB_PORT=5432
DB_DATABASE=n8n
DB_USERNAME=n8n
{{ with secret "n8n/config" }}
DB_PASSWORD={{ .Data.data.db_password }}
ENCRYPTION_KEY={{ .Data.data.encryption_key }}
N8N_BASIC_AUTH_PASSWORD={{ .Data.data.basic_auth_password }}
{{ end }}
N8N_BASIC_AUTH_USER=admin
N8N_HOST=n8n.hx.dev.local
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.hx.dev.local/
EOF

# Start Vault Agent
sudo systemctl enable vault-agent
sudo systemctl start vault-agent
```

**Option B: Direct Vault CLI Integration**

```bash
#!/bin/bash
# /opt/n8n/scripts/load-env-from-vault.sh

set -e

VAULT_ADDR="https://vault.hx.dev.local:8200"
VAULT_TOKEN="$(cat /var/run/vault-token)"

# Fetch secrets from Vault
DB_PASSWORD=$(vault kv get -field=db_password n8n/config)
ENCRYPTION_KEY=$(vault kv get -field=encryption_key n8n/config)
BASIC_AUTH_PASSWORD=$(vault kv get -field=basic_auth_password n8n/config)

# Generate .env file
cat > /opt/n8n/.env << EOF
DB_TYPE=postgresdb
DB_HOST=hx-postgres-server.hx.dev.local
DB_PORT=5432
DB_DATABASE=n8n
DB_USERNAME=n8n
DB_PASSWORD=${DB_PASSWORD}
ENCRYPTION_KEY=${ENCRYPTION_KEY}
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=${BASIC_AUTH_PASSWORD}
N8N_HOST=n8n.hx.dev.local
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.hx.dev.local/
EOF

# Set permissions
chmod 600 /opt/n8n/.env
chown n8n:n8n /opt/n8n/.env
```

### 4.2 AWS Secrets Manager Integration

#### 4.2.1 Store Secrets in AWS Secrets Manager

```bash
# Install AWS CLI
sudo apt-get install awscli

# Configure AWS credentials
aws configure

# Create secret
aws secretsmanager create-secret \
  --name n8n/production/config \
  --description "N8N production credentials" \
  --secret-string '{
    "db_password": "'$(openssl rand -base64 48)'",
    "encryption_key": "'$(openssl rand -base64 32)'",
    "basic_auth_password": "'$(openssl rand -base64 32)'"
  }'
```

#### 4.2.2 N8N Integration with AWS Secrets Manager

**Python Script to Fetch Secrets**

```python
#!/usr/bin/env python3
# /opt/n8n/scripts/load-env-from-aws.py

import boto3
import json
import os

def get_secret(secret_name, region_name="us-east-1"):
    """Retrieve secret from AWS Secrets Manager"""
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise

    return json.loads(get_secret_value_response['SecretString'])

def generate_env_file():
    """Generate .env file from AWS Secrets Manager"""
    secrets = get_secret('n8n/production/config')

    env_content = f"""DB_TYPE=postgresdb
DB_HOST=hx-postgres-server.hx.dev.local
DB_PORT=5432
DB_DATABASE=n8n
DB_USERNAME=n8n
DB_PASSWORD={secrets['db_password']}
ENCRYPTION_KEY={secrets['encryption_key']}
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD={secrets['basic_auth_password']}
N8N_HOST=n8n.hx.dev.local
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.hx.dev.local/
"""

    # Write .env file
    env_path = '/opt/n8n/.env'
    with open(env_path, 'w') as f:
        f.write(env_content)

    # Set permissions
    os.chmod(env_path, 0o600)
    os.chown(env_path, 1001, 1001)  # n8n user UID:GID

    print(f"Successfully generated {env_path}")

if __name__ == '__main__':
    generate_env_file()
```

**Systemd Service Integration**

```ini
# /etc/systemd/system/n8n-env-loader.service
[Unit]
Description=Load N8N environment from AWS Secrets Manager
Before=n8n.service

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 /opt/n8n/scripts/load-env-from-aws.py
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

```ini
# Update /etc/systemd/system/n8n.service
[Unit]
Description=N8N Workflow Automation
After=network.target postgresql.service redis.service n8n-env-loader.service
Requires=n8n-env-loader.service
```

### 4.3 Azure Key Vault Integration

#### 4.3.1 Store Secrets in Azure Key Vault

```bash
# Install Azure CLI
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Create Key Vault (if not exists)
az keyvault create \
  --name n8n-production-kv \
  --resource-group n8n-rg \
  --location eastus

# Store secrets
az keyvault secret set \
  --vault-name n8n-production-kv \
  --name db-password \
  --value "$(openssl rand -base64 48)"

az keyvault secret set \
  --vault-name n8n-production-kv \
  --name encryption-key \
  --value "$(openssl rand -base64 32)"

az keyvault secret set \
  --vault-name n8n-production-kv \
  --name basic-auth-password \
  --value "$(openssl rand -base64 32)"
```

#### 4.3.2 N8N Integration with Azure Key Vault

**Python Script to Fetch Secrets**

```python
#!/usr/bin/env python3
# /opt/n8n/scripts/load-env-from-azure.py

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import os

def get_secrets(vault_url):
    """Retrieve secrets from Azure Key Vault"""
    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=vault_url, credential=credential)

    return {
        'db_password': client.get_secret('db-password').value,
        'encryption_key': client.get_secret('encryption-key').value,
        'basic_auth_password': client.get_secret('basic-auth-password').value
    }

def generate_env_file():
    """Generate .env file from Azure Key Vault"""
    vault_url = "https://n8n-production-kv.vault.azure.net/"
    secrets = get_secrets(vault_url)

    env_content = f"""DB_TYPE=postgresdb
DB_HOST=hx-postgres-server.hx.dev.local
DB_PORT=5432
DB_DATABASE=n8n
DB_USERNAME=n8n
DB_PASSWORD={secrets['db_password']}
ENCRYPTION_KEY={secrets['encryption_key']}
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD={secrets['basic_auth_password']}
N8N_HOST=n8n.hx.dev.local
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.hx.dev.local/
"""

    # Write .env file
    env_path = '/opt/n8n/.env'
    with open(env_path, 'w') as f:
        f.write(env_content)

    # Set permissions
    os.chmod(env_path, 0o600)
    os.chown(env_path, 1001, 1001)  # n8n user UID:GID

    print(f"Successfully generated {env_path}")

if __name__ == '__main__':
    generate_env_file()
```

**Required Python Packages**

```bash
# Install Azure SDK
pip install azure-identity azure-keyvault-secrets

# Configure Managed Identity (Azure VM)
# OR configure Service Principal credentials
export AZURE_CLIENT_ID="<client-id>"
export AZURE_CLIENT_SECRET="<client-secret>"
export AZURE_TENANT_ID="<tenant-id>"
```

### 4.4 Migration Path from .env Files to Secret Managers

#### Phase 1: Audit Current .env Files

```bash
#!/bin/bash
# audit-env-files.sh

echo "=== Auditing .env Files ==="

# Find all .env files
find /opt/n8n -name ".env" -type f | while read env_file; do
    echo "File: $env_file"
    echo "Permissions: $(stat -c "%a" "$env_file")"
    echo "Owner: $(stat -c "%U:%G" "$env_file")"
    echo "Variables:"
    grep -E '^[A-Z_]+=' "$env_file" | cut -d= -f1 | sed 's/^/  - /'
    echo ""
done
```

#### Phase 2: Extract Variables to Secret Manager

```bash
#!/bin/bash
# migrate-to-vault.sh

set -e

ENV_FILE="/opt/n8n/.env"
VAULT_PATH="n8n/config"

# Load .env file
source "$ENV_FILE"

# Store in Vault
vault kv put "$VAULT_PATH" \
  db_password="$DB_PASSWORD" \
  encryption_key="$ENCRYPTION_KEY" \
  basic_auth_password="$N8N_BASIC_AUTH_PASSWORD"

# Backup original .env
cp "$ENV_FILE" "${ENV_FILE}.backup.$(date +%Y%m%d%H%M%S)"

echo "Migration complete. Original .env backed up."
echo "Test Vault integration before removing .env file."
```

#### Phase 3: Test Secret Manager Integration

```bash
# Test secret retrieval
/opt/n8n/scripts/load-env-from-vault.sh

# Verify .env was generated correctly
sudo -u n8n cat /opt/n8n/.env

# Test N8N startup
sudo systemctl restart n8n
sudo systemctl status n8n

# Verify N8N can read secrets
curl -u admin:$(vault kv get -field=basic_auth_password n8n/config) \
  https://n8n.hx.dev.local/
```

#### Phase 4: Remove .env Files

```bash
# Remove original .env (keep backup)
sudo rm /opt/n8n/.env

# Verify N8N still works with Vault-generated .env
sudo systemctl restart n8n
sudo systemctl status n8n
```

---

## 5. Validation Checks and Automated Testing

### 5.1 .env Format Validation Script

```bash
#!/bin/bash
# /opt/n8n/scripts/validate-env.sh

set -e

ENV_FILE="${1:-/opt/n8n/.env}"
EXIT_CODE=0

echo "=== Validating $ENV_FILE ==="

# Check file exists
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: File not found: $ENV_FILE"
    exit 1
fi

# Check permissions
PERMS=$(stat -c "%a" "$ENV_FILE")
if [ "$PERMS" != "600" ]; then
    echo "ERROR: Incorrect permissions. Expected: 600, Actual: $PERMS"
    EXIT_CODE=1
fi

# Check ownership
OWNER=$(stat -c "%U:%G" "$ENV_FILE")
if [ "$OWNER" != "n8n:n8n" ]; then
    echo "ERROR: Incorrect ownership. Expected: n8n:n8n, Actual: $OWNER"
    EXIT_CODE=1
fi

# Validate syntax (no syntax errors)
if ! grep -E '^([A-Z_][A-Z0-9_]*=.*|^#.*|^$)' "$ENV_FILE" > /dev/null; then
    echo "ERROR: Invalid .env syntax detected"
    EXIT_CODE=1
fi

# Check for required variables
REQUIRED_VARS=(
    "DB_TYPE"
    "DB_HOST"
    "DB_PORT"
    "DB_DATABASE"
    "DB_USERNAME"
    "DB_PASSWORD"
    "ENCRYPTION_KEY"
    "N8N_BASIC_AUTH_USER"
    "N8N_BASIC_AUTH_PASSWORD"
)

for var in "${REQUIRED_VARS[@]}"; do
    if ! grep -q "^${var}=" "$ENV_FILE"; then
        echo "ERROR: Missing required variable: $var"
        EXIT_CODE=1
    fi
done

# Check for placeholder values
if grep -qE '(CHANGEME|REPLACE|TODO|FIXME|XXX)' "$ENV_FILE"; then
    echo "ERROR: Placeholder values detected. Replace with actual values."
    grep -E '(CHANGEME|REPLACE|TODO|FIXME|XXX)' "$ENV_FILE"
    EXIT_CODE=1
fi

# Validate password strength (minimum 20 characters)
while IFS= read -r line; do
    if [[ "$line" =~ ^[A-Z_]*PASSWORD= ]]; then
        password_value="${line#*=}"
        if [ ${#password_value} -lt 20 ]; then
            echo "WARNING: Weak password detected (< 20 characters): ${line%%=*}"
            EXIT_CODE=2
        fi
    fi
done < "$ENV_FILE"

# Validate URLs
if grep -q "^WEBHOOK_URL=" "$ENV_FILE"; then
    WEBHOOK_URL=$(grep "^WEBHOOK_URL=" "$ENV_FILE" | cut -d= -f2-)
    if ! [[ "$WEBHOOK_URL" =~ ^https?:// ]]; then
        echo "ERROR: Invalid WEBHOOK_URL format: $WEBHOOK_URL"
        EXIT_CODE=1
    fi
fi

if [ $EXIT_CODE -eq 0 ]; then
    echo "SUCCESS: $ENV_FILE validation passed"
elif [ $EXIT_CODE -eq 2 ]; then
    echo "WARNING: $ENV_FILE validation passed with warnings"
else
    echo "FAILURE: $ENV_FILE validation failed"
fi

exit $EXIT_CODE
```

### 5.2 Required Variable Checklist

```yaml
# /opt/n8n/config/env-requirements.yaml
required_variables:
  database:
    - DB_TYPE
    - DB_HOST
    - DB_PORT
    - DB_DATABASE
    - DB_USERNAME
    - DB_PASSWORD

  encryption:
    - ENCRYPTION_KEY

  authentication:
    - N8N_BASIC_AUTH_USER
    - N8N_BASIC_AUTH_PASSWORD

  networking:
    - N8N_HOST
    - N8N_PORT
    - N8N_PROTOCOL
    - WEBHOOK_URL

optional_variables:
  email:
    - N8N_EMAIL_MODE
    - N8N_SMTP_HOST
    - N8N_SMTP_PORT

  performance:
    - EXECUTIONS_DATA_SAVE_ON_SUCCESS
    - EXECUTIONS_DATA_SAVE_ON_ERROR

  security:
    - N8N_SECURE_COOKIE
    - N8N_JWT_SECRET

validation_rules:
  DB_PORT:
    type: integer
    range: [1, 65535]

  DB_PASSWORD:
    min_length: 20
    pattern: "^[A-Za-z0-9!@#$%^&*-_+=]+$"

  ENCRYPTION_KEY:
    min_length: 32
    pattern: "^[A-Za-z0-9+/=]+$"

  WEBHOOK_URL:
    pattern: "^https?://[^/]+/$"
```

### 5.3 Value Format Validation

```python
#!/usr/bin/env python3
# /opt/n8n/scripts/validate-env-advanced.py

import re
import sys
from pathlib import Path

class EnvValidator:
    def __init__(self, env_file):
        self.env_file = Path(env_file)
        self.errors = []
        self.warnings = []

    def validate(self):
        """Run all validation checks"""
        if not self.env_file.exists():
            self.errors.append(f"File not found: {self.env_file}")
            return False

        self.check_permissions()
        self.check_syntax()
        self.check_required_vars()
        self.check_value_formats()

        return len(self.errors) == 0

    def check_permissions(self):
        """Check file permissions and ownership"""
        stat = self.env_file.stat()
        perms = oct(stat.st_mode)[-3:]

        if perms != '600':
            self.errors.append(f"Incorrect permissions: {perms} (expected 600)")

    def check_syntax(self):
        """Validate .env file syntax"""
        valid_line_pattern = re.compile(r'^([A-Z_][A-Z0-9_]*=.*|#.*|)$')

        with open(self.env_file) as f:
            for i, line in enumerate(f, 1):
                line = line.rstrip('\n')
                if not valid_line_pattern.match(line):
                    self.errors.append(f"Line {i}: Invalid syntax: {line}")

    def check_required_vars(self):
        """Check for required variables"""
        required = [
            'DB_TYPE', 'DB_HOST', 'DB_PORT', 'DB_DATABASE',
            'DB_USERNAME', 'DB_PASSWORD', 'ENCRYPTION_KEY',
            'N8N_BASIC_AUTH_USER', 'N8N_BASIC_AUTH_PASSWORD'
        ]

        with open(self.env_file) as f:
            content = f.read()

        for var in required:
            if not re.search(f'^{var}=', content, re.MULTILINE):
                self.errors.append(f"Missing required variable: {var}")

    def check_value_formats(self):
        """Validate value formats"""
        with open(self.env_file) as f:
            for line in f:
                line = line.strip()
                if '=' not in line or line.startswith('#'):
                    continue

                key, value = line.split('=', 1)

                # Validate DB_PORT
                if key == 'DB_PORT':
                    if not value.isdigit() or not (1 <= int(value) <= 65535):
                        self.errors.append(f"Invalid DB_PORT: {value}")

                # Validate passwords
                if 'PASSWORD' in key:
                    if len(value) < 20:
                        self.warnings.append(f"Weak {key}: length < 20")
                    if 'CHANGEME' in value or 'TODO' in value:
                        self.errors.append(f"Placeholder value in {key}")

                # Validate URLs
                if 'URL' in key or key.endswith('_HOST'):
                    if key == 'WEBHOOK_URL':
                        if not re.match(r'^https?://[^/]+/$', value):
                            self.errors.append(f"Invalid {key} format: {value}")

                # Validate booleans
                if key in ['N8N_SECURE_COOKIE', 'EXECUTIONS_DATA_SAVE_ON_SUCCESS']:
                    if value.lower() not in ['true', 'false']:
                        self.errors.append(f"Invalid boolean value for {key}: {value}")

    def report(self):
        """Print validation report"""
        print(f"=== Validation Report: {self.env_file} ===")

        if self.errors:
            print("\nERRORS:")
            for error in self.errors:
                print(f"  ❌ {error}")

        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  ⚠️  {warning}")

        if not self.errors and not self.warnings:
            print("\n✅ All checks passed")
            return 0
        elif not self.errors:
            print("\n⚠️  Validation passed with warnings")
            return 2
        else:
            print("\n❌ Validation failed")
            return 1

if __name__ == '__main__':
    env_file = sys.argv[1] if len(sys.argv) > 1 else '/opt/n8n/.env'
    validator = EnvValidator(env_file)
    validator.validate()
    sys.exit(validator.report())
```

### 5.4 Automated Validation in CI/CD

#### GitLab CI Example

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - deploy

validate-env:
  stage: validate
  image: ubuntu:24.04
  script:
    - apt-get update && apt-get install -y python3
    - python3 /opt/n8n/scripts/validate-env-advanced.py .env.example
  only:
    changes:
      - .env.example
  allow_failure: false

deploy-n8n:
  stage: deploy
  dependencies:
    - validate-env
  script:
    - ansible-playbook -i inventory deploy-n8n.yml
  only:
    - main
```

#### GitHub Actions Example

```yaml
# .github/workflows/validate-env.yml
name: Validate Environment Files

on:
  pull_request:
    paths:
      - '.env.example'
      - 'scripts/validate-env*.py'

jobs:
  validate:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v3

      - name: Validate .env.example
        run: |
          python3 scripts/validate-env-advanced.py .env.example

      - name: Check for hardcoded credentials
        run: |
          if grep -r "password\s*=\s*[^(CHANGEME|REPLACE)]" .; then
            echo "ERROR: Hardcoded credentials detected"
            exit 1
          fi
```

---

## 6. Password Manager Usage

### 6.1 1Password Integration

#### Store N8N Credentials in 1Password

```bash
# Install 1Password CLI
wget https://downloads.1password.com/linux/debian/amd64/stable/1password-cli-amd64-latest.deb
sudo dpkg -i 1password-cli-amd64-latest.deb

# Sign in to 1Password
op signin

# Create item
op item create \
  --category=Login \
  --title="N8N Production" \
  --vault="Infrastructure" \
  --field="username=n8n" \
  --field="db_password=$(openssl rand -base64 48)" \
  --field="encryption_key=$(openssl rand -base64 32)" \
  --field="basic_auth_password=$(openssl rand -base64 32)"

# Retrieve credentials
DB_PASSWORD=$(op item get "N8N Production" --fields db_password)
ENCRYPTION_KEY=$(op item get "N8N Production" --fields encryption_key)
BASIC_AUTH_PASSWORD=$(op item get "N8N Production" --fields basic_auth_password)
```

#### Generate .env from 1Password

```bash
#!/bin/bash
# /opt/n8n/scripts/load-env-from-1password.sh

set -e

# Authenticate to 1Password
export OP_SESSION=$(op signin --raw)

# Generate .env file
cat > /opt/n8n/.env << EOF
DB_TYPE=postgresdb
DB_HOST=hx-postgres-server.hx.dev.local
DB_PORT=5432
DB_DATABASE=n8n
DB_USERNAME=n8n
DB_PASSWORD=$(op item get "N8N Production" --fields db_password)
ENCRYPTION_KEY=$(op item get "N8N Production" --fields encryption_key)
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=$(op item get "N8N Production" --fields basic_auth_password)
N8N_HOST=n8n.hx.dev.local
N8N_PORT=5678
N8N_PROTOCOL=https
WEBHOOK_URL=https://n8n.hx.dev.local/
EOF

# Set permissions
chmod 600 /opt/n8n/.env
chown n8n:n8n /opt/n8n/.env

echo "Successfully generated /opt/n8n/.env from 1Password"
```

### 6.2 LastPass Integration

```bash
# Install LastPass CLI
sudo apt-get install lastpass-cli

# Login
lpass login user@example.com

# Store credentials
lpass add "N8N Production" --non-interactive <<EOF
Username: n8n
Password: $(openssl rand -base64 48)
URL: https://n8n.hx.dev.local
DB_Password: $(openssl rand -base64 48)
Encryption_Key: $(openssl rand -base64 32)
EOF

# Retrieve credentials
DB_PASSWORD=$(lpass show "N8N Production" --field=DB_Password)
ENCRYPTION_KEY=$(lpass show "N8N Production" --field=Encryption_Key)
```

### 6.3 Bitwarden Integration

```bash
# Install Bitwarden CLI
sudo snap install bw

# Login
bw login user@example.com

# Unlock vault
export BW_SESSION=$(bw unlock --raw)

# Create item
bw create item <<EOF
{
  "organizationId": null,
  "collectionIds": null,
  "folderId": null,
  "type": 1,
  "name": "N8N Production",
  "notes": "N8N production credentials",
  "favorite": false,
  "fields": [
    {"name": "db_password", "value": "$(openssl rand -base64 48)", "type": 0},
    {"name": "encryption_key", "value": "$(openssl rand -base64 32)", "type": 0},
    {"name": "basic_auth_password", "value": "$(openssl rand -base64 32)", "type": 0}
  ],
  "login": {
    "username": "n8n",
    "password": "$(openssl rand -base64 48)",
    "totp": null
  }
}
EOF

# Retrieve credentials
DB_PASSWORD=$(bw get item "N8N Production" | jq -r '.fields[] | select(.name=="db_password").value')
```

### 6.4 Team Sharing Best Practices

#### Access Control
- Use team vaults/collections for shared credentials
- Implement least-privilege access (only admins access production credentials)
- Require MFA for password manager access
- Regularly audit access logs

#### Onboarding/Offboarding
```bash
# Onboarding: Grant access to team vault
op vault user grant "Infrastructure" user@example.com

# Offboarding: Revoke access and rotate credentials
op vault user revoke "Infrastructure" former-employee@example.com

# Rotate ALL credentials after employee departure
./scripts/rotate-all-credentials.sh
```

### 6.5 Access Audit Trails

```bash
# 1Password: View access logs
op events list --event-type=ItemUsage --vault="Infrastructure"

# LastPass: Export audit log
lpass export-audit-log

# Bitwarden: Organization event logs (via web UI)
# https://vault.bitwarden.com/#/organizations/<org-id>/events
```

---

## 7. Credential Rotation Policy

### 7.1 Rotation Frequency

| Environment | Password Type | Rotation Frequency | Automation |
|-------------|---------------|-------------------|------------|
| Production  | Database      | 90 days           | Required   |
| Production  | API Keys      | 90 days           | Required   |
| Production  | Encryption    | 180 days          | Manual     |
| Staging     | All           | 180 days          | Optional   |
| Development | All           | Annual            | Optional   |

### 7.2 Zero-Downtime Rotation Procedure

#### Database Password Rotation

```bash
#!/bin/bash
# /opt/n8n/scripts/rotate-db-password.sh

set -e

DB_NAME="n8n"
DB_USER="n8n"
DB_HOST="hx-postgres-server.hx.dev.local"

# Generate new password
NEW_PASSWORD=$(openssl rand -base64 48)

# Update PostgreSQL password (Quinn Davis coordinates this)
PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" psql -h "$DB_HOST" -U postgres <<EOF
ALTER USER $DB_USER WITH PASSWORD '$NEW_PASSWORD';
EOF

# Update .env file (atomic replacement)
TEMP_ENV=$(mktemp)
sed "s/^DB_PASSWORD=.*/DB_PASSWORD=$NEW_PASSWORD/" /opt/n8n/.env > "$TEMP_ENV"
chmod 600 "$TEMP_ENV"
chown n8n:n8n "$TEMP_ENV"
mv "$TEMP_ENV" /opt/n8n/.env

# Restart N8N (graceful restart with connection draining)
systemctl reload n8n || systemctl restart n8n

# Verify connection
sleep 5
if systemctl is-active --quiet n8n; then
    echo "SUCCESS: Database password rotated"

    # Update secret manager
    vault kv put n8n/config db_password="$NEW_PASSWORD"
else
    echo "ERROR: N8N failed to start after password rotation"
    exit 1
fi
```

#### Encryption Key Rotation (Requires Data Re-encryption)

```bash
#!/bin/bash
# /opt/n8n/scripts/rotate-encryption-key.sh
# WARNING: This requires re-encrypting all existing credentials

set -e

# Generate new encryption key
NEW_KEY=$(openssl rand -base64 32)
OLD_KEY=$(grep "^ENCRYPTION_KEY=" /opt/n8n/.env | cut -d= -f2)

# Backup database before rotation
pg_dump -h hx-postgres-server.hx.dev.local -U n8n n8n > /backup/n8n-pre-rotation-$(date +%Y%m%d).sql

# Update .env with new key
sed -i "s/^ENCRYPTION_KEY=.*/ENCRYPTION_KEY=$NEW_KEY/" /opt/n8n/.env

# N8N automatic re-encryption on next start
# (N8N detects key change and re-encrypts credentials)
systemctl restart n8n

# Monitor logs for re-encryption
journalctl -u n8n -f | grep -i "encryption"
```

### 7.3 Service Restart Coordination

#### Multi-Service Rotation

```bash
#!/bin/bash
# /opt/n8n/scripts/coordinated-rotation.sh

set -e

echo "=== Coordinated Credential Rotation ==="

# 1. Notify monitoring (Nathan Lewis) - disable alerts
curl -X POST http://alertmanager.hx.dev.local/api/v1/silences \
  -d '{"matchers":[{"name":"service","value":"n8n"}],"duration":"30m"}'

# 2. Rotate database password
./rotate-db-password.sh

# 3. Rotate Redis password (if applicable)
./rotate-redis-password.sh

# 4. Update secret manager
vault kv put n8n/config \
  db_password="$NEW_DB_PASSWORD" \
  redis_password="$NEW_REDIS_PASSWORD"

# 5. Restart dependent services
systemctl restart n8n
systemctl restart n8n-worker  # If using queue mode

# 6. Verify health
sleep 10
curl -f https://n8n.hx.dev.local/healthz || {
    echo "ERROR: Health check failed after rotation"
    exit 1
}

# 7. Re-enable monitoring alerts
curl -X DELETE http://alertmanager.hx.dev.local/api/v1/silences/<silence-id>

echo "SUCCESS: Coordinated rotation complete"
```

### 7.4 Rotation Audit Log

```bash
# /var/log/n8n/credential-rotation.log
# Format: TIMESTAMP | CREDENTIAL_TYPE | ROTATED_BY | STATUS

2025-11-09T12:00:00Z | DB_PASSWORD | william.torres@hx.dev.local | SUCCESS
2025-11-09T12:05:00Z | BASIC_AUTH_PASSWORD | william.torres@hx.dev.local | SUCCESS
2025-11-09T12:10:00Z | ENCRYPTION_KEY | william.torres@hx.dev.local | FAILED (manual intervention required)
```

### 7.5 Automated Rotation Scheduling

```bash
# /etc/cron.d/n8n-credential-rotation

# Rotate database password every 90 days (quarterly)
0 2 1 */3 * n8n /opt/n8n/scripts/rotate-db-password.sh >> /var/log/n8n/rotation.log 2>&1

# Reminder for manual encryption key rotation (every 180 days)
0 9 1 */6 * n8n echo "REMINDER: Rotate N8N encryption key" | mail -s "N8N Credential Rotation" admin@hx.dev.local
```

---

## 8. Compliance References

### 8.1 PCI-DSS Requirements

#### PCI-DSS 8.2.1: Password Complexity
**Requirement**: Passwords must be at least 7 characters and contain both numeric and alphabetic characters.

**N8N Implementation**:
- Minimum 32 characters (exceeds requirement)
- Alphanumeric + special characters
- Generated using cryptographically secure methods (openssl rand)

**Validation**:
```bash
# Check password meets PCI-DSS 8.2.1
password_length=${#DB_PASSWORD}
if [ $password_length -ge 7 ] && [[ "$DB_PASSWORD" =~ [0-9] ]] && [[ "$DB_PASSWORD" =~ [A-Za-z] ]]; then
    echo "✅ PCI-DSS 8.2.1 COMPLIANT"
else
    echo "❌ PCI-DSS 8.2.1 NON-COMPLIANT"
fi
```

#### PCI-DSS 8.2.4: Password Changes
**Requirement**: User passwords must be changed at least every 90 days.

**N8N Implementation**:
- Automated rotation script (Section 7.5)
- Rotation audit log
- Cron job for quarterly rotation

### 8.2 SOC 2 Requirements

#### SOC 2 CC6.1: Logical and Physical Access Controls
**Requirement**: The entity implements logical access security software, infrastructure, and architectures over protected information assets to protect them from security events to meet the entity's objectives.

**N8N Implementation**:
- File permissions: 600 (owner read/write only)
- Service user isolation (n8n user)
- Secrets stored in encrypted vault (HashiCorp Vault, AWS Secrets Manager)
- MFA required for secret manager access

**Audit Evidence**:
```bash
# Generate SOC 2 compliance report
cat > /tmp/soc2-compliance-report.txt << EOF
=== SOC 2 CC6.1 Compliance Report ===
Generated: $(date)

File Permissions:
$(ls -la /opt/n8n/.env)

Secret Manager: HashiCorp Vault
Vault Address: https://vault.hx.dev.local:8200
Encryption: AES-256-GCM

Access Controls:
- MFA Required: Yes
- Least Privilege: Yes
- Audit Logging: Enabled

Rotation Policy:
- Database Password: 90 days
- API Keys: 90 days
- Encryption Key: 180 days
EOF
```

### 8.3 NIST 800-53 Requirements

#### NIST 800-53 IA-5: Authenticator Management
**Control**: The organization manages information system authenticators by:
- Verifying the identity of the individual, group, role, or device receiving the authenticator
- Establishing initial authenticator content
- Ensuring authenticators have sufficient strength for their intended use

**N8N Implementation**:
- Initial credentials generated using FIPS 140-2 compliant method (openssl)
- Password strength: 48 characters (entropy: ~288 bits)
- Secure storage: File permissions 600, encryption at rest (Vault)

#### NIST 800-53 IA-5(1): Password-Based Authentication
**Control**: For password-based authentication:
- Enforce minimum password complexity
- Store and transmit passwords in protected form
- Obscure feedback of authentication information

**N8N Implementation**:
```bash
# Password complexity enforcement
MIN_LENGTH=32
REQUIRED_CHAR_TYPES=4  # uppercase, lowercase, numbers, symbols

# Encrypted transmission (HTTPS only)
N8N_PROTOCOL=https

# Encrypted storage (Vault with AES-256)
vault kv put n8n/config db_password="<encrypted>"
```

### 8.4 GDPR Considerations

#### Article 32: Security of Processing
**Requirement**: Implement appropriate technical and organizational measures to ensure a level of security appropriate to the risk, including pseudonymization and encryption.

**N8N Implementation**:
- Encryption at rest (Vault, database encryption)
- Encryption in transit (TLS 1.3)
- Access controls (file permissions, MFA)
- Audit logging (credential access logs)

### 8.5 Compliance Checklist

```markdown
# N8N Environment Security Compliance Checklist

## PCI-DSS
- [x] 8.2.1: Password complexity (32+ chars, alphanumeric + symbols)
- [x] 8.2.4: Password rotation (90 days)
- [x] 8.2.5: Strong cryptographic methods (openssl rand)

## SOC 2
- [x] CC6.1: Logical access controls (600 permissions, service user)
- [x] CC6.7: Encryption at rest (Vault)
- [x] CC6.8: Encryption in transit (TLS 1.3)

## NIST 800-53
- [x] IA-5: Authenticator management (secure generation, rotation)
- [x] IA-5(1): Password-based authentication (complexity, encrypted storage)
- [x] SC-13: Cryptographic protection (AES-256, TLS 1.3)

## GDPR
- [x] Article 32: Security of processing (encryption, access controls, audit logs)

## Internal Policies
- [x] .env files excluded from version control
- [x] Secrets stored in enterprise secret manager
- [x] MFA required for secret access
- [x] Quarterly credential rotation
```

---

## 9. .env Format Validation

### 9.1 Syntax Checker Script (Bash)

```bash
#!/bin/bash
# /opt/n8n/scripts/validate-env-syntax.sh

set -e

ENV_FILE="${1:-/opt/n8n/.env}"
LINE_NUMBER=0
ERRORS=0

echo "=== Validating .env syntax: $ENV_FILE ==="

while IFS= read -r line; do
    ((LINE_NUMBER++))

    # Skip empty lines
    if [ -z "$line" ]; then
        continue
    fi

    # Skip comments
    if [[ "$line" =~ ^# ]]; then
        continue
    fi

    # Valid line format: KEY=VALUE
    if ! [[ "$line" =~ ^[A-Z_][A-Z0-9_]*=.*$ ]]; then
        echo "ERROR: Line $LINE_NUMBER: Invalid syntax: $line"
        ((ERRORS++))
    fi

    # Check for unquoted spaces in values (common mistake)
    if [[ "$line" =~ =[^\"\']*[[:space:]]+[^\"\']*$ ]]; then
        echo "WARNING: Line $LINE_NUMBER: Unquoted space in value: $line"
    fi

    # Check for missing values
    if [[ "$line" =~ ^[A-Z_][A-Z0-9_]*=$ ]]; then
        echo "WARNING: Line $LINE_NUMBER: Empty value: $line"
    fi

done < "$ENV_FILE"

if [ $ERRORS -eq 0 ]; then
    echo "✅ Syntax validation passed"
    exit 0
else
    echo "❌ Syntax validation failed with $ERRORS errors"
    exit 1
fi
```

### 9.2 Common Format Errors

#### Error 1: Spaces Around Equals Sign
```bash
# WRONG
DB_PASSWORD = my_password

# CORRECT
DB_PASSWORD=my_password
```

#### Error 2: Unquoted Special Characters
```bash
# WRONG (causes shell expansion issues)
WEBHOOK_URL=https://n8n.hx.dev.local/webhook?token=abc123&user=admin

# CORRECT
WEBHOOK_URL="https://n8n.hx.dev.local/webhook?token=abc123&user=admin"
```

#### Error 3: Multiline Values Without Quotes
```bash
# WRONG
PRIVATE_KEY=-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQ...
-----END PRIVATE KEY-----

# CORRECT
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQ...
-----END PRIVATE KEY-----"
```

#### Error 4: Shell Metacharacters Without Escaping
```bash
# WRONG (backticks cause command execution)
DB_PASSWORD=my`password

# CORRECT
DB_PASSWORD="my\`password"
```

### 9.3 Validation Integration

#### Pre-deployment Validation Hook

```bash
#!/bin/bash
# /opt/n8n/hooks/pre-deploy.sh

set -e

echo "=== Pre-deployment validation ==="

# 1. Validate syntax
/opt/n8n/scripts/validate-env-syntax.sh /opt/n8n/.env

# 2. Validate advanced rules
/opt/n8n/scripts/validate-env-advanced.py /opt/n8n/.env

# 3. Check permissions
/opt/n8n/scripts/verify-env-permissions.sh

echo "✅ All pre-deployment checks passed"
```

#### Ansible Playbook Integration

```yaml
# ansible/tasks/validate-env.yml
- name: Validate .env syntax
  command: /opt/n8n/scripts/validate-env-syntax.sh /opt/n8n/.env
  register: syntax_check
  failed_when: syntax_check.rc != 0

- name: Validate .env advanced rules
  command: /opt/n8n/scripts/validate-env-advanced.py /opt/n8n/.env
  register: advanced_check
  failed_when: advanced_check.rc == 1

- name: Verify .env permissions
  stat:
    path: /opt/n8n/.env
  register: env_stat
  failed_when: env_stat.stat.mode != '0600'
```

---

## 10. Troubleshooting Common Issues

### 10.1 Permission Denied Errors

#### Symptom
```
Error: EACCES: permission denied, open '/opt/n8n/.env'
```

#### Diagnosis
```bash
# Check file permissions
ls -la /opt/n8n/.env

# Check file ownership
stat -c "%U:%G" /opt/n8n/.env

# Check process user
ps aux | grep n8n | grep -v grep
```

#### Resolution
```bash
# Fix ownership
sudo chown n8n:n8n /opt/n8n/.env

# Fix permissions
sudo chmod 600 /opt/n8n/.env

# Verify n8n service user
sudo -u n8n cat /opt/n8n/.env
```

### 10.2 Variable Not Loaded Errors

#### Symptom
```
Error: Environment variable DB_PASSWORD is not set
```

#### Diagnosis
```bash
# Check variable exists in .env
grep "^DB_PASSWORD=" /opt/n8n/.env

# Check variable is loaded by N8N
sudo -u n8n env | grep DB_PASSWORD

# Check systemd EnvironmentFile
systemctl cat n8n | grep EnvironmentFile
```

#### Resolution

**Option 1: Fix EnvironmentFile in systemd unit**
```ini
# /etc/systemd/system/n8n.service
[Service]
EnvironmentFile=/opt/n8n/.env
```

**Option 2: Explicit environment variables**
```ini
# /etc/systemd/system/n8n.service
[Service]
Environment="DB_PASSWORD=<value>"
```

**Option 3: Use dotenv library (Node.js)**
```javascript
// In N8N startup script
require('dotenv').config({ path: '/opt/n8n/.env' });
```

### 10.3 Special Character Escaping

#### Symptom
```
Error: Unexpected token in .env file
Syntax error near unexpected token `&'
```

#### Diagnosis
```bash
# Check for unescaped special characters
grep '[`$"\\&|;<>()]' /opt/n8n/.env
```

#### Resolution

**Shell-safe escaping**:
```bash
# WRONG
DB_PASSWORD=my&password

# CORRECT (quoted)
DB_PASSWORD="my&password"

# CORRECT (escaped)
DB_PASSWORD=my\&password
```

**Characters requiring escaping**:
- ` (backtick) - command substitution
- $ (dollar) - variable expansion
- " (double quote) - string delimiter
- \ (backslash) - escape character
- & (ampersand) - background process
- | (pipe) - command pipe
- ; (semicolon) - command separator
- < > (redirection) - input/output redirection
- ( ) (parentheses) - subshell

### 10.4 Multiline Value Handling

#### Symptom
```
Error: Unexpected end of file in .env
```

#### Diagnosis
```bash
# Check for multiline values
grep -A 5 "BEGIN" /opt/n8n/.env
```

#### Resolution

**Correct multiline format**:
```bash
# Option 1: Quoted multiline (preferred)
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
MIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQ...
-----END PRIVATE KEY-----"

# Option 2: Single line with \n
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvgIB...\n-----END PRIVATE KEY-----"

# Option 3: Base64 encoded (recommended for binary data)
PRIVATE_KEY_B64="LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUV2Z0lCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktn..."
```

### 10.5 .env File Not Found

#### Symptom
```
Error: ENOENT: no such file or directory, open '/opt/n8n/.env'
```

#### Diagnosis
```bash
# Check file exists
test -f /opt/n8n/.env && echo "EXISTS" || echo "NOT FOUND"

# Check working directory
pwd

# Check N8N startup directory
systemctl cat n8n | grep WorkingDirectory
```

#### Resolution
```bash
# Create .env file
sudo touch /opt/n8n/.env
sudo chmod 600 /opt/n8n/.env
sudo chown n8n:n8n /opt/n8n/.env

# Verify path in systemd unit
sudo systemctl cat n8n | grep -E '(WorkingDirectory|EnvironmentFile)'

# Use absolute path in EnvironmentFile
EnvironmentFile=/opt/n8n/.env
```

### 10.6 Stale Credentials After Rotation

#### Symptom
```
Error: password authentication failed for user "n8n"
```

#### Diagnosis
```bash
# Check if .env was updated
stat /opt/n8n/.env

# Check if N8N process reloaded .env
systemctl status n8n | grep "Active"

# Check database password was actually changed
sudo -u postgres psql -c "\du n8n"
```

#### Resolution
```bash
# 1. Verify .env file has new password
grep "^DB_PASSWORD=" /opt/n8n/.env

# 2. Restart N8N to reload .env
sudo systemctl restart n8n

# 3. Verify database connection
sudo -u n8n psql -h hx-postgres-server.hx.dev.local -U n8n -d n8n -c "SELECT 1;"

# 4. If still failing, check database password
sudo -u postgres psql -h hx-postgres-server.hx.dev.local -c "ALTER USER n8n WITH PASSWORD '<new-password>';"
```

### 10.7 Emergency Recovery Checklist

```markdown
# .env Emergency Recovery Checklist

## Scenario: Lost .env file

1. [ ] Check backups
   - /backup/n8n/.env.*
   - Vault/secret manager
   - Configuration management (Ansible)

2. [ ] Regenerate from secret manager
   - `./scripts/load-env-from-vault.sh`
   - `./scripts/load-env-from-1password.sh`

3. [ ] Recreate from documentation
   - Use .env.example as template
   - Generate new passwords: `openssl rand -base64 48`
   - Update database credentials (coordinate with Quinn Davis)

4. [ ] Restore service
   - Set permissions: `chmod 600 /opt/n8n/.env`
   - Set ownership: `chown n8n:n8n /opt/n8n/.env`
   - Restart N8N: `systemctl restart n8n`

## Scenario: Corrupted .env file

1. [ ] Stop N8N service
   - `systemctl stop n8n`

2. [ ] Backup corrupted file
   - `cp /opt/n8n/.env /tmp/env.corrupted.$(date +%s)`

3. [ ] Restore from backup
   - `cp /backup/n8n/.env.latest /opt/n8n/.env`

4. [ ] Validate restored file
   - `./scripts/validate-env-advanced.py /opt/n8n/.env`

5. [ ] Restart service
   - `systemctl start n8n`
```

---

## Appendix A: Quick Reference

### Password Generation One-Liners

```bash
# 32-character secure password
openssl rand -base64 32

# 48-character secure password (recommended)
openssl rand -base64 48

# Shell-safe password (no metacharacters)
openssl rand -base64 48 | tr -d '\n' | sed 's/[`$"\\]//g'

# Alphanumeric only (64 characters)
openssl rand -hex 32
```

### Permission Commands

```bash
# Set .env permissions
sudo chmod 600 /opt/n8n/.env
sudo chown n8n:n8n /opt/n8n/.env

# Verify permissions
ls -la /opt/n8n/.env

# Batch fix permissions
find /opt/n8n -name ".env*" -exec chmod 600 {} \;
find /opt/n8n -name ".env*" -exec chown n8n:n8n {} \;
```

### Validation Commands

```bash
# Syntax validation
/opt/n8n/scripts/validate-env-syntax.sh /opt/n8n/.env

# Advanced validation
/opt/n8n/scripts/validate-env-advanced.py /opt/n8n/.env

# Permission verification
/opt/n8n/scripts/verify-env-permissions.sh
```

---

## Appendix B: Security Incident Response

### If .env File is Compromised

1. **Immediate Actions** (within 1 hour):
   - Rotate ALL credentials in .env file
   - Review access logs for unauthorized access
   - Notify security team and service owners
   - Revoke compromised credentials in database

2. **Investigation** (within 24 hours):
   - Determine scope of compromise (who, when, what)
   - Review git history for accidental commits
   - Check monitoring logs for suspicious activity
   - Identify attack vector

3. **Remediation** (within 48 hours):
   - Implement additional access controls
   - Update incident response procedures
   - Conduct security training for team
   - Migrate to enterprise secret manager if not already

4. **Post-Incident** (within 1 week):
   - Document incident in security log
   - Update compliance documentation
   - Schedule security audit
   - Review and update this guide

---

## Document Metadata

```yaml
document_type: Security Best Practices Guide
version: 1.0
date: 2025-11-09
project: POC3 N8N Deployment
author: William Torres, Systems Administrator Specialist
classification: Internal - Confidential
review_frequency: Quarterly
next_review_date: 2026-02-09
related_documents:
  - p3-tasks/p3.3-deploy/t-032-create-env-file.md
  - p7-post-deployment/EXIT-CODE-STANDARD.md
compliance_frameworks:
  - PCI-DSS
  - SOC 2
  - NIST 800-53
  - GDPR
```

---

**End of Document**
