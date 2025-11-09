# Task: Install Node.js 22.x LTS

**Task ID**: T-009
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Sequential
**Dependencies**: T-005
**Estimated Duration**: 20 minutes

---

## Objective
Install Node.js version ≥22.16.0 using NodeSource repository.

## Commands

```bash
# Add NodeSource repository
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -

# Install Node.js
sudo apt install -y nodejs

# Verify version
node --version  # Should be ≥22.16.0
npm --version

# Test Node.js
node -e "console.log('Node.js installed successfully')"
```

## Success Criteria
- [ ] Node.js ≥22.16.0 installed
- [ ] npm installed
- [ ] Test script executes successfully

## Validation
```bash
node --version
npm --version
which node
```

---
**Source**: phase3-execution-plan.md:236-263, agent-william-planning-analysis.md:468-488
