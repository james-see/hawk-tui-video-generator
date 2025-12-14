# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hawk TUI is a terminal-based CEO agent CLI powered by the Claude Agent SDK. It provides a keyboard-first interface for managing email, calendar, CRM, tasks, and content creation with AI assistance.

**Status**: Project specification exists (`ceo-cli-claude-instructions-hawk-tui.md`) but implementation not yet started.

## Tech Stack

- **Agent Runtime**: Claude Agent SDK (Python)
- **TUI Framework**: Textual + Rich
- **Image Generation**: Replicate (FLUX models)
- **Video Creation**: FFmpeg
- **Package Manager**: uv (recommended) or pip
- **Python Version**: 3.11+

## Build & Run Commands

```bash
# Install dependencies (using uv)
uv add claude-agent-sdk textual rich replicate httpx pillow python-dotenv

# Run the TUI
python -m hawk.main

# Skip boot animation
python -m hawk.main --no-boot
```

## Architecture

The project follows a modular skill-based architecture:

- `hawk/main.py` - Entry point with PS2-style boot sequence
- `hawk/app.py` - Main Textual TUI application with CEO CLI aesthetic
- `hawk/agent.py` - Claude Agent SDK wrapper with MCP tools
- `hawk/skills/` - Modular integrations (Gmail, Calendar, Fizzy, HubSpot, Snowflake, Replicate, FFmpeg)
- `hawk/ui/` - TUI components (loading animations, theme, widgets, screens)
- `hawk/mcp/` - MCP server for custom skills

## Key Design Patterns

- **Keyboard-first**: Single-letter shortcuts for all actions
- **Human-in-the-loop**: AI proposes actions, user confirms before execution
- **PS2 aesthetic**: Dark theme (#1a1d23), gold accents (#c9a227), green borders (#4a5f4a)
- **Cruise mode**: Rapid-fire inbox review for quick processing

## Environment Variables

Required API keys go in `.env` (never commit):
- `ANTHROPIC_API_KEY` - Claude Agent SDK
- `REPLICATE_API_TOKEN` - Image generation
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` - Gmail/Calendar
- `FIZZY_ACCESS_TOKEN` - 37signals kanban
- `HUBSPOT_API_KEY` - CRM
- Snowflake credentials

## Git Workflow

Commit after each batch of changes with descriptive messages.
