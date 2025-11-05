# Archived Templates

**Date Archived**: 2025-11-04
**Reason**: Context mismatch with Hana-X infrastructure deployment focus
**Archived By**: R5-D4 (Claude Code)
**Backlog Item**: BI-009

---

## Purpose of This Archive

This directory contains templates that were part of the original governance framework but were determined to be **misaligned with Hana-X infrastructure deployment needs**. These templates are preserved for reference and potential future use in application development contexts.

---

## Archived Templates

### t-0.1-plan-template.md
**Original Purpose**: Implementation plan for feature development
**Why Archived**:
- References external file system paths not in Hana-X (`/memory/constitution.md`, `.specify/` directories)
- Assumes command-based workflows (`/plan`, `/tasks` commands) not documented in Hana-X
- Focuses on software feature development (TDD, REST APIs, contracts) vs. infrastructure deployment
- References external scripts (`scripts/bash/update-agent-context.sh`) not part of Hana-X

**Hana-X Replacement**: t-0.8-deployment-plan-template.md (BI-002) aligned with Deployment Methodology

---

### t-0.2-spec-template.md
**Original Purpose**: Feature specification for user-facing functionality
**Why Archived**:
- Focuses on user stories, acceptance criteria for application features
- Not aligned with infrastructure deployment specifications (server configs, service deployments)
- Written for non-technical stakeholders vs. technical infrastructure team
- Execution flow assumes programmatic processing (`main()` functions)

**Hana-X Use Case**: May be useful for application layer features on hx-dev/hx-demo servers if needed in future

---

### t-0.3-tasks-template.md
**Original Purpose**: Task breakdown for TDD software development
**Why Archived**:
- TDD-focused workflow (Setup → Tests → Core → Integration → Polish)
- Source code structure references (`src/`, `tests/`, `backend/`, `frontend/`)
- Not aligned with infrastructure task breakdown (provision → configure → deploy → validate)
- Contract tests, unit tests focus vs. infrastructure validation

**Hana-X Replacement**: Task structure defined in Deployment Methodology §5 (task-by-task deployment validation)

---

## Context: Why These Templates Existed

These templates appear to have been created for a **software application development project** with:
- Automated CLI workflow tools (`/plan`, `/tasks` commands)
- Test-Driven Development (TDD) methodology
- Feature-based development (user stories → specs → tests → implementation)
- Different project structure (`.specify/` system, `/memory/` paths)

This is a **valid and well-structured approach** for application development, but does not align with Hana-X's focus on **infrastructure deployment** (servers, services, network configuration, system integration).

---

## Future Use

These templates may be valuable if Hana-X moves into **application development** phases on:
- **hx-dev-server** (192.168.10.222) - Development environment
- **hx-demo-server** (192.168.10.223) - Demo environment

At that time, these templates could be:
1. Reviewed and adapted for Hana-X context
2. Moved back to active templates directory
3. Used as reference for creating application-focused templates

---

## Decision Authority

**Approved By**: Agent Zero (Jarvis Richardson / AZ)
**Date**: 2025-11-04
**Governance Reference**: Traceability Matrix v1.1, Template Review Report 2025-11-04

---

## Active Templates (Post-Archive)

The following templates remain **active and aligned with Hana-X**:

| Template | Purpose | Status |
|----------|---------|--------|
| t-0.4-defect-log-template.md | Bug tracking and resolution | ✅ Active |
| t-0.5-task-tracker-template.md | Project work management | ✅ Active |
| t-0.6-backlog-template.md | Backlog prioritization | ✅ Active (In Use) |
| t-0.7-status-report-template.md | Project progress reporting | ✅ Active (Updated BI-010) |
| t-0.8-deployment-plan-template.md | Infrastructure deployment planning | ✅ Active (Created BI-002) |

---

## Related Documentation

- **Backlog Item BI-009**: Archive Legacy Templates
- **Backlog Item BI-002**: Create Deployment Plan Template (replacement for t-0.1)
- **Backlog Item BI-010**: Update Status Report Template (t-0.7)
- **Backlog Item BI-011**: Update Traceability Matrix §5.1
- **Template Review Report**: 2025-11-04
- **Traceability Matrix**: 0.5-hx-traceability-matrix.md §5.1

---

**Archive Status**: Complete
**Restore Procedure**: If needed, copy templates back to parent directory and update governance documents
