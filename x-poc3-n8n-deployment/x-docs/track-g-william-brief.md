═══════════════════════════════════════════════════════════════
🎯 TRACK G: NGINX INSTALLATION & CONFIGURATION
═══════════════════════════════════════════════════════════════

@agent-william - You are being invoked for Phase 2, Task 2.4

**⚠️ STATUS: AWAITING TRACK F (FRANK) COMPLETION**

This brief is prepared and ready. You will be launched when Track F (@agent-frank) completes SSL certificate transfer and provides the required SSL paths.

---

PROJECT: POC3 N8N Workflow Automation Platform Deployment
PHASE: Phase 2 - Infrastructure Validation
TASK: 2.4 - Install Nginx and configure reverse proxy with SSL termination
DURATION: 1.5 hours
EXECUTION MODE: Sequential (Group 2, awaits Track F)

HANDOFF DATA FROM PHASE 1 (Track B - @agent-william):
✅ Server: hx-n8n-server (192.168.10.215)
✅ Node.js: v22.21.0
✅ pnpm: 10.18.3
✅ Service user: n8n (uid=999)
✅ Directories: /opt/n8n, /var/log/n8n, /srv/n8n (created)

REQUIRED HANDOFF FROM TRACK F (@agent-frank):
⏳ PENDING - Waiting for Track F completion
⏳ SSL certificate path: /etc/ssl/certs/n8n.hx.dev.local.crt (to be confirmed)
⏳ SSL private key path: /etc/ssl/private/n8n.hx.dev.local.key (to be confirmed)
⏳ Permission verification: 600 for key, 644 for cert (to be confirmed)

YOUR TASK:
Install Nginx and configure reverse proxy with SSL/TLS termination for n8n web UI access.

SERVER: agent0@192.168.10.215 (hx-n8n-server)

DETAILED REQUIREMENTS:
1. SSH to hx-n8n-server (agent0@192.168.10.215)
2. Install Nginx: sudo apt install -y nginx
3. Create Nginx site configuration file: /etc/nginx/sites-available/n8n.conf
4. Configure Nginx with:
   a) HTTP → HTTPS redirect (port 80 → 443)
   b) HTTPS listener on port 443 with SSL/TLS
   c) Reverse proxy to n8n backend (127.0.0.1:5678)
   d) SSL certificate paths FROM TRACK F HANDOFF
   e) WebSocket upgrade headers (required for n8n real-time features)
   f) Security headers (X-Real-IP, X-Forwarded-For, X-Forwarded-Proto)
5. Enable site: sudo ln -sf /etc/nginx/sites-available/n8n.conf /etc/nginx/sites-enabled/
6. Test configuration syntax: sudo nginx -t
   
   **If validation fails, troubleshoot**:
   - Read the exact syntax error (nginx -t reports file and line number)
   - Check Nginx error logs: `sudo tail -n 50 /var/log/nginx/error.log`
   - Verify included files for:
     - Missing semicolons (`;`) at end of directives
     - Mismatched braces (`{` `}`)
     - Invalid file paths (SSL certs, includes)
   - Dump full processed config: `sudo nginx -T` (capital T)
   - Test with explicit config: `sudo nginx -c /etc/nginx/nginx.conf -t`
   - Check service status: `sudo systemctl status nginx`
   - Verify file permissions (config files readable by nginx user)
   - Re-test after fixes: `sudo nginx -t`

7. **DO NOT START NGINX YET** (n8n application not running in Phase 2)
8. Document configuration for Phase 3 startup

NGINX CONFIGURATION TEMPLATE:
```nginx
server {
    listen 80;
    server_name n8n.hx.dev.local;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name n8n.hx.dev.local;

    # SSL configuration (PATHS FROM TRACK F)
    ssl_certificate /etc/ssl/certs/n8n.hx.dev.local.crt;
    ssl_certificate_key /etc/ssl/private/n8n.hx.dev.local.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    # Reverse proxy to n8n
    location / {
        proxy_pass http://127.0.0.1:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (CRITICAL for n8n)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

VALIDATION CRITERIA:
✅ Nginx package installed successfully
✅ Configuration file created at /etc/nginx/sites-available/n8n.conf
✅ Configuration syntax valid (nginx -t returns OK)
✅ SSL certificate paths correct (from Track F handoff)
✅ WebSocket upgrade headers present
✅ HTTP → HTTPS redirect configured
✅ Reverse proxy points to 127.0.0.1:5678
✅ Site enabled (symlink created)
✅ Service NOT started yet (awaiting Phase 3)

REFERENCE DOCUMENTATION:
Execution Plan: /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/phase3-execution-plan.md
Lines 498-558 (Task 2.4 details)

DELIVERABLES:
1. Nginx installation confirmation (apt install output)
2. Configuration file contents (full n8n.conf)
3. Syntax validation output (nginx -t)
4. SSL path verification (confirm matches Track F handoff)
5. WebSocket configuration confirmation
6. Readiness report for Phase 3 startup

COORDINATION CONTEXT:
- SEQUENTIAL execution (awaits Track F completion)
- Track F (Frank) provides SSL certificate paths (dependency)
- Running in parallel with Track E (Samuel - Redis) timeline
- Your completion triggers Phase 2 checkpoint
- Phase 3 will start Nginx service (not done in Phase 2)

HANDOFF FROM TRACK F (EXPECTED):
When Track F completes, @agent-frank will provide:
- SSL certificate path: /etc/ssl/certs/n8n.hx.dev.local.crt
- SSL private key path: /etc/ssl/private/n8n.hx.dev.local.key
- Permission confirmation: 600 for key (critical), 644 for cert
- Checksum verification: Files transferred successfully

QUALITY REQUIREMENTS:
- Quality Over Speed: Take full 1.5 hours if needed for thorough configuration
- Validate syntax BEFORE reporting completion (nginx -t must pass)
- WebSocket headers are CRITICAL - n8n won't work without them
- DO NOT start Nginx service (n8n not running yet)
- 2-attempt rule: Try twice, escalate to @agent-zero if blocked

CRITICAL CONFIGURATION NOTES:
1. **WebSocket Support**: MUST include `proxy_http_version 1.1`, `Upgrade`, and `Connection "upgrade"` headers
   - Without these, n8n real-time updates will fail
2. **SSL Paths**: MUST match Track F handoff exactly
   - Wrong path = Nginx won't start in Phase 3
3. **Proxy Target**: 127.0.0.1:5678 (n8n default port)
   - Do NOT use public IP (security risk)
4. **HTTP Redirect**: All HTTP traffic MUST redirect to HTTPS
   - No unencrypted access allowed

PHASE 3 STARTUP CONTEXT:
In Phase 3, Nginx will be started AFTER n8n application starts:
- Phase 3 Task 3.7: Start n8n service (listen on 127.0.0.1:5678)
- Phase 3 Task 3.8: Start Nginx service (reverse proxy)
- Phase 3 Task 3.9: Validate HTTPS access (https://n8n.hx.dev.local)

Your Phase 2 configuration ensures Nginx is ready when Phase 3 needs it.

---

**LAUNCH TRIGGER**: Track F (@agent-frank) completion notification
**EXPECTED LAUNCH**: ~30 minutes after Phase 2 start (Track F duration)

⏳ STANDING BY FOR TRACK F COMPLETION SIGNAL...

---

When Track F completes, @agent-zero will launch you with updated handoff data.

**END OF TRACK G BRIEF**
