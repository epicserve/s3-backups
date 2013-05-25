from datetime import datetime, timedelta
from dateutil import tz

import logging

log = logging.getLogger('s3_backups')

"""
The default schedule does the following ...

- Keeps all archives for 7 days
- Keeps midnight backups for every other day for 30 days
- Keeps the first day of the month forever
"""

ONE_WEEK = timedelta(days=7)
ONE_MONTH = timedelta(days=30)
utc = tz.tzutc()


class OddEven:

    current = 'even'

    def toggle(self):
        if self.current == 'even':
            self.current = 'odd'
        else:
            self.current = 'even'
        return self.current

oe = OddEven()


def keep_file(key):
    utcnow = datetime.utcnow()
    utcnow = utcnow.replace(tzinfo=utc)
    timediff = utcnow - key.utc_last_modified
    odd_even = oe.toggle()

    if timediff <= ONE_WEEK:
        log.info("%s - Keeping key \"%s\" because it's less than a week old." % (timediff, key.name))
        return True
    elif timediff > ONE_WEEK and timediff < ONE_MONTH:
        if key.local_last_modified.hour != 0:
            log.info("%s - Removing key \"%s\" because it's not a midnight backup and it's older than one week but less than a month" % (timediff, key.name))
            return False
        elif odd_even == 'even':
            log.info("%s - Removing key \"%s\" because it's older than one week but less than a month and not an even day." % (timediff, key.name))
            return False
        else:
            log.info("%s - Keeping key \"%s\" because it's older than one week but less than a month and it's an even day." % (timediff, key.name))
            return True
    elif timediff > ONE_MONTH:
        if key.local_last_modified.day == 1:
            log.info("%s - Keeping key \"%s\" because it's older than a month and also the first day of the month." % (timediff, key.name))
            return True
        else:
            log.info("%s - Removing key \"%s\" because it's older than a month and not the first day of the month." % (timediff, key.name))
            return False
