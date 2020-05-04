from src.modules import reddit


def test_is_reddit_webm():
    legit_webm_link = "https://v.redd.it/h6w76wza6o841"
    link_two = "https://redd.it/h6w76wza6o841"
    link_three = "www.reddit.com"
    assert reddit.is_reddit_webm(legit_webm_link) is True
    assert reddit.is_reddit_webm(link_two) is False
    assert reddit.is_reddit_webm(link_three) is False


