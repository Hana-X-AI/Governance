# CodeRabbit CLI Integration Guide

**Document Version**: 1.0  
**Last Updated**: November 7, 2025  
**Status**: Active  
**Related Documents**: [Development and Coding Standards](./development-and-coding-standards.md)

---

## Overview

CodeRabbit CLI is an AI-powered code review tool that integrates with Claude Code and other development environments. It automatically reviews code to catch bugs, security vulnerabilities, logic errors, and code quality issues before they reach production.

### Key Capabilities

- **Security Analysis**: Detects vulnerabilities and exposed secrets
- **Logic Error Detection**: Catches race conditions, memory leaks, and AI hallucinations
- **Code Quality**: Identifies code smells, performance bottlenecks, and missing tests
- **Error Handling**: Flags missing error handling and edge cases
- **Automated Reviews**: Runs in background during development workflows

---

## Installation

### Quick Install

Single command to install CodeRabbit CLI globally:

```bash
curl -fsSL https://cli.coderabbit.ai/install.sh | sh
```

### Verify Installation

```bash
# Check version
coderabbit --version

# View available commands
coderabbit --help
```

---

## Authentication

CodeRabbit requires authentication for full functionality:

1. **Create Account**: Visit [coderabbit.ai](https://coderabbit.ai) and sign up with your GitHub account

2. **Authenticate CLI**:
   ```bash
   coderabbit login
   ```
   This opens a browser window for authentication.

---

## Basic Usage

After installation, you can:

### Review Code Manually

```bash
coderabbit review --plain
```

Provides AI-optimized output that's easy to read and can be passed to Claude Code for fixes.

### Review Specific Changes

```bash
# Reviews staged and unstaged changes
coderabbit review --plain
```

---

## Integration with Claude Code

CodeRabbit integrates with Claude Code to enable autonomous review cycles:

### Workflow

1. Claude Code generates/modifies code
2. CodeRabbit runs in background to review (using `--prompt-only` flag)
3. Claude Code reads the review output
4. Claude Code automatically fixes issues found
5. Process repeats until code is clean

### What CodeRabbit Detects

- Security vulnerabilities and exposed secrets
- Race conditions and memory leaks
- Logic errors from AI hallucinations
- Missing error handling and edge cases
- Performance bottlenecks
- Missing tests and code coverage gaps
- Code smells and anti-patterns

---

## Project Configuration

### Step 1: Create Project Standards

Create a `claude.md` file in your project root to define coding standards:

```bash
# Navigate to your project
cd /path/to/your/project

# Create claude.md
touch claude.md
```

### Step 2: Define Review Standards

Add configuration to `claude.md`:

```markdown
# Code Review Standards

## Quality Principles

- Accuracy is paramount - correctness over speed
- Apply OOP principles: encapsulation, inheritance, polymorphism, abstraction
- Favor composition over inheritance
- Follow SOLID principles strictly

## Review Focus Areas

1. **Architecture**: Verify proper separation of concerns
2. **Error Handling**: All edge cases must be covered
3. **Testing**: Unit tests required for all business logic
4. **Security**: No vulnerabilities or exposed secrets
5. **Performance**: Identify bottlenecks and inefficiencies

## Code Standards

- Clear, descriptive naming (no abbreviations)
- Comprehensive documentation for all public interfaces
- Defensive programming - validate all inputs
- Proper exception handling with meaningful messages

## Iterative Process

- Review in small, logical chunks
- Fix one category of issues at a time
- Re-review after each fix iteration
```

---

## MCP Server Integration (Optional)

For deeper integration with Claude Code, configure the MCP server:

### Step 1: Create MCP Configuration

```bash
# Create .claude directory
mkdir -p .claude

# Create mcp.json configuration
cat > .claude/mcp.json << 'EOF'
{
  "mcpServers": {
    "coderabbitai": {
      "command": "npx",
      "args": ["coderabbitai-mcp@latest"],
      "env": {
        "GITHUB_PAT": "${GITHUB_PAT}"
      }
    }
  }
}
EOF
```

### Step 2: Set Up GitHub Token

```bash
# Create a GitHub Personal Access Token at:
# https://github.com/settings/tokens
# Required scopes: repo, read:org

# Export in your shell (add to ~/.bashrc or ~/.zshrc)
export GITHUB_PAT="ghp_your_token_here"
```

---

## Workflow Scripts

### Quality-Focused Review Script

Create reusable scripts for common workflows:

```bash
# Create scripts directory
mkdir -p .claude/scripts

# Create review script
cat > .claude/scripts/review.sh << 'EOF'
#!/bin/bash
# Quality-focused review script

echo "=== Starting CodeRabbit Review ==="
echo "Quality over speed - thorough analysis in progress..."

# Run review with full output
coderabbit review --plain > /tmp/coderabbit_review.txt

# Check if issues found
if [ -s /tmp/coderabbit_review.txt ]; then
    echo ""
    echo "=== Issues Found ==="
    cat /tmp/coderabbit_review.txt
    echo ""
    echo "=== Review complete. Address issues before proceeding. ==="
    exit 1
else
    echo "=== No issues found. Code meets quality standards. ==="
    exit 0
fi
EOF

chmod +x .claude/scripts/review.sh
```

### Iterative Review Workflow

```bash
cat > .claude/scripts/iterative-review.sh << 'EOF'
#!/bin/bash
# Iterative review and fix workflow

MAX_ITERATIONS=5
ITERATION=0

echo "=== Iterative Code Review Process ==="
echo "Quality-focused: Will iterate until code meets standards"
echo ""

while [ $ITERATION -lt $MAX_ITERATIONS ]; do
    ITERATION=$((ITERATION + 1))
    echo "--- Iteration $ITERATION of $MAX_ITERATIONS ---"
    
    # Run review in background
    coderabbit review --plain > /tmp/review_$ITERATION.txt 2>&1
    
    # Check if any issues found
    if ! grep -q "issue" /tmp/review_$ITERATION.txt; then
        echo "✓ No issues found. Code quality verified."
        exit 0
    fi
    
    echo "Issues found in iteration $ITERATION:"
    cat /tmp/review_$ITERATION.txt
    echo ""
    echo "Waiting for fixes before next iteration..."
    echo "Press Enter when ready for next review, or Ctrl+C to stop"
    read -r
done

echo "=== Max iterations reached. Manual review recommended. ==="
exit 1
EOF

chmod +x .claude/scripts/iterative-review.sh
```

---

## Usage Patterns

### Pattern 1: Manual Review Before Commit

```bash
# After making changes
git add .
coderabbit review --plain
# Fix issues, then commit
```

### Pattern 2: Background Review

```bash
# Start review in background
coderabbit review --plain > review.log 2>&1 &
echo $! > /tmp/coderabbit.pid

# Continue working...

# Check when ready
if ps -p $(cat /tmp/coderabbit.pid) > /dev/null; then
    echo "Review still running..."
else
    cat review.log
fi
```

### Pattern 3: Integrated with Claude Code

```bash
# Let Claude Code handle the workflow
# In Claude Code, say:
# "Review this code with CodeRabbit and fix all issues iteratively"
```

---

## Testing the Setup

Verify everything works:

```bash
# 1. Test basic review
echo "console.log('test')" > test.js
coderabbit review --plain

# 2. Test with staged changes
git add test.js
coderabbit review --plain

# 3. Clean up
rm test.js
```

---

## Next Steps

### For Hana-X Projects

1. **Project Type Configuration**: Adapt review standards for Python (agents, MCP servers) and TypeScript (Next.js frontend)
2. **Pre-commit Hooks**: Set up automatic review before every commit
3. **Quality Gates**: Configure minimum requirements:
   - 80% test coverage minimum
   - No high-severity security issues
   - All SOLID principle violations must be addressed
4. **CI/CD Integration**: Add CodeRabbit to GitHub Actions workflow
5. **Team Onboarding**: Train team on iterative review process

### Related Documents

- [Development and Coding Standards](./development-and-coding-standards.md) - Core coding standards that CodeRabbit will enforce
- [Agent Constitution](../../0.1-agents/hx-agent-constitution.md) - Agent development guidelines

---

**Questions or Issues?**  
Contact: Hana-X Development Team  
Last Reviewed: November 7, 2025