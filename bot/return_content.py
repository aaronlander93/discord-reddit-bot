import random
import praw
import os

reddit = praw.Reddit(client_id= os.environ.get('praw_id'),
                     client_secret=os.environ.get('praw_secret'),
                     username= os.environ.get('praw_username'),
                     password= os.environ.get('praw_password'),
                     user_agent='agent')

sub_dict = {}
string_to_sub = {}

def create_subreddit_list(subreddit, string):  
    try:
        subreddit = string_to_sub[string]
        sub_dict[subreddit]
        return    
    except:
        print('')
    content = []
    sub_obj = reddit.subreddit(subreddit)

    for submissions in sub_obj.hot(limit=30):
        if submissions.stickied:
            continue
        content.append(submissions)
    sub_dict[subreddit] = content
    string_to_sub[string] = subreddit
        
def give_subreddit_content(string):
    subreddit = string_to_sub[string]
        
    if sub_dict[subreddit]:
        last_post = random.choice(sub_dict[subreddit])
        sub_dict[subreddit].remove(last_post)
    else:
        sub_obj = reddit.subreddit(subreddit)
        content = []

        for submissions in sub_obj.hot(limit=30):
            if submissions.stickied:
                continue
            content.append(submissions)
        sub_dict[subreddit] = content

        last_post = random.choice(sub_dict[subreddit].url)
        sub_dict[subreddit].remove(last_post)
 
    url = last_post.url

    return url

def give_random_content(subreddit):
    sub_obj = reddit.subreddit(subreddit)
    content = []

    for submissions in sub_obj.hot(limit=5):
        if submissions.stickied:
            continue
        elif content:
            break
        else:
            content.append(submissions.url)
    return content[0]

def get_subname(string):
    try:
        return string_to_sub[string]
    except:
        return None

def get_subobj(string):
    try:
        return sub_dict[string]
    except:
        return None

def get_stringdict():
    return string_to_sub

def get_subdict():
    return sub_dict
    
