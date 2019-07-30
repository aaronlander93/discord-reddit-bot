import return_content as con

async def modify_subreddit(choice, subreddit, message, client, channel):
    async def one():
        string_dict = con.get_stringdict()
        await client.send_message(channel, 'What word/phrase would you like to add?')
        msg = await client.wait_for_message(author=message.author, timeout=10)

        test = msg.content in con.get_subdict()
        while test == True:
            await client.send_message(channel, 'Word/phrase already in use. Enter another.')
            msg = await client.wait_for_message(author=message.author, timeout=10)
            test = msg.content.lower() in con.get_stringdict()

        string_dict[msg.content.lower()] = subreddit
        await client.send_message(channel, 'Word/phrase added to subreddit.')

    async def two():
        await client.send_message(channel, 'What word/phrase would you like to remove?')
        msg = await client.wait_for_message(author=message.author, timeout=10)

        test = con.get_subname(msg)

        while test == None or test != subreddit:
            await client.send_message(channel, 'Word/phrase not associated with r/' + subreddit)
            string = 'Subreddit is matched with the phrase(s) '

            for key, value in con.get_stringdict().items():
                if subreddit == value:
                    string += '"' + key + '",'
            await client.send_message(channel, string)
            await client.send_message(channel, 'Which word/phrase would you like to remove?')
            msg = await client.wait_for_message(author=message.author, timeout=10)
            test = string_sub_dict.get(msg.content.lower(), None)

        del string_sub_dict[msg.content.lower()]
        await client.send_message(channel, msg.content.lower() + ' deleted from r/' + subreddit)

        found = False
        for key, value in string_sub_dict.items():
            if subreddit == value:
                found = True
                break
        if not found:
            del sub_dict[subreddit]

    async def three():
        await client.send_message(channel, 'What subreddit would you like to remove?')
        msg = await client.wait_for_message(author=message.author, timeout=10)

        subreddit = sub_dict.get(msg.content.lower(), None)

        while subreddit == None:
            await client.send_message(channel, 'Subreddit not configured with Reddit Bot. Try again.')

            await client.send_message(channel, 'What subreddit would you like to remove?')
            msg = await client.wait_for_message(author=message.author, timeout=10)

            subreddit = sub_dict.get(msg.content.lower(), None)

        # Delete strings associated with sub
        for key, value in string_sub_dict.items():
            if subreddit == value:
                del string_sub_dict[key]

        # Delete sub from dictionary
        del sub_dict[msg.content]

        await client.send_message(channel, 'Subreddit removed.')

    if choice == '1':
        await one()
    elif choice == '2':
        await two()
    elif choice == '3':
        await three()

  
