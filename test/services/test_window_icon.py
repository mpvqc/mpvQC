#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest
from unittest.mock import patch, MagicMock

import inject

from mpvqc.services import WindowIconService, ResourceService


class TestWindowIconService(unittest.TestCase):
    MODULE = 'mpvqc.services.window_icon'

    def setUp(self):
        inject.clear_and_configure(lambda binder: binder
                                   .bind(ResourceService, MagicMock()))

    def tearDown(self):
        inject.clear()

    @patch(f'{MODULE}.QIcon')
    def test_setWindowIcon_called(self, *_):
        q_gui_app = MagicMock()

        service = WindowIconService()
        service.restore(q_gui_app)

        q_gui_app.setWindowIcon.assert_called()
