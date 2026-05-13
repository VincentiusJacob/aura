# Telegram Agent AI

A modular, AI-powered Telegram bot that understands natural language, remembers conversations, and can perform real-world actions — like searching, taking notes, or scheduling events.

---

## Table of Contents

- [What This Project Does](#what-this-project-does)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Adding New Features](#adding-new-features)
- [Development Guidelines](#development-guidelines)
- [Running Tests](#running-tests)

---

## What This Project Does

This bot connects Telegram to an AI agent that can:

- **Chat naturally** — understands your messages like a real assistant
- **Remember context** — keeps track of the conversation over time
- **Take actions** — searches the web, creates notes, manages schedules, and more
- **Be extended** — add new tools and capabilities without touching existing code

---

## How It Works

Here's the flow from a user's message to a response:

```
User sends message on Telegram
        ↓
  bot/handlers/          ← Receives and routes the message
        ↓
  agent/core.py          ← Orchestrates the full reasoning loop
        ↓
  agent/planner.py       ← Decides: reply directly, or use a tool?
        ↓
  agent/executor.py      ← Runs the chosen tool
        ↓
  tools/                 ← Does the actual work (search, notes, etc.)
        ↓
  db/ + agent/memory.py  ← Saves and retrieves conversation history
        ↓
  Response sent back to Telegram
```

---

## Project Structure

```
telegram-agent/
├── pyproject.toml              # Project config, dependencies, tooling
├── .env.example                # Template for environment variables
│
├── src/
│   └── telegram_agent/
│       ├── main.py             # App entry point — starts the bot
│       ├── config.py           # Loads settings from environment variables
│       │
│       ├── bot/                # Telegram interface layer
│       │   ├── router.py       # Registers all handlers in one place
│       │   ├── handlers/       # Responds to messages and commands
│       │   ├── keyboards/      # Button/menu layouts
│       │   └── middlewares/    # Runs before/after every message
│       │
│       ├── agent/              # AI reasoning layer
│       │   ├── core.py         # Main loop: input → think → respond
│       │   ├── planner.py      # Decides what action to take
│       │   ├── executor.py     # Runs tool calls
│       │   ├── memory.py       # Manages conversation history logic
│       │   └── prompts.py      # All AI system prompts in one place
│       │
│       ├── tools/              # Things the agent can do
│       ├── services/           # Wrappers for external APIs (LLM, etc.)
│       ├── db/                 # Database models, queries, sessions
│       └── utils/              # Small helper functions
│
├── tests/                      # Unit and integration tests
└── scripts/                    # Dev utilities (seed DB, run bot manually, etc.)
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- A Telegram bot token (get one from [@BotFather](https://t.me/BotFather))
- An OpenAI API key
- A running PostgreSQL (or compatible) database

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/your-username/telegram-agent.git
cd telegram-agent
```

**2. Install dependencies**

```bash
pip install -e .
```

**3. Set up environment variables**

```bash
cp .env.example .env
# Open .env and fill in your values
```

**4. Run the bot**

```bash
python -m telegram_agent.main
```

Your bot is now live and listening for messages on Telegram.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in the following:

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token from [@BotFather](https://t.me/BotFather) |
| `OPENAI_API_KEY` | Your OpenAI API key |
| `DATABASE_URL` | PostgreSQL connection string |

---

## Adding New Features

| What you want to do | Where to add it |
|---|---|
| Handle a new `/command` | `bot/handlers/` |
| Add a new AI reasoning behavior | `agent/` |
| Add a new tool the agent can use | `tools/` |
| Integrate a new external API | `services/` |
| Add a new database table | `db/models.py` |
| Add a new database query | `db/repository.py` |
| Add a small utility/helper | `utils/` |

### Example: Adding a `/remind` command

1. Create `bot/handlers/remind.py` — handle the Telegram command
2. Create `tools/reminders.py` — implement the reminder logic
3. Register the handler in `bot/router.py`

---

## Module Reference

### `bot/` — Telegram Interface

| File/Folder | Purpose |
|---|---|
| `router.py` | Combines all handlers and attaches them to the bot |
| `handlers/start.py` | Handles the `/start` command |
| `handlers/chat.py` | Main handler for user messages — sends them to the agent |
| `handlers/actions.py` | Handles inline button taps |
| `keyboards/` | Button layouts only — no logic |
| `middlewares/` | Logging, auth checks, injecting DB sessions |

### `agent/` — AI Brain

| File | Purpose |
|---|---|
| `core.py` | Orchestrates the full reasoning loop |
| `planner.py` | Decides whether to reply or call a tool |
| `executor.py` | Maps tool names to functions and runs them |
| `memory.py` | Reads and writes conversation context |
| `prompts.py` | Centralized system prompts for the AI |

### `db/` — Database

| File | Purpose |
|---|---|
| `models.py` | Table definitions (User, Message, Session, etc.) |
| `repository.py` | All DB queries (`get_user()`, `save_message()`, etc.) |
| `session.py` | Manages DB connections |

---

## Development Guidelines

- **Keep handlers thin** — they should receive the message and pass it to the agent, nothing more
- **Separate thinking from doing** — `planner.py` decides, `executor.py` acts
- **All DB access goes through `repository.py`** — no raw queries elsewhere
- **External APIs belong in `services/`** — agent and tools call services, not APIs directly
- **All prompts live in `prompts.py`** — never hardcode prompts inside logic files

---

## Running Tests

```bash
pytest tests/
```

Test files are organized to mirror the source:

- `tests/test_agent.py` — agent reasoning logic
- `tests/test_tools.py` — individual tool functions
- `tests/test_handlers.py` — Telegram handler behavior

---

## Scripts

Utility scripts for development (not part of the main app):

| Script | Purpose |
|---|---|
| `scripts/run_bot.py` | Run the bot manually without the full setup |
| `scripts/seed_db.py` | Populate the database with test data |
| `scripts/index_workflows.py` | Precompute embeddings for workflows |