import discord
import run_discord_bot as bot
import os

client = discord.Client()

while True:
    client.loop.create_task(bot.run_discord_bot(client))

    try:
        client.run(os.environ.get('bot_token'))
    except Exception as e:
        print(str(e))
 
