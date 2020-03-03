import os
from datetime import time
import time
import requests
from modules import imgur, gfycat, indexer


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


# todo lilripper.py -r dankmemes -u 1000 --no-index -f jpg png gif
def rip_subreddit_no_index(subreddit_name, download_location, min_upvotes, formats):
    time_from = int(time.time())
    try:
        # It just works - Todd Howard
        while True and time_from > 1:
            json_link = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit_name}" \
                        f"&sort=desc&sort_type=created_utc&before={time_from}&score=>{min_upvotes-1}&size=1000&is_self=false"
            print(json_link)
            json_data = requests.get(json_link).json()
            json_try(json_link, download_location, formats)
            time_from = json_data["data"][-1].get("created_utc")
    except IndexError:
        # When all json files are generated, break loop and finish.
        print(f"All json url/s were generated, finished...")


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
        download_file(url, directory, formats)
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


def download_file(url, directory, formats):
    try:
        # Check if it ends with valid format.
        if is_downloadable(url, formats):
            req = requests.get(url)
            filename = str(url).split("/")[-1]
            # Convert .gifv to .mp4
            if str(url).endswith(".gifv") and "mp4" in tuple(formats):
                filename = filename.replace(".gifv", ".mp4")
            # Check if already exists, if not, download file.
            if not check_for_dupes(directory, filename):
                with open(os.path.join(directory, filename), "wb") as f:
                    f.write(req.content)
                    print(f"Downloaded [{url}].")
    except Exception:
        # todo fix this band-aid exception, it works but well, it doesn't really tell why the problem happened.
        print(f"Downloading [{url}] has failed, skipping...")


def is_downloadable(url, formats):
    # If it is a .gifv and .mp4 is to be downloaded, use that extra ugly check.
    return str(url).endswith(tuple(formats)) or str(url).endswith("gifv") and "mp4" in tuple(formats)


def check_for_dupes(directory, filename):
    """
    Checks whether a file with given filename already exists to not have to download it.
    """
    full_path = os.path.join(directory, filename)
    if os.path.exists(full_path):
        print("File [{}] already exists, skipping download...".format(filename))
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


def json_try(json_url, directory, formats):
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
            handle_url(x["url"], directory, formats)
    except Exception:
        print("Analyzing .json has failed...")


if __name__ == "__main__":
    #handle_url("https://imgur.com/a/xzCD0wC", "/home/joe/github/lil_ripper/testing_grounds", ["jpg, png"])
    #download_file("https://imgur.com/HHDZK1t.jpg", "/home/joe/github/lil_ripper/testing_grounds/imgur_xzCD0wC", ["jpg"])
    rip_subreddit_no_index("dankmemes", "C:\\Users\\workstation\\Desktop\\lil ripper github\\lil_ripper\\old_data\\test", 100, ["jpg", "png", "gif"])