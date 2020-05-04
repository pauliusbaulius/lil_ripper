import os
import sqlite3
import json
from definitions import ROOT_DIR


def load_csv(csv_name):
    with open(csv_name) as f:
        content = f.readlines()
    # You may also want to remove whitespace characters like `\n` at the end
    # of each line.
    content = [x.strip() for x in content]
    return content


def get_db_connection(database_name):
    # Check if default db has to be used, otherwise use new one.
    if database_name == load_settings()["database"]:
        database = load_settings()["database"]
        database_path = os.path.join(ROOT_DIR, database)
    else:
        database_path = database_name
    try:
        return sqlite3.connect(database_path)
    except sqlite3.Error as error:
        print(f"Could not open database: [{error}]")


def load_settings():
    settings_path = os.path.join(ROOT_DIR, "settings.json")
    try:
        with open(settings_path) as json_file:
            settings = json.load(json_file)
        return settings
    except json.decoder.JSONDecodeError:
        print("Could not load settings.json, check if file is formatted correctly!.")
    except FileNotFoundError:
        print("File settings.json could not be found. I refuse to work under such conditions.")


if __name__ == "__main__":
    print("Will run tests.")


