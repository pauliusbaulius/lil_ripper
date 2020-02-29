# lil parser - ripper

A python program to archive subreddit media. Will handle most of media urls. C00mers dream - gonewild archived in a day.
It is not a complete archival tool, since some media hosted on 3rd party weird sites will not be downloaded if it is not a direct link.

**lil parser** - given a list of subreddits, it will build a database table for subreddit containing all post url's it can find.
Uses pushshift to download post json files, each one containing 1000 posts. Iterates downwards until subreddit creation date is reached.
Uses SQLite for it's database.

**lil ripper** - in progress... 

## supported download links
- [x] direct link ending in valid format
- [x] i.reddit
- [x] imgur direct link
- [x] imgur album
- [ ] imgur album with one item aka no /a/ in link
- [x] gfycat

## usage

lil parser takes a txt file with subreddits. Each line should be a subreddit.
It also requires you to specify goal database.
lil parser can be executed using *lilparser --input <your_file>.txt --database <db_name>.db*

lil ripper takes database name and subreddit name. Will download yet not downloaded media.

## settings.json -> use args
- [ ] perkelt settings.json i cli arguments

**formats_to_rip**:
	Specify which formats to download. File formats not in this list will be ignored.

**logging**:
	If true, will create a log file of the operation. Can be done with leenox commands, but this is for n00bs.

**download_directory**:
	Absolute location where your stuff will be saved. Works as base directory, since each subreddit and imgur album will have their own folders.

**reddit_batch_size**:
	How many posts you want to fit in one JSON request. Maximum is 1000.

**time_interval_in_days**:
	For reddit downloader. Used together with reddit_batch_size. If you think a subreddit gets 1000 posts a day, make interval one day.    If it is a smallish subreddit, can go up to a month.

**sleep_time_in_seconds**:
	How many seconds to sleep between requests. 1 = 1s, 0.5 = half a second etc... If you don't want to get blacklisted, don't overload servers.    Especially with gfycat. It does blacklist IP from VPN if you abuse them. Happened a lot during testing.



## to-do

- [ ] compress images to reduce storage usage
- [ ] automatically delete `ìmage deleted` images from imgur...
- [ ] rip from txt list with subreddits
- [ ] show total network usage
- [x] show total time
- [ ] show compression gains
- [x] continue-stop from certain time range instead of going from today to sub creation, takes a while to go thru already downloaded stuff.
- [x] database containing information about posts
- [x] new and improved pushshift iterator
- [ ] call lil ripper using args in terminal