import return_content as con

async def modify_subreddit(choice, subreddit, message, client, channel):
    def pred(m):
        return m.author == message.author and m.channel == message.channel

    #User interacting with the bot
    user = message.author
    
    async def add_phrase():
        #Receive phrase to add
        string_dict = con.get_stringdict()
        await send_message('What word/phrase would you like to add?')
        phrase = await receive_message(user)

        #Test if phrase is in use
        while phrase_used(phrase):
            await send_message('Word/phrase already in use. Enter another.')
            phrase = await receive_message(user)

        #Add phrase
        string_dict[phrase] = subreddit
        await send_message('Word/phrase added to subreddit.')

    async def remove_phrase():
        #Receive phrase to delete
        await send_message('What word/phrase would you like to remove?')
        phrase = await receive_message(user)

        #Test if phrase is associated with subreddit
        while con.get_subname(phrase) != subreddit:
            await send_message('Word/phrase not associated with r/' + subreddit)

            #List all phrases associated with subreddit
            enum_phrases = enumerate_matched_phrases(subreddit)
            await send_message(enum_phrases)
            
            await send_message('Which word/phrase would you like to remove?')
            msg = await receive_message(muser)

        #Remove phrase
        string_dict = con.get_stringdict()
        del string_dict[phrase]
        await send_message(phrase + ' deleted from r/' + subreddit)

        test_for_deletion(subreddit)

    async def remove_subreddit():
        delete_sub(subreddit)        
        await send_message('Subreddit removed.')
        
    async def send_message(message):
        await channel.send(message)

    async def receive_message(user):
        msg = await client.wait_for('message', check=pred)
        return msg.content.lower()

    if choice == '1':
        await add_phrase()
    elif choice == '2':
        await remove_phrase()
    elif choice == '3':
        await remove_subreddit()
        
    
    
def phrase_used(phrase):
    if phrase in con.get_stringdict():
        return True
    else:
        return False

def enumerate_matched_phrases(subreddit):
    string = 'Subreddit is matched with the phrase(s) '
    string_dict = con.get_stringdict()

    for key, value in string_dict.items():
        if subreddit == value:
            string += '"' + key + '",'
    
    return enum_phrases

def test_for_deletion(subreddit):
    found_sub = False
    sub_dict = con.get_subdict()

    #Test if any strings are attached to sub. If no strings attached to sub, delete the sub. 
    for key in sub_dict.copy():
        if subreddit == sub_dict[key]:
            found_sub = True
            break
    if not found_sub:
        delete_sub(subreddit)

def delete_sub(subreddit):
    # Delete strings associated with sub
    string_dict = con.get_stringdict()
    sub_dict = con.get_subdict()
    
    for key in string_dict.copy():
        if string_dict[key] == subreddit:
            del string_dict[key]
            
    # Delete sub from dictionary
    del sub_dict[subreddit]
    
            

            
