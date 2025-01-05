import discord
from discord.ext import commands

from utility.starboard import Starboard

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.starboard = Starboard(bot)
    
    @commands.Cog.listener(name="on_raw_reaction_add")
    async def star_added_raw(self, payload: discord.RawReactionActionEvent):
        await self.starboard.process(payload)
    
    @commands.Cog.listener(name="on_raw_reaction_remove")
    async def star_remove_raw(self, payload: discord.RawReactionActionEvent):
        await self.starboard.process(payload)
        
    @commands.Cog.listener(name="on_raw_reaction_clear")
    async def star_clear_raw(self, payload: discord.RawReactionActionEvent):
        await self.starboard.process(payload)
        
    @commands.Cog.listener(name="on_raw_reaction_clear_emoji")
    async def star_clear_emoji_raw(self, payload: discord.RawReactionActionEvent):
        await self.starboard.process(payload)
    
async def setup(bot):
    await bot.add_cog(Events(bot))
    print(f"> {__name__} loaded")
    
async def teardown(bot):
    await bot.remove_cog(Events(bot))
    print(f"> {__name__} unloaded")