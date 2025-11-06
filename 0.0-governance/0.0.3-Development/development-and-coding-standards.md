# Hana-X Development and Coding Standards

**Version**: 1.0  
**Effective Date**: November 6, 2025  
**Scope**: All Hana-X development teams (Application, Infrastructure, Agent Development, MCP Servers)  
**Last Updated**: November 6, 2025

---

## 1. Introduction

### 1.1 Purpose

This document establishes development and coding standards for all Hana-X projects. These standards ensure:

- **Code Quality**: Maintainable, testable, and reliable software
- **Team Alignment**: Consistent practices across all teams
- **Technical Excellence**: Industry best practices and proven design patterns
- **Developer Productivity**: Clear guidelines that accelerate development
- **Long-term Sustainability**: Reduced technical debt and easier onboarding

### 1.2 Scope

These standards apply to:

- **Languages**: Python (FastAPI, Pydantic), TypeScript/JavaScript (Next.js, React)
- **Components**: Agent systems, MCP servers, APIs, frontend applications, infrastructure code
- **Teams**: All developers, architects, and technical leads working on Hana-X projects
- **Lifecycle**: Development, code review, testing, deployment, and maintenance

### 1.3 Authority

This document is maintained by the Hana-X Architecture and Governance team. Exceptions require approval from the technical lead and must be documented.

### 1.4 Related Documents

- [SOLID Principles Deep Dive Analysis](../WIP/news and notes/solid-principles-deep-dive-analysis.md)
- [Hana-X Project Scope](../0.1-hana_x_project_scope_final.md)
- [Hana-X Platform Nodes](../0.2-hana_x_platform_nodes_final.md)
- [Hana-X Ecosystem Architecture](../0.3-hana_x_ecosystem_architecture_final.md)

---

## 2. SOLID Principles

SOLID principles form the foundation of our object-oriented design approach. These five principles ensure code is maintainable, extensible, and testable.

### 2.1 Single Responsibility Principle (SRP)

**Rule**: A class should have one, and only one, reason to change.

**Application**: Each class serves one clear purpose. All methods and properties work toward the same goal.

#### Python Example

❌ **Bad Design** (Multiple Responsibilities):

```python
class OrdersReport:
    def get_orders_info(self, start_date, end_date):
        # BAD: Database access mixed with business logic
        orders = self.query_db_for_orders(start_date, end_date)
        return self.format(orders)
    
    def query_db_for_orders(self, start_date, end_date):
        # BAD: Direct DB access in report class
        return db.query("SELECT * FROM orders WHERE created_at BETWEEN ? AND ?", 
                       start_date, end_date)
    
    def format(self, orders):
        # BAD: Presentation logic in same class
        return f"<h1>Orders: {orders}</h1>"
```

✅ **Good Design** (Separated Responsibilities):

```python
from abc import ABC, abstractmethod
from typing import Protocol

class OutputFormatter(Protocol):
    """Interface for output formatting"""
    def format(self, data: dict) -> str: ...

class HTMLFormatter:
    """Single responsibility: HTML formatting"""
    def format(self, data: dict) -> str:
        return f"<h1>Orders: {data}</h1>"

class OrdersRepository:
    """Single responsibility: Data persistence"""
    def get_orders_with_date(self, start_date, end_date):
        return db.query("SELECT * FROM orders WHERE created_at BETWEEN ? AND ?",
                       start_date, end_date)

class OrdersReport:
    """Single responsibility: Orchestration"""
    def __init__(self, repository: OrdersRepository, formatter: OutputFormatter):
        self.repository = repository
        self.formatter = formatter
    
    def get_orders_info(self, start_date, end_date):
        orders = self.repository.get_orders_with_date(start_date, end_date)
        return self.formatter.format(orders)
```

#### TypeScript Example

❌ **Bad Design**:

```typescript
class OrdersReport {
  getOrdersInfo(startDate: Date, endDate: Date): string {
    const orders = this.queryDB(startDate, endDate);
    return this.format(orders);
  }
  
  private queryDB(startDate: Date, endDate: Date) {
    // BAD: Direct DB access
    return db.query("SELECT * FROM orders WHERE created_at BETWEEN ? AND ?", 
                    startDate, endDate);
  }
  
  private format(orders: any): string {
    // BAD: HTML formatting in same class
    return `<h1>Orders: ${orders}</h1>`;
  }
}
```

✅ **Good Design**:

```typescript
interface OutputFormatter {
  format(data: any): string;
}

class HTMLFormatter implements OutputFormatter {
  format(data: any): string {
    return `<h1>Orders: ${data}</h1>`;
  }
}

class OrdersRepository {
  getOrdersWithDate(startDate: Date, endDate: Date): Promise<any[]> {
    return db.query("SELECT * FROM orders WHERE created_at BETWEEN ? AND ?",
                    startDate, endDate);
  }
}

class OrdersReport {
  constructor(
    private repository: OrdersRepository,
    private formatter: OutputFormatter
  ) {}
  
  async getOrdersInfo(startDate: Date, endDate: Date): Promise<string> {
    const orders = await this.repository.getOrdersWithDate(startDate, endDate);
    return this.formatter.format(orders);
  }
}
```

#### Hana-X Applications

- ✅ Agent classes have single, clear responsibilities
- ✅ Separate API clients from business logic
- ✅ Keep data access separate from data transformation
- ✅ MCP servers separate protocol handling from tool implementation
- ❌ Don't mix authentication, data processing, and presentation in one class

### 2.2 Open-Closed Principle (OCP)

**Rule**: Entities should be open for extension, but closed for modification.

**Application**: Add new functionality by extending code, not by modifying existing code.

#### Python Example

❌ **Bad Design** (Modification Required):

```python
class CostManager:
    def calculate(self, shape):
        cost_per_unit = 1.5
        # BAD: Adding Square requires modifying this method
        if isinstance(shape, Rectangle):
            area = shape.width * shape.height
        elif isinstance(shape, Circle):
            area = shape.radius * shape.radius * 3.14159
        else:
            raise ValueError("Unknown shape")
        
        return cost_per_unit * area
```

✅ **Good Design** (Extension via Polymorphism):

```python
from abc import ABC, abstractmethod

class AreaInterface(ABC):
    """Contract for area calculation"""
    @abstractmethod
    def calculate_area(self) -> float:
        pass

class Rectangle(AreaInterface):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def calculate_area(self) -> float:
        return self.width * self.height

class Circle(AreaInterface):
    def __init__(self, radius: float):
        self.radius = radius
    
    def calculate_area(self) -> float:
        return self.radius * self.radius * 3.14159

class Square(AreaInterface):  # NEW: Add without modifying CostManager
    def __init__(self, side: float):
        self.side = side
    
    def calculate_area(self) -> float:
        return self.side * self.side

class CostManager:
    def calculate(self, shape: AreaInterface) -> float:
        cost_per_unit = 1.5
        return cost_per_unit * shape.calculate_area()
```

#### TypeScript Example

✅ **Good Design**:

```typescript
interface AreaInterface {
  calculateArea(): number;
}

class Rectangle implements AreaInterface {
  constructor(private width: number, private height: number) {}
  
  calculateArea(): number {
    return this.width * this.height;
  }
}

class Circle implements AreaInterface {
  constructor(private radius: number) {}
  
  calculateArea(): number {
    return this.radius * this.radius * Math.PI;
  }
}

class CostManager {
  calculate(shape: AreaInterface): number {
    const costPerUnit = 1.5;
    return costPerUnit * shape.calculateArea();
  }
}
```

#### Hana-X Applications

- ✅ Plugin architecture for MCP tools
- ✅ Strategy pattern for different LLM providers
- ✅ Extensible agent capabilities without core modifications
- ✅ Format handlers (Markdown, JSON, XML) as implementations of common interface
- ❌ Don't use `instanceof` or type checking to handle different types

### 2.3 Liskov Substitution Principle (LSP)

**Rule**: Subclass/derived class should be substitutable for their base/parent class.

**Application**: Derived classes must honor the contract of their base class.

#### Python Example

❌ **Bad Design** (Violates LSP):

```python
class VideoPlayer:
    def play(self, file: str):
        print(f"Playing {file}")

class AviVideoPlayer(VideoPlayer):
    def play(self, file: str):
        # BAD: Strengthens precondition
        if not file.endswith('.avi'):
            raise Exception("Only AVI files supported")
        print(f"Playing {file}")

# Problem: This breaks when substituting
def play_video(player: VideoPlayer, file: str):
    player.play(file)  # May fail with AviVideoPlayer!
```

✅ **Good Design** (Honors LSP):

```python
from abc import ABC, abstractmethod

class VideoPlayer(ABC):
    @abstractmethod
    def play(self, file: str) -> bool:
        """Returns True if playback started successfully"""
        pass
    
    @abstractmethod
    def can_play(self, file: str) -> bool:
        """Check if this player supports the file"""
        pass

class UniversalVideoPlayer(VideoPlayer):
    def can_play(self, file: str) -> bool:
        return file.endswith(('.mp4', '.avi', '.mkv'))
    
    def play(self, file: str) -> bool:
        if not self.can_play(file):
            return False
        print(f"Playing {file}")
        return True

class AviVideoPlayer(VideoPlayer):
    def can_play(self, file: str) -> bool:
        return file.endswith('.avi')
    
    def play(self, file: str) -> bool:
        if not self.can_play(file):
            return False
        print(f"Playing AVI {file}")
        return True

# Correct usage
def play_video(player: VideoPlayer, file: str):
    if player.can_play(file):
        player.play(file)
    else:
        print(f"Player cannot play {file}")
```

#### TypeScript Example

✅ **Good Design**:

```typescript
interface VideoPlayer {
  canPlay(file: string): boolean;
  play(file: string): boolean;
}

class UniversalVideoPlayer implements VideoPlayer {
  canPlay(file: string): boolean {
    return file.endsWith('.mp4') || file.endsWith('.avi') || file.endsWith('.mkv');
  }
  
  play(file: string): boolean {
    if (!this.canPlay(file)) return false;
    console.log(`Playing ${file}`);
    return true;
  }
}

class AviVideoPlayer implements VideoPlayer {
  canPlay(file: string): boolean {
    return file.endsWith('.avi');
  }
  
  play(file: string): boolean {
    if (!this.canPlay(file)) return false;
    console.log(`Playing AVI ${file}`);
    return true;
  }
}
```

#### Hana-X Applications

- ✅ All agent implementations must honor base agent contract
- ✅ MCP tool implementations must not change expected behavior
- ✅ Database adapters (Qdrant, Supabase, Redis) must be truly interchangeable
- ✅ LLM client implementations must have consistent interfaces
- ❌ Don't strengthen preconditions or weaken postconditions in subclasses

### 2.4 Interface Segregation Principle (ISP)

**Rule**: A client should not be forced to implement an interface that it doesn't use.

**Application**: Break large interfaces into smaller, more specific ones.

#### Python Example

❌ **Bad Design** (Fat Interface):

```python
from abc import ABC, abstractmethod

class WorkerInterface(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def sleep(self):
        pass

class HumanWorker(WorkerInterface):
    def work(self):
        print("Human working")
    
    def sleep(self):
        print("Human sleeping")

class RobotWorker(WorkerInterface):
    def work(self):
        print("Robot working")
    
    def sleep(self):
        # BAD: Forced to implement unused method
        pass  # Robots don't sleep!
```

✅ **Good Design** (Segregated Interfaces):

```python
from abc import ABC, abstractmethod

class WorkAbleInterface(ABC):
    @abstractmethod
    def work(self):
        pass

class SleepAbleInterface(ABC):
    @abstractmethod
    def sleep(self):
        pass

class HumanWorker(WorkAbleInterface, SleepAbleInterface):
    def work(self):
        print("Human working")
    
    def sleep(self):
        print("Human sleeping")

class RobotWorker(WorkAbleInterface):
    def work(self):
        print("Robot working")
    # No need to implement sleep()
```

#### TypeScript Example

✅ **Good Design**:

```typescript
interface WorkAble {
  work(): void;
}

interface SleepAble {
  sleep(): void;
}

class HumanWorker implements WorkAble, SleepAble {
  work(): void {
    console.log("Human working");
  }
  
  sleep(): void {
    console.log("Human sleeping");
  }
}

class RobotWorker implements WorkAble {
  work(): void {
    console.log("Robot working");
  }
  // No sleep() method needed
}
```

#### Hana-X Applications

- ✅ Separate MCP capabilities into focused interfaces (Readable, Writable, Callable)
- ✅ Agent capabilities should be composable traits
- ✅ Tool interfaces should be specific (SearchTool, CrawlTool, not GenericTool)
- ✅ API clients should split read/write/admin operations
- ❌ Don't create monolithic interfaces that force dummy implementations

### 2.5 Dependency Inversion Principle (DIP)

**Rule**: 
1. High-level modules should not depend on low-level modules. Both should depend on abstractions.
2. Abstractions should not depend on details. Details should depend on abstractions.

**Application**: Depend on interfaces/abstractions, not concrete implementations.

#### Python Example

❌ **Bad Design** (Depends on Concrete Class):

```python
class MySQLConnection:
    def connect(self):
        print("MySQL Connection")

class PasswordReminder:
    def __init__(self):
        # BAD: Hardcoded dependency on MySQL
        self.db_connection = MySQLConnection()
    
    def send_reminder(self, email: str):
        self.db_connection.connect()
        # Send reminder logic
```

✅ **Good Design** (Depends on Abstraction):

```python
from abc import ABC, abstractmethod

class ConnectionInterface(ABC):
    @abstractmethod
    def connect(self):
        pass

class MySQLConnection(ConnectionInterface):
    def connect(self):
        print("MySQL Connection")

class MongoDBConnection(ConnectionInterface):
    def connect(self):
        print("MongoDB Connection")

class PasswordReminder:
    def __init__(self, db_connection: ConnectionInterface):
        # GOOD: Depends on interface
        self.db_connection = db_connection
    
    def send_reminder(self, email: str):
        self.db_connection.connect()
        # Send reminder logic

# Usage with dependency injection
mysql_conn = MySQLConnection()
reminder = PasswordReminder(mysql_conn)

# Easy to swap implementations
mongo_conn = MongoDBConnection()
reminder2 = PasswordReminder(mongo_conn)
```

#### TypeScript Example

✅ **Good Design**:

```typescript
interface ConnectionInterface {
  connect(): Promise<void>;
}

class MySQLConnection implements ConnectionInterface {
  async connect(): Promise<void> {
    console.log("MySQL Connection");
  }
}

class MongoDBConnection implements ConnectionInterface {
  async connect(): Promise<void> {
    console.log("MongoDB Connection");
  }
}

class PasswordReminder {
  constructor(private dbConnection: ConnectionInterface) {}
  
  async sendReminder(email: string): Promise<void> {
    await this.dbConnection.connect();
    // Send reminder logic
  }
}

// Usage with dependency injection
const mysqlConn = new MySQLConnection();
const reminder = new PasswordReminder(mysqlConn);

// Easy to swap
const mongoConn = new MongoDBConnection();
const reminder2 = new PasswordReminder(mongoConn);
```

#### Hana-X Applications

- ✅ All agents should depend on interfaces for LLM clients
- ✅ MCP servers should depend on tool interfaces, not concrete tools
- ✅ Database access should be abstracted (repository pattern)
- ✅ API clients should be injected, not instantiated
- ❌ Don't instantiate concrete classes inside other classes

---

## 3. Documentation Standards

High-quality documentation is essential for team collaboration, knowledge transfer, and project sustainability.

### 3.1 Code Documentation

#### 3.1.1 Docstrings (Python)

**Required for**:
- All public classes
- All public functions/methods
- All modules

**Format**: Use Google-style docstrings

```python
def calculate_embedding(
    text: str,
    model: str = "text-embedding-3-small",
    dimensions: int = 1536
) -> list[float]:
    """
    Calculate embedding vector for given text.
    
    Args:
        text: Input text to embed
        model: OpenAI model name for embeddings
        dimensions: Target dimension count for embedding vector
    
    Returns:
        List of floats representing the embedding vector
    
    Raises:
        ValueError: If text is empty or dimensions invalid
        APIError: If OpenAI API call fails
    
    Example:
        >>> embedding = calculate_embedding("Hello world")
        >>> len(embedding)
        1536
    """
    if not text:
        raise ValueError("Text cannot be empty")
    # Implementation
```

#### 3.1.2 JSDoc (TypeScript)

**Required for**:
- All exported functions
- All public class methods
- All interfaces

**Format**: Use JSDoc standard

```typescript
/**
 * Calculate embedding vector for given text.
 * 
 * @param text - Input text to embed
 * @param model - OpenAI model name for embeddings
 * @param dimensions - Target dimension count for embedding vector
 * @returns Promise resolving to embedding vector
 * @throws {ValueError} If text is empty or dimensions invalid
 * @throws {APIError} If OpenAI API call fails
 * 
 * @example
 * ```typescript
 * const embedding = await calculateEmbedding("Hello world");
 * console.log(embedding.length); // 1536
 * ```
 */
export async function calculateEmbedding(
  text: string,
  model: string = "text-embedding-3-small",
  dimensions: number = 1536
): Promise<number[]> {
  if (!text) {
    throw new ValueError("Text cannot be empty");
  }
  // Implementation
}
```

#### 3.1.3 Inline Comments

**Use comments to explain WHY, not WHAT**:

```python
# ❌ Bad: Explains obvious what
# Increment counter by 1
counter += 1

# ✅ Good: Explains non-obvious why
# Cache invalidation requires +1 offset due to zero-indexing bug in Redis client
counter += 1
```

**When to comment**:
- ✅ Complex algorithms or business logic
- ✅ Non-obvious performance optimizations
- ✅ Workarounds for third-party library bugs
- ✅ Security-critical sections
- ❌ Self-explanatory code
- ❌ Redundant descriptions

### 3.2 Project Documentation

#### 3.2.1 README.md Requirements

Every repository must have a README.md with:

1. **Project Title and Description**
2. **Prerequisites** (Python version, Node version, system dependencies)
3. **Installation Instructions**
4. **Usage Examples**
5. **Configuration** (environment variables, config files)
6. **Architecture Overview** (high-level diagram or description)
7. **Testing Instructions**
8. **Contributing Guidelines** (link to CONTRIBUTING.md if extensive)
9. **License Information**

**Template**:

```markdown
# Project Name

Brief description of what this project does.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

## Installation

\`\`\`bash
# Clone repository
git clone https://github.com/Hana-X-AI/project-name.git

# Install dependencies
pip install -r requirements.txt
\`\`\`

## Configuration

Create a `.env` file:

\`\`\`bash
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
OPENAI_API_KEY=sk-...
\`\`\`

## Usage

\`\`\`python
from project_name import Agent

agent = Agent(name="my-agent")
result = agent.execute("task description")
\`\`\`

## Testing

\`\`\`bash
pytest tests/
\`\`\`

## License

MIT License - see LICENSE file for details
```

#### 3.2.2 CHANGELOG.md

Maintain a changelog using [Keep a Changelog](https://keepachangelog.com/) format:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New feature X

### Changed
- Modified behavior of Y

### Deprecated
- Feature Z will be removed in v2.0

### Removed
- Old API endpoint /v1/legacy

### Fixed
- Bug in authentication flow

### Security
- Patched XSS vulnerability in input validation

## [1.0.0] - 2025-11-06

### Added
- Initial release
```

### 3.3 Daily Stand-up Documentation

Stand-up documentation follows SOLID-inspired principles for clarity and maintainability.

#### 3.3.1 Stand-up Document Structure

**File naming**: `standup-YYYY-MM-DD.md`

**Location**: `docs/standups/` in each repository

**Format**:

```markdown
# Stand-up - November 6, 2025

**Team**: Agent Development  
**Attendees**: Alice, Bob, Carol  
**Facilitator**: Alice

---

## Alice (Senior Engineer)

### Yesterday
- Completed OpenAI client abstraction layer
- Fixed bug in embedding cache invalidation
- Reviewed PR #234 for MCP tool system

### Today
- Implement Anthropic client following same interface
- Add unit tests for LLM client factory
- Pair with Bob on agent orchestration

### Blockers
- None

---

## Bob (Mid-level Engineer)

### Yesterday
- Started agent orchestration refactor
- Updated documentation for tool system

### Today
- Continue orchestration work with Alice
- Add integration tests

### Blockers
- **BLOCKER**: Need clarification on state management approach
  - **Owner**: Carol
  - **Due**: EOD today

---

## Carol (Tech Lead)

### Yesterday
- Architecture review for state management
- Sprint planning preparation

### Today
- Resolve Bob's state management blocker
- Review Anthropic client PR when ready

### Blockers
- None

---

## Parking Lot

Items requiring separate discussion:

1. **Performance optimization strategy** - Schedule dedicated session
   - **Owner**: Alice
   - **Action**: Schedule 1-hour working session by Friday

2. **Database migration approach** - Needs architecture review
   - **Owner**: Carol
   - **Action**: Prepare RFC document by Monday

---

## Task Board

Link: [Jira Board](https://hana-x.atlassian.net/board/123)

**Sprint Progress**: 12/20 story points completed
```

#### 3.3.2 SOLID Principles Applied to Stand-up Documentation

| Principle | Application |
|-----------|-------------|
| **Single Responsibility** | Each entry focuses on one person's update. No mixing of project status, architecture decisions, or other topics. |
| **Open-Closed** | Historical entries are not modified. New entries added daily. Changes tracked separately if needed. |
| **Liskov Substitution** | All entries follow identical structure. Anyone can write in the same format regardless of role or team. |
| **Interface Segregation** | Different views for different audiences: summary for managers, detailed for engineers, blocker-only for unblocking team. |
| **Dependency Inversion** | Focus on tasks and dependencies between work items, not on specific individuals. Work continues if people are absent. |

#### 3.3.3 Asynchronous Stand-ups

For distributed teams:

1. **Update by EOD previous day** or **start of your workday**
2. **Review others' updates** within first hour of your day
3. **Comment on blockers** you can help unblock
4. **Use threading** in Slack/Teams for discussions

**Slack Integration Example**:

```
/standup-bot update
Yesterday: Completed API refactor
Today: Adding tests
Blockers: None
```

### 3.4 Architecture Decision Records (ADRs)

For significant architectural decisions, create ADRs in `docs/adr/`:

**Template** (`docs/adr/0001-use-qdrant-for-vector-storage.md`):

```markdown
# ADR 0001: Use Qdrant for Vector Storage

**Status**: Accepted  
**Date**: 2025-11-06  
**Deciders**: Carol (Tech Lead), Alice (Senior Engineer)  
**Consulted**: Bob (Engineer), Infrastructure Team

## Context

We need a vector database for storing agent memory and embeddings. Requirements:
- High-dimensional vector search (1536 dimensions)
- 100K+ vectors initially, scaling to 10M+
- Sub-100ms query latency
- Self-hosted option for data sovereignty

## Decision

We will use Qdrant as our primary vector database.

## Consequences

### Positive
- Excellent performance for our scale
- Rust-based, stable and fast
- Good Python client library
- Can self-host on our infrastructure
- Active community and development

### Negative
- Team needs to learn new technology
- Less mature than Pinecone (but sufficient for our needs)
- Self-hosting requires DevOps resources

### Neutral
- Need to implement backup/restore procedures
- Will need monitoring setup

## Alternatives Considered

### Pinecone
- **Pros**: Managed service, very mature
- **Cons**: Vendor lock-in, cost at scale, no self-hosting

### Weaviate
- **Pros**: Open source, feature-rich
- **Cons**: Higher resource requirements, complex setup

### PostgreSQL with pgvector
- **Pros**: Leverage existing PG knowledge
- **Cons**: Performance limitations at scale
```

---

## 4. Code Review Checklist

Use this checklist during all code reviews. Reviewers and authors should verify each applicable item.

### 4.1 SOLID Principles Compliance

- [ ] **Single Responsibility**: Each class/function has one clear purpose
- [ ] **Open-Closed**: New functionality added via extension, not modification
- [ ] **Liskov Substitution**: Subclasses honor parent contracts
- [ ] **Interface Segregation**: No fat interfaces forcing unused implementations
- [ ] **Dependency Inversion**: Depends on abstractions, not concrete implementations

### 4.2 Code Quality

- [ ] **Naming**: Clear, descriptive names (no `data`, `temp`, `x`, `foo`)
- [ ] **Function Length**: Functions under 50 lines (exceptions documented)
- [ ] **Complexity**: Cyclomatic complexity under 10 per function
- [ ] **DRY Principle**: No duplicated logic (extract to shared functions)
- [ ] **Magic Numbers**: No unexplained constants (use named constants)
- [ ] **Error Handling**: Appropriate try/catch blocks with specific exceptions
- [ ] **Type Hints**: All function signatures have type annotations (Python/TypeScript)

### 4.3 Documentation

- [ ] **Docstrings**: All public functions/classes documented
- [ ] **Inline Comments**: Complex logic explained with WHY, not WHAT
- [ ] **README Updated**: If API changes or new features added
- [ ] **CHANGELOG Updated**: Entry added for user-facing changes
- [ ] **ADR Created**: If architectural decision made

### 4.4 Testing

- [ ] **Unit Tests**: All new functions have unit tests
- [ ] **Test Coverage**: Minimum 80% code coverage for new code
- [ ] **Edge Cases**: Tests include boundary conditions and error cases
- [ ] **Integration Tests**: Added if multiple components interact
- [ ] **Tests Pass**: All tests passing in CI pipeline

### 4.5 Security

- [ ] **Input Validation**: All user inputs validated and sanitized
- [ ] **SQL Injection**: Using parameterized queries or ORM
- [ ] **XSS Prevention**: Output properly escaped
- [ ] **Secrets Management**: No hardcoded API keys, passwords, or tokens
- [ ] **Authentication**: Proper auth checks on protected endpoints
- [ ] **Authorization**: User permissions verified for sensitive operations

### 4.6 Performance

- [ ] **Database Queries**: No N+1 queries (use joins or eager loading)
- [ ] **Indexing**: Database indexes exist for queried fields
- [ ] **Caching**: Appropriate caching for expensive operations
- [ ] **Async Operations**: Long-running tasks are asynchronous
- [ ] **Resource Cleanup**: Files, connections, and resources properly closed

### 4.7 Dependencies

- [ ] **Dependency Injection**: Dependencies injected, not hardcoded
- [ ] **Version Pinning**: Package versions specified in requirements.txt/package.json
- [ ] **License Compatibility**: New dependencies have compatible licenses
- [ ] **Security Audit**: No known vulnerabilities (check with `pip audit` or `npm audit`)

### 4.8 Git Practices

- [ ] **Branch Naming**: Follows convention (`feature/`, `bugfix/`, `hotfix/`)
- [ ] **Commit Messages**: Clear, descriptive commit messages
- [ ] **Small PRs**: Pull request under 400 lines (exceptions documented)
- [ ] **Single Concern**: PR addresses one feature/bug, not multiple unrelated changes
- [ ] **Merge Conflicts**: Resolved correctly

### 4.9 Code Review Etiquette

**For Reviewers**:
- ✅ Be respectful and constructive
- ✅ Explain the "why" behind suggestions
- ✅ Distinguish between blocking issues and nitpicks
- ✅ Approve when requirements met, even if minor style differences exist
- ❌ Don't be pedantic about personal preferences

**For Authors**:
- ✅ Respond to all comments
- ✅ Ask for clarification if feedback unclear
- ✅ Accept feedback graciously
- ✅ Request re-review after making changes
- ❌ Don't take feedback personally

---

## 5. Testing Standards

Comprehensive testing ensures code quality, prevents regressions, and enables confident refactoring.

### 5.1 Testing Pyramid

Follow the testing pyramid approach:

```
         /\
        /  \        E2E Tests (5-10%)
       /____\       Few, high-value end-to-end tests
      /      \
     /        \     Integration Tests (20-30%)
    /__________\    Test component interactions
   /            \
  /              \  Unit Tests (60-70%)
 /________________\ Test individual functions/classes
```

### 5.2 Unit Testing

#### 5.2.1 Python Unit Tests (pytest)

**Requirements**:
- Minimum 80% code coverage for new code
- All public functions have unit tests
- Use descriptive test names

**Example**:

```python
import pytest
from unittest.mock import Mock, patch
from myapp.agents import Agent
from myapp.llm import LLMClient

class TestAgent:
    """Test suite for Agent class"""
    
    def test_agent_initialization_with_valid_params(self):
        """Agent should initialize with name and LLM client"""
        llm_client = Mock(spec=LLMClient)
        agent = Agent(name="test-agent", llm_client=llm_client)
        
        assert agent.name == "test-agent"
        assert agent.llm_client == llm_client
    
    def test_agent_initialization_raises_error_with_empty_name(self):
        """Agent should raise ValueError if name is empty"""
        llm_client = Mock(spec=LLMClient)
        
        with pytest.raises(ValueError, match="Name cannot be empty"):
            Agent(name="", llm_client=llm_client)
    
    @patch('myapp.agents.LLMClient')
    def test_agent_execute_calls_llm_client(self, mock_llm_class):
        """Agent.execute should call LLM client with correct params"""
        mock_llm = Mock()
        mock_llm.generate.return_value = "test response"
        mock_llm_class.return_value = mock_llm
        
        agent = Agent(name="test-agent", llm_client=mock_llm)
        result = agent.execute("test task")
        
        mock_llm.generate.assert_called_once_with("test task")
        assert result == "test response"
    
    def test_agent_handles_llm_api_error(self):
        """Agent should handle LLM API errors gracefully"""
        llm_client = Mock(spec=LLMClient)
        llm_client.generate.side_effect = APIError("Rate limit exceeded")
        
        agent = Agent(name="test-agent", llm_client=llm_client)
        
        with pytest.raises(APIError, match="Rate limit exceeded"):
            agent.execute("test task")
```

**Test Organization**:

```
tests/
├── unit/
│   ├── test_agents.py
│   ├── test_llm_client.py
│   └── test_tools.py
├── integration/
│   ├── test_agent_with_tools.py
│   └── test_mcp_server.py
├── e2e/
│   └── test_complete_workflow.py
├── conftest.py  # Shared fixtures
└── pytest.ini
```

**pytest.ini Configuration**:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --cov=myapp
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

#### 5.2.2 TypeScript Unit Tests (Jest/Vitest)

**Example**:

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { Agent } from '../src/agents';
import { LLMClient } from '../src/llm';

describe('Agent', () => {
  let mockLLMClient: LLMClient;
  
  beforeEach(() => {
    mockLLMClient = {
      generate: vi.fn(),
    } as any;
  });
  
  it('should initialize with name and LLM client', () => {
    const agent = new Agent('test-agent', mockLLMClient);
    
    expect(agent.name).toBe('test-agent');
    expect(agent.llmClient).toBe(mockLLMClient);
  });
  
  it('should throw error if name is empty', () => {
    expect(() => {
      new Agent('', mockLLMClient);
    }).toThrow('Name cannot be empty');
  });
  
  it('should call LLM client when executing task', async () => {
    (mockLLMClient.generate as any).mockResolvedValue('test response');
    
    const agent = new Agent('test-agent', mockLLMClient);
    const result = await agent.execute('test task');
    
    expect(mockLLMClient.generate).toHaveBeenCalledWith('test task');
    expect(result).toBe('test response');
  });
  
  it('should handle LLM API errors', async () => {
    (mockLLMClient.generate as any).mockRejectedValue(
      new Error('Rate limit exceeded')
    );
    
    const agent = new Agent('test-agent', mockLLMClient);
    
    await expect(agent.execute('test task')).rejects.toThrow('Rate limit exceeded');
  });
});
```

### 5.3 Integration Testing

**Purpose**: Test how multiple components work together

**Example** (Python with FastAPI):

```python
import pytest
from fastapi.testclient import TestClient
from myapp.main import app
from myapp.database import get_db
from myapp.llm import LLMClient

@pytest.fixture
def test_db():
    """Fixture providing test database"""
    # Setup test database
    db = create_test_database()
    yield db
    # Teardown
    db.close()

@pytest.fixture
def mock_llm_client():
    """Fixture providing mock LLM client"""
    client = Mock(spec=LLMClient)
    client.generate.return_value = "test response"
    return client

def test_agent_api_endpoint_with_valid_request(test_db, mock_llm_client):
    """Test complete flow through API endpoint"""
    app.dependency_overrides[get_db] = lambda: test_db
    app.dependency_overrides[LLMClient] = lambda: mock_llm_client
    
    client = TestClient(app)
    response = client.post(
        "/api/v1/agents/execute",
        json={"agent_name": "test-agent", "task": "test task"}
    )
    
    assert response.status_code == 200
    assert response.json()["result"] == "test response"
```

### 5.4 End-to-End Testing

**Purpose**: Test complete user workflows

**Example** (Playwright for frontend):

```typescript
import { test, expect } from '@playwright/test';

test.describe('Agent Workflow', () => {
  test('user can create and execute agent', async ({ page }) => {
    // Navigate to agent creation page
    await page.goto('/agents/create');
    
    // Fill in agent details
    await page.fill('[data-testid="agent-name"]', 'My Test Agent');
    await page.selectOption('[data-testid="llm-provider"]', 'openai');
    await page.click('[data-testid="create-button"]');
    
    // Verify agent created
    await expect(page.locator('[data-testid="success-message"]'))
      .toContainText('Agent created successfully');
    
    // Execute agent task
    await page.fill('[data-testid="task-input"]', 'Summarize this text');
    await page.click('[data-testid="execute-button"]');
    
    // Verify result displayed
    await expect(page.locator('[data-testid="result-output"]'))
      .toBeVisible();
  });
});
```

### 5.5 Test Coverage Requirements

| Component Type | Minimum Coverage | Target Coverage |
|----------------|------------------|-----------------|
| Core Business Logic | 90% | 95% |
| API Endpoints | 80% | 90% |
| Utilities | 80% | 90% |
| UI Components | 70% | 80% |
| Overall Project | 80% | 85% |

### 5.6 Mocking and Fixtures

**When to Mock**:
- ✅ External API calls (OpenAI, Anthropic, etc.)
- ✅ Database queries in unit tests
- ✅ File system operations
- ✅ Time-dependent functions
- ✅ Expensive computations

**When NOT to Mock**:
- ❌ Pure functions (just test them directly)
- ❌ Simple utilities
- ❌ In integration tests (use real dependencies)

**Example Fixtures** (pytest):

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_openai_client():
    """Mock OpenAI client for testing"""
    client = Mock()
    client.embeddings.create.return_value = Mock(
        data=[Mock(embedding=[0.1] * 1536)]
    )
    return client

@pytest.fixture
def sample_agent_config():
    """Sample agent configuration"""
    return {
        "name": "test-agent",
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000
    }
```

### 5.7 Test Data Management

**Principles**:
- Use factories for creating test data
- Keep test data minimal and focused
- Use realistic data patterns
- Don't share mutable state between tests

**Example** (Factory Pattern):

```python
# tests/factories.py
from dataclasses import dataclass

@dataclass
class AgentFactory:
    """Factory for creating test agents"""
    
    @staticmethod
    def create(
        name: str = "test-agent",
        model: str = "gpt-4",
        temperature: float = 0.7
    ):
        return Agent(
            name=name,
            llm_client=Mock(spec=LLMClient),
            config={"model": model, "temperature": temperature}
        )

# Usage in tests
def test_agent_with_custom_temperature():
    agent = AgentFactory.create(temperature=0.9)
    assert agent.config["temperature"] == 0.9
```

### 5.8 Continuous Integration

**CI Pipeline Requirements**:
1. Run all tests on every pull request
2. Fail PR if coverage drops below threshold
3. Run linters (pylint, eslint) before tests
4. Run security checks (bandit, npm audit)
5. Generate coverage reports

**GitHub Actions Example** (`.github/workflows/test.yml`):

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linters
        run: |
          pylint myapp/
          black --check myapp/
      
      - name: Run tests with coverage
        run: |
          pytest --cov=myapp --cov-report=xml --cov-fail-under=80
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## 6. Language-Specific Standards

### 6.1 Python Standards

#### 6.1.1 Style Guide

Follow [PEP 8](https://pep8.org/) with these specific rules:

- **Line Length**: 100 characters (not 79)
- **Imports**: Use absolute imports, group by stdlib, third-party, local
- **Naming**:
  - Classes: `PascalCase`
  - Functions/Variables: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`
  - Private: `_leading_underscore`

#### 6.1.2 Type Hints

**Required**: Type hints on all function signatures

```python
from typing import List, Dict, Optional

def process_embeddings(
    texts: List[str],
    model: str = "text-embedding-3-small",
    batch_size: int = 100
) -> Dict[str, List[float]]:
    """Process texts into embeddings"""
    pass
```

#### 6.1.3 Error Handling

```python
# ✅ Good: Specific exceptions
try:
    result = llm_client.generate(prompt)
except RateLimitError:
    # Handle rate limiting
    time.sleep(60)
    result = llm_client.generate(prompt)
except APIError as e:
    logger.error(f"API error: {e}")
    raise

# ❌ Bad: Bare except
try:
    result = llm_client.generate(prompt)
except:  # Don't do this!
    pass
```

#### 6.1.4 Async/Await

Use `async`/`await` for I/O-bound operations:

```python
import asyncio
from typing import List

async def fetch_embeddings(texts: List[str]) -> List[List[float]]:
    """Fetch embeddings concurrently"""
    tasks = [llm_client.embed(text) for text in texts]
    return await asyncio.gather(*tasks)
```

### 6.2 TypeScript/JavaScript Standards

#### 6.2.1 Style Guide

Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)

- **Use TypeScript** for all new code
- **Strict mode**: Enable `strict: true` in tsconfig.json
- **No `any`**: Avoid `any` type, use `unknown` if necessary

#### 6.2.2 Type Definitions

```typescript
// ✅ Good: Proper types
interface AgentConfig {
  name: string;
  model: string;
  temperature: number;
  maxTokens?: number;  // Optional
}

function createAgent(config: AgentConfig): Agent {
  // Implementation
}

// ❌ Bad: Using any
function createAgent(config: any): any {
  // Don't do this!
}
```

#### 6.2.3 Async/Await

Always use `async`/`await`, not Promise chains:

```typescript
// ✅ Good: async/await
async function fetchData(): Promise<Data> {
  try {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
  } catch (error) {
    logger.error('Failed to fetch data', error);
    throw error;
  }
}

// ❌ Bad: Promise chains
function fetchData(): Promise<Data> {
  return fetch('/api/data')
    .then(response => response.json())
    .then(data => data)
    .catch(error => {
      logger.error('Failed to fetch data', error);
      throw error;
    });
}
```

#### 6.2.4 React Components

```typescript
// ✅ Good: Functional component with TypeScript
interface AgentCardProps {
  agent: Agent;
  onSelect: (agent: Agent) => void;
}

export const AgentCard: React.FC<AgentCardProps> = ({ agent, onSelect }) => {
  const handleClick = () => {
    onSelect(agent);
  };
  
  return (
    <div className="agent-card" onClick={handleClick}>
      <h3>{agent.name}</h3>
      <p>{agent.description}</p>
    </div>
  );
};
```

---

## 7. Version Control Standards

### 7.1 Branch Naming

**Convention**: `<type>/<ticket-number>-<short-description>`

**Types**:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Urgent production fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions or updates

**Examples**:
- `feature/HX-123-add-anthropic-client`
- `bugfix/HX-456-fix-embedding-cache`
- `hotfix/HX-789-patch-auth-vulnerability`

### 7.2 Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

**Format**: `<type>(<scope>): <subject>`

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting, missing semicolons)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Build process, dependencies

**Examples**:
```
feat(agent): add support for Anthropic Claude
fix(embedding): correct cache invalidation logic
docs(readme): update installation instructions
refactor(llm): extract common interface for providers
test(agent): add unit tests for execute method
```

### 7.3 Pull Request Guidelines

**PR Title**: Same format as commit message

**PR Description Template**:

```markdown
## Description
Brief description of changes

## Related Ticket
HX-123

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings
- [ ] Tests pass locally
- [ ] Coverage maintained/improved

## Screenshots (if applicable)
```

---

## 8. Enforcement and Adoption

### 8.1 Tooling

**Python**:
- **Linter**: `pylint` with custom config
- **Formatter**: `black`
- **Type Checker**: `mypy`
- **Security**: `bandit`

**TypeScript**:
- **Linter**: `eslint` with Airbnb config
- **Formatter**: `prettier`
- **Type Checker**: Built into TypeScript

### 8.2 Pre-commit Hooks

Install pre-commit hooks to enforce standards:

```bash
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.10.0
    hooks:
      - id: black
  
  - repo: https://github.com/pycqa/pylint
    rev: v3.0.0
    hooks:
      - id: pylint
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.6.0
    hooks:
      - id: mypy
```

### 8.3 Gradual Adoption

**Phase 1** (Immediate):
- All new code follows these standards
- Code reviews enforce checklist

**Phase 2** (Month 1-2):
- Refactor critical paths to meet standards
- Add tests to untested code

**Phase 3** (Month 3-6):
- Systematically refactor legacy code
- Achieve target test coverage

### 8.4 Exceptions

Exceptions to these standards require:
1. Technical lead approval
2. Documentation in code comments explaining why
3. Tracking in technical debt backlog

---

## 9. Resources

### 9.1 Reference Documents

- [SOLID Principles Deep Dive Analysis](../../WIP/news and notes/solid-principles-deep-dive-analysis.md)
- [Hana-X Architecture](../0.2-hana_x_platform_nodes_final.md)
- [Agent Constitution](../../0.1-agents/hx-agent-constitution.md)

### 9.2 External Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Clean Code by Robert C. Martin](https://www.amazon.com/Clean-Code-Handbook-Software-Craftsmanship/dp/0132350882)

### 9.3 Tools

- **Python**: pytest, black, pylint, mypy, bandit
- **TypeScript**: vitest, prettier, eslint, typescript
- **Git**: pre-commit, commitlint
- **CI/CD**: GitHub Actions, codecov

---

## 10. Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-06 | GitHub Copilot | Initial release - comprehensive development standards |

---

**Questions or Suggestions?**  
Contact: Hana-X Architecture Team  
Last Reviewed: November 6, 2025
