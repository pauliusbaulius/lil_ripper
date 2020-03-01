import os
import requests
import json
from source.modules import imgur
from source.modules import gfycat
import time

total_session_downloads = 0


def load_settings():
    with open(r"/home/joe/github/lil_ripper/settings.json") as json_file: #todo see if it works on leenox
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
        print("new directory [{}] was created.".format(directory))
    return directory


def check_for_dupes(directory, filename):
    """
    Checkes wheter a file with given filename already exists to not have to download it.
    """
    full_path = os.path.join(directory, filename)
    if os.path.exists(full_path):
        print("file [{}] already exists, skipping download...".format(filename))
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
            req = requests.get(url) # todo check headers to not download files under 2KB https://stackoverflow.com/questions/14270698/get-file-size-using-python-requests-while-only-getting-the-header
            filename = str(url).split("/")[-1]  # use this for filename now, later use hash

            # Convert .gifv to .mp4
            if str(url).endswith(".gifv") and ".mp4" in tuple(downloadable_formats):
                filename = filename.replace(".gifv", ".mp4")

            # Check if already exists, if not, download file.
            if not check_for_dupes(directory, filename):
                with open(os.path.join(directory, filename), "wb") as f:
                    f.write(req.content)
                    size = sizeof_fmt(os.fstat(f.fileno()).st_size)
                    f.close()
                    print("downloaded [{}] with size of {}".format(url, size))
                    total_session_downloads += 1
            else:
                print("file [{}] was not downloaded...".format(url))

    except Exception:
        # todo fix this band-aid exception, it works but well, it doesn't really tell why the problem happened.
        print("downloading [{}] has failed, skipping...".format(url))


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
    Checks url and sends it to a method that handles downloading.
    """
    sleep_time_in_seconds = load_settings()["sleep_time_in_seconds"]
    time.sleep(sleep_time_in_seconds)
    # If it is a directly downloadable link ending in valid format.
    # If it is a .gifv and .mp4 is to be downloaded, use that extra ugly check.
    if str(url).endswith(tuple(downloadable_formats)) or str(url).endswith(".gifv") and ".mp4" in tuple(downloadable_formats):
        download_file(url, directory)
    # If it is an imgur album...
    elif imgur.is_imgur_album(url):
        print("downloading imgur album [{}]".format(url))
        imgur.download_imgur_album(url, directory)
    # If it is gfycat link...
    elif gfycat.is_gfycat_link(url):
        print("downloading gfycat video [{}]".format(url))
        gfycat.download_gfycat_video(url, directory)
    else:
        print("cannot download this url yet [{}]".format(url))



