S3 Backups
==========

Overview
--------

S3 Backups goal is to provide easy scripts that system administrators can use
to backup data from programs likes PostgreSQL, MySQL, Redis, etc. Currently
the only script it provides is a script for backing up PostgreSQL.

.. _installation:

Installation
------------

To install s3-backups::

    $ sudo pip install s3-backups

Usage
-----

Setting Up S3 Backups to Run Automatically Using Cron
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 1. Install S3 Backups following the `installation`_ instructions.

Step 2. Add the following to the file ``/etc/cron.d/postgres_to_s3`` and then change the command arguments so the command is using your correct AWS credentials, backup bucket and the correct base S3 Key/base folder.

::

    0 */1 * * * postgres /usr/local/bin/postgres_to_s3.py --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' --S3_BUCKET_NAME='my-backup-bucket' --S3_KEY_NAME='postgres/my-awesome-server' --backup --archive

Manually Running Backups and Archiving
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To backup PostgreSQL, run the following::

    $ postgres_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='postgres/my-awesome-server' \
    --backup

You can remove old PostgreSQL backups automatically and move backups into a
``year/month`` sub folder (technically a S3 key). The archive command will use
the default schedule which will does the following.

- Keeps all archives for 7 days
- Keeps midnight backups for every other day for 30 days
- Keeps the first day of the month forever

To archive PostgreSQL backups, run the following::::

    $ postgres_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='postgres/my-awesome-server' \
    --archive

Contribute
----------

If you'd like to contribute, create an issue to get a dialog going about the
feature you want to add. After a plan is place then fork the repository and
then create your fix or feature on a new branch. When your finished, make a
pull request to get your changes pulled in.
