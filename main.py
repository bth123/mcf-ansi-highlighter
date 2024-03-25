from hl import Hl

import discord
from discord.ext import commands
from discord import app_commands

class TheBot(commands.Bot):
	def __init__(self, *, intents: discord.Intents, command_prefix: str):
		super().__init__(intents=intents, command_prefix=command_prefix)

	async def setup_hook(self):
		await self.tree.sync()
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
hl_bot = TheBot(intents=intents, command_prefix="$")


class HlModal(discord.ui.Modal):
	def __init__(self):
		super().__init__(title="Highlight")

	string = discord.ui.TextInput(
		label="Function",
		style=discord.TextStyle.long,
		placeholder="say gex",
		max_length=1999
	)
	async def on_submit(self, ctx: discord.Interaction):
		hl_ed = f"```ansi\n{Hl.highlight(self.string.value)}\n```"
		if len(hl_ed) <= 2000:
			await ctx.response.send_message(hl_ed)
		else:
			await ctx.response.send_message("Output is too long", ephemeral=True)

@hl_bot.tree.command(name="hl", description="Highlights your mcfunctions")
@app_commands.user_install()
@app_commands.allow_contexts(guilds=True, dms=True, private_channels=True)
async def hl(ctx: discord.Interaction):
	await ctx.response.send_modal(HlModal())

hl_bot.run("MGIyNRsaY1GeXbRbRyzaL1gT8Uwu.l_jk5g.9_ZOvhTeFp2pTUwUiL14bJK88rYZenC0ReYn69p")
