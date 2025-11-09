# Phase 3.2: Build Tasks

**Phase**: POC3 n8n Deployment - Phase 3.2 (Build)
**Agent**: @agent-omar (Omar Rodriguez - N8N Workflow Worker Specialist)
**Created**: 2025-11-07
**Status**: Task files created, ready for execution

---

## Overview

This directory contains 7 individual task files for Phase 3.2 (Build) of the POC3 n8n deployment project. These tasks build the n8n application from source code, creating production-ready compiled artifacts.

---

## Task List

### Category 1: Build Preparation (T-020 to T-022)
Prepare build environment and verify prerequisites

| Task ID | Task Name | Duration | Description |
|---------|-----------|----------|-------------|
| **T-020** | Verify Build Prerequisites | 15 min | Verify Node.js, pnpm, build tools, n8n user |
| **T-021** | Clone n8n Repository | 10 min | Copy n8n-master from knowledge vault to /opt/n8n/build/ |
| **T-022** | Prepare Build Environment | 20 min | Verify disk space (≥20GB), setup logging, review docs |

**Subtotal**: 45 minutes

---

### Category 2: Application Build (T-023 to T-026)
Execute build process and validate output

| Task ID | Task Name | Duration | Description |
|---------|-----------|----------|-------------|
| **T-023** | Install Dependencies | 10-15 min | Execute pnpm install (2000+ packages) |
| **T-024** | Build n8n Application | 20-30 min | Execute pnpm build:deploy (30+ packages) |
| **T-025** | Verify Build Output | 10 min | Validate dist/ directories and compiled artifacts |
| **T-026** | Test Build Executable | 5 min | Test n8n CLI (node packages/cli/bin/n8n --version) |

**Subtotal**: 45-60 minutes

---

## Total Duration

**Estimated Total**: 90-105 minutes (1.5-1.75 hours)

**Critical Path**: T-020 → T-021 → T-022 → T-023 → T-024 → T-025 → T-026

**Longest Task**: T-024 (Build n8n Application) - 20-30 minutes for Turbo to compile 30+ packages

---

## Prerequisites

### From Phase 3.1 (Infrastructure Prerequisites)
All tasks T-001 through T-019 must be complete:

- [x] **Node.js ≥22.16.0** installed (T-009)
- [x] **pnpm 10.18.3** installed via corepack (T-010)
- [x] **Build tools** installed: gcc, g++, make, python3 (T-005)
- [x] **Graphics libraries** installed: cairo, pango, libpng (T-006)
- [x] **PostgreSQL client** installed (T-007)
- [x] **System user** `n8n:n8n` created (T-011)
- [x] **Directory structure** `/opt/n8n/` created (T-012)
- [x] **Disk space**: ≥20GB free on /opt partition

### Knowledge Vault Access
- Source repository: `/srv/knowledge/vault/n8n-master/` (n8n version 1.117.0)

---

## Build Process Details

### Build System
- **Package Manager**: pnpm 10.18.3 (strict requirement - must be installed via corepack)
- **Build Orchestrator**: Turbo (monorepo build system)
- **Compiler**: TypeScript → JavaScript (tsc)
- **Target**: ES2022 JavaScript modules

### Build Commands
```bash
# Dependency installation
pnpm install
# Expected: 2000+ packages installed in ~10-15 minutes

# Application compilation
pnpm build:deploy
# Expected: 30+ packages compiled in ~20-30 minutes
# Output: packages/*/dist/ directories with compiled JavaScript
```

### Build Output
- **Location**: `/opt/n8n/build/packages/*/dist/`
- **Format**: Compiled JavaScript files (.js), type declarations (.d.ts), source maps (.js.map)
- **Critical packages**:
  - `packages/cli/dist/` - Main CLI application
  - `packages/core/dist/` - Core workflow engine
  - `packages/workflow/dist/` - Workflow execution
  - `packages/nodes-base/dist/` - Standard nodes
  - `packages/editor-ui/dist/` - Web UI

### Build Validation
- **CLI executable**: `packages/cli/bin/n8n`
- **Version check**: `node packages/cli/bin/n8n --version` returns `1.117.0`
- **No TypeScript source in dist/**: Only .js, .d.ts, .js.map files
- **Package count**: 30+ packages with dist/ directories

---

## Success Criteria

Phase 3.2 is complete when:

- [ ] All task files T-020 through T-026 executed successfully
- [ ] Build prerequisites verified (Node.js, pnpm, build tools)
- [ ] n8n repository cloned to `/opt/n8n/build/`
- [ ] Build environment prepared (disk space, logging, docs)
- [ ] Dependencies installed (`pnpm install` successful, 2000+ packages)
- [ ] Application built (`pnpm build:deploy` successful, 30+ packages)
- [ ] Build output validated (all critical packages have dist/ directories)
- [ ] CLI executable tested (`n8n --version` returns 1.117.0)
- [ ] Build log captured in `/opt/n8n/logs/build.log`
- [ ] No critical errors in build output
- [ ] Build verification report generated (T-025)
- [ ] Executable test report generated (T-026)

---

## Critical Requirements

### Node.js Version
**Required**: ≥22.16.0 and <25.0.0
**Validation**:
```bash
node --version
# Expected: v22.x.x or v24.x.x
```

**Why critical**: n8n 1.117.0 requires Node.js 22.x or 24.x. Earlier or later versions will fail.

### pnpm Version
**Required**: Exactly 10.18.3 (installed via corepack)
**Validation**:
```bash
pnpm --version
# Expected: 10.18.3

which pnpm
# Expected: /usr/local/bin/pnpm (via corepack, not npm install -g)
```

**Why critical**: n8n's package.json specifies `"packageManager": "pnpm@10.18.3"`. Other versions may cause build failures.

**Rationale for Exact Version Pinning**:
- **node_modules Layout**: Different pnpm versions use different dependency hoisting algorithms, producing different node_modules structures even from the same lockfile
- **Lockfile Format**: pnpm lockfile format (pnpm-lock.yaml) evolves between versions; newer pnpm may not honor older lockfile constraints correctly
- **Reproducibility**: Exact version ensures identical dependency resolution across development, CI/CD, and production builds
- **Deterministic Builds**: Prevents "works on my machine" issues caused by subtle pnpm version differences

### Disk Space
**Required**: ≥20GB free on /opt partition
**Validation**:
```bash
df -h /opt
# Expected: 20GB+ available
```

**Why critical**: Build artifacts, dependencies, and source code require ~15-18GB total.

### Build Duration
**Expected**: 1.5-1.75 hours total
**Breakdown**:
- T-020 to T-022 (Prep): 45 min
- T-023 (Dependencies): 10-15 min
- T-024 (Build): 20-30 min
- T-025 to T-026 (Validation): 15 min

**Warning**: If build exceeds 2 hours, investigate performance issues (disk I/O, memory constraints).

---

## Common Issues & Troubleshooting

### Issue 1: pnpm Version Mismatch
**Symptom**: Build fails with "packageManager" error
**Solution**: Reinstall pnpm via corepack (See T-010 in Phase 3.1)

### Issue 2: Out of Memory
**Symptom**: Build killed during Turbo compilation
**Solution**: Close unnecessary processes, verify 4+ GB RAM available

### Issue 3: Disk Space Exhaustion
**Symptom**: "ENOSPC: no space left on device"
**Solution**: Clean up /tmp, verify ≥20GB free before starting

### Issue 4: Network Timeout
**Symptom**: pnpm install fails with timeout
**Solution**: Retry with `pnpm install --network-timeout 300000`

### Issue 5: TypeScript Errors
**Symptom**: Build fails with "TS" errors
**Solution**: Verify Node.js version correct, clean node_modules and retry

---

## Rollback Procedures

All tasks include individual rollback procedures. General rollback process:

1. **Stop any running builds**: `Ctrl+C` or kill build process
2. **Clean build artifacts**:
   ```bash
   cd /opt/n8n/build/
   rm -rf node_modules packages/*/dist packages/*/node_modules
   pnpm store prune
   ```
3. **Document failure**: Record error messages and context in `/opt/n8n/logs/build.log`
4. **Investigate root cause**: Review logs, verify prerequisites
5. **Retry after fixes**: Re-execute from T-020 or failed task

---

## Agent Coordination

### Primary Agent
**@agent-omar** (Omar Rodriguez - N8N Workflow Worker Specialist)
- Responsible for: All build tasks T-020 through T-026
- Knowledge source: `/srv/knowledge/vault/n8n-master`
- Expertise: n8n monorepo build process, pnpm workspaces, Turbo orchestration

### Supporting Agents

**@agent-william** (William Taylor - Ubuntu Systems)
- Phase 3.1 infrastructure tasks complete (T-004 through T-015)
- Available for system-level issues (permissions, disk space, package installation)

**@agent-julia** (Julia Santos - Testing & QA)
- Will review build validation steps (T-025, T-026)
- Available for test procedure feedback

**@agent-alex** (Alex Rivera - Platform Architect)
- Available for architecture questions
- Reviews build process alignment with platform standards

---

## Next Phase

**Phase 3.3: Deployment**

After T-026 sign-off:
- Handoff to @agent-omar for deployment tasks (T-027 through T-044)
- Deploy artifacts from `/opt/n8n/build/` to `/opt/n8n/app/`
- Create systemd service and start n8n
- Expected duration: ~2.5 hours

---

## Task File Template

All task files follow the standard individual task template:
- Template: `/srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md`
- Structure: Quick Reference, Task Overview, Prerequisites, Detailed Steps, Validation, Rollback, Results, Metadata
- Detail level: Comprehensive with commands, expected output, validation, troubleshooting

---

## File Locations

**Task files**: `/srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.2-build/t-*.md`

**Planning source**: `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md:450-500`

**Build location**: `/opt/n8n/build/` on hx-n8n-server.hx.dev.local (192.168.10.215)

**Logs**:
- Build log: `/opt/n8n/logs/build.log`
- Build verification: `/opt/n8n/docs/build-verification-report.md`
- Executable test: `/opt/n8n/docs/executable-test-report.md`

**Documentation**: `/opt/n8n/docs/`

---

## Notes

1. **SOLID Principles Applied**: Each task has single responsibility (one build phase per task)
2. **Sequential Execution**: Tasks must run in order T-020 → T-026 (no parallel execution)
3. **Comprehensive Logging**: All build output captured in `/opt/n8n/logs/build.log`
4. **Validation Gates**: T-025 and T-026 ensure build quality before deployment
5. **Build Time Tracking**: Each task records start/end times for performance analysis
6. **Resource Monitoring**: Tasks include memory and disk space checks
7. **Rollback Safety**: Clean rollback procedures allow retry without data loss
8. **Documentation**: Complete build reports generated for audit trail
9. **Observability**: Structured logs for build duration and performance metrics enable post-build analysis and performance trend tracking across multiple deployments

---

**Created**: 2025-11-07
**Agent**: @agent-omar
**Status**: ✅ All 7 task files created and ready for execution
**Next Action**: Execute T-020 after confirming Phase 3.1 complete

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial README creation for Phase 3.2 Build tasks | @agent-omar |
| 1.1 | 2025-11-07 | **CodeRabbit Remediation**: (1) Added rationale for exact pnpm version pinning (lines 156-160) explaining node_modules layout differences, lockfile format evolution, and reproducibility requirements. (2) Added observability note (#9, line 297) to Notes section emphasizing structured logs for build duration and performance metrics to enable trend tracking across deployments. | Claude Code |
