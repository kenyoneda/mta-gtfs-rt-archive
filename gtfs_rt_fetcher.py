'''
Script to continuously download MTA GTFS realtime data and save to disk
'''
import datetime
import os
import requests
import time

API_KEY = "API_KEY"
BASE_URL = "http://datamine.mta.info/mta_esi.php?key={}&feed_id={}"
FEED_IDS = {'123456S': '1',
            'ACEHS': '26',
            'NQRW': '16',
            'BDFM': '21',
            'L': '2',
            'SIR': '11',
            'G': '31',
            'JZ': '36',
            '7': '51'}
FEED_INTERVAL_SEC = 30
ROOT_DIR = 'data'
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H-%M-%S"
FILENAME = "feed{}-{}-{}"  # feed no, date, time


def get_gtfs_rt_data():
    '''Downloads GTFS real-time feed for every line'''
    for lines, feed in FEED_IDS.items():
        # Generate path to write files
        the_feed = 'feed' + feed
        d = datetime.datetime.utcnow()
        year = str(d.year)
        month = str(d.month).zfill(2)
        day = str(d.day).zfill(2)
        hour = str(d.hour).zfill(2)
        path = os.path.join(ROOT_DIR, the_feed, year, month, day, hour)

        # Download .proto file
        try:
            r = requests.get(BASE_URL.format(API_KEY, feed))
        except requests.exceptions.RequestException:
            continue

        if r.status_code == 200:
            # Write to disk
            if not os.path.isdir(path):
                os.makedirs(path)

            the_date = d.strftime(DATE_FORMAT)
            the_time = d.strftime(TIME_FORMAT)
            filename = FILENAME.format(feed, the_date, the_time)
            full_path = path + os.path.sep + filename
            with open(full_path, 'wb') as f:
                f.write(r.content)


def run_every(sec, func):
    '''Helper to run function every n seconds with
    best attempt to account for drift'''
    def tick():
        start = time.time()
        count = 0

        while True:
            count += 1
            # Use max to protect sleep from negative numbers
            # i.e. when func takes longer than time period (sec)
            yield max(start + count * sec - time.time(), 0)

    t = tick()

    while True:
        time.sleep(next(t))
        func()


if __name__ == '__main__':
    run_every(FEED_INTERVAL_SEC, get_gtfs_rt_data)
