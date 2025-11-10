# Task: Create Admin User

**Task ID**: T-042
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 10 minutes |
| **Dependencies** | T-041 |

## Task Overview

Create the first admin user account via the n8n web UI to enable workflow creation and system administration.

## Success Criteria
- [ ] Admin user created successfully
- [ ] Can log in with credentials
- [ ] Dashboard accessible after login
- [ ] User has admin privileges
- [ ] Credentials documented securely

## Execution Steps

### Step 1: Access Setup Page
```bash
echo "============================================"
echo "ADMIN USER CREATION"
echo "============================================"
echo ""
echo "1. Open browser to:"
echo "   http://hx-n8n-server.hx.dev.local:5678"
echo ""
echo "2. You should see initial setup form"
echo ""
```

### Step 2: Create User Credentials
```bash
echo "3. Enter user details:"
echo ""
echo "   Recommended credentials:"
echo "   - Email: admin@hx.dev.local"
echo "   - First Name: n8n"
echo "   - Last Name: Administrator"
echo "   - Password: [Use strong password - min 8 chars]"
echo ""
echo "   ⚠️  IMPORTANT: Document password securely"
echo ""
```

### Step 3: Complete Setup
```bash
echo "4. Click 'Get Started' or 'Create Account'"
echo ""
echo "5. Wait for account creation"
echo ""
echo "6. Should redirect to n8n dashboard"
echo ""
```

### Step 4: Verify Login
```bash
echo "7. Verify you see:"
echo "   - n8n dashboard/editor"
echo "   - User profile in top-right"
echo "   - 'Create Workflow' button visible"
echo ""
echo "Press ENTER after user created and logged in..."
read
```

### Step 5: Document Credentials
```bash
cat > /opt/n8n/docs/admin-credentials.txt << CREDEOF
n8n POC3 - Admin User Credentials
===========================================
Created: $(date)
Server: hx-n8n-server.hx.dev.local

Admin User:
-----------
Email: admin@hx.dev.local
Password: [REDACTED - stored securely]

Access URL:
-----------
http://hx-n8n-server.hx.dev.local:5678

Security Notes:
---------------
- This is the POC3 development environment
- Change password in production deployment
- Enable MFA when available
- Review user permissions regularly

===========================================
CREDEOF

sudo chown n8n:n8n /opt/n8n/docs/admin-credentials.txt
sudo chmod 600 /opt/n8n/docs/admin-credentials.txt

echo "✅ Credentials documented (password redacted)"
```

### Step 6: Verify Database User Entry
```bash
echo "=== Verifying User in Database ==="

user_count=$(psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 \
  -t -c "SELECT COUNT(*) FROM \"user\";" 2>/dev/null)

echo "Users in database: $user_count"

if [ "$user_count" -eq 1 ]; then
  echo "✅ Admin user created in database"
else
  echo "⚠️  Unexpected user count: $user_count"
fi
```

## Validation
```bash
# Verify user exists
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 \
  -c "SELECT email, \"firstName\", \"lastName\" FROM \"user\";" 2>/dev/null

# Should show admin@hx.dev.local
```

## Troubleshooting

### If Setup Form Not Shown
```bash
# May already have user - check database
psql -h hx-postgres-server.hx.dev.local -U n8n_user -d n8n_poc3 \
  -c "SELECT COUNT(*) FROM \"user\";"

# If user exists but can't login, may need password reset
```

### If User Creation Fails
```bash
# Check logs
sudo journalctl -u n8n -n 50 | grep -i "user\|auth\|create"

# Check database permissions
# Coordinate with @agent-quinn
```

## Task Metadata
```yaml
task_id: T-042
source: agent-omar-planning-analysis.md:604 (T6.2)
security_note: |
  Admin credentials created. Password should be:
  - Minimum 12 characters
  - Include upper, lower, numbers, symbols
  - Stored in password manager
  - Changed for production deployment
```
