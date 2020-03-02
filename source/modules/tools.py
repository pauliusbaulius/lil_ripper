import os
import requests
import json
from source.modules import imgur
from source.modules import gfycat
from datetime import datetime
import time

total_session_downloads = 0


def load_settings():
    # todo use relative positioning!
    with open(r"/home/joe/github/lil_ripper/settings.json") as json_file:
        settings = json.load(json_file)
    return settings


downloadable_formats = load_settings()["formats_to_rip"]


def create_dir(folder_name, save_path=os.getcwd()):
    """
    Creates directory in save path. If no save path is given, current working dir is used.
    Directory name is a given parameter.
    """
    directory = os.path.join(save_path, folder_name)
    if not os.path.exists(directory):
        os.mkdir(directory)
        print(f"New directory [{directory}] was created.")
    return directory


def check_for_dupes(directory, filename):
    """
    Checks whether a file with given filename already exists to not have to download it.
    """
    full_path = os.path.join(directory, filename)
    if os.path.exists(full_path):
        print("File [{}] already exists, skipping download...".format(filename))
        return True


def download_file(url, directory):
    """
    Will download file given direct link to it. If it cannot download the file,
    it will print a message but won't halt the program. Checks if file is already donwloaded based on name, if it is
    it will be skipped.
    :param url: direct link to file
    :param directory: save path for downloaded file
    """
    global total_session_downloads
    try:
        if str(url).endswith(tuple(downloadable_formats)):  # check if it ends with valid format for direct download
            # todo check headers to not download files under 2KB https://stackoverflow.com/questions/14270698/get-file-size-using-python-requests-while-only-getting-the-header
            req = requests.get(url)
            # todo use this for filename now, later use hash
            filename = str(url).split("/")[-1]
            # Convert .gifv to .mp4
            if str(url).endswith(".gifv") and ".mp4" in tuple(downloadable_formats):
                filename = filename.replace(".gifv", ".mp4")

            # Check if already exists, if not, download file.
            if not check_for_dupes(directory, filename):
                with open(os.path.join(directory, filename), "wb") as f:
                    f.write(req.content)
                    size = sizeof_fmt(os.fstat(f.fileno()).st_size)
                    f.close()
                    print(f"Downloaded [{url}] with size of {size}.")
                    total_session_downloads += 1
            else:
                print(f"File [{url}] was not downloaded...")

    except Exception:
        # todo fix this band-aid exception, it works but well, it doesn't really tell why the problem happened.
        print(f"Downloading [{url}] has failed, skipping...")


""" Stuff I finessed on Stackoverflow and etc."""


def sizeof_fmt(num, suffix='B'):
    """
    https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    Thanks to this dude.
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def parse_link(url, directory):
    """
    Checks url and sends it to the method that handles downloading.
    """
    sleep_time_in_seconds = load_settings()["sleep_time_in_seconds"]
    time.sleep(sleep_time_in_seconds)
    # If it is a directly downloadable link ending in valid format.
    # If it is a .gifv and .mp4 is to be downloaded, use that extra ugly check.
    if str(url).endswith(tuple(downloadable_formats)) or str(url).endswith(".gifv") and ".mp4" in tuple(downloadable_formats):
        download_file(url, directory)
    # If it is an imgur album...
    elif imgur.is_imgur_album(url):
        print(f"Downloading imgur album [{url}]")
        imgur.download_imgur_album(url, directory)
    # If it is gfycat link...
    elif gfycat.is_gfycat_link(url):
        print(f"Downloading gfycat video [{url}]")
        gfycat.download_gfycat_video(url, directory)
    else:
        print(f"Cannot download this url yet [{url}]")


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
        print("Analyzing .json has failed...")


def archive_subreddit(subreddit, min_upvotes=0):
    """
    Basically eina nuo dabartinio timestamp iki subreddit creation date in one week interval.
    """
    global total_session_downloads
    day_in_seconds = 24 * 60 * 60
    save_path = create_dir(load_settings()["download_directory"])
    reddit_batch_size = load_settings()["reddit_batch_size"]
    time_interval = load_settings()["time_interval_in_days"] * day_in_seconds
    directory = create_dir(os.path.join(save_path, subreddit))  # creates dir using subreddit name

    # todo find out how to get subreddit creation date without reddit account!
    #creation_date = int(reddit.subreddit(subreddit).created_utc)
    creation_date = 1
    current_time = int(time.time())
    iterator = 0

    while creation_date <= current_time:
        previous_date = current_time - time_interval
        print("from {} to {} is batch {}. Batch size is {} posts.".format(datetime.utcfromtimestamp(current_time), datetime.utcfromtimestamp(previous_date), iterator, reddit_batch_size))
        json_link = "https://api.pushshift.io/reddit/search/submission/?subreddit={}&sort=desc&sort_type=created_utc&after={}&before={}&size={}".format(subreddit, previous_date, current_time, reddit_batch_size)
        json_try(json_link, directory)
        current_time -= time_interval
        iterator += 1

    print(f"Downloaded [{total_session_downloads}] files in this session.")


if __name__ == "__main__":
    print("Running directly as tools.py!")
    archive_subreddit("gonewild")

