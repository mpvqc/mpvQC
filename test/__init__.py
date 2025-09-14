# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


def add_repository_root_to_path():
    import os
    from pathlib import Path

    os.environ["PATH"] = str(Path(__file__).parent.parent.absolute()) + os.pathsep + os.environ["PATH"]


add_repository_root_to_path()
