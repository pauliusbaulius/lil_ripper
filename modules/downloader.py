import os
from datetime import time
import time
import requests
from modules import imgur, gfycat, indexer

@DeprecationWarning
def rip_subreddit(subreddit_name, continue_download, download_location, database_location, min_upvotes):
    """
    Given a subreddit name, tries to download all media files from links found in the database.
    If subreddit table is not found, indexes it first before downloading.
    Downloadable media file formats, default download location and database location can be changed in settings.json.
    """
    print("called rip_subreddit", subreddit_name, download_location, database_location, min_upvotes, continue_download)
    # python3 lilripper.py -r dankmemes -u 100 --continue-download
    # todo implement check for db, if needed update
    # if not in db, index
    # if in db, start downloading and setting status=1 if success
    # if continue_download=False, ignore status! or set to 0
    indexer.index_subreddit(subreddit_name, min_upvotes, database_location)


def rip_subreddit_no_index(subreddit_name, download_location, min_upvotes, formats):
    download_location = create_directory(download_location, subreddit_name)
    # Check if user already started download and get last json's data if it is the case.
    is_there_json_file(subreddit_name, download_location)
    # if last_json is not None:
    #     json_data = requests.get(last_json).json()
    #     time_from = json_data["data"][0].get("created_utc")

    # Get first and last urls from file, to generate json urls for new posts and older yet not downloaded posts.
    filename = os.path.join(download_location, f"{subreddit_name}.txt")
    times = get_first_last_json_link(filename)
    # Bad way to check whether there are json links stored in file.
    if len(times[0]) > 1:
        # Get first link first post utc and generate links from time.now to that post
        new_posts_time_to = requests.get(times[0]).json()["data"][0].get("created_utc")
        links = generate_json_urls(subreddit_name, int(time.time()), new_posts_time_to, min_upvotes)
        # Get last link last post first post utc and generate from that to 1 and append to links!
        last_post_time_from = requests.get(times[1]).json()["data"][0].get("created_utc")
        links = links + generate_json_urls(subreddit_name, last_post_time_from, 1, min_upvotes)
    else:
        links = generate_json_urls(subreddit_name, int(time.time()), 1, min_upvotes)
    # Download from json!
    for json_link in links:
        filename = os.path.join(download_location, f"{subreddit_name}.txt")
        # Write current json url to file, so if the program was stopped or crashed, we could resume.
        with open(filename, "a") as f:
            f.write(json_link + "\n")
        download_from_json(json_link, download_location, formats)

    # todo have to sort the links inside of text file somehow! so there would not be fuckery

    # # Generate all json links.
    # # todo also generate json for fresh ones! so from now to last json!
    # # time_from now
    # # time_to = last line first post
    # # generate links
    # # set time from to json_links last item last entry
    # # generate links and append
    # # start download!
    # json_links = generate_json_urls(subreddit_name, time_from, 1, min_upvotes)
    # # Download from links!
    # for json_link in json_links:
    #     filename = os.path.join(download_location, f"{subreddit_name}.txt")
    #     # Write current json url to file, so if the program was stopped or crashed, we could resume.
    #     with open(filename, "a") as f:
    #         f.write(json_link + "\n")
    #     download_from_json(json_link, download_location, formats)


def generate_json_urls(subreddit, time_from, time_to, min_upvotes):
    # todo take time_to, so we could generate links for new posts too!
    json_links = []
    try:
        while True and time_from > time_to:
            json_link = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}" \
                        f"&sort=desc&sort_type=created_utc&before={time_from}&score=>{min_upvotes - 1}&size=1000&is_self=false"
            json_links.append(json_link)
            json_data = requests.get(json_link).json()
            time_from = json_data["data"][-1].get("created_utc")
            # Sleep for 1 second to only make one api call per second.
            time.sleep(1)
    except IndexError:
        # When all json files are generated, break loop and finish.
        print(f"{len(json_links)} json links were generated. Will start downloading...")
    finally:
        return json_links


def is_there_json_file(filename, directory):
    # todo maybe make new function that returns first and last json links, so we could generate links for new and older posts?
    """
    Checks for file named <subreddit>.txt
    If there is no such file, it is created and function returns None
    If there is such a file, it returns last line, which should be json url.
    Assumes that user will not have such text file with other data.
    Assumes that user will not modify the text file on their own.
    """
    filename = f"{filename}.txt"
    for file in os.listdir(directory):
        # If there is a file already, return last json
        if file.endswith(filename):
            filename = os.path.join(directory, filename)
            with open(filename, "r") as f:
                last_line = ""
                # todo iterates over whole file, not the best solution..
                for line in f:
                    last_line = line
                # Return url if it is a valid one.
                if last_line.startswith("https://api.pushshift.io/reddit/search/submission/"):
                    return last_line
                else:
                    return None
    # Otherwise, create a new file.
    else:
        filename = os.path.join(directory, filename)
        open(filename, "w").close()
        return None


def get_first_last_json_link(filepath):
    """
    Given a complete filepath, reads first and last lines of the file.
    Returns a list containing first and last line contents.
    Assumes that the file has lines.
    Assumes that the file has json links, aka nobody tampered with it.
    """
    last_line = ""
    with open(filepath, "r") as f:
        first_line = f.readline()
        for line in f:
            last_line = line
    return [first_line, last_line]


@DeprecationWarning
def rip_all(continue_download, download_location):
    """
    Tries to download all media files from links found in database tables.
    """
    print("called rip_all", download_location, continue_download)
    # todo just iterate over each table and


def handle_url(url, directory, formats):
    """
    Checks url and sends it to the method that handles downloading.
    """
    # If it is a directly downloadable link ending in valid format.
    if is_downloadable(url, formats):
        # Make .gifv files into .mp4 files, to be playable on computers that do not support .gifv.
        if str(url).endswith(".gifv"):
            url = url.replace(".gifv", ".mp4")
            download_file(url, directory)
        else:
            download_file(url, directory)
    # If it is a reddit webm
    elif is_reddit_webm(url):
        # todo remove print() when function is implemented and working!
        print(f"It is a reddit webm! [{url}]")
        #download_reddit_webm(url)
    # If it is an imgur album...
    elif imgur.is_imgur_album(url):
        print(f"Downloading imgur album [{url}]")
        imgur.download_imgur_album(url, directory, formats)
    # If it is gfycat link...
    elif gfycat.is_gfycat_link(url):
        print(f"Downloading gfycat video [{url}]")
        gfycat.download_gfycat_video(url, directory, formats)
    else:
        print(f"Cannot download this url (yet): [{url}]")


def download_file(url, directory):
    try:
        # Had to do it to em because of gfycat ip bans.
        if gfycat.is_gfycat_link(url):
            time.sleep(10)
        req = requests.get(url)
        # todo check whether this impacts some subreddits that could host images smaller than 10KB.
        # Do not download files under 10KB to not download imgur deleted images and other most likely non-trivial stuff.
        if len(req.content) > 10240:
            filename = str(url).split("/")[-1]
            # Check if already exists, if not, download file.
            # todo check for dupes before getting anything to speed shit up!
            if not check_for_dupes(directory, filename):
                with open(os.path.join(directory, filename), "wb") as f:
                    f.write(req.content)
                    size = sizeof_fmt(os.fstat(f.fileno()).st_size)
                    print(f"Downloaded [{url}] {size}")
        else:
            print(f"File is under 10KB in size, will not download.")
    except Exception as error:
        # todo fix this band-aid exception, it works but well, it doesn't really tell why the problem happened.
        print(f"Downloading [{url}] has failed, skipping...")
        print(error)


def is_downloadable(url, formats):
    """Given one url and a list of formats, check whether the link leads to file we want to download."""
    # If it is a .gifv and .mp4 is to be downloaded, use that extra ugly check.
    return str(url).endswith(tuple(formats)) or str(url).endswith("gifv") and "mp4" in tuple(formats)


def is_reddit_webm(url):
    """Hacky test to see whether the url leads to reddit video which should be a webm or not."""
    return "v.redd.it" in url


def download_reddit_webm(url):
    # todo handle webm files! aka v.reddit downloads!
    # append .json to the end
    # extract json fallback_url
    # download that
    # replace fallback_url DASH with audio
    # download sound
    # combine
    # save
    # profit
    print(url)
    json_url = url + ".json"
    r = requests.get(json_url)
    json_data = r.json()
    print(json_data)
    # Get webm url
    fallback_url = json_data["0"]
    # todo strip everything up to first /
    # todo append audio to new url
    # todo download both urls
    # todo combine both https://stackoverflow.com/questions/28219049/combining-an-audio-file-with-video-file-in-python
    # todo change to only works on linux due to ffmpeg!
    print(fallback_url)


def check_for_dupes(directory, filename):
    """
    Checks whether a file with given filename already exists to not have to download it.
    """
    full_path = os.path.join(directory, filename)
    if os.path.exists(full_path):
        print(f"File [{filename}] already exists, skipping download...")
        return True


def create_directory(base_dir, new_dir):
    """
    If directory does not exist, make one. Otherwise return already existing directory.
    :param base_dir: base directory where to create new directory.
    :param new_dir: name of the new directory.
    :return: path to new/existing directory.
    """
    album_directory = os.path.join(base_dir, new_dir)
    if not os.path.exists(album_directory):
        os.mkdir(album_directory)
        print(f"New directory [{album_directory}] was created.")
        return album_directory
    else:
        print(f"Directory [{album_directory}] already exists.")
        return album_directory


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


def download_from_json(json_url, directory, formats):
    """
    Given a json url, directory for downloads and format wishlist, goes over all posts in json file,
    extracts links and and sends them to url handler one by one.
    """
    try:
        r = requests.get(json_url)
        json_data = r.json()
        link_data = json_data["data"]
        for x in link_data:
            handle_url(x["url"], directory, formats)
    except Exception as error:
        print(f"Analyzing [{json_url}] has failed.")
        # Gives user complete error traceback, because they love it.
        print(error.with_traceback())


if __name__ == "__main__":
    #handle_url("https://imgur.com/a/xzCD0wC", "/home/joe/github/lil_ripper/testing_grounds", ["jpg, png"])
    #download_file("https://imgur.com/HHDZK1t.jpg", "/home/joe/github/lil_ripper/testing_grounds/imgur_xzCD0wC", ["jpg"])
    #rip_subreddit_no_index("dankmemes", "C:\\Users\\workstation\\Desktop\\lil ripper github\\lil_ripper\\downloads\\testing", 1000, ["jpg", "png", "gif", "webm"])
    download_reddit_webm("https://www.reddit.com/r/Idiotswithguns/comments/fdxn2q/soarcarl_gets_banned_on_twitch/")

    #print(is_there_json_file("lithuaniax", "X:\\downloads\\"))