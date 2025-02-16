# mpvQC

<img alt="Logo" src="data/icon.svg" width="128" height="128"/>

A libmpv-based application for quick and easy creation of video file quality control reports.  
https://mpvqc.github.io

# Development Setup

This project assumes that a virtual environment is used:

* [Guide for Linux](docs/dev-setup-linux.md)
* [Guide for Windows](docs/dev-setup-windows.md)

We use [uv](https://github.com/astral-sh/uv) and [just](https://github.com/casey/just) to build our application.

```shell
$ just
Available recipes:
    format                 # Format code
    init                   # Initialize repository

    [build]
    build                  # Build full project into build/release
    build-develop          # Build and compile resources into source directory
    clean                  # Remove ALL generated files

    [i18n]
    add-translation locale # Add new language
    update-translations    # Update *.ts files by traversing the source code

    [lint]
    lint-python            # Lint Python files
    lint-qml               # Lint QML files

    [test]
    test                   # Run Python and QML tests
    test-python            # Run Python tests
    test-qml               # Run QML tests
```

Run `just build-develop` after each change in the `data`, `i18n`, or `qml` directories.
This will *compile* everything into a Python file and move it into the `mpvqc` directory
where it will be picked up on app start.

If you're on Linux, and you're using PyCharm or something similar:
Create a run configuration that runs the `build-develop` recipe before starting the application.

# Internationalization

If you want to help translating this application into other languages, checkout the [guide](docs/internationalization.md).
Please feel free to open a new issue in case you need help.
