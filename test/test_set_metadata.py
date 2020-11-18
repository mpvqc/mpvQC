import unittest

from mpvqc import get_metadata
# noinspection PyProtectedMember
from mpvqc._metadata import set_metadata


class TestMetadata(unittest.TestCase):

    def test_set_metadata(self):
        dir_program = ""
        app_version = "0.7.0"
        app_name = "mpvqc"
        set_metadata(dir_program, app_version, app_name)

        md = get_metadata()
        self.assertEqual(dir_program, md.dir_program)
        self.assertEqual(app_version, md.app_version)
        self.assertEqual(app_name, md.app_name)

