import discord
import os
import random
from DB import database

def dice():
    return random.randint(1, 5)

def get_command(command_detail):
    return command_detail

client = discord.Client()

def get_server_table(guild_id):
    return 'table_' + str(guild_id)

@client.event
async def on_guild_join(guild):
    server_table = get_server_table(guild.id)
    db = database(server_table)
    db.create_table()
    db.insert_default_topics()
    with open('command.txt', 'r') as file:
        data = file.read()
        await message.channel.send(data)

@client.event
async def on_ready():
    print(f"We have logged in")

@client.event
async def on_message(message):
    if message.author == client:
        return

    if message.content.startswith('?gum'):
        db = database(get_server_table(message.guild.id))
        topic_set = db.get_topic_set()
        for index, topic in enumerate(topic_set):
            index += 1
            topic = f"{index}: {topic}"
            await message.channel.send(topic)


    if message.content.startswith('?dice'):
        dice_num = dice()
        await message.channel.send(dice_num)

    if message.content.startswith('?rule'):
        with open('rule.txt', 'r') as file:
            data = file.read()
            await message.channel.send(data)


    if message.content.startswith('?command') or message.content.startswith('?help'):
        with open('command.txt', 'r') as file:
            data = file.read()
            await message.channel.send(data)

    if message.content.startswith('?add '):
        topic = "'" + message.content.split()[1] + "'"
        db = database(get_server_table(message.guild.id))
        db.insert_topic(topic)
        await message.channel.send(f"{topic}を追加しました")

    if message.content.startswith('?remove '):
        topic = "'" + message.content.split()[1] + "'"
        db = database(get_server_table(message.guild.id))
        db.remove_topic(topic)
        await message.channel.send(f"{topic}を削除しました")

    if message.content.startswith('?topics'):
        db = database(get_server_table(message.guild.id))
        result = db.get_all_topics()
        await message.channel.send(result)


token = os.getenv("DISCORD_TOKEN")
client.run(token)
