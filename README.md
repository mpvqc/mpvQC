<div align="center">
  <h1>mpvQC</h1>
  <img alt="Logo" src="https://avatars3.githubusercontent.com/u/47739558?s=200&v=4" width="128" height="128"/>
  <br/>
  <br/>
  <img alt="Tests" src="https://github.com/mpvqc/mpvQC/workflows/Tests/badge.svg"/>
  <br>
  <b>libmpv based application for the quick and easy creation of quality control reports of video files</b>
</div>

---

## Dependencies

- Python 3.6 or later
- PyQt5
- [python-mpv](https://github.com/jaseg/python-mpv) (AGPLv3) (already included in this repository)
- [libmpv](https://github.com/mpv-player/mpv) (0.29.0 or later)

## Installation

### Windows

For portable Windows binaries please look [here](https://mpvqc.github.io/).

### Linux

For Linux there is a little work required to get the application up and running which also involves using the terminal.

1. Make sure you have `PyQt5`, and `libmpv` packages installed
1. First download the *release-build-artifact* from the release page
1. Unzip the *release-build-artifact* file
1. Navigate to the unzipped directory and run the following command.
   This will tell mpvQC to store settings and backups in this directory.
   ```shell
   touch portable
   ```
1. Start the application
   ```shell
   python main.py 
   ```

## Keybindings

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

To change the keybindings, you have to go to `Options --> Edit input.conf...`  
You can use most of the input commands listed [here](https://mpv.io/manual/master/#list-of-input-commands).
