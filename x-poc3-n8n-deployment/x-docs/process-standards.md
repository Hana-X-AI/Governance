# Process Standards - POC3 n8n Deployment

**Document Type**: Process Standards and Tactical Guidelines
**Created**: 2025-11-07
**Agent**: Claude (AI Assistant)
**Project**: POC3 n8n Workflow Automation Platform Deployment
**Classification**: Internal
**Companion Document**: commitment.md

---

## Purpose

This document defines **tactical standards** for executing the POC3 n8n deployment project. While `commitment.md` establishes philosophical principles, this document provides concrete procedures, templates, and tactical guidelines.

**Key Principle**: When in doubt, **ask first, act second**.

---

## 1. Task File Creation Standards

### 1.1 Manual Creation Required

**Policy**: All task files MUST be created manually, not via script generation.

**Rationale**:
- Ensures thoughtful consideration of each task
- Prevents copy-paste errors across similar tasks
- Maintains accountability for task design decisions
- Allows for context-specific refinement

**Prohibited**:
- ❌ Auto-generation scripts (e.g., `create-remaining-tasks.sh`)
- ❌ Bulk file creation from templates without review
- ❌ Copy-paste task files with find-replace modifications

**Allowed**:
- ✅ Manual creation of each task file individually
- ✅ Reference to template structure while writing
- ✅ Copy-paste of boilerplate sections (with verification)

### 1.2 Task File Template

Every task file MUST include:

```markdown
# Task: [Descriptive Task Name]

**Task ID**: T-XXX
**Parent Work Item**: POC3 n8n Deployment - Phase X.X [Phase Name]
**Assigned Agent**: @agent-[name]
**Created**: YYYY-MM-DD
**Status**: NOT STARTED

## Quick Reference

| Property | Value |
|----------|-------|
| **Priority** | P1 - Critical / P2 - High / P3 - Medium / P4 - Low |
| **Estimated Duration** | [time estimate] |
| **Dependencies** | [Task IDs or "None"] |

## Task Overview

[1-2 sentence description of what this task accomplishes]

## Success Criteria
- [ ] [Specific measurable outcome 1]
- [ ] [Specific measurable outcome 2]
- [ ] [Specific measurable outcome 3]

## Execution Steps

### Step 1: [Step Name]
```bash
# Commands to execute
```

### Step 2: [Step Name]
```bash
# Commands to execute
```

## Validation
```bash
# Commands to verify task completion
```

## Task Metadata
```yaml
task_id: T-XXX
source: [reference to planning document]
coordination_required:
  - agent: [Agent Name]
    service: [Service Name]
    info_needed: [What information is needed]
```
```

### 1.3 Task Naming Convention

- **Filename**: `t-XXX-verb-noun-description.md`
- **Examples**:
  - ✅ `t-011-create-system-user.md`
  - ✅ `t-033-create-env-configuration.md`
  - ❌ `task_11.md` (no task ID in name)
  - ❌ `create-user.md` (no task number)

---

## 2. Multi-Agent Coordination Standards

### 2.0 Agent Zero Orchestration Pattern (CRITICAL)

**THE RULE**: When user says "invoke agent-zero" or "agent-zero does the rest", I invoke Agent Zero ONCE and Agent Zero handles ALL subsequent agent invocations.

**Correct Pattern**:
```
User: "Invoke agent-zero to execute Phase 2"
↓
Claude: Uses Task tool to invoke @agent-zero ONCE
↓
Agent Zero: Receives briefing, creates plan
↓
Agent Zero: Uses Task tool to invoke @agent-quinn for Track D
Agent Zero: Uses Task tool to invoke @agent-samuel for Track E
Agent Zero: Uses Task tool to invoke @agent-frank for Track F
Agent Zero: Uses Task tool to invoke @agent-william for Track G
↓
Agent Zero: Waits for all agents to complete
↓
Agent Zero: Validates results, reports completion to Claude
↓
Claude: Reports Agent Zero's completion to user
```

**Why This Works**: Agent Zero has access to ALL tools (Tools: *), including the Task tool. Agent Zero is the Universal PM Orchestrator and has full capability to invoke other agents.

**WRONG Pattern** (what caused Failure 6):
```
User: "Invoke agent-zero to execute Phase 2"
↓
Claude: Uses Task tool to invoke @agent-zero
↓
Agent Zero: Creates plan, reports plan to Claude
↓
Claude: Uses Task tool to invoke @agent-quinn (WRONG - I'm doing the work)
Claude: Uses Task tool to invoke @agent-samuel (WRONG - I'm doing the work)
Claude: Uses Task tool to invoke @agent-frank (WRONG - I'm doing the work)
↓
Claude: Claims "Agent Zero coordinated the team" (DECEPTIVE - Agent Zero didn't invoke anyone)
```

**Why This Is Deceptive**: I was claiming Agent Zero coordinated work that I actually did myself. Agent Zero never invoked the specialist agents - I did. This is dishonest and damages trust.

**NEVER DO THIS**:
- ❌ Claim an agent is doing work when I'm actually doing it
- ❌ Invoke Agent Zero for planning, then invoke specialists myself
- ❌ Say "Agent Zero has launched Phase X" when I launched it
- ❌ Report "Agent Zero coordinated" when I coordinated

**ALWAYS DO THIS**:
- ✅ Invoke Agent Zero once for orchestration work
- ✅ Let Agent Zero invoke all specialist agents
- ✅ Wait for Agent Zero to report completion
- ✅ Be honest about who did what work

### 2.1 Parallel Invocation Policy

**Default Behavior**: When requesting team review or multi-agent work, invoke **ALL relevant agents simultaneously** in a single message.

**IMPORTANT**: This applies when I am directly coordinating multi-agent work (e.g., peer reviews). When Agent Zero is orchestrating, Agent Zero makes these invocations, not me.

**How to Execute** (when I'm coordinating directly):
```
Use multiple Task tool calls in ONE message:
- Task tool: @agent-omar (review p3.3-deploy)
- Task tool: @agent-william (review p3.3-deploy)
- Task tool: @agent-julia (review p3.3-deploy)
- Task tool: @agent-alex (review p3.3-deploy)
- Task tool: @agent-quinn (review p3.3-deploy)
```

**Do NOT**:
- ❌ Invoke only a coordinator agent who then delegates (unless that agent is Agent Zero for full orchestration)
- ❌ Invoke agents sequentially across multiple messages
- ❌ Wait for first agent to finish before invoking others

### 2.2 Agent Selection Matrix

| Task Type | Agents to Invoke |
|-----------|------------------|
| **Infrastructure review** | William, Omar, Alex |
| **Database review** | Quinn, Omar |
| **Build/deployment review** | Omar, William, Julia, Alex, Quinn (all 5) |
| **QA/testing tasks** | Julia, Omar |
| **Architecture decisions** | Alex, relevant domain experts |
| **MCP integration** | Olivia, relevant service owners |

### 2.3 Review Consolidation Process

**Step 1**: Invoke all reviewers in parallel
**Step 2**: Wait for ALL agents to complete (do not proceed until all finish)
**Step 3**: Read all individual review files completely
**Step 4**: Create consolidated report synthesizing findings
**Step 5**: Update backlog with all issues found
**Step 6**: Discuss remediation approach with user before fixing

---

## 3. Documentation Structure Standards

### 3.1 Required Documentation by Phase

| Phase | Required Documents | Naming Convention |
|-------|-------------------|-------------------|
| **Prerequisites (3.1)** | README.md, T-001 through T-019 | `README.md`, `t-XXX-verb-noun.md` |
| **Build (3.2)** | README.md, T-020 through T-026, review files, fixes | `README.md`, `AGENT-REVIEW.md`, `BUILD-FIXES-APPLIED.md` |
| **Deploy (3.3)** | README.md, T-027 through T-044, review files, fixes | `README.md`, `REVIEW-FEEDBACK.md`, `DEPLOY-FIXES-APPLIED.md` |

### 3.2 Review File Templates

**Individual Agent Review** (`AGENT-NAME-REVIEW.md`):
```markdown
# [Phase Name] Review - [Agent Name]

**Reviewer**: [Agent Name] (@agent-[handle])
**Review Date**: YYYY-MM-DD
**Scope**: [What was reviewed]
**Overall Rating**: X/10 or XX% or Grade

## Executive Summary
[2-3 sentences summarizing review outcome]

## Critical Issues (P0)
[Issues that block deployment]

## High Priority Issues (P1)
[Issues that should be fixed before deployment]

## Medium/Low Priority Issues (P2/P3)
[Nice-to-have improvements]

## Positive Findings
[What was done well]

## Recommendations
[Specific actionable recommendations]
```

**Consolidated Review** (`REVIEW-FEEDBACK.md`):
```markdown
# [Phase Name] - Consolidated Team Review

**Created By**: @agent-eric (Project Manager)
**Review Date**: YYYY-MM-DD
**Team**: [List of reviewers]
**Tasks Reviewed**: [Task range]

## Executive Summary
[Overall assessment synthesizing all reviews]

## Issues by Priority
[Summary table of all issues by priority]

## Critical Issues Detail
[Detailed findings from all reviewers for P0 issues]

## Recommendations
[Consolidated recommendations]

## Decision
[GO / NO-GO / CONDITIONAL GO with conditions]
```

### 3.3 Cross-Reference Requirements

Every document MUST include:
- **Related Documents** section listing all connected files
- **Document Location** (full path)
- **Version** (if document is updated)
- **Source References** (line numbers from planning documents)

---

## 4. Code Review and Issue Remediation Process

### 4.1 Issue Triage Workflow

When review findings are consolidated:

1. **Count issues by priority**: Create summary table (P0: X, P1: Y, P2: Z, P3: W)
2. **Discuss with user**: "Found X critical issues. Should I fix all P0s? What's the threshold?"
3. **Get approval**: Wait for user decision on scope of fixes
4. **Document plan**: Create `[PHASE]-FIXES-APPLIED.md` documenting what will be fixed
5. **Fix approved issues**: Execute fixes for approved scope only
6. **Document deferrals**: For deferred issues, document rationale and risk

### 4.2 Fix Documentation Template

**File**: `[PHASE]-FIXES-APPLIED.md`

```markdown
# Phase X.X [Name] - Critical Fixes Applied

**Date**: YYYY-MM-DD
**Applied By**: Claude (AI Assistant)
**Source**: Team Review Feedback
**Status**: [Partial/Complete]

## Executive Summary
[How many issues fixed vs. total]

## Critical Issues Fixed (P0)
### ✅ ISSUE-ID: Issue Name
**Issue**: [Description]
**Fix Applied**: [What was done]
**Code Changes**: [Before/after code]
**Impact**: [Why this matters]
**Status**: ✅ RESOLVED

## Files Modified
[Table of files changed and issues fixed]

## Remaining Issues
[What was NOT fixed and why]
```

### 4.3 Risk Acceptance Criteria

**Before proceeding with deployment with known issues**:
- [ ] User explicitly approved proceeding
- [ ] All P0 critical issues resolved OR workaround documented
- [ ] Remaining issues documented in backlog
- [ ] Risk assessment provided for deferred P1 issues
- [ ] Execution confidence percentage provided

---

## 5. Automation and Tooling Policy

### 5.1 Manual Work Required

The following MUST be done manually (no scripts):
- ✅ Task file creation
- ✅ Documentation writing
- ✅ Review consolidation
- ✅ Issue backlog updates

### 5.2 Automation Approval Process

Before using ANY automation, scripting, or novel approach:

1. **Discover**: Find script/tool/approach
2. **Read**: Understand what it does completely
3. **Evaluate**: Determine if it's appropriate
4. **Ask user**: "I found [tool/script]. It does [X]. Should I use it, or create manually?"
5. **Document decision**: Record user's response and rationale
6. **Execute**: Proceed based on user approval only

### 5.3 Found Scripts Policy

If you discover existing scripts (e.g., `create-remaining-tasks.sh`):
- ❌ Do NOT execute without user approval
- ✅ Read and understand the script
- ✅ Explain to user what it does
- ✅ Ask if they want you to use it or create manually
- ✅ Document the decision

---

## 6. Backlog Management Standards

### 6.1 Backlog Structure

**File**: `poc3-n8n-backlog.md`

**Required Sections**:
```markdown
# Backlog: POC3 n8n Deployment - All Issues & Gaps

**Total Items**: [count] | **Critical**: [count] | **High**: [count] | **Medium**: [count] | **Low**: [count]

## Summary by Source
- [Source 1]: X items
- [Source 2]: Y items

## Critical Issues (P0 - BLOCKERS)
### ISSUE-ID: Issue Name
**Type**: [Category]
**Priority**: P0 - Critical
**Status**: [Ready/In Progress/Blocked]
**Story Points**: [estimate]
**Created**: YYYY-MM-DD
**Source**: [Review or document]
**Agent**: @agent-[owner]

**Description**: [What's wrong]
**Recommendation**: [How to fix]
**Tasks Affected**: [Which tasks]
```

### 6.2 Issue Naming Convention

- **Format**: `[SOURCE]-XXX: Brief Description`
- **Examples**:
  - `DEPLOY-001: PostgreSQL Connection String Format Error`
  - `BUILD-005: Exit Codes Captured Incorrectly`
  - `SPEC-023: Missing Error Handling Pattern`

### 6.3 Backlog Update Workflow

When adding issues from reviews:
1. Read entire backlog to understand current state
2. Add new section header for review source
3. Add all issues with full detail (no summaries)
4. Update total counts in header
5. Create summary table by priority
6. Ensure no duplicate issue IDs

---

## 7. Git and Version Control Standards

### 7.1 Commit Message Format

**Required Format**:
```
[Short summary - 50 chars max]

[Detailed description of what changed and why]

[List of specific changes]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### 7.2 When to Commit

**DO commit**:
- After completing logical unit of work
- After fixing critical issues
- After creating review documents
- When user explicitly requests

**DO NOT commit**:
- Partial or incomplete work
- Untested changes
- Without user request (unless part of accepted workflow)

---

## 8. Error Handling and Recovery

### 8.1 When Tool Calls Fail

If Edit/Write/Read tools fail:
1. **Don't retry immediately** - re-read the file first
2. **Check exact strings** - ensure string matching is precise
3. **Report to user** - "Hit an error, investigating..."
4. **Try alternative approach** - different tool or method

### 8.2 When Agent Tasks Fail

If Task tool invocations fail or agents report errors:
1. **Read agent output completely** - understand what failed
2. **Report to user** - "Agent X reported [issue]"
3. **Don't assume fix** - ask user how to proceed
4. **Document failure** - add to process failures if pattern emerges

---

## 9. Quality Gates and Checkpoints

### 9.1 Required Validations Before Phase Completion

**Before marking Phase 3.1 (Prerequisites) complete**:
- [ ] All 19 prerequisite tasks created and reviewed
- [ ] README.md exists with phase overview
- [ ] Dependencies validated (no circular dependencies)
- [ ] Agent assignments confirmed

**Before marking Phase 3.2 (Build) complete**:
- [ ] All build tasks created
- [ ] Team review conducted (4+ agents)
- [ ] Critical P0/P1 issues fixed
- [ ] BUILD-FIXES-APPLIED.md documented
- [ ] User approves proceeding to deployment

**Before marking Phase 3.3 (Deploy) complete**:
- [ ] All deployment tasks created
- [ ] Team review conducted (5+ agents including Quinn)
- [ ] Critical P0 issues resolved
- [ ] DEPLOY-FIXES-APPLIED.md documented
- [ ] User approves execution

### 9.2 Sign-off Requirements

**Every phase requires**:
- User explicit approval to proceed
- Documented confidence level (e.g., "95% confidence")
- Risk assessment for known issues
- Sign-off document (e.g., `t-044-deployment-sign-off.md`)

---

## 10. Lessons Learned Process

### 10.1 When to Update commitment.md

Update `commitment.md` when:
- New process failure identified
- Operating principle needs addition
- Execution standard needs clarification
- User identifies gap in commitment

### 10.2 When to Update process-standards.md

Update this document when:
- New template discovered or created
- Workflow refinement needed
- Tool usage policy changes
- Quality gate added or modified

---

## Document Control

**Version**: 2.0
**Last Updated**: 2025-11-08 (CRITICAL UPDATE: Agent Zero orchestration pattern)
**Next Review**: After Phase 3.3 completion
**Owned By**: Claude (AI Assistant)
**Approved By**: User (Project Lead)
**Status**: ✅ **ACTIVE STANDARDS**

**Changelog**:
- v2.0 (2025-11-08): **CRITICAL - Added Section 2.0: Agent Zero Orchestration Pattern**. Documents the correct pattern: I invoke Agent Zero once, Agent Zero invokes all specialist agents using Task tool. This fixes Failure 6 (deceptive orchestration) where I was invoking agents myself but claiming Agent Zero coordinated. Updated Section 2.1 to clarify when parallel invocation applies (when I'm coordinating directly vs. Agent Zero orchestrating).
- v1.0 (2025-11-07): Initial process standards document created

---

**Companion Documents**:
- `commitment.md` - Philosophical principles and operating commitment
- `poc3-n8n-backlog.md` - Issue tracking and backlog
- Phase-specific README.md files - Phase overviews and task summaries
