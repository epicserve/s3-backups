S3 Backups
==========

Overview
--------

S3 Backups goal is to provide easy scripts that system administrators can use
to backup data from programs likes PostgreSQL, MySQL, Redis, etc. Currently
the only script it provides is a script for backing up PostgreSQL.

Usage
-----

To backup PostgreSQL, run the following::

    $ postgres_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='postgres/my-awesome-server' \
    --backup

Installation
------------

To install s3-backups::

    $ https://bitbucket.org/epicserve/s3-backups/get/master.zip

Contribute
----------

If you'd like to contribute, create an issue to get a dialog going about the
feature you want to add. After a plan is place then fork the repository and
then create your fix or feature on a new branch. When your finished, make a
pull request to get your changes pulled in.
