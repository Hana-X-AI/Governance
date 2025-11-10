# Task: Verify Web UI Accessible

**Task ID**: T-041
**Parent Work Item**: POC3 n8n Deployment - Phase 3.3 Deployment
**Assigned Agent**: @agent-omar
**Created**: 2025-11-07
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical |
| **Estimated Duration** | 5 minutes |
| **Dependencies** | T-040 |

## Task Overview

Verify that the n8n web UI is accessible at http://hx-n8n-server.hx.dev.local:5678 and displays the initial setup screen.

## Success Criteria
- [ ] Web UI responds to HTTP requests
- [ ] Setup page loads successfully
- [ ] No JavaScript errors in browser console
- [ ] Can access from browser
- [ ] Initial user creation prompt visible

## Execution Steps

### Step 1: Test HTTP Endpoint
```bash
echo "=== Testing HTTP Endpoint ==="

curl -I http://hx-n8n-server.hx.dev.local:5678/ 2>&1

# Expected: HTTP 200 OK or 302 redirect
```

### Step 2: Test with Full Request
```bash
echo "=== Testing Full Page Load ==="

response=$(curl -s -o /dev/null -w "%{http_code}" http://hx-n8n-server.hx.dev.local:5678/)

if [ "$response" = "200" ] || [ "$response" = "302" ]; then
  echo "✅ Web UI responding (HTTP $response)"
else
  echo "❌ Web UI not accessible (HTTP $response)"
  exit 1
fi
```

### Step 3: Check Health Endpoint
```bash
echo "=== Checking Health Endpoint ==="

curl -s http://hx-n8n-server.hx.dev.local:5678/healthz

# Expected: {"status":"ok"}
```

### Step 4: Verify HTML Content
```bash
echo "=== Verifying Page Content ==="

page_content=$(curl -s http://hx-n8n-server.hx.dev.local:5678/)

if echo "$page_content" | grep -q "n8n"; then
  echo "✅ n8n content detected"
else
  echo "⚠️  Unexpected page content"
fi
```

### Step 5: Test from Browser
```bash
echo ""
echo "============================================"
echo "MANUAL BROWSER TEST REQUIRED"
echo "============================================"
echo ""
echo "Open browser and navigate to:"
echo "  http://hx-n8n-server.hx.dev.local:5678"
echo ""
echo "Expected:"
echo "  - n8n logo visible"
echo "  - 'Get started' or user creation form"
echo "  - No error messages"
echo "  - Page title contains 'n8n'"
echo ""
echo "Failure Criteria (STOP if any occur):"
echo "  - 404 Not Found"
echo "  - 503 Service Unavailable"
echo "  - 'Cannot connect' or timeout"
echo "  - Blank page or unformatted HTML"
echo "  - JavaScript console errors (check browser console)"
echo ""
echo "Press ENTER after verifying in browser..."
read
```

### Step 6: Verify API Endpoint
```bash
echo "=== Testing API Endpoint ==="

api_response=$(curl -s http://hx-n8n-server.hx.dev.local:5678/api/v1/health)

echo "API Response: $api_response"
```

## Validation
```bash
# Comprehensive check
curl -s http://hx-n8n-server.hx.dev.local:5678/healthz | grep -q "ok" && \
curl -s -o /dev/null -w "%{http_code}" http://hx-n8n-server.hx.dev.local:5678/ | grep -q "200\|302" && \
echo "✅ Web UI fully accessible" || \
echo "❌ Web UI accessibility issues"
```

## Troubleshooting

### If Web UI Not Accessible
```bash
# Check if service running
sudo systemctl status n8n.service

# Check port listening
sudo ss -tlnp | grep :5678

# Check firewall
sudo ufw status | grep 5678

# Check logs for errors
sudo journalctl -u n8n -n 50
```

### If Page Loads but Broken
```bash
# Check browser console for JavaScript errors
# Check network tab for failed resource loads
# Verify static assets loading correctly
```

## Task Metadata
```yaml
task_id: T-041
source: agent-omar-planning-analysis.md:603 (T6.1)
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial task creation for web UI accessibility verification | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: Added explicit failure criteria to manual browser test section (lines 91-96). Prevents subjective pass/fail interpretation by listing 5 specific failure conditions: 404 Not Found, 503 Service Unavailable, connection timeout, blank/unformatted page, and JavaScript console errors. Also added page title check to expected outcomes. Makes verification objective and prevents ambiguous task completion. | Claude Code |
