# Ship Qt resources as a binary .rcc bundle

The standard `pyside6-project` flow compiles the qrc file into a generated Python module (~8.4 MB) that the application
imports at startup. Parsing that module cost ~100 ms per launch, paid in full on read-only deployments such as Flatpak,
where bytecode caches are absent. We compile the same qrc with `pyside6-rcc --binary` into a resource bundle (~2.9 MB)
instead and register it at startup with `QResource.registerResource()`, which costs almost nothing.

## Consequences

- Registration must run before the first `qrc:/` read. Startup reads build-info out of the bundle, so registering
  resources is the first thing the app does after path setup.
- Every packaging path must place the bundle next to the application entry point: the build recipe, the Nuitka
  data-file flag in the Windows release workflow, and the install line in the Flatpak manifest (packaging repo).
- The Python and QML test harnesses register their own staged bundle instead of importing a staged module.
