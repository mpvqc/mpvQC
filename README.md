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
- [distutils_ui](https://github.com/frispete/distutils_ui) for developing

## Installation

### Windows

For portable Windows binaries please look [here](https://mpvqc.github.io/).

### Linux

For Linux there is a little work required to get the application up and running.  
For Ubuntu 20.04 we have listed all steps [here](docs/dev-environment-setup.md).  
Other distributions behave similarly, but package names vary.

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
