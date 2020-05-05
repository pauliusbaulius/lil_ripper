from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lilripper",
    version="0.0.9",
    description="Reddit subreddit/4chan archival tool, can download pictures, videos, gifs from i.reddit, v.reddit, imgur, gfycat. Requires ffmpeg to download v.reddit videos.",
    author="pauliusbaulius",
    license="MIT",
    url="https://github.com/pauliusbaulius/lil_ripper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Natural Language :: English",
        "Topic :: Internet"
    ],
    install_requires=[
        "beautifulsoup4 >= 4.9.0",
        "requests >= 2.23.0",
        "fake-useragent >= 0.1.11"
    ],
    packages=find_packages(),
    python_requires=">=3.8"
    # FIXME Stuff that is not needed? No idea what to do with it. Gonna need some help.
    #scripts=["src/cli.py"]
    # entry_points={
    #     "console_scripts": ["lilripper=src.cli:main"]
    # }
    # py_modules=[""],
    # package_dir={"": "src"},
)
