import unittest
from datetime import datetime

from src.utils import date_utils


class TestDateUtils(unittest.TestCase):
    def test_iso_to_datetime(self):
        # given
        str_date = "2025-11-01 10:30:00"

        # when
        converted_date = date_utils.iso_to_datetime(str_date)

        # then
        self.assertEqual(datetime(2025, 11, 1, 10, 30), converted_date)

    def test_iso_to_datetime_invalid(self):
        # given
        str_date = "2025-11-011"

        # when
        converted_date = date_utils.iso_to_datetime(str_date)

        # then
        self.assertIsNone(converted_date)

    def test_iso_to_datetime_none(self):
        # given
        str_date = None

        # when
        converted_date = date_utils.iso_to_datetime(str_date)

        # then
        self.assertIsNone(converted_date)

    def test_datetime_to_iso(self):
        # given
        input_date = datetime(2025, 11, 1, 10, 30)

        # when
        str_date = date_utils.datetime_to_iso(input_date)

        # then
        self.assertEqual("2025-11-01T10:30:00", str_date)

    def test_datetime_to_iso_none(self):
        # given
        input_date = None

        # when
        str_date = date_utils.datetime_to_iso(input_date)

        # then
        self.assertIsNone(str_date)