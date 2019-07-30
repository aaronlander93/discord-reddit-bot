import discord
import return_content as con
import modify_subreddit as mod
import re

async def message_handler(message, client, channel):
    new_subreddit_regex = re.compile(r'^!(\w+$)')
    
    #Test if string is used to request content
    test = con.get_subname(message.content.lower())

    if message.content.lower() == '!random':
        subreddit = message.content.lower()[1:]
        content = con.give_random_content(subreddit)
        await client.send_message(channel, content)  
    elif test is not None:
        content = con.give_subreddit_content(message.content.lower())
        await client.send_message(channel, content)

    #Test if user is attempting to add subreddit using the notation '!subredditname'
    elif new_subreddit_regex.search(message.content.lower()):
        new_subreddit_regex = re.compile(r'^!(\w+$)')
        match = new_subreddit_regex.search(message.content.lower())
        subreddit = match.group(1)

        test = con.get_subobj(subreddit)

        if test is not None and test != '':
            string = 'Subreddit is already matched with the phrase(s) '

            string_dict = con.get_stringdict()
            
            for key,value in string_dict.items():
                if subreddit == value:
                    string += '"' + key + '",'
            string += ' what would you like to do?'
                        
            await client.send_message(channel, string)
            await client.send_message(channel, '\nPress 1, 2, or 3')
            await client.send_message(channel, '1. Add phrase\n2. Remove phrase\n3. Delete subreddit')
            msg = await client.wait_for_message(author=message.author, timeout=10)
            choice = msg.content

            while choice not in ('1', '2', '3'):
                await client.send_message(channel, 'Invalid choice. Try again.')
                await client.send_message(channel, '\nPress 1, 2, or 3')
                await client.send_message(channel, '1. Add phrase\n2. Remove phrase\n3. Delete subreddit')
                msg = await client.wait_for_message(author=message.author, timeout=10)
                choice = msg.content
            await mod.modify_subreddit(choice, subreddit, message, client, channel)
                
        else:
            await client.send_message(channel, 'Enter a word/comment to request content from r/' + subreddit + '.')
            msg = await client.wait_for_message(author=message.author, timeout=10)
            string = msg.content.lower()
                
            con.create_subreddit_list(subreddit, string)
            content = con.give_subreddit_content(string)
            await client.send_message(channel, content)
