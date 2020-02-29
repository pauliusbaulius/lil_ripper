import praw
from modules import tools
from modules.tools import parse_link
import time


"""
Using reddit api and being limited to 1k posts.
"""


reddit = praw.Reddit(client_id="psA2ANY3X7zdlg",
                     client_secret="LHpWLqkhYG932fAqfflSXNnCs54",
                     username="crusty_cum_socks",
                     password="OsamaBinLaden911",
                     user_agent="Python bot for learning purposes. Will read posts, get information and download associated media.")


@DeprecationWarning
def rip_subreddits(list_subreddits):
    for subreddit in list_subreddits:
        rip_subreddit(subreddit)


@DeprecationWarning
def rip_subreddit(name, save_path, amount_posts=None):
    subreddit = reddit.subreddit(name)
    posts = subreddit.top(limit=amount_posts)
    directory = tools.create_dir(save_path, subreddit.display_name)  # creates dir using subreddit name
    for post in posts:
        time.sleep(0.5) # sleep for .5 sec
        parse_link(post.url, subreddit.display_name)



