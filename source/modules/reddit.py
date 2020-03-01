import praw
import time
import requests
from datetime import datetime
import os

from source.modules import tools
from source.modules.tools import parse_link

total_downloads = 0

#save_path = tools.create_dir(r"C:\Users\workstation\PycharmProjects\lil ripper\testing")



reddit = praw.Reddit(client_id="psA2ANY3X7zdlg",
                     client_secret="LHpWLqkhYG932fAqfflSXNnCs54",
                     username="crusty_cum_socks",
                     password="OsamaBinLaden911",
                     user_agent="Python bot for learning purposes. Will read posts, get information and download associated media.")


"""
Going wild with pushshift 8-)
"""


def json_try(json_url, directory):
    """
    Takes a json url and a directory, goes over json data and downloads media using parse_link()
    :param json_url: url of json file containing post data from reddit
    :param directory: directory where downloaded files are stored
    :return:
    """
    try:
        r = requests.get(json_url)
        json_data = r.json()
        link_data = json_data["data"]
        for x in link_data:
            parse_link(x["url"], directory)
    except Exception:
        print("alayzing json has failed...")


# todo make it continue from last stopped date of that subreddit aka resume. only if settings has resume=true, since it can be buggy
def archive_subreddit(subreddit):
    """
    Basically eina nuo dabartinio timestamp iki subreddit creation date in one week interval.
    """
    day_in_seconds = 24 * 60 * 60
    save_path = tools.create_dir(tools.load_settings()["download_directory"])
    reddit_batch_size = tools.load_settings()["reddit_batch_size"]
    time_interval = tools.load_settings()["time_interval_in_days"] * day_in_seconds
    directory = tools.create_dir(os.path.join(save_path, subreddit))  # creates dir using subreddit name

    creation_date = int(reddit.subreddit(subreddit).created_utc)
    current_time = int(time.time())
    iterator = 0

    while creation_date <= current_time:
        previous_date = current_time - time_interval
        print("from {} to {} is batch {}. Batch size is {} posts.".format(datetime.utcfromtimestamp(current_time), datetime.utcfromtimestamp(previous_date), iterator, reddit_batch_size))
        json_link = "https://api.pushshift.io/reddit/search/submission/?subreddit={}&sort=desc&sort_type=created_utc&after={}&before={}&size={}".format(subreddit, previous_date, current_time, reddit_batch_size)
        json_try(json_link, directory)
        current_time -= time_interval
        iterator += 1

    print("downloaded [{}] files in this session.".format(tools.total_session_downloads))


# todo delet after testing :)
archive_subreddit("dankmemes")

# todo downloading gfycat video [https://imgur.com/TchWpq4] - nesiuncia jei ne albumas ir neturi ending iskarto.


# todo https://redgifs.com/watch/quarrelsomemadarieltoucan
#todo https://imgur.com/z5ixEXI.gifv

# todo take input arguments -> able to start multiple instances then
# input argument to use riplist.txt or just state --subreddit lithuania hentai_gifs --batch 1000
# ? first get all json files with links, extract downloadable shit and divide work
# todo multiprocessing https://www.youtube.com/watch?v=RR4SoktDQAw