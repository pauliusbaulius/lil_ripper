import os
import subprocess

import requests


def is_reddit_webm(url):
    """Hacky test to see whether the url leads to reddit video which should be a webm or not."""
    return "v.redd.it" in url


def download_reddit_webm(url):
    # https://www.reddit.com/r/Idiotswithguns/comments/fdxn2q/soarcarl_gets_banned_on_twitch/.json

    # Post id will be filename
    filename = str(url).split("/")[-3]
    print(filename)

    # Json url is just reddit post url with ".json" appended to the end.
    json_url = url + ".json"
    json_data = requests.get(json_url).json()
    print(json_data)

    for item in json_data:
        print(item)

    webm_url = json_data["0"]["data"]["media"]["fallback_url"]
    print(webm_url)

    # extract json fallback_url
    # download that
    # replace fallback_url DASH with audio
    # download sound


    # todo strip everything up to first /

    # todo append audio to new url
    # todo download both urls
    # todo Cannot use default function, since they do not have file endings and have to be combined!


def join_video_audio(filename_video, filename_audio, path):
    os.chdir(path)
    #filename_video = os.path.join(path, filename_video)
    #filename_audio = os.path.join(path, filename_audio)
    # https://superuser.com/questions/277642/how-to-merge-audio-and-video-file-in-ffmpeg
    # Call shell and merge audio with video using ffmpeg.
    # todo test on linux
    # https://v.redd.it/m15irthkqvk41/audio
    # https://v.redd.it/m15irthkqvk41/DASH_720?source=fallback
    command = f"ffmpeg -i {filename_video}.mp4 -i {filename_audio}.mp4 -c:v copy -c:a aac -strict experimental {filename_video}.mp4"
    subprocess.call(command, shell=True)
    # Delete audio file after merging.
    os.remove(filename_audio)


if __name__ == "__main__":
    print("Will run tests.")
    # todo run pytests
    download_reddit_webm("https://www.reddit.com/r/Idiotswithguns/comments/fdxn2q/soarcarl_gets_banned_on_twitch/")
