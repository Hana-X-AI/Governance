# Defect Log - POC4 Test Project

**Generated**: 2025-11-10 20:04:48
**Analyzed Files**: 5
**Total Defects**: 24

---

## Summary

| Priority | Count |
|----------|-------|
| P0 (Critical) | 0 |
| P1 (High) | 9 |
| P2 (Medium) | 15 |
| P3 (Low) | 0 |
| P4 (Info) | 0 |

---

## Defects

### DEF-0001: Possible SQL injection vector through string-based query construction. [Priority.HIGH]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/test_sample.py:26`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/plugins/b608_hardcoded_sql_expressions.html
- **Fix**: Possible SQL injection
- **Fingerprint**: `7739ac654335f195`

---

### DEF-0002: Use of unsafe yaml load. Allows instantiation of arbitrary objects. Consider yaml.safe_load(). [Priority.HIGH]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/test_sample.py:29`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/plugins/b506_yaml_load.html
- **Fix**: Avoid yaml.load(), use yaml.safe_load()
- **Fingerprint**: `bdccac0e77dcc09f`

---

### DEF-0003: Test coverage is 60.0% (target: ≥80%) [Priority.HIGH]

- **File**: `Overall:None`
- **Category**: Category.TESTING
- **Source**: pytest (layer1)
- **Details**: Missing coverage: 40.0%
- **Fix**: Add unit tests for uncovered code
- **Fingerprint**: `7429d700f5b3963d`

---

### DEF-0004: Unused import os [Priority.HIGH]

- **File**: `test_sample.py:14`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: unused-import (W0611)
- **Fix**: None
- **Fingerprint**: `7785cb95ae857731`

---

### DEF-0005: Unused import pickle [Priority.HIGH]

- **File**: `test_sample.py:15`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: unused-import (W0611)
- **Fix**: None
- **Fingerprint**: `4155a37d5c5f5e19`

---

### DEF-0006: Using open without explicitly specifying an encoding [Priority.HIGH]

- **File**: `test_sample.py:29`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: unspecified-encoding (W1514)
- **Fix**: None
- **Fingerprint**: `7986f6da28959f65`

---

### DEF-0007: Unused variable 'config' [Priority.HIGH]

- **File**: `test_sample.py:29`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: unused-variable (W0612)
- **Fix**: None
- **Fingerprint**: `61c9f6b84adc6166`

---

### DEF-0008: Unused variable 'another_unused' [Priority.HIGH]

- **File**: `test_sample.py:75`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: unused-variable (W0612)
- **Fix**: None
- **Fingerprint**: `afd7cd6458ff6e8e`

---

### DEF-0009: Unnecessary pass statement [Priority.HIGH]

- **File**: `test_sample.py:85`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: unnecessary-pass (W0107)
- **Fix**: None
- **Fingerprint**: `51fdfae7e0e8127b`

---

### DEF-0010: Consider possible security implications associated with pickle module. [Priority.MEDIUM]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/test_sample.py:15`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/blacklists/blacklist_imports.html#b403-import-pickle
- **Fix**: Consider implications of importing pickle
- **Fingerprint**: `255d1eb0cba50834`

---

### DEF-0011: Possible hardcoded password: 'hardcoded_password_123' [Priority.MEDIUM]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/test_sample.py:19`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/plugins/b105_hardcoded_password_string.html
- **Fix**: Use secrets module or environment variables instead of hardcoded passwords
- **Fingerprint**: `60bf91912874c27a`

---

### DEF-0012: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. [Priority.MEDIUM]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/tests/test_basic.py:19`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/plugins/b101_assert_used.html
- **Fix**: Review security best practices for this issue
- **Fingerprint**: `dff643d0749fe885`

---

### DEF-0013: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. [Priority.MEDIUM]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/tests/test_basic.py:20`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/plugins/b101_assert_used.html
- **Fix**: Review security best practices for this issue
- **Fingerprint**: `06bf02d98175ab51`

---

### DEF-0014: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. [Priority.MEDIUM]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/tests/test_basic.py:25`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/plugins/b101_assert_used.html
- **Fix**: Review security best practices for this issue
- **Fingerprint**: `4d4657dcf63ec953`

---

### DEF-0015: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. [Priority.MEDIUM]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/tests/test_basic.py:26`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/plugins/b101_assert_used.html
- **Fix**: Review security best practices for this issue
- **Fingerprint**: `b15168697f6c6d0e`

---

### DEF-0016: Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. [Priority.MEDIUM]

- **File**: `/srv/cc/Governance/x-poc4-coderabbit/0.3-Testing/test-project/tests/test_basic.py:32`
- **Category**: Category.SECURITY
- **Source**: bandit (layer1)
- **Details**: https://bandit.readthedocs.io/en/1.8.6/plugins/b101_assert_used.html
- **Fix**: Review security best practices for this issue
- **Fingerprint**: `4995b87546f3d789`

---

### DEF-0017: Consider using 'with' for resource-allocating operations [Priority.MEDIUM]

- **File**: `test_sample.py:29`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: consider-using-with (R1732)
- **Fix**: None
- **Fingerprint**: `9079ca83f4ea93df`

---

### DEF-0018: Too many arguments (7/5) [Priority.MEDIUM]

- **File**: `test_sample.py:34`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: too-many-arguments (R0913)
- **Fix**: None
- **Fingerprint**: `29a1828840db1297`

---

### DEF-0019: Too many positional arguments (7/5) [Priority.MEDIUM]

- **File**: `test_sample.py:34`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: too-many-positional-arguments (R0917)
- **Fix**: None
- **Fingerprint**: `394d43dd1baf22f1`

---

### DEF-0020: Too many branches (14/12) [Priority.MEDIUM]

- **File**: `test_sample.py:34`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: too-many-branches (R0912)
- **Fix**: None
- **Fingerprint**: `9756a501912b7925`

---

### DEF-0021: Too many nested blocks (7/5) [Priority.MEDIUM]

- **File**: `test_sample.py:41`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: too-many-nested-blocks (R1702)
- **Fix**: None
- **Fingerprint**: `84091c4154b3e027`

---

### DEF-0022: Method name "BadMethodName" doesn't conform to snake_case naming style [Priority.MEDIUM]

- **File**: `test_sample.py:83`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: invalid-name (C0103)
- **Fix**: None
- **Fingerprint**: `5edb44708f19bbc1`

---

### DEF-0023: Missing function or method docstring [Priority.MEDIUM]

- **File**: `test_sample.py:87`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: missing-function-docstring (C0116)
- **Fix**: None
- **Fingerprint**: `4b68fa0bf6d01c2f`

---

### DEF-0024: Import "from test_sample import missing_types, divide, complex_function" should be placed at the top of the module [Priority.MEDIUM]

- **File**: `tests/test_basic.py:14`
- **Category**: Category.QUALITY
- **Source**: pylint (layer1)
- **Details**: wrong-import-position (C0413)
- **Fix**: None
- **Fingerprint**: `4dcbcd12cee92ebf`

---

