# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


def main():
    import platform

    if platform.system() == "Windows":
        _add_directory_to_path()

    import rc_project  # noqa: F401
    from mpvqc.startup import perform_startup

    perform_startup()


def _add_directory_to_path():
    import os
    import sys

    os.environ["PATH"] = os.path.dirname(sys.argv[0]) + os.pathsep + os.environ["PATH"]  # noqa: PTH120
    os.environ["PATH"] = os.path.dirname(__file__) + os.pathsep + os.environ["PATH"]  # noqa: PTH120


if __name__ == "__main__":
    main()
