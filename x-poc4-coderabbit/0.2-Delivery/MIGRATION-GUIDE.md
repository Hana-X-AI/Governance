# Phase 2 to Phase 3 Migration Guide

**Document Type**: Delivery - Migration Guide
**Project**: POC4 CodeRabbit Integration - Path A
**Version**: 1.0
**Date**: 2025-11-10
**Target Audience**: Future developers, maintainers, operations teams

---

## Overview

This guide provides step-by-step instructions for upgrading Roger Code Review Orchestrator from Phase 2 (Layer 1 only) to Phase 3 (Layer 1 + Layer 3 CodeRabbit AI integration).

**Migration Type**: Non-breaking upgrade (backward compatible)
**Estimated Time**: 30-45 minutes
**Downtime Required**: None (Layer 3 is disabled by default)
**Rollback Supported**: Yes

---

## Prerequisites

Before starting the migration, ensure the following prerequisites are met:

### 1. Phase 2 Baseline Verification

```bash
# Navigate to Roger directory
cd /srv/cc/hana-x-infrastructure/.claude/agents/roger

# Verify Phase 2 is operational
python -m pytest test_roger.py -v

# Expected output: 17/17 tests PASSED
```

**Required**: All 17 Phase 2 tests must pass before proceeding.

### 2. Infrastructure Requirements

```bash
# 1. CodeRabbit CLI installed and accessible
which coderabbit
# Expected: /usr/local/bin/coderabbit

coderabbit --version
# Expected: 0.3.4 or higher

# 2. Redis server accessible
redis-cli -h hx-redis-server.hx.dev.local ping
# Expected: PONG

# Alternative: Use IP address
redis-cli -h 192.168.10.210 ping
# Expected: PONG

# 3. CodeRabbit API key set
echo $CODERABBIT_API_KEY
# Expected: cr-... (should display API key)

# 4. Verify cache directory permissions
mkdir -p /srv/cc/hana-x-infrastructure/.claude/agents/roger/cache/coderabbit
touch /srv/cc/hana-x-infrastructure/.claude/agents/roger/cache/coderabbit/test.tmp
rm /srv/cc/hana-x-infrastructure/.claude/agents/roger/cache/coderabbit/test.tmp
# Expected: No errors (directory is writable)
```

---

## Migration Steps

### Step 1: Backup Phase 2 Configuration

**Why**: Create restore point in case of issues

```bash
# Create backup directory
mkdir -p /srv/cc/hana-x-infrastructure/.claude/agents/roger/backups/phase2-$(date +%Y%m%d)

# Backup Phase 2 files
cp roger_orchestrator.py backups/phase2-$(date +%Y%m%d)/
cp layer3_stub.py backups/phase2-$(date +%Y%m%d)/
cp linter_aggregator.py backups/phase2-$(date +%Y%m%d)/

# Verify backup
ls -lh backups/phase2-$(date +%Y%m%d)/
```

**Expected**: 3 files backed up successfully

---

### Step 2: Deploy Phase 3 Code

**Method A: Git Pull (Recommended)**

```bash
# From Roger directory
cd /srv/cc/hana-x-infrastructure

# Fetch latest Phase 3 code
git fetch origin
git pull origin main

# Verify Phase 3 files present
ls -lh .claude/agents/roger/layer3_coderabbit.py
ls -lh .claude/agents/roger/coderabbit_client.py
ls -lh .claude/agents/roger/coderabbit_cache.py
ls -lh .claude/agents/roger/rate_limiter.py
```

**Method B: Manual Deployment** (if Git not available)

```bash
# Copy Phase 3 files to Roger directory
cp <source>/layer3_coderabbit.py .claude/agents/roger/
cp <source>/coderabbit_client.py .claude/agents/roger/
cp <source>/coderabbit_cache.py .claude/agents/roger/
cp <source>/rate_limiter.py .claude/agents/roger/

# Verify permissions
chmod 644 .claude/agents/roger/layer3_coderabbit.py
chmod 644 .claude/agents/roger/coderabbit_client.py
chmod 644 .claude/agents/roger/coderabbit_cache.py
chmod 644 .claude/agents/roger/rate_limiter.py
```

---

### Step 3: Deploy Configuration File

**Create Layer 3 configuration**:

```bash
# Create config directory if not exists
mkdir -p /srv/cc/hana-x-infrastructure/.claude/agents/roger/configs

# Deploy configuration file
cp <source>/layer3-coderabbit.yaml configs/

# OR create manually:
cat > configs/layer3-coderabbit.yaml <<'EOF'
# Layer 3 CodeRabbit Configuration
version: "1.0"

# Enable/disable Layer 3 globally
enabled: false  # Default: disabled (expensive)

# API Configuration
api:
  cli_path: "/usr/local/bin/coderabbit"
  timeout_seconds: 60
  max_retries: 0
  plain_mode: true

# Cache Configuration
cache:
  enabled: true
  directory: "/srv/cc/hana-x-infrastructure/.claude/agents/roger/cache/coderabbit"
  ttl_seconds: 3600  # 1 hour
  max_size_gb: 1
  purge_on_startup: false
  shard_levels: 2

# Rate Limit Configuration
rate_limit:
  enabled: true
  calls_per_hour: 900
  buffer_calls: 50
  warning_threshold: 720
  storage: "redis"
  redis_url: "redis://192.168.10.210:6379/0"
  fallback_file: "./cache/rate_limit.json"

# Categories
categories:
  - solid_violation
  - design_pattern
  - architecture

# Security
security:
  validate_file_paths: true
  allowed_extensions:
    - ".py"
    - ".pyi"
    - ".md"
    - ".yaml"
    - ".yml"
    - ".json"
  blocked_paths:
    - "/etc/"
    - "/var/"
    - "/root/"

# Logging
logging:
  level: "INFO"
  log_file: "./logs/layer3.log"
  log_api_calls: true
  log_cache_hits: false
EOF
```

**Verify configuration**:

```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('configs/layer3-coderabbit.yaml'))"
# Expected: No errors

# Verify permissions
chmod 644 configs/layer3-coderabbit.yaml
```

---

### Step 4: Validate Phase 3 Installation

**Run Phase 3 unit tests**:

```bash
# From Roger directory
cd /srv/cc/hana-x-infrastructure/.claude/agents/roger

# Run all tests (Phase 2 + Phase 3)
python -m pytest test_*.py -v

# Expected output: 47/47 tests PASSED (17 Phase 2 + 30 Phase 3)
```

**If tests fail**:

```bash
# Run Phase 2 tests only (verify no regressions)
python -m pytest test_roger.py -v
# Expected: 17/17 PASSED

# Run Phase 3 tests only (identify Phase 3 issues)
python -m pytest test_layer3.py -v
# Expected: 30/30 PASSED
```

---

### Step 5: Test Layer 3 Disabled (Backward Compatibility)

**Verify Roger still works with Layer 3 disabled**:

```bash
# Run Roger with Layer 3 disabled (default)
./bin/roger --path /srv/cc/hana-x-infrastructure/.claude/agents/roger

# Expected output:
# - Layer 1 analysis completes successfully
# - No Layer 3 calls made
# - Exit code 0 (or 1 if issues found, but no errors)

# Verify in output:
grep "Layer 3: disabled" DEFECT-LOG.md || echo "Layer 3 correctly disabled"
```

**This confirms Phase 2 functionality is preserved.**

---

### Step 6: Test Layer 3 Enabled (New Functionality)

**Enable Layer 3 and test**:

```bash
# Edit configuration to enable Layer 3
sed -i 's/enabled: false/enabled: true/' configs/layer3-coderabbit.yaml

# Run Roger with Layer 3 enabled
./bin/roger --path /srv/cc/hana-x-infrastructure/.claude/agents/roger --enable-layer3

# Expected output:
# - Layer 1 analysis completes
# - Layer 3 analysis completes
# - Cache statistics shown
# - Rate limit status shown
# - Findings deduplicated (Layer 1 precedence)

# Verify in output:
grep "Layer 3: enabled" DEFECT-LOG.md
grep "Cache hit rate:" DEFECT-LOG.md
grep "API calls:" DEFECT-LOG.md
```

**Verify cache created**:

```bash
# Check cache directory structure
ls -lh cache/coderabbit/
# Expected: metadata.json + 2-level directory sharding

# Check cache metadata
cat cache/coderabbit/metadata.json
# Expected: JSON with cache statistics
```

**Verify Redis rate limiting**:

```bash
# Check Redis for rate limit keys
redis-cli -h 192.168.10.210 KEYS "coderabbit:*"
# Expected: One or more keys for rate limit tracking

# Check rate limit count
redis-cli -h 192.168.10.210 GET "coderabbit:rate_limit:$(date +%Y%m%d%H)"
# Expected: Number <= 900
```

---

### Step 7: Validate Deduplication

**Test Layer 1 + Layer 3 deduplication**:

```bash
# Run Roger with both layers enabled on a test file
./bin/roger --path tests/test_file.py --enable-layer3 --format json > test_output.json

# Count findings by layer
jq '.findings | group_by(.source_layer) | map({layer: .[0].source_layer, count: length})' test_output.json

# Expected output:
# [
#   {"layer": "layer1", "count": X},
#   {"layer": "layer3", "count": Y}
# ]

# Verify no duplicate fingerprints
jq '.findings | map(.fingerprint) | group_by(.) | map(select(length > 1))' test_output.json
# Expected: [] (empty array - no duplicates)
```

---

## Configuration Migration Checklist

### Phase 2 Configuration (No Changes Needed)

The following Phase 2 configurations remain unchanged:

- ✅ `RogerConfig` dataclass (roger_orchestrator.py)
- ✅ Linter configurations (linter_aggregator.py)
- ✅ Defect logger settings (defect_logger.py)
- ✅ CLI wrapper options (bin/roger)

### New Phase 3 Configurations

The following new configurations are added:

- ✅ `configs/layer3-coderabbit.yaml` (create manually or deploy)
- ✅ Environment variable: `CODERABBIT_API_KEY` (must be set)
- ✅ Redis connection: `redis://192.168.10.210:6379/0` (verify accessible)
- ✅ Cache directory: `/srv/cc/hana-x-infrastructure/.claude/agents/roger/cache/coderabbit` (create with permissions)

---

## Testing Validation Procedures

### Validation Test Suite

Run the following tests to confirm successful migration:

**1. Phase 2 Regression Tests** (MUST PASS):

```bash
python -m pytest test_roger.py -v
# Expected: 17/17 PASSED
```

**2. Phase 3 Unit Tests** (MUST PASS):

```bash
python -m pytest test_layer3.py -v
# Expected: 30/30 PASSED
```

**3. Integration Tests** (MUST PASS):

```bash
# Test Layer 3 disabled (backward compatibility)
./bin/roger --path . > /tmp/test_layer1_only.log 2>&1
echo "Exit code: $?"

# Test Layer 3 enabled (new functionality)
./bin/roger --path . --enable-layer3 > /tmp/test_layer1_layer3.log 2>&1
echo "Exit code: $?"

# Compare outputs (Layer 3 should have additional findings)
wc -l /tmp/test_layer1_only.log /tmp/test_layer1_layer3.log
```

**4. Performance Tests** (SHOULD PASS):

```bash
# Measure execution time with Layer 3 enabled
time ./bin/roger --path . --enable-layer3

# Expected: <5 seconds with 90% cache hit rate
# Note: First run may be slower (cache miss)
```

**5. Cache Tests** (SHOULD PASS):

```bash
# Run twice to test cache hit
./bin/roger --path . --enable-layer3 > /dev/null 2>&1
time ./bin/roger --path . --enable-layer3 > /dev/null 2>&1

# Expected: Second run much faster (cache hits)

# Check cache hit rate
jq '.cache_stats.hit_rate' DEFECT-LOG.md
# Expected: >0.7 (70%+)
```

---

## Rollback Procedure

If Phase 3 migration fails or causes issues, follow this rollback procedure:

### Step 1: Restore Phase 2 Code

```bash
# From Roger directory
cd /srv/cc/hana-x-infrastructure/.claude/agents/roger

# Restore Phase 2 files from backup
cp backups/phase2-*/roger_orchestrator.py .
cp backups/phase2-*/layer3_stub.py .
cp backups/phase2-*/linter_aggregator.py .

# Verify Phase 2 tests pass
python -m pytest test_roger.py -v
# Expected: 17/17 PASSED
```

### Step 2: Remove Phase 3 Files (Optional)

```bash
# Remove Phase 3-specific files
rm -f layer3_coderabbit.py
rm -f coderabbit_client.py
rm -f coderabbit_cache.py
rm -f rate_limiter.py
rm -f test_layer3.py

# Remove configuration
rm -f configs/layer3-coderabbit.yaml

# Remove cache (optional - preserves cache for future retry)
# rm -rf cache/coderabbit/
```

### Step 3: Verify Phase 2 Operational

```bash
# Run Roger with Phase 2 only
./bin/roger --path .

# Expected: Clean execution, no Layer 3 errors
```

---

## Troubleshooting

### Issue: Tests Fail After Migration

**Symptoms**:
- `pytest test_layer3.py` fails
- ImportError or ModuleNotFoundError

**Diagnosis**:

```bash
# Check Python can import Phase 3 modules
python3 -c "from layer3_coderabbit import CodeRabbitLayer3; print('OK')"

# Check file permissions
ls -lh layer3_coderabbit.py coderabbit_client.py coderabbit_cache.py rate_limiter.py
```

**Solution**:

```bash
# Fix permissions if needed
chmod 644 *.py

# Verify Python path
echo $PYTHONPATH

# Re-run tests with verbose output
python -m pytest test_layer3.py -v -s
```

---

### Issue: CodeRabbit CLI Not Found

**Symptoms**:
- "CodeRabbit CLI not found" error
- API calls fail with PATH error

**Diagnosis**:

```bash
# Check if coderabbit is in PATH
which coderabbit

# Check configuration
grep "cli_path" configs/layer3-coderabbit.yaml
```

**Solution**:

```bash
# Option 1: Fix PATH
export PATH="/usr/local/bin:$PATH"

# Option 2: Update configuration with full path
sed -i 's|cli_path: "coderabbit"|cli_path: "/usr/local/bin/coderabbit"|' configs/layer3-coderabbit.yaml
```

---

### Issue: Redis Connection Failed

**Symptoms**:
- "Redis unavailable" warnings
- Fallback to file-based rate limiting

**Diagnosis**:

```bash
# Test Redis connection
redis-cli -h hx-redis-server.hx.dev.local ping
redis-cli -h 192.168.10.210 ping

# Check configuration
grep "redis_url" configs/layer3-coderabbit.yaml
```

**Solution**:

```bash
# Option 1: Fix Redis connection (check with Samuel Wilson)
# Contact: @agent-samuel

# Option 2: Use file-based fallback (temporary)
# Edit configuration:
sed -i 's/storage: "redis"/storage: "file"/' configs/layer3-coderabbit.yaml

# Note: File-based tracking is less reliable for concurrent access
```

---

### Issue: Cache Hit Rate Too Low (<70%)

**Symptoms**:
- Performance slower than expected
- Cache hit rate <70%

**Diagnosis**:

```bash
# Check cache statistics
cat cache/coderabbit/metadata.json

# Check cache directory size
du -sh cache/coderabbit/

# Check cache TTL
grep "ttl_seconds" configs/layer3-coderabbit.yaml
```

**Solution**:

```bash
# Option 1: Increase TTL (if files change infrequently)
sed -i 's/ttl_seconds: 3600/ttl_seconds: 7200/' configs/layer3-coderabbit.yaml

# Option 2: Pre-warm cache (run Roger multiple times)
for i in {1..3}; do
    ./bin/roger --path . --enable-layer3 > /dev/null 2>&1
    echo "Run $i complete"
done

# Option 3: Accept lower hit rate for dynamic codebases
# (70% target is for stable code, active development may be 50-60%)
```

---

## Post-Migration Validation

After successful migration, perform the following validations:

### Validation Checklist

- [ ] All 47 tests passing (17 Phase 2 + 30 Phase 3)
- [ ] Layer 3 disabled works (backward compatibility)
- [ ] Layer 3 enabled works (new functionality)
- [ ] Cache hit rate >70% after warm-up
- [ ] Redis rate limiting operational
- [ ] Performance <5 seconds with 90% cache hit
- [ ] No regressions in Phase 2 functionality
- [ ] Defect logs generated correctly
- [ ] JSON and text output formats work
- [ ] CLI flags (`--enable-layer3`) functional

### Sign-Off

**Migration Completed By**: _________________
**Date**: _________________
**Phase 2 Tests**: ___/17 PASSED
**Phase 3 Tests**: ___/30 PASSED
**Performance**: _____ seconds
**Cache Hit Rate**: _____%
**Issues Encountered**: _________________

---

## Appendix: Configuration Reference

### Phase 2 vs Phase 3 Configuration Comparison

| Setting | Phase 2 | Phase 3 | Notes |
|---------|---------|---------|-------|
| **Linter Aggregator** | ✅ Active | ✅ Active | No changes |
| **Layer 3 Integration** | ❌ Stub only | ✅ Full implementation | New capability |
| **Cache** | ❌ None | ✅ SHA256, 1-hour TTL | Performance optimization |
| **Rate Limiting** | ❌ None | ✅ 900/hour, Redis | API cost control |
| **Deduplication** | ✅ Basic | ✅ Layer 1 precedence | Enhanced logic |
| **Configuration File** | ❌ None | ✅ YAML-based | Centralized config |
| **Security Validation** | ❌ Basic | ✅ Path/extension checks | Enhanced security |

---

**Document Version**: 1.0
**Last Updated**: 2025-11-10
**Maintained By**: POC4 CodeRabbit Team

---

**END OF MIGRATION GUIDE**
