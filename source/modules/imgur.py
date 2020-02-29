import requests
import re
import os
from modules import tools

"""
Since imgur wants you to create user account to access read-only api which also required to give your email and phone number,
I went with direct json request method. You can extract album id from album link and pass it to hit.json.
This gives you json file with information about album that also contains hashes aka image links and their type.
It is enough to download one json file and extract+reconstruct links to all album images.
"""


def get_album_id(album_url):
    # todo a proper id extraction.
    # remove trailing / if it exists.
    if album_url.endswith("/"):
        album_url = album_url[:-1]

    if album_url.endswith(".gifv"):
        album_url = album_url[:-5]

    return str(album_url).split("/")[-1]


def get_album_json(album_url):
    """
    Given imgur album link, creates json download link, downloads it and returns json file.
    Assumes that imgur album link is legit.
    """
    album_id = get_album_id(album_url)
    json_link = "https://imgur.com/ajaxalbums/getimages/{}/hit.json".format(album_id)
    r = requests.get(json_link)
    json_data = r.json()
    return json_data


def find_album_media_data(json_data):
    """
    Goes over given json file and finds image hash and ext values. Adds them to a dictionary.
    Returns a dictionary of key-value pairs in form hash:ext
    ext is image format.
    """
    try:
        images = {}
        image_data = json_data["data"]["images"]
        for image in image_data:
            images[image["hash"]] = image["ext"]
        return images
    except TypeError:
        raise TypeError("parsing imgur album json failed, skipping...")


def reconstruct_links(image_data_dict):
    """
    Takes a dictionary from find_album_images_json() and constructs direct imgur links to pictures.
    """
    links = []
    imgur_link = "https://imgur.com/"
    for key, value in image_data_dict.items():
        url = imgur_link + key + value
        links.append(url)
    return links


def is_imgur_album(url):
    """
    Checks whether a link is imgur album or not.
    """
    url = str(url)
    if url.find("imgur.com/a/") >= 0:
        return True
    else:
        return False


def find_all_album_media(album_url):
    """
    Given imgur album url will return a list of direct links to all pictures in album.
    Returns None if link is invalid.
    """
    try:
        if is_imgur_album(album_url):
            json_data = get_album_json(album_url)
            image_data = find_album_media_data(json_data)
            image_links = reconstruct_links(image_data)
            return image_links
    except Exception:
        print("finding imgur album images failed, skipping...")
        return None


def download_imgur_album(url, directory=os.getcwd()):
    """
    Downloads all media from imgur album and stores in given directory. Album name will be it's id.
    :param url: imgur album url
    :param directory: directory where files will be saved. default is current dir.
    """
    try:
        album_name = get_album_id(url)
        file_urls = find_all_album_media(url)
        if file_urls is not None:
            album_directory = os.path.join(directory, album_name)
            tools.create_dir(album_directory)  # create new dir with album id as name
            for file_url in file_urls:
                tools.download_file(file_url, album_directory)
        else:
            print("imgur album does not exist anymore, skipping...")
    except TypeError:
        print("imgur album does not exist anymore, skipping...")


def download_imgur_albums():
    # todo read from riplist.csv and rip all albums where first column is imguralbum
    pass


