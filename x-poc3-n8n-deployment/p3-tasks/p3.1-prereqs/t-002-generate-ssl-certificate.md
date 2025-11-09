# Task: Generate SSL Certificate for n8n.hx.dev.local

**Task ID**: T-002
**Assigned Agent**: @agent-frank
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-001
**Estimated Duration**: 30 minutes

---

## Objective
Generate SSL certificate from Samba CA for n8n.hx.dev.local with proper SANs.

## Commands

```bash
# Generate private key
sudo openssl genrsa -out /etc/ssl/private/n8n.hx.dev.local.key 2048
sudo chmod 600 /etc/ssl/private/n8n.hx.dev.local.key

# Create SAN config
sudo tee /tmp/n8n-san.cnf <<'EOF'
[ req ]
default_bits = 2048
distinguished_name = req_distinguished_name
req_extensions = v3_req

[ req_distinguished_name ]
CN = n8n.hx.dev.local

[ v3_req ]
subjectAltName = @alt_names

[ alt_names ]
DNS.1 = n8n.hx.dev.local
DNS.2 = hx-n8n-server.hx.dev.local
EOF

# Generate CSR
sudo openssl req -new -key /etc/ssl/private/n8n.hx.dev.local.key \
  -out /tmp/n8n.hx.dev.local.csr \
  -subj "/CN=n8n.hx.dev.local/O=Hana-X/OU=AI Ecosystem" \
  -config /tmp/n8n-san.cnf

# Sign with Samba CA (adapt based on CA setup)
sudo openssl x509 -req -in /tmp/n8n.hx.dev.local.csr \
  -CA /var/lib/samba/private/tls/ca.pem \
  -CAkey /var/lib/samba/private/tls/key.pem \
  -CAcreateserial \
  -out /etc/ssl/certs/n8n.hx.dev.local.crt \
  -days 365 -sha256 \
  -extensions v3_req -extfile /tmp/n8n-san.cnf

# Export CA cert
sudo cp /var/lib/samba/private/tls/ca.pem /etc/ssl/certs/hx-dev-ca.crt
sudo chmod 644 /etc/ssl/certs/hx-dev-ca.crt
```

## Success Criteria
- [ ] Private key generated (0600 permissions)
- [ ] Certificate signed by Samba CA
- [ ] SANs include n8n.hx.dev.local and hx-n8n-server.hx.dev.local
- [ ] Certificate valid for 365 days

## Validation
```bash
sudo openssl verify -CAfile /etc/ssl/certs/hx-dev-ca.crt /etc/ssl/certs/n8n.hx.dev.local.crt
sudo openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -text -noout | grep -A 2 "Subject Alternative Name"
```

---
**Source**: x-poc3-n8n-deployment/p2-specification/phase3-execution-plan.md:181-231, x-poc3-n8n-deployment/p1-planning/agent-frank-planning-analysis.md:59-145
