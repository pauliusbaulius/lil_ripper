from src import ripper
from bs4 import BeautifulSoup
import requests


def is_gfycat_link(url):
    if str(url).find("gfycat.com/") >= 0:
        return True
    else:
        return False


def handle_gfycat_url(url, path):
    # If gfycat link is an URI, do not try to extract.
    if str(url).endswith(".mp4"):
        ripper.download_file(url, path)
    else:
        # Otherwise, extract media link from page.
        new_url = extract_gfycat_direct_link(url)
        # todo handle None here, do not send to downloader.
        if new_url is not None:
            ripper.download_file(new_url, path)


@DeprecationWarning
def download_gfycat_video(url, directory):
    download_location = extract_gfycat_direct_link(url)
    ripper.download_file(path=download_location, url=url)


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
    except TypeError:
        print(f"Gfycat video [{url}] has been deleted/your IP is banned.")
    except Exception as error:
        print("Failed to extract gfycat video link...", error)


if __name__ == "__main__":
    print("Will run tests.")
