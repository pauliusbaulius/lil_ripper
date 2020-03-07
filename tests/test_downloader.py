from testing_grounds import downloader


def test_is_reddit_webm():
    legit_webm_link = "https://v.redd.it/h6w76wza6o841"
    link_two = "https://redd.it/h6w76wza6o841"
    link_three = "www.reddit.com"
    assert downloader.is_reddit_webm(legit_webm_link) is True
    assert downloader.is_reddit_webm(link_two) is False
    assert downloader.is_reddit_webm(link_three) is False


def test_is_downloadable():
    # Should work with "." too.
    formats = [".jpg", "webm", "png"]
    link_one = "https://imgur.com/a/4ciLVAU"
    link_two = "https://i.imgur.com/46FuGK9.jpg"
    link_three = "https://i.imgur.com/vIf6U6Z.mp4"
    link_four = "https://i.imgur.com/2PbBGcy.webm"
    assert downloader.is_downloadable(link_one, formats) is False
    assert downloader.is_downloadable(link_two, formats) is True
    assert downloader.is_downloadable(link_three, formats) is False
    assert downloader.is_downloadable(link_four, formats) is True

