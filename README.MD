# mpvQC

<img alt="Logo" src="data/icon.svg" width="128" height="128"/>

A libmpv-based application for quick and easy creation of video file quality control reports.  
https://mpvqc.github.io

# Development Setup

- **Install the following tools:**
    - [uv](https://github.com/astral-sh/uv)
    - [just](https://github.com/casey/just)
    - **On Windows, also install:**
        - [Python 3.12 or later](https://www.python.org/downloads/)
        - [Git Bash](https://git-scm.com/downloads)
        - **Make sure to use just from Git Bash**

- **Clone the repository**

- **Open a terminal** where you cloned the repository

- **Ensure libmpv is in your path:**
    - **Linux**: Install libmpv via your package manager
    - **Windows**: Download [libmpv](https://sourceforge.net/projects/mpv-player-windows/files/libmpv/), extract it and
      place the `libmpv-*.dll` in the repository’s root folder

- **Initialize the environment:**
  ```shell
  just init
  ```

Run `just build-develop` every time you change files in the `data`, `i18n`, or `qml` directories.  
This command compiles everything into a Python file and places it in the `mpvqc` folder, 
so the application picks it up on startup.

**Tipp:** Configure your IDE to run the `build-develop` recipe before launching the app.

# Internationalization

If you want to help translating this application into other languages, checkout
the [guide](docs/internationalization.md).
Please feel free to open a new issue in case you need help.
