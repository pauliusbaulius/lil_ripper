import os
import subprocess
import requests

"""
Reddit's video posts are hosted on v.redd.it. Reddit does not let you download those videos directly, 
you have to extract direct link to video using .json of the post and finding fallback_url property.
Those videos come with no sound, but sound can be downloaded in a separate file and then merged
together using ffmpeg. It is a workaround, but it seems to work fine.
Requests also uses Firefox user's header, because reddit does not like programs interacting with them,
without a header, you will get HTTP ERROR 429.
"""
# todo use reddit api with a bot to not use some headers as a 3rd party scrapper.


def is_reddit_webm(url):
    """Hacky test to see whether the url leads to reddit video which should be a webm or not."""
    return "v.redd.it" in url


def download_reddit_webm(url, download_path):
    """
    Given a valid url to reddit video post and a download path,
    it will try to extract video uri and matching audio uri.
    Then it will download those files and call function to merge them.
    :param url: Reddit post url containing a video.
    :param download_path: Download path to store video.
    :return: Returns a boolean, True if everything succeeded, False if something went wrong.
    """
    # todo handle exceptions better than just printing trace and returning false.
    try:
        # Post id will be filename
        webm_filename = str(url).split("/")[-3]
        audio_filename = webm_filename + "_audio"
        # Json url is just reddit post url with ".json" appended to the end.
        json_url = url + ".json"
        # Download post json file and make it into json object.
        r = requests.get(json_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0'})
        json_data = r.json()
        # Extract webm url from json data...
        webm_url = json_data[0]["data"]["children"][0]["data"]["media"]["reddit_video"]["fallback_url"]
        # Split url into parts by "/", remove last elements, join back into string and append "/audio"
        # This creates audio url for the webm.
        audio_url = "/".join(webm_url.split("/")[0:-1]) + "/audio"
        # Download both files and merge into one video if both files got downloaded.
        download_file(f"{webm_filename}.mp4", webm_url, download_path)
        download_file(f"{audio_filename}.mp4", audio_url, download_path)
        join_video_audio(f"{webm_filename}.mp4", f"{audio_filename}.mp4", download_path)
        return True
    except Exception as error:
        print(error.with_traceback())
        return False


def download_file(webm_filename, webm_url, download_path):
    webm_content = requests.get(webm_url).content
    with open(os.path.join(download_path, webm_filename), "wb") as f:
        f.write(webm_content)
        print(f"Downloaded [{webm_url}]")
        return True


def join_video_audio(filename_video, filename_audio, path):
    """Uses ffmpeg to merge audio and video files together into one mp4 file."""
    try:
        # Go to location of webm files.
        os.chdir(path)
        # Call shell and merge audio with video using ffmpeg.
        command = f"ffmpeg -y -i {filename_video} -i {filename_audio} -c:v copy -c:a aac -strict experimental reddit_{filename_video}"
        # stdout and stderr to hide shell output, since it would cause a lot of additional spam.
        subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # Delete audio file after merging.
        os.remove(filename_audio)
        os.remove(filename_video)
        return True
    except Exception as error:
        print(error.with_traceback())
        return False


if __name__ == "__main__":
    print("Will run tests.")
    # todo run pytests
    download_reddit_webm("https://www.reddit.com/r/Idiotswithguns/comments/fdxn2q/soarcarl_gets_banned_on_twitch/", "/home/joe/github/lil_ripper/testing_grounds")
    download_reddit_webm(download_path="/home/joe/github/lil_ripper/testing_grounds", url="https://www.reddit.com/r/Idiotswithguns/comments/fdyj21/interesting_way_to_propose/")