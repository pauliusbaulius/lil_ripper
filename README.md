# lil ripper

A python program to index and download entire subreddits. *It is not a complete archival tool, since some media hosted on 3rd party weird sites will not be downloaded if it is not a direct link.*
Uses [pushshift](https://pushshift.io/) to generate json files containing media urls, and downloads them using all of your cores. There is a random delay between downloads to not abuse providers.
Generating json files from pushshift will take some time, because lil ripper sleeps between requests to make 1 request per second.


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
