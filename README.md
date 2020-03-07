# lil ripper

A multiprocess-python program for subreddit archiving purposes. It will try to extract all media links from subreddit posts and download them. It uses [pushshift](https://pushshift.io/) to generate json links containing Reddit post data. **Generating links will take a while, to not spam pushshift with API calls.** Be patient.



## Features

:clown_face:Does not download already downloaded files if same directory is given.

:ghost:Downloading is distributed between multiple processes. 

:alien: Downloading introduces a delay between 1 and 5 seconds for normal links and additional delay for gfycat links, to not get your ip blacklisted. *Happens almost instantly if you are not using good headers and spamming them with requests. Be gentle.*

:sunglasses: Only tested on GNU/Linux systems.




## Supported download links
- [x] direct link ending in valid format given by user
- [x] i.reddit
- [x] imgur direct link
- [x] imgur album
- [x] imgur album with one item aka no /a/ in link
- [x] gfycat



## Usage

```
python lilripper.py
-r, --rip <subreddit(s), csv(s)>
	items you wish to use for indexing/ripping
	
-u, --min-upvotes <integer> 
	minimum upvotes to consider a post for ripping/indexing.
	default minimum is 5 upvotes.

-d, --download-path <path>
	location for downloads, empty will use default location

-f, --formats <space separated extensions> 
	formats to download
```



## Examples

```bash
# Download from r/cars, posts with >= 100 upvotes and store in custom directory.
python3 lilripper.py -r cars -u 100 -d /run/media/joe_mama/hoarding/downloads

```
