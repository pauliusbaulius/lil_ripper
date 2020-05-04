import os
import random
from datetime import time
import time
import requests
from fake_useragent import UserAgent


def timer(func):
    def f(x, y):
        before = time()
        return_value = func(x, y)
        after = time()
        # TODO add this to DEBUG logger with time in ms/s and func name
        print(f"calculated in {after - before}")
        return return_value
    return f


def create_dir(base_path: str, new_dir: str) -> str:
    """
    If directory does not exist, make one. Otherwise return already existing directory.
    :param base_path: base directory where to create new directory.
    :param new_dir: name of the new directory.
    :return: path to new/existing directory.
    """
    full_path = os.path.join(base_path, new_dir)
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"New directory [{full_path}] was created.")
        return full_path
    else:
        print(f"Directory [{full_path}] already exists.")
        return full_path


def download_file_new(url: str, path: str, formats: list):
    # TODO migrate to this downloader, since it supports format check.
    """
    Given a download path and file url, tries to download it.
    + Checks if file already exists before trying to download, skips if item
    exists.
    + Names files by their url endings.
    + Does not download files under 10KB to prevent downloading of deleted
    imgur image placeholders
    and other unwanted data!
    - Downloads only files with matching format.
    Returns status as boolean, True if file was downloaded, False if it wasn't.
    :param path: Download location.
    :param url: Link to resource to download.
    :return: True if file has been downloaded, False if file failed to download.
    """
    try:
        before = time.time()
        # Check if user wants the file first.
        if is_downloadable(url, formats):
            # Filename is url ending.
            filename = str(url).split("/")[-1]
            # Check if already exists, if not, download file.
            if not check_if_downloaded(path, filename):
                time.sleep(random.randint(1, 5))
                # Request is done using random browser agent.
                request = requests.get(url, headers={
                    'User-Agent': str(UserAgent().random)})
                # Save file content to variable.
                file_content = request.content
                # Do not download files under 10KB to not download imgur
                # deleted images and other most likely non-trivial stuff.
                if len(file_content) > 10240:
                    # Save file to disk.
                    with open(os.path.join(path, filename), "wb") as f:
                        f.write(file_content)
                        # Calculate size in human-readable format for UI.
                        size = sizeof_fmt(os.fstat(f.fileno()).st_size)
                        after = time.time()
                        print(f"Downloaded [{url}] [{size}] ["
                              f"{after - before:.2f}s]")
                        return True
                else:
                    print(f"File [{url}] is under 10KB in size, skipping...")
                    return False
            else:
                print(f"File [{filename}] already exists, skipping...")
                return False
    except Exception as error:
        # FIXME fix this band-aid exception!
        print(f"Downloading [{url}] has failed, skipping...")
        print(error)
        return False


def is_downloadable(url, formats):
    """Given one url and a list of formats,
    check whether the link leads to file we want to download."""
    # If it is a .gifv and .mp4 is to be downloaded, use that extra ugly check.
    return str(url).endswith(tuple(formats)) \
        or str(url).endswith("gifv") \
        and "mp4" in tuple(formats)


def check_if_downloaded(path, filename):
    """
    Given a path and filename, checks whether a file already exists or not.
    Returns True if file exists.
    :param path:
    :param filename:
    :return:
    """
    full_path = os.path.join(path, filename)
    if os.path.exists(full_path):
        return True


def sizeof_fmt(num, suffix='B'):
    """
    Calculates file size in human-readable format.
    Copy-pasted from StackOverflow, thanks to this dude:
    https://stackoverflow.com/questions/1094841/
    reusable-library-to-get-human-readable-version-of-file-size
    """
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def load_csv(csv_name):
    with open(csv_name) as f:
        content = f.readlines()
    # You may also want to remove whitespace characters like `\n` at the end
    # of each line.
    content = [x.strip() for x in content]
    return content


if __name__ == "__main__":
    pass
