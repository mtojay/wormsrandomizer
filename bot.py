# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
import asyncio
import random
import os
import json
from typing import List, Tuple, Optional

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def load_maps():
    """Load maps from maps.json file"""
    try:
        with open('maps.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convert to tuple format for compatibility
            return [(map_data['emoji'], map_data['name'], map_data['tags']) 
                   for map_data in data['maps']]
    except FileNotFoundError:
        print("Error: maps.json file not found!")
        print("Please create maps.json with your map data.")
        return []
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in maps.json: {e}")
        return []
    except Exception as e:
        print(f"Error loading maps: {e}")
        return []

# Load maps from JSON file
WORMS_MAPS = load_maps()

class WormsMapSelector:
    def __init__(self):
        if not WORMS_MAPS:
            raise ValueError("No maps loaded! Check your maps.json file.")
        self.all_maps = WORMS_MAPS.copy()
        random.shuffle(self.all_maps)
        self.match1_map = None
        self.match2_map_a = None
        self.match2_map_b = None
    
    def get_maps_with_shared_tags(self, reference_map):
        """Get maps that share at least one tag with the reference map"""
        reference_tags = set(reference_map[2])  # Get tags from reference map
        compatible_maps = []
        
        for map_data in self.all_maps:
            if map_data == reference_map:  # Skip the reference map itself
                continue
            map_tags = set(map_data[2])
            # Check if they share any tags
            if reference_tags.intersection(map_tags):
                compatible_maps.append(map_data)
        
        return compatible_maps if compatible_maps else [m for m in self.all_maps if m != reference_map]
    
    def format_map_list(self, available_maps, pointer_index=-1):
        """Format the map list with optional pointer and styled tags"""
        lines = []
        for i, (emoji, name, tags) in enumerate(available_maps):
            # Create pill-style tags
            tag_pills = " ".join([f"`{tag}`" for tag in tags])
            
            if i == pointer_index:
                lines.append(f"  👉 {emoji} **{name}** {tag_pills}")
            else:
                lines.append(f"     {emoji} **{name}** {tag_pills}")
        return "\n".join(lines)
    
    async def animate_selection(self, message, round_num, available_maps, title_text):
        """Animate the selection process and return selected map"""
        if not available_maps:
            return None
        
        # Check for development mode
        dev_mode = os.getenv('DEV_MODE') or os.getenv('TESTING_MODE')
        
        if dev_mode:
            # Super fast for development
            total_spins = random.randint(5, 8)
            base_delay = 0.02
            max_additional_delay = 0.3
        else:
            # Faster than before but still smooth
            total_spins = random.randint(4, 8)  # Reduced from 20-30
            base_delay = 0.04  # Reduced from 0.05
            max_additional_delay = 0.6  # Reduced from 0.8
        
        # Animation loop with exponential slowdown curve
        for spin in range(total_spins):
            pointer_index = spin % len(available_maps)
            
            # Create animation content
            content = f"🎯 **{title_text}**\n\n"
            content += self.format_map_list(available_maps, pointer_index)
            
            # Edit message with current frame
            try:
                await message.edit(content=content)
            except discord.NotFound:
                break
            
            # Smooth exponential curve for realistic spin slowdown
            progress = spin / (total_spins - 1)
            curve_factor = progress ** 2.5
            current_delay = base_delay + (curve_factor * max_additional_delay)
            
            await asyncio.sleep(current_delay)
        
        # Final selection
        final_index = (total_spins - 1) % len(available_maps)
        selected_map = available_maps[final_index]
        
        # Show final selection
        final_content = f"🎯 **{title_text}**\n\n"
        final_content += self.format_map_list(available_maps, final_index)
        final_content += f"\n\n✅ **Selected: {selected_map[0]} {selected_map[1]}**"
        
        try:
            await message.edit(content=final_content)
        except discord.NotFound:
            pass
        
        # Shorter pause between rounds in dev mode
        pause_time = 0.5 if dev_mode else 1.2  # Reduced from 1.5
        await asyncio.sleep(pause_time)
        return selected_map

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

@bot.tree.command(name='worms', description='Select maps for 2 Worms matches with tag-based pairing')
async def worms_command(interaction: discord.Interaction):
    """Handle the /worms slash command with new match structure"""
    
    # Defer the response since animation will take time
    await interaction.response.defer()
    
    # Create selector instance
    selector = WormsMapSelector()
    
    # Send initial message
    initial_content = "🎮 **Worms Match Randomizer**\n\nPreparing map selection..."
    message = await interaction.followup.send(content=initial_content)
    
    await asyncio.sleep(1)
    
    try:
        # SPIN 1: Match 1 map (both teams play this map)
        selector.match1_map = await selector.animate_selection(
            message, 1, selector.all_maps, "Spin 1 - Match 1 Map (Both Teams)"
        )
        
        # Remove Match 1 map from available maps
        remaining_maps = [m for m in selector.all_maps if m != selector.match1_map]
        
        # SPIN 2: First map for Match 2
        selector.match2_map_a = await selector.animate_selection(
            message, 2, remaining_maps, "Spin 2 - Match 2 Option A"
        )
        
        # SPIN 3: Second map for Match 2 (tag-based selection)
        compatible_maps = selector.get_maps_with_shared_tags(selector.match2_map_a)
        # Remove maps already selected
        compatible_maps = [m for m in compatible_maps if m not in [selector.match1_map, selector.match2_map_a]]
        
        if compatible_maps:
            spin3_title = f"Spin 3 - Match 2 Option B (Compatible with {selector.match2_map_a[1]})"
        else:
            # Fallback if no compatible maps
            compatible_maps = [m for m in selector.all_maps if m not in [selector.match1_map, selector.match2_map_a]]
            spin3_title = "Spin 3 - Match 2 Option B (Random)"
        
        selector.match2_map_b = await selector.animate_selection(
            message, 3, compatible_maps, spin3_title
        )
        
        # Create final summary
        if selector.match1_map and selector.match2_map_a and selector.match2_map_b:
            final_summary = "🎉 **Worms Match Setup Complete!**\n\n"
            final_summary += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Match 1 - Both teams same map
            final_summary += "# 🥇 Match 1\n"
            final_summary += "### Both teams play\n\n"
            final_summary += f"## 🔹 {selector.match1_map[0]} **{selector.match1_map[1]}** {selector.match1_map[0]} 🔹\n\n"
            final_summary += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Match 2 - Winner picks between two options  
            final_summary += "### 🥈 Match 2\n"
            final_summary += "### Winner chooses between\n\n"
            final_summary += f"## {selector.match2_map_a[0]} **{selector.match2_map_a[1]}** {selector.match2_map_a[0]}    {selector.match2_map_b[0]} **{selector.match2_map_b[1]}** {selector.match2_map_b[0]}\n\n"
            
            # Show shared tags with pill styling
            shared_tags = set(selector.match2_map_a[2]).intersection(set(selector.match2_map_b[2]))
            if shared_tags:
                tag_pills = " ".join([f"`{tag}`" for tag in shared_tags])
                final_summary += f"🏷️ *Connected by:* {tag_pills}\n\n"
            
            final_summary += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            final_summary += "# 🎯 Good luck in your Worms battles!"
            
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