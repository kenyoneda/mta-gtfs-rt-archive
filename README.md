TODO: Organize this README...

Update: As of 30 April 2020, LIRR/MNR is also being stored

####################################################################################################

Description: Archive of MTA's GTFS-Realtime feeds. Packaged into archives every hour (one per feed).
Every archive contains 120 files as the feed is generated every 30 seconds.

For list of feeds, see below:
    LINE(S) | FEED
    123456  | 1
    ACEHS   | 26
    NQRW    | 16
    BDFM    | 21
    L       | 2
    SIR     | 11
    G       | 31 
    JZ      | 36
    7       | 51
    LIRR    | -lirr
    MNR     | -mnr

    http://datamine.mta.info/list-of-feeds (deprecated as of 1 May 2020).
    
Note: As of 30 April 2020 (~2345 UTC), script is now downloading from https://api.mta.info/. However, old feed
ids (above) are still used for simplicity.


Archives are named in the following format:

    {feed}-{year}-{month}-{day}-{hour}.tar.bz2

    e.g. feed26-2018-04-28-00.tar.bz2

To access via API, use following URL structure:

    https://2m9ldwhcmh.execute-api.us-east-2.amazonaws.com/gtfs_rt/historic.mta/{feed}/{year}/{month}/{day}/{archive}

    e.g. https://2m9ldwhcmh.execute-api.us-east-2.amazonaws.com/gtfs_rt/historic.mta/feed26/2018/04/28/feed26-2018-04-28-00.tar.bz2


Archive Start: 16:00:00 EST, 27 April 2018
Archive Start (LIRR/MNR): 19:30:00 EST, 30 April 2020

Throttling: Limited to 10 requests per second

####################################################################################################

TMUX session is running data fetcher script (gtfs_rt_fetcher.sh)

CRONTAB contains 2 scheduled jobs:
1. Clean up everyday at 02:00AM (clean_empty_dirs.sh)
2. Upload to S3 every hour on the first minute (gtfs_rt_uploader.py)
