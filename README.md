## mpvQC

**mpvQC** is a **libmpv** or (at your choice) **mpv** based application for the quick and easy creation of quality control reports of video files, initially intended to be a less broken alternative to [kSub](http://dakoworks.ath.cx/projects/ksub).

## Dependencies

- [libmpv](https://github.com/mpv-player/mpv) or [mpv](https://mpv.io/installation/)
- Python 3.4
- [python-mpv](https://github.com/jaseg/python-mpv) or [mpv-python-ipc](https://github.com/siikamiika/mpv-python-ipc)
- PyQt5
- [Requests](https://github.com/kennethreitz/requests)
- [Pyperclip](https://github.com/asweigart/pyperclip)

## Installation

### Windows

For Windows binaries please look [here](https://mpvqc.rekt.cc/download/).

### Linux

It's possible to use **libmpv** via [python-mpv](https://github.com/jaseg/python-mpv) or **mpv** in a slave-mode-kinda way via [mpv-python-ipc](https://github.com/siikamiika/mpv-python-ipc).

> **Note:** I wasn't able to get _libmpv_ via _python-mpv_ working while testing on OpenSUSE, only _mpv_ via _mpv-python-ipc_, I don't know wether it's a problem with _python-mpv_ or the _libmpv_ package. But you could still try, I guess.

- Make sure all the dependencies are properly installed and working (Also make sure that libmpv/mpv is up to date)
- Download [master](https://github.com/Frechdachs/mpvQC/archive/master.zip)
- If you want to use _mpv_ instead of _libmpv_ open `mpvQC.py` and change the global variable `mpvslave` from `False` to `True` (It's located right below the imports)
- You can now start _mpvQC_ by executing `mpvQC.py`

### OS X

On OS X you can't use _mpv_ instead of _libmpv_, because OS X does not support window embedding of foreign processes. Other than that the installation process should be the same as on Linux.
