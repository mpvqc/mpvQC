# Development Setup - Generic Linux

## Tools

* Make sure `python` is on version **3.12** or later
* Install `just` (https://github.com/casey/just)

## Setup

1. Clone this repository
1. Set up virtual environment:
    1. `python -m venv venv`
    1. `source venv/bin/activate` (*bash*) or `source venv/bin/activate.fish` (*fish*)
1. Install requirements `just install-dependencies`
1. Install libmpv (package names vary depending on your distro)
1. Create an empty file `portable` in the root of the repository.
   This will tell mpvQC to store all app data in a new folder called `appdata`
