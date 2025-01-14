#!/home/ubuntu/miniconda3/envs/historic-mta/bin/python
"""Script to archive (.tar.bz2) and upload
all files generated before current hour to S3 bucket"""
import boto3
import datetime
import os
import sys
import tarfile

EXTENSION = '.tar.bz2'
FILENAME_SEP = '-'
PREFIX = 'feed'

ARCHIVE_DIR = 'archives'
ROOT_DIR = 'data'

STORAGE_SERVICE = 's3'
BUCKET_NAME = 'historic.mta'


def get_date_hour():
    """Get date and current hour. Use to determine
    which folders are still being downloaded to"""
    d = datetime.datetime.now(datetime.UTC)
    year = str(d.year)
    month = str(d.month).zfill(2)
    day = str(d.day).zfill(2)
    hour = str(d.hour).zfill(2)
    return year, month, day, hour


def upload_dirs():
    """Tar and upload all files in directory of form:
    /year/month/date/hour/"""
    # Exclude all directories that represent current hour
    date_hour = get_date_hour()
    date_hour_path = '/'.join(list(date_hour))

    paths_to_process = []
    for path, _, files in os.walk(ROOT_DIR):
        # Data folder does not represent current hour
        if files and (date_hour_path not in path) and (PREFIX in path):
            paths_to_process.append(path)

    archives = compress_and_archive(paths_to_process)

    # Remove leading root directory and trailing hour directory
    upload_paths = [path.replace(ROOT_DIR + os.path.sep, '') for path in paths_to_process]
    upload_paths = [path.rsplit(os.path.sep, 1)[0] for path in upload_paths]

    upload_s3(archives, upload_paths)
    cleanup(archives, paths_to_process)


def compress_and_archive(paths):
    if not os.path.isdir(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    archives = []
    for path in paths:
        # Remove root dir from path to generate filename
        i = path.index(PREFIX)
        out_name = path[i:].replace(os.path.sep, FILENAME_SEP) + EXTENSION
        out_name = os.path.join(ARCHIVE_DIR, out_name)

        # Compress and create archive
        with tarfile.open(out_name, 'w:bz2') as tar:
            tar.add(path, arcname='.')

        archives.append(out_name)

    return archives


def upload_s3(archives, upload_paths):
    s3 = boto3.resource(STORAGE_SERVICE)
    bucket = s3.Bucket(BUCKET_NAME)

    # Generate archive full S3 paths
    # /{feed}/{year}/{month}/{day}/<feed-YYYY-MM-DD-HH.tar.bz2>
    archive_names = [a.replace(ARCHIVE_DIR + os.path.sep, '') for a in archives]
    upload_paths = ['/'.join([u, a]) for u, a in zip(upload_paths, archive_names)]

    # Upload to S3
    for archive, path in zip(archives, upload_paths):
        try:
            bucket.upload_file(archive, path)
        except:
            # Upload failed - wait till next hour to try again
            sys.exit(1)


def cleanup(archives, paths_to_process):
    # Delete archive files
    for archive in archives:
        os.remove(archive)

    # Delete all files in processed directories
    for path in paths_to_process:
        delete = [os.path.join(path, f) for f in os.listdir(path)]
        for d in delete:
            os.remove(d)


if __name__ == '__main__':
    upload_dirs()
