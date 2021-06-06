import discord
import json
import os
from discord.ext import commands

with open('./settings/botSetting.json') as SettingFile:
    SettingData = json.load(SettingFile)

with open('./settings/token.json') as TokenFile:
    TokenData = json.load(TokenFile)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=SettingData['Prefix'], intents=intents)

for Filename in os.listdir(r'.\commands'):
    if Filename.endswith('.py'):
        bot.load_extension(f'commands.{Filename[:-3]}')

if __name__ == "__main__":
    bot.run(TokenData['Token'])