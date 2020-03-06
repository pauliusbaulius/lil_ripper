from modules import downloader
from bs4 import BeautifulSoup
import requests

# todo convert to new_ripper links!


def is_gfycat_link(url):
    if str(url).find("gfycat.com/") >= 0:
        return True
    else:
        return False


def download_gfycat_video(url, directory, formats):
    download_location = extract_gfycat_direct_link(url)
    downloader.download_file(download_location, directory, formats)


def extract_gfycat_direct_link(url):
    # todo pytest and make it return booleans
    """
    Gets gfycat site html and extracts video download link. If something goes wrong, it prints a statement and skips this url.
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        # bs4 to get that video link.
        return soup.find("meta", property="og:video")["content"]
    except Exception as error:
        print("Failed to extract gfycat video link...")
        print(error)



