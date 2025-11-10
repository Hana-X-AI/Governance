# CodeRabbit Fix: Database Username Inconsistency - n8n_user vs svc-n8n

**Document**: Multiple documents across planning, specification, and execution phases
**Date**: 2025-11-09
**Reviewer**: CodeRabbit AI + Agent Zero
**Type**: Configuration Drift / Naming Convention Inconsistency

---

## Issue: Inconsistent Database Username Across Project Artifacts

**Location**: Planning/Specification vs Execution/Validation phases
**Severity**: MEDIUM - Deployment Drift Risk / Documentation Inconsistency
**Category**: Configuration Management / Naming Standards

### Problem

**Two different database usernames used across project lifecycle**:

**Phase 1 & 2 (Planning/Specification): `n8n_user`**
- `p1-planning/agent-omar-planning-analysis.md`
- `p1-planning/agent-quinn-planning-analysis.md`
- `p1-planning/phase0-discovery.md`
- `p1-planning/phase2-collaborative-planning.md`
- `p1-planning/phase3-execution-plan.md`
- `p2-specification/poc3-n8n-deployment-specification.md`
- `p2-specification/review-william-infrastructure.md`
- `p2-specification/review-quinn-database.md`

**Phase 3, 4, 7 (Execution/Validation/Post-Deployment): `svc-n8n`**
- `p3-execution/PHASE3-COMPLETION-SUMMARY.md`
- `p4-validation/test-execution-report.md`
- `p4-validation/qa-sign-off.md`
- `p7-post-deployment/lessons-learned.md`
- `p7-post-deployment/operational-runbook.md`
- `p7-post-deployment/PROJECT-COMPLETION-SUMMARY.md`

### Analysis

**Timeline of Username Evolution**:

1. **Phase 1 (Planning)**: `n8n_user` established
   - Omar's analysis: `DB_POSTGRESDB_USER=n8n_user`
   - Quinn's analysis: Database user `n8n_user`
   - Phase 3 execution plan: `DB_POSTGRESDB_USER=n8n_user`

2. **Phase 2 (Specification)**: `n8n_user` confirmed
   - Specification: "user `n8n_user` having CREATE, SELECT, INSERT, UPDATE, DELETE privileges"
   - Quinn's review: "CREATE USER n8n_user WITH PASSWORD..."

3. **Phase 3 (Execution)**: Changed to `svc-n8n` without updating planning docs
   - Phase 3 summary: "Created dedicated PostgreSQL service account `svc-n8n`"
   - Rationale: "URL-safe credentials following LiteLLM pattern (`svc-litellm`)"
   - Password changed from `Major8859!` to `Major8859` (removed `!` for URL safety)

4. **Phase 4 (Validation)**: `svc-n8n` used in all tests
   - Test execution: `psql -U svc-n8n`
   - QA sign-off: "Database credentials secured (svc-n8n user...)"

5. **Phase 7 (Post-Deployment)**: `svc-n8n` documented as standard
   - Operational runbook: `DB_POSTGRESDB_USER=svc-n8n`
   - Lessons learned: "Account Name: `svc-{application}` (e.g., `svc-n8n`, `svc-litellm`)"

**Root Cause**:
- Planning phase established `n8n_user` as database username
- During execution (Phase 3), DEFECT-001 occurred: password with `!` character caused URL encoding issues
- Resolution: Created new service account `svc-n8n` with URL-safe password
- **Planning/specification documents never updated** to reflect this change

**Impact**:

1. **Documentation Drift**:
   - Planning says `n8n_user`
   - Reality uses `svc-n8n`
   - Creates confusion for future deployments

2. **Reproduction Risk**:
   - Following planning docs would create wrong database user
   - Would cause deployment failure (credentials mismatch)
   - Requires troubleshooting and rework

3. **Training/Onboarding Issues**:
   - New team members read planning docs
   - Expect `n8n_user` but actual system uses `svc-n8n`
   - Wastes time troubleshooting non-existent account

4. **Automation Failure**:
   - Automated deployments following specification would fail
   - Scripts using `n8n_user` would not connect
   - Requires manual intervention

---

## Resolution: Standardize on `svc-n8n`

### Rationale for Choosing `svc-n8n`

**Reasons to use `svc-n8n` (RECOMMENDED)**:

1. ✅ **Already deployed and operational** - Current production uses `svc-n8n`
2. ✅ **Follows naming convention** - Matches LiteLLM pattern (`svc-litellm`)
3. ✅ **URL-safe password** - `Major8859` without special characters
4. ✅ **Documented in lessons learned** - Established as organizational standard
5. ✅ **Post-deployment docs consistent** - Runbook, completion summary all use `svc-n8n`
6. ✅ **Service account pattern** - `svc-{application}` is clear, descriptive naming

**Reasons NOT to revert to `n8n_user`**:

1. ❌ Would require database account recreation
2. ❌ Would invalidate all test results
3. ❌ Would require updating production `.env` file
4. ❌ Would break operational runbook
5. ❌ Loses URL-safe password benefit
6. ❌ Breaks naming convention alignment with LiteLLM

**Decision**: Update planning/specification documents to use `svc-n8n`

---

## Required Changes by Document

### Phase 1: Planning Documents

#### 1. `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-omar-planning-analysis.md`

**Find and replace all instances**:

**Line 145** (and similar):
```bash
# BEFORE:
DB_POSTGRESDB_USER=n8n_user

# AFTER:
DB_POSTGRESDB_USER=svc-n8n
```

**Add clarification note** (after environment variables section):
```markdown
**Note on Database Username**: The specification originally referenced `n8n_user` but during
Phase 3 execution, this was changed to `svc-n8n` to follow organizational naming conventions
(`svc-{application}`) and use URL-safe credentials. All documentation has been updated to
reflect the deployed configuration.
```

#### 2. `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/agent-quinn-planning-analysis.md`

**Update user creation SQL**:

**BEFORE**:
```sql
CREATE USER n8n_user WITH PASSWORD 'Major8859!';
GRANT CONNECT ON DATABASE n8n_poc3 TO n8n_user;
COMMENT ON ROLE n8n_user IS 'n8n application database user - POC3';
```

**AFTER**:
```sql
CREATE USER svc-n8n WITH PASSWORD 'Major8859';  -- URL-safe password (no special chars)
GRANT CONNECT ON DATABASE n8n_poc3 TO svc-n8n;
COMMENT ON ROLE svc-n8n IS 'n8n application database service account - POC3';

-- Note: Username follows organizational convention: svc-{application}
-- Password is URL-safe (alphanumeric only) to prevent connection string encoding issues
```

**Update environment variable references**:
```bash
# BEFORE:
DB_POSTGRESDB_USER=n8n_user

# AFTER:
DB_POSTGRESDB_USER=svc-n8n
```

#### 3. `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/phase0-discovery.md`

**Update responsibility statement**:

**BEFORE**:
```markdown
- **Responsibility**: Create database `n8n_poc3`, user `n8n_user`, configure connection parameters
```

**AFTER**:
```markdown
- **Responsibility**: Create database `n8n_poc3`, user `svc-n8n` (service account), configure connection parameters
```

#### 4. `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/phase2-collaborative-planning.md`

**BEFORE**:
```markdown
- PostgreSQL database `n8n_poc3` created with `n8n_user`
```

**AFTER**:
```markdown
- PostgreSQL database `n8n_poc3` created with service account `svc-n8n`
```

#### 5. `/srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/phase3-execution-plan.md`

**Update all `.env` file examples**:

**BEFORE**:
```bash
DB_POSTGRESDB_USER=n8n_user
```

**AFTER**:
```bash
DB_POSTGRESDB_USER=svc-n8n
```

**Add note in database configuration section**:
```markdown
## Database Service Account

**Username**: `svc-n8n`
**Convention**: Service accounts follow `svc-{application}` pattern (e.g., `svc-litellm`, `svc-n8n`)
**Password**: URL-safe (alphanumeric only, no special characters)

**Rationale**: URL-safe passwords prevent connection string encoding issues common with special characters like `!`, `@`, `#` in PostgreSQL connection URLs.
```

---

### Phase 2: Specification Documents

#### 6. `/srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/poc3-n8n-deployment-specification.md`

**Find and replace**: `n8n_user` → `svc-n8n`

**Update acceptance criteria**:

**BEFORE**:
```markdown
**Given**: PostgreSQL database `n8n_poc3` created with user `n8n_user`
```

**AFTER**:
```markdown
**Given**: PostgreSQL database `n8n_poc3` created with service account `svc-n8n`
```

**Update database setup section**:

**BEFORE**:
```markdown
PostgreSQL ≥13.x, create database `n8n_poc3`, user `n8n_user` with CREATE, SELECT, INSERT, UPDATE, DELETE privileges
```

**AFTER**:
```markdown
PostgreSQL ≥13.x, create database `n8n_poc3`, service account `svc-n8n` (following `svc-{application}` naming convention) with CREATE, SELECT, INSERT, UPDATE, DELETE privileges
```

#### 7. `/srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/review-william-infrastructure.md`

**Update environment variable examples**:

**BEFORE**:
```bash
DB_POSTGRESDB_USER=n8n_user
```

**AFTER**:
```bash
DB_POSTGRESDB_USER=svc-n8n
```

#### 8. `/srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/review-quinn-database.md`

**Update all SQL commands** (extensive changes):

**BEFORE**:
```sql
CREATE USER n8n_user WITH PASSWORD 'Major8859!';
GRANT CONNECT ON DATABASE n8n_poc3 TO n8n_user;
GRANT CREATE ON DATABASE n8n_poc3 TO n8n_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO n8n_user;
```

**AFTER**:
```sql
CREATE USER svc-n8n WITH PASSWORD 'Major8859';  -- URL-safe password
GRANT CONNECT ON DATABASE n8n_poc3 TO svc-n8n;
GRANT CREATE ON DATABASE n8n_poc3 TO svc-n8n;
GRANT ALL PRIVILEGES ON SCHEMA public TO svc-n8n;

-- Service account naming convention: svc-{application}
-- URL-safe password prevents connection string encoding issues
```

**Update all psql command examples**:

**BEFORE**:
```bash
psql -h 192.168.10.209 -U n8n_user -d n8n_poc3 -c "\dt"
```

**AFTER**:
```bash
psql -h 192.168.10.209 -U svc-n8n -d n8n_poc3 -c "\dt"
```

**Update environment variable**:
```bash
# BEFORE:
DB_POSTGRESDB_USER=n8n_user

# AFTER:
DB_POSTGRESDB_USER=svc-n8n
```

---

## Global Search and Replace Strategy

### Automated Update Script

```bash
#!/bin/bash
# Update all POC3 documents to use svc-n8n instead of n8n_user

BASE_DIR="/srv/cc/Governance/x-poc3-n8n-deployment"

# Directories to update
DIRS=(
  "$BASE_DIR/p1-planning"
  "$BASE_DIR/p2-specification"
)

echo "=== POC3 Database Username Update ==="
echo "Updating: n8n_user → svc-n8n"
echo ""

# Find all markdown files
FILES=$(find "${DIRS[@]}" -type f -name "*.md")

for file in $FILES; do
    echo "Updating: $file"

    # Create backup
    cp "$file" "${file}.bak"

    # Replace n8n_user with svc-n8n (case-sensitive)
    sed -i 's/n8n_user/svc-n8n/g' "$file"

    # Update password (Major8859! → Major8859, URL-safe)
    # Only if password is in same context as username change
    sed -i "s/Major8859!/Major8859/g" "$file"

    echo "  ✅ Updated"
done

echo ""
echo "=== Update Complete ==="
echo "Total files updated: $(echo "$FILES" | wc -l)"
echo ""
echo "Review changes with: git diff"
echo "Restore backups if needed: find . -name '*.md.bak' -exec mv {} {}.bak {} \;"
```

### Verification After Update

```bash
#!/bin/bash
# Verify no n8n_user references remain in planning/spec phases

echo "=== Verification: Database Username Consistency ==="

# Should return 0 results
echo "Checking for remaining n8n_user references in planning/spec..."
PLANNING_REFS=$(grep -r "n8n_user" /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/ /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/ 2>/dev/null | wc -l)

if [ "$PLANNING_REFS" -eq 0 ]; then
    echo "✅ PASS - No n8n_user references in planning/specification"
else
    echo "❌ FAIL - Found $PLANNING_REFS references to n8n_user"
    grep -r "n8n_user" /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/ /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/ 2>/dev/null
fi

# Should return multiple results (execution/validation/post-deployment)
echo ""
echo "Checking for svc-n8n references (should exist)..."
SVC_REFS=$(grep -r "svc-n8n" /srv/cc/Governance/x-poc3-n8n-deployment/ 2>/dev/null | wc -l)

if [ "$SVC_REFS" -gt 40 ]; then
    echo "✅ PASS - Found $SVC_REFS svc-n8n references across project"
else
    echo "⚠️  WARNING - Only found $SVC_REFS svc-n8n references (expected >40)"
fi

echo ""
echo "=== Verification Complete ==="
```

---

## Documentation Standard Update

### Proposed Standard: Service Account Naming Convention

**Add to governance documentation**:

```markdown
## Database Service Account Naming Convention

**Standard**: All application database users must follow the service account pattern:

**Format**: `svc-{application}`

**Examples**:
- LiteLLM: `svc-litellm`
- N8N: `svc-n8n`
- Future apps: `svc-{app-name}`

**Rationale**:
1. **Clear identification**: Immediate recognition as service account
2. **Naming consistency**: Uniform pattern across all applications
3. **Security best practice**: Distinguishes service accounts from human users
4. **Audit trail**: Easy to identify service accounts in logs and permissions

**Password Requirements**:
- **URL-safe characters only**: Alphanumeric (a-z, A-Z, 0-9)
- **No special characters**: Avoid `!`, `@`, `#`, `$`, `%`, etc.
- **Minimum length**: 8 characters
- **Pattern**: `MajorXXXX` where XXXX is numeric

**Example**:
```sql
CREATE USER svc-n8n WITH PASSWORD 'Major8859';
```

**Prohibited**:
```sql
-- WRONG - Generic name
CREATE USER n8n_user WITH PASSWORD 'password123';

-- WRONG - Special characters in password
CREATE USER svc-n8n WITH PASSWORD 'Major8859!@#';
```

**Migration from Legacy Naming**:
- Existing `{app}_user` accounts should be renamed to `svc-{app}` during next maintenance window
- Document migration in release notes
- Update all connection strings and configurations
```

---

## Testing After Fix

### Test Suite: Username Consistency

```bash
#!/bin/bash
# Test suite for database username consistency

echo "=== Database Username Consistency Test Suite ==="

# Test 1: Planning docs use svc-n8n
echo "Test 1: Planning documents use svc-n8n"
PLANNING_CORRECT=$(grep -r "svc-n8n" /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/ 2>/dev/null | wc -l)
if [ "$PLANNING_CORRECT" -gt 0 ]; then
    echo "✅ PASS - Planning docs reference svc-n8n ($PLANNING_CORRECT occurrences)"
else
    echo "❌ FAIL - Planning docs do not reference svc-n8n"
fi

# Test 2: Specification docs use svc-n8n
echo "Test 2: Specification documents use svc-n8n"
SPEC_CORRECT=$(grep -r "svc-n8n" /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/ 2>/dev/null | wc -l)
if [ "$SPEC_CORRECT" -gt 0 ]; then
    echo "✅ PASS - Specification docs reference svc-n8n ($SPEC_CORRECT occurrences)"
else
    echo "❌ FAIL - Specification docs do not reference svc-n8n"
fi

# Test 3: No n8n_user in planning/spec
echo "Test 3: No n8n_user references in planning/specification"
LEGACY_REFS=$(grep -r "n8n_user" /srv/cc/Governance/x-poc3-n8n-deployment/p1-planning/ /srv/cc/Governance/x-poc3-n8n-deployment/p2-specification/ 2>/dev/null | wc -l)
if [ "$LEGACY_REFS" -eq 0 ]; then
    echo "✅ PASS - No legacy n8n_user references"
else
    echo "❌ FAIL - Found $LEGACY_REFS legacy n8n_user references"
fi

# Test 4: Execution docs use svc-n8n
echo "Test 4: Execution documents use svc-n8n"
EXEC_REFS=$(grep -r "svc-n8n" /srv/cc/Governance/x-poc3-n8n-deployment/p3-execution/ 2>/dev/null | wc -l)
if [ "$EXEC_REFS" -gt 0 ]; then
    echo "✅ PASS - Execution docs use svc-n8n ($EXEC_REFS occurrences)"
else
    echo "❌ FAIL - Execution docs do not use svc-n8n"
fi

# Test 5: Validation docs use svc-n8n
echo "Test 5: Validation documents use svc-n8n"
VAL_REFS=$(grep -r "svc-n8n" /srv/cc/Governance/x-poc3-n8n-deployment/p4-validation/ 2>/dev/null | wc -l)
if [ "$VAL_REFS" -gt 0 ]; then
    echo "✅ PASS - Validation docs use svc-n8n ($VAL_REFS occurrences)"
else
    echo "❌ FAIL - Validation docs do not use svc-n8n"
fi

echo ""
echo "=== Test Suite Complete ==="
```

---

## Summary of Required Changes

### Critical Fix: Update Planning/Specification Documents

**Files to Update** (8 files):
1. `p1-planning/agent-omar-planning-analysis.md`
2. `p1-planning/agent-quinn-planning-analysis.md`
3. `p1-planning/phase0-discovery.md`
4. `p1-planning/phase2-collaborative-planning.md`
5. `p1-planning/phase3-execution-plan.md`
6. `p2-specification/poc3-n8n-deployment-specification.md`
7. `p2-specification/review-william-infrastructure.md`
8. `p2-specification/review-quinn-database.md`

**Change Pattern**:
- Find: `n8n_user`
- Replace: `svc-n8n`
- Find: `Major8859!` (in database context)
- Replace: `Major8859`

**Add Clarification Note** (in each updated file):
```markdown
**Note**: Database username follows organizational service account naming convention:
`svc-{application}`. Originally specified as `n8n_user` during planning, updated to
`svc-n8n` during Phase 3 execution to align with LiteLLM precedent and use URL-safe credentials.
```

---

## Version History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2025-11-09 | Initial CodeRabbit remediation: Identified database username inconsistency (n8n_user in planning/spec vs svc-n8n in execution/validation), recommended updating all planning/specification documents to use svc-n8n for consistency with deployed configuration | Agent Zero + CodeRabbit AI |

---

**Status**: ✅ REMEDIATION DOCUMENTED
**Next Step**: Update 8 planning/specification documents to use svc-n8n
**Priority**: MEDIUM - Documentation drift (prevents future deployment issues)
**Coordination**: Quinn Baker (database owner) should review changes before application
