# n8n MCP Server Deployment: Process Rules

**Document Type**: Process Rules
**Created**: November 11, 2025
**Project Code**: HX-N8N-MCP-001
**Classification**: Internal - Project Management
**Authority**: CAIO (Jarvis Richardson)
**Enforcement**: Mandatory for all project team members

---

## Overview

These process rules govern the execution of the n8n MCP Server deployment project (HX-N8N-MCP-001). All team members must follow these rules throughout the project lifecycle. Non-compliance may result in task rejection, rework, or escalation to the CAIO.

**Scope**: This document applies to:
- All agents working on project tasks
- All documentation creation and updates
- All code and configuration changes
- All quality assurance activities
- All phase gate reviews

---

## Process Rules

### Rule 1: CodeRabbit Analysis Required

**Rule**: Run CodeRabbit analysis after completing each task, or as explicitly directed by the CAIO.

**Applies To**:
- All documentation creation or updates
- All code changes
- All configuration file modifications
- Phase completion checkpoints
- Any work product before marking task "complete"

**Execution**:
```bash
coderabbit --prompt-only --type all --cwd [working-directory]
```

**Requirements**:
- CodeRabbit must complete successfully (exit code 0)
- CRITICAL and HIGH severity issues must be resolved before task acceptance
- MEDIUM severity issues should be resolved or documented in RAID log
- LOW severity issues may be deferred with justification

**Exemptions**:
- Read-only operations (file reads, status checks, log reviews)
- Emergency hotfixes (with CAIO approval and post-fix analysis)

**Evidence Required**:
- CodeRabbit analysis results (stdout/summary)
- Issue remediation proof (git diff or RAID log entry for deferred items)

**Enforcement**: Agent Zero will validate CodeRabbit compliance at task acceptance and phase gates.

---

### Rule 2: Naming Standards Compliance

**Rule**: Follow and enforce HANA-X naming standards from `/srv/cc/Governance/0.0-governance/0.0.1-Planning/0.0.1.0-naming-standards.md`.

**Standards Summary**:

**File Naming**:
- Use kebab-case: all lowercase, hyphens for spaces (e.g., `project-plan.md`, `test-results.json`)
- Template files: `t-0.##-[name]-template.md`
- Hierarchical numbering: `0.0.#.#-[name].md`
- README.md always capitalized (exception to lowercase rule)
- No redundant prefixes at root level (use `project-plan.md`, not `n8n-mcp-server-project-plan.md`)

**Metadata Headers** (Required for all documents):
```markdown
**Document Type**: [Type]
**Created**: YYYY-MM-DD
**Classification**: [Internal/Confidential/Public]
```

**Directory Structure**:
- Phase directories: `01-phase1-research-planning/`, `02-phase2-infrastructure/`, etc.
- Supporting directories: `10-testing/`, `20-risks-issues/`, `00-foundation/`
- No mixed case in directory names

**Applies To**:
- All new files created
- All directory structures
- All document metadata
- All file references in documentation
- All git commit messages

**Validation**:
- Agent Zero will review all naming during task acceptance
- CodeRabbit analysis (Rule 1) will detect naming violations
- Non-compliant files will be rejected for renaming

**Enforcement**: Files not following naming standards will not be accepted and must be corrected before task completion.

---

### Rule 3: No Password Rotation

**Rule**: Passwords and credentials will NOT be rotated during this project.

**Rationale**:
- Project duration is 18 days (short-term deployment)
- Credential rotation introduces unnecessary complexity and risk
- Focus on delivery over operational maintenance activities
- Existing credentials are sufficient for project scope

**Applies To**:
- All service accounts (Samba DC, database accounts, API keys)
- All shared credentials used for integration
- All authentication tokens and certificates
- Any credentials generated during deployment

**Exceptions** (Require CAIO Approval):
- Credential compromise or security incident
- Regulatory requirement discovered during project
- Critical security vulnerability requiring immediate rotation

**Clarifications**:
- Initial credential creation for NEW services is allowed and required
- Updating incorrect or non-functional credentials is allowed
- Certificate renewal due to expiration is allowed (not considered rotation)

**Documentation**:
- All credentials must be documented per credentials-standards.md
- No credential rotation schedules will be created during this project
- Post-project handoff will include credential inventory (static snapshot)

**Enforcement**: Any password rotation activity requires explicit CAIO approval via escalation to Agent Zero.

---

## Rule Compliance Checklist

Before marking any task "complete", validate:

- [ ] **Rule 1**: CodeRabbit analysis run and issues resolved/documented
- [ ] **Rule 2**: All files follow naming standards (kebab-case, metadata, structure)
- [ ] **Rule 3**: No password rotation performed (unless CAIO-approved exception)

---

## Rule Violations

**Reporting**: Any team member who identifies a rule violation must:
1. Immediately notify Agent Zero
2. Document the violation (what, when, who, impact)
3. Halt affected work until resolved

**Remediation**:
1. **Minor Violation** (e.g., missed CodeRabbit on low-risk task):
   - Run CodeRabbit immediately
   - Fix any issues found
   - Update RAID log if needed
   - No escalation required

2. **Moderate Violation** (e.g., multiple naming standard violations):
   - Fix all violations immediately
   - Agent Zero review required before proceeding
   - RAID log entry created for tracking
   - May delay phase gate approval

3. **Major Violation** (e.g., password rotation without approval):
   - Immediately escalate to CAIO
   - Work stoppage until resolution
   - Root cause analysis required
   - Corrective action plan required

---

## Rule Updates

**Authority**: Only the CAIO may update these process rules.

**Process**:
1. Proposed change documented with rationale
2. Impact assessment by Agent Zero
3. CAIO approval required
4. All team members notified
5. Change log updated below

**Emergency Changes**: CAIO may update rules verbally with retroactive documentation within 24 hours.

---

## Change Log

| Version | Date | Author | Change Description |
|---------|------|--------|-------------------|
| 1.0 | 2025-11-11 | CAIO (Jarvis Richardson) via Agent Zero | Initial process rules established |

---

## Acknowledgment

By working on this project, all team members acknowledge:
- I have read and understood these process rules
- I will comply with all rules throughout project execution
- I will report any violations immediately
- I understand non-compliance may result in task rejection or rework

---

**Status**: ✅ ACTIVE
**Last Reviewed**: November 11, 2025
**Next Review**: Phase 4 Gate (or as needed)
**Owner**: Agent Zero (enforcement)
**Authority**: CAIO (rule-making)
