#!/usr/bin/env python

import os
import sys
import s3_backups

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='s3-backups',
    version=s3_backups.__version__,
    description='Backup stuff to S3',
    author="Brent O'Connor",
    author_email='epicserve@gmail.com',
    url='https://github.com/epicserve/s3-backups',
    packages=[
        's3_backups',
        's3_backups.schedules',
    ],
    package_data={'': ['LICENSE']},
    package_dir={'s3-backups': 's3-backups'},
    include_package_data=True,
    install_requires=['boto==2.9.4', 'python-dateutil==2.1'],
    license=open('LICENSE').read(),
    zip_safe=False,
    scripts=['s3_backups/postgres_to_s3.py', 's3_backups/redis_to_s3.py', 's3_backups/mysql_to_s3.py'],
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
