# mpvQC
#
# Copyright (C) 2025 mpvQC developers
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

from collections.abc import Generator
from importlib.util import find_spec
from typing import Any

import pytest

from mpvqc.application import MpvqcApplication
from mpvqc.services import TypeMapperService


@pytest.fixture(scope="session", autouse=True)
def check_generated_resources():
    if find_spec("test.generated_resources") is None:
        message = (
            "Can not find resource module 'test.generated_resources'\n"
            "To execute individual tests, please run 'just test-python' once before"
        )
        raise FileNotFoundError(message)
    import test.generated_resources  # noqa: F401


@pytest.fixture(scope="session")
def type_mapper() -> TypeMapperService:
    return TypeMapperService()


@pytest.fixture(scope="session")
def qt_app() -> Generator[MpvqcApplication, Any]:
    app = MpvqcApplication([])
    yield app
    app.shutdown()
