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

> **Note:** Unfortunately mpv/libmpv still catches mouse events even when embedded in another window on Linux. Because of that some things won't work: Double clicking to go fullscreen and right mouse click to open the context menu. You have to use the keyboard to go to fullscreen (f) and to open the context menu (e). If pressing a key doesn't work, then the mainwindow currently is not active, meaning you have to click on something inside the application that is not the video. (Clicking on the video again after that fortunately won't deactivate the application window again.) This will be fixed as soon (or if) the following feature request gets addressed: [#2750](https://github.com/mpv-player/mpv/issues/2750).

### OS X

On OS X you can't use _mpv_ instead of _libmpv_, because OS X does not support window embedding of foreign processes. Other than that the installation process should be the same as on Linux.
