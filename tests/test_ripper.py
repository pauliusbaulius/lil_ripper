from src import ripper


def test_create_dir():
    # TODO how to create temp dir for testing purposes and delete after?
    pass


def test_is_downloadable():
    # Should work with "." too.
    formats = [".jpg", "webm", "png"]
    link_one = "https://imgur.com/a/4ciLVAU"
    link_two = "https://i.imgur.com/46FuGK9.jpg"
    link_three = "https://i.imgur.com/vIf6U6Z.mp4"
    link_four = "https://i.imgur.com/2PbBGcy.webm"
    assert ripper.is_downloadable(link_one, formats) is False
    assert ripper.is_downloadable(link_two, formats) is True
    assert ripper.is_downloadable(link_three, formats) is False
    assert ripper.is_downloadable(link_four, formats) is True
    assert ripper.is_downloadable(".jpg", ["jpeg"]) is False
    assert ripper.is_downloadable(".jpg", ["jpg"]) is True
    assert ripper.is_downloadable(".jpg.webm", ["jpg"]) is False


def test_check_if_downloaded():
    is_downloaded = ripper.check_if_downloaded("test_dir/", "test.jpeg")
    assert is_downloaded

    is_downloaded = ripper.check_if_downloaded("test", "test.jpeg")
    assert is_downloaded is None

    is_downloaded = ripper.check_if_downloaded("test_dir", "test.gif")
    assert is_downloaded is None


def test_load_csv():
    subreddits = ripper.load_csv("test_dir/subreddits.csv")
    assert ['news', 'linux', 'programmingcirclejerk'] == subreddits
