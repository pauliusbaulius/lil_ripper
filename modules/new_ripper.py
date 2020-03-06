import concurrent.futures
import os
from datetime import time
import time
import requests
from modules import imgur, gfycat, reddit

# If no path is specified in CLI, uses current directory as base path.
BASE_DOWNLOAD_PATH = "/home/joe/github/lil_ripper/testing_grounds/parallel_test/"
# If no formats are specified, uses basic predefined formats.
DOWNLOAD_FORMATS = ["jpg", "jpeg", "png", "gif", "mp4", "webm"]


def ripper(subreddit_name, download_location, min_upvotes, formats):
    """
    -1. Create download directory. (create_dir:download_path, subreddit_name)
    -2. Create <subreddit_name>.csv in download directory. (create_csv:directory, name)
        -2.1 csv structure: downloaded,utc_from,utc_to,url
    -3. Generate pushift urls: (generate_pushift_links:subreddit_name, time_from, time_to, min_upvotes, batch_size)
        -3.1 New posts = from current_utc to first utc_from in .csv (get_csv_new)
            -3.1.1 Sort .csv by time_from (sort_csv:path)
        -3.2 Old posts = from last utc_to in .csv to utc 1
            -3.2.1 Sort .csv by time_from
    -4. Download using pushift url's frm .csv (download_from_json:json_url)
        -4.1 If url has downloaded=true, skip it
        -4.2 After downloading, set matching url downloaded status to true (update_csv:path, url)
        -4.3 Downloader function checks for dupes first thing, to speed things up!
        +4.4 Url handler works with reddit webm's

    :param subreddit_name:
    :param download_location:
    :param min_upvotes:
    :param formats:
    :return:
    """
    # Set global variable to not have to pass download_path to other functions!
    global BASE_DOWNLOAD_PATH
    BASE_DOWNLOAD_PATH = download_location
    download_from_json()


def create_dir(new_dir):
    """
    If directory does not exist, make one. Otherwise return already existing directory.
    :param base_dir: base directory where to create new directory.
    :param new_dir: name of the new directory.
    :return: path to new/existing directory.
    """
    full_path = os.path.join(BASE_DOWNLOAD_PATH, new_dir)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
        print(f"New directory [{full_path}] was created.")
        return full_path
    else:
        print(f"Directory [{full_path}] already exists.")
        return full_path


def create_csv(filename):
    """Given a base path and a new filename, creates a .csv file."""
    global BASE_DOWNLOAD_PATH


def sort_csv(filename):
    """Given path and .csv filename, sorts the file by utc_from field."""
    global BASE_DOWNLOAD_PATH


def get_csv_newest_utc(filename):
    """
    Given path and .csv filename, returns highest utc_from value.
    Assumes that the file is sorted by utc_from.
    # todo Maybe sort the file before looking to make sure? And reduce possible malfunctions.
    """
    global BASE_DOWNLOAD_PATH


def get_csv_oldest_utc(filename):
    """
    Given path and .csv filename, returns lowest utc_to value.
    Assumes that the file is sorted by utc_from.
    # todo Maybe sort the file before looking to make sure? And reduce possible malfunctions.
    """
    global BASE_DOWNLOAD_PATH
    pass


def generate_pushift_urls(subreddit, utc_from, utc_to, min_upvotes, batch_size):
    """
    Given a subreddit, utc times, minimum upvote count and batch size,
    generates appropriate pushift json urls and stores them in a list.
    Returns a list of urls.
    :param subreddit:
    :param utc_from:
    :param utc_to:
    :param min_upvotes:
    :param batch_size:
    :return:
    """
    pass


def download_from_json(json_url):
    """
    Given one json url, extracts media urls.
    Passes them to media url handler.
    :param json_url: Pushift json url.
    """
    urls = []
    try:
        request = requests.get(json_url)
        json_data = request.json()
        link_data = json_data["data"]
        for x in link_data:
            urls.append(x["url"])
        # Start parallel downloader here.
        with concurrent.futures.ProcessPoolExecutor() as parallel:
            [parallel.submit(handle_media_url, url) for url in urls]
    except Exception as error:
        print(f"Analyzing [{json_url}] has failed.")
        # Gives user complete error traceback, because they love it.
        print(error.with_traceback())
        return False


def handle_media_url(url):
    """
    Given one url, it checks if url is downloadable and passes downloadable urls to downloader.
    Uses global variable to check formats.
    :param url: Direct url of a file to download, aka URI.
    """
    # If it is a directly downloadable link ending in valid format.
    if is_downloadable(url, DOWNLOAD_FORMATS):
        # Make .gifv files into .mp4 files, to be playable on computers that do not support .gifv.
        if str(url).endswith(".gifv"):
            url = url.replace(".gifv", ".mp4")
            download_file(url=url, path=BASE_DOWNLOAD_PATH)
        else:
            download_file(url=url, path=BASE_DOWNLOAD_PATH)
    # If it is a reddit webm
    elif reddit.is_reddit_webm(url):
        # todo remove print() when function is implemented and working!
        print(f"It is a reddit webm! [{url}]")
        reddit.download_reddit_webm(url, BASE_DOWNLOAD_PATH)
    # If it is an imgur album...
    elif imgur.is_imgur_album(url):
        print(f"Downloading imgur album [{url}]")
        imgur.download_imgur_album(url, BASE_DOWNLOAD_PATH, DOWNLOAD_FORMATS)
    # If it is gfycat link...
    elif gfycat.is_gfycat_link(url):
        print(f"Downloading gfycat video [{url}]")
        gfycat.download_gfycat_video(url, BASE_DOWNLOAD_PATH, DOWNLOAD_FORMATS)
    else:
        print(f"Cannot download this url (yet): [{url}]")


def is_downloadable(url, formats):
    """Given one url and a list of formats, check whether the link leads to file we want to download."""
    # If it is a .gifv and .mp4 is to be downloaded, use that extra ugly check.
    return str(url).endswith(tuple(formats)) or str(url).endswith("gifv") and "mp4" in tuple(formats)


def download_file(path, url):
    """
    Given a download path and file url, tries to download it.
    - Checks if file already exists before trying to download, skips if item exists.
    - Names files by their url endings.
    - Does not download files under 10KB to prevent downloading of deleted imgur image placeholders
    and other unwanted data!
    Returns status as boolean, True if file was downloaded, False if it wasn't.
    :param path: Download location.
    :param url: Link to resource to download.
    :return: True if file has been downloaded, False if file failed to download.
    """
    try:
        # Filename is url ending.
        filename = str(url).split("/")[-1]
        # Check if already exists, if not, download file.
        if not check_if_downloaded(path, filename):
            # Do not be greedy.
            time.sleep(5)
            # Wait for 10 seconds between gfycat requests to not get ip ban.
            # todo play around with the value, maybe 5 seconds are enough...
            if gfycat.is_gfycat_link(url):
                time.sleep(10)
            request = requests.get(url)
            # Save file content to variable.
            file_content = request.content
            # todo check whether this impacts some subreddits that could host images smaller than 10KB.
            # Do not download files under 10KB to not download imgur deleted images and other most likely non-trivial stuff.
            if len(file_content) > 10240:
                # Save file to disk.
                with open(os.path.join(path, filename), "wb") as f:
                    f.write(file_content)
                    # Calculate size in human-readable format for displaying purposes.
                    size = sizeof_fmt(os.fstat(f.fileno()).st_size)
                    print(f"Downloaded [{url}] [{size}]")
                    return True
            else:
                print(f"File [{url}] is under 10KB in size, skipping download...")
                return False
        else:
            print(f"File [{filename}] already exists, skipping download...")
            return False
    except Exception as error:
        # todo fix this band-aid exception, it works but it doesn't really tell why the problem happened.
        print(f"Downloading [{url}] has failed, skipping...")
        print(error)
        return False


def check_if_downloaded(path, filename):
    """
    Given a download path and filename, checks whether a file already exists or not.
    Returns True if file exists.
    :param path:
    :param filename:
    :return:
    """
    full_path = os.path.join(path, filename)
    if os.path.exists(full_path):
        return True


def sizeof_fmt(num, suffix='B'):
    """
    Calculates file size in human-readable format. Copy-pasted from StackOverflow, thanks to this dude:
    https://stackoverflow.com/questions/1094841/reusable-library-to-get-human-readable-version-of-file-size
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


if __name__ == "__main__":
    print("Will run tests.")
    # todo run tests
    json_link = f"https://api.pushshift.io/reddit/search/submission/?subreddit=lithuania" \
                f"&sort=desc&sort_type=created_utc&before={int(time.time())}&score=>10&size=1000&is_self=false"
    download_from_json(json_link)
