# Task: Install Graphics Libraries

**Task ID**: T-006
**Assigned Agent**: @agent-william
**Status**: NOT STARTED
**Priority**: P1 - Critical
**Execution Type**: Parallel
**Dependencies**: T-004
**Estimated Duration**: 15 minutes

---

## Objective
Install Cairo, Pango, and image processing libraries required for n8n canvas operations.

## Commands

```bash
sudo apt install -y \
  libcairo2-dev \
  libpango1.0-dev \
  libjpeg-dev \
  libgif-dev \
  librsvg2-dev \
  libpixman-1-dev \
  pkg-config \
  libpq-dev

# Verify installations
pkg-config --modversion cairo
pkg-config --modversion pango
pg_config --version
```

## Success Criteria
- [ ] All graphics libraries installed
- [ ] pkg-config can locate cairo and pango
- [ ] libpq-dev installed for PostgreSQL client libraries

## Validation
```bash
pkg-config --modversion cairo
pkg-config --modversion pango
pg_config --version
dpkg -l | grep libcairo2-dev
dpkg -l | grep libpq-dev
```

---
**Source**: agent-william-planning-analysis.md:410-429
