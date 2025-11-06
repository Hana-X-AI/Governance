# Task List: Nginx Config Reload

**Work ID**: POC-001
**Phase**: Phase 2 (Planning) - UPDATED with Agent William's Enhancements
**Date**: 2025-11-06
**Orchestrator**: Agent Zero
**Executing Agent**: @agent-william (reassigned from @agent-frank)
**Version**: 1.1 (Enhanced per Phase 3 alignment reviews)

---

## Task Breakdown

### Pre-Flight Checks

**T0**: Verify SSH connectivity to hx-ssl-server
- **Assigned**: Agent Zero
- **Command**: `ssh agent0@192.168.10.202 "hostname"`
- **Expected**: `hx-ssl-server`
- **Status**: ⬜ Pending

**T0.5**: Snapshot current nginx configuration [ENHANCEMENT - William R2]
- **Assigned**: @agent-william
- **Command**: `ssh agent0@192.168.10.202 "sudo cp /etc/nginx/nginx.conf /srv/cc/Governance/x-poc1/06-docs/nginx.conf.before-reload-$(date +%Y%m%d-%H%M%S)"`
- **Expected**: Config file copied to 06-docs/ directory
- **Status**: ⬜ Pending
- **Dependencies**: T0 complete
- **Rationale**: Provides baseline for diff analysis, satisfies @agent-frank recommendation
- **Benefit**: Enables comparison if issues arise, governance best practice

---

### Phase 1: Configuration Testing

**T1**: Test nginx configuration syntax
- **Assigned**: @agent-william
- **Reference**: `/srv/cc/Governance/WIP/Current State/hx-ssl-server-baseline.md` (lines 243-261)
- **Command**: `ssh agent0@192.168.10.202 "sudo nginx -t"`
- **Expected**: "syntax is ok" + "test is successful"
- **Status**: ⬜ Pending
- **Dependencies**: T0.5 complete
- **Validation**: Exit code = 0

**T1a**: [CONDITIONAL] If T1 fails - Review config errors
- **Assigned**: @agent-william
- **Command**: `ssh agent0@192.168.10.202 "sudo nginx -t 2>&1"`
- **Action**: Document all errors in 03-EXECUTION-LOG.md
- **Status**: ⬜ Pending (conditional)
- **Next**: Fix errors, return to T1

---

### Phase 2: Service Reload

**T2**: Reload nginx service
- **Assigned**: @agent-william
- **Command**: `ssh agent0@192.168.10.202 "sudo systemctl reload nginx"`
- **Expected**: Exit code 0, no error output
- **Status**: ⬜ Pending
- **Dependencies**: T1 complete (config valid)
- **Validation**: Command completes successfully
- **Note**: Uses SIGHUP (graceful reload), not SIGTERM (restart) - zero downtime

**T3**: Verify reload timestamp
- **Assigned**: @agent-william
- **Command**: `ssh agent0@192.168.10.202 "systemctl status nginx | grep 'Active:'"`
- **Expected**: Date shows 2025-11-06
- **Status**: ⬜ Pending
- **Dependencies**: T2 complete
- **Validation**: Timestamp updated

---

### Phase 3: Post-Reload Validation

**T4**: Check nginx error logs
- **Assigned**: @agent-william
- **Command**: `ssh agent0@192.168.10.202 "sudo journalctl -u nginx --since '2 minutes ago' | grep -i error"`
- **Expected**: No new error entries (or empty)
- **Status**: ⬜ Pending
- **Dependencies**: T2 complete
- **Validation**: 0 new errors

**T5**: Verify nginx is serving
- **Assigned**: @agent-william
- **Command**: `curl -k https://192.168.10.202/ -I`
- **Expected**: HTTP 200 or 30x response
- **Status**: ⬜ Pending
- **Dependencies**: T2 complete
- **Validation**: Service responding

**T5.5**: Verify/create operations log file [ENHANCEMENT - William R1]
- **Assigned**: @agent-william
- **Command**: `ssh agent0@192.168.10.202 "sudo touch /var/log/hx-ssl-server-operations.log && sudo chmod 644 /var/log/hx-ssl-server-operations.log"`
- **Expected**: Log file exists and is writable
- **Status**: ⬜ Pending
- **Dependencies**: T5 complete
- **Rationale**: Prevents T6 failure if log file doesn't exist
- **Benefit**: Ensures operations log documentation succeeds

---

### Phase 4: Documentation

**T6**: Document completion in operations log
- **Assigned**: @agent-william
- **Command**: `ssh agent0@192.168.10.202 "echo '$(date): Nginx config reloaded (Oct 21 changes applied) - Agent Zero POC-001' | sudo tee -a /var/log/hx-ssl-server-operations.log"`
- **Expected**: Log entry created
- **Status**: ⬜ Pending
- **Dependencies**: T5.5 complete (log file exists)

**T7**: Create completion summary
- **Assigned**: Agent Zero
- **File**: `05-COMPLETION-SUMMARY.md`
- **Content**: Results, timestamps, lessons learned
- **Status**: ⬜ Pending
- **Dependencies**: T6 complete

---

## Task Summary (Updated with Enhancements)

| Phase | Tasks | Parallel? | Dependencies | Est. Time |
|-------|-------|-----------|--------------|-----------|
| Pre-Flight | T0, T0.5 | Sequential | None | 1 min |
| Testing | T1 (T1a) | No | T0.5 | 1-2 min |
| Reload | T2, T3 | Sequential | T1 | 1 min |
| Validation | T4, T5, T5.5 | Sequential | T2 | 2-3 min |
| Documentation | T6, T7 | Sequential | T5.5 | 2 min |

**Total Estimated Time**: 7-9 minutes (was 6-8 minutes, +1 minute for enhancements)

**Total Tasks**: 9 tasks (was 7, +2 enhancements: T0.5 config snapshot, T5.5 log creation)

---

## Execution Protocol (Updated)

1. **Agent Zero** verifies connectivity (T0)
2. **@agent-william** snapshots nginx config (T0.5) [ENHANCEMENT]
3. **@agent-william** executes T1-T6 with validation at each step
4. **Agent Zero** creates completion summary (T7)
5. **Agent Zero** updates governance (Platform Nodes, Gap Analysis)

**Enhancements Applied**:
- ✅ T0.5: Config snapshot before reload (addresses @agent-frank recommendation)
- ✅ T5.5: Operations log file creation (prevents T6 failure)
- ✅ Agent reassignment: @agent-william (correct agent per governance)
- ✅ Baseline documentation reference added to T1

---

## Success Definition (Updated)

✅ All 9 tasks complete (was 7, +2 enhancements) - or T1a if needed
✅ All acceptance criteria met (AC-001 through AC-004)
✅ 0 new errors in logs
✅ Documentation updated
✅ Config snapshot captured (T0.5)
✅ Operations log file created (T5.5)

---

## Change Log

**Version 1.1** (2025-11-06) - Enhancements per Phase 3 Alignment:
- Added T0.5: Config snapshot (William R2, addresses Frank recommendation)
- Added T5.5: Operations log file creation (William R1)
- Reassigned from @agent-frank to @agent-william (correct agent)
- Added baseline documentation reference to T1 (William R4)
- Updated time estimate: 7-9 minutes (was 6-8)
- Total tasks: 9 (was 7)

**Version 1.0** (2025-11-06) - Initial task list

---

**Status**: Complete ✅ - Enhanced Version Ready
**Next Phase**: Phase 4 (Execution with @agent-william)
**CAIO Approval**: ✅ OPTION 2 approved (2025-11-06)
