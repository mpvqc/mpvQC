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

    if "--version" in sys.argv[1:]:
        _print_version()
        sys.exit(0)

    from mpvqc.startup import perform_startup

    perform_startup(process_started_at=_PROCESS_STARTED_AT)


def _add_directory_to_path() -> None:
    import os
    import sys
    from pathlib import Path

    os.environ["PATH"] = str(Path(sys.argv[0]).parent) + os.pathsep + os.environ["PATH"]
    os.environ["PATH"] = str(Path(__file__).parent) + os.pathsep + os.environ["PATH"]


def _print_version() -> None:
    from mpvqc.build import ChannelRelease, Unofficial, get_build_info

    app = get_build_info().application
    match app.origin:
        case ChannelRelease(channel):
            origin_line = f"build-origin: official ({channel})"
        case Unofficial():
            origin_line = "build-origin: unofficial"

    print(f"{app.name} {app.version} ({app.commit})")
    print(origin_line)


def _register_resources() -> None:
    from pathlib import Path

    from PySide6.QtCore import QResource

    resources = Path(__file__).resolve().parent / "project.rcc"
    if not QResource.registerResource(str(resources)):
        msg = f"Can not register resource file '{resources}'"
        raise FileNotFoundError(msg)


if __name__ == "__main__":
    main()
