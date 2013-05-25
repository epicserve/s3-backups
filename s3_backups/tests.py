from datetime import datetime, timedelta
from dateutil import tz
from s3_backups.schedules import default
from s3_backups.postgres_to_s3 import archive
import unittest


class mockS3Key:

    def get_aws_datetime_string(self, dt):
        return "%s.000Z" % dt.strftime("%Y-%m-%dT%H:%M:%S")

    def __init__(self, utc_datetime):
        self.last_modified = self.get_aws_datetime_string(utc_datetime)
        self.name = "all_databases_%(year)s%(month)s%(day)s_%(hour)s%(minute)s%(second)s.tar.gz" % {
            'year': utc_datetime.year,
            'month': "%02d" % utc_datetime.month,
            'day': "%02d" % utc_datetime.day,
            'hour': "%02d" % utc_datetime.hour,
            'minute': "%02d" % utc_datetime.minute,
            'second': "%02d" % utc_datetime.second,
        }


class TestDefaultSchedule(unittest.TestCase):

    def setUp(self):
        self.utc = tz.tzutc()
        self.local_tz = tz.tzlocal()
        self.local_now = datetime.now()
        self.local_now = self.local_now.replace(tzinfo=self.local_tz)
        self.utcnow = datetime.utcnow()
        self.utcnow = self.utcnow.replace(tzinfo=self.utc)
        self.local_now_midnight = self.local_now.replace(hour=0, minute=0, second=0)
        self.utc_midnight = self.local_now_midnight.astimezone(self.utc)

    def get_key(self, dt):
        return archive.add_datetimes_to_key(mockS3Key(dt))

    def test_keep_all_archives_for_7_days(self):

        self.assertTrue(default.keep_file(self.get_key(self.utcnow - timedelta(days=6, hours=23, minutes=59, seconds=59))))
        self.assertTrue(default.keep_file(self.get_key(self.utcnow)))

    def test_gt_one_week_and_lt_one_month(self):

        default.oe.current = 'even'
        self.assertTrue(default.keep_file(self.get_key(self.utc_midnight - timedelta(days=9))))
        self.assertFalse(default.keep_file(self.get_key(self.utc_midnight - timedelta(days=10))))
        self.assertFalse(default.keep_file(self.get_key(self.utc_midnight - timedelta(days=10, hours=1))))

    def test_gt_one_month(self):

        # older than one month and not the first
        dt_1 = self.utc_midnight - timedelta(days=365)
        dt_1 = dt_1.replace(day=2)
        self.assertFalse(default.keep_file(self.get_key(dt_1)))

        # older than one month and the first
        dt_2 = dt_1.replace(day=1)
        self.assertTrue(default.keep_file(self.get_key(dt_2)))

if __name__ == '__main__':
    unittest.main()
