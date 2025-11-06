**Document Type**: Template - Individual Task  
**Created**: 2025-11-06  
**Topic**: Individual Task Template  
**Purpose**: Template for detailed individual task tracking and execution  
**Classification**: Internal

---

# Task: [TASK DESCRIPTION]

**Task ID**: [T###]
**Parent Work Item**: [Link to parent task list or work plan]
**Assigned Agent**: [@agent-name]
**Created**: [YYYY-MM-DD]
**Status**: [NOT STARTED | IN PROGRESS | COMPLETED | BLOCKED | FAILED]

---

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | [P1/P2/P3 - Critical/High/Normal/Low] |
| **Execution Type** | [Parallel/Sequential] |
| **Dependencies** | [Blocked by: T### | No dependencies] |
| **Estimated Duration** | [X minutes/hours] |
| **Actual Duration** | [X minutes/hours] |
| **Systems Affected** | [Server names, IPs, services] |
| **Rollback Required** | [Yes/No] |

---

## Task Overview

### Objective
[Clear, concise statement of what this task accomplishes]

**Example**: Deploy Docling Worker v2.5 to hx-docling-server (192.168.10.216) to improve processing performance from 45s to 30s per document.

### Context
[Brief background explaining why this task is needed]

**Example**: Current Docling Worker (v2.3) processes documents in ~45s. Version 2.5 includes optimizations that reduce processing time by 33%. This upgrade is part of the broader performance improvement initiative.

### Success Criteria
[Measurable criteria that define task completion]

- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Example**:
- [ ] Docling Worker v2.5 installed and running
- [ ] Test document processes successfully in <35s
- [ ] No errors in service logs for 15 minutes
- [ ] Integration with Docling MCP verified

---

## Prerequisites

### Required Access
- [ ] [Access type 1 - e.g., SSH to server]
- [ ] [Access type 2 - e.g., sudo privileges]
- [ ] [Access type 3 - e.g., service credentials]

**Example**:
- [ ] SSH access to hx-docling-server (192.168.10.216)
- [ ] Sudo privileges on hx-docling-server
- [ ] Access to /srv/docling-worker/ directory

### Required Resources
- [ ] [Resource 1 - e.g., installation package]
- [ ] [Resource 2 - e.g., configuration file]
- [ ] [Resource 3 - e.g., credentials]

**Example**:
- [ ] Docling Worker v2.5 package (downloaded from repo)
- [ ] Updated configuration template
- [ ] Service account credentials (svc-docling)

### Required Knowledge
- [ ] [Knowledge area 1]
- [ ] [Knowledge area 2]

**Example**:
- [ ] Systemd service management
- [ ] Docling Worker configuration syntax
- [ ] Rollback procedures for service failures

### Blocking Dependencies
[List any tasks that must complete before this task can start]

- [ ] [T### - Task name and why it blocks this task]
- [ ] [T### - Task name and why it blocks this task]

**Example**:
- [ ] T015 - Download Docling v2.5 model to Ollama (model must be available)
- [ ] T022 - Backup current Docling Worker config (backup needed for rollback)

---

## Detailed Execution Steps

### Step 1: [Step Name]

**Command/Action**:
```bash
[command or action to perform]
```

**Expected Output**:
```
[what you should see if successful]
```

**Validation**:
```bash
[command to verify step succeeded]
```

**If This Fails**:
- [Troubleshooting step 1]
- [Troubleshooting step 2]

**Example**:
```bash
# Stop Docling Worker service
sudo systemctl stop docling-worker
```

**Expected Output**:
```
[No output - silence is success]
```

**Validation**:
```bash
sudo systemctl status docling-worker
# Expected: "inactive (dead)"
```

**If This Fails**:
- Check if service exists: `systemctl list-units | grep docling`
- Force stop if needed: `sudo systemctl kill docling-worker`
- Check for processes: `ps aux | grep docling`

---

### Step 2: [Step Name]

**Command/Action**:
```bash
[command or action to perform]
```

**Expected Output**:
```
[what you should see if successful]
```

**Validation**:
```bash
[command to verify step succeeded]
```

**If This Fails**:
- [Troubleshooting step 1]
- [Troubleshooting step 2]

---

### Step 3: [Step Name]

**Command/Action**:
```bash
[command or action to perform]
```

**Expected Output**:
```
[what you should see if successful]
```

**Validation**:
```bash
[command to verify step succeeded]
```

**If This Fails**:
- [Troubleshooting step 1]
- [Troubleshooting step 2]

---

[Continue adding steps as needed]

---

## Validation & Testing

### Functional Validation
[Tests to verify the task achieved its objective]

**Test 1**: [Test name]
```bash
[test command or procedure]
```
**Expected Result**: [What success looks like]
**Actual Result**: [Fill in during execution]

**Example**:
**Test 1**: Process test document
```bash
curl -X POST http://192.168.10.216:8080/process \
  -H "Content-Type: application/json" \
  -d '{"document": "test.pdf"}'
```
**Expected Result**: HTTP 200, processing time <35s, valid output
**Actual Result**: _[Fill in during execution]_

---

### Integration Validation
[Tests to verify integration with other systems]

**Test 1**: [Integration test name]
```bash
[test command or procedure]
```
**Expected Result**: [What success looks like]
**Actual Result**: [Fill in during execution]

**Example**:
**Test 1**: Docling MCP → Worker connection
```bash
curl http://192.168.10.214:3000/health
# Check "worker_connected": true
```
**Expected Result**: Health check shows worker connected, status healthy
**Actual Result**: _[Fill in during execution]_

---

### Performance Validation
[Tests to verify performance meets targets]

**Metric 1**: [Performance metric]
- **Target**: [Target value]
- **Actual**: [Fill in during execution]

**Example**:
**Metric 1**: Document processing time
- **Target**: <35s per document
- **Actual**: _[Fill in during execution]_

**Metric 2**: Service startup time
- **Target**: <10s
- **Actual**: _[Fill in during execution]_

---

## Rollback Procedure

**When to Rollback**: [Conditions that trigger rollback]

**Example**: Rollback if processing time >45s, service fails to start, or errors appear in logs.

### Rollback Steps

**Step R1**: [Rollback step]
```bash
[rollback command]
```
**Validation**: [How to verify rollback succeeded]

**Example**:
```bash
# Step R1: Stop new version
sudo systemctl stop docling-worker

# Step R2: Restore backed-up config
sudo cp /srv/backups/docling-worker-config-20251105.tar.gz /srv/docling-worker/
sudo tar -xzf docling-worker-config-20251105.tar.gz -C /srv/docling-worker/

# Step R3: Start service with original config
sudo systemctl start docling-worker

# Step R4: Verify original version running
systemctl status docling-worker
journalctl -u docling-worker -n 20 | grep "version"
# Expected: Shows v2.3, not v2.5
```

---

## Execution Log

### Execution Timeline

| Timestamp | Event | Details |
|-----------|-------|---------|
| [HH:MM] | Task started | [Notes] |
| [HH:MM] | Step 1 completed | [Notes] |
| [HH:MM] | Step 2 completed | [Notes] |
| [HH:MM] | [Event] | [Notes] |
| [HH:MM] | Task completed | [Notes] |

**Example**:
| Timestamp | Event | Details |
|-----------|-------|---------|
| 14:30 | Task started | SSH to hx-docling-server successful |
| 14:32 | Step 1 completed | Service stopped cleanly |
| 14:35 | Step 2 completed | Config updated, backup verified |
| 14:38 | Step 3 completed | Service started, no errors |
| 14:45 | Validation passed | Test doc processed in 32s |
| 14:50 | Task completed | All criteria met |

---

### Issues Encountered

| Issue | Time | Resolution | Time to Resolve |
|-------|------|------------|-----------------|
| [Issue description] | [HH:MM] | [How resolved] | [X min] |

**Example**:
| Issue | Time | Resolution | Time to Resolve |
|-------|------|------------|-----------------|
| Service failed first start | 14:38 | Missing environment variable, added to config | 5 min |
| Model not found | 14:43 | Incorrect path in config, corrected | 2 min |

---

### Commands Executed

**For audit trail and reproducibility**

```bash
# [Timestamp] - [Description]
[actual command run]

# [Timestamp] - [Description]
[actual command run]
```

**Example**:
```bash
# 14:30 - Stop service
sudo systemctl stop docling-worker

# 14:32 - Backup current config
sudo tar -czf /srv/backups/docling-worker-config-20251105.tar.gz /srv/docling-worker/config.yaml

# 14:33 - Update config file
sudo nano /srv/docling-worker/config.yaml
# Changed: model_version: "2.5"

# 14:38 - Start service
sudo systemctl start docling-worker

# 14:39 - Check status
systemctl status docling-worker

# 14:40 - Watch logs
journalctl -u docling-worker -f
```

---

## Results

### Task Outcome
- **Status**: [COMPLETED | FAILED | PARTIALLY COMPLETED]
- **Start Time**: [HH:MM]
- **End Time**: [HH:MM]
- **Duration**: [X minutes]
- **Rollback Needed**: [Yes/No]

### Success Criteria Results

| Criterion | Met? | Evidence |
|-----------|------|----------|
| [Criterion 1] | [✅/❌] | [Proof/measurement] |
| [Criterion 2] | [✅/❌] | [Proof/measurement] |
| [Criterion 3] | [✅/❌] | [Proof/measurement] |

**Example**:
| Criterion | Met? | Evidence |
|-----------|------|----------|
| Service running | ✅ | `systemctl status` shows active |
| Processing <35s | ✅ | Test doc processed in 32s |
| No errors in logs | ✅ | 15min monitor showed no errors |
| MCP integration OK | ✅ | Health check shows connected |

---

## Documentation Updates

### Files Modified

| File | Change Type | Description |
|------|-------------|-------------|
| [File path] | [Created/Modified/Deleted] | [What changed] |

**Example**:
| File | Change Type | Description |
|------|-------------|-------------|
| /srv/docling-worker/config.yaml | Modified | Updated model_version to "2.5" |
| /srv/backups/docling-worker-config-20251105.tar.gz | Created | Backup of original config |

### Documentation to Update

- [ ] [Document name] - [Update description]
- [ ] [Document name] - [Update description]

**Example**:
- [ ] Service Operations Guide - Update Docling Worker version to v2.5
- [ ] Performance Benchmarks - Add v2.5 processing times
- [ ] Troubleshooting Runbook - Add v2.5-specific issues

---

## Knowledge Transfer

### Key Learnings
[Important discoveries or insights from this task]

1. [Learning 1]
2. [Learning 2]
3. [Learning 3]

**Example**:
1. Docling Worker v2.5 requires environment variable `DOCLING_MODEL_PATH` set
2. Service takes ~8s to fully initialize the model
3. First document after restart processes slower (~45s) due to model warmup

### Tips for Next Time
[Advice for anyone performing similar tasks]

- [Tip 1]
- [Tip 2]

**Example**:
- Always wait 30s after service start before processing first document
- Monitor memory usage - v2.5 uses 15% more RAM than v2.3
- Keep backup config for at least 7 days

### Related Resources
[Links to documentation, guides, or references]

- [Resource 1]
- [Resource 2]

**Example**:
- Docling Worker v2.5 Release Notes: `/srv/docs/docling-worker-v2.5-notes.md`
- Service Management Guide: `/srv/docs/service-operations.md`
- Rollback Procedures: `/srv/docs/rollback-guide.md`

---

## Coordination & Communication

### Notifications Sent

| Time | Recipient | Message |
|------|-----------|---------|
| [HH:MM] | [@agent] | [Message summary] |

**Example**:
| Time | Recipient | Message |
|------|-----------|---------|
| 14:30 | @agent-julia | Starting Docling Worker upgrade |
| 14:50 | @agent-eric | Upgrade complete, MCP can reconnect |
| 15:00 | All agents | Task T042 completed successfully |

### Handoffs

**To**: [@agent-name]
**What**: [What was handed off]
**Status**: [Current state]
**Next Steps**: [What they should do]

**Example**:
**To**: @agent-julia
**What**: Upgraded Docling Worker ready for testing
**Status**: Service running, basic validation passed
**Next Steps**: Run full performance test suite, verify 30s target

---

## Attachments

### Screenshots
[List any screenshots captured during execution]

- [Screenshot 1]: [Description]
- [Screenshot 2]: [Description]

### Log Excerpts
[Key log sections that provide evidence of success/failure]

```
[Relevant log output]
```

**Example**:
```
Nov 06 14:38:15 hx-docling-server systemd[1]: Starting Docling Worker v2.5...
Nov 06 14:38:23 hx-docling-server docling-worker[12345]: Model loaded: docling-v2.5
Nov 06 14:38:23 hx-docling-server docling-worker[12345]: Service ready on port 8080
Nov 06 14:38:23 hx-docling-server systemd[1]: Started Docling Worker v2.5
```

---

## Task Metadata

```yaml
task_id: [T###]
task_type: [Deployment/Configuration/Testing/Documentation/Other]
parent_work_item: [Link to parent]
assigned_agent: [@agent-name]
created_date: [YYYY-MM-DD]
completed_date: [YYYY-MM-DD]
status: [COMPLETED/FAILED/BLOCKED]
priority: [P1/P2/P3]
execution_type: [Parallel/Sequential]
estimated_duration: [X minutes]
actual_duration: [X minutes]
systems_affected: [list]
rollback_performed: [yes/no]
template: /srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.13-individual-task-template.md
```

---

## Template Usage Instructions

### When to Use This Template

Use this individual task template when:
- ✅ Task requires detailed step-by-step documentation
- ✅ Task affects critical systems or services
- ✅ Task has complex rollback procedures
- ✅ Detailed audit trail is required
- ✅ Task will be repeated or referenced later
- ✅ Multiple people need to understand the task

Use summary task list (0.0.6.11) when:
- ✅ Managing multiple related tasks
- ✅ Need to coordinate across agents
- ✅ Focus is on sequencing and dependencies

### How to Use This Template

1. **Copy template** to your project directory
2. **Fill in header** with task ID, assignment, status
3. **Define objective** and success criteria clearly
4. **List prerequisites** before starting work
5. **Document each step** as you execute it
6. **Record issues** and resolutions in real-time
7. **Capture results** and validation evidence
8. **Update status** as task progresses
9. **Complete metadata** when finished
10. **Archive** for future reference

### Best Practices

✅ **Document as you go** - Don't wait until after completion
✅ **Include actual commands** - Copy/paste exactly what you ran
✅ **Capture outputs** - Show success and failure messages
✅ **Note timestamps** - Helps with troubleshooting and audits
✅ **Be specific** - "Service failed" is not helpful, "Service failed with SIGKILL due to timeout" is
✅ **Link related tasks** - Reference blocking and dependent tasks
✅ **Think about next time** - Document what would help someone else

---

**Template Version**: 1.0  
**Maintained By**: Hana-X AI Governance  
**Template ID**: 0.0.6.13  
**Classification**: Individual Task Template  
**Related Templates**: 0.0.6.11 (Summary Task List), 0.0.6.9 (Work Plan), 0.0.6.10 (Work Spec)

---

**Version**: 1.0  
**Maintained By**: Agent Zero / Project Managers  
**Related Documents**:
- `0.0.6.8-summary-task-template.md` - Template
- `0.0.6.2-task-tracker-template.md` - Template  
**Classification**: Internal  
**Status**: Template - Ready for Use  
**Last Review**: 2025-11-06
