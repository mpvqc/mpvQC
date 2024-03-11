# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from unittest.mock import patch, MagicMock
from urllib.error import HTTPError, URLError

from mpvqc.services import VersionCheckerService


class VersionCheckerServiceTest(unittest.TestCase):

    @staticmethod
    def _mock_response(mock, *, status=200, body='', error=None):
        if error:
            mock.side_effect = error
            return

        cm = MagicMock()
        cm.getcode.return_value = status
        cm.read.return_value = body.encode()
        cm.__enter__.return_value = cm
        mock.return_value = cm

    @staticmethod
    def _mock_current_version(mock, *, version: str):
        mock.return_value.applicationVersion.return_value = version

    def _verify(self, expected_title: str):
        service = VersionCheckerService()
        actual_title, _ = service.check_for_new_version()
        self.assertEqual(expected_title, actual_title)

    @property
    def _http_error(self):
        return HTTPError('http://example.com', 500, 'Internal Error', {}, None)

    @property
    def _url_error(self):
        return URLError(reason="it's a mock, brooooo")

    @patch('mpvqc.services.version_checker.urllib.request.urlopen')
    @patch('mpvqc.services.version_checker.QCoreApplication.instance', return_value=MagicMock())
    def test_latest(self, qcore_mock, request_mock):
        self._mock_response(request_mock, body='{ "latest": "0.1.0" }')
        self._mock_current_version(qcore_mock, version='0.1.0')

        expected_title = "👌"
        self._verify(expected_title)

    @patch('mpvqc.services.version_checker.urllib.request.urlopen')
    @patch('mpvqc.services.version_checker.QCoreApplication.instance', return_value=MagicMock())
    def test_update_available(self, qcore_mock, request_mock):
        self._mock_response(request_mock, body='{ "latest": "0.1.0" }')
        self._mock_current_version(qcore_mock, version='0.1.1')

        expected_title = "New Version Available"
        self._verify(expected_title)

    @patch('mpvqc.services.version_checker.urllib.request.urlopen')
    @patch('mpvqc.services.version_checker.QCoreApplication.instance', return_value=MagicMock())
    def test_server_error(self, qcore_mock, request_mock):
        self._mock_response(request_mock, error=self._http_error)
        self._mock_current_version(qcore_mock, version='0.1.0')

        expected_title = "Server Error"
        self._verify(expected_title)

    @patch('mpvqc.services.version_checker.urllib.request.urlopen')
    @patch('mpvqc.services.version_checker.QCoreApplication.instance', return_value=MagicMock())
    def test_url_error(self, qcore_mock, request_mock):
        self._mock_response(request_mock, error=self._url_error)
        self._mock_current_version(qcore_mock, version='0.1.0')

        expected_title = "Server Not Reachable"
        self._verify(expected_title)
