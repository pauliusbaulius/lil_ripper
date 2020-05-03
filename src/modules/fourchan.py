import requests
from bs4 import BeautifulSoup
import re
import src.ripper as ripper


def is_4chan_thread(url: str) -> bool:
    """
    Checks whether given url leads to 4chan thread or not.
    :param url: any string, preferably url to 4chan thread.
    :return: True if it is a valid thread link, False otherwise.
    """
    regex = re.compile("https://boards..*/thread/")
    return True if regex.match(url) else False


def extract_thread_media_urls(thread_url: str) -> list:
    """
    Scraps all media file links from a thread.
    All media links start with //i.4cdn.org.
    :param thread_url: url of a 4chan thread.
    :return: list of complete links to media files.
    """
    raw_html = requests.get(thread_url).content
    bs4 = BeautifulSoup(raw_html, features="html.parser")
    urls = [construct_download_url(link.get("href"))
            for link
            in bs4.findAll("a", attrs={'href': re.compile("^//i.4cdn.org")})]
    return list(set(urls))


def construct_download_url(partial_url: str) -> str:
    """
    Adds https: to the front of the string. That's it.
    :param partial_url: url like //i.4cdn.org..
    that needs https part to make it full url.
    :return: complete url to the resource.
    """
    return f"https:{partial_url}"


def extract_thread_name(thread_url: str) -> str:
    return thread_url.split("/")[-1]


def download_thread(url: str, download_path: str):
    # Check if it is a thread first, if not - exit.
    if is_4chan_thread(url):
        print(f"Downloading thread [{url}] to [{download_path}]")
    else:
        print(f"Invalid thread url [{url}]. Stopping ripper.")
        exit()

    thread_name = extract_thread_name(url)
    download_path = ripper.create_dir(download_path, thread_name)

    urls = extract_thread_media_urls(url)
    for url in urls:
        ripper.download_file(url, download_path)
