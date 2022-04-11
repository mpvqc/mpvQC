# mpvQC-qt6

## Development Setup

* [Windows](docs/developer/dev-env-windows.md)
* [Linux](docs/developer/dev-env-linux.md)

## Makefile targets

* `clean`  
  Cleans up all generated files


* `build`  
  Builds the project into build/mpvqc
* `build-clean`  
  Cleans up the build directory


* `develop-build`  
  Generates resources and copies them into the source directory.  
  This allows to develop/debug the project normally
* `develop-clean`  
  Cleans up the compiled resources in the source directory


* `test`  
  Runs all tests
* `test-clean`  
  Cleans up the compiled resources in the test directory


* `update-translations`  
  Traverses qml & .py files to update translation files
* `create-new-translation`  
  Allows to add translations to the project: make create-new-translation lang=<locale>

## Documentation

### Architecture

The architecture isn't cut in stone and will probably change once we include the mpv dependency. Currently, we have
**4** layers in this application:

* **QML Layer** is the user interface layer
* **PyObject Layer** is the glue layer of Python and Qml
* **Service Layer** is the application logic layer
* **Impl Layer** is the implementation layer for services

### Dependencies

* Dependency Injection: https://github.com/ivankorobkov/python-inject
