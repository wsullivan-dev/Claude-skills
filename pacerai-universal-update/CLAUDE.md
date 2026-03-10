# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

PacerAI Universal Update — a Claude Code skill that makes any repo in the PacerAI workspace AI Native. It adds CLAUDE.md, AGENTS.md, .claude/ config, PDBRDD docs structure, Claude GitHub workflows, and Notion documentation guidance.

## Key Files

- `SKILL.md` — Full skill definition with 11-step workflow, repo type adaptations, and file templates

## How It Works

The skill follows a systematic process:
1. Assess current state (don't overwrite existing files)
2. Determine repo type (web app, Python, CLI, scaffold, skill)
3. Create PDBRDD directory structure
4. Migrate existing docs into correct folders
5. Create CLAUDE.md, AGENTS.md, .claude/settings.local.json
6. Create lifecycle docs (overview, checklist, issues, changelog, notion-guidance, runbook)
7. Add Claude GitHub workflows (claude.yml, claude-code-review.yml)
8. Verify all checks pass
9. Update root workspace CLAUDE.md

## Reference Implementation

All templates are derived from `04_PacerAI_GTM/website-PacerAI/` — the original PDBRDD repo.
