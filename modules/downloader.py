import os
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


if __name__ == "__main__":
    #handle_url("https://imgur.com/a/xzCD0wC", "/home/joe/github/lil_ripper/testing_grounds", ["jpg, png"])
    download_file("https://imgur.com/HHDZK1t.jpg", "/home/joe/github/lil_ripper/testing_grounds/imgur_xzCD0wC", ["jpg"])