import discord
import os
import random
from DB import database


topic_list = [
    ['アイスクリームの話', '職務質問された話', '親友の話', '昆虫の話'],
    ['ネタバレした話', '悪役の話', '乗り物の話', '謎の話'],
    ['移動の話', '包丁の話', 'みかんの話', 'リコーダーの話'],
    ['最近読んだ本の話', '映画の話', '地元の話', '占いの話'],
    ['麻婆豆腐の話', '名前を間違えた話', '休暇の話', '落ち葉の話'],
    ['冬休みの話', 'アレルギーの話', '意識高い話', '記憶の話'],
    ['サウナの話', '犬の話', 'お正月の話', '昆布の話'],
    ['配信の話', 'とろろの話', 'ライオンの話', '冬の話'],
    ['ジブリの話', '夏の話', '先月の話', 'パチンコの話'],
]

command_detail = """
ガムトークbotで使えるコマンド一覧:

?rule - ルールの説明
?gum - 4つの話題を取得
?dice - サイコロを振る
?topics - 全ての話題を表示する
"""

def get_topic(topic_list):
    topic_num = random.randint(0, len(topics) - 1)
    topic = topics[topic_num]
    return topic

def get_all_topics(topic_list):
    return topic_list

rule = '「ガムトーク」は、めくったカードの中から、指定されたお題について話をするゲーム……というよりも、トーク用アイテム。話のオチはなくてオッケー、聞いた人は必ず「良い話や」と言うことになっているので、安心して話せます。"?gum"と入力してお題を引きましょう！サイコロは"?dice"で振れるよ！'


def dice():
    return random.randint(1, 4)

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
        topic = get_topic(topics)
        for index, topic in enumerate(topic):
            topic = f"{index}: {topic}"
            await message.channel.send(topic)

    if message.content.startswith('?dice'):
        dice_num = dice()
        await message.channel.send(dice_num)

    if message.content.startswith('?rule'):
        await message.channel.send(rule)

    if message.content.startswith('?topics'):
        all_topics = get_all_topics(topic_list)
        for index, topic in enumerate(all_topics):
            topic1, topic2, topic3, topic4 = topic
            index = index + 1
            topic =f"Topic {index}\n {topic1}、{topic2}、{topic3}、{topic4}\n"
            await message.channel.send(topic)

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

    if message.content.startswith('?all_topics'):
        db = database(get_server_table(message.guild.id))
        result = db.get_topics()
        await message.channel.send(result)
        # for topic in result:
        #     await message.channel.send(topic)


token = os.getenv("DISCORD_TOKEN")
client.run(token)
