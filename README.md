# Discord Worms Map Randomizer Bot

An animated Discord bot that selects maps for a tournament-style Worms match through spinning wheel animations.

## Features

- **Tournament Format**: 2 matches with strategic map selection
- **Tag-Based Pairing**: Maps with compatible themes face off in Match 2
- **Animated Selection**: Visual spinning pointer with progressive slowdown
- **External Configuration**: Easy map management via `maps.json`
- **Development Mode**: Fast animations for testing
- **Docker Ready**: Containerized for easy deployment

## Tournament Format

### Match Structure
- **🥇 Match 1**: Both teams play the same map
- **🥈 Match 2**: Winner chooses between two tag-compatible options

### Map Selection Process
1. **Spin 1**: Selects Match 1 map (any available map)
2. **Spin 2**: Selects Match 2 Option A (from remaining maps)  
3. **Spin 3**: Selects Match 2 Option B (compatible tags with Option A)

## Maps & Tags

Maps are configured in `maps.json` with tags for strategic pairing:

```json
{
  "maps": [
    {
      "emoji": "🏰",
      "name": "Burg",
      "tags": ["large", "fortress"]
    },
    {
      "emoji": "🌳", 
      "name": "Baum",
      "tags": ["large", "nature"]
    }
  ]
}
```

### Default Maps Included

- 🏰 **Burg** - `[large, fortress]`
- 🏠 **Haus** - `[small, cozy]`
- 🚀 **Rakete** - `[mid, tech]`
- 🌳 **Baum** - `[large, nature]`
- 🍄 **Pilz** - `[small, nature]`
- 🐴 **Esel** - `[small, mid]`
- 🚢 **Schiff** - `[mid, water]`
- ☢️ **Reaktor** - `[large, tech]`

## Quick Start

### Prerequisites

- Python 3.11+
- Discord bot token
- Docker (optional)

### Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and bot
3. Copy the bot token
4. Invite bot to your server with these permissions:
   - Send Messages
   - Use Slash Commands
   - Embed Links

### Installation Options

#### Option 1: Docker (Recommended)

1. Clone/download the files
2. Create `.env` file:
   ```
   DISCORD_BOT_TOKEN=your_token_here
   ```
3. Ensure `maps.json` is in the same directory
4. Run with Docker Compose:
   ```bash
   docker-compose up -d --build
   ```

#### Option 2: Direct Python

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure `maps.json` is in the same directory as `bot.py`
3. Set environment variable:
   ```bash
   export DISCORD_BOT_TOKEN="your_token_here"
   ```
4. Run the bot:
   ```bash
   python bot.py
   ```

#### Option 3: Docker Build

```bash
# Build the image
docker build -t worms-bot .

# Run the container with volume mount
docker run -d \
  --name worms-bot \
  -e DISCORD_BOT_TOKEN="your_token_here" \
  -v $(pwd)/maps.json:/app/maps.json:ro \
  --restart unless-stopped \
  worms-bot
```

## Usage

1. Use the `/worms` slash command in any channel
2. Watch the 3 animated spins
3. Get your tournament setup with 2 matches!

## Example Output

```
🎉 Worms Match Setup Complete!

🥇 Match 1: Both teams play
🔹 🌳 Baum 🌳

🥈 Match 2: Winner chooses
🔸 🍄 Pilz 🍄  ⚔️  🏠 Haus 🏠 🔸

🏷️ Connected by: small

🎯 Good luck in your Worms battles!
```

## Configuration

### Maps Configuration

Edit `maps.json` to customize available maps. After changes:

**For Python:** Restart the bot
**For Docker:** Restart the container (maps.json is mounted as volume)

```bash
docker-compose restart worms-bot
```

### Development Mode

For faster testing during development:

```bash
# Faster animations
DEV_MODE=1 python bot.py

# With Docker
docker-compose up -d --build -e DEV_MODE=1
```

### Environment Variables

- `DISCORD_BOT_TOKEN`: Your Discord bot token (required)
- `DEV_MODE`: Enable fast animations for development (optional)

### Animation Customization

You can modify these values in `bot.py`:

- **Normal mode**: 15-22 spins, 40ms start
- **Dev mode**: 5-8 spins, 20ms start
- **Curve factor**: Adjust `progress ** 2.5` for different slowdown styles

## File Structure

```
worms-bot/
├── bot.py                 # Main bot code
├── maps.json             # Map configuration
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose setup
├── .env                  # Environment variables (create this)
└── README.md            # This documentation
```

## Troubleshooting

### Bot doesn't respond to `/worms`

1. Check bot permissions (Send Messages, Use Slash Commands)
2. Wait a few minutes for slash commands to sync
3. Try restarting the bot

### Maps not loading

1. Verify `maps.json` exists in the correct location
2. Check JSON syntax is valid
3. Ensure file is accessible by the bot process
4. Check console for error messages

### Docker container won't start

1. Verify your `.env` file has the correct token
2. Ensure `maps.json` exists in the same directory
3. Check Docker logs: `docker-compose logs worms-bot`
4. Verify no port conflicts

## License

This project is open source and available under the MIT License.