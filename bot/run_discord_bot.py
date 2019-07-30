import return_content as content
import message_handler as handler


async def run_discord_bot(client, channel):
    @client.event
    async def on_ready():
        print('Online')

    @client.event
    async def on_message(message):
        await handler.message_handler(message, client, channel)
            
    
