# Monorepo Starter (FastAPI + Next.js)

This repo is a starter pack for a strongly-typed, clean, maintainable monorepo:
- `apps/api`: FastAPI backend (PostgreSQL)
- `apps/web`: Next.js frontend (Bootstrap responsive)

## Docs
- `docs/DECISIONS.md` - stack/architecture decisions
- `docs/API_CONTRACT.md` - API shapes + endpoints contract
- `docs/CODING_STANDARDS.md` - coding conventions + testing requirements
- `docs/SKILLS.md` - agent rules (Claude Code / AI assistant)

## Quick Start (high level)
1. Choose your Python + Node versions (see DECISIONS.md)
2. Create backend venv using explicit Python version:
   - `py -3.12 -m venv .venv`
3. Keep secrets out of git; use `.env` locally and commit only `.env.example`
