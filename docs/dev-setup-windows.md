# Development Setup - Windows

## Tools

1. Install  [python v3.8+](https://www.python.org/downloads/)
1. Install  [git-bash](https://git-scm.com/downloads)
1. Install [just](https://github.com/casey/just)

**just is supposed to be used from git-bash**

## Checkout

1. Clone this repository
1. Open git-bash in the directory
1. Set up virtual environment:
    1. `python -m venv venv`
    1. `source venv/Scripts/activate`
1. Install requirements `python -m pip install -r requirements.txt`
1. Download [libmpv](https://sourceforge.net/projects/mpv-player-windows/files/libmpv/), extract it and move the
   libmpv-*.dll into the root of the repository
