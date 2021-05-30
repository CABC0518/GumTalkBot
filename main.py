import discord
import os
import random


def get_topics():
    topics = [
        ['1: アイスクリームの話', '2: 職務質問された話', '3:親友の話', '4: 昆虫の話'],
        ['1: ネタバレした話', '2: 悪役の話', '3:乗り物の話', '4: 謎の話'],
        ['1: 移動の話', '2: 包丁の話', '3: みかんの話', '4: リコーダーの話'],
        ['1: 最近読んだ本の話', '2: 映画の話', '3:地元の話', '4: 占いの話'],
        ['1: 麻婆豆腐の話', '2: 名前を間違えた話', '3: 休暇の話', '4: 落ち葉の話'],
        ['1: 冬休みの話', '2: アレルギーの話', '3: 意識高い話', '4: 記憶の話'],
        ['1: サウナの話', '2: 犬の話', '3: お正月の話', '4: 昆布の話'],
        ['1: 配信の話', '2: ととろの話', '3: ライオンの話', '4: 冬の話'],
        ['1: ジブリの話', '2: 夏の話', '3: 先月の話', '4: パチンコの話'],
    ]
    topic_num = random.randint(0, len(topics) - 1)
    topic = topics[topic_num]
    return topic


rule = '「ガムトーク」は、めくったカードの中から、指定されたお題について話をするゲーム……というよりも、トーク用アイテム。話のオチはなくてオッケー、聞いた人は必ず「良い話や」と言うことになっているので、安心して話せます。"?gum"と入力してお題を引きましょう！サイコロは"?dice"で振れるよ！'


def dice():
    return random.randint(1, 4)


client = discord.Client()


@client.event
async def on_ready():
    print(f"We have logged in")
    get_topics()


@client.event
async def on_message(message):
    if message.author == client:
        return

    if message.content.startswith('?gum'):
        topics = get_topics()
        for topic in topic:
            await message.channel.send(topics)

    if message.content.startswith('?dice'):
        dice_num = dice()
        await message.channel.send(dice_num)

    if message.content.startswith('?rule'):
        await message.channel.send(rule)

if message.content.startswith('?topics'):
    topics = get_topics()
    await message.channel.send(topics)

token = os.getenv("DISCORD_TOKEN")
client.run(token)
