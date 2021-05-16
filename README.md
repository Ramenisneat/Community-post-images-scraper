# Youtube Community Posts + Image scraper

### **Purpose**

You ever saw a youtube channel that had some *quality* posts that gave you the urge to archive them, *\*ahem\** Kamitsurugi *\*ahem\**?
No? Welp, if you ever do, you can use my crappy, unoptimized tool. No worries.

### **Usage**

You will need to have to get selenium for python and all other needed libraries should be default.

Make a `.env` that follows the provided `.env.example`. `CHANNEL` is obviously the channel name and `FOLDER` is the folder the script needs to create and use; can be expressed as a full path.

The `scraper.py` file uses argparse and therefore has an `-h` help option.
There's only 2 flags available:
- `-s` : This one scrapes all the available community posts from the specified channel. Stores the available posts in `urls.txt` and images in `FOLDER`.
- `-u` : Since Youtube limits how far back you can view the posts, better run the update utility time to time so the posts are up to date. The settings again taken from the `.env`. I use a simple CRON job that timely runs this.
