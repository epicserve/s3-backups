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
    name='s3_backups',
    version=s3_backups.__version__,
    description='Backup stuff to S3',
    author="Brent O'Connor",
    author_email='epicserve@gmail.com',
    packages=[
        's3_backups',
    ],
    package_data={},
    package_dir={'s3_backups': 's3_backups'},
    include_package_data=True,
    install_requires=['boto==2.9.4'],
    license=open('LICENSE').read(),
    zip_safe=False,
    scripts=['s3_backups/postgres_to_s3.py'],
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ),
)
