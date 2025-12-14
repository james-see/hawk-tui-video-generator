# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hawk TUI is a terminal-based TikTok video creator. It generates images using custom Replicate models and assembles them into 9:16 videos with FFmpeg. Think "CapCut TUI with AI".

## Tech Stack

- **TUI Framework**: Textual + Rich
- **Image Generation**: Replicate (custom trained models)
- **Video Creation**: FFmpeg
- **AI**: Anthropic Claude (via anthropic SDK)
- **Python Version**: 3.11+

## Build & Run Commands

```bash
# Install dependencies
pip install -e .
# or with uv
uv pip install -e .

# Run the TUI
python -m hawk.main
# or after install
hawk
```

## Architecture

```
hawk/
├── main.py              # Entry point
├── app.py               # Main Textual TUI
├── config.py            # Projects + model mappings
├── replicate_client.py  # Replicate API wrapper
├── video.py             # FFmpeg video assembly
├── screens/             # TUI screens (future)
└── widgets/             # TUI widgets (future)
```

## Projects & Models

| Project | Replicate Model | Trigger | Use |
|---------|-----------------|---------|-----|
| wedding-vision | digital-prairie-labs/spring-wedding | TOK | Wedding florals |
| latin-bible | digital-prairie-labs/catholic-prayers-v2.1 | - | Religious imagery |
| dxp-albs | digital-prairie-labs/futuristic | TOK | Sci-fi scenes |

## Content Structure

```
content/
├── wedding-vision/
│   ├── images/    # Generated images
│   ├── audio/     # Audio files for videos
│   └── exports/   # Final TikTok videos
├── latin-bible/
└── dxp-albs/
```

## Keyboard Shortcuts

- `1/2/3` - Switch project
- `g` - Generate images (uses prompt input)
- `a` - Select all images
- `s` - Toggle selection
- `v` - Create video from selected
- `o` - Show audio files
- `b` - Open exports folder
- `d` - Delete selected images
- `q` - Quit

## Environment Variables

Required in `.env`:
- `REPLICATE_API_TOKEN` - Replicate API
- `ANTHROPIC_API_KEY` - Claude API (optional, for prompt enhancement)

## Git Workflow

Commit after each batch of changes with descriptive messages.
