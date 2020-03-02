import praw
import time
import requests
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




# todo downloading gfycat video [https://imgur.com/TchWpq4] - nesiuncia jei ne albumas ir neturi ending iskarto.


# todo https://redgifs.com/watch/quarrelsomemadarieltoucan
#todo https://imgur.com/z5ixEXI.gifv

# todo take input arguments -> able to start multiple instances then
# input argument to use riplist.txt or just state --subreddit lithuania hentai_gifs --batch 1000
# ? first get all json files with links, extract downloadable shit and divide work
# todo multiprocessing https://www.youtube.com/watch?v=RR4SoktDQAw