from src.modules import fourchan


def test_extract_thread_name():
    url_a = "https://boards.4channel.org/biz/thread/18841550"
    url_b = "https://boards.4channel.org/g/thread/51971506/the-g-wiki"
    name_a = fourchan.extract_thread_name(url_a)
    name_b = fourchan.extract_thread_name(url_b)
    assert "18841550" == name_a
    assert "the-g-wiki" == name_b


def test_is_4chan_thread():
    url_a = "https://boards.4chan.org/g/thread/444444"
    url_b = "https://boards.4channel.org/g/thread/51971506/the-g-wiki"
    assert fourchan.is_4chan_thread(url_a) == True
    assert fourchan.is_4chan_thread(url_b) == True
    assert fourchan.is_4chan_thread("im cool") == False
    assert fourchan.is_4chan_thread("https://boards.4channel.org/biz/") == False


def test_construct_download_url():
    incomplete_url = "//i.4cdn.org/g/1572537433319.gif"
    complete_url = fourchan.construct_download_url(incomplete_url)
    assert complete_url == "https://i.4cdn.org/g/1572537433319.gif"


def test_extract_thread_media_urls():
    # /g/ sticky should not expire, otherwise test will break lol
    url = "https://boards.4channel.org/g/thread/51971506/the-g-wiki"
    urls = fourchan.extract_thread_media_urls(url)
    assert len(urls) == 2
