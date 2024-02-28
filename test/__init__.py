# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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

def add_repository_root_directory_to_path():
    import os
    from pathlib import Path

    os.environ["PATH"] = str(Path(__file__).parent.parent.absolute()) + os.pathsep + os.environ["PATH"]


add_repository_root_directory_to_path()

try:
    import test.generated_resources
except ImportError:
    import sys

    print('Can not find resource module \'test.generated_resources\'', file=sys.stderr)
    print('To execute individual tests, please run \'just test-python\' once before', file=sys.stderr)
    sys.exit(1)
