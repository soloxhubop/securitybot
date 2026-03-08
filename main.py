import discord
from discord.ext import commands
from discord import ui

# --- CONFIGURAZIONE ---
TOKEN = os.environ.get('TOKEN')
MIO_ID = 123456789012345678  # <--- METTI IL TUO ID QUI!

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="?", intents=intents)

# Stato delle funzioni
config = {"link": True, "spam": True, "nuke": True}

# --- INTERFACCIA SETUP ---
class SetupView(ui.View):
    @ui.select(placeholder="Attiva/Disattiva funzioni...", options=[
        discord.SelectOption(label="Anti-Link", value="link"),
        discord.SelectOption(label="Anti-Spam", value="spam"),
        discord.SelectOption(label="Anti-Nuke", value="nuke")
    ])
    async def select_callback(self, interaction, select):
        feature = select.values[0]
        config[feature] = not config[feature]
        status = "ATTIVATO" if config[feature] else "DISATTIVATO"
        await interaction.response.send_message(f"✅ {feature.upper()} ora è {status}", ephemeral=True)

@bot.command()
async def setup(ctx):
    if ctx.author.id != MIO_ID: return
    await ctx.send("🔧 **Pannello di Controllo Sicurezza**", view=SetupView())

# --- LOGICA DI SICUREZZA ---
@bot.event
async def on_message(message):
    if message.author.bot or message.author.id == MIO_ID:
        await bot.process_commands(message)
        return

    # Anti-Link
    if config["link"] and "http" in message.content.lower():
        await message.delete()
        await message.channel.send(f"🚫 {message.author.mention}, link non permessi!")

    # Anti-Spam (semplificato)
    if config["spam"]:
        # Qui potresti aggiungere un contatore basato su tempo
        pass 

    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    # Anti-Nuke
    if config["nuke"] and member.bot and member.id != MIO_ID:
        await member.kick(reason="Bot non autorizzato")

# --- COMANDI UTILITY ---
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ Eliminati {amount} messaggi.", delete_after=3)

bot.run(TOKEN)
