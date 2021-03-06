import discord
from discord.ext import commands

import time

from assets import UrbanDict, count_lines, time_calc


class Info(commands.Cog, description='Returns information about specific aspects of the server, bot, or a user.\n'
                                     r'Maybe does even more, idk. ¯\_(ツ)_/¯'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', description='Returns the latency in milliseconds.')
    async def ping_command(self, ctx):
        before = time.monotonic()
        message = await ctx.reply("Pong!")
        ping_time = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong! `Latency: {int(ping_time)}ms`")

    @commands.command(name='countlines', aliases=['countline'], description='Counts the number of lines of python code '
                                                                            'the bot currently has.')
    async def countlines_func(self, ctx):
        lines = count_lines.countlines('./')
        final_str = f"I am made of {lines} lines of python code. Pretty cool, imo."
        await ctx.send(final_str)

    @commands.command(name='userid', description='Returns the User\'s ID mentioned. '
                                                 'Returns author\'s ID if no argument is given.')
    async def userid(self, ctx, target: discord.Member = None):
        if target:
            await ctx.reply(target.id)
        else:
            await ctx.reply(ctx.author.id)

    @commands.command(name='avatar', description='Returns the avatar/pfp of the user mentioned.')
    async def get_avatar(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author
        embed = discord.Embed(
            title=f'Avatar of {user.name}'
        ).set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo', description='Returns basic information about the server.')
    @commands.guild_only()
    async def serverinfo(self, ctx):
        guild_name = ctx.guild.name
        guild_id = ctx.guild.id
        owner = str(ctx.guild.owner.name)
        description = f'Server ID: {guild_id}'
        thumb_url = str(ctx.guild.icon_url)
        role_count = str(len(ctx.guild.roles) - 1)
        bots_count = len([bot.mention for bot in ctx.guild.members if bot.bot])
        categories_list = len(list(ctx.guild.categories))
        channels_list = "{:,} text, {:,} voice".format(len(ctx.guild.text_channels), len(ctx.guild.voice_channels))
        created_details = ctx.guild.created_at
        created_date, created_time = time_calc.parse_utc(str(created_details))
        members = ctx.guild.member_count
        emojis_count = len(ctx.guild.emojis)
        booster_role = str(ctx.guild.premium_subscriber_role)
        boost_tier = str(ctx.guild.premium_tier)
        boost_count = str(ctx.guild.premium_subscription_count)

        embed = discord.Embed(title=guild_name, description=description, timestamp=ctx.message.created_at,
                              color=discord.Color.random())
        embed.set_thumbnail(url=thumb_url)
        embed.add_field(name='Owner', value=owner, inline=True)
        embed.add_field(name='Members', value=members, inline=True)
        embed.add_field(name='No. of roles', value=role_count, inline=True)
        embed.add_field(name='Date of creation', value=str(created_date), inline=True)
        embed.add_field(name='Time of creation', value=str(created_time), inline=True)
        embed.add_field(name='Channel Categories', value=str(categories_list), inline=True)
        embed.add_field(name='Channels', value=str(channels_list), inline=True)
        embed.add_field(name='Booster Role', value=booster_role, inline=True)
        embed.add_field(name='Boost Tier', value=f'Tier {boost_tier}')
        embed.add_field(name='No. of Boosts', value=boost_count)
        embed.add_field(name='Emojis', value=str(emojis_count), inline=True)
        embed.add_field(name='Bots', value=str(bots_count))
        embed.set_footer(text=f'Command requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='roleinfo', description='Returns basic information about the role mentioned as argument.')
    @commands.guild_only()
    async def role_info(self, ctx, role: discord.Role):
        role_name = role.name
        role_id = role.id
        role_creation_date, role_creation_time = time_calc.parse_utc(str(role.created_at))
        members_count = len(role.members)
        is_mentionable = str(role.mentionable)
        role_color = role.color
        embed = discord.Embed(title=f'Role: {role_name}', description=f'ID: {role_id} | Color: {role_color}',
                              timestamp=ctx.message.created_at, color=role_color)
        embed.add_field(name='Creation Date', value=role_creation_date, inline=True)
        embed.add_field(name='Creation Time', value=role_creation_time, inline=True)
        embed.add_field(name='No. of members', value=str(members_count), inline=True)
        embed.add_field(name='Mentionable', value=is_mentionable, inline=False)
        embed.set_footer(text=f'Command requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='userinfo', aliases=['user'], description='Returns basic information about the user mentioned as argument.')
    @commands.guild_only()
    async def user_info(self ,ctx, user: discord.Member):
        name = user.display_name
        color = user.color
        id = user.id
        bot_bool = user.bot
        username = user.name
        avatar = user.avatar_url
        creation_date, creation_time = time_calc.parse_utc(str(user.created_at))
        try:
            mutual_guilds = len(user.mutual_guilds)
        except:
            mutual_guilds = 0

        embed = discord.Embed(title=name, description=f'ID: {id}', color=color, timestamp=ctx.message.created_at)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text=f'Command requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        embed.add_field(name='Username', value=str(username), inline=True)
        embed.add_field(name='Is a Bot', value=bot_bool)
        embed.add_field(name='Color', value=color, inline=True)
        embed.add_field(name='Account Creation Date', value=creation_date, inline=True)
        embed.add_field(name='Creation Time', value=creation_time, inline=True)
        embed.add_field(name=f'Mutual Servers with {self.bot.user.name}', value=str(mutual_guilds), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name='emojiinfo', description='Returns information about the emoji, passed as argument')
    async def emoji_info(self, ctx, emoji: discord.Emoji):
        emoji = ctx.author if not emoji else emoji
        emoji_name = emoji.name
        guild = emoji.guild
        available_for_use = emoji.available
        creation_date, creation_time = time_calc.parse_utc(str(emoji.created_at))
        emoji_id = emoji.id
        emoji_url = emoji.url
        creator = emoji.user

        embed = discord.Embed(title=emoji_name, description=f'ID: {emoji_id}', color=discord.Color.random())
        embed.set_thumbnail(url=emoji_url)
        embed.add_field(name='Source Server', value=guild, inline=True)
        embed.add_field(name='Creator', value=creator, inline=True)
        embed.add_field(name="Is available", value=available_for_use, inline=True)
        embed.add_field(name='Date of creation', value=creation_date, inline=True)
        embed.add_field(name='Time of creation', value=creation_time, inline=True)
        embed.set_footer(text=f'Command requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name='define', description='Pulls a description from Urban Dictionary of the term entered as '
                                                 'argument.\n '
                                                 'Take caution, as sometimes it can be a bit... too accurate.')
    async def define_from_urban(self, ctx, *, term):
        try:
            word, definition, likes, dislikes, example, author = await UrbanDict.define(term)
        except:
            await ctx.send(f'Could not load definition for **{term}**.')
            return
        embed = discord.Embed(title=word, description=definition, color=discord.Color.random())
        embed.set_footer(text=f'Powered by UrbanDictionary | Author - {author}')
        embed.add_field(name="Example", value=example, inline=False)
        embed.add_field(name='Likes', value=f"👍 {likes} | 👎 {dislikes}", inline=True)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
