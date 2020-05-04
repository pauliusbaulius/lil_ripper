## Table of contents <a name="toc">

1. [Table of contents](#toc)
2. [Project](#project)
3. [Installation](#installation)
4. [Usage](#usage)
   1. [Developers](#developers)
5. [Roadmap](#roadmap)
6. [Changelog](#changelog)
7. [Authors and acknowledment](#aaa)
8. [License](#license)



# lil ripper <a name="project">

Lil ripper is a media archival tool for subreddits/chan threads. It downloads images and video files from given subreddit(s) by extracting all urls from posts. It uses [pushshift](https://pushshift.io/) to generate json links containing Reddit post data, which includes urls. **Generating links will take a while, to not spam pushshift with API calls.** Be patient, program is not frozen. If you are trying to archive a big subreddit, there might be a few thousand of urls that have to be parsed. Chan threads are downloaded without having to generate anything.

**This project requires `ffmpeg` to download v.reddit videos**, since they are made out of two parts. One file is video without sound, another is just sound. `ffmpeg` is used to join both files together and create one `.webm`. 

Since this project does not eploy proxies, you may encounter trouble with subreddits that contain a lot of gfycat links. Gfycat does not like people scrapping their website and will blacklist your IP for several hours, if you make a lot of requests. This is a problem I am trying to solve in next updates.



**! WORKS ON LINUX ONLY !** Since I haven't tested it on other systems, I made it Linux only. This might change in the future, when I will get access to a Windows machine and/or a Mac.

![https://i.imgur.com/BsNMI3a.png](https://i.imgur.com/BsNMI3a.png)

### Currently supported links

- [x] direct uri to the media file
- [x] i.reddit
- [x] v.reddit
- [x] imgur direct link
- [x] imgur album
- [x] imgur album with one item aka no /a/ in link
- [x] gfycat video
- [x] 4chan thread



## Installation <a name="installation">

Lil ripper can be installed via pip, since it has been uploaded to [pypi](https://pypi.org/). Type `pip3 install lilripper` in your shell to install it. You can then call `python3 -m lilripper <arguments>`. Take a look at [usage](#usage) for examples.

If you do not want to install a pip package, you can clone the project and then execute `python3 lilripper <arguments>` in the root directory.



## Usage <a name="usage">

Following arguments can be passed:

```
-r, --reddit <subreddit(s)>
	Subreddit(s) you want to archive
	
	-r cars, --reddit cars, -r homelab linux
	
-c, --fourchan <thread(s)>
	Downloads thread(s) you want to archive.

-u, --min-upvotes <integer> 
	Minimum upvotes to consider a post for ripping/indexing.
	Default minimum is 5 upvotes.
	
	-u 10, --min-upvotes 9999

-d, --download-path <path>
	Location for downloads, empty will use current location.
	
	-d /home/mamamia/Downloads/reddit

-f, --formats
	Formats of media files you want to download, leaving this blank
	will use default list of: ["jpg", "jpeg", "png", "gif", "mp4", "webm"]
	Notice: gifv links are converted to mp4, since mp4 is supported on more systems.
	If you wan't gifvs, you can pass mp4 to -f.
	
	-f jpg png, -f webm, --formats gif mp4 webm
```



Some examples:

```python
# Download all possible media from r/dankmemes from posts with >=10.000 upvotes to Downloads directory. It will create a folder "dankmemes".
python3 -m lilripper -r dankmemes -u 10000 -d /home/boolean/Downloads

# Download all possible media from r/dankmemes and r/memes with >=1.00 upvotes to Download directory. Will create directories for each subreddit.
python3 -m lilripper -r dankmemes memes -u 1000 -d /home/boolean/Downloads

# Download all media from a thread in /g/.
python3 -m lilripper -c https://boards.4channel.org/g/thread/51971506/the-g-wiki -d /home/boolean/Downloads
    
# Download all webms from a subreddit.
python3 -m lilripper -r idiotsincars -f webm -d /home/boolean/Downloads
```



### Developers <a name="developers">

#TODO information how to build the package, run tests and create venv.



## Roadmap <a name="roadmap">

- [x] fix -f flag, since it does not work at all anymore.
- [ ] A separate queue for gfycat videos that waits longer between requests to evade IP ban or something that at least reduces the frequency of bans.
- [x] 4chan thread media archiving, under -c flag.
- [ ] pinterest board media archiving, under -p flag.
- [ ] add pytest tests, something I have to learn to write.
- [ ] a better way to quit program, since ctrl+c does not cancel all threads at once.
- [ ] show status how long it took to generate links and download each file. maybe a progress bar?
  - [x] download time
  - [ ] generation time
  - [ ] progress bar
- [ ] add image/video compression option to reduce size of media on disk in exchange for cpu usage and electricity.
- [ ] skip v.reddit videos if user has no ffmpeg, check for it first.



## Changelog <a name="changelog">

[0.0.7] 

- You can now download 4chan threads with -c flag.
- -f flag is working as intended.

## Authors and acknowledgment <a name="aaa">

Nothing yet, reserved for contributors.



## License <a name="license">

This project is licensed under [MIT](https://choosealicense.com/licenses/mit/) License.