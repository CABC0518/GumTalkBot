import discord
import os
import random
from DB import database

def dice():
    return random.randint(1, 5)

client = discord.Client()


# take discord server id and return table name ("table_ + id")
def get_server_table(guild_id):
    return 'table_' + str(guild_id)

# when the bot joins a  new server, it creates a new table for it and inserts default topics in it.
# Before inserting, all topics will be deleted to avoid dupulicats (when the bot rejoins a server for some reasons)
@client.event
async def on_guild_join(guild):
    try:
        server_table = get_server_table(guild.id)
        db = database(server_table)
        db.create_table()
        db.delete_all_topics()
        db.insert_default_topics()
    except Exception as e:
        print(e)

# when a bot is ready, this will be executed
@client.event
async def on_ready():
    print(f"We have logged in")

# This function defines what the bot will return when the specific messages are sent by users
@client.event
async def on_message(message):
    if message.author == client:
        return

# get a set of random topics from database and send it to users
    if message.content.startswith('?gum'):
        try:
            db = database(get_server_table(message.guild.id))
            topic_set = db.get_topic_set()
            for index, topic in enumerate(topic_set):
                index += 1
                topic = f"{index}: {topic}"
                await message.channel.send(topic)
        except Exception as e:
            print(e)

# get a random number and send it to users
    if message.content.startswith('?dice'):
        dice_num = dice()
        await message.channel.send(dice_num)

# get rule text from rule.txt and send it to users
    if message.content.startswith('?rule'):
        with open('rule.txt', 'r') as file:
            data = file.read()
            await message.channel.send(data)

# get command text from command.txt and send it to users
    if message.content.startswith('?command') or message.content.startswith('?help'):
        with open('command.txt', 'r') as file:
            data = file.read()
            await message.channel.send(data)

    if message.content.startswith('?add '):
        # The topic string will have '' which is required to insert into database
        topic = "'" + message.content.split()[1] + "'"
        try:
            db = database(get_server_table(message.guild.id))
            db.insert_topic(topic)
            await message.channel.send(f"{topic}を追加しました")
        except:
            print(e)

    if message.content.startswith('?remove '):
        # The topic string will have '' which is required to insert into database
        topic = "'" + message.content.split()[1] + "'"
        try:
            db = database(get_server_table(message.guild.id))
            db.remove_topic(topic)
            await message.channel.send(f"{topic}を削除しました")
        except Exception as e:
            print(e)

    if message.content.startswith('?topics'):
        try:
            db = database(get_server_table(message.guild.id))
            result = db.get_all_topics()
            await message.channel.send(result)
        except Exception as e:
            print(e)


token = os.getenv("DISCORD_TOKEN")
client.run(token)
