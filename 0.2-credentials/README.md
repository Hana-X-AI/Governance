# Credentials Directory
**Purpose**: Centralized credential storage for Hana-X infrastructure

## Contents

- `hx-credentials.md` - ALL credentials for hx.dev.local environment

## Security Notice

⚠️ **DEVELOPMENT ENVIRONMENT ONLY**

These credentials are for the hx.dev.local development environment and use simplified security:
- Standard password: Major8859! (used for all service accounts)
- Domain admin: Administrator@HX.DEV.LOCAL / Major3059!
- CA passphrase: Longhorn88

**DO NOT** use these credentials in production environments.

## Usage

All agents reference this directory for authentication credentials. Never hardcode credentials in agent profiles or operational procedures.

**Reference Pattern**:
```markdown
**Credentials**: See `/srv/cc/Governance/0.2-credentials/hx-credentials.md`
```

## Production Migration

When moving to production:
- ✅ Generate unique passwords for each service (16+ characters)
- ✅ Use secrets management (HashiCorp Vault, AWS Secrets Manager)
- ✅ Enable MFA for administrative accounts
- ✅ Implement password rotation (90 days)
- ✅ Audit credential usage
