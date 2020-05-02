from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lil-ripper",
    version="0.0.1",
    description="reddit subreddit archival tool, can download pictures, videos, gifs from i.reddit, v.reddit, imgur, "
                "gfycat. requires ffmpeg.",
    py_modules=[""],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT",
        "Operating System :: Linux",
    ],
    install_requires=[
        "beautifulsoup4 >= 4.9.0",
        "requests >= 2.23.0",
        "fake-useragent >= 0.1.11"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown"
)
