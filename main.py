"""DealVault Discord bot with simple commands.

Install: pip install -U discord.py
Start by setting the DISCORD_TOKEN environment variable.
"""

import os
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

TOKEN_FILE = Path(__file__).with_name("token.env")
load_dotenv(TOKEN_FILE)

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
if not DISCORD_TOKEN and TOKEN_FILE.is_file():
	DISCORD_TOKEN = TOKEN_FILE.read_text(encoding="utf-8").strip()

TESTI = {
	"en": {
			"nome_aiuto": "/help",
		"nome_ping": "/ping",
		"nome_server": "/server",
		"nome_userinfo": "/userinfo",
		"comando_aiuto": "Show available commands",
		"comando_ping": "Check bot latency",
		"comando_server": "Show server information",
		"comando_userinfo": "Display detailed information about a user",
		"ping": "Pong! Latency: {ms} ms.",
		"ping_titolo": "Bot latency",
		"aiuto": "Available commands",
		"server": "Server information",
		"server_name": "Name",
		"server_members": "Members",
		"server_owner": "Owner",
		"server_boosts": "Boosts",
		"server_created": "Created",
		"server_description": "Description",
		"server_boosts_yes": "Yes - Tier {livello} ({numero} boosts)",
		"server_boosts_no": "No boosts",
		"server_no_description": "No description provided.",
		"errore": "Something went wrong. Please try again later.",
	},
}


def testo(utente_id, chiave, **valori):
	return TESTI["en"][chiave].format(**valori)


class DealVaultBot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix="!", intents=discord.Intents.default())

	async def setup_hook(self):
		await self.tree.sync()

	async def on_ready(self):
		print(f"Bot online: {self.user}")


bot = DealVaultBot()


@bot.tree.command(name="ping", description="Check bot latency")
async def ping(interaction: discord.Interaction):
	embed = discord.Embed(
		title=testo(interaction.user.id, "ping_titolo"),
		description=testo(interaction.user.id, "ping", ms=round(bot.latency * 1000)),
		color=discord.Color.green(),
	)
	await interaction.response.send_message(embed=embed)


async def esegui_aiuto(interaction: discord.Interaction):
	testo_lingua = TESTI["en"]
	embed = discord.Embed(title=testo_lingua["aiuto"], color=0x5865F2)
	embed.add_field(name=testo_lingua["nome_aiuto"], value=testo_lingua["comando_aiuto"], inline=False)
	embed.add_field(name=testo_lingua["nome_ping"], value=testo_lingua["comando_ping"], inline=False)
	embed.add_field(name=testo_lingua["nome_server"], value=testo_lingua["comando_server"], inline=False)
	embed.add_field(name=testo_lingua["nome_userinfo"], value=testo_lingua["comando_userinfo"], inline=False)
	await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="help", description="Show available commands")
async def help_command(interaction: discord.Interaction):
	await esegui_aiuto(interaction)


@bot.tree.command(name="server", description="Show server information")
async def server(interaction: discord.Interaction):
	if interaction.guild is None:
		embed = discord.Embed(
			title=testo(interaction.user.id, "server"),
			description="Use this command in a server.",
			color=discord.Color.red(),
		)
		await interaction.response.send_message(embed=embed, ephemeral=True)
		return
	embed = discord.Embed(
		title=testo(interaction.user.id, "server"),
		color=discord.Color.blurple(),
	)
	embed.add_field(name=testo(interaction.user.id, "server_name"), value=interaction.guild.name, inline=False)
	embed.add_field(name=testo(interaction.user.id, "server_members"), value=str(interaction.guild.member_count), inline=False)
	owner = interaction.guild.owner
	owner_value = owner.mention if owner else f"<@{interaction.guild.owner_id}>"
	boosts = interaction.guild.premium_subscription_count or 0
	boost_value = testo(
		interaction.user.id,
		"server_boosts_yes",
		livello=interaction.guild.premium_tier,
		numero=boosts,
	) if boosts else testo(interaction.user.id, "server_boosts_no")
	embed.add_field(name=testo(interaction.user.id, "server_owner"), value=owner_value, inline=False)
	embed.add_field(name=testo(interaction.user.id, "server_boosts"), value=boost_value, inline=False)
	embed.add_field(
		name=testo(interaction.user.id, "server_created"),
		value=f"<t:{int(interaction.guild.created_at.timestamp())}:F>",
		inline=False,
	)
	embed.add_field(
		name=testo(interaction.user.id, "server_description"),
		value=interaction.guild.description or testo(interaction.user.id, "server_no_description"),
		inline=False,
	)
	if interaction.guild.icon:
		embed.set_thumbnail(url=interaction.guild.icon.url)
	await interaction.response.send_message(embed=embed)


@bot.event
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
	messaggio = testo(interaction.user.id, "errore")
	if interaction.response.is_done():
		await interaction.followup.send(messaggio, ephemeral=True)
	else:
		await interaction.response.send_message(messaggio, ephemeral=True)
	print(f"Command error: {error}")


@bot.tree.command(name="userinfo", description="Display detailed information about a user")
@app_commands.describe(member="The user you want to inspect (optional)")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    target = member or interaction.user
    
    embed = discord.Embed(
        title=f"👤 User Profile: {target.display_name}",
        color=target.color
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="Full Name", value=str(target), inline=True)
    embed.add_field(name="ID", value=target.id, inline=True)
    embed.add_field(name="Account Created", value=f"<t:{int(target.created_at.timestamp())}:R>", inline=False)
    
    if isinstance(target, discord.Member) and target.joined_at:
        embed.add_field(name="Joined Server", value=f"<t:{int(target.joined_at.timestamp())}:R>", inline=False)
        roles = [role.mention for role in target.roles if role.name != "@everyone"]
        embed.add_field(
            name=f"Roles ({len(roles)})", 
            value=" ".join(roles) if roles else "No custom roles", 
            inline=False
        )
        
    await interaction.response.send_message(embed=embed)

async def setup_hook(self):
    print("Syncing commands...")
    await self.tree.sync() # Registers commands globally
    print("Command synchronization complete!")

if __name__ == "__main__":
	if not DISCORD_TOKEN:
		raise RuntimeError("Set the DISCORD_TOKEN environment variable before starting the bot.")
	bot.run(DISCORD_TOKEN)
