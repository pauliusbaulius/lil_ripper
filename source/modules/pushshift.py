from datetime import datetime
from datetime import timedelta
from source.modules import test_nsfw
import signal
import requests
import time
import sqlite3

# Global var to track total insertions to db. Clean code preachers hate him.
total_db_updates = 0
iteration_db_updates = 0


def add_post_data_database(subreddit_name, json_link):
    """
    Given a valid json url to reddit post data, it downloads the file and extracts data to db.
    Data added to db is post_id, created_utc, url, author and title.
    Returns created_utc of last post in json file. This is used to generate new json in parent function.
    :param subreddit_name: Subreddit name as string.
    :param json_link: Url to json file containing post data.
    :return: Unix timestamp of last post creation date.
    """
    global total_db_updates
    global iteration_db_updates

    json_data = requests.get(json_link).json()
    # todo take database name from args or settings.json

    with sqlite3.connect("/home/joe/github/lil_ripper/test.db") as db_connection:
        db_cursor = db_connection.cursor()
        db_rows = db_cursor.rowcount
        # Add each post as separate entry to db
        for post in json_data["data"]:
            try:
                sql_query_insert = f"""
                    INSERT OR REPLACE INTO {subreddit_name} 
                    VALUES ("{post["id"]}", {post["created_utc"]}, "{post["url"]}", "{post["author"]}", "{post["title"]}", NULL)
                    """
                db_cursor.execute(sql_query_insert)
                # If new row was added, increment total.
                if db_rows < db_cursor.rowcount:
                    iteration_db_updates += 1
                    # todo idk why there are exceptions but this fixes. due to formatting. fix execute query.
            except Exception:
                pass
        db_connection.commit()
        total_db_updates += iteration_db_updates
    return json_data["data"][-1].get("created_utc")


def pushshift_get_parse_add_timed(subreddit_name, time_from, time_to):
    # todo handle exception if url could not be opened, https://www.datasciencelearner.com/how-to-get-json-data-from-url-in-python/
    iteration = 0
    """
    Given subreddit name, extracts all json urls containing post data.
    :param subreddit_name: Name of subreddit as string value
    :return: List of lists containing json urls.
    """

    subreddit_name = fix_subreddit_name(subreddit_name)

    # Iterate downwards until we reach the end and error will be thrown, since no posts will be found in json file.
    try:
        # It just works - Todd Howard
        while True and time_from > time_to:
            iteration += 1
            start_time = time.time()
            json_link = "https://api.pushshift.io/reddit/search/submission/?subreddit={}&sort=desc&sort_type=created_utc&before={}&size=1000&is_self=false".format(
                subreddit_name, time_from)
            time_from = add_post_data_database(subreddit_name, json_link)
            elapsed_time = time.time() - start_time
            print(f"for r/{subreddit_name} in iteration [{iteration}] parsed [{json_link}] up to post on [{datetime.utcfromtimestamp(time_from)}] in {elapsed_time:.2f} seconds.")
    except IndexError:
        # When all json files are generated, break loop and finish.
        print(f"{iteration} json url/s were generated, finished...")
    except TypeError:
        # todo well this creates table, do this before to not create table!
        print(f"subreddit [{subreddit_name}] does not exist,")


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


def update_db(subreddit_name):
    """
    Tries to find all posts and add their data to database for further processing.
    Resumes where left of by default. When started will get new posts and continue updating db with older posts until everything is archived.
    :param subreddit_name: Subreddit name as string.
    """
    # For time measurement, prints total time taken by this function, even when it is cancelled.
    start_time = time.time()
    # Handles the problem with database names cannot start with integer but subreddits can...
    subreddit_name = fix_subreddit_name(subreddit_name)

    try:
        with sqlite3.connect("/home/joe/github/lil_ripper/test.db") as db_connection:
            # todo get db name from settings! not hardcoded
            db_cursor = db_connection.cursor()
            # Creates table if doesn't exist. Otherwise it will not work if subreddit was not archived before.
            sql_query_table = f"""
            CREATE TABLE IF NOT EXISTS {subreddit_name} 
            (post_id TEXT PRIMARY KEY, created_utc INTEGER, url TEXT, author TEXT, title BLOB, status TEXT)
            """
            # todo also add upvotes! score:
            sql_query_table_new = f"""
            CREATE TABLE IF NOT EXISTS {subreddit_name} 
            (post_id TEXT PRIMARY KEY, created_utc INTEGER, score INTEGER, author TEXT, title BLOB, url TEXT, status TEXT)
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
            pushshift_get_parse_add_timed(subreddit_name, int(time.time()), highest_db_utc)
            db_cursor.execute(sql_query_time_min)
            lowest_db_utc = db_cursor.fetchone()[0]
            # Parse old data if doesn't exist. Should stop directly if there is nothing to parse.
            pushshift_get_parse_add_timed(subreddit_name, lowest_db_utc, 1)
            # Handle ctrl+c
            signal.signal(signal.SIGINT, signal.default_int_handler)
    except KeyboardInterrupt:
        print("program manually stopped.")
    finally:
        elapsed_time = time.time() - start_time
        print(f"indexed this subreddit in {timedelta(seconds=round(elapsed_time))}. \ntotal {total_db_updates} of read/write operations to the db in this run.")


if __name__ == "__main__":
    # TESTING GROUNDS! lil parser is working 8-)
    subs = test_nsfw.parse_scroller_subs()
    # todo this can be parallelized 8-)
    for x in subs:
        update_db(x)
