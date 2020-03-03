import argparse
import sys
from modules import tools, indexer, downloader

default_database = tools.load_settings()["database"]
default_download = tools.load_settings()["download_directory"]


def get_args(arguments=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="lil ripper, your #1 choice for subreddit archiving!")
    # Only allow to either index or rip, not both at once!
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "--rip",
                       nargs="+",
                       help="specify what to rip: subreddit(s), csv(s), db(s). no input uses default db as target.",
                       default=default_database)
    group.add_argument("-i", "--index",
                       nargs="+",
                       help="specify what to index: subreddit(s), csv(s).")
    parser.add_argument("-u", "--min-upvotes",
                        type=int,
                        help="minimum amount of upvotes to index/download a post. default is 0.",
                        default=0)
    parser.add_argument("-o", "--output",
                        help="path to download to. no input uses default download location. ",
                        default=default_download)
    parser.add_argument("-d", "--database",
                        help="path to database. no input uses default database. ",
                        default=default_database)
    # Handle continue/no-continue for downloads
    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument('--continue-download', dest='continue_download', action='store_true')
    feature_parser.add_argument('--no-continue-download', dest='continue_download', action='store_false')
    parser.set_defaults(feature=True)
    # todo what does this do?
    parser.add_argument("-v", "--verbose", dest='verbose', action='store_true', help="Verbose mode.")
    arguments = parser.parse_args(arguments)
    return arguments


def handle_args(arguments):
    # print(arguments)
    # print(arguments.rip)
    # print(arguments.index)
    # print(arguments.min_upvotes)
    # print(arguments.output)
    # print(arguments.database)
    # print(arguments.continue_download)
    # python3 main.py -i nsfw_subs.csv -u 5 -d /home/joe/github/lil_ripper/b.db 5

    # Handle indexing
    if arguments.index:
        print(f"Starting indexing: {', '.join(arguments.index)}")
        for item in arguments.index:
            if str(item).endswith(".csv"):
                subreddits = tools.load_csv(item)
                indexer.index_subreddits(subreddits=subreddits, min_upvotes=arguments.min_upvotes,
                                         default_database=arguments.database)
            else:
                indexer.index_subreddit(subreddit_name=arguments.index[0], min_upvotes=arguments.min_upvotes,
                                        database_location=arguments.database)

    # Handle ripping
    elif arguments.rip:
        print(f"Starting indexing and ripping: {', '.join(arguments.rip)}")
        for item in arguments.rip:
            # If it is a csv file, extract subreddits and pass to ripper one by one.
            if str(item).endswith(".csv"):
                subreddits = tools.load_csv(item)
                for subreddit in subreddits:
                    # todo start indexing and then ripping
                    downloader.rip_subreddit(subreddit_name=subreddit,
                                             download_location=arguments.output,
                                             database_location=arguments.database,
                                             min_upvotes=arguments.min_upvotes,
                                             continue_download=arguments.continue_download)
            # todo handle different sqlite extensions!
            # If it is a db, pass to db_ripper.
            elif str(item).endswith(".db"):
                downloader.rip_all(arguments.output)
            # If it is subreddit or list of subs, pass them to ripper one by one.
            else:
                # todo start indexing and then ripping
                downloader.rip_subreddit(subreddit_name=arguments.rip[0],
                                         download_location=arguments.output,
                                         database_location=arguments.database,
                                         min_upvotes=arguments.min_upvotes,
                                         continue_download=arguments.continue_download)


if __name__ == "__main__":
    args = get_args()
    handle_args(args)
