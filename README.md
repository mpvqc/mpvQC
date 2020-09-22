# mpvQC

**mpvQC** is a **libmpv** based application for the quick and easy creation of quality control reports of video files, 
initially intended to be a less broken alternative to *kSub*.

## Dependencies

- Python 3.6 or later
- PyQt5
- [python-mpv](https://github.com/jaseg/python-mpv) (AGPLv3) (already included in this repository)
- [libmpv](https://github.com/mpv-player/mpv) (0.28.0 or later)
- [distutils_ui](https://github.com/frispete/distutils_ui) for developing

## Installation

### Windows

For portable Windows binaries please look [here](https://mpvqc.rekt.cc/download/).

### Linux

#### Arch

- Install dependencies: ```sudo pacman -S python-pyqt5 python-requests mpv```
- Download [master](https://github.com/Frechdachs/mpvQC/archive/master.zip) and extract its contents
- Mark `start.py` as executable and run it.

#### Ubuntu 18.04

- Install dependencies: `sudo apt-get install python3-pyqt5 python3-requests`
- Build mpv from Source:
    ```shell script
    sudo apt-get install git devscripts equivs
    git clone https://github.com/mpv-player/mpv-build.git
    cd mpv-build
    mk-build-deps -s sudo -i
    echo --enable-libmpv-shared > mpv_options
    ./rebuild -j4
    sudo ./install
    ```
- Download [master](https://github.com/Frechdachs/mpvQC/archive/master.zip) and extract its contents
- Mark `start.py` as executable and run it.

#### Ubuntu 20.04

- Install dependencies: `sudo apt-get install python3-pyqt5 python3-requests libmpv1`
- Download [master](https://github.com/Frechdachs/mpvQC/archive/master.zip) and extract its contents
- Mark `start.py` as executable and run it.

## Keybindings

To change the keybindings, you have to go to `Options --> Settings --> MPV Settings -> Input.conf`.<br>
You can use most of the input commands listed [here](https://mpv.io/manual/master/#list-of-input-commands).

### Default Bindings

Keybindings marked with \* cannot be changed.

- `Right click`\*, `e`\*: Open context menu
- `Left double-click`\*, `f`\*: Enter/leave fullscreen mode
- `Left click`, `SPACE`: Play/pause
- `LEFT`, `RIGHT`: Seek backward/forward by exactly 2 seconds
- `Shift+LEFT`, `Shift+RIGHT`: Seek backward/forward by 5 seconds to a keyframe
- `9`, `0`, `Mouse Wheel`: Decrease/increase volume
- `m`: Mute/unmute
- `.`, `,`: Go forward/backward by one frame
- `j`: Cycle through subtitle tracks
- `#`: Cycle through audio tracks
- `Backward button`, `Forward button`: Seek to previous/next chapter
- `s`: Make a screenshot of the unscaled video
- `S`: Make a screenshot of the scaled video
- `b`: Toggle between rendering the subtitles at window resolution and video resolution
- `i`: Display statistics of the currently played video

## Special Thanks

- [maddo](https://github.com/maddovr) for the Italian translation
