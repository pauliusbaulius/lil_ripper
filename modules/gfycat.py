from modules import new_ripper
from bs4 import BeautifulSoup
import requests


# todo convert to new_ripper links!


def is_gfycat_link(url):
    if str(url).find("gfycat.com/") >= 0:
        return True
    else:
        return False


def download_gfycat_video(url, directory):
    download_location = extract_gfycat_direct_link(url)
    new_ripper.download_file(path=download_location, url=url)


def extract_gfycat_direct_link(url):
    # todo pytest and make it return booleans
    """
    Gets gfycat site html and extracts video download link. If something goes wrong, it prints a statement and skips this url.
    """
    try:
        r = requests.get(url,  headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        soup = BeautifulSoup(r.text, "html.parser")
        # bs4 to get that video link.
        return soup.find("meta", property="og:video")["content"]
    except Exception as error:
        print("Failed to extract gfycat video link...")
        print(error)



