# Agent William Taylor - POC3 N8N Deployment Planning Analysis

**Document Type**: Agent Planning Analysis
**Created**: 2025-11-07
**Agent**: William Taylor (@agent-william)
**Role**: Ubuntu Systems Administrator
**Project**: POC3 N8N Workflow Automation Deployment
**Phase**: Phase 2 - Collaborative Planning
**Classification**: Internal - Project Documentation

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Agent Responsibilities](#agent-responsibilities)
3. [Detailed Task Breakdown](#detailed-task-breakdown)
4. [Deliverables](#deliverables)
5. [Dependencies](#dependencies)
6. [Timeline & Effort Estimation](#timeline--effort-estimation)
7. [Validation Criteria](#validation-criteria)
8. [Risk Assessment](#risk-assessment)
9. [Handoff Protocols](#handoff-protocols)
10. [Sign-off Criteria](#sign-off-criteria)

---

## 1. Executive Summary

### 1.1 Role Summary

As Agent William Taylor, Ubuntu Systems Administrator, I am responsible for **preparing the operating system foundation** for the n8n deployment on hx-n8n-server (192.168.10.215). My work establishes the secure, performant, and reliable platform upon which @agent-omar will deploy the n8n application.

### 1.2 Critical Scope

**In Scope**:
- Ubuntu 22.04/24.04 LTS server provisioning and hardening
- Node.js 22.x LTS installation (≥22.16.0, ≤24.x)
- pnpm 10.18.3 installation via corepack
- System dependencies (build-essential, python3, cairo, pango, etc.)
- User/group creation for n8n service (dedicated service account)
- Directory structure creation (/opt/n8n/, /var/log/n8n/, /srv/n8n/)
- Firewall configuration (ufw - port 5678 internal access)
- Nginx installation and base configuration (reverse proxy with SSL termination)
- System performance tuning (sysctl, ulimit, resource limits)
- Systemd service unit template creation

**Out of Scope** (Other Agents):
- DNS record creation → @agent-frank (FreeIPA Identity & Trust)
- SSL/TLS certificate generation → @agent-frank
- Domain service account creation → @agent-frank
- PostgreSQL database creation → @agent-quinn
- Redis configuration → @agent-samuel
- N8N application deployment → @agent-omar
- N8N configuration → @agent-omar

### 1.3 Key Success Criteria

- ✅ Server ready for n8n deployment with all system prerequisites met
- ✅ Node.js 22.16+ and pnpm 10.18.3 verified operational
- ✅ System dependencies installed and tested
- ✅ Service user and directory structure properly configured (permissions verified)
- ✅ Nginx reverse proxy configured with SSL termination ready
- ✅ Firewall rules configured (internal access only to port 5678)
- ✅ System performance tuned for Node.js workloads
- ✅ Documentation complete with validation evidence

---

## 2. Agent Responsibilities

### 2.1 Primary Responsibilities for POC3

As the Ubuntu Systems owner, my responsibilities for this deployment are:

#### 2.1.1 Operating System Configuration
- **Server verification**: Confirm hx-n8n-server (192.168.10.215) is accessible and running Ubuntu 22.04 or 24.04 LTS
- **System updates**: Apply all security patches and system updates
- **Kernel tuning**: Configure sysctl parameters for Node.js performance
- **Resource limits**: Set ulimit and systemd resource limits

#### 2.1.2 Node.js Runtime Environment
- **Version requirement**: Node.js ≥22.16.0, ≤24.x (n8n requirement per technical analysis)
- **Installation method**: Official NodeSource repository (recommended) or nvm for version management
- **Verification**: Validate Node.js version and npm functionality
- **PATH configuration**: Ensure node/npm binaries accessible system-wide

#### 2.1.3 Package Manager Installation
- **pnpm requirement**: Exactly version 10.18.3 (n8n requirement)
- **Installation method**: Node.js corepack (recommended approach)
- **Verification**: Validate pnpm version and functionality
- **Configuration**: Enable corepack, prepare pnpm version

#### 2.1.4 System Dependencies
Per n8n technical analysis (Section 4.4), install required packages:

**Build Tools**:
- build-essential (gcc, g++, make)
- python3 (for node-gyp)
- python3-pip
- git
- curl
- ca-certificates

**Graphics Libraries** (for canvas/image processing):
- libcairo2-dev
- libpango1.0-dev
- libjpeg-dev
- libgif-dev
- librsvg2-dev

**PostgreSQL Client** (for database connectivity testing):
- postgresql-client-15 (or 16 for Ubuntu 24.04)

**Optional but Recommended**:
- nginx (reverse proxy)
- logrotate (log management)

#### 2.1.5 User & Group Management
- **Service user**: Create dedicated `n8n` user (non-login, system account)
- **Home directory**: `/opt/n8n` (application base)
- **Group**: Create `n8n` group
- **Shell**: `/usr/sbin/nologin` (security best practice)
- **Ownership**: Assign proper ownership to application directories

#### 2.1.6 Directory Structure
Create and configure:

```
/opt/n8n/                  # Application base directory
├── .n8n/                  # N8N data directory
│   ├── .encryption-key    # (Created by n8n on first start)
│   ├── config/            # Custom configuration files
│   ├── nodes/             # Custom community nodes
│   └── static/            # Static assets (uploaded files)
├── app/                   # Application code (from @agent-omar)
│   └── bin/n8n            # N8N executable
└── .env                   # Environment configuration (from @agent-omar)

/var/log/n8n/              # Log directory
└── n8n.log                # Application logs

/srv/n8n/                  # Additional data storage (optional)
└── backups/               # Backup storage
```

**Permissions**:
- `/opt/n8n/`: `0755` (owner: n8n:n8n)
- `/opt/n8n/.n8n/`: `0700` (owner: n8n:n8n) - **CRITICAL for encryption key security**
- `/var/log/n8n/`: `0755` (owner: n8n:n8n)
- `/srv/n8n/`: `0755` (owner: n8n:n8n)

#### 2.1.7 Firewall Configuration
- **Tool**: ufw (Uncomplicated Firewall)
- **Port 5678**: Internal access only (localhost + internal network)
- **Port 80/443**: Nginx reverse proxy (external access)
- **SSH**: Maintain existing SSH access rules

**Firewall Rules**:
```bash
# Allow SSH (maintain existing)
sudo ufw allow 22/tcp

# Allow Nginx (HTTP/HTTPS)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Port 5678: ONLY allow localhost + internal network
sudo ufw allow from 192.168.10.0/24 to any port 5678 proto tcp comment 'N8N internal access'
sudo ufw deny 5678/tcp comment 'N8N external deny'

# Enable firewall
sudo ufw enable
```

#### 2.1.8 Nginx Installation & Base Configuration
- **Installation**: Install nginx from Ubuntu repositories
- **Configuration**: Create base reverse proxy configuration
- **SSL Termination**: Configure for SSL (certificate from @agent-frank)
- **WebSocket Support**: Enable WebSocket upgrades (required for n8n editor)
- **Security Headers**: Add recommended security headers
- **Logging**: Configure access/error logs

**Base Nginx Configuration Template** (to be finalized with @agent-frank's SSL cert):

```nginx
# /etc/nginx/sites-available/n8n
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name n8n.hx.dev.local;  # DNS from @agent-frank

    # SSL Configuration (certificate paths from @agent-frank)
    ssl_certificate /etc/ssl/certs/n8n.hx.dev.local.crt;
    ssl_certificate_key /etc/ssl/private/n8n.hx.dev.local.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Logging
    access_log /var/log/nginx/n8n-access.log;
    error_log /var/log/nginx/n8n-error.log;

    # Client upload limits (for workflow files)
    client_max_body_size 200M;

    # Proxy to n8n backend
    location / {
        proxy_pass http://127.0.0.1:5678;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Port $server_port;

        # Timeouts for long-running workflows
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;

        # Buffering
        proxy_buffering off;
        proxy_request_buffering off;
    }

    # WebSocket support for push notifications
    location /push {
        proxy_pass http://127.0.0.1:5678/push;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name n8n.hx.dev.local;

    return 301 https://$server_name$request_uri;
}
```

#### 2.1.9 System Performance Tuning

**Sysctl Parameters** (`/etc/sysctl.d/99-n8n.conf`):
```bash
# Increase file descriptor limits for Node.js
fs.file-max = 2097152

# TCP tuning for API server
net.core.somaxconn = 4096
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 600

# Memory management
vm.swappiness = 10
```

**Systemd Resource Limits** (in service unit):
```ini
[Service]
# File descriptor limits
LimitNOFILE=65536
LimitNPROC=4096

# Memory limits (if needed)
# MemoryMax=4G

# CPU limits (if needed)
# CPUQuota=200%
```

**User Limits** (`/etc/security/limits.d/n8n.conf`):
```
n8n soft nofile 65536
n8n hard nofile 65536
n8n soft nproc 4096
n8n hard nproc 4096
```

#### 2.1.10 Systemd Service Template

Create base systemd service unit template (final configuration by @agent-omar):

```ini
# /etc/systemd/system/n8n.service
[Unit]
Description=n8n Workflow Automation Platform
Documentation=https://docs.n8n.io
After=network.target postgresql.service
Wants=postgresql.service

[Service]
Type=simple
User=n8n
Group=n8n
WorkingDirectory=/opt/n8n
EnvironmentFile=/opt/n8n/.env
ExecStart=/usr/bin/node /opt/n8n/app/bin/n8n start
ExecReload=/bin/kill -HUP $MAINPID
KillMode=mixed
KillSignal=SIGTERM
TimeoutStopSec=30
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=n8n

# Security hardening
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/n8n/.n8n /var/log/n8n

# Resource limits
LimitNOFILE=65536
LimitNPROC=4096

[Install]
WantedBy=multi-user.target
```

**Note**: Service will not be started/enabled by me. @agent-omar will validate and start the service after deploying the application.

---

## 3. Detailed Task Breakdown

### 3.1 Task List (Organized by Execution Phase)

#### PHASE 1: System Verification & Preparation (Parallel with Infrastructure)

**Task 1.1: Server Accessibility & OS Verification**
- **Description**: Verify SSH access to hx-n8n-server (192.168.10.215) and confirm Ubuntu version
- **Commands**:
  ```bash
  ssh hx-n8n-server.hx.dev.local
  lsb_release -a  # Verify Ubuntu 22.04 or 24.04 LTS
  uname -a        # Verify kernel version
  df -h           # Check disk space (minimum 20GB free)
  free -h         # Check RAM (minimum 4GB)
  nproc           # Check CPU cores
  ```
- **Success Criteria**: SSH access confirmed, Ubuntu 22.04/24.04 LTS verified, sufficient resources available
- **Duration**: 15 minutes
- **Blocking**: None (can start immediately)
- **Parallel**: Can run parallel with @agent-frank DNS/certificate work

**Task 1.2: System Updates & Security Patches**
- **Description**: Apply all available security patches and system updates
- **Commands**:
  ```bash
  sudo apt update
  sudo apt upgrade -y
  sudo apt autoremove -y
  sudo apt autoclean
  ```
- **Success Criteria**: All packages updated, no errors reported
- **Duration**: 30 minutes (depends on number of updates)
- **Blocking**: Task 1.1 (server access required)
- **Parallel**: Can run parallel with @agent-frank work

#### PHASE 2: System Dependencies Installation (Parallel Execution)

**Task 2.1: Install Build Tools & Core Dependencies**
- **Description**: Install compiler toolchain and core system dependencies
- **Commands**:
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
- **Success Criteria**: All packages installed without errors, version checks pass
- **Duration**: 20 minutes
- **Blocking**: Task 1.2 (system updates complete)
- **Parallel**: Can run in parallel with Task 2.2

**Task 2.2: Install Graphics Libraries**
- **Description**: Install Cairo, Pango, and image processing libraries (required for n8n canvas operations)
- **Commands**:
  ```bash
  sudo apt install -y \
    libcairo2-dev \
    libpango1.0-dev \
    libjpeg-dev \
    libgif-dev \
    librsvg2-dev \
    libpixman-1-dev

  # Verify installations
  pkg-config --modversion cairo
  pkg-config --modversion pango
  ```
- **Success Criteria**: All graphics libraries installed and pkg-config can locate them
- **Duration**: 15 minutes
- **Blocking**: Task 1.2 (system updates complete)
- **Parallel**: Can run in parallel with Task 2.1

**Task 2.3: Install PostgreSQL Client**
- **Description**: Install PostgreSQL client tools for database connectivity testing
- **Commands**:
  ```bash
  # Ubuntu 22.04
  sudo apt install -y postgresql-client-15

  # Ubuntu 24.04
  sudo apt install -y postgresql-client-16

  # Verify installation
  psql --version
  ```
- **Success Criteria**: PostgreSQL client installed and version confirmed
- **Duration**: 10 minutes
- **Blocking**: Task 1.2 (system updates complete)
- **Parallel**: Can run in parallel with Tasks 2.1, 2.2

**Task 2.4: Install Nginx**
- **Description**: Install Nginx web server for reverse proxy
- **Commands**:
  ```bash
  sudo apt install -y nginx

  # Verify installation
  nginx -v

  # Stop nginx (will configure later)
  sudo systemctl stop nginx
  ```
- **Success Criteria**: Nginx installed successfully
- **Duration**: 10 minutes
- **Blocking**: Task 1.2 (system updates complete)
- **Parallel**: Can run in parallel with other Task 2.x tasks

#### PHASE 3: Node.js & pnpm Installation (Sequential)

**Task 3.1: Install Node.js 22.x LTS**
- **Description**: Install Node.js version ≥22.16.0 using NodeSource repository
- **Commands**:
  ```bash
  # Add NodeSource repository for Node.js 22.x
  curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -

  # Install Node.js
  sudo apt install -y nodejs

  # Verify installation
  node --version   # Should be ≥22.16.0
  npm --version    # Should be installed with Node.js

  # Verify Node.js works
  node -e "console.log('Node.js installed successfully')"
  ```
- **Success Criteria**: Node.js ≥22.16.0 installed, npm functional, test script executes
- **Duration**: 20 minutes
- **Blocking**: Tasks 2.1-2.4 (all system dependencies installed)
- **Parallel**: No (must complete before Task 3.2)

**Task 3.2: Install pnpm 10.18.3 via Corepack**
- **Description**: Install pnpm package manager using Node.js corepack
- **Commands**:
  ```bash
  # Enable corepack
  sudo corepack enable

  # Prepare pnpm 10.18.3
  sudo corepack prepare pnpm@10.18.3 --activate

  # Verify pnpm installation
  pnpm --version   # Should output: 10.18.3

  # Test pnpm functionality
  pnpm --help
  ```
- **Success Criteria**: pnpm version 10.18.3 installed and functional
- **Duration**: 10 minutes
- **Blocking**: Task 3.1 (Node.js must be installed first)
- **Parallel**: No (sequential after Task 3.1)

#### PHASE 4: User & Directory Structure (Sequential)

**Task 4.1: Create n8n Service User**
- **Description**: Create dedicated system user for n8n service
- **Commands**:
  ```bash
  # Create system user with no login shell
  sudo useradd -r -m -s /usr/sbin/nologin -d /opt/n8n -U n8n

  # Verify user creation
  id n8n
  grep n8n /etc/passwd
  grep n8n /etc/group

  # Verify home directory
  ls -ld /opt/n8n
  ```
- **Success Criteria**: User `n8n` created, group `n8n` exists, home directory `/opt/n8n` exists with correct ownership
- **Duration**: 10 minutes
- **Blocking**: Tasks 2.x, 3.x complete (system ready)
- **Parallel**: Can run in parallel with Task 4.2

**Task 4.2: Create Directory Structure**
- **Description**: Create all required directories for n8n application
- **Commands**:
  ```bash
  # Create application directories
  sudo mkdir -p /opt/n8n/{.n8n,app,backups}
  sudo mkdir -p /opt/n8n/.n8n/{config,nodes,static}

  # Create log directory
  sudo mkdir -p /var/log/n8n

  # Create backup directory
  sudo mkdir -p /srv/n8n/backups

  # Set ownership
  sudo chown -R n8n:n8n /opt/n8n
  sudo chown -R n8n:n8n /var/log/n8n
  sudo chown -R n8n:n8n /srv/n8n

  # Set permissions
  sudo chmod 755 /opt/n8n
  sudo chmod 700 /opt/n8n/.n8n       # CRITICAL: Encryption key security
  sudo chmod 755 /opt/n8n/.n8n/config
  sudo chmod 755 /opt/n8n/.n8n/nodes
  sudo chmod 755 /opt/n8n/.n8n/static
  sudo chmod 755 /var/log/n8n
  sudo chmod 755 /srv/n8n

  # Verify directory structure
  tree -L 3 -p /opt/n8n
  ls -la /var/log/n8n
  ls -la /srv/n8n
  ```
- **Success Criteria**: All directories created with correct permissions and ownership
- **Duration**: 15 minutes
- **Blocking**: Task 4.1 (user must exist)
- **Parallel**: No (depends on Task 4.1)

#### PHASE 5: System Configuration (Parallel Execution)

**Task 5.1: Configure Firewall Rules**
- **Description**: Configure ufw firewall with required rules for n8n
- **Commands**:
  ```bash
  # Ensure ufw is installed
  sudo apt install -y ufw

  # Configure rules
  sudo ufw default deny incoming
  sudo ufw default allow outgoing

  # Allow SSH (maintain access)
  sudo ufw allow 22/tcp comment 'SSH'

  # Allow HTTP/HTTPS for Nginx
  sudo ufw allow 80/tcp comment 'HTTP'
  sudo ufw allow 443/tcp comment 'HTTPS'

  # Port 5678: Internal network only
  sudo ufw allow from 192.168.10.0/24 to any port 5678 proto tcp comment 'N8N internal'
  sudo ufw deny 5678/tcp comment 'N8N external deny'

  # Enable firewall
  sudo ufw --force enable

  # Verify rules
  sudo ufw status numbered
  ```
- **Success Criteria**: Firewall enabled, all rules configured correctly, SSH access maintained
- **Duration**: 15 minutes
- **Blocking**: Tasks 4.x complete
- **Parallel**: Can run in parallel with Tasks 5.2, 5.3

**Task 5.2: Configure System Performance Tuning**
- **Description**: Apply sysctl and ulimit tuning for Node.js performance
- **Commands**:
  ```bash
  # Create sysctl configuration
  sudo tee /etc/sysctl.d/99-n8n.conf <<'EOF'
  # N8N Performance Tuning

  # File descriptor limits
  fs.file-max = 2097152

  # TCP tuning
  net.core.somaxconn = 4096
  net.ipv4.tcp_max_syn_backlog = 8192
  net.ipv4.tcp_fin_timeout = 30
  net.ipv4.tcp_keepalive_time = 600

  # Memory management
  vm.swappiness = 10
  EOF

  # Apply sysctl settings
  sudo sysctl -p /etc/sysctl.d/99-n8n.conf

  # Create user limits configuration
  sudo tee /etc/security/limits.d/n8n.conf <<'EOF'
  n8n soft nofile 65536
  n8n hard nofile 65536
  n8n soft nproc 4096
  n8n hard nproc 4096
  EOF

  # Verify sysctl settings
  sudo sysctl fs.file-max
  sudo sysctl net.core.somaxconn
  ```
- **Success Criteria**: All tuning parameters applied and verified
- **Duration**: 10 minutes
- **Blocking**: Tasks 4.x complete
- **Parallel**: Can run in parallel with Tasks 5.1, 5.3

**Task 5.3: Create Systemd Service Template**
- **Description**: Create base systemd service unit for n8n
- **Commands**:
  ```bash
  sudo tee /etc/systemd/system/n8n.service <<'EOF'
  [Unit]
  Description=n8n Workflow Automation Platform
  Documentation=https://docs.n8n.io
  After=network.target postgresql.service
  Wants=postgresql.service

  [Service]
  Type=simple
  User=n8n
  Group=n8n
  WorkingDirectory=/opt/n8n
  EnvironmentFile=/opt/n8n/.env
  ExecStart=/usr/bin/node /opt/n8n/app/bin/n8n start
  ExecReload=/bin/kill -HUP $MAINPID
  KillMode=mixed
  KillSignal=SIGTERM
  TimeoutStopSec=30
  Restart=on-failure
  RestartSec=10
  StandardOutput=journal
  StandardError=journal
  SyslogIdentifier=n8n

  # Security hardening
  NoNewPrivileges=true
  PrivateTmp=true
  ProtectSystem=strict
  ProtectHome=true
  ReadWritePaths=/opt/n8n/.n8n /var/log/n8n

  # Resource limits
  LimitNOFILE=65536
  LimitNPROC=4096

  [Install]
  WantedBy=multi-user.target
  EOF

  # Reload systemd
  sudo systemctl daemon-reload

  # Verify service file syntax
  sudo systemd-analyze verify n8n.service
  ```
- **Success Criteria**: Service file created, systemd reloaded, no syntax errors
- **Duration**: 10 minutes
- **Blocking**: Task 4.1 (user must exist)
- **Parallel**: Can run in parallel with Tasks 5.1, 5.2

#### PHASE 6: Nginx Configuration (Sequential - Requires @agent-frank SSL)

**Task 6.1: Create Base Nginx Configuration**
- **Description**: Create nginx reverse proxy configuration (SSL paths to be updated by @agent-frank)
- **Commands**:
  ```bash
  sudo tee /etc/nginx/sites-available/n8n <<'EOF'
  server {
      listen 443 ssl http2;
      listen [::]:443 ssl http2;
      server_name n8n.hx.dev.local;

      # SSL Configuration (PLACEHOLDER - will be updated by @agent-frank)
      ssl_certificate /etc/ssl/certs/n8n.hx.dev.local.crt;
      ssl_certificate_key /etc/ssl/private/n8n.hx.dev.local.key;
      ssl_protocols TLSv1.2 TLSv1.3;
      ssl_ciphers HIGH:!aNULL:!MD5;
      ssl_prefer_server_ciphers on;

      # Security Headers
      add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
      add_header X-Frame-Options "SAMEORIGIN" always;
      add_header X-Content-Type-Options "nosniff" always;
      add_header X-XSS-Protection "1; mode=block" always;

      # Logging
      access_log /var/log/nginx/n8n-access.log;
      error_log /var/log/nginx/n8n-error.log;

      # Client upload limits
      client_max_body_size 200M;

      # Proxy to n8n backend
      location / {
          proxy_pass http://127.0.0.1:5678;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_set_header X-Forwarded-Host $host;
          proxy_set_header X-Forwarded-Port $server_port;

          # Timeouts for long-running workflows
          proxy_connect_timeout 300s;
          proxy_send_timeout 300s;
          proxy_read_timeout 300s;

          # Buffering
          proxy_buffering off;
          proxy_request_buffering off;
      }

      # WebSocket support for push notifications
      location /push {
          proxy_pass http://127.0.0.1:5678/push;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }
  }

  # Redirect HTTP to HTTPS
  server {
      listen 80;
      listen [::]:80;
      server_name n8n.hx.dev.local;

      return 301 https://$server_name$request_uri;
  }
  EOF

  # Test nginx configuration (will fail without SSL cert - expected)
  sudo nginx -t || echo "Expected failure - SSL cert not installed yet"

  # Do NOT enable site or start nginx yet (waiting for @agent-frank SSL cert)
  ```
- **Success Criteria**: Nginx configuration file created, syntax valid (except SSL cert missing)
- **Duration**: 15 minutes
- **Blocking**: Task 5.x complete, @agent-frank SSL certificate delivered
- **Parallel**: No (must wait for @agent-frank SSL cert)

**Task 6.2: Enable Nginx Site & Start Service** *(Coordinated with @agent-frank)*
- **Description**: Enable n8n site and start nginx (after SSL cert installed by @agent-frank)
- **Commands**:
  ```bash
  # Create symlink to enable site
  sudo ln -s /etc/nginx/sites-available/n8n /etc/nginx/sites-enabled/

  # Test nginx configuration (should pass now with SSL cert)
  sudo nginx -t

  # Start nginx
  sudo systemctl start nginx
  sudo systemctl enable nginx

  # Verify nginx status
  sudo systemctl status nginx

  # Test HTTPS redirect
  curl -I http://n8n.hx.dev.local  # Should return 301 redirect
  ```
- **Success Criteria**: Nginx running, configuration test passes, HTTPS redirect functional
- **Duration**: 10 minutes
- **Blocking**: Task 6.1 complete, @agent-frank SSL cert installed
- **Parallel**: No (sequential after SSL cert installation)

#### PHASE 7: Validation & Documentation (Sequential)

**Task 7.1: System Validation Tests**
- **Description**: Comprehensive validation of all system components
- **Commands**:
  ```bash
  # Create validation script
  tee /opt/n8n/validate-system.sh <<'EOF'
  #!/bin/bash
  echo "=== N8N System Validation ==="

  # Node.js version
  echo -n "Node.js version: "
  node --version

  # pnpm version
  echo -n "pnpm version: "
  pnpm --version

  # Service user
  echo -n "Service user exists: "
  id n8n && echo "OK" || echo "FAIL"

  # Directory structure
  echo "Directory structure:"
  ls -la /opt/n8n
  ls -la /var/log/n8n

  # Permissions check
  echo -n "/opt/n8n/.n8n permissions: "
  stat -c "%a" /opt/n8n/.n8n

  # Firewall rules
  echo "Firewall rules:"
  sudo ufw status numbered | grep -E "(5678|80|443)"

  # Sysctl settings
  echo "Sysctl settings:"
  sudo sysctl fs.file-max
  sudo sysctl net.core.somaxconn

  # Nginx status
  echo -n "Nginx status: "
  systemctl is-active nginx

  # Test database connectivity (if @agent-quinn provides credentials)
  if [ ! -z "$DB_PASSWORD" ]; then
    echo "Testing PostgreSQL connectivity:"
    PGPASSWORD=$DB_PASSWORD psql -h hx-postgres-server.hx.dev.local \
      -U n8n_user -d n8n_poc3 -c "SELECT 1" 2>&1 | head -1
  fi

  echo "=== Validation Complete ==="
  EOF

  chmod +x /opt/n8n/validate-system.sh

  # Run validation
  /opt/n8n/validate-system.sh
  ```
- **Success Criteria**: All validation checks pass
- **Duration**: 20 minutes
- **Blocking**: All previous tasks complete
- **Parallel**: No (final validation)

**Task 7.2: Create System Documentation**
- **Description**: Document all configuration for handoff to operations and @agent-omar
- **Commands**:
  ```bash
  tee /opt/n8n/SYSTEM_CONFIGURATION.md <<'EOF'
  # N8N System Configuration

  **Server**: hx-n8n-server.hx.dev.local (192.168.10.215)
  **Configured By**: @agent-william (William Taylor)
  **Date**: $(date +%Y-%m-%d)
  **Purpose**: POC3 N8N Workflow Automation Platform

  ## Software Versions

  - **Ubuntu**: $(lsb_release -ds)
  - **Kernel**: $(uname -r)
  - **Node.js**: $(node --version)
  - **npm**: $(npm --version)
  - **pnpm**: $(pnpm --version)
  - **Nginx**: $(nginx -v 2>&1)
  - **PostgreSQL Client**: $(psql --version)

  ## Service User

  - **Username**: n8n
  - **UID**: $(id -u n8n)
  - **GID**: $(id -g n8n)
  - **Home Directory**: /opt/n8n
  - **Shell**: /usr/sbin/nologin

  ## Directory Structure

  \`\`\`
  $(tree -L 2 /opt/n8n)
  \`\`\`

  ## Firewall Rules

  \`\`\`
  $(sudo ufw status numbered)
  \`\`\`

  ## System Tuning

  - **Sysctl Config**: /etc/sysctl.d/99-n8n.conf
  - **User Limits**: /etc/security/limits.d/n8n.conf

  ## Nginx Configuration

  - **Config File**: /etc/nginx/sites-available/n8n
  - **Enabled**: /etc/nginx/sites-enabled/n8n
  - **Access Log**: /var/log/nginx/n8n-access.log
  - **Error Log**: /var/log/nginx/n8n-error.log

  ## Systemd Service

  - **Service File**: /etc/systemd/system/n8n.service
  - **Status**: $(systemctl is-active n8n) (not started yet - waiting for @agent-omar)

  ## Next Steps (For @agent-omar)

  1. Deploy n8n application code to /opt/n8n/app/
  2. Create .env file with configuration
  3. Test application deployment
  4. Start n8n service: sudo systemctl start n8n
  5. Enable on boot: sudo systemctl enable n8n
  6. Verify logs: sudo journalctl -u n8n -f

  ## Validation Script

  Run validation: /opt/n8n/validate-system.sh
  EOF
  ```
- **Success Criteria**: Documentation complete and readable
- **Duration**: 30 minutes
- **Blocking**: Task 7.1 (validation complete)
- **Parallel**: No (final documentation)

---

## 4. Deliverables

### 4.1 Primary Deliverables

Upon completion of all tasks, I will deliver:

#### 4.1.1 Fully Configured Server
- **Description**: hx-n8n-server ready for n8n application deployment
- **Validation**: All system validation checks pass
- **Location**: hx-n8n-server.hx.dev.local (192.168.10.215)

#### 4.1.2 Software Installation Documentation
- **Description**: Complete record of installed versions
- **File**: `/opt/n8n/SYSTEM_CONFIGURATION.md`
- **Contents**:
  - Ubuntu version and kernel
  - Node.js version (≥22.16.0)
  - pnpm version (10.18.3)
  - All installed system dependencies with versions
  - Service user details (UID, GID, home directory)
  - Directory structure with permissions
  - Firewall rules
  - System tuning parameters

#### 4.1.3 Validation Script
- **Description**: Automated script to verify system configuration
- **File**: `/opt/n8n/validate-system.sh`
- **Purpose**: Quick health check for operations team and troubleshooting

#### 4.1.4 Nginx Configuration
- **Description**: Reverse proxy configuration ready for SSL cert
- **Files**:
  - `/etc/nginx/sites-available/n8n`
  - `/etc/nginx/sites-enabled/n8n` (symlink)
- **Status**: Configured but waiting for @agent-frank SSL certificate

#### 4.1.5 Systemd Service Unit
- **Description**: Service configuration template for n8n
- **File**: `/etc/systemd/system/n8n.service`
- **Status**: Created but not enabled/started (waiting for @agent-omar application deployment)

#### 4.1.6 Directory Structure
- **Description**: Complete directory tree with proper ownership/permissions
- **Locations**:
  - `/opt/n8n/` - Application base (owner: n8n:n8n, mode: 0755)
  - `/opt/n8n/.n8n/` - Data directory (owner: n8n:n8n, mode: 0700)
  - `/var/log/n8n/` - Log directory (owner: n8n:n8n, mode: 0755)
  - `/srv/n8n/backups/` - Backup storage (owner: n8n:n8n, mode: 0755)

### 4.2 Handoff Package for @agent-omar

I will provide @agent-omar with:

1. **Server Access**:
   - SSH access to hx-n8n-server.hx.dev.local
   - Service user `n8n` configured (for application ownership)

2. **Deployment Paths**:
   - Application directory: `/opt/n8n/app/`
   - Configuration file: `/opt/n8n/.env`
   - Data directory: `/opt/n8n/.n8n/`
   - Log directory: `/var/log/n8n/`

3. **Service Management**:
   - Systemd service unit: `/etc/systemd/system/n8n.service`
   - Start command: `sudo systemctl start n8n`
   - Enable on boot: `sudo systemctl enable n8n`
   - Check logs: `sudo journalctl -u n8n -f`

4. **Validation**:
   - System validation script: `/opt/n8n/validate-system.sh`
   - Node.js verification: `node --version` (should show ≥22.16.0)
   - pnpm verification: `pnpm --version` (should show 10.18.3)

5. **Network Access**:
   - Internal application port: 5678 (accessible from 192.168.10.0/24)
   - External HTTPS: https://n8n.hx.dev.local (via Nginx proxy)
   - WebSocket support: Configured in Nginx

6. **Documentation**:
   - System configuration: `/opt/n8n/SYSTEM_CONFIGURATION.md`
   - Directory structure diagram
   - Firewall rules reference
   - System tuning parameters

### 4.3 Coordination Artifacts

**For @agent-frank**:
- DNS record request: `n8n.hx.dev.local → 192.168.10.215`
- SSL certificate request: Subject CN=n8n.hx.dev.local
- Certificate installation path: `/etc/ssl/certs/n8n.hx.dev.local.crt`, `/etc/ssl/private/n8n.hx.dev.local.key`
- Nginx configuration ready for certificate paths

**For @agent-quinn**:
- PostgreSQL client installed for connectivity testing
- Database connection test command documented
- Expecting database credentials for validation

**For @agent-julia**:
- System validation script available for testing
- Test plan for OS-level verification
- Validation criteria documented

---

## 5. Dependencies

### 5.1 Upstream Dependencies (What I Need from Others)

#### 5.1.1 From @agent-frank (FreeIPA Identity & Trust) - CRITICAL

**Blocking Tasks**: Task 6.2 (Enable Nginx & Start Service)

**Required Deliverables**:

1. **DNS Record**:
   - **Record**: A record for `n8n.hx.dev.local` → `192.168.10.215`
   - **Purpose**: Hostname resolution for n8n service
   - **Urgency**: Required before Nginx can be fully tested
   - **Validation**: `nslookup n8n.hx.dev.local` should return 192.168.10.215

2. **SSL/TLS Certificate**:
   - **Certificate Type**: Samba AD CA signed certificate
   - **Subject**: CN=n8n.hx.dev.local
   - **Files Needed**:
     - Certificate: `/etc/ssl/certs/n8n.hx.dev.local.crt`
     - Private Key: `/etc/ssl/private/n8n.hx.dev.local.key`
     - CA Certificate: `/etc/ssl/certs/ca.crt` (for client trust)
   - **Purpose**: SSL/TLS termination in Nginx
   - **Urgency**: BLOCKING for Nginx startup
   - **Validation**: `openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -text -noout`

3. **Certificate Installation** (Optional - can do myself if Frank provides files):
   - If @agent-frank delivers certificate files, I can install them
   - Preferred: Frank installs certificates directly (his expertise)
   - Fallback: Frank provides files, I install per his instructions

**Coordination Protocol**:
```
@agent-frank

I need DNS and SSL certificate for n8n deployment.

Current Status:
- Task: Nginx reverse proxy configuration
- Progress: Base configuration complete
- Blocker: Cannot enable Nginx without SSL certificate

Request:
- Action 1: Create DNS A record n8n.hx.dev.local → 192.168.10.215
- Action 2: Generate SSL certificate for n8n.hx.dev.local
- Action 3: Install certificate to /etc/ssl/certs/ and /etc/ssl/private/
- Scope: Samba AD CA signed certificate

Context:
- Service: N8N Workflow Automation
- Server: hx-n8n-server.hx.dev.local (192.168.10.215)
- Purpose: POC3 deployment
- Timeline: Blocking Nginx startup

Success Criteria:
- DNS resolves correctly: nslookup n8n.hx.dev.local
- Certificate installed: /etc/ssl/certs/n8n.hx.dev.local.crt
- Certificate valid: openssl verify check passes
- Nginx configuration test passes: sudo nginx -t

Handoff Back:
- I will: Enable Nginx site and start service
- I need: Certificate paths and CA certificate location
- Verify via: sudo nginx -t && curl -I https://n8n.hx.dev.local
```

#### 5.1.2 From @agent-quinn (PostgreSQL) - NICE-TO-HAVE

**Blocking Tasks**: None (Task 7.1 validation enhanced if available)

**Required Deliverables** (Optional for my work):

1. **Database Credentials** (for connectivity testing):
   - Database: `n8n_poc3`
   - Username: `n8n_user`
   - Password: `<password>`
   - Host: `hx-postgres-server.hx.dev.local`
   - Port: `5432`

**Purpose**: Test PostgreSQL client connectivity during validation (Task 7.1)

**Note**: NOT blocking my work. If credentials available, I can include database connectivity test in validation script. If not, @agent-omar will test database connection during application deployment.

#### 5.1.3 From @agent-omar (N8N Application) - INFORMATION ONLY

**Blocking Tasks**: None (my work enables Omar's work)

**Information Requests** (for optimization):

1. **Resource Requirements**:
   - Expected memory usage?
   - Expected CPU usage?
   - Expected disk I/O patterns?
   - **Purpose**: Helps me tune systemd resource limits if needed

2. **Port Requirements**:
   - Confirm port 5678 is correct?
   - Any additional ports needed?
   - **Purpose**: Firewall configuration accuracy

3. **Environment Variables**:
   - Any special environment variables needed in systemd unit?
   - Any PATH modifications required?
   - **Purpose**: Systemd service unit optimization

**Note**: These are optional optimizations. I have created baseline configuration based on n8n technical analysis. Omar can request changes if needed.

### 5.2 Downstream Dependencies (Who Needs My Work)

#### 5.2.1 @agent-omar (N8N Application) - PRIMARY CONSUMER

**Omar depends on**:
- Server access (SSH credentials)
- Node.js 22.x LTS installed and functional
- pnpm 10.18.3 installed and functional
- Service user `n8n` created
- Directory structure created with correct permissions
- Systemd service unit template ready
- Nginx reverse proxy configured
- Firewall rules allowing port 5678 internal access

**Handoff Point**: After Task 7.2 (Documentation Complete)

**Omar's Next Steps**:
1. Deploy n8n application code to `/opt/n8n/app/`
2. Create `.env` configuration file
3. Test application deployment
4. Start systemd service
5. Validate application functionality

#### 5.2.2 @agent-julia (Testing & QA) - VALIDATION CONSUMER

**Julia depends on**:
- System validation script
- Validation criteria documentation
- Test plans for OS-level verification

**Handoff Point**: After Task 7.1 (Validation Complete)

**Julia's Validation Steps**:
1. Run system validation script
2. Verify all checks pass
3. Test firewall rules
4. Verify system performance

### 5.3 External Dependencies

#### 5.3.1 Infrastructure Resources

**Server Hardware/VM**:
- **Requirement**: hx-n8n-server (192.168.10.215) accessible via SSH
- **Minimum Specs**:
  - CPU: 4 cores
  - RAM: 8GB (minimum), 16GB (recommended)
  - Disk: 50GB free (minimum), 100GB (recommended)
  - Network: 1Gbps link to internal network
- **Owner**: Infrastructure team (assumed provisioned)
- **Validation**: Task 1.1 (Server Accessibility Check)

#### 5.3.2 Network Infrastructure

**Network Connectivity**:
- **Requirement**: Server has network access to:
  - Internal network: 192.168.10.0/24
  - Internet: For package downloads (Ubuntu repos, NodeSource)
  - DNS: For hostname resolution
- **Owner**: Network team
- **Validation**: Task 1.1 (Network connectivity check)

**DNS Infrastructure**:
- **Requirement**: FreeIPA DNS server operational
- **Owner**: @agent-frank
- **Validation**: DNS record creation and resolution test

---

## 6. Timeline & Effort Estimation

### 6.1 Task Duration Summary

| Phase | Tasks | Duration | Can Run in Parallel? |
|-------|-------|----------|----------------------|
| **Phase 1: System Verification** | 1.1-1.2 | 45 min | Partially (1.1 first, then 1.2) |
| **Phase 2: Dependencies** | 2.1-2.4 | 45 min | YES (all 4 tasks parallel after Phase 1) |
| **Phase 3: Node.js & pnpm** | 3.1-3.2 | 30 min | NO (sequential) |
| **Phase 4: User & Directories** | 4.1-4.2 | 25 min | Partially (4.1 first, then 4.2) |
| **Phase 5: System Configuration** | 5.1-5.3 | 35 min | YES (all 3 tasks parallel) |
| **Phase 6: Nginx** | 6.1-6.2 | 25 min | NO (sequential, blocked by @agent-frank) |
| **Phase 7: Validation & Docs** | 7.1-7.2 | 50 min | NO (sequential) |
| **Total Execution Time** | - | **255 min (4h 15m)** | With parallelization: **~3 hours** |

### 6.2 Detailed Timeline (Optimized for Parallelization)

#### Hour 1: System Prep & Dependencies

**00:00-00:15** - Task 1.1: Server Verification
- Verify SSH access, Ubuntu version, resources
- **Output**: Server confirmed ready

**00:15-00:45** - Task 1.2: System Updates
- Apply all security patches
- **Output**: System fully updated

**00:45-01:30** - Phase 2 Parallel Execution (Tasks 2.1, 2.2, 2.3, 2.4)
- All four tasks run simultaneously:
  - 2.1: Build tools (20 min)
  - 2.2: Graphics libraries (15 min)
  - 2.3: PostgreSQL client (10 min)
  - 2.4: Nginx (10 min)
- **Output**: All system dependencies installed

#### Hour 2: Node.js, User Setup, System Config

**01:30-01:50** - Task 3.1: Node.js Installation
- Install Node.js 22.x from NodeSource
- **Output**: Node.js ≥22.16.0 operational

**01:50-02:00** - Task 3.2: pnpm Installation
- Install pnpm 10.18.3 via corepack
- **Output**: pnpm 10.18.3 operational

**02:00-02:10** - Task 4.1: Create Service User
- Create `n8n` system user
- **Output**: User `n8n` created

**02:10-02:25** - Task 4.2: Create Directory Structure
- Create all application directories
- **Output**: Directory tree ready

**02:25-03:00** - Phase 5 Parallel Execution (Tasks 5.1, 5.2, 5.3)
- All three tasks run simultaneously:
  - 5.1: Firewall configuration (15 min)
  - 5.2: Performance tuning (10 min)
  - 5.3: Systemd service (10 min)
- **Output**: System fully configured

#### Hour 3: Nginx & Validation (Waiting on @agent-frank)

**03:00-03:15** - Task 6.1: Nginx Base Configuration
- Create nginx config file
- **Output**: Nginx config ready (waiting for SSL cert)

**WAIT FOR @agent-frank** - SSL Certificate Delivery
- **Duration**: Variable (depends on Frank's schedule)
- **Estimated**: 1-4 hours
- **Parallel Work**: While waiting, can work on documentation (Task 7.2)

**03:15-03:25** - Task 6.2: Enable Nginx & Start
- Enable site, start nginx
- **Output**: Nginx operational with HTTPS

**03:25-03:45** - Task 7.1: System Validation
- Run comprehensive validation tests
- **Output**: All checks pass

**03:45-04:15** - Task 7.2: Documentation
- Create system configuration documentation
- **Output**: Complete handoff package

### 6.3 Critical Path Analysis

**Critical Path** (cannot be parallelized):
1. Task 1.1: Server Verification (15 min)
2. Task 1.2: System Updates (30 min)
3. Task 3.1: Node.js Installation (20 min) - blocked by Phase 2
4. Task 3.2: pnpm Installation (10 min) - blocked by Task 3.1
5. Task 4.2: Directory Creation (15 min) - blocked by Task 4.1
6. Task 6.2: Nginx Start (10 min) - **BLOCKED by @agent-frank SSL cert**
7. Task 7.1: Validation (20 min) - blocked by all previous tasks
8. Task 7.2: Documentation (30 min) - blocked by Task 7.1

**Total Critical Path**: ~150 minutes (2.5 hours) + @agent-frank SSL cert wait time

### 6.4 Realistic Schedule

**Scenario 1: Fast Track** (@agent-frank delivers SSL cert within 1 hour)
- **Start**: 08:00 AM
- **Phase 1-5 Complete**: 11:00 AM
- **Wait for Frank**: 11:00 AM - 12:00 PM
- **Phase 6-7 Complete**: 1:00 PM
- **Total Duration**: 5 hours (8 AM - 1 PM)

**Scenario 2: Standard Track** (@agent-frank delivers SSL cert within 4 hours)
- **Start**: 08:00 AM
- **Phase 1-5 Complete**: 11:00 AM
- **Wait for Frank**: 11:00 AM - 3:00 PM
- **Phase 6-7 Complete**: 4:00 PM
- **Total Duration**: 8 hours (8 AM - 4 PM)

**Scenario 3: Delayed Track** (SSL cert next day)
- **Day 1**: Complete Phases 1-5, create nginx config (3 hours)
- **Day 2**: Wait for SSL cert, complete Phases 6-7 (1 hour)
- **Total Duration**: 2 days, 4 hours active work

### 6.5 My Availability

**Commitment**: I can begin immediately upon project approval.

**Preferred Schedule**: Scenario 1 or 2 (complete in single day)

**Flexibility**: Can accommodate SSL cert delays by working on documentation while waiting

**Coordination**: Will proactively check with @agent-frank on SSL cert timing to optimize schedule

---

## 7. Validation Criteria

### 7.1 System-Level Validation

Upon completion, the following validation checks must pass:

#### 7.1.1 Operating System Validation

**Check**: Ubuntu version verification
```bash
lsb_release -a | grep -E "(Ubuntu 22.04|Ubuntu 24.04)"
```
**Expected**: Ubuntu 22.04 LTS or 24.04 LTS confirmed

**Check**: System fully updated
```bash
sudo apt update && sudo apt list --upgradable
```
**Expected**: No upgradable packages (or only non-critical packages)

**Check**: Kernel version reasonable
```bash
uname -r
```
**Expected**: Kernel version ≥5.15 (Ubuntu 22.04) or ≥6.8 (Ubuntu 24.04)

#### 7.1.2 Node.js & pnpm Validation

**Check**: Node.js version
```bash
node --version
```
**Expected**: v22.16.0 or higher, ≤v24.x

**Check**: npm functionality
```bash
npm --version && npm list -g --depth=0
```
**Expected**: npm version displayed, global packages listed

**Check**: pnpm version
```bash
pnpm --version
```
**Expected**: 10.18.3 (exact version)

**Check**: pnpm functionality
```bash
pnpm --help
```
**Expected**: pnpm help output displayed

**Check**: Node.js execution test
```bash
node -e "console.log('Node.js OK'); process.exit(0);"
```
**Expected**: "Node.js OK" output, exit code 0

#### 7.1.3 System Dependencies Validation

**Check**: Build tools installed
```bash
gcc --version && g++ --version && make --version
```
**Expected**: All commands return version information

**Check**: Python installed
```bash
python3 --version && pip3 --version
```
**Expected**: Python 3.10+ (Ubuntu 22.04) or 3.12+ (Ubuntu 24.04)

**Check**: Graphics libraries available
```bash
pkg-config --modversion cairo pango
```
**Expected**: Version numbers for both libraries

**Check**: PostgreSQL client installed
```bash
psql --version
```
**Expected**: PostgreSQL client version 15+ (Ubuntu 22.04) or 16+ (Ubuntu 24.04)

**Check**: Git installed
```bash
git --version
```
**Expected**: Git version displayed

#### 7.1.4 User & Permissions Validation

**Check**: Service user exists
```bash
id n8n
```
**Expected**: User `n8n` exists with UID and GID displayed

**Check**: User has no login shell
```bash
grep "^n8n:" /etc/passwd | grep nologin
```
**Expected**: Entry shows `/usr/sbin/nologin` as shell

**Check**: Home directory exists with correct ownership
```bash
ls -ld /opt/n8n
```
**Expected**: `drwxr-xr-x n8n n8n` (755 permissions, n8n:n8n ownership)

**Check**: Data directory has secure permissions
```bash
stat -c "%a %U:%G" /opt/n8n/.n8n
```
**Expected**: `700 n8n:n8n` (highly restrictive for encryption key)

**Check**: Log directory accessible
```bash
ls -ld /var/log/n8n
```
**Expected**: `drwxr-xr-x n8n n8n`

#### 7.1.5 Firewall Validation

**Check**: Firewall enabled
```bash
sudo ufw status
```
**Expected**: Status: active

**Check**: SSH allowed
```bash
sudo ufw status | grep 22/tcp
```
**Expected**: 22/tcp ALLOW

**Check**: HTTP/HTTPS allowed
```bash
sudo ufw status | grep -E "(80|443)/tcp"
```
**Expected**: Both 80/tcp and 443/tcp ALLOW

**Check**: Port 5678 internal access only
```bash
sudo ufw status numbered | grep 5678
```
**Expected**:
- ALLOW from 192.168.10.0/24 to any port 5678
- DENY to any port 5678

**Check**: Firewall test (external access denied)
```bash
# From external IP (not in 192.168.10.0/24)
timeout 5 nc -zv <external-ip> 5678; echo "Exit code: $?"
```
**Expected**: Connection timeout or refused (exit code non-zero)

#### 7.1.6 System Performance Validation

**Check**: Sysctl parameters applied
```bash
sudo sysctl fs.file-max net.core.somaxconn vm.swappiness
```
**Expected**:
- fs.file-max = 2097152
- net.core.somaxconn = 4096
- vm.swappiness = 10

**Check**: User limits configured
```bash
sudo su - n8n -s /bin/bash -c "ulimit -n"
```
**Expected**: 65536 (file descriptor limit)

**Check**: Systemd service unit exists
```bash
systemctl cat n8n.service
```
**Expected**: Service unit file content displayed

**Check**: Systemd service syntax valid
```bash
sudo systemd-analyze verify n8n.service; echo "Exit code: $?"
```
**Expected**: Exit code 0 (no errors)

#### 7.1.7 Nginx Validation

**Check**: Nginx installed
```bash
nginx -v
```
**Expected**: Nginx version displayed

**Check**: Nginx configuration syntax
```bash
sudo nginx -t
```
**Expected**: "syntax is ok", "test is successful"

**Check**: Nginx service active
```bash
systemctl is-active nginx
```
**Expected**: active

**Check**: Nginx site enabled
```bash
ls -la /etc/nginx/sites-enabled/n8n
```
**Expected**: Symlink exists pointing to /etc/nginx/sites-available/n8n

**Check**: HTTPS redirect functional
```bash
curl -I http://n8n.hx.dev.local 2>&1 | grep "301"
```
**Expected**: HTTP 301 redirect to HTTPS

**Check**: SSL certificate valid (after @agent-frank install)
```bash
openssl s_client -connect n8n.hx.dev.local:443 -servername n8n.hx.dev.local < /dev/null 2>&1 | grep "Verify return code"
```
**Expected**: "Verify return code: 0 (ok)"

#### 7.1.8 DNS Validation (requires @agent-frank)

**Check**: DNS record resolves
```bash
nslookup n8n.hx.dev.local
```
**Expected**: Returns 192.168.10.215

**Check**: Reverse DNS (optional)
```bash
nslookup 192.168.10.215
```
**Expected**: Returns n8n.hx.dev.local (optional - depends on PTR record)

### 7.2 Integration Validation (with Other Agents)

#### 7.2.1 Database Connectivity (with @agent-quinn)

**Check**: PostgreSQL reachable (if credentials provided)
```bash
PGPASSWORD=$DB_PASSWORD psql -h hx-postgres-server.hx.dev.local \
  -U n8n_user -d n8n_poc3 -c "SELECT version();"
```
**Expected**: PostgreSQL version information displayed

#### 7.2.2 Application Readiness (for @agent-omar)

**Check**: Application directory ready
```bash
sudo -u n8n touch /opt/n8n/app/test.txt && \
sudo -u n8n rm /opt/n8n/app/test.txt && \
echo "Write test OK"
```
**Expected**: "Write test OK" (user `n8n` can write to app directory)

**Check**: Data directory secure
```bash
sudo -u root ls /opt/n8n/.n8n
```
**Expected**: Permission denied OR only accessible by n8n user

**Check**: Environment file location ready
```bash
sudo -u n8n touch /opt/n8n/.env && \
sudo -u n8n rm /opt/n8n/.env && \
echo "Env file location OK"
```
**Expected**: "Env file location OK"

### 7.3 Automated Validation Script

The validation script `/opt/n8n/validate-system.sh` will perform all checks above and output:

**Success Output**:
```
=== N8N System Validation ===
✅ Node.js version: v22.16.0
✅ pnpm version: 10.18.3
✅ Service user exists: n8n (UID 999)
✅ Directory structure: OK
✅ /opt/n8n/.n8n permissions: 700
✅ Firewall rules: OK (5678 internal only, 80/443 open)
✅ Sysctl settings: OK
✅ Nginx status: active
✅ Nginx configuration: valid
✅ DNS resolution: n8n.hx.dev.local → 192.168.10.215
✅ SSL certificate: valid (expires 2026-11-07)
=== All Validation Checks Passed ===
```

**Failure Example**:
```
=== N8N System Validation ===
✅ Node.js version: v22.16.0
❌ pnpm version: 10.17.0 (expected 10.18.3)
✅ Service user exists: n8n (UID 999)
...
=== Validation Failed: 1 error(s) ===
```

---

## 8. Risk Assessment

### 8.1 Technical Risks

#### Risk 1: Node.js Version Incompatibility

**Description**: Node.js version installed doesn't meet n8n requirements (≥22.16.0, ≤24.x)

**Probability**: Low

**Impact**: High (blocks application deployment)

**Mitigation**:
- Use official NodeSource repository (tested and reliable)
- Verify version immediately after installation (Task 3.1)
- Have fallback plan to use nvm for version management if needed

**Contingency**:
```bash
# If Ubuntu default repo has wrong version:
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
source ~/.bashrc

# Install Node.js 22 LTS
nvm install 22
nvm use 22
nvm alias default 22
```

#### Risk 2: pnpm Installation Failure

**Description**: pnpm 10.18.3 fails to install via corepack

**Probability**: Low

**Impact**: High (blocks application build)

**Mitigation**:
- Use official Node.js corepack (built-in, reliable)
- Test pnpm immediately after installation (Task 3.2)
- Have fallback to npm global install

**Contingency**:
```bash
# If corepack fails:
npm install -g pnpm@10.18.3
pnpm --version  # Verify
```

#### Risk 3: Graphics Library Dependency Conflicts

**Description**: Cairo/Pango libraries have unmet dependencies or version conflicts

**Probability**: Low-Medium

**Impact**: Medium (n8n may work but some features fail)

**Mitigation**:
- Install from official Ubuntu repositories (well-tested)
- Use pkg-config to verify library availability (Task 2.2)
- Document any version discrepancies

**Contingency**:
- Install from Ubuntu backports if needed
- Compile from source as last resort (time-consuming)

#### Risk 4: Firewall Rule Conflicts

**Description**: Existing firewall rules conflict with n8n requirements

**Probability**: Low

**Impact**: Medium (access issues)

**Mitigation**:
- Check existing ufw rules before adding new ones (Task 5.1)
- Use ufw numbered status to verify rule order
- Test connectivity after rule changes

**Contingency**:
- Adjust rule priorities if needed
- Use specific source IP ranges instead of broad rules
- Document any custom rules for operations team

#### Risk 5: Nginx SSL Configuration Issues

**Description**: SSL certificate from @agent-frank has incorrect format or permissions

**Probability**: Low

**Impact**: High (HTTPS doesn't work)

**Mitigation**:
- Verify certificate format with openssl before nginx start (Task 6.2)
- Check file permissions (cert: 644, key: 600)
- Coordinate closely with @agent-frank on certificate delivery

**Contingency**:
```bash
# Verify certificate
openssl x509 -in /etc/ssl/certs/n8n.hx.dev.local.crt -text -noout

# Verify private key
openssl rsa -in /etc/ssl/private/n8n.hx.dev.local.key -check

# Match certificate and key
openssl x509 -noout -modulus -in /etc/ssl/certs/n8n.hx.dev.local.crt | openssl md5
openssl rsa -noout -modulus -in /etc/ssl/private/n8n.hx.dev.local.key | openssl md5
# Hashes should match
```

#### Risk 6: System Resource Constraints

**Description**: Server has insufficient CPU/RAM/Disk for n8n

**Probability**: Low (assuming proper VM provisioning)

**Impact**: High (performance issues or deployment failure)

**Mitigation**:
- Verify resources during initial server check (Task 1.1)
- Document actual resources in SYSTEM_CONFIGURATION.md
- Alert if resources below recommended minimums

**Thresholds**:
- **Minimum**: 4 CPU, 8GB RAM, 50GB disk
- **Recommended**: 8 CPU, 16GB RAM, 100GB disk

**Contingency**:
- Request VM resource increase before proceeding
- Escalate to infrastructure team
- Adjust systemd resource limits if needed

### 8.2 Coordination Risks

#### Risk 7: @agent-frank SSL Certificate Delay

**Description**: SSL certificate delivery delayed, blocking nginx startup

**Probability**: Medium

**Impact**: Medium (delays project timeline but doesn't block my work)

**Mitigation**:
- Proactive communication with @agent-frank on timing (Task 6.1)
- Create nginx config early, ready for certificate (can run in parallel)
- Use wait time for documentation (Task 7.2)

**Contingency**:
- Complete all non-nginx work (Phases 1-5)
- Document system ready for nginx start
- Wait for next day if needed (not a blocker for Omar's early prep work)

#### Risk 8: @agent-omar Application Requirements Change

**Description**: Omar discovers different requirements during deployment

**Probability**: Low-Medium

**Impact**: Low-Medium (may require config adjustments)

**Mitigation**:
- Base configuration on official n8n technical analysis (Section 4)
- Create flexible systemd template (easy to modify)
- Document configuration clearly for easy changes

**Contingency**:
- Adjust systemd service unit as needed
- Modify resource limits if required
- Update firewall rules if additional ports needed

### 8.3 Operational Risks

#### Risk 9: Server Accessibility Issues

**Description**: Cannot SSH to hx-n8n-server due to network/credential issues

**Probability**: Low

**Impact**: Critical (blocks all work)

**Mitigation**:
- Verify SSH access in first task (Task 1.1)
- Escalate immediately if access fails
- Have backup access method (console access)

**Contingency**:
- Work with infrastructure team to resolve access
- Verify server IP and hostname correct
- Check SSH key or password credentials

**Escalation**: Contact infrastructure team immediately if Task 1.1 fails

#### Risk 10: Documentation Incomplete or Unclear

**Description**: Handoff documentation doesn't provide enough detail for @agent-omar

**Probability**: Low

**Impact**: Medium (slows Omar's deployment)

**Mitigation**:
- Use comprehensive documentation template (Task 7.2)
- Include validation script for quick checks
- Provide clear examples and commands
- Review with Omar before final handoff

**Contingency**:
- Schedule handoff call with Omar to walk through config
- Add clarifications as needed
- Be available for questions during Omar's deployment phase

---

## 9. Handoff Protocols

### 9.1 Handoff to @agent-omar (Primary Handoff)

**Timing**: After Task 7.2 (Documentation Complete)

**Handoff Method**: Formal handoff message with all deliverables

**Handoff Message Template**:

```
@agent-omar

Server hx-n8n-server ready for n8n application deployment.

Current Status:
- Task: System configuration complete
- Progress: All 7 phases complete (100%)
- Validation: All system checks passed

Deliverables:
1. Server Access:
   - Hostname: hx-n8n-server.hx.dev.local
   - IP: 192.168.10.215
   - SSH: Use your credentials
   - Service User: n8n (non-login, use sudo)

2. Software Installed:
   - Node.js: v22.16.0 (verified: node --version)
   - pnpm: 10.18.3 (verified: pnpm --version)
   - System Dependencies: build-essential, python3, cairo, pango, etc. (full list in docs)

3. Directory Structure:
   - Application Base: /opt/n8n/ (owner: n8n:n8n, mode: 755)
   - App Deployment: /opt/n8n/app/ (your code goes here)
   - Data Directory: /opt/n8n/.n8n/ (owner: n8n:n8n, mode: 700) **CRITICAL: Encryption key location**
   - Environment File: /opt/n8n/.env (create this with your config)
   - Logs: /var/log/n8n/ (owner: n8n:n8n, mode: 755)

4. Systemd Service:
   - Service File: /etc/systemd/system/n8n.service (template ready)
   - Start Command: sudo systemctl start n8n
   - Enable Boot: sudo systemctl enable n8n
   - View Logs: sudo journalctl -u n8n -f
   - Status Check: sudo systemctl status n8n

5. Network Configuration:
   - Internal Port: 5678 (accessible from 192.168.10.0/24)
   - External Access: https://n8n.hx.dev.local (Nginx reverse proxy)
   - DNS: n8n.hx.dev.local → 192.168.10.215 (configured by @agent-frank)
   - SSL: Installed by @agent-frank, Nginx configured for HTTPS

6. Validation:
   - System Validation Script: /opt/n8n/validate-system.sh
   - Run Anytime: /opt/n8n/validate-system.sh
   - All Checks: PASSED ✅

7. Documentation:
   - System Config: /opt/n8n/SYSTEM_CONFIGURATION.md
   - Includes: Software versions, directory structure, firewall rules, tuning params

Your Next Steps:
1. SSH to hx-n8n-server.hx.dev.local
2. Deploy n8n application code:
   - Extract/build n8n to /opt/n8n/app/
   - Ensure /opt/n8n/app/bin/n8n executable exists
3. Create /opt/n8n/.env file with your n8n configuration:
   - Database connection (from @agent-quinn)
   - N8N settings (ports, URLs, etc.)
   - See: /srv/cc/Governance/x-poc3-n8n-deployment/x-docs/n8n-master-deep-dive-analysis.md Section 5.3
4. Test application:
   - As user n8n: /usr/bin/node /opt/n8n/app/bin/n8n --version
5. Start service:
   - sudo systemctl start n8n
   - sudo systemctl status n8n
   - sudo journalctl -u n8n -f
6. Verify application:
   - Internal: curl http://localhost:5678/healthz
   - External: curl https://n8n.hx.dev.local/healthz
7. Enable on boot (once working):
   - sudo systemctl enable n8n

Notes:
- Systemd service NOT started yet (waiting for your application deployment)
- Environment file (.env) NOT created yet (you own this configuration)
- Firewall allows port 5678 from internal network only (192.168.10.0/24)
- Nginx configured for SSL termination (HTTPS)
- WebSocket support enabled in Nginx (required for n8n editor)

Questions or Issues?
- System configuration: Contact @agent-william
- DNS/SSL issues: Contact @agent-frank
- Database issues: Contact @agent-quinn

I'll be available for:
- System-level troubleshooting
- Firewall adjustments if needed
- Systemd service tuning
- Performance optimization

Ready for your deployment!
```

### 9.2 Handoff to @agent-julia (Testing & QA)

**Timing**: After Task 7.1 (Validation Complete)

**Handoff Method**: Validation report with test plan

**Handoff Message Template**:

```
@agent-julia

System validation complete. Server ready for your OS-level testing.

Validation Summary:
- Validation Script: /opt/n8n/validate-system.sh
- All Checks: PASSED ✅
- Test Plan: Below

Test Plan for QA:

1. System Validation:
   - Run: /opt/n8n/validate-system.sh
   - Expected: All checks pass

2. Node.js Verification:
   - Run: node --version
   - Expected: v22.16.0 or higher

3. pnpm Verification:
   - Run: pnpm --version
   - Expected: 10.18.3 (exact)

4. User Permissions:
   - Run: sudo -u n8n touch /opt/n8n/.n8n/test && sudo -u n8n rm /opt/n8n/.n8n/test
   - Expected: Success (no errors)

5. Firewall Testing:
   - Internal: nc -zv 192.168.10.215 5678 (from 192.168.10.x)
   - External: nc -zv <external-ip> 5678 (from outside 192.168.10.0/24)
   - Expected: Internal succeeds, external fails/times out

6. Nginx Testing:
   - Run: curl -I http://n8n.hx.dev.local
   - Expected: 301 redirect to HTTPS
   - Run: curl -I https://n8n.hx.dev.local
   - Expected: 502 Bad Gateway (n8n not running yet - expected)

7. DNS Resolution:
   - Run: nslookup n8n.hx.dev.local
   - Expected: Returns 192.168.10.215

8. SSL Certificate:
   - Run: openssl s_client -connect n8n.hx.dev.local:443 -servername n8n.hx.dev.local < /dev/null | grep "Verify return code"
   - Expected: "Verify return code: 0 (ok)"

Test Documentation:
- Location: /opt/n8n/SYSTEM_CONFIGURATION.md
- Contains: All software versions, configurations, tuning parameters

Pass/Fail Criteria:
- ✅ PASS: All 8 tests above succeed
- ❌ FAIL: Any test fails (escalate to @agent-william)

Let me know if you need any clarifications on test procedures.
```

### 9.3 Coordination with @agent-frank (Ongoing)

**Handoff Type**: Collaborative (DNS and SSL)

**Communication Cadence**:
- Initial request: Start of Phase 5 (after system dependencies installed)
- Follow-up: Before Task 6.2 (need SSL cert status)
- Final confirmation: After nginx started successfully

**Status Updates**:
- I will inform Frank when I'm ready for SSL cert (Task 6.1 complete)
- Frank will inform me when SSL cert is installed
- I will confirm nginx operational after SSL cert installed

### 9.4 Escalation Protocol

**Level 1: Internal Resolution**
- **Scope**: Issues I can resolve independently (configuration, tuning, troubleshooting)
- **Timeline**: Within 30 minutes
- **Examples**: Package installation failures, permission issues, firewall rules

**Level 2: Agent Coordination**
- **Scope**: Issues requiring another agent (SSL cert, database connectivity, DNS)
- **Timeline**: Within 2 hours
- **Method**: Direct message to relevant agent (@agent-frank, @agent-quinn)
- **Examples**: SSL cert format issues, DNS resolution failures

**Level 3: Project Orchestrator**
- **Scope**: Blocking issues affecting project timeline
- **Timeline**: Immediate
- **Method**: Message to @agent-zero with full context
- **Examples**: Server access failure, critical resource constraints, conflicting requirements

**Escalation Message Template**:

```
@agent-zero

ESCALATION: [Issue Title]

Issue:
- Task Blocked: [Task number and name]
- Blocking Agent: [If applicable]
- Description: [Clear description of problem]

Attempted Resolution:
- Action 1: [What I tried]
- Result 1: [What happened]
- Action 2: [What I tried]
- Result 2: [What happened]

Impact:
- Blocks: [What work is blocked]
- Timeline: [How much delay]
- Workaround: [If any available]

Request:
- [Specific help needed]
- [Who needs to be involved]
- [Timeline for resolution]
```

---

## 10. Sign-off Criteria

### 10.1 My Sign-off (Agent William Taylor)

I will sign off on my deliverables when ALL of the following are complete:

#### Phase 1-5: System Preparation ✅
- [ ] Server accessible via SSH (hx-n8n-server.hx.dev.local)
- [ ] Ubuntu 22.04/24.04 LTS verified
- [ ] All system updates applied
- [ ] Node.js ≥22.16.0 installed and verified
- [ ] pnpm 10.18.3 installed and verified
- [ ] All system dependencies installed (build-essential, python3, cairo, pango, etc.)
- [ ] Service user `n8n` created with correct settings
- [ ] Complete directory structure created with correct permissions
- [ ] Firewall configured (port 5678 internal only, 80/443 open)
- [ ] System performance tuning applied (sysctl, ulimit)
- [ ] Systemd service unit template created

#### Phase 6: Nginx Configuration ✅
- [ ] Nginx installed
- [ ] Nginx reverse proxy configuration created
- [ ] SSL certificate installed (by @agent-frank)
- [ ] Nginx configuration test passes (sudo nginx -t)
- [ ] Nginx site enabled and service started
- [ ] HTTPS redirect functional (curl test passes)

#### Phase 7: Validation & Documentation ✅
- [ ] System validation script created and tested
- [ ] All validation checks pass (automated script)
- [ ] Manual validation checks verified
- [ ] System configuration documentation complete
- [ ] Handoff package prepared for @agent-omar

#### Integration Checks ✅
- [ ] DNS resolution verified (n8n.hx.dev.local → 192.168.10.215)
- [ ] SSL certificate valid and trusted
- [ ] Database connectivity testable (PostgreSQL client installed)
- [ ] Application deployment path ready (/opt/n8n/app/)

### 10.2 Sign-off Format

When all criteria met, I will provide formal sign-off:

```
=== AGENT WILLIAM TAYLOR SIGN-OFF ===

Project: POC3 N8N Deployment
Server: hx-n8n-server.hx.dev.local (192.168.10.215)
Date: [Completion Date]
Duration: [Actual hours worked]

DELIVERABLES STATUS: ✅ COMPLETE

Phase 1: System Verification - ✅ COMPLETE
Phase 2: System Dependencies - ✅ COMPLETE
Phase 3: Node.js & pnpm - ✅ COMPLETE
Phase 4: User & Directory Structure - ✅ COMPLETE
Phase 5: System Configuration - ✅ COMPLETE
Phase 6: Nginx Configuration - ✅ COMPLETE
Phase 7: Validation & Documentation - ✅ COMPLETE

VALIDATION RESULTS:
- System Validation Script: PASSED ✅
- Node.js Version: [Installed version] ✅
- pnpm Version: 10.18.3 ✅
- Service User: n8n (UID [XXX]) ✅
- Directory Structure: VERIFIED ✅
- Firewall Rules: CONFIGURED ✅
- System Tuning: APPLIED ✅
- Nginx Status: ACTIVE ✅
- DNS Resolution: VERIFIED ✅
- SSL Certificate: VALID ✅

HANDOFF TO:
- Primary: @agent-omar (N8N Application Deployment)
- Validation: @agent-julia (Testing & QA)

DOCUMENTATION:
- System Configuration: /opt/n8n/SYSTEM_CONFIGURATION.md
- Validation Script: /opt/n8n/validate-system.sh

NOTES:
- [Any special notes or considerations]
- [Known issues or pending items]
- [Recommendations for next phase]

SERVER READY FOR APPLICATION DEPLOYMENT ✅

Signed: Agent William Taylor (@agent-william)
Date: [YYYY-MM-DD HH:MM]
```

### 10.3 Dependencies for Sign-off

My sign-off is **BLOCKED BY**:

1. **@agent-frank (FreeIPA Identity & Trust)**:
   - DNS A record: n8n.hx.dev.local → 192.168.10.215
   - SSL certificate installed and valid
   - Certificate validation passes

**Note**: I cannot complete Phase 6 (Nginx) without @agent-frank's SSL certificate. However, I can complete Phases 1-5 and 7 independently. I will document "Nginx pending SSL cert" in that case and provide conditional sign-off.

### 10.4 Conditional Sign-off (if SSL cert delayed)

If SSL certificate is not available, I can provide conditional sign-off:

```
=== AGENT WILLIAM TAYLOR CONDITIONAL SIGN-OFF ===

Project: POC3 N8N Deployment
Server: hx-n8n-server.hx.dev.local (192.168.10.215)
Date: [Completion Date]

DELIVERABLES STATUS: ⚠️ PARTIAL COMPLETE

Phases 1-5: ✅ COMPLETE (System fully prepared)
Phase 6: ⏳ PENDING (Nginx configured, waiting for SSL cert from @agent-frank)
Phase 7: ✅ COMPLETE (Validation and documentation done)

BLOCKING ITEM:
- SSL certificate for n8n.hx.dev.local
- Owner: @agent-frank
- Status: PENDING
- Impact: Nginx cannot be started until certificate installed

WORK COMPLETED:
- [List of completed work]

REMAINING WORK:
1. @agent-frank installs SSL certificate
2. I enable nginx site and start service (10 minutes)
3. I verify HTTPS functionality
4. I provide final sign-off

SERVER READY FOR APPLICATION DEPLOYMENT: ⚠️ NO (waiting for SSL cert)

Conditional Sign-off: Agent William Taylor (@agent-william)
Date: [YYYY-MM-DD HH:MM]
```

---

## CodeRabbit Note: Development Standards Compliance Section

**Status**: ⚠️ MISSING (Non-Blocking for POC3)

This planning document currently lacks a Development Standards Compliance section analyzing adherence to SOLID principles (specifically Dependency Inversion Principle). Other agent planning documents (Omar, Frank, George, Olivia) include comprehensive DIP analysis with ratings and actionable recommendations.

**CodeRabbit Feedback**: "DIP compliance gap identified but no concrete mitigation proposed. For Chill review level, mark as [noted]."

**What's Missing**:
- Analysis of how systemd services, shell scripts, and configuration management use abstractions (environment variables, config files) instead of hardcoded values
- Rating of DIP compliance (e.g., 7/10) with specific examples
- Actionable TODO comments identifying where hardcoded thresholds (MIN_PACKAGES, LOG_RETENTION_DAYS, etc.) should be externalized

**Recommendation for Phase 4**:
Add Section 9 ("Development Standards Compliance") with subsections for each SOLID principle, focusing on DIP analysis with concrete examples from systemd service templates (T-034), resource validation scripts (T-001), and logging configuration (T-036).

**Reference**: See `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/CODERABBIT-NOTE-william-dip-analysis-gap.md` for detailed analysis and template for future implementation.

---

## Document Metadata

```yaml
document_type: Agent Planning Analysis
project: POC3 N8N Workflow Automation Deployment
agent_name: William Taylor
agent_shortname: william
agent_invocation: "@agent-william"
role: Ubuntu Systems Administrator
phase: Phase 2 - Collaborative Planning
created_date: 2025-11-07
created_by: Agent William Taylor
server: hx-n8n-server.hx.dev.local
server_ip: 192.168.10.215
classification: Internal - Project Documentation
related_documents:
  - /srv/cc/Governance/x-poc3-n8n-deployment/planning/work-plan.md
  - /srv/cc/Governance/x-poc3-n8n-deployment/x-docs/n8n-master-deep-dive-analysis.md
  - /srv/cc/Governance/0.0-governance/0.0.5-Delivery/0.0.5.0-agent-constitution.md
  - /srv/cc/Governance/0.1-agents/agent-william.md
knowledge_source:
  - n8n technical analysis (Section 4: Installation Requirements)
  - Ubuntu Systems Administration best practices
  - Nginx reverse proxy configuration standards
  - SOLID principles (Development Standards)
status: Draft - Ready for Phase 2 Review
version: 1.0
last_updated: 2025-11-07
location: /srv/cc/Governance/x-poc3-n8n-deployment/x-docs/agent-william-planning-analysis.md
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-07 | Initial planning analysis document for William Taylor's infrastructure tasks | @agent-william |
| 1.1 | 2025-11-07 | **CodeRabbit Note**: Added section documenting missing Development Standards Compliance / DIP analysis (lines 2269-2285). Marked as non-blocking for POC3 "Chill review level" but noted for Phase 4 implementation. Created reference document `CODERABBIT-NOTE-william-dip-analysis-gap.md` with detailed recommendations for future DIP section including actionable TODO comments for systemd services, validation scripts, and configuration files. | Claude Code |

---

**Document Type**: Agent Planning Analysis
**Version**: 1.1
**Date**: 2025-11-07
**Location**: `/srv/cc/Governance/x-poc3-n8n-deployment/x-docs/agent-william-planning-analysis.md`

---

**END OF DOCUMENT**
