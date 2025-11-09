# Phase 3.1: Infrastructure Prerequisites Tasks

**Phase**: POC3 n8n Deployment - Phase 3.1 (Infrastructure Prerequisites)
**Primary Agents**: @agent-frank, @agent-william, @agent-quinn
**Created**: 2025-11-07
**Status**: Task files created, ready for execution

---

## Overview

This directory contains 19 individual task files for Phase 3.1 (Infrastructure Prerequisites) of the POC3 n8n deployment project. These tasks establish the foundational infrastructure required before building and deploying the n8n application.

---

## Task List

### Category 1: DNS & SSL (T-001 to T-003)
Configure DNS and SSL certificates - **Agent: @agent-frank**

| Task ID | Task Name | Duration | Agent | Description |
|---------|-----------|----------|-------|-------------|
| **T-001** | Create DNS Record | 10 min | @agent-frank | Create hx-n8n-server.hx.dev.local → 192.168.10.215 |
| **T-002** | Generate SSL Certificate | 15 min | @agent-frank | Generate from Samba CA |
| **T-003** | Transfer SSL Certificate | 5 min | @agent-frank | Transfer cert to hx-n8n-server |

**Subtotal**: 30 minutes

---

### Category 2: Server Provisioning (T-004)
Provision Ubuntu server - **Agent: @agent-william**

| Task ID | Task Name | Duration | Agent | Description |
|---------|-----------|----------|-------|-------------|
| **T-004** | Provision Ubuntu Server | 30 min | @agent-william | Install Ubuntu 24.04 LTS, domain join |

**Subtotal**: 30 minutes

---

### Category 3: System Dependencies (T-005 to T-010)
Install system-level dependencies - **Agent: @agent-william**

| Task ID | Task Name | Duration | Agent | Description |
|---------|-----------|----------|-------|-------------|
| **T-005** | Install Build Tools | 10 min | @agent-william | gcc, g++, make, python3 |
| **T-006** | Install Graphics Libraries | 10 min | @agent-william | cairo, pango, libpng |
| **T-007** | Install PostgreSQL Client | 5 min | @agent-william | psql client tools |
| **T-008** | Install Nginx | 10 min | @agent-william | Reverse proxy server |
| **T-009** | Install Node.js | 10 min | @agent-william | Node.js ≥22.16.0 |
| **T-010** | Install pnpm | 5 min | @agent-william | pnpm 10.18.3 via corepack |

**Subtotal**: 50 minutes

---

### Category 4: System Configuration (T-011 to T-014)
Configure system user and settings - **Agent: @agent-william**

| Task ID | Task Name | Duration | Agent | Description |
|---------|-----------|----------|-------|-------------|
| **T-011** | Create Service User | 5 min | @agent-william | Create n8n:n8n system user |
| **T-012** | Create Directory Structure | 5 min | @agent-william | /opt/n8n/, /var/log/n8n/, etc. |
| **T-013** | Configure Firewall | 10 min | @agent-william | UFW rules for 5678, 443, 22 |
| **T-014** | Configure System Tuning | 10 min | @agent-william | Kernel params, limits |

**Subtotal**: 30 minutes

---

### Category 5: Service Templates (T-015 to T-016)
Create service configuration templates - **Agent: @agent-william** (T-015), **@agent-frank** (T-016)

| Task ID | Task Name | Duration | Agent | Description |
|---------|-----------|----------|-------|-------------|
| **T-015** | Create Systemd Service | 10 min | @agent-william | Template systemd unit file |
| **T-016** | Configure Nginx SSL | 15 min | @agent-frank | Nginx virtual host with SSL |

**Subtotal**: 25 minutes

---

### Category 6: Database Setup (T-017 to T-019)
Configure PostgreSQL database - **Agent: @agent-quinn**

| Task ID | Task Name | Duration | Agent | Description |
|---------|-----------|----------|-------|-------------|
| **T-017** | Create PostgreSQL Database | 5 min | @agent-quinn | Create n8n_poc3 database |
| **T-018** | Create PostgreSQL User | 5 min | @agent-quinn | Create n8n_user with password |
| **T-019** | Validate Database Connection | 5 min | @agent-quinn | Test connectivity from hx-n8n-server |

**Subtotal**: 15 minutes

---

## Total Duration

**Estimated Total**: 180 minutes (3 hours)

**Critical Path**:
1. T-001 (DNS) → T-002 (SSL) → T-003 (Transfer)
2. T-004 (Server) → T-005-T-010 (Dependencies) → T-011-T-014 (Config)
3. T-017 (DB) → T-018 (User) → T-019 (Validate)

**Parallel Execution Opportunities**:
- Frank's DNS/SSL tasks (T-001 to T-003) can run parallel to William's server provisioning (T-004)
- Quinn's database tasks (T-017 to T-019) can run parallel to William's system config (T-011 to T-014)

---

## Prerequisites

### Required Access
- **@agent-frank**: Access to Samba CA for SSL certificates, DNS server access
- **@agent-william**: SSH access to hx-n8n-server, sudo privileges
- **@agent-quinn**: Access to hx-postgres-server (192.168.10.209), PostgreSQL admin privileges

### Required Information
- Server IP: 192.168.10.215
- Hostname: hx-n8n-server.hx.dev.local
- Domain: hx.dev.local
- PostgreSQL server: hx-postgres-server.hx.dev.local (192.168.10.209)
- Database name: n8n_poc3
- Database user: n8n_user

---

## Agent Coordination

### Primary Agents

**@agent-frank** (Frank Lucas - Identity & Trust)
- Responsible for: T-001, T-002, T-003, T-016
- DNS and SSL certificate management
- Nginx SSL configuration

**@agent-william** (William Taylor - Ubuntu Server)
- Responsible for: T-004 through T-015 (except T-006)
- Server provisioning and system configuration
- Most tasks in this phase

**@agent-quinn** (Quinn Davis - PostgreSQL)
- Responsible for: T-017, T-018, T-019
- Database setup and validation

---

## Success Criteria

Phase 3.1 is complete when:

- [ ] All task files T-001 through T-019 executed successfully
- [ ] DNS resolves: `nslookup hx-n8n-server.hx.dev.local` returns 192.168.10.215
- [ ] SSL certificate deployed and valid
- [ ] Ubuntu server online and domain-joined
- [ ] Node.js ≥22.16.0 installed
- [ ] pnpm 10.18.3 installed via corepack
- [ ] All build dependencies installed (gcc, make, python3, cairo, pango)
- [ ] System user `n8n:n8n` created
- [ ] Directory structure `/opt/n8n/` created with correct ownership
- [ ] Firewall configured (ports 22, 443, 5678)
- [ ] PostgreSQL database `n8n_poc3` created
- [ ] PostgreSQL user `n8n_user` created with password
- [ ] Database connection validated from hx-n8n-server
- [ ] All prerequisite validation reports generated

---

## Critical Blockers

### Blocker 1: Server Availability
**Task**: T-004
**Impact**: All subsequent tasks blocked until server is online
**Owner**: @agent-william

### Blocker 2: DNS Resolution
**Task**: T-001
**Impact**: Affects SSL certificate generation and validation
**Owner**: @agent-frank

### Blocker 3: Database Credentials
**Task**: T-018
**Impact**: Password needed for Phase 3.3 deployment configuration
**Owner**: @agent-quinn
**Action**: Securely communicate n8n_user password to @agent-omar

---

## Execution Order

Tasks should be executed in this order:

**Stage 1: DNS & Server Foundation** (Can run in parallel)
- Track A: T-001 → T-002 → T-003 (Frank: DNS/SSL)
- Track B: T-004 (William: Server provisioning)

**Stage 2: System Dependencies** (Sequential after T-004)
- T-005 → T-006 → T-007 → T-008 → T-009 → T-010 (William)

**Stage 3: System Configuration** (Sequential after Stage 2)
- T-011 → T-012 → T-013 → T-014 (William)

**Stage 4: Service Templates** (Can run in parallel)
- Track A: T-015 (William: Systemd)
- Track B: T-016 (Frank: Nginx SSL, requires T-003)

**Stage 5: Database Setup** (Can run parallel to Stage 2-4)
- T-017 → T-018 → T-019 (Quinn)

**CHECKPOINT**: All prerequisites validated before Phase 3.2

---

## Next Phase

**Phase 3.2: Build**

After all T-001 through T-019 complete successfully:
- Handoff to @agent-omar for n8n build tasks (T-020 through T-026)
- Build location: `/opt/n8n/build/`
- Expected duration: 1.5-1.75 hours

---

## Task File Template

All task files follow the standard individual task template:
- Template: `/srv/cc/Governance/0.0-governance/0.0.6-Templates/0.0.6.10-individual-task-template.md`
- Structure: Quick Reference, Task Overview, Prerequisites, Detailed Steps, Validation, Rollback, Results, Metadata
- Detail level: Comprehensive with commands, expected output, validation, troubleshooting

---

## File Locations

**Task files**: `/srv/cc/Governance/x-poc3-n8n-deployment/p3-tasks/p3.1-prereqs/t-*.md`

**Planning sources**:
- `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-frank-planning-analysis.md`
- `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-william-planning-analysis.md`
- `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-quinn-planning-analysis.md`
- `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md`

**Server location**: hx-n8n-server.hx.dev.local (192.168.10.215)

**Documentation**: `/opt/n8n/docs/`

---

## Notes

1. **SOLID Principles Applied**: Each task has single responsibility
2. **Multi-Agent Coordination**: Three primary agents coordinate across 19 tasks
3. **Parallel Execution**: Multiple parallel tracks reduce total time from 180min to ~90min
4. **Comprehensive Detail**: Each task includes commands, expected output, validation, troubleshooting
5. **Rollback Procedures**: Every task includes rollback steps
6. **Security First**: SSL certificates, firewall rules, secure credentials established upfront
7. **Validation Gates**: Each category has validation tasks to ensure quality
8. **Documentation**: Each step generates documentation for audit trail

---

**Created**: 2025-11-07
**Agents**: @agent-frank, @agent-william, @agent-quinn
**Status**: ✅ All 19 task files created and ready for execution
**Next Action**: Begin execution with parallel tracks (T-001 + T-004) after coordination meeting
