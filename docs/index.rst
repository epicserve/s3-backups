S3 Backups
==========

.. image:: https://pypip.in/v/s3-backups/badge.png
        :target: https://pypi.python.org/pypi/s3-backups

.. image:: https://travis-ci.org/epicserve/s3-backups.png?branch=master
    :alt: Build Status
    :target: http://travis-ci.org/epicserve/epicserve

`S3 Backups <https://github.com/epicserve/s3-backups>`_ provides easy scripts that system administrators can use to backup
data from programs likes PostgreSQL, MySQL, Redis, etc.

Installation
------------

To install s3-backups::

    $ sudo pip install s3-backups

Usage
-----

Setting Up S3 Backups to Run Automatically Using Cron
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


PostgreSQL
''''''''''

Add the following to the file ``/etc/cron.d/postgres_to_s3`` and then change the command arguments so the command is using your correct AWS credentials, backup bucket and the correct base S3 Key/base folder.

::

    0 */1 * * * postgres /usr/local/bin/postgres_to_s3.py --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' --S3_BUCKET_NAME='my-backup-bucket' --S3_KEY_NAME='postgres/my-awesome-server' --backup --archive

Redis
'''''

Add the following to the file ``/etc/cron.d/redis_to_s3`` and then change the command arguments so the command is using your correct AWS credentials, backup bucket and the correct base S3 Key/base folder.

::

    0 */1 * * * root redis_to_s3.py --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' --S3_BUCKET_NAME='my-backup-bucket' --S3_KEY_NAME='redis/my-awesome-server' --backup --archive


MySQL
'''''

Add the following to the file ``/etc/cron.d/mysql_to_s3`` and then change the command arguments so the command is using your correct AWS credentials, backup bucket and the correct base S3 Key/base folder.

::

    0 */1 * * * root mysql_to_s3.py --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' --S3_BUCKET_NAME='my-backup-bucket' --S3_KEY_NAME='mysql/my-awesome-server' --backup --archive



Manually Running Backups and Archiving
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When running the archive command, S3 Backups moves backups into a
``year/month`` sub folder (technically a S3 key) for archives it's scheduled
to keep and removes all other archives. S3 Backups, will use the default
schedule unless you you tell it to use a different schedule with the
``--schedule_module`` argument.

The default archive schedule will ...

- keep all archives for 7 days
- keep midnight backups for every other day for 30 days
- keep the first day of the month forever
- remove all other files that aren't scheduled to be kept

To backup PostgreSQL, run the following::

    $ postgres_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='postgres/my-awesome-server' \
    --backup

To archive PostgreSQL backups, run the following::

    $ postgres_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='postgres/my-awesome-server' \
    --archive

To backup Redis, run the following::

    $ redis_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='redis/my-awesome-server' --backup

To archive Redis, run the following::

    $ redis_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='redis/my-awesome-server' --archive

To backup MySQL, run the following::

    $ mysql_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='redis/my-awesome-server' --backup

To archive MySQL, run the following::

    $ mysql_to_s3.py \
    --AWS_ACCESS_KEY_ID='xxxxxxxxxxxxxxxxxxxx' \
    --AWS_SECRET_ACCESS_KEY='xxxxxxxxxxxxxxxxxxxx' \
    --S3_BUCKET_NAME='my-backup-bucket' \
    --S3_KEY_NAME='redis/my-awesome-server' --archive

Contribute
----------

1. Look for an open `issue <https://github.com/epicserve/s3-backups/issues>`_ or create new issue to get a dialog going about the new feature or bug that you've discovered.

2. Fork the `repository <https://github.com/epicserve/s3-backups>`_ on Github to start making your changes to the master branch (or branch off of it).

3. Write a test which shows that the bug was fixed or that the feature works as expected.

4. Make a pull request.
