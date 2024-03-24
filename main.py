#!/usr/bin/env python

def main():
    import platform
    if platform.system() == 'Windows':
        _add_directory_to_path()

    from mpvqc.startup import perform_startup
    perform_startup()


def _add_directory_to_path():
    import os
    import sys
    os.environ["PATH"] = os.path.dirname(sys.argv[0]) + os.pathsep + os.environ["PATH"]


if __name__ == "__main__":
    main()
