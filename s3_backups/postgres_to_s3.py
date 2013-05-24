#!/usr/bin/env python

from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.exception import S3ResponseError
from datetime import datetime
from s3_backups.utils import ColoredFormatter

import tarfile
import subprocess
import tempfile
import os
import argparse
import logging
import sys

log = logging.getLogger(__file__)


def backup():
    """Backups Postgres to S3 using pg_dump"""

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

    log.info("Preparing " + ARCHIVE_NAME + ".tar.gz from the database dump ...")

    # create postgres databeses dump
    with tempfile.NamedTemporaryFile() as t1:
        proc1 = subprocess.Popen(POSTGRES_DUMP_PATH, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        t1.write(proc1.communicate()[0])

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

        log.info("Sucessfully uploaded the archive to Amazon S3")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Backs up Postgres to S3 using pg_dump or archives backups.')

    # required arguments
    parser.add_argument('--AWS_ACCESS_KEY_ID', required=True, help='S3 access key')
    parser.add_argument('--AWS_SECRET_ACCESS_KEY', required=True, help='S3 secret access key')
    parser.add_argument('--S3_BUCKET_NAME', required=True, help='S3 bucket name')
    parser.add_argument('--S3_KEY_NAME', required=True, help='S3 key name, the directory path where you want to put archive (i.e. backups/postgres/server_name)')

    # optional arguments
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--POSTGRES_DUMP_PATH', default='/usr/bin/pg_dumpall', help="Path to pg_dumpall (default: /usr/bin/pg_dumpall)")
    parser.add_argument('--ARCHIVE_NAME', default='all_databases', help='The base name for the archive')
    parser.add_argument('--backup', action='store_true', help='Backup up Postgres to S3')
    args = parser.parse_args()

    AWS_ACCESS_KEY_ID = args.AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY = args.AWS_SECRET_ACCESS_KEY
    S3_BUCKET_NAME = args.S3_BUCKET_NAME
    S3_KEY_NAME = args.S3_KEY_NAME
    POSTGRES_DUMP_PATH = args.POSTGRES_DUMP_PATH
    ARCHIVE_NAME = os.environ.get('ARCHIVE_NAME', 'all_databases')

    if args.verbose:
        log.setLevel(logging.INFO)
        ch = logging.StreamHandler()
        formatter = formatter = ColoredFormatter("$COLOR%(levelname)s: %(message)s$RESET")
        ch.setFormatter(formatter)
        log.addHandler(ch)

    if args.backup:
        backup()
