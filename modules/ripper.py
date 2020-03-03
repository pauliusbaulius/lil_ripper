

def rip_subreddit(subreddit_name, continue_download, download_location, database_location, min_upvotes):
    """
    Given a subreddit name, tries to download all media files from links found in the database.
    If subreddit table is not found, indexes it first before downloading.
    Downloadable media file formats, default download location and database location can be changed in settings.json.
    """
    print("called rip_subreddit", subreddit_name, download_location, database_location, min_upvotes, continue_download)
    # todo implement check for db, if needed update
    # if not in db, index
    # if in db, start downloading and setting status=1 if success
    # if continue_download=False, ignore status! or set to 0


def rip_all(continue_download, download_location):
    """
    Tries to download all media files from links found in database tables.
    """
    print("called rip_all", download_location)
    # todo just iterate over each table and


