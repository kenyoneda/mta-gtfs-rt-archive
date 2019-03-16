####################################################################################################

Description: Archive of MTA's GTFS-Realtime feeds. Packaged into archives every hour (one per feed).
Every archive contains 120 files as the feed is generated every 30 seconds.

For list of feeds, see:

    http://datamine.mta.info/list-of-feeds

Archives are named in the following format:

    {feed}-{year}-{month}-{day}-{hour}.tar.bz2

    e.g. feed26-2018-04-28-00.tar.bz2

To access via API, use following URL structure:

    https://2m9ldwhcmh.execute-api.us-east-2.amazonaws.com/gtfs_rt/historic.mta/{feed}/{year}/{month}/{day}/{archive}

    e.g. https://2m9ldwhcmh.execute-api.us-east-2.amazonaws.com/gtfs_rt/historic.mta/feed26/2018/04/28/feed26-2018-04-28-00.tar.bz2


Archive Start: 16:00:00 EST, 27 April 2018

Throttling: Limited to 10 requests per second

####################################################################################################

TMUX session is running data fetcher script (gtfs_rt_fetcher.sh)

CRONTAB contains 2 scheduled jobs:
1. Clean up everyday at 02:00AM (clean_empty_dirs.sh)
2. Upload to S3 every hour on the first minutea (gtfs_rt_uploader.py)
