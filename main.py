import discord
import run_discord_bot as bot
import os

client = discord.Client()
channel = discord.Object(id= os.environ.get('channel_id'))

while True:
    client.loop.create_task(bot.run_discord_bot(client, channel))

    try:
        client.run(os.environ.get('bot_token'))
    except Exception as e:
        print(str(e))
