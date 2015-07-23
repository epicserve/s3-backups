#!/usr/bin/env python

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError
from datetime import datetime
from s3_backups.utils import ColoredFormatter, timeit
from dateutil import tz

import importlib
import tarfile
import subprocess
import tempfile
import argparse
import logging
import sys
import re
import os

log = logging.getLogger('s3_backups')


@timeit("The backup took %(time)s to run")
def backup():
    """Backup Postgres to S3 using pg_dump"""

    key_name = S3_KEY_NAME
    if not key_name.endswith("/") and key_name != "":
        key_name = "%s/" % key_name

    # add the file name date suffix
    now = datetime.now()
    FILENAME_SUFFIX = "_%(year)d%(month)02d%(day)02d_%(hour)02d%(minute)02d%(second)02d" % {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second
    }
    FILENAME = ARCHIVE_NAME + FILENAME_SUFFIX + ".tar.gz"

    log.info("Preparing " + FILENAME + " from the database dump ...")

    # create postgres databases dump
    with tempfile.NamedTemporaryFile() as t1:
        proc1 = subprocess.Popen(POSTGRES_DUMP_PATH, shell=True, universal_newlines=True, stdout=t1)
        proc1.wait()
        t1.flush()

        # create tar.gz for the above two files
        t2 = tempfile.NamedTemporaryFile()
        tar = tarfile.open(t2.name, "w|gz")
        tar.add(t1.name, ARCHIVE_NAME + ".sql")
        tar.close()

        log.info("Uploading the " + FILENAME + " file to Amazon S3 ...")

        # get bucket
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

        try:
            bucket = conn.get_bucket(S3_BUCKET_NAME)
        except S3ResponseError:
            sys.stderr.write("There is no bucket with the name \"" + S3_BUCKET_NAME + "\" in your Amazon S3 account\n")
            sys.stderr.write("Error: Please enter an appropriate bucket name and re-run the script\n")
            t2.close()
            return

        # upload file to Amazon S3
        k = Key(bucket)
        k.key = key_name + FILENAME
        k.set_contents_from_filename(t2.name)
        t2.close()

        log.info("Sucessfully uploaded the archive to Amazon S3")


class archive(object):
    """
    Archives all backups on S3 using the following schedule:

    - Keep all backups for 7 days
    - Keep midnight backups for every other day for 30 days
    - Keep 1st day of the month forever
    """

    def __init__(self, schedule_module='schedules.default'):

        schedule = importlib.import_module(schedule_module)
        conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
        bucket = conn.get_bucket(S3_BUCKET_NAME)

        key_name = S3_KEY_NAME
        if not key_name.endswith("/") and key_name != "":
            key_name = "%s/" % key_name

        for key in bucket.list(key_name):
            if not key.name.endswith("/"):

                key = self.add_datetimes_to_key(key)

                # create a new key that puts the archive in a year/month sub
                # directory if it's not in a year/month sub directory already
                name_parts = key.name.split('/')
                month = name_parts[-2]
                year = name_parts[-3]
                new_key_name = key.name
                if not re.match(r'[\d]{4}', year) and not re.match(r'[\d]{2}', month):
                    name_parts.insert(len(name_parts) - 1, "%d" % key.local_last_modified.year)
                    name_parts.insert(len(name_parts) - 1, "%02d" % key.local_last_modified.month)
                    new_key_name = "/".join(name_parts)

                # either keep the file or delete it
                keep_file = schedule.keep_file(key)
                if keep_file and key.name != new_key_name:
                    key.copy(S3_BUCKET_NAME, new_key_name, metadata=key.metadata, preserve_acl=True)
                    bucket.delete_key(key.name)
                elif not keep_file:
                    bucket.delete_key(key.name)

    @classmethod
    def add_datetimes_to_key(self, key):
        """
        Convert the last_modified GMT datetime string to a datetime object and
        create utc and local datetime objects.
        """

        utc = tz.tzutc()
        gmt = tz.gettz('GMT')
        local_tz = tz.tzlocal()

        key.last_modified = datetime.strptime(key.last_modified, "%Y-%m-%dT%H:%M:%S.%fZ")
        key.last_modified = key.last_modified.replace(tzinfo=gmt)
        key.utc_last_modified = key.last_modified.astimezone(utc)
        key.local_last_modified = key.last_modified.astimezone(local_tz)

        return key


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Backs up Postgres to S3 using pg_dump or archives backups.')

    # Finds the environment variables for AWS credentials prior to the argparse argument definition
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

    # required arguments
    parser.add_argument('--S3_BUCKET_NAME', required=True, help='S3 bucket name')
    parser.add_argument('--S3_KEY_NAME', required=True, help='S3 key name, the directory path where you want to put archive (i.e. backups/postgres/server_name)')

    # required arguments if not defined in environment variables
    parser.add_argument('--AWS_ACCESS_KEY_ID', required=AWS_ACCESS_KEY_ID is None, help='S3 access key (required if not defined in AWS_ACCESS_KEY_ID environment variable)', default=AWS_ACCESS_KEY_ID)
    parser.add_argument('--AWS_SECRET_ACCESS_KEY', required=AWS_SECRET_ACCESS_KEY is None, help='S3 secret access key (required if not defined in AWS_SECRET_ACCESS_KEY environment variable)', default=AWS_SECRET_ACCESS_KEY)

    # optional arguments
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--POSTGRES_DUMP_PATH', default='/usr/bin/pg_dumpall', help="Path to pg_dumpall (default: /usr/bin/pg_dumpall)")
    parser.add_argument('--ARCHIVE_NAME', default='all_databases', help='The base name for the archive')
    parser.add_argument('--schedule_module', default='s3_backups.schedules.default', help='Use a different archive schedule module (default: schedules.default)')
    parser.add_argument('--backup', action='store_true', help='Backup up Postgres to S3')
    parser.add_argument('--archive', action='store_true', help='Archive backups on S3')
    args = parser.parse_args()

    AWS_ACCESS_KEY_ID = args.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = args.AWS_SECRET_ACCESS_KEY
    S3_BUCKET_NAME = args.S3_BUCKET_NAME
    S3_KEY_NAME = args.S3_KEY_NAME
    POSTGRES_DUMP_PATH = args.POSTGRES_DUMP_PATH
    ARCHIVE_NAME = args.ARCHIVE_NAME

    if args.verbose:
        log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = formatter = ColoredFormatter("$COLOR%(levelname)s: %(message)s$RESET")
        ch.setFormatter(formatter)
        log.addHandler(ch)

    if args.backup:
        backup()

    if args.archive:
        archive(args.schedule_module)
