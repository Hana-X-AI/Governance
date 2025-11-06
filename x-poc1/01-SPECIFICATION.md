# Specification: Nginx Config Reload

**Work ID**: POC-001
**Phase**: Phase 1 (Specification)
**Date**: 2025-11-06
**Author**: Agent Zero

---

## Requirements

### Functional Requirements

**FR-001**: Nginx Configuration Testing
- MUST execute `nginx -t` to validate config syntax
- MUST complete without syntax errors
- MUST verify all referenced files exist

**FR-002**: Nginx Service Reload
- MUST execute `systemctl reload nginx` if config valid
- MUST complete without service errors
- MUST maintain zero downtime (reload, not restart)

**FR-003**: Error Handling
- IF config test fails, MUST identify and document errors
- IF config has errors, MUST fix before reload attempt
- MUST NOT reload with invalid configuration

**FR-004**: Timestamp Verification
- MUST verify service "Active" timestamp updates to current date
- MUST confirm config changes are now active

### Non-Functional Requirements

**NFR-001**: Safety
- Operation MUST be non-destructive
- Previous config already loaded (safe rollback state)

**NFR-002**: Documentation
- MUST log all commands executed
- MUST capture all output (stdout + stderr)
- MUST document any issues encountered

### Operational Requirements

**OR-001**: Execution Context
- Execute as: agent0@hx-ssl-server.hx.dev.local
- Credentials: Standard domain credentials (Major8859!)
- Access: SSH from control plane

---

## Acceptance Criteria

**AC-001**: Config Test Success
```bash
nginx -t
# Expected output:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful
```

**AC-002**: Reload Success
```bash
systemctl reload nginx
# Expected: Command completes with exit code 0
```

**AC-003**: Updated Timestamp
```bash
systemctl status nginx | grep "Active:"
# Expected: Shows date 2025-11-06 (today)
```

**AC-004**: No Errors in Logs
```bash
journalctl -u nginx --since "1 minute ago" | grep -i error
# Expected: No error entries (or only pre-existing errors)
```

---

## Success Metrics

- **Config Valid**: `nginx -t` exit code = 0
- **Reload Success**: `systemctl reload` exit code = 0
- **Timestamp Current**: Active since matches today's date
- **Error Count**: 0 new errors in logs

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Config has syntax errors | Cannot reload | Test first (`nginx -t`), fix errors before reload |
| Service fails to reload | Brief downtime | Reload is safe (not restart), previous config still loaded |
| Missing referenced files | Config invalid | Verify all paths exist before reload |

---

## Rollback Plan

**If reload fails**:
1. Previous configuration already loaded (no change made)
2. Review nginx error log: `journalctl -u nginx -n 50`
3. Fix configuration issues
4. Re-test with `nginx -t`
5. Retry reload

**No explicit rollback needed** - reload operation is safe.

---

## References

- **Gap Analysis**: P0-CONFIG-001 (lines 106-178)
- **Server Baseline**: `/srv/cc/Governance/WIP/Current State/hx-ssl-server-baseline.md`
- **Agent**: @agent-frank (Frank Lucas)

---

**Status**: Complete ✅
**Next Phase**: Phase 2 (Planning - Task List)
