# Discord Worms Map Randomizer Bot

An animated Discord bot that randomly selects 3 Worms maps through a spinning wheel-style animation.

## Features

- **Animated Selection**: Visual spinning pointer with progressive slowdown
- **3-Round Selection**: Picks 3 unique maps without duplicates
- **8 Worms Maps**: Burg, Haus, Rakete, Baum, Pilz, Esel, Schiff, Reaktor
- **Slash Command**: Modern `/worms` command interface
- **Docker Ready**: Containerized for easy deployment

## Maps Included

- 🏰 Burg
- 🏠 Haus
- 🚀 Rakete
- 🌳 Baum
- 🍄 Pilz
- 🐴 Esel
- 🚢 Schiff
- ☢️ Reaktor

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
3. Run with Docker Compose:
   ```bash
   docker-compose up -d
   ```

#### Option 2: Direct Python

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variable:
   ```bash
   export DISCORD_BOT_TOKEN="your_token_here"
   ```
3. Run the bot:
   ```bash
   python bot.py
   ```

#### Option 3: Docker Build

```bash
# Build the image
docker build -t worms-bot .

# Run the container
docker run -d \
  --name worms-bot \
  -e DISCORD_BOT_TOKEN="your_token_here" \
  --restart unless-stopped \
  worms-bot
```

## Usage

1. Invite the bot to your Discord server
2. Use the `/worms` slash command in any channel
3. Watch the animated selection process
4. Get your 3 selected maps for your Worms battle!

## Animation Details

- **Speed**: Starts at 100ms, progressively slows down
- **Duration**: 15-25 animation steps with final slowdown
- **Visual**: Text-based pointer (👉) moving through map list
- **Rounds**: 3 consecutive selections, removing chosen maps

## Example Output

```
🎯 Round 1 - Selecting Map...

     🏰 Burg
  👉 🏠 Haus
     🚀 Rakete
     🌳 Baum
     🍄 Pilz
     🐴 Esel
     🚢 Schiff
     ☢️ Reaktor

✅ Selected: 🏠 Haus
```

Final result:
```
🎉 All Selected Maps:

1. 🏠 Haus
2. 🚀 Rakete  
3. ☢️ Reaktor

🎯 Good luck in your Worms battle!
```

## Configuration

### Environment Variables

- `DISCORD_BOT_TOKEN`: Your Discord bot token (required)

### Customization

You can modify these values in `bot.py`:

- **Maps**: Edit `WORMS_MAPS` list to change available maps
- **Animation Speed**: Adjust `base_delay` and `delay_increment`
- **Spin Count**: Modify `total_spins` range
- **Selection Rounds**: Change the range in the main loop

## Error Handling

The bot includes comprehensive error handling for:

- Network issues during animation
- Discord API rate limits
- Missing permissions
- Invalid tokens
- Message editing failures

## Troubleshooting

### Bot doesn't respond to `/worms`

1. Check bot permissions (Send Messages, Use Slash Commands)
2. Wait a few minutes for slash commands to sync
3. Try kicking and re-inviting the bot

### Animation stops mid-way

- Usually due to Discord rate limits or network issues
- Bot will attempt to recover and show final results

### Docker container won't start

1. Verify your `.env` file has the correct token
2. Check Docker logs: `docker-compose logs worms-bot`
3. Ensure no port conflicts

## File Structure

```
worms-bot/
├── bot.py                 # Main bot code
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose setup
├── .env                  # Environment variables (create this)
└── README.md            # This documentation
```

## Support

For issues or questions:

1. Check the console/logs for error messages
2. Verify your Discord bot token is correct
3. Ensure the bot has proper permissions in your server
4. Try restarting the bot

## License

This project is open source and available under the MIT License.