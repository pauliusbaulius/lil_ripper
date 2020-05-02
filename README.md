

# lil_ripper <a name="project">

Lil ripper is a media archival tool for subreddits. It downloads images and video files from given subreddit(s) by extracting all urls from posts. It uses [pushshift](https://pushshift.io/) to generate json links containing Reddit post data, which includes urls. **Generating links will take a while, to not spam pushshift with API calls.** Be patient, program is not frozen. If you are trying to archive a big subreddit, there might be a few thousand of urls that have to be parsed.

**This project requires `ffmpeg` to download v.reddit videos**, since they are made out of two parts. One file is video without sound, another is just sound. `ffmpeg` is used to join both files together and create one `.webm`. 

Since this project does not eploy proxies, you may encounter trouble with subreddits that contain a lot of gfycat links. Gfycat does not like people scrapping their website and will blacklist your IP for several hours, if you make a lot of requests. This is a problem I am trying to solve in next updates.



### Currently supported links

- [x] direct uri to the media file
- [x] i.reddit
- [x] v.reddit
- [x] imgur direct link
- [x] imgur album
- [x] imgur album with one item aka no /a/ in link
- [x] gfycat video



## Table of contents <a name="toc">

1. [Project](#project)
2. [Table of contents](#toc)
3. [Installation](#installation)
4. [Usage](#usage)
   1. [Developers](#developers)
5. [Roadmap](#roadmap)
6. [Changelog](#changelog)
7. [More Documentation](#documentation)
8. [Authors and acknowledment](#aaa)
9. [License](#license)



## Installation <a name="installation">

Lil ripper can be installed via pip, since it has been uploaded to [pypi](https://pypi.org/). Type `pip3 install lilripper` in your shell to install it. You can then call `python3 -m lilripper <arguments>`. Take a look at [usage](#usage) for examples.

If you do not want to install a pip package, you can clone the project and then execute `python3 lilripper <arguments>` in the root directory.



## Usage <a name="usage">

Following arguments can be passed:

```
-r, --rip <subreddit(s)>
	subreddit(s) you want to archive
	
-u, --min-upvotes <integer> 
	minimum upvotes to consider a post for ripping/indexing.
	default minimum is 5 upvotes.

-d, --download-path <path>
	location for downloads, empty will use current location.
```



Some examples:

```python
# Download all possible media from r/dankmemes from posts with >=10.000 upvotes to Downloads directory. It will create a folder "dankmemes".
python3 -m lilripper -r dankmemes -u 10000 -d /home/boolean/Downloads

# Download all possible media from r/dankmemes and r/memes with >=1.00 upvotes to Download directory. Will create directories for each subreddit.
python3 -m lilripper -r dankmemes memes -u 1000 -d /home/boolean/Downloads
```



### Developers <a name="developers">

- pauliusbaulius



## Roadmap <a name="roadmap">

- [ ] fix -f flag, since it does not work at all anymore.
- [ ] A separate queue for gfycat videos that waits longer between requests to evade IP ban or something that at least reduces the frequency of bans.
- [ ] 4chan thread media archiving, under -c flag.
- [ ] pinterest board media archiving, under -p flag.
- [ ] add pytest tests, something I have to learn to write.
- [ ] a better way to quit program, since ctrl+c does not cancel all threads at once.
- [ ] show status how long it took to generate links and download each file. maybe a progress bar?

## Changelog <a name="changelog">

All changes are documented in CHANGELOG.md file in the root directory.



## Authors and acknowledgment <a name="aaa">

[Martin Heinz](https://martinheinz.dev/) for his Python template setup, which I modified and adapted right here.



## License <a name="license">

This project is licensed under [MIT](https://choosealicense.com/licenses/mit/) License..