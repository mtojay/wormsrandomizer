# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio
import random
import os
from typing import List, Tuple, Optional

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Worms maps with emojis
WORMS_MAPS = [
    ("🏰", "Burg"),
    ("🏠", "Haus"),
    ("🚀", "Rakete"),
    ("🌳", "Baum"),
    ("🍄", "Pilz"),
    ("🐴", "Esel"),
    ("🚢", "Schiff"),
    ("☢️", "Reaktor")
]

class WormsMapSelector:
    def __init__(self):
        self.available_maps = WORMS_MAPS.copy()
        random.shuffle(self.available_maps)  # Randomize map order each time
        self.selected_maps = []
    
    def format_map_list(self, pointer_index=-1):
        """Format the map list with optional pointer"""
        lines = []
        for i, (emoji, name) in enumerate(self.available_maps):
            if i == pointer_index:
                lines.append(f"  👉 {emoji} {name}")
            else:
                lines.append(f"     {emoji} {name}")
        return "\n".join(lines)
    
    async def animate_selection(self, message, round_num):
        """Animate the selection process and return selected map"""
        if not self.available_maps:
            return None, None
        
        # Animation parameters
        total_spins = random.randint(10, 15)  # More spins for smoother curve
        base_delay = 0.05  # Starting delay (50ms)
        
        # Animation loop with exponential slowdown curve
        for spin in range(total_spins):
            pointer_index = spin % len(self.available_maps)
            
            # Create animation content
            content = f"🎯 **Round {round_num}** - Selecting Map...\n\n"
            content += self.format_map_list(pointer_index)
            
            # Edit message with current frame
            try:
                await message.edit(content=content)
            except discord.NotFound:
                break
            
            # Smooth exponential curve for realistic spin slowdown
            # Progress from 0.0 to 1.0 through the animation
            progress = spin / (total_spins - 1)
            
            # Exponential curve: starts fast, smooth gradual slowdown
            curve_factor = progress ** 2.5  # Adjust curve steepness (higher = more dramatic)
            current_delay = base_delay + (curve_factor * 0.8)  # Max additional delay
            
            await asyncio.sleep(current_delay)
        
        # Final selection
        final_index = (total_spins - 1) % len(self.available_maps)
        selected_map = self.available_maps[final_index]
        
        # Show final selection
        final_content = f"🎯 **Round {round_num}** - Selected!\n\n"
        final_content += self.format_map_list(final_index)
        final_content += f"\n\n✅ **Selected: {selected_map[0]} {selected_map[1]}**"
        
        try:
            await message.edit(content=final_content)
        except discord.NotFound:
            pass
        
        # Remove selected map and add to results
        self.available_maps.remove(selected_map)
        self.selected_maps.append(selected_map)
        
        await asyncio.sleep(1.5)  # Pause before next round
        
        return selected_map[0], selected_map[1]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name='worms', description='Select 3 random Worms maps with animated selection')
async def worms_command(interaction: discord.Interaction):
    """Handle the /worms slash command"""
    
    # Defer the response since animation will take time
    await interaction.response.defer()
    
    # Create selector instance
    selector = WormsMapSelector()
    
    # Send initial message
    initial_content = "🎮 **Worms Map Randomizer**\n\nPreparing selection..."
    message = await interaction.followup.send(content=initial_content)
    
    await asyncio.sleep(1)
    
    # Run 3 selection rounds
    try:
        for round_num in range(1, 4):
            emoji, name = await selector.animate_selection(message, round_num)
            if not emoji:  # Safety check
                break
        
        # Create final summary
        if len(selector.selected_maps) == 3:
            final_summary = "🎉 **All Selected Maps:**\n\n"
            for i, (emoji, name) in enumerate(selector.selected_maps, 1):
                final_summary += f"{i}. {emoji} {name}\n"
            
            final_summary += "\n🎯 Good luck in your Worms battle!"
            
            await message.edit(content=final_summary)
        else:
            await message.edit(content="❌ Error occurred during selection. Please try again.")
            
    except Exception as e:
        error_message = "⚠️ An error occurred during map selection. Please try again."
        try:
            await message.edit(content=error_message)
        except:
            await interaction.followup.send(content=error_message)
        print(f"Error in worms command: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Handle command errors"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore unknown commands
    print(f"Command error: {error}")

# Error handling for slash commands
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
    """Handle slash command errors"""
    if interaction.response.is_done():
        await interaction.followup.send("❌ An error occurred. Please try again.", ephemeral=True)
    else:
        await interaction.response.send_message("❌ An error occurred. Please try again.", ephemeral=True)
    print(f"Slash command error: {error}")

def main():
    """Main function to run the bot"""
    token = os.getenv('DISCORD_BOT_TOKEN')
    
    if not token:
        print("Error: DISCORD_BOT_TOKEN environment variable not set!")
        print("Please set your Discord bot token as an environment variable.")
        return
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("Error: Invalid Discord bot token!")
    except Exception as e:
        print(f"Error starting bot: {e}")

if __name__ == "__main__":
    main()