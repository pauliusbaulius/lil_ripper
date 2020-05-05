import concurrent.futures
import logging
import os
import subprocess
import time
from datetime import timedelta
import requests
from src import ripper
from fake_useragent import UserAgent
from src.modules import imgur, gfycat

"""
Reddit's video posts are hosted on v.redd.it. Reddit does not let you download those videos directly, 
you have to extract direct link to video using .json of the post and finding fallback_url property.
Those videos come with no sound, but sound can be downloaded in a separate file and then merged
together using ffmpeg. It is a workaround, but it seems to work fine.
Requests also uses Firefox user's header, because reddit does not like programs interacting with them,
without a header, you will get HTTP ERROR 429.
"""


def download_subreddit(subreddit_name: str, formats: list,
                       download_path: str, min_upvotes: int):
    """
    :param subreddit_name: Name of the subreddit you want to archive.
    :param formats: List of media file formats you want to download.
    :param download_path: Path to the location. A directory with subreddit's
    name will be created there.
    :param min_upvotes: Minimum amount of upvotes to download post's media.
    """
    start_time = time.time()

    # Create dir for downloads
    download_path = ripper.create_dir(download_path, subreddit_name)

    # Generate json urls for subreddit.
    print("Generating download links, might take a while...")
    json_urls = generate_pushift_urls(subreddit_name, int(time.time()), 1,
                                      min_upvotes, batch_size=1000)

    # Download files from each json
    for url in json_urls:
        download_from_json(url, formats, download_path)

    elapsed_time = time.time() - start_time
    print(f"Downloading finished in {timedelta(seconds=round(elapsed_time))}.")


def generate_pushift_urls(subreddit, utc_from, utc_to, min_upvotes,
                          batch_size=1000) -> list:
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
            json_link = f"https://api.pushshift.io/reddit/search/submission/" \
                        f"?subreddit={subreddit}" \
                        f"&sort=desc&sort_type=created_utc" \
                        f"&before={utc_from}" \
                        f"&score=>{min_upvotes - 1}" \
                        f"&size={batch_size}" \
                        f"&is_self=false"
            logging.debug(f"Generated pushshift url [{json_link}].")
            json_links.append(json_link)
            json_data = requests.get(json_link).json()
            utc_from = json_data["data"][-1].get("created_utc")
            # Sleep for 1 second to only make one api call per second.
            time.sleep(1)
    except IndexError:
        # When all json files are generated, break loop and finish.
        print(f"[{len(json_links)}] json links were generated. "
              f"Will start downloading...")
        logging.info(f"[{len(json_links)}] json links were generated. "
                     f"Will start downloading...")
    finally:
        logging.debug(f"All pushshift links [{json_links}].")
        return json_links


def download_from_json(json_url: str, formats: list, download_path: str):
    """
    Given one json url, extracts media urls.
    Passes them to media url handler.
    :param download_path:
    :param formats:
    :param json_url: Pushift json url.
    """
    try:
        urls = generate_urls_from_json(json_url)
        # Remove duplicate urls by converting to set and back.
        urls = list(set(urls))
        # Start parallel downloader here.
        with concurrent.futures.ProcessPoolExecutor() as parallel:
            [parallel.submit(handle_media_url, url, formats, download_path)
             for url
             in urls
             ]
    except Exception as error:
        print(f"Analyzing [{json_url}] has failed.")
        logging.error(f"Analyzing [{json_url}] has failed.")
        logging.error(error)
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


def handle_media_url(url: str, formats: list, download_path: str):
    """
    Given one url, it checks if it is downloadable and passes downloadable
    urls to downloader.
    Uses global variable to check formats.
    :param download_path:
    :param formats:
    :param url: Direct url of a file to download, aka URI.
    """
    # If it is a directly downloadable link ending in valid format.
    if ripper.is_downloadable(url, formats):
        logging.debug(f"Direct download [{url}].")
        # Make .gifv files into .mp4 files, to be playable on computers that do
        # not support .gifv.
        if str(url).endswith(".gifv"):
            url = url.replace(".gifv", ".mp4")
            ripper.download_file_new(url, download_path, formats)
        else:
            ripper.download_file_new(url, download_path, formats)
    # If it is a reddit webm
    elif is_reddit_webm(url):
        logging.debug(f"Reddit Webm [{url}].")
        handle_reddit_webm(url=url, download_path=download_path)
    # If it is an imgur album...
    elif imgur.is_imgur_album(url):
        print(f"Downloading imgur album [{url}]")
        logging.debug(f"Imgur album download [{url}].")
        # Need to pass dir to make imgur folder in subreddit folder.
        imgur.download_imgur_album(url=url, formats=formats,
                                   path=download_path)
    # If it is gfycat link...
    elif gfycat.is_gfycat_link(url):
        print(f"Downloading gfycat video [{url}]")
        logging.debug(f"Gfycat video download [{url}].")
        gfycat.handle_gfycat_url(url, download_path, formats)
    # Try to convert those imgur links with no file ending to .jpg and hope for
    # the best.
    elif imgur.is_imgur_single_image(url):
        logging.debug(f"Imgur single image download [{url}].")
        url = imgur.make_imgur_image(url)
        ripper.download_file_new(url, download_path, formats)
    else:
        print(f"Cannot download this url (yet): [{url}]")
        logging.info(f"Cannot download [{url}].")


def is_reddit_webm(url):
    """
    Hacky test to see whether the url leads to reddit video,
    which should be a webm or not.
     """
    return "v.redd.it" in url


def handle_reddit_webm(url, download_path):
    """
    Given a valid url to reddit video post and a download path,
    it will try to extract video uri and matching audio uri.
    Then it will download those files and call function to merge them.
    :param url: Reddit post url containing a video.
    :param download_path: Download path to store video.
    :return: Returns a boolean, True if everything succeeded,
    False if something went wrong.
    """
    # TODO handle exceptions better than just printing trace and returning
    # false.
    try:
        # If it is a v.redd.it link, get the post link!
        if url.startswith("https://v.redd.it/"):
            r = requests.get(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
            url = r.url
        # Post id will be filename
        webm_filename = str(url).split("/")[-3]
        # Check if there is one downloaded already.
        if not ripper.check_if_downloaded(download_path,
                                          f"reddit_{webm_filename}.mp4"):
            audio_filename = webm_filename + "_audio"
            # Json url is just reddit post url with ".json" appended to the end.
            json_url = url + ".json"
            # Download post json file and make it into json object.
            r = requests.get(json_url, headers={
                'User-Agent': str(UserAgent().random)})
            json_data = r.json()
            # Extract webm url from json data...
            webm_url = json_data[0]["data"]["children"][0]["data"]["media"][
                "reddit_video"]["fallback_url"]
            # Split url into parts by "/", remove last elements, join back into string and append "/audio"
            # This creates audio url for the webm.
            audio_url = "/".join(webm_url.split("/")[0:-1]) + "/audio"
            # Download both files and merge into one video if both files got downloaded.
            download_webm(f"{webm_filename}.mp4", webm_url, download_path)
            download_webm(f"{audio_filename}.mp4", audio_url, download_path)
            webm_join_video_audio(f"{webm_filename}.mp4",
                                  f"{audio_filename}.mp4", download_path)
            return True
        else:
            print(f"File [reddit_{webm_filename}.mp4] has been downloaded"
                  f" already, skipping...")
    except Exception as error:
        print("Could not download this webm! ERROR:", error)
        logging.error("Could not download this webm! ERROR:", error)
        return False


def download_webm(webm_filename, webm_url, download_path):
    webm_content = requests.get(webm_url).content
    with open(os.path.join(download_path, webm_filename), "wb") as f:
        f.write(webm_content)
        size = ripper.sizeof_fmt(os.fstat(f.fileno()).st_size)
        print(f"Downloaded [{webm_url}] [{size}]")
        return True


def webm_join_video_audio(filename_video, filename_audio, path):
    """Uses ffmpeg to merge audio and video files together into one mp4 file."""
    try:
        # Go to location of webm files.
        os.chdir(path)
        # Call shell and merge audio with video using ffmpeg.
        command = f"ffmpeg -y -i {filename_video} -i {filename_audio} -c:v copy -c:a aac -strict experimental reddit_{filename_video}"
        # stdout and stderr to hide shell output, since it would cause a lot of additional spam.
        # TODO print stdout and stderr to log if DEBUG
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL)
        # Delete audio file after merging.
        os.remove(filename_audio)
        os.remove(filename_video)
        print(
            f"Successfully merged audio and video into one file [reddit_{filename_video}]")
        return True
    except Exception as error:
        print(f"Could not merge into one video, ERROR:", error)
        return False


if __name__ == "__main__":
    pass
