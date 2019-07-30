import discord
import return_content as con
import modify_subreddit as mod
import re

async def message_handler(message, client, channel):
    def pred(m):
        return m.author == message.author and m.channel == message.channel
    
    new_subreddit_regex = re.compile(r'^!(\w+$)')
    msg = message.content.lower()

    subreddit = con.get_subname(msg)

    #Test if user wants random content.
    if msg == '!random':
        subreddit = msg[1:]
        content = con.give_random_content(subreddit)
        await channel.send(content)

    #User is requesting content with previously mapped phrase.
    elif subreddit is not None:
        content = con.give_subreddit_content(msg)
        await channel.send(content)
        
    #Test if user is attempting to add subreddit using the notation '!subredditname'
    elif new_subreddit_regex.search(msg):
        match = new_subreddit_regex.search(msg)
        subreddit = match.group(1)

        sub_test = con.get_subobj(subreddit)

        #Subreddit already mapped. Assuming user wants to modify subreddit.
        if sub_test is not None and sub_test != '':
            string = enumerate_phrases(subreddit)            
            await channel.send(string)

            #Prompt for modification options
            await channel.send('\nPress 1, 2, or 3\n1. Add phrase\n2. Remove phrase\n3. Delete subreddit')
            msg = await client.wait_for('message', check=pred)
            choice = msg.content

            while choice not in ('1', '2', '3'):
                await channel.send('Invalid choice. Try again.\nPress 1, 2, or 3\n1. Add phrase\n2. Remove phrase\n3. Delete subreddit')
                msg = await client.wait_for('message', check=pred)
                choice = msg.content
            await mod.modify_subreddit(choice, subreddit, message, client, channel)

        #New subreddit. Receive phrase to match to subreddit.   
        else:
            await channel.send('Enter a word/comment to request content from r/' + subreddit + '.')
            msg = await client.wait_for('message', check=pred)
            string = msg.content.lower()
                
            con.create_subreddit_list(subreddit, string)
            content = con.give_subreddit_content(string)
            await channel.send(content)

    
def enumerate_phrases(subreddit):
    string = 'Subreddit is already matched with the phrase(s) '
    string_dict = con.get_stringdict()
            
    for key,value in string_dict.items():
        if subreddit == value:
            string += '"' + key + '",'
    string += ' what would you like to do?'
    return string
