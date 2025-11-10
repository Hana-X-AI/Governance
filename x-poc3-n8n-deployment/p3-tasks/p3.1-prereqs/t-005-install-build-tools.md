# Task: Install Build Tools and Core Dependencies

**Task ID**: T-005
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Parallel
**Dependencies**: T-004
**Estimated Duration**: 20 minutes

---

## Objective
Install compiler toolchain and core system dependencies for n8n build.

## Commands

```bash
sudo apt install -y \
  build-essential \
  python3 \
  python3-pip \
  git \
  curl \
  ca-certificates \
  apt-transport-https \
  software-properties-common

# Verify installations
gcc --version
g++ --version
make --version
python3 --version
git --version
```

## Success Criteria
- [ ] All packages installed without errors
- [ ] gcc, g++, make functional
- [ ] Python 3.x installed
- [ ] Git functional

## Validation
```bash
gcc --version
python3 --version
git --version
```

---
**Source**: agent-william-planning-analysis.md:384-408
