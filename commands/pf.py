import discord
import json
from discord.ext import commands
from core.classes import Cog_Extension

with open('./settings/botSetting.json') as SettingFile:
    SettingData = json.load(SettingFile)

with open('./settings/prefix.json', mode='r', encoding='utf8') as pfFile:
    pfData = json.load(pfFile)

def rnick(member):
    return pfData['prefix'] + member.name[:32-len(pfData['prefix'])]

def save(data):
    with open('./settings/prefix.json', mode='r', encoding='utf8') as pfFile:
        json.dump(pfData, pfFile, sort_keys=True, indent=4, ensure_ascii=False)

class pf(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        BotName = SettingData['BotName']
        print(f'{BotName} is on ready')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for member in guild.members:
            if member.id not in pfData['blacklist'] and not str(member.nick).startswith(pfData['prefix']):
                try:
                    await member.edit(nick=rnick(member))
                except:
                    pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.id not in pfData['blacklist']:
            await member.edit(nick=rnick(member))

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if not str(before.display_name).startwith(pfData['prefix']) and before.id not in pfData['blacklist'] and before.id not in pfData['blacklist']:
            await before.member.edit(nick=rnick(after))

    @commands.has_guild_permissions(administrator=True)
    @commands.command()
    async def pf_setup(self, ctx):
        for member in ctx.guild.members:
            if member.id not in pfData['blacklist'] and not str(member.nick).startswith(pfData['prefix']):
                try:
                    await member.edit(nick=rnick(member))
                except:
                    pass

    @commands.has_guild_permissions(administrator=True)
    @commands.command()
    async def bladd(self, ctx, mid):
        if mid.isdigit():
            mid = int(mid)
            pfData['blacklist'].append(mid)
            save(pfData)

    @commands.has_guild_permissions(administrator=True)
    @commands.command()
    async def blrem(self, ctx, mid):
        if mid.isdigit():
            mid = int(mid)
            pfData['blacklist'].remove(mid)
            save(pfData)

    @commands.has_guild_permissions(administrator=True)
    @commands.command()
    async def blrem(self, ctx, prefixstr):
        pfData['prefix'] = prefixstr
        save(pfData)

def setup(bot):
    bot.add_cog(pf(bot))