import re
import requests
from modules import new_ripper

"""
Since imgur wants you to create user account to access read-only api which also required to give your email and phone number,
I went with direct json request method. You can extract album id from album link and pass it to hit.json.
This gives you json file with information about album that also contains hashes aka image links and their type.
It is enough to download one json file and extract+reconstruct links to all album images.
"""


def is_imgur_album(url):
    # todo https://imgur.com/gallery/jViWuze is also valid name!
    """
    Checks whether a link is imgur album or not.
    """
    url = str(url)
    if url.find("imgur.com/a/") >= 0:
        return True
    else:
        return False


def is_imgur_single_image(url):
    # todo [https://imgur.com/RLCNQFq] should be handled with regex? if not imgur.com/a/ and doesnt contain . at the -3 -4, append .jpg
    regex_pattern = re.compile("https://imgur.com/[^a/](.+)[^.jpg|.png|.gifv|.mp4]")
    url = str(url)
    try:
        if str(re.match(regex_pattern, url).string):
            return True
    except AttributeError:
        return False


def make_imgur_image(url):
    # Make link into jpg image and hope it is an image.
    return url + ".jpg"


def download_imgur_album(url, formats, path):
    """
    Downloads all media from imgur album and stores images in a new folder named imgur_<album_id> in given base dir.
    :param url: imgur album url
    :param directory: directory where files will be saved.
    """
    try:
        album_name = "imgur_" + get_album_id(url)
        album_image_urls = find_all_album_media(url)
        if album_image_urls is not None:
            # Create new dir with album id as name
            album_directory = new_ripper.create_dir(base_path=path, new_dir=album_name)
            for file_url in album_image_urls:
                if new_ripper.is_downloadable(url=file_url, formats=formats):
                    new_ripper.download_file(url=file_url, path=album_directory)
    except TypeError:
        print("Imgur album has been does not exist anymore, skipping...")


def get_album_id(album_url):
    # Remove trailing / if it exists.
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


def find_album_media(json_data):
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


def find_all_album_media(album_url):
    """
    Given imgur album url will return a list of direct links to all pictures in album.
    Returns None if link is invalid.
    """
    try:
        if is_imgur_album(album_url):
            json_data = get_album_json(album_url)
            image_data = find_album_media(json_data)
            image_links = reconstruct_links(image_data)
            return image_links
    except Exception:
        print("finding imgur album images failed, skipping...")
        return None


def download_imgur_albums(url):
    # todo read from riplist.csv and rip all albums where first column is imguralbum
    if is_imgur_album(url):
        print("Is imgur album, will download pictures...")


if __name__ == "__main__":
    print("Will run tests.")
    #create_album_dir("/home/joe/github/lil_ripper/testing_grounds", "bruhtonium")
    #download_imgur_album("https://imgur.com/a/xzCD0wC", "/home/joe/github/lil_ripper/testing_grounds", ["jpg"])
    #print(is_imgur_single_image("https://imgur.com/RLCNQFq"))
    #print(is_imgur_single_image("https://i.imgur.com/cRgEyJX.jpg"))