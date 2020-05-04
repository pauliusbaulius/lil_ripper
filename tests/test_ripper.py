from src import ripper


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
