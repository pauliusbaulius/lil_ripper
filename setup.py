from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="lil-ripper",
    version="0.0.2",
    description="Reddit subreddit archival tool, can download pictures, videos, gifs from i.reddit, v.reddit, imgur, gfycat. Requires ffmpeg to download v.reddit videos.",
    author="pauliusbaulius",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #py_modules=[""],
    #package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 4 - Beta",
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
    #scripts=["src/cli.py"]
    entry_points={
        "console_scripts": ["ripper=src.cli:main"] # TODO this is okay?
    }
)
