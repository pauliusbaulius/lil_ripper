from setuptools import setup

setup(
    name="lil-ripper",
    version="0.0.1",
    description="Reddit subreddit media archival tool. Able to download images, videos, gifs, webms.",
    py_modules=[],
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Operating System :: Unix",
        "License :: OSI Approved :: " # TODO generate and add LICENSE
    ],
    install_requires=[
        "beautifulsoup4 >=", # TODO versions bruh
        "requests >=",
        "fake_useragent >="
    ],
    extras_require={
        "dev": [
            "pytest >="
        ]
    }

)