from sqlite3 import connect
from turtle import title
import discord
import os
import sys
import asyncio
import time
import json
import config

from discord.ext import commands
from discord.utils import get

#bot = discord.Client()
bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())

BADWORDS = ["pizdet", "лох", "мудак", "нигер", "петух", "ватник", "москаль", "пиратка", "пидр", "педик", "гомик", "хиджаб", "хохлы", "хачи", "талибан", "игил", "гидра", "даун", "пизда", "конча", "инцел", "симп", "девственник", "девственница", "я твою маму"]
LINKS = ["https", "http", "://", ".com", ".ru", ".net", ".org", ".shop", ".ру", ".рф"]

@bot.event
async def on_ready():
    print("- АККАУНТ БОТА -")
    print()
    print(f"Имя бота: {bot.user.name}")
    print(f"ID бота: {bot.user.id}")
    print()
    #for user in bot.get_all_members():
    #    print(user)
    
    if not os.path.exists('users.json'):
        with open('users.json', 'w') as file:
            file.write('{}')
            file.close()

        for guild in bot.guilds:
            print(len(guild.members))
            for member in guild.members:
                print(member)
                with open('users.json', 'r') as file:
                    data = json.load(file)
                    file.close()

                with open('users.json', 'w') as file:
                    data[str(member.id)] = {
                        "WARNS": 0,
                        "CAPS": 0

                    }

                    json.dump(data, file, indent=4)
                    file.close()
@bot.event
async def on_message(message):
    WARN = BADWORDS + LINKS

    for i in range(0, len(WARN)):
        if WARN[i] in message.content.lower():
            await message.delete()
            with open('users.json', 'r') as file:
                data = json.load(file)
                file.close()

            with open('users.json', 'w') as file:
                data[str(message.author.id)]['WARNS'] += 1
                json.dump(data, file, indent=4)

                file.close()

            emb = discord.Embed(
                title="Нарушение",
                description=f"*Ранее, у нарушителя было уже {data[str(message.author.id)]['WARNS'] - 1} нарушений, после 7 он будет забанен!*",
                timestamp=message.created_at
            )

            emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
            emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="Ругательства/ссылки", inline=True)

            await get(message.guild.text_channels, id=959501635661471744).send(embed=emb)

            if data[str(message.author.id)]['WARNS'] >= 7:
                await message.author.ban(reason="Вы превысили допустимое кол-во нарушений!")
    if message.content.isupper(): #проверка на CAPS
        with open('users.json', 'r') as file:
            data = json.load(file)
            file.close()
        
        with open('users.json', 'w') as file:
            data[str(message.author.id)]["CAPS"] += 1
            json.dump(data, file, indent=4)

        if data[str(message.author.id)]["CAPS"] >= 3:
            with open('users.json', 'w') as file:
                print('CAPS +1') #Проверка на количество нарушений за CAPS
                data[str(message.author.id)]["CAPS"] = 0    
                data[str(message.author.id)]["WARNS"] += 1
            
                json.dump(data, file, indent=4)
                file.close()

            emb = discord.Embed(
                title="Нарушение",
                description=f"*Ранее, у нарушителя было уже {data[str(message.author.id)]['WARNS'] - 1} нарушений, после 7 он будет забанен!*",
                timestamp=message.created_at
            )

            emb.add_field(name="Канал:", value=message.channel.mention, inline=True)
            emb.add_field(name="Нарушитель:", value=message.author.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="КАПС", inline=True)

            await get(message.guild.text_channels, id=959501635661471744).send(embed=emb)
            
            if data[str(message.author.id)]['WARNS'] >= 7:
                await message.author.ban(reason="Вы превысили допустимое кол-во нарушений!") 
    await bot.process_commands(message)
    
@bot.command()
@commands.has_permissions(manage_channels=True)
async def warn(ctx, member: discord.Member, reason: str):
    if reason.lower() == "badwords" or reason.lower() == "links":
        with open('users.json', 'r') as file:
            data = json.load(file)

            file.close()

        with open('users.json', 'w') as file:
            data[str(member.id)]['WARNS'] += 1
            json.dump(data, file, indent=4)
        
            file.close()
        
        emb = discord.Embed(
            title="Нарушение",
            description=f"*Ранее, у нарушителя было уже {data[str(member.id)]['WARNS'] - 1} нарушений, после 7 он будет забанен!*",
            timestamp=ctx.message.created_at
        )

        emb.add_field(name="Канал:", value='канал не определен', inline=True)
        emb.add_field(name="Нарушитель:", value=member.mention, inline=True)
        emb.add_field(name="Тип нарушения:", value="Ругательства/ссылки", inline=True)

        await get(ctx.guild.text_channels, id=959501635661471744).send(embed=emb)

        if data[str(member.id)]['WARNS'] >= 7:
            await member.ban(reason="Вы превысили допустимое кол-во нарушений!")
        
        await ctx.message.reply(embed=discord.Embed(
            title="Успешно",
            description="*Предупреждение выдано*",
            timestapm=ctx.message.created_at
        ))

    elif reason.lower() == "caps":
        with open('users.json', 'r') as file:
            data = json.load(file)

            file.close()
        
        with open('users.json', 'w') as file:
            data[str(member.id)]['WARNS'] += 1
            json.dump(data, file, indent=4)
            
            file.close()

            emb = discord.Embed(
                title="Нарушение",
                description=f"*Ранее, у нарушителя было уже {data[str(member.id)]['WARNS'] - 1} нарушений, после 7 он будет забанен!*",
                timestamp=ctx.message.created_at
            )

            emb.add_field(name="Канал:", value='канал не определен', inline=True)
            emb.add_field(name="Нарушитель:", value=member.mention, inline=True)
            emb.add_field(name="Тип нарушения:", value="КАПС", inline=True)

            await get(ctx.message.guild.text_channels, id=959501635661471744).send(embed=emb)
            
            if data[str(member.id)]['WARNS'] >= 7:
                await member.ban(reason="Вы превысили допустимое кол-во нарушений!")
    else:
        await ctx.message.reply(embed=discord.Embed(
            title="Ошибка",
            description="Не правильная причина!",
            timestamp=ctx.message.created_at    
        ))

@warn.error
async def error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description="*Использование: .warn (@Участник) (Причина)*",
            timestamp=ctx.message.created_at
        ))

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=discord.Embed(
            title="Ошибка",
            description="*У вас недостаточно прав!*",
            timestamp=ctx.message.created_at
        ))

@bot.command()
@commands.has_permissions(manage_channels=True)
async def unwarn(ctx, member: discord.Member):
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()

    with open('users.json', 'w') as file:
        data[str(member.id)]['WARNS'] -= 1
        json.dump(data, file, indent=4)

        file.close()

        del data   

@bot.command()
@commands.has_permissions(administrator=True)
async def clear_warns(ctx, member: discord.Member):
    with open('users.json', 'r') as file:
        data = json.load(file)
        file.close()

    with open('users.json', 'w') as file:
        data[str(member.id)]['WARNS'] = 0
        json.dump(data, file, indent=4)

        file.close()
    
  
bot.run(config.TOKEN)
