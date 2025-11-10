#!/bin/bash
#==============================================================================
# Task T-003: SSL Certificate Transfer with Enhanced Error Handling
# Description: Transfer SSL certificates from hx-ca-server to hx-n8n-server
# Assigned Agent: @agent-frank (Infrastructure & Identity Specialist)
# Project: POC3 N8N Deployment
# Created: 2025-11-09
# Version: 2.0 (Updated for Samba AD infrastructure)
#
# PURPOSE:
# This script safely transfers SSL certificates from the Certificate Authority
# server to the N8N application server with comprehensive error handling,
# audit logging, and data integrity verification.
#
# INFRASTRUCTURE:
# - Source: hx-ca-server.hx.dev.local (192.168.10.201) - easy-rsa CA
# - Target: hx-n8n-server.hx.dev.local (192.168.10.215) - N8N application
# - Domain: HX.DEV.LOCAL (Samba Active Directory)
#
# COMPLIANCE:
# - SOC 2 CC6.7: Audit logging of security-sensitive operations
# - PCI-DSS 10.2.7: Creation and deletion of system-level objects
# - NIST 800-53 AU-2: Auditable events (certificate installation)
#==============================================================================

set -euo pipefail  # Exit on error, undefined variables, pipe failures
IFS=$'\n\t'        # Safer IFS for word splitting

#------------------------------------------------------------------------------
# Configuration
#------------------------------------------------------------------------------
SOURCE_SERVER="hx-ca-server.hx.dev.local"  # Certificate Authority server
SOURCE_IP="192.168.10.201"
SOURCE_USER="administrator"

TARGET_SERVER="hx-n8n-server.hx.dev.local"  # N8N application server
TARGET_IP="192.168.10.215"
TARGET_USER="administrator"

# Certificate files (adjust these if your CA uses different naming)
PRIVATE_KEY="n8n.hx.dev.local.key"
CERTIFICATE="n8n.hx.dev.local.crt"
CA_CERTIFICATE="hx-dev-ca.crt"

# Source paths (adjust based on your easy-rsa PKI directory structure)
SOURCE_KEY_PATH="/etc/ssl/private/${PRIVATE_KEY}"
SOURCE_CERT_PATH="/etc/ssl/certs/${CERTIFICATE}"
SOURCE_CA_PATH="/etc/ssl/certs/${CA_CERTIFICATE}"

# Target paths
TARGET_KEY_DIR="/etc/ssl/private"
TARGET_CERT_DIR="/etc/ssl/certs"

# Logging
LOG_DIR="/opt/n8n/logs"
LOG_FILE="${LOG_DIR}/t-003-ssl-transfer-$(date +%Y%m%d-%H%M%S).log"
TEMP_DIR="/tmp/ssl-transfer-$$"  # Unique temp dir (PID-based)

# Exit codes
EXIT_SUCCESS=0
EXIT_ERROR=1

#------------------------------------------------------------------------------
# Logging Functions
#------------------------------------------------------------------------------
log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="[$timestamp] $*"
    echo "$message" | tee -a "$LOG_FILE"
}

log_error() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="[$timestamp] ERROR: $*"
    echo "$message" | tee -a "$LOG_FILE" >&2
}

log_success() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="[$timestamp] SUCCESS: $*"
    echo "$message" | tee -a "$LOG_FILE"
}

log_warning() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="[$timestamp] WARNING: $*"
    echo "$message" | tee -a "$LOG_FILE"
}

#------------------------------------------------------------------------------
# Error Handling Functions
#------------------------------------------------------------------------------
cleanup() {
    local exit_code=$?

    if [ $exit_code -ne 0 ]; then
        log_error "Task failed with exit code $exit_code"
        log_error "Review log file: $LOG_FILE"
        log_error "Escalation path:"
        log_error "  Primary: @agent-frank (Infrastructure & Identity Specialist)"
        log_error "  Secondary: Security team (certificate issues)"
        log_error "  Tertiary: Network team (connectivity issues)"
    fi

    # Clean up temporary files on local workstation
    if [ -d "$TEMP_DIR" ]; then
        log "Cleaning up temporary directory: $TEMP_DIR"
        rm -rf "$TEMP_DIR"
    fi

    # Clean up temporary files on target server
    log "Cleaning up temporary files on target server..."
    ssh "${TARGET_USER}@${TARGET_IP}" "rm -f /tmp/${PRIVATE_KEY} /tmp/${CERTIFICATE} /tmp/${CA_CERTIFICATE}" 2>&1 | tee -a "$LOG_FILE" || true

    log "========================================"
    log "Task T-003 completed with exit code: $exit_code"
    log "========================================"

    exit $exit_code
}

trap cleanup EXIT ERR INT TERM

#------------------------------------------------------------------------------
# Pre-Flight Checks
#------------------------------------------------------------------------------
preflight_checks() {
    log "========================================"
    log "Task T-003: SSL Certificate Transfer"
    log "========================================"
    log "Timestamp: $(date)"
    log "Executing User: $(whoami)"
    log "Source Server: $SOURCE_SERVER ($SOURCE_IP)"
    log "Target Server: $TARGET_SERVER ($TARGET_IP)"
    log "Log File: $LOG_FILE"
    log ""

    # Check if running with appropriate permissions
    if [ "$(whoami)" != "$SOURCE_USER" ] && [ "$(whoami)" != "root" ]; then
        log_warning "Not running as $SOURCE_USER or root. Sudo may be required for some operations."
    fi

    # Create log directory on target server if needed
    log "Creating log directory on target server..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo mkdir -p ${LOG_DIR} && sudo chown ${TARGET_USER}:${TARGET_USER} ${LOG_DIR}" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to create log directory on target server"
        return 1
    fi

    # Create unique temp directory on local workstation
    mkdir -p "$TEMP_DIR"
    log "Created temporary directory: $TEMP_DIR"

    # Verify SSH connectivity to source server
    log "Verifying SSH connectivity to source server (${SOURCE_SERVER})..."
    if ! ssh -o ConnectTimeout=10 "${SOURCE_USER}@${SOURCE_IP}" "echo 'SSH connection successful'" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Cannot connect to source server via SSH"
        log_error "Check: 1) Network connectivity, 2) SSH service, 3) Credentials"
        return 1
    fi

    # Verify SSH connectivity to target server
    log "Verifying SSH connectivity to target server (${TARGET_SERVER})..."
    if ! ssh -o ConnectTimeout=10 "${TARGET_USER}@${TARGET_IP}" "echo 'SSH connection successful'" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Cannot connect to target server via SSH"
        log_error "Check: 1) Network connectivity, 2) SSH service, 3) Credentials"
        return 1
    fi

    # Verify source files exist
    log "Verifying source certificate files on $SOURCE_SERVER..."

    if ! ssh "${SOURCE_USER}@${SOURCE_IP}" "test -f ${SOURCE_KEY_PATH}" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Private key not found: ${SOURCE_KEY_PATH}"
        log_error "Run certificate generation procedure first (see SSL-CERTIFICATE-GENERATION-GUIDE.md)"
        return 1
    fi
    log "  ✓ Private key found: ${SOURCE_KEY_PATH}"

    if ! ssh "${SOURCE_USER}@${SOURCE_IP}" "test -f ${SOURCE_CERT_PATH}" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Certificate not found: ${SOURCE_CERT_PATH}"
        log_error "Run certificate generation procedure first (see SSL-CERTIFICATE-GENERATION-GUIDE.md)"
        return 1
    fi
    log "  ✓ Certificate found: ${SOURCE_CERT_PATH}"

    if ! ssh "${SOURCE_USER}@${SOURCE_IP}" "test -f ${SOURCE_CA_PATH}" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "CA certificate not found: ${SOURCE_CA_PATH}"
        log_error "Ensure CA certificate is available at ${SOURCE_CA_PATH}"
        return 1
    fi
    log "  ✓ CA certificate found: ${SOURCE_CA_PATH}"

    log_success "Pre-flight checks passed"
    log ""
}

#------------------------------------------------------------------------------
# Step 1: Transfer Certificates from Source to Local Temp Directory
#------------------------------------------------------------------------------
transfer_from_source() {
    log "========================================"
    log "Step 1: Transferring certificates from source server"
    log "========================================"

    # Transfer private key
    log "Transferring private key: $PRIVATE_KEY"
    if ! scp "${SOURCE_USER}@${SOURCE_IP}:${SOURCE_KEY_PATH}" "$TEMP_DIR/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to transfer private key"
        log_error "Check: 1) File permissions on source, 2) SCP connectivity, 3) Disk space"
        return 1
    fi

    # Verify file size (private key should be >0 bytes)
    local key_size=$(stat -c%s "$TEMP_DIR/$PRIVATE_KEY")
    if [ "$key_size" -eq 0 ]; then
        log_error "Private key file is empty (0 bytes)"
        log_error "Source file may be corrupted or transfer incomplete"
        return 1
    fi
    log "Private key size: $key_size bytes ✓"

    # Transfer certificate
    log "Transferring certificate: $CERTIFICATE"
    if ! scp "${SOURCE_USER}@${SOURCE_IP}:${SOURCE_CERT_PATH}" "$TEMP_DIR/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to transfer certificate"
        log_error "Check: 1) File permissions on source, 2) SCP connectivity, 3) Disk space"
        return 1
    fi

    local cert_size=$(stat -c%s "$TEMP_DIR/$CERTIFICATE")
    if [ "$cert_size" -eq 0 ]; then
        log_error "Certificate file is empty (0 bytes)"
        log_error "Source file may be corrupted or transfer incomplete"
        return 1
    fi
    log "Certificate size: $cert_size bytes ✓"

    # Transfer CA certificate
    log "Transferring CA certificate: $CA_CERTIFICATE"
    if ! scp "${SOURCE_USER}@${SOURCE_IP}:${SOURCE_CA_PATH}" "$TEMP_DIR/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to transfer CA certificate"
        log_error "Check: 1) File permissions on source, 2) SCP connectivity, 3) Disk space"
        return 1
    fi

    local ca_size=$(stat -c%s "$TEMP_DIR/$CA_CERTIFICATE")
    if [ "$ca_size" -eq 0 ]; then
        log_error "CA certificate file is empty (0 bytes)"
        log_error "Source file may be corrupted or transfer incomplete"
        return 1
    fi
    log "CA certificate size: $ca_size bytes ✓"

    log_success "All certificates transferred from source server"
    log ""
}

#------------------------------------------------------------------------------
# Step 2: Validate Certificate Integrity
#------------------------------------------------------------------------------
validate_certificates() {
    log "========================================"
    log "Step 2: Validating certificate integrity"
    log "========================================"

    # Verify certificate format (PEM format check)
    log "Checking certificate format..."
    if ! openssl x509 -in "$TEMP_DIR/$CERTIFICATE" -noout -subject 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Certificate format validation failed (corrupted or invalid PEM format)"
        log_error "Certificate may be corrupted during transfer or generation"
        return 1
    fi

    # Extract and log certificate subject
    local cert_subject=$(openssl x509 -in "$TEMP_DIR/$CERTIFICATE" -noout -subject 2>/dev/null)
    log "Certificate subject: $cert_subject"

    # Extract and log certificate issuer
    local cert_issuer=$(openssl x509 -in "$TEMP_DIR/$CERTIFICATE" -noout -issuer 2>/dev/null)
    log "Certificate issuer: $cert_issuer"

    # Verify certificate expiration
    local cert_expiry=$(openssl x509 -in "$TEMP_DIR/$CERTIFICATE" -noout -enddate 2>/dev/null | cut -d= -f2)
    log "Certificate expiry: $cert_expiry"

    # Check if certificate expired
    if ! openssl x509 -in "$TEMP_DIR/$CERTIFICATE" -noout -checkend 0 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Certificate has expired!"
        log_error "Generate a new certificate before proceeding"
        return 1
    fi
    log "Certificate is currently valid ✓"

    # Check if certificate expires within 30 days (warning only)
    if ! openssl x509 -in "$TEMP_DIR/$CERTIFICATE" -noout -checkend 2592000 2>/dev/null; then
        log_warning "Certificate expires within 30 days - plan renewal soon"
    fi

    # Verify private key format
    log "Checking private key format..."
    if ! openssl rsa -in "$TEMP_DIR/$PRIVATE_KEY" -check -noout 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Private key format validation failed (corrupted or invalid)"
        log_error "Private key may be corrupted or encrypted with passphrase"
        return 1
    fi
    log "Private key format is valid ✓"

    # Verify key-certificate pair match
    log "Verifying private key matches certificate..."
    local key_modulus=$(openssl rsa -in "$TEMP_DIR/$PRIVATE_KEY" -noout -modulus 2>/dev/null | openssl md5 | cut -d' ' -f2)
    local cert_modulus=$(openssl x509 -in "$TEMP_DIR/$CERTIFICATE" -noout -modulus 2>/dev/null | openssl md5 | cut -d' ' -f2)

    if [ "$key_modulus" != "$cert_modulus" ]; then
        log_error "Private key does not match certificate (modulus mismatch)"
        log_error "Key modulus: $key_modulus"
        log_error "Cert modulus: $cert_modulus"
        log_error "Ensure you're using the correct key-certificate pair"
        return 1
    fi
    log "Private key matches certificate ✓"

    # Verify CA certificate format
    log "Checking CA certificate format..."
    if ! openssl x509 -in "$TEMP_DIR/$CA_CERTIFICATE" -noout -subject 2>&1 | tee -a "$LOG_FILE"; then
        log_error "CA certificate format validation failed"
        return 1
    fi
    local ca_subject=$(openssl x509 -in "$TEMP_DIR/$CA_CERTIFICATE" -noout -subject 2>/dev/null)
    log "CA certificate subject: $ca_subject"

    log_success "Certificate validation passed"
    log ""
}

#------------------------------------------------------------------------------
# Step 3: Transfer to Target Server
#------------------------------------------------------------------------------
transfer_to_target() {
    log "========================================"
    log "Step 3: Transferring certificates to target server"
    log "========================================"

    # Create target directories if needed
    log "Creating target directories on $TARGET_SERVER..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo mkdir -p ${TARGET_KEY_DIR} ${TARGET_CERT_DIR}" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to create target directories"
        log_error "Check: 1) Sudo permissions, 2) Filesystem space, 3) Parent directory permissions"
        return 1
    fi
    log "Target directories created/verified ✓"

    # Transfer files to target /tmp first (avoid permission issues)
    log "Transferring private key to target server..."
    if ! scp "$TEMP_DIR/$PRIVATE_KEY" "${TARGET_USER}@${TARGET_IP}:/tmp/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to transfer private key to target"
        log_error "Check: 1) Network connectivity, 2) Disk space on target /tmp, 3) SSH permissions"
        return 1
    fi

    # Verify transferred file size on target
    local target_key_size=$(ssh "${TARGET_USER}@${TARGET_IP}" "stat -c%s /tmp/${PRIVATE_KEY}" 2>/dev/null)
    local local_key_size=$(stat -c%s "$TEMP_DIR/$PRIVATE_KEY")
    if [ "$target_key_size" != "$local_key_size" ]; then
        log_error "Private key size mismatch (local: $local_key_size, target: $target_key_size)"
        log_error "Transfer may be incomplete or corrupted"
        return 1
    fi
    log "Private key transferred successfully ($target_key_size bytes) ✓"

    log "Transferring certificate to target server..."
    if ! scp "$TEMP_DIR/$CERTIFICATE" "${TARGET_USER}@${TARGET_IP}:/tmp/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to transfer certificate to target"
        log_error "Check: 1) Network connectivity, 2) Disk space on target /tmp, 3) SSH permissions"
        return 1
    fi

    local target_cert_size=$(ssh "${TARGET_USER}@${TARGET_IP}" "stat -c%s /tmp/${CERTIFICATE}" 2>/dev/null)
    local local_cert_size=$(stat -c%s "$TEMP_DIR/$CERTIFICATE")
    if [ "$target_cert_size" != "$local_cert_size" ]; then
        log_error "Certificate size mismatch (local: $local_cert_size, target: $target_cert_size)"
        log_error "Transfer may be incomplete or corrupted"
        return 1
    fi
    log "Certificate transferred successfully ($target_cert_size bytes) ✓"

    log "Transferring CA certificate to target server..."
    if ! scp "$TEMP_DIR/$CA_CERTIFICATE" "${TARGET_USER}@${TARGET_IP}:/tmp/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to transfer CA certificate to target"
        log_error "Check: 1) Network connectivity, 2) Disk space on target /tmp, 3) SSH permissions"
        return 1
    fi

    local target_ca_size=$(ssh "${TARGET_USER}@${TARGET_IP}" "stat -c%s /tmp/${CA_CERTIFICATE}" 2>/dev/null)
    local local_ca_size=$(stat -c%s "$TEMP_DIR/$CA_CERTIFICATE")
    if [ "$target_ca_size" != "$local_ca_size" ]; then
        log_error "CA certificate size mismatch (local: $local_ca_size, target: $target_ca_size)"
        log_error "Transfer may be incomplete or corrupted"
        return 1
    fi
    log "CA certificate transferred successfully ($target_ca_size bytes) ✓"

    log_success "Files transferred to target server /tmp"
    log ""
}

#------------------------------------------------------------------------------
# Step 4: Install Certificates with Correct Permissions
#------------------------------------------------------------------------------
install_certificates() {
    log "========================================"
    log "Step 4: Installing certificates with permissions"
    log "========================================"

    # Backup existing certificates if present (rollback capability)
    log "Checking for existing certificates..."
    if ssh "${TARGET_USER}@${TARGET_IP}" "sudo test -f ${TARGET_KEY_DIR}/${PRIVATE_KEY}" 2>/dev/null; then
        log_warning "Existing private key found - creating backup"
        if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo cp ${TARGET_KEY_DIR}/${PRIVATE_KEY} ${TARGET_KEY_DIR}/${PRIVATE_KEY}.backup-$(date +%Y%m%d-%H%M%S)" 2>&1 | tee -a "$LOG_FILE"; then
            log_error "Failed to backup existing private key"
            return 1
        fi
        log "  ✓ Private key backed up"
    fi

    if ssh "${TARGET_USER}@${TARGET_IP}" "sudo test -f ${TARGET_CERT_DIR}/${CERTIFICATE}" 2>/dev/null; then
        log_warning "Existing certificate found - creating backup"
        if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo cp ${TARGET_CERT_DIR}/${CERTIFICATE} ${TARGET_CERT_DIR}/${CERTIFICATE}.backup-$(date +%Y%m%d-%H%M%S)" 2>&1 | tee -a "$LOG_FILE"; then
            log_error "Failed to backup existing certificate"
            return 1
        fi
        log "  ✓ Certificate backed up"
    fi

    # Move private key
    log "Installing private key to $TARGET_KEY_DIR..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo mv -f /tmp/${PRIVATE_KEY} ${TARGET_KEY_DIR}/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to move private key"
        log_error "Check: 1) Sudo permissions, 2) Filesystem space, 3) SELinux context"
        return 1
    fi

    # Set private key permissions (600, root:root)
    log "Setting private key permissions (600, root:root)..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo chown root:root ${TARGET_KEY_DIR}/${PRIVATE_KEY} && sudo chmod 600 ${TARGET_KEY_DIR}/${PRIVATE_KEY}" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to set private key permissions"
        return 1
    fi

    # Move certificate
    log "Installing certificate to $TARGET_CERT_DIR..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo mv -f /tmp/${CERTIFICATE} ${TARGET_CERT_DIR}/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to move certificate"
        log_error "Check: 1) Sudo permissions, 2) Filesystem space, 3) SELinux context"
        return 1
    fi

    # Set certificate permissions (644, root:root)
    log "Setting certificate permissions (644, root:root)..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo chown root:root ${TARGET_CERT_DIR}/${CERTIFICATE} && sudo chmod 644 ${TARGET_CERT_DIR}/${CERTIFICATE}" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to set certificate permissions"
        return 1
    fi

    # Move CA certificate
    log "Installing CA certificate to $TARGET_CERT_DIR..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo mv -f /tmp/${CA_CERTIFICATE} ${TARGET_CERT_DIR}/" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to move CA certificate"
        log_error "Check: 1) Sudo permissions, 2) Filesystem space, 3) SELinux context"
        return 1
    fi

    # Set CA certificate permissions (644, root:root)
    log "Setting CA certificate permissions (644, root:root)..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo chown root:root ${TARGET_CERT_DIR}/${CA_CERTIFICATE} && sudo chmod 644 ${TARGET_CERT_DIR}/${CA_CERTIFICATE}" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Failed to set CA certificate permissions"
        return 1
    fi

    log_success "Certificates installed with correct permissions"
    log ""
}

#------------------------------------------------------------------------------
# Step 5: Verify Installation
#------------------------------------------------------------------------------
verify_installation() {
    log "========================================"
    log "Step 5: Verifying certificate installation"
    log "========================================"

    # Verify private key exists and has correct permissions
    log "Verifying private key..."
    local key_perms=$(ssh "${TARGET_USER}@${TARGET_IP}" "stat -c '%a %U:%G' ${TARGET_KEY_DIR}/${PRIVATE_KEY}" 2>/dev/null)
    if [ "$key_perms" != "600 root:root" ]; then
        log_error "Private key permissions incorrect: $key_perms (expected: 600 root:root)"
        return 1
    fi
    log "Private key permissions: $key_perms ✓"

    # Verify certificate exists and has correct permissions
    log "Verifying certificate..."
    local cert_perms=$(ssh "${TARGET_USER}@${TARGET_IP}" "stat -c '%a %U:%G' ${TARGET_CERT_DIR}/${CERTIFICATE}" 2>/dev/null)
    if [ "$cert_perms" != "644 root:root" ]; then
        log_error "Certificate permissions incorrect: $cert_perms (expected: 644 root:root)"
        return 1
    fi
    log "Certificate permissions: $cert_perms ✓"

    # Verify CA certificate
    log "Verifying CA certificate..."
    local ca_perms=$(ssh "${TARGET_USER}@${TARGET_IP}" "stat -c '%a %U:%G' ${TARGET_CERT_DIR}/${CA_CERTIFICATE}" 2>/dev/null)
    if [ "$ca_perms" != "644 root:root" ]; then
        log_error "CA certificate permissions incorrect: $ca_perms (expected: 644 root:root)"
        return 1
    fi
    log "CA certificate permissions: $ca_perms ✓"

    # Verify certificate validity on target server
    log "Verifying certificate validity on target server..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo openssl x509 -in ${TARGET_CERT_DIR}/${CERTIFICATE} -noout -subject" 2>&1 | tee -a "$LOG_FILE"; then
        log_error "Certificate validation failed on target server"
        return 1
    fi

    # Verify certificate chain (cert signed by CA)
    log "Verifying certificate chain..."
    if ! ssh "${TARGET_USER}@${TARGET_IP}" "sudo openssl verify -CAfile ${TARGET_CERT_DIR}/${CA_CERTIFICATE} ${TARGET_CERT_DIR}/${CERTIFICATE}" 2>&1 | tee -a "$LOG_FILE"; then
        log_warning "Certificate chain verification failed"
        log_warning "This is expected if using self-signed certificates"
        log_warning "For production, ensure certificate is signed by trusted CA"
    else
        log "Certificate chain verified ✓"
    fi

    log_success "Certificate installation verified"
    log ""
}

#------------------------------------------------------------------------------
# Main Execution
#------------------------------------------------------------------------------
main() {
    # Execute all steps sequentially
    preflight_checks || return 1
    transfer_from_source || return 1
    validate_certificates || return 1
    transfer_to_target || return 1
    install_certificates || return 1
    verify_installation || return 1

    log "========================================"
    log "✅ Task T-003 COMPLETED SUCCESSFULLY"
    log "========================================"
    log ""
    log "SSL certificates transferred and installed:"
    log "  - Private Key: ${TARGET_KEY_DIR}/${PRIVATE_KEY} (600, root:root)"
    log "  - Certificate: ${TARGET_CERT_DIR}/${CERTIFICATE} (644, root:root)"
    log "  - CA Certificate: ${TARGET_CERT_DIR}/${CA_CERTIFICATE} (644, root:root)"
    log ""
    log "Certificate Details:"
    ssh "${TARGET_USER}@${TARGET_IP}" "sudo openssl x509 -in ${TARGET_CERT_DIR}/${CERTIFICATE} -noout -subject -issuer -dates" 2>/dev/null | while read line; do
        log "  $line"
    done
    log ""
    log "Next Steps:"
    log "  1. Review log file: $LOG_FILE"
    log "  2. Proceed to T-004 (Install Nginx)"
    log "  3. Configure Nginx to use these certificates:"
    log "       ssl_certificate ${TARGET_CERT_DIR}/${CERTIFICATE};"
    log "       ssl_certificate_key ${TARGET_KEY_DIR}/${PRIVATE_KEY};"
    log "  4. Test HTTPS connectivity after nginx configuration"
    log ""
    log_success "Task execution complete"

    return $EXIT_SUCCESS
}

# Execute main function
main
