# todo get both from settings.json
default_download_location = ""
default_database_location = ""


def rip_subreddit(subreddit_name, download_location=default_download_location, database_location=default_database_location):
    """
    Given a subreddit name, tries to download all media files from links found in the database.
    If subreddit table is not found, indexes it first before downloading.
    Downloadable media file formats, default download location and database location can be changed in settings.json.

    :param subreddit_name: Name of subreddit to download files from.
    :param download_location: Directory to place downloaded files in, if left blank - default location from settings.json will be used.
    :param database_location: Location of database containing links if left blank - default location from settings.json will be used.
    """
    pass


def rip_all(download_location=default_download_location):
    """
    Tries to download all media files from links found in database tables.
    :param download_location: Directory to place downloaded files in, if left blank - default location from settings.json will be used.
    """
    pass

