# Introduction

> AI coding tools let you ship 10x faster, but code reviews still take days. CodeRabbit solves the AI coding bottleneck with context-aware reviews that learn from your team's preferences.

This page provides a conceptual introduction to CodeRabbit. For hands-on setup, see [Quickstart](/getting-started/quickstart/).

AI coding tools like Cursor and Claude Code let you write code 10x faster. But code reviews still happen manually. Senior engineers spend days reviewing AI-generated PRs. The queue backs up. Teams get stuck.

CodeRabbit solves this AI coding bottleneck with context-aware reviews that actually understand your codebase - not just the code you changed, but how it connects to your architecture, follows your patterns, and affects downstream dependencies.

<iframe width="100%" height="400" src="https://www.youtube.com/embed/3SyUOSebG7E?si=i0oT9RAnH0PW81lY" title="CodeRabbit AI code review demonstration" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerPolicy="strict-origin-when-cross-origin" allowFullScreen />

## Core capabilities

CodeRabbit delivers human-like reviews through three core capabilities:

### 1. Easier to review pull requests

Skip the diff diving. Get context fast.

<CardGroup cols={2}>
  <Card title="Summary" icon="file-text">
    AI-generated summary of what changed and why it matters to your system
    architecture.
  </Card>

  <Card title="Walkthrough" icon="list">
    File-by-file breakdown showing exactly what each change does.
  </Card>

  <Card title="Diagram" icon="workflow">
    Visual flow diagram showing how changes affect your system architecture.
  </Card>

  <Card title="Chat to learn" icon="messages-square">
    Ask CodeRabbit questions about the changes in natural language.
  </Card>
</CardGroup>

### 2. Context-aware code analysis

Reviews code like a senior dev who knows your entire codebase.

<CardGroup cols={1}>
  <Card title="CodeRabbit learns from every interaction" icon="graduation-cap" color="#FF570A">
    Tell CodeRabbit you prefer 2-space indentation over 4-space, or want more
    focus on security. It remembers and applies these preferences across all
    future reviews in your repository. **Example**: When CodeRabbit suggests
    4-space indentation but your team uses 2-space, reply in the PR comment.
    CodeRabbit acknowledges the feedback and adjusts all subsequent reviews
    accordingly. [See how learning works
    →](https://www.youtube.com/watch?v=Yu0cmmOYA-U)
  </Card>
</CardGroup>

<CardGroup cols={2}>
  <Card title="Code guidelines" icon="scan-text">
    Automatically detects and applies your team's coding standards and patterns.
  </Card>

  <Card title="Code graph" icon="git-branch">
    Maps dependencies and downstream effects of your changes across the
    codebase.
  </Card>
</CardGroup>

<CardGroup cols={3}>
  <Card title="Sandbox" icon="flask-conical">
    Creates ephemeral environments for code exploration.
  </Card>

  <Card title="40+ linters" icon="settings">
    Runs industry-standard analyzers and synthesizes results into actionable
    feedback.
  </Card>

  <Card title="Web search" icon="search">
    Fetches up-to-date information about libraries and frameworks in your code.
  </Card>

  <Card title="AI code reviews" icon="bot">
    Catches race conditions, security holes, and architectural drift that
    pattern matching misses.
  </Card>

  <Card title="Code suggestions" icon="lightbulb">
    Provides committable fixes you can apply with one click.
  </Card>

  <Card title="Linked issues" icon="link-2">
    Verifies that PR changes actually address the linked issues.
  </Card>
</CardGroup>

<Tip>
  **Free for public repositories**: Get full Pro tier features at no cost for
  open source projects. Rate limits may apply.
</Tip>

### 3. Automatic finishing touches

Handle the polish that makes code professional.

<CardGroup cols={2}>
  <Card title="Unit tests" icon="test-tube">
    Generate comprehensive tests covering edge cases with one click.
  </Card>

  <Card title="Docstrings" icon="file-text">
    Write clear documentation for functions and complex logic automatically.
  </Card>
</CardGroup>

## Embedded in your pull requests

CodeRabbit reviews happen where you already work - as comments on your PRs. Each review considers the full context of your codebase, not just the changed files.

Every review runs your changes through 40+ industry-standard tools - linters, security analyzers, performance checkers. CodeRabbit synthesizes all this into human-readable feedback that highlights what actually matters.

Chat with CodeRabbit directly in PR comments. Ask questions, provide context, or give feedback on its review style. CodeRabbit learns from every interaction and applies your preferences to future reviews.

<Accordion title="Advanced configuration options">
  Beyond chat learning, you can:

  * [Add configuration files](/getting-started/configure-coderabbit) for repository-wide settings
  * Set [path-based instructions](/guides/review-instructions) for how different parts of your codebase should be reviewed
  * Customize review focus areas through the CodeRabbit web interface

  CodeRabbit works out of the box with sensible defaults, delivering meaningful reviews within minutes of setup.
</Accordion>

### Supports major Git platforms

Integration takes minutes across popular platforms:

<CardGroup cols={2}>
  <Card title="GitHub" icon="github" href="/platforms/github-com">
    GitHub, GitHub Enterprise Cloud, GitHub Enterprise Server
  </Card>

  <Card title="GitLab" icon="gitlab" href="/platforms/gitlab-com">
    GitLab, GitLab Self-Managed
  </Card>

  <Card
    title="Azure DevOps"
    icon={
  		<svg
  			xmlns="http://www.w3.org/2000/svg"
  			width={24}
  			height={24}
  			fill="none"
  			{...props}
  		>
  			<path
  				fill="url(#a)"
  				d="M22.667 5.333V18.32l-5.334 4.373-8.266-3.013v2.986l-4.68-6.12 13.64 1.067V5.92l4.64-.587Zm-4.547.653-7.653-4.653v3.053L3.44 6.453 1.333 9.16v6.146l3.014 1.334V8.76L18.12 5.986Z"
  			/>
  			<defs>
  				<linearGradient
  					id="a"
  					x1={12}
  					x2={12}
  					y1={22.626}
  					y2={1.373}
  					gradientUnits="userSpaceOnUse"
  				>
  					<stop offset={1} stopColor="#FF570A" />
  				</linearGradient>
  			</defs>
  		</svg>
  	}
    href="/platforms/azure-devops"
  >
    Azure DevOps
  </Card>

  <Card title="Bitbucket" icon="bitbucket" href="/platforms/bitbucket-cloud">
    Bitbucket Cloud, Bitbucket Server
  </Card>
</CardGroup>

For complete platform details, see [Supported Git Platforms](/platforms/).

### Integrate with issue trackers

CodeRabbit connects with issue management platforms to create tickets during reviews or discuss code directly in issue comments:

* [GitHub Issues](/guides/issue-creation)
* [GitLab Issues](/guides/issue-creation)
* [Jira](/guides/issue-creation)
* [Linear](/guides/issue-creation)

Learn more about [Issue Creation](/guides/issue-creation) and [Issue Chat](/guides/issue-chat).

## IDE extensions

The free CodeRabbit VSCode extension brings core review features to VSCode, Cursor, Windsurf, and compatible editors. Review and polish changes locally before creating PRs.

<Info>
  **Local reviews**: Catch issues before they reach your team's review queue.
  The extension uses the same context-aware analysis as our PR reviews.
</Info>

See [Review local changes](/code-editors) for setup details.

## Data privacy and security

CodeRabbit protects your code through ephemeral processing:

* All LLM queries exist in-memory only, with zero retention after completion
* We don't use your code or reviews to train language models
* No customer data is shared with third parties
* All data remains confidential and isolated by organization
* SOC 2 and GDPR compliant data practices

Learn more at [CodeRabbit Trust Center](https://trust.coderabbit.ai).

## Flexible pricing

<CardGroup cols={2}>
  <Card title="Public repositories" icon="lock-open">
    **Free Pro tier features** for open source projects. Help improve code
    quality across the developer community.
  </Card>

  <Card title="Private repositories" icon="lock">
    **Multiple tiers available** from Free (unlimited summaries) to Enterprise
    (advanced features + SLA support).
  </Card>
</CardGroup>

See complete details at [Pricing](https://www.coderabbit.ai/pricing).

<Note>
  CodeRabbit Enterprise offers self-hosted deployment for teams with 500+ users.
  Contact [CodeRabbit Sales](mailto:sales@coderabbit.ai) for enterprise options.
</Note>

## What's next

<CardGroup cols={3}>
  <Card title="Quickstart" icon="rocket" href="/getting-started/quickstart/">
    Experience your first CodeRabbit review in under 5 minutes.
  </Card>

  <Card title="Why CodeRabbit?" icon="lightbulb" href="/overview/why-coderabbit">
    Deep dive into our approach and competitive advantages.
  </Card>

  <Card title="IDE Extension" icon="code" href="/code-editors">
    Install the extension to review local changes before pushing.
  </Card>
</CardGroup>
