# mpvQC

**mpvQC** is a **libmpv** or (at your choice) **mpv** based application for the quick and easy creation of quality control reports of video files, initially intended to be a less broken alternative to [kSub](http://dakoworks.ath.cx/projects/ksub).

## Dependencies

- [libmpv](https://github.com/mpv-player/mpv) or [mpv](https://mpv.io/installation/) (0.16.0 or later)
- Python 3.4 or later
- [python-mpv](https://github.com/jaseg/python-mpv) or [mpv-python-ipc](https://github.com/siikamiika/mpv-python-ipc)
- PyQt5
- [Requests](https://github.com/kennethreitz/requests)

## Installation

### Windows

For portable Windows binaries please look [here](https://mpvqc.rekt.cc/download/).

### Linux

It's possible to use **libmpv** via [python-mpv](https://github.com/jaseg/python-mpv) or **mpv** in a slave-mode-kinda way via [mpv-python-ipc](https://github.com/siikamiika/mpv-python-ipc).

- Make sure all the dependencies are properly installed and working (Also make sure that libmpv/mpv is up to date)
- Download [master](https://github.com/Frechdachs/mpvQC/archive/master.zip) or a [Release](https://github.com/Frechdachs/mpvQC/releases) (0.3.0 or later)
- If you want to use _mpv_ instead of _libmpv_ open `mpvQC.py` in a text editor and change the global variable `mpvslave` from `False` to `True` (It's located right below the imports)
- You can now start _mpvQC_ by executing `mpvQC.py`

### OS X

On OS X you can't use _mpv_ instead of _libmpv_, because OS X does not support window embedding of foreign processes. Other than that the installation process should be the same as on Linux.

## Keybindings

To change the keybindings, you have to go to `Options --> Edit input.conf...`.
You can use most of the input commands listed [here](https://mpv.io/manual/master/#list-of-input-commands).

### Default Bindings

Keybindings marked with (*) cannot be changed.

- `Right click`(*), `e`(*): Open context menu
- `Left double-click`(*), `f`(*): Enter/leave fullscreen mode
- `Left click`: Play/pause
- `SPACE`: Play/pause
- `LEFT`, `RIGHT`: Seek backward/forward by exactly 2 seconds
- `Shift+LEFT`, `Shift+Right`: Seek backward/forward by 5 seconds to a keyframe
- `9`, `0`: Decrease/increase volume
- `m`: Mute/unmute
- `.`, `,`: Go forward/backward by one frame
- `j`: Cycle through subtitle tracks
- `#`: Cycle through audio tracks
- `Backward button`, `Forward button`: Seek to previous/next chapter
- `s`: Make a screenshot of the unscaled video
- `S`: Make a screenshot of the scaled video
- `b`: Toggle between rendering the subtitles at window resolution and video resolution
- `i`: Display statistics of the currently played video
