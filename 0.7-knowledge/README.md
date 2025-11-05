# Knowledge & Reference Documentation
**Purpose**: Platform architecture, decisions, and reference materials

## Contents

- `architecture-decisions.md` - ADRs (Architecture Decision Records)
- `technology-stack.md` - Complete technology stack reference
- `network-topology.md` - Network diagram and routing tables
- `security-model.md` - Development vs production security model
- `glossary.md` - Terms, acronyms, definitions

## Architecture Decision Records (ADRs)

Document significant architectural decisions:
- Context: Why this decision was needed
- Decision: What was decided
- Consequences: Impact and trade-offs
- Alternatives Considered: What else was evaluated
- Date and Author

## Technology Stack

Complete inventory of:
- Operating Systems (Ubuntu 24.04 LTS)
- Databases (PostgreSQL, Redis, Qdrant, MongoDB)
- LLM Infrastructure (Ollama, LiteLLM, Langchain)
- Container Platforms (Docker)
- Automation (Ansible, GitHub Actions)
- Monitoring (Prometheus, Grafana)
- Identity (FreeIPA, Samba AD)

## Usage

**Referenced for**:
- Onboarding new team members
- Understanding platform architecture
- Technology selection decisions
- Security compliance reviews
- Network troubleshooting

## Maintenance

Update when:
- Major architectural decisions made
- New technology adopted
- Network topology changes
- Security model updated
