# Task: Install pnpm 10.18.3

**Task ID**: T-010
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-009
**Estimated Duration**: 10 minutes

---

## Objective
Install pnpm 10.18.3 via corepack (strict version requirement).

## Commands

```bash
# Enable corepack
sudo corepack enable

# Prepare pnpm 10.18.3
sudo corepack prepare pnpm@10.18.3 --activate

# Verify version
pnpm --version  # Must be exactly 10.18.3

# Test pnpm
pnpm --help
```

## Success Criteria
- [ ] pnpm version 10.18.3 installed (exact version)
- [ ] pnpm command functional

## Validation
```bash
pnpm --version
which pnpm
```

---
**Source**: phase3-execution-plan.md:250-255, agent-william-planning-analysis.md:490-509
