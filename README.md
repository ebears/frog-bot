# 🐸 Frog Bot

A Discord bot built with Python and discord.py, featuring slash commands and a modular cog-based architecture.

## Prerequisites

- Python 3.11+
- Docker (optional)

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv

# Mac/Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```bash
DISCORD_TOKEN=your_bot_token_here
GUILD_ID=your_test_server_id_here
```

To get these values:

- **DISCORD_TOKEN**: Go to the [Discord Developer Portal](https://discord.com/developers/applications) → Your App → Bot → Reset Token
- **GUILD_ID**: Enable Developer Mode in Discord (Settings → Advanced), then right-click your server and click **Copy Server ID**

### 4. Invite the bot to your server

In the Developer Portal, go to **OAuth2 → URL Generator** and select the following scopes:

- `bot`
- `applications.commands`

And the following permissions:

- `Send Messages`
- `Read Messages / View Channels`
- `Embed Links`

Open the generated URL in your browser and add the bot to your server.

## Running the Bot

### Without Docker

```bash
python bot.py
```

### With Docker

```bash
docker compose up --build   # First run
docker compose up -d        # Run in background
docker compose down         # Stop the bot
docker compose logs -f bot  # View live logs
```

## Syncing Slash Commands

Once the bot is running, use the following prefix commands to register slash commands:

| Command | Description |
| --- | --- |
| `!sync` | Syncs commands to your test server (instant) |
| `!sync global` | Syncs commands globally (up to 1 hour to propagate) |

Use `!sync` during development and `!sync global` when deploying to production.

## Available Commands

| Command | Description |
| --- | --- |
| `/ping` | Check the bot's latency |
| `/hello` | Get a greeting from the bot |
| `/info` | Display info about the server |
| `/say` | Make the bot repeat a message |

## Adding New Cogs

1. Create a new file in the `cogs/` directory, e.g. `cogs/moderation.py`
2. Define a class that inherits from `commands.Cog`
3. Add a `setup()` function at the bottom
4. Register it in `bot.py` by adding `await bot.load_extension("cogs.moderation")`
5. Restart the bot and run `!sync`
