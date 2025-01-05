import discord
from datetime import datetime
from discord.ext import commands
from discord import app_commands

from database.mongoclient import StarchaserClient

class Commands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot
        self.client: StarchaserClient() = StarchaserClient(bot)
    
    @app_commands.command(name="starboard", description="Set the Starboard channel")
    @app_commands.default_permissions(manage_channels=True)
    async def starboard(self, interaction: discord.Interaction, channel: discord.TextChannel):
        
        db_guild = await self.client.get_guild(interaction.guild.id)
        settings = db_guild.settings
        
        if "stars" not in settings:
            settings["stars"] = 3
        
        stars = settings["stars"]
        
        embed = discord.Embed(
            title="Starboard",
            description="",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(
            name="<:helioschevronright:1267515447406887014> Starboard-Channel",
            value=f"> - {channel.mention} <:edit:1210725875625099304>",
            inline=False
        )
        embed.add_field(
            name="<:heliosmedal:1267515459012657245> Stars needed per Message",
            value=f"> - {stars} :star:",
            inline=False
        )
        
        settings["starboard_channel"] = channel.id
        
        db_guild.settings = settings
        
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="stars", description="Set the needed stars")
    @app_commands.default_permissions(manage_channels=True)
    async def stars(self, interaction: discord.Interaction, stars: int):
        
        starboard_channel = None
        
        db_guild = await self.client.get_guild(interaction.guild.id)
        settings = db_guild.settings
        
        if "starboard_channel" not in settings:
            settings["starboard_channel"] = None
            
        if settings["starboard_channel"] is not None:
            starboard_channel = self.bot.get_channel(settings["starboard_channel"])
        
        embed = discord.Embed(
            title="Starboard",
            description="",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.add_field(
            name="<:helioschevronright:1267515447406887014> Starboard-Channel",
            value=f"> - {starboard_channel.mention if starboard_channel is not None else "Not Set (set with `/starboard`)"}",
            inline=False
        )
        embed.add_field(
            name="<:heliosmedal:1267515459012657245> Stars needed to be starred",
            value=f"> - {stars} :star: <:edit:1210725875625099304>",
            inline=False
        )
        
        settings["stars"] = stars
        
        db_guild.settings = settings
        
        await interaction.response.send_message(embed=embed)
        
    @app_commands.command(name="about", description="About me")
    async def about(self, interaction: discord.Interaction):        
        embed = discord.Embed(
            title=f"About {self.bot.user.name}",
            color=discord.Color.blue(),
            description="",
            timestamp=datetime.now(),
        )
        
        embed.add_field(
            name="<:info:1226139199351296051> General Information",
            value=f"> - `Bot Name:` *{self.bot.user.name}#{self.bot.user.discriminator}*" + 
                f"\n> - `Bot ID:` *{self.bot.user.id}*" +
                "\n> - `Developer:` *.smplx*" + 
                "\n> - `Developer ID:` *579111799794958377*",
            inline=False
        )
        
        embed.add_field(
            name="<:info:1226139199351296051> Links",
            value="> - [GitHub](https://github.com/SimplexDE/Starchaser)" \
                "\n> - [Invite me](https://discord.com/oauth2/authorize?client_id=881186799538540565&permissions=322560&integration_type=0&scope=applications.commands+bot)",
            inline=False
        )
        
        embed.set_author(name="🧑‍💻 Simplex", url="https://discord.com/users/881186799538540565")
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Licsensed under MIT", icon_url=self.bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)
    
async def setup(bot):
    await bot.add_cog(Commands(bot))
    print(f"> {__name__} loaded")
    
async def teardown(bot):
    await bot.remove_cog(Commands(bot))
    print(f"> {__name__} unloaded")