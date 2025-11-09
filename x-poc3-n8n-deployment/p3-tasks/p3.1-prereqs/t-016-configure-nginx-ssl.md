# Task: Configure Nginx with SSL

**Task ID**: T-016
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-003, T-008
**Estimated Duration**: 30 minutes

---

## Objective
Create Nginx reverse proxy configuration with SSL termination.

## Commands

```bash
sudo tee /etc/nginx/sites-available/n8n.conf <<'EOF'
server {
    listen 80;
    server_name n8n.hx.dev.local;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name n8n.hx.dev.local;

    ssl_certificate /etc/ssl/certs/n8n.hx.dev.local.crt;
    ssl_certificate_key /etc/ssl/private/n8n.hx.dev.local.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
        proxy_pass http://127.0.0.1:5678;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/n8n.conf /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

## Success Criteria
- [ ] Nginx configured with SSL/TLS
- [ ] WebSocket upgrade headers configured
- [ ] Configuration syntax valid
- [ ] Nginx started successfully

## Validation
```bash
sudo nginx -t
sudo systemctl status nginx
curl -I https://n8n.hx.dev.local
```

---
**Source**: phase3-execution-plan.md:472-533
