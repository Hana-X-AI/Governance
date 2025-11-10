# CodeRabbit CLI Installation

## ⚠️ Security Notice

**DO NOT blindly pipe remote scripts to shell interpreters.** Always download, inspect, and verify installation scripts before execution.

## Recommended Installation Methods

### Option 1: Download, Inspect, Execute (Recommended)

```bash
# Download the installer
curl -fsSL https://cli.coderabbit.ai/install.sh -o /tmp/coderabbit-install.sh

# Inspect the script contents
less /tmp/coderabbit-install.sh
# OR
cat /tmp/coderabbit-install.sh

# After reviewing and verifying the script is safe, execute it
chmod +x /tmp/coderabbit-install.sh
/tmp/coderabbit-install.sh

# Clean up
rm /tmp/coderabbit-install.sh
```

### Option 2: Package Managers (Safer Alternative)

**Homebrew (macOS/Linux)**:
```bash
# If available via Homebrew
brew install coderabbit-cli
```

**Platform-Specific Packages**:
- Check CodeRabbit's official documentation for distro-specific packages (apt, yum, dnf, pacman)
- Verify package signatures when available

### Option 3: Direct Binary Download

```bash
# Download pre-built binary directly
# (Check https://cli.coderabbit.ai for latest release URLs)
curl -fsSL https://cli.coderabbit.ai/releases/latest/coderabbit-linux-amd64 -o /usr/local/bin/coderabbit
chmod +x /usr/local/bin/coderabbit

# Verify installation
coderabbit --version
```

## ⛔ Unsafe Method (NOT RECOMMENDED)

```bash
# ❌ DO NOT USE: Pipes remote script directly to shell without inspection
# curl -fsSL https://cli.coderabbit.ai/install.sh | sh
```

**Why This Is Dangerous**:
- No opportunity to review what the script does before execution
- Script could be compromised via MITM attack
- No verification of script integrity or authenticity
- Executes with current user's privileges immediately

## Platform-Specific Notes

**Linux**:
- Prefer distro package managers (apt, yum, dnf) if packages are available
- Verify GPG signatures when downloading binaries

**macOS**:
- Use Homebrew if available
- macOS Gatekeeper may require additional permissions for unsigned binaries

**Windows**:
- Check for official MSI installer or Chocolatey package
- PowerShell execution policy may need adjustment

## Post-Installation

```bash
# Verify installation
coderabbit --version

# Configure API key (never hardcode in scripts)
export CODERABBIT_API_KEY="<your-api-key>"

# Or store in secure location
echo 'export CODERABBIT_API_KEY="<your-api-key>"' >> ~/.bashrc
```

## Security Best Practices

1. **Always inspect scripts** before piping to shell
2. **Use package managers** when available (built-in verification)
3. **Verify checksums/signatures** for direct binary downloads
4. **Use HTTPS** for all downloads
5. **Store API keys securely** (environment variables, not hardcoded)

