# lil ripper

A multiprocess-python program for subreddit archiving purposes. Lil ripper will try to extract all media links from subreddit posts and download them. Duplicate files will be ignored. Lil ripper uses [pushshift](https://pushshift.io/) to generate .json links containing media links. Downloading is then distributed between multiple processes. Downloading also introduces a delay between 1 and 5 seconds for normal links and additional delay for gfycat links, to not get your ip blacklisted from the site. *Happens almost instantly if you are not using good headers and spamming them with requests. Be gentle.*
Generating json files from pushshift will take some time, because lil ripper sleeps between requests to make 1 request per second.

:sunglasses: Works on GNU/Linux systems only, I assume, since I haven't tested it on other operating systems that I don't have. :sunglasses:




## Supported download links
- [x] direct link ending in valid format given by user
- [x] i.reddit
- [x] imgur direct link
- [x] imgur album
- [x] imgur album with one item aka no /a/ in link
- [x] gfycat

## Usage

Works with Linux CLI. 

```
lilripper.py
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
