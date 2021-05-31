import discord
import os
import random
from DB import database


command_detail = """
ガムトークbotで使えるコマンド一覧:

?rule - ルールの説明
?gum - 4つの話題を取得
?dice - サイコロを振る
?topics - 全ての話題を表示する
"""

rule = '「ガムトーク」は、めくったカードの中から、指定されたお題について話をするゲーム……というよりも、トーク用アイテム。話のオチはなくてオッケー、聞いた人は必ず「良い話や」と言うことになっているので、安心して話せます。"?gum"と入力してお題を引きましょう！サイコロは"?dice"で振れるよ！'


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
        await message.channel.send(rule)


    if message.content.startswith('?command') or message.content.startswith('?help'):
        await message.channel.send(command_detail)

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
        # for index, topic in enumerate(result):
        #     topic1, topic2, topic3, topic4 = topic
        #     index = index + 1
        #     topic =f"Topic {index}\n {topic1}、{topic2}、{topic3}、{topic4}\n"
        #     await message.channel.send(topic)
        # for topic in result:
        #     await message.channel.send(topic)
        print(result)
        await message.channel.send(result)


token = os.getenv("DISCORD_TOKEN")
client.run(token)
