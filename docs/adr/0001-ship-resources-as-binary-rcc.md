# Ship Qt resources as a binary .rcc bundle

The standard `pyside6-project` flow compiles `project.qrc` into a generated Python module (`rc_project.py`, ~8.4 MB)
that the application imports at startup. Parsing that module cost ~100 ms per launch, paid in full on read-only
deployments such as Flatpak, where bytecode caches are absent. We compile the same `project.qrc` with
`pyside6-rcc --binary` into `project.rcc` (~2.9 MB) instead and register it at startup with
`QResource.registerResource()`, which costs almost nothing.

## Consequences

- Registration must run before the first `qrc:/` read. `perform_startup()` reads `:/data/build-info.toml`, so
  registering resources is the first thing `main()` does after path setup.
- Every packaging path must place `project.rcc` next to `main.py`: the `build` recipe in the `Justfile`, the Nuitka
  `--include-data-files` flag in `release.yml`, and the install line in the Flatpak manifest (`mpvQC-flatpak` repo).
- The test harnesses register staged copies (`test/project.rcc`, `testqml/project.rcc`) instead of importing a staged
  module.
