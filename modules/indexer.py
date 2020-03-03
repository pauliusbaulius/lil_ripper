from datetime import datetime, timedelta
import signal
import requests
import time
from modules import tools
import sys


def fix_subreddit_name(subreddit_name):
    """
    Since sqlite does not support tables starting with a digit, we have to append something before that.
    This lil function appends "_" to the start of subreddit name if it starts with digit, and it also
    removes "_" if it finds it in the given string. So this one function can add and remove "_".
    """
    if subreddit_name[0].isdigit():
        return "_" + subreddit_name
    elif subreddit_name.startswith("_"):
        return subreddit_name[1:]
    else:
        return subreddit_name


def update_database(subreddit_name, json_link, min_upvotes, database_location):
    """
    Given a valid json url to reddit post data, it downloads the file and extracts data to db.
    Data added to db is post_id, created_utc, url, author and title.
    Returns created_utc of last post in json file. This is used to generate new json in parent function.
    :param min_upvotes:
    :param subreddit_name: Subreddit name as string.
    :param json_link: Url to json file containing post data.
    :return: Unix timestamp of last post creation date.
    """
    json_data = requests.get(json_link).json()
    sql_query_insert = f"""
                INSERT OR REPLACE INTO {subreddit_name} (post_id, created_utc, score, author, title, url, status)
                VALUES (?, ?, ?, ? ,? ,?, ?)
                """
    # Store post data here, insert into database when whole json is parsed to reduce needed db operations drastically.
    posts_to_insert = []
    with tools.get_db_connection(database_location) as db_connection:
        db_cursor = db_connection.cursor()
        # Add each post as separate entry to db
        for post in json_data["data"]:
            try:
                upvotes = post["score"]
                # Only add to database if upvote count is met.
                if upvotes >= min_upvotes:
                    values = (post["id"], post["created_utc"], upvotes, post["author"], post["title"], post["url"], 0)
                    posts_to_insert.append(values)
            except Exception:
                pass
        # Insert all parsed posts at once.
        db_cursor.executemany(sql_query_insert, posts_to_insert)
        db_connection.commit()
    return json_data["data"][-1].get("created_utc")


def download_data(subreddit_name, time_from, time_to, min_upvotes, database_location):
    """
    Given subreddit name, extracts all json urls containing post data.
    :param subreddit_name: Name of subreddit as string value
    :return: List of lists containing json urls.
    """
    # todo handle exception if url could not be opened, https://www.datasciencelearner.com/how-to-get-json-data-from-url-in-python/
    iteration = 0
    subreddit_name = fix_subreddit_name(subreddit_name)
    # Iterate downwards until we reach the end and error will be thrown, since no posts will be found in json file.
    try:
        # It just works - Todd Howard
        while True and time_from > time_to:
            iteration += 1
            start_time = time.time()
            json_link = f"https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit_name}" \
                        f"&sort=desc&sort_type=created_utc&before={time_from}&score=>{min_upvotes-1}&size=1000&is_self=false"
            # Insert json data into the database.
            time_from = update_database(subreddit_name, json_link, min_upvotes=min_upvotes, database_location=database_location)
            elapsed_time = time.time() - start_time
            print(f"For r/{subreddit_name} in iteration [{iteration}] parsed [{json_link}] up to post on "
                  f"[{datetime.utcfromtimestamp(time_from)}] in {elapsed_time:.2f} seconds.")
    except IndexError:
        # When all json files are generated, break loop and finish.
        print(f"{iteration} json url/s were generated, finished...")
    except TypeError:
        # todo well this creates table, do this before to not create table!
        print(f"Subreddit [{subreddit_name}] does not exist,")


# todo remove default db after testing!
def index_subreddit(subreddit_name, database_location, min_upvotes=0):
    """
    Tries to find all posts and add their data to database for further processing.
    Resumes where left of by default. When started will get new posts and continue updating db with older posts until everything is archived.
    :param min_upvotes: Minimum upvotes needed to index post. Default is 0. Leaving it at 0 indexes a lot of deleted spam posts.
    :param subreddit_name: Subreddit name as string.
    """
    # For time measurement, prints total time taken by this function, even when it is cancelled.
    start_time = time.time()
    # Handles the problem with database names cannot start with integer but subreddits can...
    subreddit_name = fix_subreddit_name(subreddit_name)
    try:
        with tools.get_db_connection(database_location) as db_connection:
            db_cursor = db_connection.cursor()
            # Creates table if doesn't exist. Otherwise it will not work if subreddit was not archived before.
            sql_query_table = f"""
            CREATE TABLE IF NOT EXISTS {subreddit_name} 
            (post_id TEXT PRIMARY KEY, created_utc INTEGER, score INTEGER, author TEXT, title BLOB, url TEXT, status INTEGER)
            """
            sql_query_time_max = f"""
            SELECT MAX(created_utc) 
            FROM {subreddit_name}
            """
            sql_query_time_min = f"""
            SELECT MIN(created_utc) 
            FROM {subreddit_name}
            """
            db_cursor.execute(sql_query_table)
            # Get highest utc and lowest utc from db, to skip parsing json data for existing entries, saves time. Let's resume.
            db_cursor.execute(sql_query_time_max)
            highest_db_utc = db_cursor.fetchone()[0]
            # If there is nothing in db, start downloading everything.
            if highest_db_utc is None:
                highest_db_utc = 1
            # Parse new data
            download_data(subreddit_name, int(time.time()), highest_db_utc, min_upvotes=min_upvotes, database_location=database_location)
            # Parse old data if doesn't exist. Should stop directly if there is nothing to parse.
            db_cursor.execute(sql_query_time_min)
            lowest_db_utc = db_cursor.fetchone()[0]
            download_data(subreddit_name, lowest_db_utc, 1, min_upvotes=min_upvotes, database_location=database_location)
            # Handle ctrl+c
            signal.signal(signal.SIGINT, signal.default_int_handler)
    except KeyboardInterrupt:
        print("Program manually stopped!")
        sys.exit()
    finally:
        elapsed_time = time.time() - start_time
        print(f"Indexed this subreddit in {timedelta(seconds=round(elapsed_time))}.")


def index_subreddits(subreddits, default_database, min_upvotes=0):
    for subreddit in subreddits:
        index_subreddit(subreddit, min_upvotes, default_database)


if __name__ == "__main__":
    # todo this can be parallelized 8-)
    # Test by parsing all nsfw subreddits.
    nsfw_subs = tools.load_csv("/home/joe/github/lil_ripper/nsfw_subs.csv")
    for sub in nsfw_subs:
        index_subreddit(sub, min_upvotes=5)
