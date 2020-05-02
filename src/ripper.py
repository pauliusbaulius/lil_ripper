import concurrent.futures
import os
import random
from datetime import time, timedelta
import time
import requests
from src.modules import gfycat, imgur, reddit
from fake_useragent import UserAgent

# If no path is specified in CLI, uses current directory as base path.
BASE_DOWNLOAD_PATH = os.getcwd()
# If no formats are specified, uses basic predefined formats.
DOWNLOAD_FORMATS = ["jpg", "jpeg", "png", "gif", "mp4", "webm"]


def ripper(subreddit_name, formats, download_location, min_upvotes):
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
    start_time = time.time()
    # Set global variable to not have to pass download_path to other functions!
    global BASE_DOWNLOAD_PATH
    global DOWNLOAD_FORMATS
    # Create dir for downloads
    save_location = create_dir(download_location, subreddit_name)
    BASE_DOWNLOAD_PATH = save_location
    # Set download formats
    DOWNLOAD_FORMATS = formats
    # Generate json urls for subreddit.
    print("Generating download links, might take a while...")
    json_urls = generate_pushift_urls(subreddit_name, int(time.time()), 1, min_upvotes, batch_size=1000)
    # Download files from each json
    for url in json_urls:
        download_from_json(url)
    elapsed_time = time.time() - start_time
    print(f"Downloading finished, took {timedelta(seconds=round(elapsed_time))}.")


def create_dir(base_path, new_dir):
    """
    If directory does not exist, make one. Otherwise return already existing directory.
    :param base_dir: base directory where to create new directory.
    :param new_dir: name of the new directory.
    :return: path to new/existing directory.
    """
    #todo https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
    # todo Create dirs for given path if they do not exist yet.
    full_path = os.path.join(base_path, new_dir)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
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


def generate_pushift_urls(subreddit, utc_from, utc_to, min_upvotes, batch_size=1000):
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
    json_links = []
    try:
        while True and utc_from > utc_to:
            json_link = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}" \
                        f"&sort=desc&sort_type=created_utc&before={utc_from}&score=>{min_upvotes - 1}&size={batch_size}&is_self=false"
            json_links.append(json_link)
            json_data = requests.get(json_link).json()
            utc_from = json_data["data"][-1].get("created_utc")
            # Sleep for 1 second to only make one api call per second.
            time.sleep(1)
    except IndexError:
        # When all json files are generated, break loop and finish.
        print(f"{len(json_links)} json links were generated. Will start downloading...")
    finally:
        return json_links


def download_from_json(json_url):
    """
    Given one json url, extracts media urls.
    Passes them to media url handler.
    :param json_url: Pushift json url.
    """
    try:
        urls = generate_urls_from_json(json_url)
        # todo check for dupes in dir, eliminate dupes from urls to download, should speed it up!
        urls = check_dupes(urls)
        # Start parallel downloader here.
        with concurrent.futures.ProcessPoolExecutor() as parallel:
            [parallel.submit(handle_media_url, url) for url in urls]
    except Exception as error:
        print(f"Analyzing [{json_url}] has failed.")
        # Gives user complete error traceback, because they love it.
        print(error.with_traceback())
        return False


def generate_urls_from_json(json_url):
    """Given a pushshift json url, extracts urls from reddit posts."""
    urls = []
    request = requests.get(json_url)
    json_data = request.json()
    link_data = json_data["data"]
    for x in link_data:
        urls.append(x["url"])
    return urls


def check_dupes(urls):
    """
    Given a list of urls, checks for duplicates and then checks
    for already downloaded files using url ending as filename.
    """
    amount_start = len(urls)
    print(f"{len(urls)} have been given.")
    # First, remove duplicate links from list.
    urls = list(dict.fromkeys(urls))
    # Second, remove links of already downloaded files.
    # todo check file stems only. do not look at file ending!
    # todo multiprocessing here too?
    # for url in urls:
    #     status = check_if_downloaded(BASE_DOWNLOAD_PATH, filename=str(url).split("/")[-1])
    #     if status:
    #         urls.remove(url)
    print(f"Removed {amount_start - len(urls)} duplicates and already downloaded links, {len(urls)} are left to download.")
    return urls


# todo alternative version without dupe checking, assumes that dupes are checked before, worst case - stuff will be overwritten
def download_file_new(url, path):
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
        # Do not be greedy.
        time.sleep(random.randint(1, 5))
        # Wait for 5-15 seconds between gfycat requests to not get ip ban.
        if gfycat.is_gfycat_link(url):
            print("will sleep now")
            time.sleep(random.randint(30, 60))
        # todo select random header from list of headers
        request = requests.get(url, headers={
            'User-Agent': str(UserAgent().random)})
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
    except Exception as error:
        # todo fix this band-aid exception, it works but it doesn't really tell why the problem happened.
        print(f"Downloading [{url}] has failed, skipping...")
        print(error)
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
            download_file(url, BASE_DOWNLOAD_PATH)
        else:
            download_file(url, BASE_DOWNLOAD_PATH)
    # If it is a reddit webm
    elif reddit.is_reddit_webm(url):
        reddit.download_reddit_webm(url=url, download_path=BASE_DOWNLOAD_PATH)
    # If it is an imgur album...
    elif imgur.is_imgur_album(url):
        print(f"Downloading imgur album [{url}]")
        # Need to pass dir to make imgur folder in subreddit folder.
        imgur.download_imgur_album(url=url, formats=DOWNLOAD_FORMATS, path=BASE_DOWNLOAD_PATH)
    # If it is gfycat link...
    elif gfycat.is_gfycat_link(url):
        print(f"Downloading gfycat video [{url}]")
        gfycat.handle_gfycat_url(url, BASE_DOWNLOAD_PATH)
    # Tries to convert those imgur links with no file ending to .jpg and hope for the best.
    elif imgur.is_imgur_single_image(url):
        url = imgur.make_imgur_image(url)
        download_file(url)
    else:
        print(f"Cannot download this url (yet): [{url}]")


def is_downloadable(url, formats):
    """Given one url and a list of formats, check whether the link leads to file we want to download."""
    # If it is a .gifv and .mp4 is to be downloaded, use that extra ugly check.
    return str(url).endswith(tuple(formats)) or str(url).endswith("gifv") and "mp4" in tuple(formats)


def download_file(url, path):
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
            time.sleep(random.randint(1, 5))
            # Wait for 5-15 seconds between gfycat requests to not get ip ban.
            if gfycat.is_gfycat_link(url):
                time.sleep(random.randint(15, 30))
            # todo select random header from list of headers
            request = requests.get(url, headers={
            'User-Agent': str(UserAgent().random)})
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
    #ripper(subreddit_name="dankmemes", min_upvotes=50000)
    ua = UserAgent()
    print(str(ua.random))

