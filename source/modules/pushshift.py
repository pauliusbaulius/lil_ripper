from datetime import datetime
from datetime import timedelta

from modules import test_nsfw

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
    # todo handle db errors!
    # todo take database name from args or settings.json
    db_connection = sqlite3.connect("../test.db")
    db_cursor = db_connection.cursor()
    db_rows = db_cursor.rowcount
    # Add each post as separate entry to db
    removed_post = 0
    for post in json_data["data"]:
        try:
            # If this is present in post json, it was removed, skip it.
            post["removed_by_category"]
            removed_post += 1
        except KeyError:
            try:
                # todo this db query is not safe from injection attacks and usernames that kill queries 8-)
                db_cursor.execute(
                    f'''INSERT OR REPLACE INTO {subreddit_name} VALUES ("{post["id"]}", {post["created_utc"]}, "{post["url"]}", "{post["author"]}", "{post["title"]}", NULL)''')
                # If new row was added, increment total.
                if db_rows < db_cursor.rowcount:
                    iteration_db_updates += 1
                    # todo idk why there are exceptions but this fixes. due to formatting. fix execute query.
            except Exception:
                pass
    db_connection.commit()
    db_connection.close()
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


def update_db(subreddit_name):
    """
    Tries to find all posts and add their data to database for further processing.
    Resumes where left of by default. When started will get new posts and continue updating db with older posts until everything is archived.
    :param subreddit_name: Subreddit name as string.
    """
    # For time measurement, prints total time taken by this function, even when it is cancelled.
    start_time = time.time()
    try:
        # todo get db name from settings! not hardcoded
        # todo put db connection and etc to separate function for DRY
        db_connection = sqlite3.connect("../test.db")
        db_cursor = db_connection.cursor()
        # Creates table if doesn't exist. Otherwise it will not work if subreddit was not archived before.
        db_cursor.execute(
            '''CREATE TABLE IF NOT EXISTS {} (post_id TEXT PRIMARY KEY, created_utc INTEGER, url TEXT, author TEXT, title BLOB, status TEXT)'''.format(
                subreddit_name))
        # Get highest utc and lowest utc from db, to skip parsing json data for existing entries, saves time. Let's resume.
        db_cursor.execute(f'''SELECT MAX(created_utc) FROM {subreddit_name}''')
        highest_db_utc = db_cursor.fetchone()[0]
        db_connection.close()
        # If there is nothing in db, start downloading everything.
        if highest_db_utc is None:
            highest_db_utc = 1
        # Parse new data
        pushshift_get_parse_add_timed(subreddit_name, int(time.time()), highest_db_utc)
        db_connection = sqlite3.connect("../test.db")
        db_cursor = db_connection.cursor()
        db_cursor.execute(f'''SELECT MIN(created_utc) FROM {subreddit_name}''')
        lowest_db_utc = db_cursor.fetchone()[0]
        # todo figure out how to close connection sooner, or is it not a big deal?
        db_connection.close()
        # Parse old data if doesn't exist. Should stop directly if there is nothing to parse.
        pushshift_get_parse_add_timed(subreddit_name, lowest_db_utc, 1)
        # Handle ctrl+c
        signal.signal(signal.SIGINT, signal.default_int_handler)
    except KeyboardInterrupt:
        print("program manually stopped.")
    finally:
        elapsed_time = time.time() - start_time
        # todo neveikia mes iteration_db_updates gets set to 0 before this prints
        print(
            f"updated r/{subreddit_name} database and added/updated {iteration_db_updates} lines in {timedelta(seconds=round(elapsed_time))}. FALSE DATA! IGNORE!")
        print(f"total {total_db_updates} of read/write operations to the db in this run.")


if __name__ == "__main__":
    # TESTING GROUNDS! lil parser is working 8-)
    #update_db("gonxxewild")
    subs = test_nsfw.parse_scroller_subs()
    #todo this can be parallelized 8-)
    for x in subs:
        update_db(x)


# todo concurrency https://stackoverflow.com/questions/18207193/concurrent-writing-with-sqlite3
# spawn multiple processes