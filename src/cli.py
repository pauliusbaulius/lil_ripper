#!/usr/bin/env python3

import argparse
import os
import sys
from src import ripper
from src.modules import fourchan, reddit

DEFAULT_DOWNLOAD_FORMATS = ["jpg", "jpeg", "png", "gif", "mp4", "webm"]
DEFAULT_DOWNLOAD_PATH = os.getcwd()


def main():
    # TODO logger init here!
    args = get_args()
    handle_args(args)


def get_args(arguments=None):
    if arguments is None:
        arguments = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="lil ripper, your #1 choice for media archiving!")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--reddit",
                       nargs="+",
                       help="Subreddit(s) to download."
                       )
    group.add_argument("-c", "--fourchan",
                       nargs="+",
                       type=str,
                       help="4Chan thread(s) to download."
                       )
    parser.add_argument("-u", "--min-upvotes",
                        type=int,
                        help="Minimum amount of upvotes to download a post. "
                             "Default is 5.",
                        default=5)
    parser.add_argument("-d", "--download-path",
                        help="Path to download to. No input uses current dir.",
                        default=DEFAULT_DOWNLOAD_PATH)
    parser.add_argument("-f", "--formats",
                        nargs="+",
                        help="Formats to consider. Default downloads all.",
                        default=DEFAULT_DOWNLOAD_FORMATS)
    arguments = parser.parse_args(arguments)
    return arguments


def handle_args(arguments):
    # print(arguments) # TODO debug, remove when building package!

    if arguments.reddit is not None:
        handle_reddit(arguments)
    if arguments.fourchan is not None:
        handle_fourchan(arguments)


def handle_reddit(arguments):
    print(f"Starting ripping: [{', '.join(arguments.reddit)}]")
    subreddits = []
    for item in arguments.reddit:
        # If it is a csv file, extract subreddits to a list.
        if str(item).endswith(".csv"):
            subreddits.append(ripper.load_csv(item))
        else:
            subreddits.append(item)

    for subreddit in subreddits:
        reddit.download_subreddit(subreddit_name=subreddit,
                                  download_path=arguments.download_path,
                                  min_upvotes=arguments.min_upvotes,
                                  formats=arguments.formats)


def handle_fourchan(arguments):
    print(f"Starting ripping: [{', '.join(arguments.fourchan)}]")
    for url in arguments.fourchan:
        fourchan.download_thread(url=url,
                                 download_path=arguments.download_path,
                                 formats=arguments.formats)


if __name__ == "__main__":
    main()
