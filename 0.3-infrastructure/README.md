# Infrastructure Procedures
**Purpose**: Core infrastructure operations referenced by all agents

## Contents

- `ldap-domain-integration.md` - Domain user creation and SSSD configuration
- `dns-management.md` - DNS record management via samba-tool
- `ssl-tls-deployment.md` - SSL/TLS certificate generation and deployment
- `network-configuration.md` - Netplan, routing, firewall rules (TODO)
- `backup-recovery.md` - Infrastructure backup and disaster recovery (TODO)

## Usage

These procedures apply to ALL services across the 30-server infrastructure.

**Referenced by**:
- All service owner agents (for LDAP, DNS, SSL integration)
- Infrastructure agents (Frank, William, Amanda)
- Deployment procedures in 0.0-governance/

## Integration Workflow

For every new service deployment:
1. **LDAP/Domain Integration** (PRE-REQ-06) - Create domain service account
2. **DNS Registration** (DEPLOY-09) - Register hostname in DNS
3. **SSL/TLS Deployment** (DEPLOY-10) - Generate and deploy certificates (web services only)

See each procedure document for detailed step-by-step instructions.
