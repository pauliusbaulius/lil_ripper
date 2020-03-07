import argparse
import os
import sys
from modules import tools, new_ripper
from testing_grounds import indexer, downloader

# default_database = tools.load_settings()["database"]
# default_download = tools.load_settings()["download_directory"]
# default_formats = tools.load_settings()["formats_to_rip"]
DOWNLOAD_FORMATS = ["jpg", "jpeg", "png", "gif", "mp4", "webm"]


def get_args(arguments=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="lil ripper, your #1 choice for subreddit archiving!")
    # Only allow to either index or rip, not both at once!
    parser.add_argument("-r", "--rip",
                        nargs="+",
                        help="specify what to rip: subreddit(s), csv(s)",
                        required=True
                        )
    parser.add_argument("-u", "--min-upvotes",
                        type=int,
                        help="minimum amount of upvotes to index/download a post. default is 0.",
                        default=5)
    parser.add_argument("-d", "--download-path",
                        help="path to download to. no input uses current location.",
                        default=os.getcwd())
    parser.add_argument("-f", "--formats",
                        help="formats to consider. no input uses default formats from settings.json",
                        default=DOWNLOAD_FORMATS)
    arguments = parser.parse_args(arguments)
    return arguments


def handle_args(arguments):
    print(arguments)
    print(arguments.rip)
    print(arguments.min_upvotes)
    print(arguments.download_path)
    print(arguments.formats)

    print(f"Starting ripping: {', '.join(arguments.rip)}")
    for item in arguments.rip:
        # If it is a csv file, extract subreddits and pass to ripper one by one.
        if str(item).endswith(".csv"):
            subreddits = tools.load_csv(item)
            for subreddit in subreddits:
                new_ripper.ripper(subreddit_name=subreddit,
                                  download_location=arguments.download_path,
                                  min_upvotes=arguments.min_upvotes,
                                  formats=arguments.formats)
        else:
            new_ripper.ripper(subreddit_name=item,
                              download_location=arguments.download_path,
                              min_upvotes=arguments.min_upvotes,
                              formats=arguments.formats)


if __name__ == "__main__":
    args = get_args()
    handle_args(args)
    #python3 lilripper.py -r cars -u 100 -d /run/media/joe/ProjectX/linux_downloads/uhh

