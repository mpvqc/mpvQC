# mpvQC

**mpvQC** is a **libmpv** based application for the quick and easy creation of quality control reports of video files, initially intended to be a less broken alternative to [kSub](http://dakoworks.ath.cx/projects/ksub).

- [Dependencies](#dependencies)
- [Installation](#installation)
  - [Windows](#windows)
  - [Linux](#linux)
     - [Arch/Manjaro](#archmanjaro)
     - [Debian/Ubuntu](#debianubuntu)
- [Keybindings](#keybindings)
  - [Default Bindings](#default-bindings)
- [Special Thanks](#special-thanks)

## Dependencies

- Python 3.6 or later
- PyQt5
- [python-mpv](https://github.com/jaseg/python-mpv) (AGPLv3) (already included in this repository)
- [libmpv](https://github.com/mpv-player/mpv) (0.28.0 or later)

## Installation

### Windows

For portable Windows binaries please look [here](https://mpvqc.rekt.cc/download/).

### Linux

#### Arch/Manjaro

- Install dependencies: ```sudo pacman -S python-pyqt5 mpv```
- Download [master](https://github.com/Frechdachs/mpvQC/archive/master.zip) and extract its contents
- Mark `start.py` as executable and run it.

#### Debian/Ubuntu

Unfortunately, the _libmpv_ package on Debian and Ubuntu is way too old to be used with this program.

- Remove previously installed mpv and/or libmpv packages.
- Build and install mpv/libmpv:
```
sudo apt-get install git devscripts equivs
git clone https://github.com/mpv-player/mpv-build.git
cd mpv-build
mk-build-deps -s sudo -i
echo --enable-libmpv-shared > mpv_options
./rebuild -j4
sudo ./install
```
- Install dependencies: ```sudo apt-get install python3-pyqt5 python3-requests```
- Download [master](https://github.com/Frechdachs/mpvQC/archive/master.zip) and extract its contents
- Mark `start.py` as executable and run it.

## Keybindings

To change the keybindings, you have to go to `Options --> Edit input.conf...`.<br>
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

- [trin94](https://github.com/trin94) for refactoring the project
- [maddo](https://github.com/maddovr) for the Italian translation
