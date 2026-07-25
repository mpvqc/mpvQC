# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import time

_PROCESS_STARTED_AT = time.perf_counter()


def main() -> None:
    import sys

    if sys.platform == "win32":
        _add_directory_to_path()

    _register_resources()

    from mpvqc.startup import perform_startup

    perform_startup(process_started_at=_PROCESS_STARTED_AT)


def _register_resources() -> None:
    from pathlib import Path

    from PySide6.QtCore import QResource

    resources = Path(__file__).resolve().parent / "project.rcc"
    if not QResource.registerResource(str(resources)):
        msg = f"Can not register resource file '{resources}'"
        raise FileNotFoundError(msg)


def _add_directory_to_path() -> None:
    import os
    import sys

    os.environ["PATH"] = os.path.dirname(sys.argv[0]) + os.pathsep + os.environ["PATH"]  # noqa: PTH120
    os.environ["PATH"] = os.path.dirname(__file__) + os.pathsep + os.environ["PATH"]  # noqa: PTH120


if __name__ == "__main__":
    main()
