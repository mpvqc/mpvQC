# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import platform

import pytest

linux_only = pytest.mark.skipif(platform.system() != "Linux", reason="Requires Linux")
