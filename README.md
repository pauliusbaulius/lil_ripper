# lil ripper

A python program to index and download entire subreddits. *It is not a complete archival tool, since some media hosted on 3rd party weird sites will not be downloaded if it is not a direct link.*



## Supported download links
- [x] direct link ending in valid format
- [x] i.reddit
- [x] imgur direct link
- [x] imgur album
- [ ] imgur album with one item aka no /a/ in link
- [x] gfycat



## Usage

Works with Linux CLI. 

```
lilripper.py
-r, --rip <subreddit(s), csv(s), db(s)> 
	items you wish to use for indexing/ripping

-i, --index <subreddit(s), csv(s)> 
	items you wish to use for indexing
	
-u, --min-upvotes <integer> 
	minimum upvotes to consider a post for ripping/indexing.
	default minimum is 0 upvotes.

-o, --output <path> 
	location for downloads, empty will use default location

-d, --database <path> 
	location of db for indexing, empty will use default location

-f, --formats <space separated extensions> 
	formats to download

--continue-download 
	does not continue downloading from last download in database, looks for first 	downloaded=0 flag.

--no-continue-download 
	ignores flags, downloads from first to last entry in database

--no-index 
	does not build index before ripping, goes directly to downloading from newest to oldest post in subreddit(s)
```



## Examples

```bash
# download jpg, png, gif media files from posts with >= 1000 upvotes from r/dankmemes and put in downloads folder
lilripper.py -r dankmemes -u 1000 --no-index -f jpg png gif -o /home/picklerick/downloads/

# index subreddits in csv file, consider posts with >=5 upvotes only and put data in ripper.db
lilripper.py -i cool_subs.csv -u 5 -d /home/pickerick/databases/ripper.db

# index subreddit r/dankmemes and use default database and default upvote count.
lilripper.py -i cool_subs.csv

python lilripper.py -i dankmemes -u 1000 -d dankmemes_test.db
```



## settings.json
**database**:

​	Default location of index database.

**formats_to_rip**:
	Specify which default formats to download. File formats not in this list will be ignored.

**download_directory**:
	Absolute location where your stuff will be saved. Works as base directory, since each subreddit and imgur album will have their own folders.



## to-do

- [ ] compress images to reduce storage usage
  - [ ] show compression gains
- [x] rip from csv list with subreddits
- [ ] show total network usage
- [x] continue-stop from certain time range instead of going from today to sub creation, takes a while to go thru already downloaded stuff.
- [x] database containing information about posts
- [x] new and improved pushshift iterator
- [x] call lil ripper using args in terminal