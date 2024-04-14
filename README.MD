# mpvQC

<img alt="Logo" src="data/icon.svg" width="128" height="128"/>

libmpv based application for the quick and easy creation of quality control reports of video files.  
Visit <a href="https://mpvqc.github.io">https://mpvqc.github.io</a> for downloads.

# Development Setup

This project assumes that a virtual environment is used:

* [Guide for Linux](docs/dev-setup-linux.md)
* [Guide for Windows](docs/dev-setup-windows.md)

We use `just` (https://github.com/casey/just) to build our application.

```shell
$ just --list
Available recipes:
    add-translation locale # Add new language
    build                  # Build full project into build/release
    build-develop          # Build and compile resources into source directory
    clean                  # Remove ALL generated files
    format                 # Format code
    lint-python            # Lint Python files
    lint-qml               # Lint QML files
    test                   # Run Python and QML tests
    test-python            # Run Python tests
    test-qml               # Run QML tests
    update-translations    # Update *.ts files by traversing the source code
```

Run `just build-develop` after each change in the `data`, `i18n`, or `qml` directories.
This will *compile* everything into a Python file and move it into the `mpvqc` directory
where it will be picked up on app start.

If you're on Linux, and you're using PyCharm or something similar:
Create a run configuration that runs the `build-develop` recipe before starting the application.

# Internationalization

If you want to help translating this application into other languages, please open a new issue :)

## Read Further

* Qt6: https://doc.qt.io/
* Python: https://www.python.org/
* PySide6: https://doc.qt.io/qtforpython/contents.html
* QML Coding Conventions: https://doc.qt.io/qt-6/qml-codingconventions.html
* Python & Qml: https://doc.qt.io/qtforpython/PySide6/QtQml/index.html
* Scripting: https://doc.qt.io/qt-6/topics-scripting.html
* Importing JavaScript Resources in QML: https://doc.qt.io/qt-6/qtqml-javascript-imports.html
* Qt, QtQuick & Python examples are located in `venv/lib/<python-version>/site-packages/PySide6/examples`
  after dev environment is set up completely
