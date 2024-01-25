# Development Setup

* [Linux](dev-setup-linux.md)
* [Windows](dev-setup-windows.md)

This project assumes that a virtual environment is used.

# Internationalization

Please continue [here](internationalization.md).

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

# Just recipes

```shell
$ just --list
Available recipes:
    add-translation locale    # Allows adding additional languages
    build                     # Builds the project into build/release
    build-develop             # Builds the project. This will add all compiled resources into the Python source directory.
    clean                     # Removes ALL generated files
    lint-qml                  # Will run the linter against QML files
    test                      # Runs all Python and QML tests
    test-python               # Runs all Python tests
    test-qml                  # Runs all QML tests
    update-translations       # Traverses QML and Python files and updates translation files with new strings
```

# Workflow

Run `just build-develop` after each change in the `data`, `i18n`, or `qml` directories.
This will *compile* everything into a Python file and move it into the `mpvqc` directory
where it will be picked up on app start.

# Tips

* If you're on Linux, and you're using PyCharm or something similar:
  Create a run configuration that runs the `build-develop` recipe before the application.
