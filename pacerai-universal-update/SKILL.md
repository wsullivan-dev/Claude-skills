---
name: pacerai-universal-update
description: Make any repo in the PacerAI workspace AI Native by adding CLAUDE.md, AGENTS.md, .claude/, PDBRDD docs structure (Plan/Design/Build/Review/Document/Deploy), Claude GitHub workflows, and Notion guidance. Use when onboarding a new repo, auditing AI readiness, or refreshing an existing repo's AI Native setup.
---

# PacerAI Universal Update

Make any repository AI Native — fully set up for productive LLM collaboration (Claude, Codex, Gemini, Copilot) with the PDBRDD lifecycle.

## When to Use This Skill

Use this skill when:
- "Make this repo AI Native"
- "Set up CLAUDE.md and docs for this project"
- "Add PDBRDD structure to this repo"
- "Onboard a new repo into the workspace"
- "Audit AI readiness across repos"
- "Refresh the AI Native setup for this project"

## Reference Implementation

The gold-standard repo is `04_PacerAI_GTM/website-PacerAI/`. Always reference its files for templates:

- `CLAUDE.md` — repo context, commands, architecture, env vars, critical rules, flag-for-review
- `AGENTS.md` — identity, operating rules, PDBRDD workflow, MCP servers, escalation triggers
- `docs/plan/overview.md` — goals, scope, success criteria, timeline
- `docs/plan/prd.md` — product requirements
- `docs/design/` — mockups, UX stories, sequence diagrams
- `docs/build/architecture.md` — tech decisions, API endpoints, file map, constraints
- `docs/review/checklist.md` — QA pass/fail sections, sign-off, ready-to-deploy decision
- `docs/review/Issues.md` — numbered issues with impact/action/status
- `docs/document/changelog.md` — reverse-chronological deploy log
- `docs/document/notion-guidance.md` — internal_docs + customer_docs Notion structure
- `docs/deploy/runbook.md` — pre-flight, deploy steps, post-deploy verify, rollback

## Workflow

### Step 1: Assess Current State

Before creating anything, inventory what already exists:

```
Check for:
- CLAUDE.md (repo root)
- AGENTS.md (repo root)
- .claude/ directory
- docs/ directory and its contents
- .github/workflows/ (existing CI/CD)
- README.md (extract architecture info)
- .env.example or environment docs
- azure.yaml, infra/ (deployment config)
```

**Do not overwrite existing files.** If a CLAUDE.md exists, suggest improvements. If docs/ has files, migrate them into PDBRDD folders.

### Step 2: Determine Repo Type

Adapt the setup based on repo type:

| Type | Examples | Adaptations |
|------|----------|-------------|
| **Web app** (Express + React) | paceraidemo, client-TDS | Full PDBRDD, Playwright MCP in review, Azure deploy runbook |
| **Python service** | agentteam | pytest in review checklist, pip/uvicorn in deploy, curl for API checks |
| **CLI tool** | pacerai-admin | Lighter PDBRDD, command validation in review, no deploy runbook needed |
| **Scaffold/reference** | pacerai-platform-demo | Minimal PDBRDD, no active deploy |
| **Skill** | Data-Story-Skill, PDFtoPPT | Lightweight: CLAUDE.md + plan/overview + build + document/changelog |
| **Next.js app** | uigen | Vitest + typecheck in review, Turbopack dev, Playwright MCP |
| **WordPress site** | website-PacerAI | WP REST API deploy, brand constraints, backup-before-deploy |

### Step 3: Create Directory Structure

```bash
mkdir -p docs/{plan,design,build,review,document,deploy} .claude
```

### Step 4: Migrate Existing Docs

Move existing flat docs into the correct PDBRDD folder. Common migrations:

| Source Pattern | Destination |
|---------------|-------------|
| `docs/architecture.md` | `docs/build/architecture.md` |
| `docs/CICD.md` | `docs/deploy/cicd.md` |
| `docs/PRD*.md` | `docs/plan/` |
| `docs/ROADMAP*.md` | `docs/plan/roadmap.md` |
| `docs/*runbook*.md` | `docs/deploy/` |
| `docs/*validation*.md` | `docs/review/` |

**Delete the originals after migration.** Do not leave duplicates.

### Step 5: Create CLAUDE.md

Follow this structure (customize content per repo):

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is
[One paragraph: what, who it serves, stack]

## Commands
[Dev, build, test, lint, deploy commands]

## Architecture
[ASCII diagram, key subsystems with file paths]

## Repository Structure
[PDBRDD docs/ tree]

## Environment Variables
[Required env vars, how to verify]

## Critical Rules
[Repo-specific guardrails]

## Flag for Human Review
[When to stop and ask]
```

### Step 6: Create AGENTS.md

Follow this structure:

```markdown
# AGENTS.md — [repo name]

## Identity & Mission
[Role definition]

## Environment
[Env vars with verification commands]

## Repository Map
[Key files and what they do]

## Operating Rules
[Numbered rules]

## PDBRDD Workflow
[Phase-by-phase guidance: PLAN, DESIGN, BUILD, REVIEW, DOCUMENT, DEPLOY]

## MCP Servers Available
[Playwright, Slack, Gmail, Notion as applicable]

## What to Flag for Human Review
[Escalation criteria]
```

### Step 7: Create .claude/settings.local.json

```json
{
  "permissions": {
    "allow": [
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      ... (add repo-specific: npm, python, pip, pytest, curl, etc.)
    ],
    "deny": []
  }
}
```

### Step 8: Create PDBRDD Docs

Create each file adapted to the repo type. Reference the templates in the reference implementation.

**docs/plan/overview.md** — always create:
- Sprint/date/owner/status
- Goal, problem statement, success criteria (checkboxes)
- Scope in/out, timeline table

**docs/review/checklist.md** — adapt per repo type:
- Web apps: auth flow, workspace routing, Power BI, chat, technical, Playwright MCP
- Python: pytest, API contract, agent validation
- CLI: command output, database state, destructive operation safety

**docs/review/Issues.md** — always create (empty template)

**docs/document/changelog.md** — always create (empty template with format)

**docs/document/notion-guidance.md** — always create:
- internal_docs: architecture decisions, sprint notes, retrospectives
- customer_docs: user guides, release notes, FAQ
- MCP integration note for Notion MCP server

**docs/deploy/runbook.md** — adapt per deploy method:
- Azure App Service: pre-flight, azd commands, post-deploy verification, rollback
- Python: pip install, uvicorn, health check
- WordPress: REST API push, backup, rollback
- CLI: skip or minimal

### Step 9: Add Claude GitHub Workflows (if PR-driven repo)

**claude.yml** — triggers on @claude mentions in issues/PRs:
- Checkout, setup language (Node 22 or Python 3.13), install deps
- Run `anthropics/claude-code-action@v1`
- Include Playwright MCP config for web app repos
- Requires `CLAUDE_CODE_OAUTH_TOKEN` secret

**claude-code-review.yml** — automated PR review:
- Triggers on PR open/sync/ready
- Generic, same across all repos
- Uses code-review plugin from claude-code marketplace

### Step 10: Verify

Run this check against the repo:

```bash
echo "=== AI NATIVE CHECK ==="
base="$(pwd)"
test -f "$base/CLAUDE.md" && echo "✓ CLAUDE.md" || echo "✗ CLAUDE.md"
test -f "$base/AGENTS.md" && echo "✓ AGENTS.md" || echo "✗ AGENTS.md"
test -d "$base/.claude" && echo "✓ .claude/" || echo "✗ .claude/"
for dir in plan design build review document deploy; do
  test -d "$base/docs/$dir" && echo "✓ docs/$dir/" || echo "✗ docs/$dir/"
done
test -f "$base/.github/workflows/claude.yml" && echo "✓ claude.yml" || echo "- claude.yml (n/a)"
```

### Step 11: Update Root CLAUDE.md

If the repo is new to the workspace, add it to the folder table and Key Repos section in `/Users/willsullivan/Documents/GitHub/CLAUDE.md`.

## Post-Setup Reminders

After running this skill, remind the user:
1. Set `CLAUDE_CODE_OAUTH_TOKEN` secret in GitHub repo settings (for Claude workflows)
2. Fill in the `docs/plan/overview.md` success criteria checkboxes
3. Run a verification by opening a new Claude Code session in the repo and asking "What is this repo?"
