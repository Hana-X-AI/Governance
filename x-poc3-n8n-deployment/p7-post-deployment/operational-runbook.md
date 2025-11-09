# N8N Operational Runbook

**Service**: N8N Workflow Automation Platform
**Environment**: hx.dev.local (Production)
**Version**: 1.118.2
**Server**: hx-n8n-server (192.168.10.215)
**Last Updated**: November 8, 2025
**Classification**: Internal Use Only

---

## Quick Reference

**Primary URL**: `https://n8n.hx.dev.local`
**Service Name**: `n8n.service`
**Service User**: `n8n`
**Installation Path**: `/opt/n8n/app/compiled`
**Configuration**: `/opt/n8n/.env`
**Logs**: `journalctl -u n8n.service -f`

---

## Service Management

### Check Service Status

```bash
ssh hx-n8n-server.hx.dev.local
sudo systemctl status n8n.service
```

**Expected Output**:
```
● n8n.service - N8N Workflow Automation
     Loaded: loaded (/etc/systemd/system/n8n.service; enabled; preset: enabled)
     Active: active (running) since [timestamp]
```

---

### Start Service

```bash
sudo systemctl start n8n.service
```

**Verification**:
```bash
curl -k https://n8n.hx.dev.local/healthz
# Expected: {"status":"ok"}
```

---

### Stop Service

```bash
sudo systemctl stop n8n.service
```

**Use Case**: Planned maintenance, configuration changes

---

### Restart Service

```bash
sudo systemctl restart n8n.service
```

**Use Case**: After configuration changes, troubleshooting

---

### View Logs (Real-Time)

```bash
sudo journalctl -u n8n.service -f
```

**Exit**: Press `Ctrl+C`

---

### View Logs (Last 100 Lines)

```bash
sudo journalctl -u n8n.service -n 100 --no-pager
```

---

### View Logs (Specific Time Range)

```bash
sudo journalctl -u n8n.service --since "2025-11-08 10:00:00" --until "2025-11-08 11:00:00"
```

---

## Health Checks

### 1. Service Health Endpoint

```bash
curl -k https://n8n.hx.dev.local/healthz
```

**Expected Response**:
```json
{"status":"ok"}
```

**Response Time**: Should be < 2 seconds (target: < 100ms)

---

### 2. Database Connectivity

```bash
ssh hx-n8n-server.hx.dev.local
sudo -u n8n bash -c 'cd /opt/n8n/app/compiled && export $(sudo cat /opt/n8n/.env | grep -v "^#" | xargs) && node -e "const pg = require(\"pg\"); const client = new pg.Client({host: \"$DB_POSTGRESDB_HOST\", port: $DB_POSTGRESDB_PORT, database: \"$DB_POSTGRESDB_DATABASE\", user: \"$DB_POSTGRESDB_USER\", password: \"$DB_POSTGRESDB_PASSWORD\"}); client.connect().then(() => console.log(\"OK\")).catch(e => console.error(e)).finally(() => client.end());"'
```

**Expected Output**: `OK`

---

### 3. HTTPS Access

```bash
curl -I -k https://n8n.hx.dev.local
```

**Expected**:
```
HTTP/2 200
server: nginx/1.24.0 (Ubuntu)
```

---

### 4. HTTP Redirect

```bash
curl -I http://n8n.hx.dev.local
```

**Expected**:
```
HTTP/1.1 301 Moved Permanently
Location: https://n8n.hx.dev.local/
```

---

### 5. Memory Usage

```bash
ssh hx-n8n-server.hx.dev.local
ps aux | grep n8n | grep -v grep
```

**Expected**: RSS memory < 4GB (typically 300-500MB)

---

### 6. CPU Usage

```bash
ssh hx-n8n-server.hx.dev.local
top -b -n 1 | grep n8n
```

**Expected**: CPU < 10% (typically < 2% at idle)

---

## Configuration Management

### View Current Configuration

```bash
ssh hx-n8n-server.hx.dev.local
sudo cat /opt/n8n/.env
```

---

### Edit Configuration

```bash
ssh hx-n8n-server.hx.dev.local
sudo nano /opt/n8n/.env
```

**After editing**:
```bash
sudo systemctl restart n8n.service
```

---

### Verify Environment Variables Loaded

```bash
systemctl show n8n.service | grep Environment
```

---

### Key Configuration Parameters

| Parameter | Current Value | Purpose |
|-----------|---------------|---------|
| `DB_TYPE` | `postgresdb` | Database type |
| `DB_POSTGRESDB_HOST` | `hx-postgres-server.hx.dev.local` | PostgreSQL server |
| `DB_POSTGRESDB_PORT` | `5432` | PostgreSQL port |
| `DB_POSTGRESDB_DATABASE` | `n8n_poc3` | Database name |
| `DB_POSTGRESDB_USER` | `svc-n8n` | Database user |
| `DB_POSTGRESDB_PASSWORD` | `Major8859` | Database password (URL-safe) |
| `N8N_HOST` | `0.0.0.0` | Listen address |
| `N8N_PORT` | `5678` | Application port |
| `N8N_PROTOCOL` | `https` | External protocol |
| `WEBHOOK_URL` | `https://n8n.hx.dev.local/` | Webhook base URL |
| `N8N_EDITOR_BASE_URL` | `https://n8n.hx.dev.local/` | Editor URL |
| `N8N_ENCRYPTION_KEY` | `90c5323a349aba2913666c6b0f1b9f8dd3801ab23114fb658d8e58a87d02cdbc` | Data encryption |
| `EXECUTIONS_MODE` | `regular` | Execution mode |
| `N8N_LOG_LEVEL` | `info` | Log verbosity |
| `N8N_RUNNERS_ENABLED` | `true` | Task runners enabled |
| `N8N_RUNNERS_MODE` | `internal` | Runner mode |

---

## Database Operations

### Connect to N8N Database

```bash
ssh hx-postgres-server.hx.dev.local
PGPASSWORD='Major8859' psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3
```

---

### Check Database Tables

```sql
\dt
```

**Expected**: ~50 tables (workflow_entity, execution_entity, credentials_entity, etc.)

---

### Check Workflow Count

```sql
SELECT COUNT(*) FROM workflow_entity;
```

---

### Check Execution Count

```sql
SELECT COUNT(*) FROM execution_entity;
```

---

### Check Active Workflows

```sql
SELECT id, name, active FROM workflow_entity WHERE active = true;
```

---

### Database Backup

```bash
ssh hx-postgres-server.hx.dev.local
sudo -u postgres pg_dump n8n_poc3 > /tmp/n8n_poc3_backup_$(date +%Y%m%d_%H%M%S).sql
```

---

### Database Restore

```bash
ssh hx-postgres-server.hx.dev.local
sudo -u postgres psql n8n_poc3 < /path/to/backup.sql
```

---

## User Management

### Check Existing Users

```sql
-- Connect to database first
SELECT * FROM user;
```

---

### Current Users

| Email | Role | Status |
|-------|------|--------|
| `caio@hx.dev.local` | Owner | Active |

---

### Reset User Password (if needed)

**Note**: User passwords are managed within N8N UI. For password reset:

1. Log into N8N as owner
2. Go to Settings → Users
3. Select user → Reset Password

**Or via database** (emergency only):
```sql
-- This requires knowing N8N's password hashing mechanism
-- Contact N8N documentation for password reset procedures
```

---

## Troubleshooting

### Problem: Service Won't Start

**Check logs**:
```bash
sudo journalctl -u n8n.service -n 50 --no-pager
```

**Common Causes**:
1. Database connection failure
   - Check `DB_POSTGRESDB_*` variables in `/opt/n8n/.env`
   - Test database connectivity (see Health Checks section)
2. Port already in use
   - Check: `sudo ss -tlnp | grep 5678`
   - Kill conflicting process or change port
3. Invalid configuration
   - Review `/opt/n8n/.env` for syntax errors
   - Ensure no quotes around values in EnvironmentFile

**Resolution**:
```bash
# Fix configuration issue
sudo nano /opt/n8n/.env

# Reload daemon
sudo systemctl daemon-reload

# Restart service
sudo systemctl restart n8n.service
```

---

### Problem: Web UI Not Accessible

**Check Nginx**:
```bash
ssh hx-nginx-server
sudo systemctl status nginx
sudo nginx -t  # Test configuration
```

**Check N8N Service**:
```bash
ssh hx-n8n-server.hx.dev.local
sudo systemctl status n8n.service
curl http://localhost:5678/healthz  # Direct local check
```

**Check DNS**:
```bash
nslookup n8n.hx.dev.local
# Should return: 192.168.10.215
```

**Check Firewall**:
```bash
ssh hx-n8n-server.hx.dev.local
sudo ss -tlnp | grep 5678
```

---

### Problem: Database Connection Errors

**Verify Database is Running**:
```bash
ssh hx-postgres-server.hx.dev.local
sudo systemctl status postgresql
```

**Test Connection**:
```bash
PGPASSWORD='Major8859' psql -h hx-postgres-server.hx.dev.local -U svc-n8n -d n8n_poc3 -c "SELECT 1;"
```

**Check Credentials**:
```bash
# On hx-n8n-server
sudo cat /opt/n8n/.env | grep DB_POSTGRESDB
```

**Verify Password** (should be `Major8859` without `!`):
- If password has `!`, see "URL-Safe Password Pattern" in credentials documentation

---

### Problem: Slow Performance

**Check Memory**:
```bash
free -h
ps aux | grep n8n | grep -v grep
```

**Check CPU**:
```bash
top -b -n 1 | grep n8n
```

**Check Database Connections**:
```sql
-- On PostgreSQL server
SELECT count(*) FROM pg_stat_activity WHERE datname = 'n8n_poc3';
```

**Check Workflow Executions**:
```sql
-- Long-running executions
SELECT id, started_at, stopped_at, status FROM execution_entity
WHERE stopped_at IS NULL AND started_at < NOW() - INTERVAL '1 hour';
```

---

### Problem: Workflows Not Executing

**Check Active Workflows**:
```sql
SELECT id, name, active FROM workflow_entity WHERE active = true;
```

**Check Execution Logs**:
```bash
sudo journalctl -u n8n.service -f | grep -i execution
```

**Check Task Runners**:
```bash
# In logs, look for:
sudo journalctl -u n8n.service | grep -i runner
```

**Verify N8N_RUNNERS_ENABLED**:
```bash
sudo cat /opt/n8n/.env | grep N8N_RUNNERS
```

---

### Problem: SSL Certificate Errors

**Check Certificate**:
```bash
openssl s_client -connect n8n.hx.dev.local:443 < /dev/null
```

**Check Nginx Configuration**:
```bash
ssh hx-nginx-server
sudo cat /etc/nginx/sites-available/n8n.conf | grep ssl
```

**Renew Certificate** (if needed):
```bash
# Contact infrastructure team (Frank Delgado)
# Samba CA certificates managed centrally
```

---

## Monitoring and Alerts

### Key Metrics to Monitor

| Metric | Check Interval | Alert Threshold |
|--------|---------------|-----------------|
| Service Status | 1 minute | Down |
| Health Endpoint | 1 minute | > 2s response or non-200 |
| Memory Usage | 5 minutes | > 4GB |
| CPU Usage | 5 minutes | > 80% for 5min |
| Database Connections | 5 minutes | > 100 |
| Failed Executions | 15 minutes | > 10 in 15min |
| Disk Usage | 1 hour | > 80% |

---

### Health Check Script

```bash
#!/bin/bash
# /opt/scripts/n8n-health-check.sh

set -e

# Health endpoint
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -k https://n8n.hx.dev.local/healthz)
if [ "$HTTP_CODE" != "200" ]; then
    echo "CRITICAL: N8N health check failed (HTTP $HTTP_CODE)"
    exit 2
fi

# Service status
if ! systemctl is-active --quiet n8n.service; then
    echo "CRITICAL: N8N service is not running"
    exit 2
fi

# Memory check
MEM_MB=$(ps aux | grep '[n]8n start' | awk '{print $6}' | head -1)
MEM_GB=$((MEM_MB / 1024 / 1024))
if [ "$MEM_GB" -gt 4 ]; then
    echo "WARNING: N8N memory usage > 4GB"
    exit 1
fi

echo "OK: N8N is healthy"
exit 0
```

---

## Backup and Recovery

### Full Backup Procedure

```bash
#!/bin/bash
# Backup N8N configuration and database

BACKUP_DIR="/opt/backups/n8n"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup configuration
ssh hx-n8n-server.hx.dev.local "sudo cat /opt/n8n/.env" > $BACKUP_DIR/env_$DATE.backup

# Backup database
ssh hx-postgres-server.hx.dev.local "sudo -u postgres pg_dump n8n_poc3" > $BACKUP_DIR/n8n_poc3_$DATE.sql

# Backup systemd service file
ssh hx-n8n-server.hx.dev.local "sudo cat /etc/systemd/system/n8n.service" > $BACKUP_DIR/n8n.service_$DATE.backup

# Compress backups
tar -czf $BACKUP_DIR/n8n_full_backup_$DATE.tar.gz $BACKUP_DIR/*_$DATE.*

echo "Backup complete: $BACKUP_DIR/n8n_full_backup_$DATE.tar.gz"
```

---

### Recovery Procedure

```bash
#!/bin/bash
# Restore N8N from backup

BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    exit 1
fi

# Extract backup
tar -xzf $BACKUP_FILE

# Restore configuration
scp env_*.backup hx-n8n-server.hx.dev.local:/tmp/
ssh hx-n8n-server.hx.dev.local "sudo cp /tmp/env_*.backup /opt/n8n/.env"

# Restore database
cat n8n_poc3_*.sql | ssh hx-postgres-server.hx.dev.local "sudo -u postgres psql n8n_poc3"

# Restart service
ssh hx-n8n-server.hx.dev.local "sudo systemctl restart n8n.service"

echo "Recovery complete"
```

---

## Upgrade Procedure

### Pre-Upgrade Checklist

- [ ] Backup current installation (see Backup section)
- [ ] Review N8N release notes
- [ ] Schedule maintenance window
- [ ] Notify users
- [ ] Test upgrade in non-production environment first

---

### Upgrade Steps

```bash
#!/bin/bash
# Upgrade N8N to new version

NEW_VERSION="1.120.0"  # Update as needed

# 1. Stop service
ssh hx-n8n-server.hx.dev.local "sudo systemctl stop n8n.service"

# 2. Backup current version
ssh hx-n8n-server.hx.dev.local "sudo cp -r /opt/n8n/app/compiled /opt/n8n/app/compiled.backup"

# 3. Clone new version (on hx-n8n-server)
ssh hx-n8n-server.hx.dev.local << 'EOF'
cd /srv/n8n
git fetch
git checkout v$NEW_VERSION
EOF

# 4. Build new version
ssh hx-n8n-server.hx.dev.local << 'EOF'
cd /srv/n8n/n8n
sudo -u n8n HOME=/home/n8n pnpm install
sudo -u n8n HOME=/home/n8n pnpm build:deploy
EOF

# 5. Deploy to /opt/n8n
ssh hx-n8n-server.hx.dev.local << 'EOF'
sudo rm -rf /opt/n8n/app/compiled/*
sudo cp -r /srv/n8n/n8n/packages/cli/dist/* /opt/n8n/app/compiled/
sudo chown -R n8n:n8n /opt/n8n/app/compiled
EOF

# 6. Run database migrations (if any)
# Check N8N release notes for migration commands

# 7. Start service
ssh hx-n8n-server.hx.dev.local "sudo systemctl start n8n.service"

# 8. Verify
curl -k https://n8n.hx.dev.local/healthz

echo "Upgrade complete to version $NEW_VERSION"
```

---

### Rollback Procedure

```bash
ssh hx-n8n-server.hx.dev.local << 'EOF'
# Stop service
sudo systemctl stop n8n.service

# Restore previous version
sudo rm -rf /opt/n8n/app/compiled
sudo mv /opt/n8n/app/compiled.backup /opt/n8n/app/compiled
sudo chown -R n8n:n8n /opt/n8n/app/compiled

# Restore database (if migrations were run)
# Use backup from pre-upgrade

# Start service
sudo systemctl start n8n.service
EOF

echo "Rollback complete"
```

---

## Security

### Access Control

**Service Level**:
- Service runs as user `n8n` (non-root)
- Configuration file permissions: `600` (owner read/write only)

**Network Level**:
- Internal network only (hx.dev.local domain)
- HTTPS enforced
- HTTP redirects to HTTPS

**Database Level**:
- Dedicated service account: `svc-n8n`
- Limited permissions (CRUD on n8n_poc3 database only)
- No superuser privileges

**Application Level**:
- Owner account: `caio@hx.dev.local`
- User authentication required
- Encrypted credentials storage (N8N_ENCRYPTION_KEY)

---

### Credential Management

**Never**:
- ❌ Store passwords in plain text
- ❌ Commit credentials to git
- ❌ Share encryption keys
- ❌ Use default passwords

**Always**:
- ✅ Use EnvironmentFile for configuration
- ✅ Restrict file permissions (600)
- ✅ Rotate credentials periodically
- ✅ Use URL-safe passwords for database accounts

---

### Audit Logging

**Enable N8N Audit Logs**:
```bash
# In /opt/n8n/.env
N8N_LOG_LEVEL=verbose
N8N_LOG_OUTPUT=file
N8N_LOG_FILE_LOCATION=/var/log/n8n/
```

**View Audit Logs**:
```bash
ssh hx-n8n-server.hx.dev.local
sudo cat /var/log/n8n/n8n.log | grep -i auth
```

---

## Contacts and Escalation

### Primary Contacts

| Role | Name | Contact | Responsibilities |
|------|------|---------|-----------------|
| Service Owner | CAIO | caio@hx.dev.local | Final approvals, strategic decisions |
| Infrastructure | Frank Delgado | frank@hx.dev.local | Server, network, LDAP |
| Database | Quinn Baker | quinn@hx.dev.local | PostgreSQL, backups, performance |
| Build/Deploy | Omar Hassan | omar@hx.dev.local | Compilation, upgrades, config |
| Nginx/Proxy | William Torres | william@hx.dev.local | Reverse proxy, SSL/TLS |
| QA/Testing | Julia Santos | julia@hx.dev.local | Validation, testing, quality |

---

### Escalation Path

**Level 1** (0-15 minutes):
- Check service status
- Review logs
- Attempt restart if safe

**Level 2** (15-30 minutes):
- Contact relevant specialist (see table above)
- Provide logs and error details

**Level 3** (30-60 minutes):
- Escalate to CAIO
- Initiate incident response
- Engage multiple specialists if needed

**Level 4** (Critical Outage):
- Immediate CAIO notification
- All-hands incident response
- Consider rollback or failover

---

## Change Management

### Standard Change (Pre-Approved)

**Examples**:
- Restart service
- View logs
- Health checks
- Routine backups

**Approval**: None required

---

### Normal Change (Planned)

**Examples**:
- Configuration changes
- Database schema changes
- Minor version upgrades

**Approval**: Service owner (CAIO) + relevant specialist
**Notice**: 24 hours minimum
**Testing**: Required in non-prod first

---

### Emergency Change (Unplanned)

**Examples**:
- Critical security patch
- Service restoration
- Urgent bug fix

**Approval**: Service owner (CAIO)
**Notice**: Immediate notification
**Testing**: May proceed without full testing if critical

---

## Documentation References

### Technical Documentation

- **Architecture**: `/srv/cc/Governance/x-poc3-n8n-deployment/p2-design/architecture.md`
- **Installation Guide**: `/srv/cc/Governance/x-poc3-n8n-deployment/p3-execution/build-instructions.md`
- **Acceptance Criteria**: `/srv/cc/Governance/x-poc3-n8n-deployment/p2-design/acceptance-criteria.md`
- **QA Report**: `/srv/cc/Governance/x-poc3-n8n-deployment/p4-validation/qa-sign-off.md`
- **Defect Log**: `/srv/cc/Governance/x-poc3-n8n-deployment/DEFECT-LOG.md`

### User Documentation

- **README**: `/srv/cc/Governance/x-poc3-n8n-deployment/p5-user-docs/README.md`
- **Login Guide**: `/srv/cc/Governance/x-poc3-n8n-deployment/p5-user-docs/1-login-guide.md`
- **Getting Started**: `/srv/cc/Governance/x-poc3-n8n-deployment/p5-user-docs/2-getting-started.md`
- **First Workflow**: `/srv/cc/Governance/x-poc3-n8n-deployment/p5-user-docs/3-first-workflow.md`

### Governance Documentation

- **Credentials**: `/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.1-credentials.md`
- **URL-Safe Password Pattern**: `/srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.2-credentials/0.0.5.2.2-url-safe-password-pattern.md`

### External Resources

- **N8N Official Docs**: https://docs.n8n.io
- **N8N Community**: https://community.n8n.io
- **N8N GitHub**: https://github.com/n8n-io/n8n

---

**Document Version**: 1.0
**Last Updated**: November 8, 2025
**Next Review**: December 8, 2025 (30 days)
**Maintained By**: Operations Team
**Classification**: Internal Use Only

**Approved By**:
- ✅ **CAIO** (Service Owner) - November 8, 2025
- ✅ **Agent Zero** (Chief Architect) - November 8, 2025
