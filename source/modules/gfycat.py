from modules import tools
from bs4 import BeautifulSoup
import requests


def is_gfycat_link(url):
    if str(url).find("gfycat.com/") >= 0:
        return True
    else:
        return False


def download_gfycat_video(url, directory):
    download_location = extract_gfycat_direct_link(url)
    tools.download_file(download_location, directory)


def extract_gfycat_direct_link(url):
    """
    Gets gfycat site html and extracts video download link. If something goes wrong, it prints a statement and skips this url.
    """
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")
        return soup.find("meta", property="og:video")["content"]  # bs4 to get that video link.
    except Exception:
        print("failed to download gfycat file...")



