# mpvQC

<img alt="Logo" src="data/icon.svg" width="128" height="128"/>

A simple libmpv-based application for creating video file quality control reports.\
https://mpvqc.github.io

______________________________________________________________________

## Development Setup

1. **Install these tools**

   - [Python 3.13 or later](https://www.python.org/downloads/)
   - [uv](https://github.com/astral-sh/uv)
   - [just](https://github.com/casey/just)
   - **Windows users also need**
     - [Git Bash](https://git-scm.com/downloads)
     - Be sure to run `just` inside Git Bash

2. **Clone the repository**

3. **Open a terminal** where you cloned it

4. **Initialize the environment**:

   ```shell
   just init
   ```

5. **Add libmpv to your path**

   - **Linux**: Install `libmpv` through your package manager
   - **Windows**: Download [libmpv (mpv-dev-x86_64)](https://github.com/shinchiro/mpv-winbuild-cmake/releases), extract it, and place the `libmpv-*.dll` in the repository’s root folder

6. **Compile Resources:**

   ```shell
   just build-develop
   ```

7. **Start the application:**

   ```shell
   uv run main.py
   ```

Whenever you change files in the `data`, `i18n`, or `qml` directories, run:

```shell
just build-develop
```

This compiles them into a Python file in the mpvqc folder, so the app recognizes them on startup.

**Tip:** Configure your IDE to run the `build-develop` before launching the application.

## Internationalization

If you want to translate this application into more languages, see the [internationalization guide](docs/internationalization.md).
Feel free to open a new issue if you need further assistance.
