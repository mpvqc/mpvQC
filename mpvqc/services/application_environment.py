# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from functools import cached_property
from pathlib import Path


class ApplicationEnvironmentService:
    @cached_property
    def is_portable(self) -> bool:
        return self.executing_directory.joinpath("portable").is_file()

    @cached_property
    def executing_directory(self) -> Path:
        return Path(sys.argv[0]).parent
